# HEADWISE-R3-CF4
## CURRENT-SOURCE SHARED-LM HEAD CHECKPOINT LINEAGE + HELD-OUT QUALITY QUALIFICATION

**Patch ID:** `HEADWISE-R3-CF4`  
**Parent source:** `ASH_PASS3_HEADWISE_R3_CF3_SELECTED_PRODUCTION_OUTPUT_CANONICAL_REFERENCE_QUALIFICATION_CODE_ONLY.zip`  
**Parent specification:** `HEADWISE-R3-CF3 SELECTED PRODUCTION OUTPUT CANONICAL-REFERENCE QUALIFICATION`  
**Successor:** `HEADWISE-R3-CF5` original W8/W9A same-invocation physical join; independent `HEADWISE-R3-CF3-PHYS` selected-output campaign.  
**Class:** exact head-training source identity, two fresh candidate checkpoints, held-out quality, native load/forward, bounded evidence.  
**Status (2026-10-09): PARTIAL SOURCE BAKE / CF4 STATIC 35/35 PASS, 33/33 negative mutations rejected; CF3 32/32 and CF2 41/41 parent STATIC preserved.** Rust COMPILE, Naga, native checkpoint training, WGPU held-out quality, actual prefix sidecar and PHYSICAL are **NOT_RUN / HOLD**. No product promotion; see section 24 SOURCE bake annex.

```text
HEADWISE-R3-CF4

CURRENT-SOURCE SHARED-LM HEAD CHECKPOINT LINEAGE
+ CF3 EXACT SOURCE BASELINE / 19-INPUT TRAINING-DIGEST RECOMPUTATION
+ CF2 NATIVE_WGPU SOURCE-CHANGE CONSEQUENCE PRESERVATION
+ NO OLD CHECKPOINT MANIFEST RESEAL
+ EXISTING FROZEN-BACKBONE SHARED-LM HEAD-ONLY TRAINER REUSE
+ TWO PREDECLARED DISTINCT RANK CANDIDATES
+ EXACT TOKENIZER / DATASET / MODEL BINDING
+ TRAIN / HELD-OUT DOCUMENT-LEVEL PARTITION
+ FRESH CHECKPOINT BYTES + ORIGINAL TRAINER MANIFEST
+ ORIGINAL STEP / DATASET / WEIGHT / SOURCE PROVENANCE
+ NATIVE CHECKPOINT READ / ACTUAL WGPU LOAD + FORWARD
+ EXISTING TWO-RANK HELD-OUT QUALITY EVALUATOR REUSE
+ FUTURE OFFSETS +2 / +3 / +4 / +5 PER-RANK OBSERVATIONS
+ TEACHER-FORCED QUALITY != RUNTIME PREFIX ACCEPTANCE
+ ACTUAL PREFIX ACCEPTANCE SIDECAR AS INDEPENDENT GATE
+ SOURCE / STATIC / COMPILE / RUNTIME / PHYSICAL / QUALITY / LINEAGE SEPARATION
+ NO TRAINER / MODEL MATH / CHECKPOINT ABI CHANGE
+ NO CF3 SELECTED-OUTPUT OR CF2 W8/W9A PHYSICAL AUTO-PASS
+ NO DEFAULT ROUTE OR CF5-D ACTIVE PROMOTION
```

---

## 0. Exact evidence baseline

**CONFIRMED / SOURCE from the CF3 parent and its bake annex:**

1. CF3 SOURCE/STATIC: `32/32 PASS`; negative source mutations `25/25 REJECTED`. CF2 STATIC: `41/41 PASS`, negatives `26/26 REJECTED`. These are *source/static* results only.
2. The full CF3 artifact SHA-256 is `57d4fbc0fa223cddbfed097f49f068f5b297fce24393553043ac18dd3beeeb2c`; entry count `8,752` and ZIP CRC PASS, per the parent annex.
3. The exact 19-input `shared_lm_training_source_digest()` under CF2 and CF3 is `0b10d1d645ce22356ca4c44bc9e0e4c4ef109f6daf9d143175cd5c9cc1a41094`. The prior training-source digest is `e20f93b19bcb8a93a96809a28d2faf5c72c68896da060002d36a43e2286b8283`.
4. `crates/model_core/src/aof_r1_shared_lm_head_math.rs::shared_lm_training_source_digest()` hashes **19 exact inputs**, including `native_wgpu.rs`, `aof_r1_shared_lm_head_training.rs`, `bin/ash_aof_r1_frozen_heads_train.rs`, tokenizer sources, `decode_runtime_binding.rs`, and `Cargo.lock`.
5. `crates/base_train/src/bin/ash_aof_r1_frozen_heads_train.rs` already accepts `--describe-input` or exactly one `<run.json>` and selects the shared-LM trainer only when `shared_lm_training` is present.
6. `crates/base_train/src/aof_r1_shared_lm_head_training.rs` validates the rank, resource budget, tokenizer/binding, targets, optimizer steps and output nonexistence; it writes a new `.safetensors` plus `.head-manifest.json`, with manifest `training.source_digest`, trained weight SHA and `state=head_only_trained_candidate`.
7. `crates/base_train/src/bin/ash_aof_r1_frozen_heads_quality.rs` accepts `--describe-input` or a quality run JSON. The native evaluator requires **exactly two** comparable shared-LM heads and document-level train/eval split provenance.
8. The native quality evaluator supports `LEGACY`, `OBSERVE`, and `ACTIVE`; `ACTIVE` requires its own prior same-source/physical proof set. Its `runtime_prefix_quality` remains `REQUIRES_CURRENT_PROFILE_CAMPAIGN_ACCEPTANCE_SIDECAR`.
9. CF3 kernel fixture remains `kernel_fixture_only=true`; `live_session_qualified=false`, and W8/W9A `physical_join_qualified=false`. CF3 COMPILE/NAGA/PHYSICAL remain `NOT_RUN` in the available annex.

