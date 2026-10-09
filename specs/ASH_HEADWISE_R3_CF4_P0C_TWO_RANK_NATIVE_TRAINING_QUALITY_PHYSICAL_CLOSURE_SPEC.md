# HEADWISE-R3-CF4-P0C
## CURRENT-SOURCE TWO-RANK HEAD CHECKPOINT + NATIVE QUALITY QUEUE-EVIDENCE CLOSURE

**Patch ID:** `HEADWISE-R3-CF4-P0C`  
**Parent code:** `ASH_PASS3_HEADWISE_R3_CF3_P0B_SELECTED_GPU_PHYSICAL_QUALIFICATION_CODE_ONLY.zip`  
**Parent ZIP SHA-256:** `0bbc0bfbc2f26e8c43c988bb2bc251a865afceb9e02ab0fab6e5e057acf5b808` (8,761 entries; ZIP CRC PASS, locally verified)  
**Parent specs:** `HEADWISE-R3-CF4`, `ASH-AOF-HEADWISE-P0-A`, `HEADWISE-R3-CF3-PHYS-P0-B`  
**Class:** Native Windows execution campaign, strict checkpoint lineage, two-rank held-out evaluation, real same-runtime GPU Queue callback evidence  
**Status (2026-10-09): SOURCE BAKED / STATIC 44/44 PASS; negative SOURCE mutations 36/36 rejected.** Rust COMPILE, native Naga, two-rank training, held-out quality, live Queue callback and performance remain **NOT_RUN / UNKNOWN**. No P0-C PHYSICAL PASS or production promotion; see SOURCE-bake annex.

```text
HEADWISE-R3-CF4-P0C

+ P0-A CURRENT/HISTORICAL SOURCE-LINEAGE CONTRACT PRESERVATION
+ P0-B SELECTED SHORT32/LONG64 PHYSICAL GATE INDEPENDENT
+ EXACT 19-INPUT HEAD-TRAINING DIGEST PRESERVATION
+ EXISTING CF4 NATIVE PREPFLIGHT / TRAIN / QUALITY REUSE
+ TWO FRESH, PREDECLARED DISTINCT-RANK HEAD-ONLY CHECKPOINTS
+ ACTUAL BACKBONE + TOKENIZER + DATASET + DOCUMENT-SPLIT IDENTITY
+ TRAINING PROCESS, CHECKPOINT BYTES, MANIFEST AND STEP RECEIPTS
+ HELD-OUT +2/+3/+4/+5 ACCURACY / CROSS-ENTROPY
+ EXISTING SAME-QUEUE COMPLETION CALLBACK EVIDENCE MATERIALIZATION
+ PHYSICAL RUNTIME / EVALUATOR / HEAD / RESULT CURRENTNESS
+ NO SECOND QUEUE WAIT OR EXTRA DEFAULT PER-TOKEN D2H
+ TEACHER-FORCED QUALITY != PREFIX ACCEPTANCE
+ OLD CF4 RECEIPT HISTORY PRESERVED, P0C RECEIPT SEPARATE
+ NO HEADWISE / AOF / CF5-D ACTIVE PRODUCTION PROMOTION
```

---

## 0. Evidence baseline and immediate source observation

**CONFIRMED / SOURCE** in the exact P0-B parent ZIP:

1. `crates/orchestrator_local/src/headwise_r3_cf4_checkpoint_lineage.rs` already owns `Cf4Campaign`, `--preflight`, `--run`, 19-input digest validation, frozen document split, two-rank trainer invocation, safetensors/manifest checks, native evaluator invocation and immutable receipt publication.
2. Native trainer: `crates/base_train/src/bin/ash_aof_r1_frozen_heads_train.rs`; native evaluator: `crates/base_train/src/bin/ash_aof_r1_frozen_heads_quality.rs`. Both accept `--describe-input` and one positional run JSON.
3. Native quality evaluator `crates/base_train/src/aof_r1_head_quality_native.rs` actually calls `burn_webgpu_backend::aof_r1_verification::wait_for_queue(handles)` after its real evaluation.
4. **Important correction:** `wait_for_queue` in `crates/burn_webgpu_backend/src/aof_r1_verification.rs` already installs `Queue::on_submitted_work_done`, polls until its atomic flag is set, and returns an error on timeout. The missing CF4 evidence is **typed per-invocation reporting**, not absence of a GPU callback implementation.
5. CF4 currently records `native_queue_callback_independently_observed=false` and terminates with `TEACHER_FORCED_QUALITY_MEASURED_PHYSICAL_CALLBACK_HOLD`. The evaluator records a human-readable `queue_completion` string; that string is not a typed proof.
6. `aof_r1_head_quality_native.rs` is in the six-input **quality evaluator source digest**, but is **not** one of the 19 exact training source inputs. Changing it requires a new evaluator digest and new binary/quality receipts, not a change to the training checkpoint digest if all 19 inputs stay byte-identical.
7. The CF4 gate still requires the original **CF3 ZIP** (`57d4fbc0fa223cddbfed097f49f068f5b297fce24393553043ac18dd3beeeb2c`) through `EXPECTED_CF3_ARCHIVE`. The active P0-B full source ZIP above is a different **current implementation baseline**, not a replacement for that historical parent artifact.
8. P0-A and P0-B are SOURCE/STATIC baked. Their Rust builds, new-lineage checkpoint generation and GPU physical campaigns remain NOT_RUN in available evidence.

**UNKNOWN:** Windows Cargo buildability, valid campaign JSON with actual files, fresh head checkpoints, measured held-out quality, independent evaluator-specific callback receipt, runtime prefix acceptance, quality improvements and speedup.

## 1. Exactly separated authorities

```text
CurrentSourceExact         : NotRun | Exact19 | Changed | Invalid
TrainingProcess           : NotRun | NativeExitedZero | Failed
HeadCheckpoint[rank]      : NotRun | Written | ByteAndManifestValidated | Failed
NativeEvaluation          : NotRun | Measured | Partial | Failed
EvaluatorQueueCompletion  : NotRun | CallbackObserved | Timeout | DeviceLost | Unavailable
QualityDecision           : Unbound | Measured | Qualified | Insufficient
RuntimePrefixAcceptance   : NotRun | Measured | Insufficient
CF3SelectedOutputPhysical : independent P0-B HOLD / measured receipt only
CF2W8W9AJoinPhysical      : independent future CF5 HOLD
GeneralProduction         : NotPromoted
```

**Completion boundaries:** Fresh checkpoint lineage PASS must not imply numerical quality PASS. Quality measurement must not imply runtime prefix acceptance. A bounded evaluator Queue callback must not imply every kernel's own map callback or W8/W9A closure.

## 2. P0C-A: locked native preflight and current source

1. Restore the exact external `vendor/sherpa-rs-main/crates/sherpa-rs` workspace dependency from a legitimate source. No stub crate, deletion, Cargo.lock rewrite, altered vendor version or silent downgrade.
2. Build from the exact P0-B full source tree. Bind SHA-256 of ZIP, source tree, `Cargo.lock`, actual binaries and the run JSONs. Pin Git HEAD only as an audit dimension; the GitHub specs-only repository is **not** the source of the P0-B code.
3. Recompute the real 19-input digest with `shared_lm_training_source_digest()`. For current P0-B exact source the expected value is `0b10d1d645ce22356ca4c44bc9e0e4c4ef109f6daf9d143175cd5c9cc1a41094`.
4. Preserve the older `e20f93b19bcb8a93a96809a28d2faf5c72c68896da060002d36a43e2286b8283` only for historical-source replay. It must never be reattached to the new checkpoint.
5. Supply the actual immutable **CF3 original ZIP** separately to the existing `Cf4Campaign.parent_archive`. Do not replace `EXPECTED_CF3_ARCHIVE` with the P0-B ZIP digest to force preflight PASS.
6. Check `Cf4Campaign` fields: schema, repo_root, parent_archive, trainer_binary, quality_binary, rank_a_run, rank_b_run, quality_run, output_root, rank_a, rank_b, trainer_binary_sha256, quality_binary_sha256. All must bind the exact executable files, not their names alone.
7. Run `--describe-input` for trainer and evaluator. Freeze JSON schemas from the binaries that will actually execute; do not invent flags or assume prior CLI versions.

### Important source-digest fence

**No edits** in P0C to any of the 19 training input files, especially `native_wgpu.rs`, `aof_r1_shared_lm_head_training.rs`, `bin/ash_aof_r1_frozen_heads_train.rs` and `Cargo.lock`. If an actual compiler fix necessarily modifies one, stop and create a distinct training-lineage revision. Do not keep the CF2 digest label for different bytes.

