# AOF-R1-CF3

## QUALITY EVALUATOR COMPUTE COMPACTION

```text
AOF-R1-CF3

+ CF1 NATIVE COMPILE CONTRACT PRESERVATION
+ CF2 PACKED RESOURCE LIFETIME CONTRACT PRESERVATION
+ VH6 QUALITY / GPU / COMMIT QUALIFICATION CONTRACT PRESERVATION

+ EVAL-ONLY FROZEN-BATCH SINGLE PRODUCTION PER DATASET BATCH
+ TWO-RANK SAME-GPU FROZEN HIDDEN / ROOT EMBEDDING REUSE
+ BATCH-LOCAL ROOT-ID READBACK REUSE
+ SAME-SPLIT / SAME-ROW / SAME-HORIZON AUTHORITY
+ EVAL-ONLY LOSS-ONLY FULL-VOCAB TILED CE
+ NO UNUSED REPRESENTATION VJP IN EVALUATOR
+ SAME F32 LOGSUMEXP / FINITE / TILE / TARGET CONTRACT
+ RANK-PAIR RESIDENCY AND BOUNDED BATCH-LIFETIME ADMISSION
+ LEGACY / OBSERVE / ACTIVE EVALUATOR MODES
+ ROW-LOCAL PREDICTION AND DOCUMENT AGGREGATION PARITY
+ ACTUAL COMPUTE / TRANSFER / WAIT ATTRIBUTION

+ EXISTING HEAD CHECKPOINT RELOAD PRESERVATION
+ TRAINING SOURCE-DIGEST DOMAIN BYTE PRESERVATION
+ NO TRAINING VJP CHANGE
+ NO MODEL / HEAD WEIGHT CHANGE
+ NO FUTUREPOOL / PREFIX-COMMIT CHANGE
+ NO FUSED PRODUCTION PROMOTION
+ NO NUMERICAL THRESHOLD RELAXATION
+ NO UNSUPPORTED SPEEDUP CLAIM
```

## 0. Identity and evidence boundary

- Patch: `AOF-R1-CF3`.
- Parent code: `ASH_PASS3_AOF_R1_CF1_CF2_VH6_CODE_ONLY.zip`.
- Contract parents: `AOF-R1-CF1`, `AOF-R1-CF2`, `AOF-R1-VH6`.
- Next: `AOF-R1-CF4 PREFIX COMMIT TRANSFER ATTRIBUTION`.
- **2026-10-08 status:** SOURCE BAKED on the exact CF1/CF2/VH6 code-only parent; STATIC only. COMPILE/RUNTIME/PHYSICAL not executed. This specification and source bake are not physical PASS receipts.
- Parent `SOURCE/STATIC` is not equivalent to `COMPILE/RUNTIME/PHYSICAL`. Unrun parents remain `HOLD/NOT_RUN` even if CF3 source is baked.

## 1. Actual source diagnosis

**Native per-rank outer loop:** `crates/base_train/src/aof_r1_head_quality_native.rs:217-255`:

```text
for rank in [A, B]:
    for each held-out batch:
        owner.batch(labels)       # frozen forward + root select + embedding gather
        evaluate_frozen_head_batch(...)
        ...
    actual queue completion
```

**Evaluator:** `crates/base_train/src/aof_r1_head_quality_math.rs:33-99`:

- Calls `lm.select_roots(hidden)` again to read root IDs.
- Iterates valid rows; computes all four representations per active row, selects winners, then calls `lm.cross_entropy_vjp()` for each valid horizon.
- Reads one scalar CE per valid `(row, horizon)` and discards VJP.

**Frozen owner:** `crates/model_core/src/aof_r1_shared_lm_training_owner.rs:142-169`:

- `owner.batch()` itself selects roots and gathers selected-root embeddings, but its `into_training_parts()` returns only `(hidden, selected_root_embedding, labels, binding)`.
- Thus CF3 cannot honestly claim **zero** extra root-selection calls without changing this checkpoint-hashed training source.

**Tiled CE:** `crates/model_core/src/aof_r1_shared_lm_head_math.rs:250-339`:

- First tile pass computes stable full-vocab logsumexp, target logit, finite status, and CE.
- Second tile pass computes `(softmax-target)/N` representation gradient.
- EVAL ignores gradient. Whether a lazy backend actually executes every unused GPU operation is **UNKNOWN without GPU traces**.

## 2. Critical frozen checkpoint source-digest law

`shared_lm_training_source_digest()` (`model_core/src/aof_r1_shared_lm_head_math.rs:77-107`) hashes multiple training sources, including:

```text
model_core/src/aof_r1_shared_lm_head_math.rs
model_core/src/aof_r1_shared_lm_training_owner.rs
model_core/src/aof_r1_shared_lm_heads.rs
model_core/src/native_wgpu.rs
model_core/src/aof_r1_verification.rs
base_train/src/aof_r1_shared_lm_head_step.rs
base_train/src/aof_r1_shared_lm_head_training.rs
... additional listed sources ...
Cargo.lock
```

`ArkSharedLmCheckpoint::read()` compares manifest `training.source_digest` with the current function result. **CF3 SHALL NOT modify any file in that hash domain or alter that function's digest logic.** The complete inclusion list, not merely the examples above, is an exact static byte-preservation gate.

Forbidden:

- changing the current training digest to a literal old value;
- bypassing checkpoint source validation;
- silently accepting stale head manifests;
- rewriting/retraining checkpoints to conceal evaluator-only code changes.

Use new EVAL-only modules and existing public/crate-local accessors. If an optimization requires a change to hashed source, HOLD that optimization and isolate it as a separately approved checkpoint-lineage revision, not CF3.

## 3. Rank-pair batch loop inversion

Change **only the native evaluator's loop ownership**:

```text
load/validate head A and B against their original checkpoints and manifest seals
require actual same NativeWgpuModel, tokenizer, split and owner
validate pair-live residency

for batch_ordinal, held_out_labels in canonical order:
    owner.require_current()
    split.require_unchanged()
    frozen = owner.batch(held_out_labels)                # exactly once per batch
    (hidden_gpu, root_embedding_gpu, labels, binding) = frozen.into_training_parts()
    root_ids_host = owner.lm_atlas().select_roots(hidden_gpu).readback()  # once per batch
    for each [A, B] with its own trained head weights:
        evaluate same hidden/root/label/root_ids without regenerating frozen batch
        accumulate into rank-local horizon/document counters
    drop batch-local aliases only after both consumers and the GPU safety boundary

complete actual bound queue; verify both checkpoints and split remain current
emit the original two profile documents and final quality receipt
```

`root_ids_host` must originate in the same frozen atlas and model owner; it is never derived from future labels. **Structural target:** for B batches, `owner.batch` calls `2B -> B` and evaluator root-ID reads `2B -> B`. `owner.batch()` still performs one GPU root selection each time; do not claim `0` total root selection.

Do not cache hidden tensors for the entire evaluation split; batch-local bounded lifetime only. No hidden/root tensor D2H/H2D introduced. Existing per-row future representations and winner/tie behavior remain unchanged.

## 4. Rank-pair residency preflight

Current per-rank `shared_lm_head_budget()` checks do not prove that both rank heads fit concurrently. Calculate and validate **pair-live** bytes for:

- shared frozen model + LM and embedding atlas (count shared backing once);
- resident head A/B transform weights (both ranks and all four horizons);
- one frozen batch hidden/root embedding and maximum active-row head evaluation working set;
- evaluation loss-only tile scratch and pre-existing backend overhead;
- actual GPU device limits and provided `available_bytes`, `workspace_bytes`.

Use checked arithmetic. Never allocate two copies of the full vocab atlas. Borrow/clone *tensor handles* to the canonical immutable native tiles, not full tensor data. If the pair cannot be admitted, emit `HOLD_AOF_R1_CF3_RANK_PAIR_RESIDENCY` and do not silently degrade `ACTIVE` to the legacy rank-outer evaluator or CPU staging. `LEGACY` mode remains separately selectable.

## 5. Reused root IDs and target plan

Keep the existing generic `evaluate_frozen_head_batch()` compatibility API for CPU fixtures. Add an EVAL-only entrypoint accepting validated root IDs and the same `(hidden, selected_root_embedding, labels, binding)`.

- Validate root count == flattened batch rows, each ID within exact vocab range, same model and same `batch_ordinal`.
- Preserve `labels.targets(vocab_size)`, segment/eos/valid masks, +2/+3/+4/+5 offsets, and `(row, head)` ordering.
- Preserve the exact `next` boundary check and `root_matches_next_label` definition.
- Do not change tie-breaking: lowest global vocab ID on equal logits.
- Building one optional batch-local valid-target plan is allowed if its row/segment coverage equals the original target iterator exactly.
- No prediction count or document assignment change is admitted.

## 6. EVAL-only loss-only full-vocab CE

Create a **new**, separately hashed EVAL-only module, suggested:

```text
crates/model_core/src/aof_r1_head_quality_loss_only.rs        ADD
crates/model_core/src/lib.rs                                MOD (module registration)
crates/base_train/src/aof_r1_head_quality_math.rs            MOD (EVAL entrypoint)
```

Implementation must use the same immutable `NativeWgpuModel::aof_r1_vocab_atlas()` tile source and current model/queue/device identity. Construct a read-only quality projector (generic tile-math helper may be used for CPU fixtures) with **no second weight allocation or independent checkpoint authority**.

Loss-only forward performs **only the current first CE tile pass**:

```text
for canonical vocab tile in exact order:
    logits = representation × frozen tile.T
    same finite predicate / first failing tile attribution
    stable running max + running exp sum
    same target-tile gather and target-logit accumulation
loss = mean(max + log(sum) - target)
```

Preserve the existing `f32` operation order, logsumexp grouping, tile boundaries, labels, finite rejection, scalar-loss shape and per-horizon target count. **Do not execute the gradient second pass** or construct `representation_gradient` in the EVAL-only path. Keep the original `ArkFrozenLmAtlas::cross_entropy_vjp()` byte-identical for training.

No generic CPU numerical fallback in Native mode. If EVAL-only CE differs from canonical CE or cannot access the original tile authority, HOLD rather than modifying checkpoint-hashed training math or relaxing tolerances.

## 7. Strict evaluation parity

Same-source `LEGACY` and `COMPACT` shall produce identical:

```text
row/horizon observation identities and ordering
label, selected root, winner, root_matches_next_label
valid-target counts and per-document coverage
per-horizon correct counts and root strata
rank A/B checkpoint and split identities
loss finite/nonnegative checks
status values, acceptance semantics, stop conditions
```

For CE: retain identical canonical arithmetic and prefer exact `f32::to_bits()` comparison for same backend, tile order and input. **No existing project-wide CE tolerance has been established in this review**. If exact CE bits differ, report first mismatch and HOLD numerical parity pending explicit analysis; do not invent `atol/rtol` or silently promote approximate similarity. Preserve per-prediction accumulation order so existing `f64` aggregate math is unchanged when scalar CE bits match.

## 8. Modes and publication

Add an optional, default-preserving evaluation-only mode (in existing quality input with `deny_unknown_fields` handling):

```rust
#[derive(Clone, Copy, Debug, Default)]
enum ArkQualityEvalMode {
    #[default]
    Legacy,
    Observe,
    Active,
}
```

- `Legacy`: exact parent evaluator and output semantics. No CF3 performance claim.
- `Observe`: legacy path is quality authority; run bounded compact shadow against same frozen input; report first mismatch; never publish unqualified compact predictions.
- `Active`: compact path is evaluation authority **only after same-source parity and parent proof**. This is **not** inference production adoption or packed head activation.
- Preserve output `ash.aof_r1.head_quality.evaluation.v1` and existing consumer-visible horizon/profile/document keys; add only explicitly versioned diagnostic metadata. Update the historical `loss_recipe` description so it no longer falsely claims VJP execution in Active.
- Preserve file `create_new`/sync semantics. If rank-loop inversion changes *failure-time partial-file availability*, classify the change explicitly and ensure partial outputs never appear as accepted complete receipts.

## 9. Provenance and parent integration

Do not weaken `require_quality_head_pair()`, split manifest seal, the tokenizer/model binding, checkpoint weights digest, `owner.require_current()`, `split.require_unchanged()`, or final physical device/queue binding check. Both rank checkpoint files and manifests must be rechecked after the shared evaluation finishes.

Extend EVAL `eval_source_digest()` to include the new loss-only module and new evaluator code, without changing `shared_lm_training_source_digest()`. The existing VH6 integrator must consume the new quality result without claiming that a prior pre-CF3 source receipt qualifies this new source. Re-run same-source CF1 compile and applicable VH6 evidence when promoting CF3. CF2 lifetime and canonical commit logic remain untouched.

## 10. Exact source scope