**UNKNOWN:** whether any valid new-lineage trained checkpoint currently exists outside this archive; whether the exact native Windows workspace compiles; WGPU execution, future-offset quality, prefix acceptance, and Headwise speedup. A result must never be promoted from UNKNOWN because a file path or hash string looks plausible.

---

## 1. Purpose and independent result domains

CF4 closes one specific gap: **real new-source head-only checkpoint creation and objective evaluation** after CF2 modified `native_wgpu.rs`.

Maintain four distinct axes:

```text
TrainingSourceLineage  : NotRecomputed | ExactCurrent | Changed | Invalid
CheckpointMaterialized: NotRun | FreshBytesWritten | Validated | Failed
TeacherForcedQuality  : NotRun | Measured | Insufficient | Failed
RuntimePrefixQuality  : NotRun | Measured | Insufficient | Failed
```

Also retain independently:

```text
CF3SelectedOutputPhysical : HOLD unless separately observed
CF2W8W9APhysicalJoin     : HOLD unless separately observed
GlobalHeadwiseProduction : DISABLED / not promoted
```

No `quality PASS` may be used to synthesize `checkpoint lineage PASS`; no training loss reduction grants quality promotion. Conversely, an actual checkpoint-lineage PASS need not depend on CF3's independent scalar-reference exact-f32 comparison.

## 2. Strict non-goals

CF4 does **not** modify attention score math, TextDensity multipliers, R2 chunked causal mask, head optimizer recipe, shared-LM gradient path, backbone weights, AOF FuturePool acceptance, W9A routing, selected Headwise kernels, canonical KV/token/stop/emit, or CF5-D ACTIVE.

It does **not** create a new general training framework, relax existing validation, or synthesize migration evidence for old checkpoint files.

**No semantic change to the current 19-input training source set is authorized in CF4.** If a required repair touches one of those inputs, classify as source-lineage-changing work and issue a separate, explicit revision; never preserve the old digest label over different source bytes.

---

## 3. P0 exact build and source preflight

Before **claiming** COMPILE, checkpoint training or native PHYSICAL:

- Confirm the CF3 full artifact exact SHA, the exact `Cargo.lock`, WGPU 26 vendor graph, and the two current source-digest functions.
- Restore missing external `vendor/sherpa-rs-main/crates/sherpa-rs` from its *actual authorized source*. No dummy crate, path deletion, version substitution, or silent lock update.
- Recompute all 19 training input hashes using the **actual Rust source-digest definition**. Compare the aggregate digest against `0b10d1d645ce22356ca4c44bc9e0e4c4ef109f6daf9d143175cd5c9cc1a41094` only when the exact parent bytes remain unchanged.
- Verify that CF4 qualification-only new files do not accidentally enter the 19-input domain. If they must, recalculate the resulting new lineage and hold compatibility with both old and CF2 hashes until explicitly admitted.
- Distinguish the head-training source digest, `ark_runtime_source_digest`, binary SHA-256, checkpoint SHA-256, and quality-evaluator source digest. One is not a substitute for another.
- Run actual `cargo metadata --locked`, release compilation, and the selected native binary before marking anything COMPILE/RUNTIME.

CF3's separate reference-shader Naga and selected-output GPU campaign may run in parallel. They are **not inferred from head training**. If their gates remain unresolved, preserve separate HOLD fields rather than blocking truthful reporting of independently materialized checkpoints.

## 4. Actual existing CLI authority

The trainer is **already present**:

```text
crates/base_train/src/bin/ash_aof_r1_frozen_heads_train.rs
    --describe-input
    <one run.json>
```

The quality evaluator is **already present**:

```text
crates/base_train/src/bin/ash_aof_r1_frozen_heads_quality.rs
    --describe-input
    <one quality-run.json>
```

The quality/profile-campaign handoff already appears in:

```text
crates/orchestrator_local/src/bin/ash_aof_r1_cf7_cf8_cf9_gate.rs
```

Do not invent a `--rank`, `--epochs`, `--checkpoint`, or `--resume` CLI switch on the existing binaries. Pass the fields via the described JSON inputs. Do not invoke the dense legacy trainer as if it were the shared-LM head-only training recipe.

## 5. Predeclared two-rank candidate manifest

The campaign MUST freeze its two ranks **before any training or evaluation**:

```text
rank_a : explicit integer
rank_b : explicit, different integer
0 < rank_a, rank_b < actual hidden_size
```

Use exactly the same:

```text
frozen backbone + source checkpoint set
model spec + tokenizer manifest + optional tokenizer model
encoded training dataset bytes
training seed
training epochs / learning rate
optimizer recipe and target/offset policy
resource-accounting method
```

Only the declared `shared_lm_training.rank` and its resulting head allocation may vary between candidate arms, unless the difference is explicitly labeled as a separate experiment.

The same seed does not guarantee mathematically identical initialization across distinct rank tensor shapes. Report matched configuration, not an invented controlled-causal rank experiment.

**No rank value or quality threshold is chosen by this specification.** The campaign owner must select and seal them before seeing outcomes. If no valid rank pair or acceptance policy exists, mark `HOLD_CF4_RANK_PAIR_OR_QUALITY_POLICY_UNBOUND`.