## 3. P0C-B: two-rank fresh checkpoint execution

Use the existing native `ash_headwise_r3_cf4_lineage_gate --run <campaign.json>` to invoke the original trainer twice. Require:

- Two distinct ranks satisfying `0 < rank < actual hidden_size`, frozen **before** the campaign.
- Same backbone checkpoint set, model spec, tokenizer manifest/model, training dataset bytes, seed, epochs, learning rate, memory budgets, root selection, head-only recipe and intended offset set. Only declared head rank is different.
- Actual `ArkLoadedHeadQualitySplit` document-level partition checks; train/eval cannot share source document identity. Preserve source segment byte evidence, not only digest strings.
- Fresh distinct `.safetensors` paths and `.head-manifest.json` files, no pre-existing target, no implicit overwrite. Each rank has its own output and optimizer state; no trained weights reused across ranks.
- Original native trainer process completion, exact exit code, stdout/stderr SHA where captured, actual completed steps/epochs, valid target counts for +2/+3/+4/+5, first/last loss, and checkpoint producer status.
- `ArkSharedLmCheckpoint::read()` on **actual weight bytes**, manifest SHA/seal, current source digest, model/tokenizer/dataset binding, rank and train-step lineage. Report `head_only_trained_candidate`, never `promoted=true`.
- Re-hash frozen model/tokenizer/dataset and both checkpoint outputs before and after native evaluation. Reject any mutation, stale run config, wrong source, wrong rank, missing horizon or duplicate artifact.

**Training GPU completion note:** The existing training CLI returns process+checkpoint evidence but does **not** export its own per-step Queue callback ticket. P0C must not synthesize such a ticket using a later evaluator callback. Training-process and checkpoint evidence are separate from evaluator Queue physical qualification.

## 4. P0C-C: same-runtime native quality and callback receipt

### Current owner to preserve

```text
NativeWgpuModel (actual loaded backbone)
  -> ArkSharedLmCheckpoint::read (each new rank)
  -> ArkSharedLmFutureTransforms::from_checkpoint
  -> actual quality evaluation, same Device/Queue
  -> existing wait_for_queue(handles)
      -> Queue::on_submitted_work_done(callback)
      -> Device::poll(...), callback observed or error
  -> quality result and four-horizon metrics
```

Do **not** add a second Queue wait solely for evidence. Instead add a typed observation to the *existing* `aof_r1_verification::wait_for_queue` implementation or a common helper used by it. Proposed API (name is not present in parent):

```rust
struct NativeQualityQueueObservation {
    physical_binding: PhysicalWgpuRuntimeBindingR1,
    callback_registered: bool,
    callback_observed: bool,
    wait_wall_ns: u64,
    // None unless the source really exposes them.
    submission_ordinal: Option<u64>,
    map_callback_observed: Option<bool>,
}

fn wait_for_queue_observed(
    handles: &NativeWgpuRuntimeHandles,
) -> anyhow::Result<NativeQualityQueueObservation>;
```

Retain legacy `wait_for_queue(handles) -> Result<()>` semantics by sharing a single internal implementation. Never register an extra callback or poll twice. On callback timeout, device loss or failed poll, error is propagated and no `callback_observed=true` can be emitted.

### Actual physical evidence binding

Within `aof_r1_head_quality_native.rs`, capture the observation from the **same actual model** that generates quality outputs. Bind:

- `PhysicalWgpuRuntimeBindingR1` (`existing_id`, `device_authority_id`, `queue_authority_id`, `runtime_generation`) both before and after evaluation.
- Actual model instance/binding, tokenizer/dataset/split seal, current quality input digest, both checkpoint SHA/seals/ranks, evaluator binary SHA and six-input source digest.
- Real `callback_registered`, `callback_observed`, actual wait wall and owner currentness.
- The **true observation scope**: `LEGACY` may wait separately per rank; `OBSERVE` has a shared end-of-pair wait. Never manufacture two callbacks from a shared event.
- WGPU output/readback provenance only where an actual producer exposes it. A returned host tensor or a `queue_completion` string does not by itself prove a distinct MAP callback.

Preserve `head_quality.json` result sealing and existing output compatibility. Add a versioned P0C sidecar or backward-compatible extension to report the typed queue proof, and include the new producer identity in its exact digest. No disk JSON file can own a live GPU lease.