| File | Scope |
|---|---|
| `crates/base_train/src/aof_r1_head_quality_native.rs` | Batch-outer/rank-inner loop, pair-budget admission, quality receipt |
| `crates/base_train/src/aof_r1_head_quality_math.rs` | root-ID-sharing quality entrypoint, loss-only callsite |
| `crates/model_core/src/aof_r1_head_quality_loss_only.rs` | New evaluation-only tiled CE projector |
| `crates/model_core/src/lib.rs` | Register new evaluation-only module |
| `crates/base_train/src/aof_r1_head_quality_tests.rs` | CPU negative/row parity fixtures |
| `crates/model_core/src/aof_r1_head_quality_loss_only_tests.rs` | New generic/full-vocab CE parity fixtures |
| `tools/validate_ash_aof_r1_cf3_quality_evaluator_compaction_static.py` | Source, digest and negative gates |
| Existing quality native CLI / VH6 integration | Only if required for optional mode/receipt compatibility |

Every file used by `shared_lm_training_source_digest()` MUST be byte-identical to the parent (including `Cargo.lock`). No refactor of production verifier, FuturePool, prefix commit, packed/fused shaders or learning/optimizer modules.

## 11. Measurement attribution

Record actual counters (not fabricated literal zeros):

```text
batch_count
rank_count
owner_batch_call_count
frozen_forward_call_count
frozen_root_selector_call_count
quality_root_selector_call_count
quality_root_readback_count
future_representation_call_count
winner_selector_call_count
ce_loss_only_call_count
ce_vjp_call_count
tile_forward_pass_count
tile_gradient_pass_count
scalar_loss_readback_count
host_alloc_bytes_observed (or UNKNOWN)
d2h_bytes_observed (or UNKNOWN)
queue_submission_count_observed (or UNKNOWN)
queue_wait_wall_ns_observed (or UNKNOWN)
backbone_wall_ns_observed (or UNKNOWN)
evaluator_wall_ns_observed (or UNKNOWN)
end_to_end_quality_wall_ns_observed (or UNKNOWN)
peak_gpu_residency_bytes_observed (or UNKNOWN)
```

Structural reduction is **not** measured GPU speedup. Unobserved fields must remain `null/UNKNOWN`, never `0` or `true`. Report model initialization and checkpoint loading time separately from per-batch evaluation time. Compare on the same GPU/model/tensor shapes/split/checkpoints/warmup/runtime configuration.

## 12. Negative fixtures

At minimum:

1. Two different trained ranks, identical frozen batch and head-order reversal produce per-rank identical predictions.
2. +2/+3/+4/+5 target coverage and offset ordering; masked/padded rows, sequence boundary, EOS, segment boundary.
3. Root greedy tie, including cross-tile equal-logit lowest-global-ID tie; root/label stratification.
4. Numerically stable extreme finite logits and target at first/last tile boundary; non-finite logits and CE must fail.
5. Root IDs wrong length/out of vocab/stale owner; no accidental labels-to-root selector path.
6. CE exact per-prediction parity and first mismatch attribution; no change to `cross_entropy_vjp()` VJP gradient tests.
7. Pair-resident budget overflow; no silent CPU fallback or second full-vocab allocation.
8. Split/change during evaluation; checkpoint/manifest tamper during either rank; fail closed.
9. Legacy/Observe/Active receipt correctness, failures and source seal; no premature partial success.
10. Original checkpoint still loads with the unchanged `shared_lm_training_source_digest()`.

## 13. Gates and native commands

**Source/static gate:** original training digest domain files byte-identical; source-only evaluator additions; all parent static gates applicable; two-rank single-batch path; no gradient second pass in loss-only module; strict split/checkpoint/finite checks; no admission/policy drift.

After exact vendor workspace path is restored, compile against real manifests:

```powershell
cargo metadata --format-version 1 --locked
cargo check -p model_core --lib --release --locked -j 1
cargo check -p base_train --lib --release --locked -j 1
cargo check -p base_train --bin ash_aof_r1_frozen_heads_quality --release --locked -j 1
cargo test -p model_core --lib aof_r1_head_quality_loss_only --release --locked -j 1
cargo test -p base_train --lib aof_r1_head_quality --release --locked -j 1
```

Run same-source native quality twice via the already declared binary CLI:

```powershell
cargo run -p base_train --release --locked --bin ash_aof_r1_frozen_heads_quality -- path/to/legacy_run.json
cargo run -p base_train --release --locked --bin ash_aof_r1_frozen_heads_quality -- path/to/observe_or_active_run.json
```

The two run inputs require separate `output` directories (existing `create_new` policy) and otherwise identical exact content, except evaluation mode. The actual native model, real head checkpoint A/B, split manifest, and GPU must be used. Re-run applicable VH6 legs under the new evaluator source if claiming VH6 continuity. No run shown above has been executed by this specification.

## 14. Receipt

Emit `aof_r1_cf3_quality_evaluator_compute_compaction_receipt.json` with:

```text
schema = ash.aof_r1.cf3.quality_evaluator_compute_compaction.v1
parent_source_digest / current_source_digest
training_source_digest_before / training_source_digest_after
training_digest_unchanged
quality_evaluator_source_digest
cf1 / cf2 / vh6 parent evidence references and states
model / tokenizer / split / checkpoint A-B hashes
GPU device/queue binding
mode (Legacy | Observe | Active)
row_horizon_parity / per_document_parity / CE_bits_parity
actual observability counters
physical_status / performance_status
failure_class / first_mismatch
production_admission = false
promoted = false
receipt_hash / pass_token
```

Use the existing audit JSON hashing conventions, not a hand-filled PASS token. `performance_status=NOT_MEASURED` unless a controlled physical A/B ran.

## 15. Failure classes

```text
FAIL_AOF_R1_CF3_TRAINING_SOURCE_DIGEST_DRIFT
FAIL_AOF_R1_CF3_CHECKPOINT_INCOMPATIBLE
FAIL_AOF_R1_CF3_RANK_PAIR_IDENTITY_DRIFT
HOLD_AOF_R1_CF3_RANK_PAIR_RESIDENCY
FAIL_AOF_R1_CF3_ROOT_ID_CURRENTNESS
FAIL_AOF_R1_CF3_ROOT_LABEL_CONTAMINATION
FAIL_AOF_R1_CF3_TARGET_COVERAGE_DRIFT
FAIL_AOF_R1_CF3_ROW_OR_DOCUMENT_DRIFT
FAIL_AOF_R1_CF3_WINNER_OR_TIE_DRIFT
FAIL_AOF_R1_CF3_CE_BITS_DRIFT
FAIL_AOF_R1_CF3_NONFINITE_GATE_DRIFT
FAIL_AOF_R1_CF3_VJP_SURVIVED_EVAL_LOSS_ONLY
FAIL_AOF_R1_CF3_OWNER_DEVICE_QUEUE_DRIFT
FAIL_AOF_R1_CF3_OUTPUT_OR_RECEIPT_PARTIAL_PROMOTION
FAIL_AOF_R1_CF3_NATIVE_COMPILE
HOLD_AOF_R1_CF3_PARENT_PHYSICAL_EVIDENCE_MISSING
HOLD_AOF_R1_CF3_PERFORMANCE_NOT_MEASURED
```

## 16. Completion law

`PASS_AOF_R1_CF3_QUALITY_EVALUATOR_COMPUTE_COMPACTION` may be issued **only** with:

```text
SOURCE: bounded rank-shared native frozen batch and eval-only loss-only path exists
STATIC: all files in training-source-digest domain unchanged; parent gates PASS
COMPILE: native model_core + base_train + actual quality binary PASS
RUNTIME: old/new per-row, horizon and document equality; checkpoint compatibility PASS
PHYSICAL: same actual WGPU device, exact head checkpoints, frozen batch reused,
          full-vocab eval-only CE exercised, no VJP second pass on evaluator route,
          no premature resource reuse, current owner/queue retained
PARENT: same-source required CF1/CF2/VH6 physical evidence actually verified
```

The following **do not** follow from CF3 acceptance and must remain independently unpromoted:

```text
GPU faster by X%
D2H eliminated
full rank-pair residency feasible for all configurations
inference packed/fused production enabled
head quality improved by optimizer change
prefix commit copy or wait eliminated
```

## Final invariant

```text
ONE ACTUAL FROZEN BATCH PER EVAL BATCH
+ TWO TRAINED RANKS SHARE THE SAME GPU HIDDEN/ROOT EMBEDDING
+ ONE EVAL ROOT-ID READBACK PER BATCH
+ FIRST-PASS ONLY FULL-VOCAB CE FOR QUALITY
+ EXACT TRAINING CHECKPOINT SOURCE DIGEST PRESERVED
+ EXISTING QUALITY / VH6 / COMMIT MEANING PRESERVED
+ VERIFIED NATIVE-PHYSICAL EVIDENCE
= AOF-R1-CF3 QUALITY EVALUATOR COMPACTION CLOSED
```
---

## 17. 2026-10-08 exact SOURCE bake annex (supersedes §10 file delta only)

Parent code-only SHA-256: `0311b820ca40ed304c8e24d7de0b0b7b62cd7784b277b2e2cfab6e4c45bdba32`.