## 6. Frozen dataset/encoder authority

The actual trainer uses `ArkHeadDataset::load(...)` and the existing tokenizer/binding checks. The quality evaluator uses `ArkLoadedHeadQualitySplit::load(...)`.

Required:

- Training dataset is produced from the exact text sources with the intended tokenizer encoder (`tools/aof_r1_tokenizer_gate: encode-dataset` is the existing producer reference).
- Numeric-only fabricated datasets must not be accepted as native encoded source lineage.
- Use the quality split manifest's exact `train_dataset`, `eval_dataset`, `train_sha256`, `eval_sha256`, document hashes and UTF-8 segment ranges.
- Train/eval partition at **parent-document identity**, not merely at batch row index. Preserve source/segment byte coverage and reject documented overlaps.
- Both rank checkpoints' `dataset_digest` equal the *actual train dataset hash* expected by the quality split.
- Eval documents/prompt choices are frozen before candidate training. Neither rank may choose its own advantageous held-out subset.
- A missing or unsupported document-leakage proof means the corresponding broader no-leakage claim is UNKNOWN; do not invent full corpus deduplication.

## 7. Actual training contract

For each rank, use the shared-LM path:

```rust
// Contract illustration: the fields already exist in the SOURCE Run structs.
// This is not new implementation code or a runnable JSON example.
Run {
    model_spec: PathBuf,
    checkpoints: Vec<PathBuf>,
    tokenizer_manifest: PathBuf,
    tokenizer_model: Option<PathBuf>,
    dataset: PathBuf,
    output: PathBuf, // new .safetensors target, distinct per rank
    training: ArkHeadTrainingConfig {
        epochs: usize,
        learning_rate: f64,
        seed: u64,
        available_bytes: u64,
        frozen_backbone_bytes: u64,
        workspace_bytes: u64,
    },
    shared_lm_training: Some(ArkSharedLmHeadTrainingOptions {
        recipe: String, // exact ARK_SHARED_LM_HEAD_RECIPE constant
        rank: usize,     // predeclared rank A or B
    }),
}
```

The native executable accepts the **JSON serialization** of those existing fields. Obtain the actual schema via `--describe-input` and use real paths, numbers, resource budgets and recipe constant; do not manufacture values. The Rust-like block above is notation, **not** code to insert into the repository.

Do not add `checkpoint_resume`, existing-weight injection, source-hash override, or permissive feature defaults.

Required runtime observations:

```text
real decoded dataset and target cardinalities for +2,+3,+4,+5
completed_epochs and completed_steps
valid_targets[4]
initialization_digest and weights_digest
training_batch_chain_digest
finite recorded loss observations
actual owner/currentness and queue completion evidence where supplied
output publication success, with no partially admitted checkpoint
```

`last_loss < first_loss` is a diagnostic, **not** sufficient for checkpoint or quality promotion. Any gradient/stability counters absent from the actual trainer must remain UNKNOWN, not invented zeros.

## 8. Memory, residency and concurrency

The trainer already checks frozen-model residency and workspace budgets. Preserve the existing equations and failure classes.

- Record the actual `available_bytes`, `frozen_backbone_bytes`, `workspace_bytes`, hidden size, vocabulary size, rank, largest batch rows and LM-atlas tile constraints.
- Retain frozen backbone and shared LM-atlas source; no new full-model gradient or optimizer state.
- Train candidates in separate fresh output roots and with independent runtime session/currentness, rather than reusing mutable head optimizer state.
- Do not automatically run simultaneous two-rank GPU training merely because the evaluation needs a rank pair. Physical OOM/memory budget must be observed.
- Do not erase a failed run or its partial `.writing` files while reporting success. Fresh retry uses explicit new output identity or the existing documented transaction recovery semantics.

## 9. Checkpoint publication and byte integrity

The original trainer publishes a candidate `.safetensors` and its sibling `.head-manifest.json` through its existing authority. Preserve `publish_shared_lm_checkpoint()` and all ordering/seal semantics.

For each candidate record:

```text
checkpoint_path / actual SHA-256
head_manifest_path / actual SHA-256
manifest.abi / recipe / offsets / rank
manifest.binding (hidden, vocab, model/tokenizer relations)
manifest.state = head_only_trained_candidate
manifest.completed_steps / training.completed_epochs
manifest.dataset_digest / training_batch_chain_digest
manifest.initialization_digest / initialization_seed
manifest.optimizer_recipe / learning_rate
manifest.training.source_digest
manifest.weights_digest / manifest.seal
```

Verify SHA-256 from **actual file bytes**, not receipt strings. Validate manifest seal and checkpoint deserialization through the existing canonical `ArkSharedLmCheckpoint::read`/manifest validation path.

No manifest rewriting after training. No rename that hides an incomplete transaction. No replacing old checkpoint bytes under a new digest.

## 10. Exact 19-input lineage gate

Recompute the actual training source digest immediately before each rank starts and after all candidate outputs have been published.

```text
training source before == training source after
training source in rank A manifest == actual current source
training source in rank B manifest == actual current source
training source in both ranks == same exact manifest-authorized digest
```

If the supplied parent source bytes are unchanged, the required digest is:

```text
0b10d1d645ce22356ca4c44bc9e0e4c4ef109f6daf9d143175cd5c9cc1a41094
```

If any hashed input differs, `HOLD_CF4_TRAINING_SOURCE_LINEAGE_DRIFT`, even if binaries compile and `source_digest` strings were copied. The old `e20f93...` checkpoint remains a separate immutable reference arm, not a candidate with a resealed manifest.