**CF4 historical audit:** Keep `TEACHER_FORCED_QUALITY_MEASURED_PHYSICAL_CALLBACK_HOLD` in previously issued CF4 receipts. P0C writes a new source-bound qualification receipt, rather than editing a historical JSON's `false` field to `true`.

## 5. Evaluator source revision and quality modes

If `aof_r1_head_quality_native.rs` is modified, the current **six-input evaluator source digest necessarily changes**. That is an evaluation-source revision even when the training 19-input digest is byte-identical.

- Update the evaluator's real source digest via its existing implementation, never hardcode the old value in a new receipt.
- Bind the new evaluator binary SHA in `Cf4Campaign.quality_binary_sha256` and re-run its full native evaluation.
- `LEGACY` can be the control arm. `OBSERVE` remains eligible only when its own same-source exact comparison and inputs are validated.
- Old `OBSERVE` or `ACTIVE` proof receipts tied to a prior evaluator-source digest cannot be reused unchanged. `ACTIVE` remains gated on its existing independent CF1/CF2/VH6 receipts and must never be silently enabled by P0C.
- No rewrite of optimizer math, evaluation logits, predicted token selection, label policy, loss formula, full-vocab CE or physical KV storage is authorized.

## 6. Four-horizon held-out quality contract

Each rank must produce, for each offset in `[2, 3, 4, 5]`:

```text
valid_targets > 0
correct_count  <= valid_targets
accuracy       = correct_count / valid_targets
cross_entropy  = actual observed value, finite
per-document horizon observation and source identity
```

The existing quality evaluator's actual field schema is authoritative. Do not rename or backfill unsupported counters solely to fit this display notation. Compare ranks using identical held-out documents and source configuration. Retain raw measured metrics and denominators; no threshold is invented by P0C.

- Fresh checkpoint generation + actual held-out evaluation can be **MEASURED** without claiming improvement over a baseline.
- A quality **selection** requires a frozen, user-approved comparison criterion. If unbound or rank results conflict, keep `QualityDecision=Unbound` and both candidates unpromoted.
- Teacher-forced offset accuracy is **not** AOF prefix acceptance probability. Runtime accepted-depth histogram, accepted/rejected prefixes, stop/EOS, published tokens and verified prefix must come from a distinct exact native profile campaign, else `RuntimePrefixAcceptance=NotRun`.

## 7. Output SSOT and receipts

**Existing (preserve):** `headwise_r3_cf4_receipt.json` and original trainer checkpoint/quality artifacts.  
**New P0C (proposed):** `headwise_r3_cf4_p0c_two_rank_quality_physical_receipt.json`.

Required P0C fields:

```text
schema; exact P0-B parent ZIP SHA; CF3 historical parent ZIP SHA
19-input training source digest; exact 19 source per-file digests
quality six-input evaluator source digest; Cargo.lock SHA
source-tree digest; Rust trainer/evaluator/qualifier binary SHA
campaign/schema and two trainer-run JSON hashes; quality-run SHA
model/checkpoint/tokenizer/split/train/eval dataset SHA + split seal
rank_a/rank_b; training recipe and immutable config
rank checkpoint bytes SHA; manifests/seals/optimizer/step/valid-targets
native eval mode; per-rank four-horizon counts/accuracy/CE
per-document observations; native forward currentness
PhysicalWgpuRuntimeBindingR1 before/after; queue callback observation(s)
queue wait wall; MAP event separately UNKNOWN if not source-observed
quality receipt SHA/seal; old CF4 receipt SHA; new P0C receipt SHA
training_physical_callback_observed = None unless independently measured
runtime_prefix_acceptance = NOT_RUN unless independent receipt exists
cf3_selected_output_physical = HOLD unless independently measured
cf2_w8_w9a_join_physical = HOLD unless independently measured
production_promoted = false; cf5_d_active = false
first_failure_stage / first_failure_class / actual provenance
```

For missing observations use `null`, `UNKNOWN`, `NOT_RUN` or typed HOLD. Literal zero is permitted **only** when a real counter actually measured zero.

## 8. Negative cases and stop law

Required negative matrix:

| Negative | Required classification |
|---|---|
| Current source digest differs from compiled 19-input | `FAIL_P0C_TRAINING_SOURCE_DRIFT` |
| Historical CF3 archive substituted with P0-B ZIP | `FAIL_P0C_CF3_PARENT_ARTIFACT_DRIFT` |
| Trainer/evaluator binary SHA mismatch | `FAIL_P0C_BINARY_PROVENANCE` |
| Rank duplicated/changed after freeze | `FAIL_P0C_RANK_PAIR_DRIFT` |
| Model, tokenizer, dataset or source document differs across ranks | `FAIL_P0C_SHARED_INPUT_DRIFT` |
| Train/eval document overlap | `FAIL_P0C_HELDOUT_LEAKAGE` |
| Old manifest rewritten to current digest | `FAIL_P0C_CHECKPOINT_RESEAL` |
| Fresh checkpoint missing or weights/manifest differ | `FAIL_P0C_CHECKPOINT_BYTES_OR_SEAL` |
| Any applicable horizon has zero/invalid targets | `HOLD_P0C_QUALITY_INCOMPLETE` |
| Evaluator source/binary changed without new receipt | `FAIL_P0C_EVALUATOR_SOURCE_DRIFT` |
| Queue callback missing/timeout/device loss | `HOLD_OR_FAIL_P0C_QUEUE_COMPLETION` |
| Queue event from wrong model/session/device | `FAIL_P0C_QUEUE_OWNER_DRIFT` |
| One shared callback labeled as two rank-local events | `FAIL_P0C_CALLBACK_CARDINALITY` |
| CPU string treated as physical callback | `FAIL_P0C_STRING_AS_CALLBACK_PROOF` |
| Prior CF4 receipt mutated to report PASS | `FAIL_P0C_HISTORICAL_RECEIPT_REWRITE` |
| Quality accuracy used as measured prefix rate | `FAIL_P0C_PREFIX_METRIC_FABRICATION` |
| Inferred production/default activation | `FAIL_P0C_EARLY_PRODUCTION_PROMOTION` |

Negative SOURCE/STATIC mutations must not be described as actual hardware negative-case execution. Any failed GPU callback or currentness fence is a terminal fail/HOLD, not an implicit legacy fallback PASS.

## 9. Minimal source touchpoints (proposed; verify exact signatures before bake)

```text
MOD? crates/burn_webgpu_backend/src/aof_r1_verification.rs
     - expose typed evidence from its existing callback wait; no second wait
MOD? crates/base_train/src/aof_r1_head_quality_native.rs
     - bind native queue observation to real quality invocation
ADD? crates/orchestrator_local/src/headwise_r3_cf4_p0c_physical_receipt.rs
     - receipt verifier/aggregation, no model math
ADD? crates/orchestrator_local/src/bin/ash_headwise_r3_cf4_p0c_gate.rs
     - optional independent CLI; do not duplicate CF4 training owner
MOD? crates/orchestrator_local/Cargo.toml
     - only if the optional gate binary is needed; Cargo.lock unchanged
ADD? tools/validate_ash_headwise_r3_cf4_p0c_static.py
     - source/currentness/cardinality/negative gates
```

Retain the existing `headwise_r3_cf4_checkpoint_lineage.rs` contract and CLI when possible; do not refactor it to alter original output. No source change to the 19 training-input files. Do not add a new custom optimizer, checkpoint writer, quality math or AOF scheduler.

## 10. Native acceptance ladder

| Tier | Mandatory evidence |
|---|---|
| SOURCE | CF4 reused, callback already in underlying wait, P0C scoped audit source |
| STATIC | P0-A 60/60; P0-B 45/45; CF4 and P0C negatives; 19-input digest exact |
| COMPILE | Locked native trainer, evaluator, CF4/P0C gate release build |
| RUNTIME TRAIN | Two actual new rank heads, process exits, step/manifest validation |
| RUNTIME QUALITY | Actual native evaluator on exact held-out set, +2/+3/+4/+5 values |
| PHYSICAL QUEUE | Same-runtime callback actually observed from natural evaluator wait |
| QUALITY DECISION | Measured/qualified only under independently frozen comparison policy |
| PREFIX | Separately measured profile campaign; never computed from teacher forcing |
| PERFORMANCE | Independent timed A/B; no inferred headwise speedup |
| PROMOTED | **Forbidden** in P0C |

If MAP callback, per-step training callback or GPU submission ordinal is not exposed, leave their fields UNKNOWN, without blocking a narrower, truthful **evaluator Queue-completed** result. Do not claim those unobserved details.