SOURCE delta: **ADD 4 / MODIFY 4 / DELETE 0**, full code-only 8,715 files, archive SHA-256 `52eb9126da1b35787cdd7ed8e1435d1c749a0bc7dea4a48855a53fd5b693fa01`. CRC verified.

Actual added paths:
- `crates/base_train/src/aof_r1_head_quality_compact.rs`
- `crates/model_core/src/aof_r1_head_quality_loss_only.rs`
- `crates/model_core/src/aof_r1_head_quality_loss_only_tests.rs`
- `tools/validate_ash_aof_r1_cf3_quality_evaluator_compaction_static.py`

Actual modified paths:
- `crates/base_train/src/aof_r1_head_quality_native.rs`
- `crates/base_train/src/aof_r1_head_quality_tests.rs`
- `crates/base_train/src/lib.rs`
- `crates/model_core/src/lib.rs`

**Deliberate scope refinement:** `aof_r1_head_quality_math.rs` remains *byte-identical*, with the existing legacy evaluator as comparison authority. The separate `aof_r1_head_quality_compact.rs` implements the new rank-pair consumer and strict row/winner/CE-bit comparator; the new model-core evaluation-only atlas duplicates only the canonical CE *first* tile pass and borrows the same native frozen vocab Tensor handles. No training gradient-second-pass code or checkpoint-hashed training source was modified. This narrows rather than expands the §10 requested changes.

Training source digest was recomputed from all 19 exact `shared_lm_training_source_digest()` byte inputs and is unchanged:
`e20f93b19bcb8a93a96809a28d2faf5c72c68896da060002d36a43e2286b8283`.
No legacy checkpoint digest bypass, synthetic checkpoint or model/tile data copy was added.

**Evaluation modes:** `LEGACY` remains the default. `OBSERVE` runs the compact and legacy consumers on one actual frozen batch per dataset batch, publishes the legacy quality values, compares `f32::to_bits` for every valid row/horizon, and records the first drift. `ACTIVE` requires same-source sealed OBSERVE proof plus CF3 static, actual CF1 compile, full CF2 numerical-rejection physical retirement and VH6 physical receipt binding. The existing forced WGPU-copy early-exit canary does **not** qualify a learned-head numerical rejection. Absent proof => HOLD; no implicit mode fallback. Compact evaluation uses one extra batch-local root-ID readback (the legacy shadow in OBSERVE performs its own readback, separately accounted).

The pair-resident guard counts frozen model/backbone once, sums both rank-head weights with checked arithmetic and reserves existing workspace once. It is a conservative **logical** bound, *not* observed physical VRAM usage. The source rechecks input hashes and original checkpoint/seal identities before any compact rank profiles are published. New `aof_r1_cf3_quality_evaluator_compute_compaction_receipt.json` is evaluation-only and does not promote inference.

**Verification results as of authoring:**
- CF3 SOURCE/STATIC: **51/51 PASS**
- Parent CF1/CF2/VH6 STATIC: **52/52 PASS**
- Negative static perturbations: training-source byte drift, CE bitwise predicate removal and first-pass logsumexp expression drift were each rejected; files restored before packaging.
- Archive CRC: PASS
- `cargo`/`rustc` unavailable in packaging environment; exact external sherpa-rs workspace input absent from code-only parent.
- Rust COMPILE: NOT_RUN; CPU/RUNTIME: NOT_RUN; real GPU PHYSICAL: NOT_RUN; measured speedup: UNKNOWN.
- No CF3 full PASS token has been observed. Same-source parent CF1 and VH6 physical campaigns must be re-executed before qualifying ACTIVE.
- No changes to FuturePool, prefix-commit, packed/fused production, training optimizer or tolerance policies.

The reported static PASS applies only to the stated source patterns and exact hashed files, not to Rust compilation, tensor numerics, physical residency, real model quality or performance.

## 18. Next real execution authority

```powershell
cargo metadata --format-version 1 --locked
cargo check -p model_core --lib --release --locked -j 1
cargo check -p base_train --lib --release --locked -j 1
cargo check -p base_train --bin ash_aof_r1_frozen_heads_quality --release --locked -j 1
cargo test -p model_core --lib aof_r1_head_quality_loss_only --release --locked -j 1
cargo test -p base_train --lib aof_r1_cf3 --release --locked -j 1
```

Then run exact two-rank real NativeWGPU `LEGACY` and `OBSERVE` on the same split/checkpoints/dataset and establish first-drift-free row/horizon/document CE parity. Resume CF1/CF2/VH6 physical admission on the changed source before `ACTIVE`.

**Completion claim stays HOLD until these external steps pass.**