## 11. Independent native checkpoint load/forward

After checkpoint publication, re-open each candidate from disk in a **new native evaluation session**:

1. Verify the original backbone model/spec and tokenizer runtime binding from actual files.
2. Read and verify `.safetensors` + `.head-manifest.json` and expected rank.
3. Instantiate the actual `NativeWgpuModel`/frozen shared-LM owner and validate its current physical binding.
4. Load the candidate head through the existing model/head loader and execute at least one finite native forward/evaluation batch.
5. Bind checkpoint weight SHA, manifest seal, model binding, runtime source and executed binary identity to that session's receipt.
6. Observe actual device/queue completion and output cardinality. Missing callback/currentness is HOLD, not a success-shaped zero.

A host-only `ArkSharedLmCheckpoint::read` proves byte/schema validity, **not** real WGPU execution. A successful teacher-forced WGPU quality run may satisfy native load/forward only to the extent its actual telemetry proves these events.

## 12. Teacher-forced held-out quality

Use the existing `ash_aof_r1_frozen_heads_quality` native evaluator, with its `heads` array of **exactly two** rank inputs and pre-sealed quality split manifest.

Required per rank and per offset `+2,+3,+4,+5`:

```text
held-out valid-target denominator
correct predicted target count / accuracy
cross-entropy or native reported loss metric
model/root-conditional counts where actually reported
per-document result and dataset membership
head rank and checkpoint SHA/source digest
finite output status and actual queue completion
```

Do not substitute training loss for held-out accuracy. Do not treat zero targets as 100% success. Record denominator zero as `NO_VALID_TARGETS / UNKNOWN`, not a fabricated metric.

The evaluator's `LEGACY` or `OBSERVE` mode can provide measured teacher-forced evidence with its actual provenance. `ACTIVE` is valid **only** if its own existing proof inputs pass; CF4 is not allowed to forge CF1/CF2/VH6 acceptance receipts merely to get an ACTIVE status.

If a numerical/parity mismatch occurs in `OBSERVE`, retain that observation and classify it explicitly, not as accepted ACTIVE.

## 13. Runtime prefix acceptance is a separate authority

Teacher-forced offset accuracy is not prefix acceptance. The existing native quality result explicitly requires a **current profile-campaign acceptance sidecar** for runtime prefix quality.

When the actual `ash_aof_r1_cf7_cf8_cf9_gate` profile campaign and acceptance telemetry are available, bind:

```text
same rank/checkpoint SHA/model/tokenizer/eval prompt
same native runtime/source/binary identity
same accepted-depth policy and candidate/verify ownership
actual emitted, attempted and accepted prefix-token counts
cold/streaming denominators where distinguished by the existing source
EOS/stop/cancel/emit-failure results and commit provenance
```

Record prefix acceptance by actual depth, horizon and rank only when the source emits those denominators. Do not infer a prefix acceptance rate from teacher-forced CE/accuracy, from a non-promoted sidecar, or from W9A's routing decision.

If the profile campaign is not executed, output:

```text
RuntimePrefixQuality = NotRun
quality promotion = HOLD
```

**No threshold is introduced to disguise an open quality problem.** Selection criteria must have an approved, frozen source before the relevant outcomes are inspected.

## 14. Rank comparison and decision policy

A two-rank comparison produces a table, not an automatically chosen winner:

| Field | Rank A | Rank B |
|---|---|---|
| Actual rank | measured/declared | measured/declared |
| Training lineage | exact / failed | exact / failed |
| Checkpoint digest and native load | observed / hold | observed / hold |
| Valid targets +2,+3,+4,+5 | observed / unknown | observed / unknown |
| Held-out CE and accuracy by offset | observed / unknown | observed / unknown |
| Per-document/conditional results | observed / unknown | observed / unknown |
| Runtime prefix acceptance | measured / NOT_RUN | measured / NOT_RUN |
| Decode token/stop/KV parity | measured / NOT_RUN | measured / NOT_RUN |
| GPU memory and latency | measured / NOT_MEASURED | measured / NOT_MEASURED |

Required interpretations:

- `CHECKPOINT_LINEAGE_QUALIFIED` may be true with no claim that the checkpoint is good.
- `TEACHER_FORCED_QUALITY_MEASURED` does not mean prefix quality or production readiness.
- `RUNTIME_PREFIX_QUALITY_MEASURED` requires actual verified/commit telemetry, not inferred acceptance.
- `RANK_ADOPTED` remains false absent an authorized frozen quality decision rule and later global admission gates.

## 15. Audit-only typed receipt proposal

Proposed qualification-only schema (not a claim that this type exists):

```rust
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum HeadwiseR3Cf4LineageState {
    NotRun,
    SourceExact,
    CheckpointMaterialized,
    CheckpointBytesValidated,
    NativeForwardObserved,
    Failed,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum HeadwiseR3Cf4QualityState {
    NotRun,
    TeacherForcedMeasured,
    RuntimePrefixMeasured,
    Hold,
    Failed,
}
```

A receipt SHALL include nullable/typed values for:

```text
schema_revision, source_tree_digest, Cargo.lock digest, native_binary_sha256
training_source_digest / full 19-input manifest
quality_evaluator_source_digest / runtime_source_digest (where actually read)
model_spec_digest, tokenizer_manifest/model digest, backbone checkpoint SHA set
train dataset digest, eval dataset digest, split seal and document membership
rank pair, training hyperparameters and budgets
checkpoint byte SHA + manifest SHA + manifest seal (each candidate)
completed_steps/epochs/valid_targets/initialization/optimizer recipe
native checkpoint load + forward/Queue completion evidence
+2/+3/+4/+5 per-rank teacher-forced measurements and denominators
per-rank prefix acceptance sidecar identity or NOT_RUN
first failure class, attempted stage and terminal state
CF3 physical status and CF2 W8/W9A join status (independently bound)
lineage_qualified, teacher_forced_measured, runtime_prefix_measured
quality_adopted=false, production_promoted=false, CF5_D_ACTIVE=false
receipt_sha256 over actual canonical serializable audit content
```

A disk receipt is **audit evidence**, not a reusable live GPU pointer, an optimizer resume token, or WGPU-lease ownership.

## 16. Run state machine and once-only publication

```text
Declared
  → SourcePreflight
  → DatasetAndBudgetAdmitted
  → RankATraining → RankACheckpointValidated
  → RankBTraining → RankBCheckpointValidated
  → NewNativeModelLoaded
  → HeldOutQualityMeasured
  → [RuntimePrefixMeasured | RuntimePrefixNotRun]
  → ScopedAuditReceiptPublished
```

Any failed transition becomes a typed `HOLD/FAIL`, with first source stage. No automatic retry against existing output paths; no mutable checkpoint overwrite; no `ZeroError` default for unrun physical legs. Existing checkpoint and optimizer publication transactions remain authoritative.

## 17. Narrow source touch points

**Prefer zero changes to all 19 hashed training inputs.** Reuse the existing binaries and their public APIs. Only when necessary, add a small qualification/audit wrapper outside that hash domain.

Existing source owners to *call/inspect*, not automatically modify:

```text
crates/model_core/src/aof_r1_shared_lm_head_math.rs
crates/base_train/src/bin/ash_aof_r1_frozen_heads_train.rs
crates/base_train/src/aof_r1_shared_lm_head_training.rs
crates/base_train/src/aof_r1_shared_lm_head_step.rs
crates/base_train/src/aof_r1_frozen_head_training.rs
crates/base_train/src/aof_r1_head_quality_native.rs
crates/base_train/src/bin/ash_aof_r1_frozen_heads_quality.rs
crates/orchestrator_local/src/bin/ash_aof_r1_cf7_cf8_cf9_gate.rs
```

Optional **proposed** new wrapper:

```text
crates/orchestrator_local/src/headwise_r3_cf4_checkpoint_lineage.rs
```

Use the existing Rust CLI for actual training and evaluation. A new Python/PowerShell checkpoint loader or trainer is **out of scope**. Avoid editing `native_wgpu.rs` or `Cargo.lock` for receipt convenience. If qualification wiring legitimately requires changes to a hashed input, stop and explicitly re-open the training source-lineage contract instead of quietly broadening CF4.

## 18. Required negatives / first-failure classes

At minimum reject or classify:

```text
FAIL_CF4_SOURCE_ARTIFACT_OR_LOCK_MISMATCH
HOLD_CF4_EXTERNAL_VENDOR_DEPENDENCY_UNRESOLVED
FAIL_CF4_TRAINING_SOURCE_DIGEST_DRIFT
FAIL_CF4_OLD_CHECKPOINT_RESEALED_AS_NEW
FAIL_CF4_INCORRECT_SHARED_LM_RECIPE
FAIL_CF4_RANK_PAIR_INVALID_OR_NOT_PREDECLARED
FAIL_CF4_TRAINING_HYPERPARAMETER_DRIFT
FAIL_CF4_MODEL_OR_TOKENIZER_BINDING_MISMATCH
FAIL_CF4_TRAIN_EVAL_DOCUMENT_OVERLAP
FAIL_CF4_SPLIT_OR_SEGMENT_IDENTITY_DRIFT
FAIL_CF4_TRAIN_DATASET_DIGEST_MISMATCH
FAIL_CF4_RANK_B_REUSES_RANK_A_OUTPUT_OR_STATE
FAIL_CF4_CHECKPOINT_MISSING_OR_INCOMPLETE
FAIL_CF4_CHECKPOINT_BYTES_OR_MANIFEST_SEAL_MISMATCH
FAIL_CF4_WEIGHT_DIGEST_OR_STEP_CHAIN_MISMATCH
FAIL_CF4_INVALID_HEAD_RANK_OR_DIMENSION
FAIL_CF4_NATIVE_LOAD_OR_FORWARD_UNAVAILABLE
FAIL_CF4_NATIVE_QUEUE_OR_CURRENTNESS_UNOBSERVED
HOLD_CF4_HELDOUT_METRIC_NO_VALID_TARGETS
FAIL_CF4_EVAL_SOURCE_OR_PROOF_DRIFT
FAIL_CF4_TEACHER_FORCED_USED_AS_PREFIX_METRIC
HOLD_CF4_RUNTIME_PREFIX_CAMPAIGN_NOT_RUN
FAIL_CF4_STALE_PREFIX_SIDECAR_OR_CHECKPOINT_MISMATCH
FAIL_CF4_UNAUTHORIZED_HEAD_OR_GLOBAL_PROMOTION
FAIL_CF4_FABRICATED_CF3_OR_W8_W9A_PHYSICAL_PASS
```

Run missing-source, changed-shader/hashed-input, stale train digest, wrong model, swapped rank, corrupt checkpoint bytes, wrong train/eval split, zero valid target, wrong current GPU owner, failed callback, old profile sidecar, false quality selection and duplicate receipt negatives.