## 11. Windows native execution commands

From the **actual extracted P0-B source root** with the exact external dependency restored:

```powershell
cargo metadata --format-version 1 --locked

# Existing SOURCE/STATIC gates
python .\tools\validate_ash_aof_headwise_p0a_lineage_contract_static.py --negative-tests
python .\tools\validate_ash_headwise_r3_cf3_p0b_physical_static.py --negative-tests
python .\tools\validate_ash_headwise_r3_cf4_checkpoint_lineage_static.py --negative-tests

# These commands read the real JSON schema; they do not train.
cargo run -p base_train --bin ash_aof_r1_frozen_heads_train `
  --release --locked -- --describe-input
cargo run -p base_train --bin ash_aof_r1_frozen_heads_quality `
  --release --locked -- --describe-input

# Rust native build: actual packages and opt-in audit binary.
cargo build -p base_train --bin ash_aof_r1_frozen_heads_train --release --locked -j 1
cargo build -p base_train --bin ash_aof_r1_frozen_heads_quality --release --locked -j 1
cargo build -p orchestrator_local --bin ash_headwise_r3_cf4_lineage_gate `
  --features orchestrator_aof_r1_audit_bins --release --locked -j 1

# Supply a real campaign JSON with the exact CF3 historical archive path.
$CAMPAIGN = '<ACTUAL_CF4_CAMPAIGN_JSON_PATH>'
.\target\release\ash_headwise_r3_cf4_lineage_gate.exe --preflight $CAMPAIGN
.\target\release\ash_headwise_r3_cf4_lineage_gate.exe --run $CAMPAIGN
```

`<ACTUAL_CF4_CAMPAIGN_JSON_PATH>` is an **unbound operator-supplied path**, not a fabricated existing fixture. If P0C adds a separate binary or validator, compile and invoke it only after those source paths actually exist, using its declared CLI. CF4 uses fresh-once destinations; a rerun must use a new output root and new checkpoint paths, not silently reuse old results.

Run WGPU Naga/physical controls separately where relevant. Compiling and running a head-quality evaluator does not close P0-B Short32/Long64 selected-output parity. No automatic new head checkpoint proof can be inferred from P0-A/P0-B static PASS.

## 12. Exit tokens and boundaries

Allowed independently scoped tokens (names **proposed**):

```text
PASS_HEADWISE_R3_CF4_P0C_CURRENT_SOURCE_TWO_RANK_CHECKPOINT_LINEAGE
PASS_HEADWISE_R3_CF4_P0C_HELDOUT_FOUR_HORIZON_MEASURED
PASS_HEADWISE_R3_CF4_P0C_NATIVE_EVALUATOR_QUEUE_COMPLETION
```

Each is valid only on its own measured provenance. A full P0C closure receipt requires all three, exact source/binary/currentness, and immutable result sealing; it **does not** certify a training-step callback that was never observed.

Always preserve:

```text
HEADWISE_CF3_P0B_SELECTED_SHORT_LONG_PHYSICAL = HOLD unless separately run
HEADWISE_CF2_W8_W9A_PHYSICAL_JOIN             = HOLD until CF5
AOF_CF5_C_SELECTED_NATIVE_CONSUMER            = HOLD
AOF_CF5_D_ACTIVE                              = false
GENERAL_HEADWISE_PRODUCTION_PROMOTED         = false
```

**Successor:** `HEADWISE-R3-CF5` real sampled W8/W9A same-native-invocation physical join, using only a genuinely admitted new-lineage checkpoint. P0-B physical campaign remains an independent parallel prerequisite for the later Headwise-R3 aggregate closure.

**Final invariant:** Actual, source-bound frozen-head training and held-out quality can be proven without changing model math or historical checkpoints. The actual evaluator Queue callback is already executed in the parent; P0C makes it an auditable same-runtime observation rather than a descriptive string. No evidence is promoted across checkpoint, quality, Queue, prefix, W8/W9A, selected-output or production boundaries.


---

## 13. Exact P0-C SOURCE bake annex (2026-10-09)

**Evidence tier:** SOURCE/STATIC only. The implementation is a qualification-only candidate, not a compiled or physically measured native campaign. Original normative sections 0–12 remain in force. No trained checkpoint, new GPU callback execution, quality improvement, rank selection or runtime prefix measurement was performed in this bake.

### 13.1 Exact code-only artifacts

| Artifact | SHA-256 | Files | CRC |
|---|---|---:|---|
| Exact P0-B parent | `0bbc0bfbc2f26e8c43c988bb2bc251a865afceb9e02ab0fab6e5e057acf5b808` | 8,761 | PASS |
| P0-C Overlay | `bfb26d35b3baa9656dd14f589ad9a0fac1fd7fa8547a67f8364e04525ec33f92` | 6 | PASS |
| P0-C Full (P0-A/P0-B included) | `aa05a6aa3b71a6cbcf48bd178925a7e59b183bba1032fca162adec52446791fd` | 8,764 | PASS |

**Delta:** MOD 3, ADD 3, DEL 0. Every unlisted parent file is byte-identical to P0-B. No `_patch` output filenames; ZIP member paths use `ash_pass3/` exactly.

### 13.2 Exact source changes

| Operation | Path | File SHA-256 |
|---|---|---|
| MOD | `crates/base_train/src/aof_r1_head_quality_native.rs` | `85b49342655b43474a9aad6563a684b32793ea68c1d0269148397b3cfa41ed96` |
| MOD | `crates/burn_webgpu_backend/src/aof_r1_commit_trace.rs` | `d6196e03025df98a7c006440dd44e5acf102d867a7b934cefe7a50a208345a6f` |
| MOD | `crates/orchestrator_local/Cargo.toml` | `372f7729aceea3d45a7a5606a68158aa1a304af410fec5ce44b35ec6f0f027f9` |
| ADD | `crates/orchestrator_local/src/bin/ash_headwise_r3_cf4_p0c_gate.rs` | `81207e495eac2eb0ddccad0edc703818a226d40d455923c48a0d2c7b09512a71` |
| ADD | `crates/orchestrator_local/src/headwise_r3_cf4_p0c_physical_receipt.rs` | `944ea18f9b76037d7fc6127f15f68f29603776791b3fc057bb011118b68f2515` |
| ADD | `tools/validate_ash_headwise_r3_cf4_p0c_static.py` | `47fe5b5389c6f59c506ce7f16ca99a2804630c0c9c480f25b08f46ae28abb759` |

### 13.3 Physical callback evidence implementation seam

**Deviation from proposed touchpoint, preserving the more important training-source contract:** `aof_r1_verification.rs` is one of the immutable 19 training inputs, so P0-C does **not** edit it or change `wait_for_queue()`'s signature. Instead, the existing `aof_r1_commit_trace.rs` already receives `callback_registered()` and `completed_wait(duration, callback_observed)` from the real wait. New `ArkP0cQualityQueueScope` observes those exact events on the calling thread, tied to the evaluator's real `PhysicalWgpuRuntimeBindingR1`. The new scope has no nested permission, requires exactly one registration and one completed callback, rejects overflow, and resets on drop. It does not register another callback, submit another command, or call another wait.

- `LEGACY`: one scoped callback for each rank, two events total.
- `OBSERVE`/`ACTIVE`: a single shared rank-pair callback event, not two fabricated rank-local events.
- The actual native evaluator rechecks frozen owner, held-out split, weight digests/manifest seals and Device/Queue binding before recording its event.
- New `head_quality.json.p0c_queue` is sealed within the existing evaluator output and binds training/evaluator source digests, trace producer digest, model instance, rank weight SHA and manifest seals, split, and exact callback event cardinality.
- MAP callback, GPU submission ordinal and training-step callback remain `null` when unobserved. There is no fabricated W8/W9A, Short32/Long64 or prefix-acceptance evidence.
- The existing CF4 `headwise_r3_cf4_receipt.json` continues to report `TEACHER_FORCED_QUALITY_MEASURED_PHYSICAL_CALLBACK_HOLD`. P0-C writes a separate new receipt only after checking that CF4 parent and actual native evaluator are byte/currentness qualified.

### 13.4 Checkpoint and evaluator source lineage

```text
current 19-input training digest:
0b10d1d645ce22356ca4c44bc9e0e4c4ef109f6daf9d143175cd5c9cc1a41094
historical pre-CF2 training digest:
e20f93b19bcb8a93a96809a28d2faf5c72c68896da060002d36a43e2286b8283