**Static negative mutations are SOURCE/STATIC only.** They are not proof that the native device or filesystem failed in the expected way.

## 19. Source / static gates

Before COMPILE/RUNTIME:

1. Exact CF3 parent artifact, hashes and original `Cargo.lock` identified.
2. Current 19-input Rust digest recomputed and compared; no whitelist.
3. Old-source checkpoint/manifests remain byte-preserved.
4. Both rank configs declared and equivalent except rank/output identity.
5. Train/eval split identity, tokenizer and dataset digests enforced.
6. Original frozen shared-LM trainer used, not dense trainer.
7. Existing head checkpoint publication transaction/manifest schema preserved.
8. Native quality requires two comparable actual heads.
9. Prefix acceptance only bound through existing actual runtime campaign.
10. CF3 physical and W8/W9A physical statuses remain independent HOLD.
11. No new default GPU D2H or per-token Queue wait from the CF4 audit wrapper.
12. Failure paths cannot produce PASS-shaped missing values or reusable permits.

Any pre-existing static checker made obsolete by the intentional CF2 training digest change must be identified as **superseded by exact new-lineage validation**; do not edit it to claim that the old digest is still current.

## 20. Exact native command sequence (NOT_EXECUTED)

PowerShell commands here *call existing native Rust binaries*; they are not a Python or PowerShell training implementation. Paths/configs are real values to be supplied from the exact workspace and `--describe-input` outputs.

```powershell
# Run from the exact extracted CF3 full source workspace with real vendor path restored.
cargo metadata --format-version 1 --locked

cargo check -p model_core --lib --release --locked -j 1
cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo check -p base_train --lib --release --locked -j 1
cargo check -p orchestrator_local --lib --release --locked -j 1

# Actual existing input schema. Do not guess recipe, budget, or CLI switches.
cargo run -p base_train --bin ash_aof_r1_frozen_heads_train --release --locked -- --describe-input
cargo run -p base_train --bin ash_aof_r1_frozen_heads_quality --release --locked -- --describe-input

# After writing two *different* fresh, predeclared rank run.json files:
cargo run -p base_train --bin ash_aof_r1_frozen_heads_train --release --locked -- .\rank_a_run.json
cargo run -p base_train --bin ash_aof_r1_frozen_heads_train --release --locked -- .\rank_b_run.json

# After verifying both checkpoint bytes + manifests + train/eval split:
cargo run -p base_train --bin ash_aof_r1_frozen_heads_quality --release --locked -- .\rank_pair_quality_run.json
```

`rank_a_run.json`, `rank_b_run.json`, `rank_pair_quality_run.json` are **operator-provided placeholders**, not files currently established in the archive. There is no proof here that the compiled binaries or GPU runs succeeded. Each command's actual exit status/log/binary hash belongs in the CF4 receipt.

Any CF3 reference WGSL Naga or selected Short32/Long64 PHYSICAL campaign is executed and documented separately under its own source-bound receipt.

## 21. Evidence and PASS tokens

Only emit **scoped** results:

```text
PASS_HEADWISE_R3_CF4_NEW_LINEAGE_CHECKPOINT_MATERIALIZED
    requires real fresh checkpoint bytes, seal, exact source training lineage,
    owner-validated native load/forward, physical completion and correct rank.

PASS_HEADWISE_R3_CF4_HELDOUT_HEAD_QUALITY_MEASURED
    requires the exact two-rank native held-out evaluator to complete,
    nonempty per-horizon denominators, actual finite accuracy/CE and source/split proof.

PASS_HEADWISE_R3_CF4_RUNTIME_PREFIX_QUALITY_MEASURED
    requires current actual profile-campaign acceptance sidecar and native
    verification/commit denominators, separately authenticated.
```

The three tokens do not imply each other. Where an artifact is only host-validated, emit a narrower `CHECKPOINT_BYTES_VALIDATED` receipt instead of `...NATIVE...` PASS. If the adopted quality selection policy is not explicitly frozen and independently satisfied, `HeadAdopted=false`.

**No CF4 aggregate live-head adoption PASS** may be issued without all applicable checkpoints/quality/sidecar authority. Even that aggregate does not issue a Headwise selected-output physical PASS or W8/W9A physical join PASS.

## 22. Performance accounting

CF4's physical costs are head-only training and evaluation, not a decoding acceleration claim. Separate:

```text
first / total head training wall time
training steps/epochs, valid targets and batch rows
peak host memory / WGPU allocated or resident bytes where measured
head-only state size / rank-dependent allocation budgets
GPU queue completion and wait wall
checkpoint write/sync wall and bytes
teacher-forced evaluator per-rank wall/queue waits
runtime profile campaign wall (if executed)
```

Do not charge CF3 qualification-only reference dispatch time to steady-state decode. Do not claim a percentage speedup or improved prefix acceptance without an actual corresponding measured run.

## 23. Final completion boundary and successor

```text
SOURCE:
    exact CF3 parent and no unreviewed training-source mutation
STATIC:
    input/lineage/negative gates; old checkpoint immutable
COMPILE:
    exact Rust native trainer/evaluator/relevant model path
RUNTIME:
    two real fresh rank training sessions, valid dataset + optimizer steps
CHECKPOINT:
    weight bytes + manifest seal + current 19-input source digest
PHYSICAL:
    actual native GPU owner/queue and head load/forward evidence
QUALITY:
    held-out four-horizon denominators + accuracy/CE per rank
PREFIX:
    separately observed only if profile campaign actually ran
SEPARATION:
    CF3 selected-output GPU qualification independent
    CF2 original W8/W9A physical join independent
    default Headwise/AOF/CF5-D unchanged
```

**Stop at the first unavailable mandatory authority.** A source-only or host-file result is reported at its own evidence tier, never inflated to native PHYSICAL.

**Next:** `HEADWISE-R3-CF5` may consume this *actual* current-source checkpoint-lineage proof to qualify the **original sampled W8 comparator and W9A same-invocation join**. The independent `HEADWISE-R3-CF3-PHYS` reference/selected-output campaign must still be completed for later R3 aggregate closure. Neither CF4 nor CF5 automatically activates capacity-strided KV storage or changes token/stop/emit behavior.

**Document state:** Sections 0–23 preserve the original specification and acceptance law. Section 24 records the actual CF4 SOURCE-only bake and its precise evidence ceiling. It does not claim Rust compilation, native training, GPU evaluation, PHYSICAL PASS or performance improvement.

---

## 24. Exact CF4 SOURCE bake annex (2026-10-09)

**Evidence classification: PARTIAL SOURCE BAKE / STATIC ONLY.** The contract in sections 0–23 remains normative. Neither this annex nor any static gate constitutes a successful Rust build, checkpoint training run, native WGPU execution or PHYSICAL PASS.

### 24.1 Exact parent and code-only artifacts

| Artifact | SHA-256 | Files / CRC |
|---|---|---|
| Parent CF3 full ZIP | `57d4fbc0fa223cddbfed097f49f068f5b297fce24393553043ac18dd3beeeb2c` | 8,752 / PASS |
| CF4 full code-only ZIP | `6f6ac28b6196104064893cbd81ac8bd2ef85d0c2e1d0ed2faef14c3a76bda01b` | 8,755 / PASS |
| CF4 source overlay ZIP | `7c80d0d711f6eed44aa80bdcb9c65f0ca11d5cc35acbba3c3dd2eb62da4ad43b` | 4 / PASS |

Relative to the **exact CF3 ZIP**, the only changes are **ADD 3 / MOD 1 / DEL 0**:

| Kind | Source path | SHA-256 (CF4 output) |
|---|---|---|
| MOD | `crates/orchestrator_local/Cargo.toml` | `2e6d4af969ed8cfb67a7186041fe9bd686e26a10d65292e81b98f9a8bdeee699` |
| ADD | `crates/orchestrator_local/src/headwise_r3_cf4_checkpoint_lineage.rs` | `da9296ce04218c6321df6e724ed2362c321d91770a715ea447b203c0ece0dbde` |
| ADD | `crates/orchestrator_local/src/bin/ash_headwise_r3_cf4_lineage_gate.rs` | `98b85138fd22d90ab7dbd0d0707d2f506b267c5aef1367ec1a15c6de32499667` |
| ADD | `tools/validate_ash_headwise_r3_cf4_checkpoint_lineage_static.py` | `02c2ab450311ac303c1eb902aa9dcf35db98f1778ec67b091218e0f5b1318d13` |

The exact 19-input `shared_lm_training_source_digest()` remains **unchanged**:

```text
0b10d1d645ce22356ca4c44bc9e0e4c4ef109f6daf9d143175cd5c9cc1a41094
```

The 19 inputs, `Cargo.lock`, all existing trainer/evaluator functions, selected Headwise WGSL, CF2 same-invocation logic, CF3 native reference, and canonical KV/token/stop/emit behavior are byte-preserved. The new Rust runner is an explicit, feature-gated audit binary (`orchestrator_aof_r1_audit_bins`), not a default production entrypoint. No new Cargo dependency was declared.

### 24.2 Actual SOURCE implementation, not executable evidence

The native Rust audit binary has two commands:

```text
ash_headwise_r3_cf4_lineage_gate --preflight CAMPAIGN.json
ash_headwise_r3_cf4_lineage_gate --run CAMPAIGN.json
```

`CAMPAIGN.json` is supplied by the operator and must include:

```text
schema = ash.headwise.r3.cf4.campaign.v1
repo_root, parent_archive, trainer_binary, quality_binary
rank_a_run, rank_b_run, quality_run, output_root
rank_a, rank_b, trainer_binary_sha256, quality_binary_sha256
```

**No ranks, quality thresholds, actual training budgets or dataset paths were invented by the bake.** The two training input JSON files and quality input JSON must conform to the existing native binaries' `--describe-input` outputs; there are no invented `--rank`, `--epochs` or `--checkpoint` CLI options.

The opt-in gate performs:

1. Exact parent archive SHA, disk `Cargo.lock`, Rust-compiled audit-source versus disk byte equality, and actual 19-input training digest recomputation, compared against the linked native model-core digest. It separately hashes the evaluator's six source files.
2. Exact predeclared rank inequality/bounds; same seed, epochs, `f64` learning-rate bits, source backbone/checkpoint set, tokenizer identity, dataset, budgets, original shared-LM recipe and distinct fresh checkpoint paths.
3. Actual `ArkLoadedHeadQualitySplit::load()` under the declared tokenizer to check parent-document/segment/UTF-8 and dataset split. Records input-file SHA-256 for all frozen backbone/model/tokenizer/dataset/split/document bytes and rechecks them across the campaign.
4. Explicit sequential native Rust child process invocations of the original head-only trainer A and B; separate process exit codes and SHA-bound stdout/stderr files. No Python/PowerShell training logic and no concurrent mutable head optimizer sharing.
5. Read-back of each freshly produced `.safetensors` and `.head-manifest.json`, original manifest validation, checkpoint SHA-256, train dataset SHA, source digest, rank/hyperparameters and original `ArkSharedLmCheckpoint::read()` host deserializer.
6. The original native held-out quality executable, with the original two-rank evaluator output. The audit checks producer source, quality receipt seal, split/dataset digests, original loaded manifest identity, both rank profiles, four nonempty `+2/+3/+4/+5` accuracy/CE observations and per-document records.
7. A **create-new**, SHA-bound terminal audit JSON with typed null/unobserved fields and the first failing stage. Existing checkpoint/manifest publication APIs are unchanged. Failed training/evaluation cannot be silently reclassified as success.