parent 6-input quality evaluator digest:
3304182b36373d5ed8c6d82251547126d50df931b530e4d458d726782ddc1995
P0-C 6-input quality evaluator digest:
03f77110045fbc225ca1f96040963e614f281469975e6c2b068dce525738e480

P0-C native trace producer source SHA-256:
d6196e03025df98a7c006440dd44e5acf102d867a7b934cefe7a50a208345a6f
```

The 19-input digest is **unchanged**. The six-input evaluator source identity **intentionally changed**. Older quality receipts are historical and cannot be replayed as P0-C native evidence; evaluation must be rerun using the newly built executable and sealed output. `Cargo.lock` and the native head trainer source were not modified.

### 13.5 Gates actually executed

```text
P0-A                       SOURCE/STATIC 60/60 PASS; lineage negative 25/25
P0-B                       SOURCE/STATIC 45/45 PASS; negative 30/30
HEADWISE R3-CF3            SOURCE/STATIC 32/32 PASS; negative 25/25
HEADWISE R3-CF4            SOURCE/STATIC 35/35 PASS; negative 33/33
P0-C                       SOURCE/STATIC 44/44 PASS; negative 36/36
P0-B parent CRC/delta      PASS
P0-C Overlay/Full CRC      PASS

RUST COMPILE                NOT_RUN
NATIVE NAGA                NOT_RUN
TWO-RANK NATIVE TRAINING   NOT_RUN
NEW HEAD CHECKPOINTS       NOT_RUN
FOUR-HORIZON HELDOUT       NOT_RUN
QUEUE PHYSICAL CALLBACK    NOT_RUN
RUNTIME PREFIX ACCEPTANCE  NOT_RUN
CF3 SELECTED OUTPUT        INDEPENDENT HOLD
W8/W9A PHYSICAL JOIN       INDEPENDENT HOLD
PRODUCTION PROMOTED        false
AOF CF5-D ACTIVE           false
```

Negative source mutations are static tests of a source-text contract, not real GPU timeout, Queue completion, device loss, or numerical parity tests. Existing parent validator passes do not mean P0-C Rust or GPU passed.

### 13.6 Windows revalidation commands (not executed in this environment)

Restore the exact external `vendor/sherpa-rs-main/crates/sherpa-rs` dependency without a stub or `Cargo.lock` rewrite, then use the extracted P0-C Full tree:

```powershell
python .\tools\validate_ash_headwise_r3_cf4_p0c_static.py --negative-tests
python .\tools\validate_ash_aof_headwise_p0a_lineage_contract_static.py --negative-tests
python .\tools\validate_ash_headwise_r3_cf3_p0b_physical_static.py --negative-tests
python .\tools\validate_ash_headwise_r3_cf4_checkpoint_lineage_static.py --negative-tests
cargo metadata --format-version 1 --locked
cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo check -p base_train --lib --release --locked -j 1
cargo build -p base_train --bin ash_aof_r1_frozen_heads_train --release --locked -j 1
cargo build -p base_train --bin ash_aof_r1_frozen_heads_quality --release --locked -j 1
cargo build -p orchestrator_local --bin ash_headwise_r3_cf4_p0c_gate `
  --features orchestrator_aof_r1_audit_bins --release --locked -j 1
cargo test -p burn_webgpu_backend --lib p0c_quality_scope --release --locked -j 1
cargo test -p orchestrator_local --bin ash_headwise_r3_cf4_p0c_gate `
  --features orchestrator_aof_r1_audit_bins --release --locked -j 1

# Operator-supplied real CF4 campaign JSON, with the original CF3 parent archive.
$CAMPAIGN = '<ACTUAL_CF4_CAMPAIGN_JSON_PATH>'
.\target\release\ash_headwise_r3_cf4_p0c_gate.exe --preflight $CAMPAIGN
.\target\release\ash_headwise_r3_cf4_p0c_gate.exe --run $CAMPAIGN
```

`--run` delegates the original CF4 training/evaluation transaction once. Existing fresh-once checkpoint/output semantics remain mandatory; re-entry requires new paths and a new campaign output root. The P0-C receipt is separate from the CF4 historical receipt and cannot upgrade absent selected-output, W8/W9A or capacity-strided consumer evidence.

**Commit boundary:** GitHub contains only this specification and its SOURCE-bake evidence annex. The code-only ZIPs are separate, not GitHub source commits. A specification commit is not a native build or physical proof.