`--preflight` is read-only. `--run` creates a new audit output root only after preflight, and requires existing parent directories for the separate native checkpoint and quality output targets. Fresh target collisions fail closed. The output root is never re-used silently.

**Important evidence limitation:** The existing native quality source reports a queue-wait description and physical runtime binding, but this wrapper does not independently capture a Queue completion callback. Consequently the scoped CF4 audit explicitly retains `native_queue_callback_independently_observed=false`, `physical_queue_callback_qualified=false`, `head_checkpoint_lineage_qualified=false` and `production_promoted=false`, even when actual native quality execution may later return a measured teacher-forced profile. A future physical campaign must separately close the callback/owner witness before issuing the full named PHYSICAL PASS.

### 24.3 Actually executed SOURCE/STATIC evidence

| Gate | Result |
|---|---|
| CF4 own SOURCE/STATIC checks | **35/35 PASS** |
| CF4 negative source mutations | **33/33 rejected** |
| CF3 parent static | **32/32 PASS** |
| CF3 parent negatives | **25/25 rejected** |
| CF2 parent static | **41/41 PASS** |
| CF2 parent negatives | **26/26 rejected** |
| Recomputed 19-input training-source digest | Exact `0b10d1...c9cc1a41094` |
| Full/Overlay archive CRC and exact parent diff | PASS |
| `cargo metadata`, Rust `cargo check`, tests | **NOT_RUN**, Rust toolchain unavailable in this execution environment |
| External `vendor/sherpa-rs-main/crates/sherpa-rs` | **MISSING** from code-only ZIP |
| Native Naga | **NOT_RUN**, no CF4 WGSL changed |
| Rank A/B fresh training, checkpoint creation | **NOT_RUN** |
| Native WGPU evaluator, held-out +2/+3/+4/+5 | **NOT_RUN** |
| Runtime prefix sidecar | **NOT_RUN** |
| CF3 selected-output PHYSICAL and CF2 W8/W9A PHYSICAL | **HOLD**, independent |
| Production / CF5-D ACTIVE | **NOT_PROMOTED** |

Static tests exercised real source-pattern mutations, not GPU faults. SOURCE/STATIC may only establish the inserted code and guards. No release binary was produced or executed in this environment.

### 24.4 Exact native Windows revalidation commands (NOT_EXECUTED)

Restore the exact missing external path dependency from its authorized upstream source before any Cargo claim. No dummy package or `[patch.crates-io]` rewrite.

```powershell
python .\tools\validate_ash_headwise_r3_cf4_checkpoint_lineage_static.py --negative-tests
python .\tools\validate_ash_headwise_r3_cf3_selected_reference_static.py --negative-tests
python .\tools\validate_ash_headwise_r3_cf2_same_invocation_static.py --negative-tests

cargo metadata --format-version 1 --locked
cargo check -p model_core --lib --release --locked -j 1
cargo check -p base_train --lib --release --locked -j 1
cargo check -p orchestrator_local --bin ash_headwise_r3_cf4_lineage_gate --release --locked --features orchestrator_aof_r1_audit_bins -j 1
cargo test -p orchestrator_local --bin ash_headwise_r3_cf4_lineage_gate --release --locked --features orchestrator_aof_r1_audit_bins -j 1

cargo build -p base_train --bin ash_aof_r1_frozen_heads_train --release --locked -j 1
cargo build -p base_train --bin ash_aof_r1_frozen_heads_quality --release --locked -j 1

.\target\release\ash_aof_r1_frozen_heads_train.exe --describe-input
.\target\release\ash_aof_r1_frozen_heads_quality.exe --describe-input

# Only after real inputs/binary SHA-256 values have been frozen in campaign.json:
.\target\release\ash_headwise_r3_cf4_lineage_gate.exe --preflight .\campaign.json
.\target\release\ash_headwise_r3_cf4_lineage_gate.exe --run .\campaign.json
```

`cargo check`/tests are never equivalent to actual WGPU training or evaluation. Actual native run receipts and trained heads must come from the target Windows/GPU machine. Running static validation alone must not create a PASS-shaped checkpoint or physical receipt.

### 24.5 Completion and handoff

Current CF4 result is **SOURCE CANDIDATE / STATIC PASS / NATIVE COMPILE HOLD / CHECKPOINT+QUALITY NOT_RUN**. The next evidence legs are the exact native Rust compile, frozen two-rank campaign inputs, fresh trained weights/manifests, same-source actual native quality and an independent physical completion/currentness campaign. Only afterward may the checkpoint provenance be supplied to CF5; it cannot substitute for CF3 selected-output parity or CF2 W8/W9A physical qualification.

**GitHub boundary:** only this specification, including the factual SOURCE bake annex, is committed to `earthroon/ASH`. The code-only ZIPs remain separate artifacts; a specification commit is not evidence of a code commit in that repository.
