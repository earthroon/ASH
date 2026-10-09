# HEADWISE-R3-CF5-CF1
## CURRENT-LINEAGE LIVE W9A SAMPLED PHYSICAL CLOSURE

**Patch ID:** `HEADWISE-R3-CF5-CF1`  
**Exact parent:** `ASH_PASS3_HEADWISE_R3_CF5_ORIGINAL_W8_W9A_SAME_INVOCATION_PHYSICAL_JOIN_CODE_ONLY.zip`  
**Parent SHA-256:** `7f4e3186befe8313c34923a7ad03475e803e19724737a7b16e68466ce10d7447`  
**Parent entries:** `8,767`, ZIP CRC PASS  
**Historical CF5 overlay SHA-256:** `f660ba5617ec54dc0debebc2be80abd2653ff269c4732225982051fd09c3ed91`  
**Class:** native selected-route execution, W8 physical completion, original W9A same-invocation receipt, checkpoint lineage and scoped physical promotion  
**Status (2026-10-09): PARTIAL SOURCE BAKE / STATIC 54/54 PASS, negative mutations 39/39 rejected.** Rust COMPILE, Naga, real W9A sampled GPU PHYSICAL, current-lineage head checkpoint and performance are NOT_RUN/UNKNOWN. The `--run` CLI is an explicit `HOLD_CF5_CF1_NATIVE_LIVE_SEAM_UNAVAILABLE` until an authorized natural native session source/ownership handoff exists. No physical PASS or production promotion. See section 24 SOURCE bake annex.

**Next:** `HEADWISE-R3-CF6` independent aggregate closure **after** CF3/P0-B selected-output, CF4/P0-C checkpoint/quality and CF5-CF1 same-invocation gates each pass within their own scope. AOF CF5-C native capacity-strided consumer qualification remains independent.

```text
HEADWISE-R3-CF5-CF1

CURRENT-LINEAGE LIVE W9A SAMPLED PHYSICAL CLOSURE

+ EXACT CF5 SOURCE/BINARY/CARGO GRAPH BINDING
+ P0-C ACTUAL TRAINED HEAD CHECKPOINT LINEAGE
+ W9A CONFIG CHECKPOINT HASH-DOMAIN SEPARATION
+ NATURAL NATIVE W9A ELIGIBILITY + SAMPLED ROUTE
+ ORIGINAL W8 V2 QUEUE/MAP/GPU STATUS EVIDENCE
+ SAME LEXICAL INVOCATION W8/W9A/CF2 JOIN
+ SESSION/STEP/LAYER/NONCE/POLICY GENERATION CURRENTNESS
+ LIVE OWNERSHIP NOT INFERRED FROM DISK JSON
+ SCOPED LIVE RESULT WITHOUT GLOBAL RequireMeasuredJoin CUTOVER
+ NATIVE NEGATIVE/RETIREMENT/CANONICAL LIFECYCLE MATRIX
+ NO NEW W8 DISPATCH / MAP / FULL-CONTEXT D2H
+ NO OLD CHECKPOINT RESEAL / 19-INPUT DRIFT
+ CF3-P0B / P0C / CF5 JOIN INDEPENDENT EVIDENCE
+ NO GENERAL HEADWISE OR AOF CF5-D ACTIVE PROMOTION
```

---

## 0. Parent facts and evidence baseline

### 0.1 Confirmed SOURCE from the exact CF5 full ZIP

1. `crates/burn_webgpu_backend/src/attention_interconnect_w8_context_parity.rs::AttentionInterconnectW8ContextParityPipeline::compare()` submits the original W8 compare/finalize/copy once, registers an `on_submitted_work_done` callback on the same Queue, and independently registers `map_async`. Its `original_physical_completion` is a host-receipt v2 optional field. The GPU status ABI remains **32 × u32 = 128 bytes**.
2. The W8 receipt records `queue_submission_ordinal: None`, not a physically measured ordinal. Local scratch retirement does not prove the caller-owned Headwise or TensorCube input leases are retired.
3. `crates/model_core/src/headwise_r3_cf2_native_join.rs::join_headwise_r3_cf2_same_call()` validates an original W8 receipt within the lexical native invocation. It projects the v2 callback fields when present and preserves `checkpoint_lineage_qualified=false`, `physical_join_qualified=false` on the historic CF2 receipt.
4. `crates/model_core/src/native_wgpu.rs` has a real W9A sampled branch that calls `compare_attention_decode_w9a_contexts()` and records W8/W9A through `record_attention_decode_w9a_layer_receipt_with_cf2_join()` in that same invocation.
5. `configure_headwise_r3_cf2_join_mode(RequireMeasuredJoin, ...)` currently **unconditionally returns HOLD**. The natural `native_wgpu.rs` decode path and receipt-recording path also reject that mode. The existing `Observe` mode is the reachable capture mode.
6. Public native observation methods include `headwise_r3_cf2_join_observations()`, `headwise_r3_cf2_join_summary()`, and `take_headwise_r3_cf2_step_join_evidence(session_id, epoch, step)`. Their return values are audit objects, not resource-owning GPU leases.
7. `crates/orchestrator_local/src/headwise_r3_cf5_physical_join.rs` provides `preflight` and `audit`; it emits **source/history HOLD**, not a live GPU physical PASS. The existing gate binary only accepts `--preflight` and `--audit`; **there is no CF5 live `--run` CLI in this parent**.
8. The older `ash_attn_decode_w9a_physical_gate` binary is a separately scoped W9A physical scenario runner. It is **not**, by its name or existence, proof that the same `NativeWgpuModel` sampled W8/W9A invocation was exercised.
9. The head-training source digest for the 19 exact inputs remains `0b10d1d645ce22356ca4c44bc9e0e4c4ef109f6daf9d143175cd5c9cc1a41094`.
10. CF5 source/static checked `51/51`, negatives `35/35`. P0-A/P0-B/P0-C parent STATIC gates passed. Historic CF2 snapshot STATIC `40/41` fails only on the now-superseded always-`None` callback assumption. Do not convert that historical FAIL into PASS.
11. CF5 computed `5fdfafa7df13132da4ea53cdf60e2204ce805d940fbf557baac6c0dc8a2cbd1f` as a **source-only projection** of runtime source identity. It is not a compiled binary SHA, adapter identity or physical event.

### 0.2 UNKNOWN / NOT_RUN

- Rust COMPILE, native Naga, real selected W9A invocation, physical sampled W8 numeric outcome, actual Queue callback on this machine, device-loss response, and performance.
- Actual current-lineage two-rank head checkpoint generation and native load.
- Whether the existing user-facing decode/generation CLI provides an unmodified non-hashed seam that supplies all exact current native live identities.
- Whether `W9AProductionConfig.checkpoint_digest` names the same artifact class as P0-C's trained head weights. A 64-character hash is **not** proof of shared domain.
- A physical all-applicable-layer coverage count until route selection and layer cardinality are observed.

---

## 1. Purpose and exact scope

The missing edge is:

```text
P0-C ACTUAL CHECKPOINT + MODEL/TOKENIZER/CHECKPOINT SOURCE
                            |
                    LIVE NativeWgpuModel
                            |
        actual eligible W9A sampled incremental invocation
                            |
       +--------------------+---------------------+
       |                                          |
 Headwise context                         TensorCube context
       +--------------------+---------------------+
                            |
                    ORIGINAL W8 compare
                   Queue callback + MAP
                            |
               ORIGINAL sealed W8 receipt
                            |
                SAME-CALL W9A route receipt
                            |
               CF2 source-owned joined record
                            |
         CF5-CF1 live physical qualifier, same owner
                            |
           BOUNDED SCOPED RECEIPT / PASS or HOLD
```

The patch qualifies a natural sampled invocation. It does **not** change attention math, W8 numeric thresholds, W9A eligibility rates, W9A pre-sampler authority, KV allocation/append, token commit, stop, emit or checkpoint weights.

### Explicit semantic limits

- The CF2 original receipt and existing CF5 disk-audit receipt remain historically truthful and unchanged.
- The **new CF5-CF1** receipt alone may mark scoped live physical completion.
- No global Headwise production cutover, `RequireMeasuredJoin` default, AOF CF5-D ACTIVE, or latency claim.
- `Observed W8 FAIL` can be a valid measurement result for a rollback-control leg. It is **not** numerical qualification of a passing W8 leg.

---

## 2. Mandatory three-axis result model

Keep these axes independent:

```rust
// PROPOSED TYPES, NOT PRESENT IN THE CF5 SOURCE
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Cf5Cf1CheckpointAdmission {
    NotProvided,
    CurrentSourceBytesVerified,
    NativeModelLoadObserved,
    LiveSessionCurrent,
    Hold,
    Failed,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Cf5Cf1W8Observation {
    NotSelected,
    Unsampled,
    MeasurementUnavailable,
    MeasuredPass,
    MeasuredFail,
    PhysicalFailure,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Cf5Cf1JoinAdmission {
    NotObserved,
    SameCallSourceJoined,
    SameCallPhysicalQualified,
    Hold,
    Failed,
}
```

`W9A route selected` is **another axis**, not an alias for `W8 MeasuredPass`.

Failure on the checkpoint axis may still allow a distinctly labeled `kernel_fixture_only` or unpromoted W8 observation, but **not** a live-current-head physical PASS.

---

## 3. First stop: real CF4/P0-C checkpoint authority

Before a **live-current-head** promotion:

1. Execute the existing `ash_headwise_r3_cf4_p0c_gate --preflight <campaign.json>` and `--run <campaign.json>` under a true native build.
2. Require actual rank A/B checkpoint bytes and matching manifests, current training source digest, model/tokenizer/dataset split, held-out +2/+3/+4/+5 quality receipts and same-evaluator Queue callback evidence.
3. Verify both checkpoints' `safetensors` bytes, manifest seals and actual head-only weights through the existing checkpoint reader, then observe **the checkpoint actually loaded by the live inference session**.
4. Do not claim runtime prefix acceptance merely from teacher-forced quality.
5. Do not silently use a source-only P0-C receipt in place of checkpoint bytes/native load.
6. An earlier-model checkpoint, or missing P0-C campaign, produces `HOLD_CF5_CF1_CURRENT_HEAD_CHECKPOINT_NOT_MATERIALIZED`.

Keep original CF4/P0-C receipts immutable. A current-lineage source string alone does not satisfy this gate.

---

## 4. W9A config digest domain must be established, not assumed

`native_wgpu.rs` presently populates `HeadwiseR3Cf2NativeInvocation.head_checkpoint_digest` by copying `W9AProductionConfig.checkpoint_digest`.

**CONFLICT / NAME VS EVIDENCE:** This is configuration provenance, not itself native proof that P0-C's head-only checkpoint is the same weights consumed by the live model.

Proposed receipt:

```rust
// PROPOSED
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum CheckpointDigestDomainRelationship {
    Unknown,
    IdenticalArtifactProven,
    DistinctArtifactsProven,
}
```

Record separately:

```text
w9a_config_checkpoint_digest
p0c_head_checkpoint_sha256
p0c_head_manifest_seal
live_model_checkpoint_content_digest
live_head_weights_digest
training_source_digest
model_instance / epoch
checkpoint_digest_domain_relationship
```

Do **not** force SHA equality for distinct artifact domains, and do not infer equality from matching 64-character strings. If semantic relationship and actual loading cannot be proved, use `HOLD_CF5_CF1_W9A_CHECKPOINT_DOMAIN_UNBOUND`.

---

## 5. Source-seam decision: protect the 19-input training hash

Preferred approach:

1. Reuse `Observe` mode and natural `NativeWgpuModel`'s selected incremental W9A branch.
2. Use existing public same-step joined observation APIs and existing owned receipts **while the same live model owner is still current**.
3. Add a qualification-only runner/aggregator in `orchestrator_local`, and only narrowly scoped new non-hashed observation support if the source proves such a seam exists.
4. Preserve `crates/model_core/src/native_wgpu.rs` byte-for-byte if possible. **It participates in the 19-input training digest**.
5. Do not change `RequireMeasuredJoin` or `cf2_join_mode` defaults just to produce a PASS.

### Conditional path if no source-preserving seam exists

If the natural selected invocation does not expose the original W8 receipt, actual checkpoint binding, or live device/queue ownership to the observer, record:

```text
HOLD_CF5_CF1_NATIVE_LIVE_SEAM_UNAVAILABLE
```

An authorized follow-up may change `native_wgpu.rs`, but that would require **recomputing all 19 training inputs and establishing a new legitimate checkpoint lineage** before any new live-current-head claim. No digest exemption, string rewrite, aliasing shim or unverified old-weight migration.

This CF1 specification does **not** assert that a source-preserving complete seam already exists.

---

## 6. Original W8 v2 evidence contract

Reuse the existing W8 comparator:

```text
crates/burn_webgpu_backend/src/attention_interconnect_w8_context_parity.rs
AttentionInterconnectW8ContextParityPipeline::compare()
```

Do not add a second comparator or replace it with a synthetic comparator-only test. Require:

```text
compare_dispatch_count      = 1
finalize_dispatch_count     = 1
queue_submit_count          = 1
compact_status_readback     = 1
status_readback_bytes       = 128
full_context_readback_count = 0
queue_callback_registered   = true (real registration)
queue_callback_observed     = true (real callback)
map_callback_observed       = true (real callback success)
gpu_compare_marker         = observed status[25]
gpu_finalize_marker        = observed status[26]
local_scratch_retired       = after both callbacks and map use
```

The local scratch completion proves only that W8-owned scratch is retired; it does not prove **input lease retirement or reuse permission**.

`queue_submission_ordinal: None` is permitted as **unobserved**, not upgraded to a numeric ordinal. Source-generated UUIDs or pointer hashes must not be substituted.

### Queue callback ordering admission

The current W8 source checks `queue_rx.try_recv()` after `device.poll(PollType::Wait)` and a successful map callback. **SOURCE alone does not establish the callback scheduling order across the Queue and MAP callback channels.**

- If the original Queue callback was not observed at the check, classify `FAIL_CF5_CF1_W8_CALLBACK_OR_MAP_UNOBSERVED`; never synthesize success from MAP completion.
- Observe the actual callback/register/notify sequence during native PHYSICAL runs. If a callback-ordering race is demonstrated, repair only the sampled original-W8 completion boundary with an explicit bounded event wait or equivalent **proven** WGPU completion contract. Do not add waits to unsampled/default decode.
- Record timeout/device loss/callback error distinctly; no silent fallback, busy-spin, or host-side mock callback.
- `PollType::Wait` by itself is not proof of the separately observed Queue callback.

Existing numeric contract remains:

```text
query_heads=32, kv_heads=4, GQA=8, head_dim=64
atol=2e-4, rtol=2e-3, relative_floor=1e-4
```

These W8 thresholds must not be replaced with CF3 exact-f32 thresholds. Reject nonfinite counts, comparison statistics, and impossible coverage; preserve original first mismatch indices and layout/source-gating semantics.

---

## 7. Natural W9A sampled selected-path authority

The proof source is the real `NativeWgpuModel` incremental path:

```text
native_wgpu.rs
  W9A configuration snapshot
  -> attention_decode_w9a_layer_eligibility(...)
  -> actual selected Headwise prepared Q/K/V
  -> actual TensorCube Stage12 candidate
  -> w9a_sampled_audit == true
  -> compare_attention_decode_w9a_contexts(...)
  -> original W8 receipt
  -> AttentionDecodeW9ALayerRouteReceipt
  -> record_attention_decode_w9a_layer_receipt_with_cf2_join(...)
```

Rules:

- A fixture manually invoking `AttentionInterconnectW8ContextParityPipeline::compare()` is a **fixture-only** result, not evidence of the selected W9A native route.
- Merely running `ash_attn_decode_w9a_physical_gate` does not prove the same native selected call. Require explicit source-level producer binding to the live invocation before reusing its artifacts.
- Do not artificially rewrite `sampled_audit=true`, canary rates, route ID or eligibility receipt after route selection.
- A legitimately configured qualification campaign may use a source-supported audit sampling policy, but the exact configured policy and natural eligibility decision must be recorded.
- An unsupported/unsampled case is `NotSelected` or `NotMeasured`, **never** a zero-mismatch PASS.

---

## 8. Exact native invocation identity

A qualifying joined observation must bind:

```text
model_instance_id / model_instance_epoch
live_head_checkpoint actually loaded + manifest provenance
tokenizer / current request + decode_session_id / session_epoch
decode_step / layer_index / seq_kv
attention_invocation_generation
cf2_join_policy_generation
candidate_nonce / candidate_invocation_digest
original W8 receipt_digest / pipeline_identity_digest
original W9A receipt_digest
route eligibility / sampled_audit / actual selected route
native Device / Queue currentness
runtime_source_digest / exact binary_sha256
```

`HeadwiseR3Cf2NativeInvocation.same_runtime_handles` is required but not, by itself, a substitute for independently verifiable live physical ownership. Use actual typed owners and generations already produced by the runtime. Where absent: `UNKNOWN` and HOLD.

No cross-session stitching, timestamp-only join, reuse of disk JSON as live pointer, or reconstructing a fake W8 receipt from CF2 summary counts.

---

## 9. Ownership and retention of original receipts

The parent `native_wgpu.rs` retains the original W8 receipt in `cf2_original_w8` within the current native lexical call. CF2's compact joined ledger contains its SHA and selected fields, **not necessarily the entire original W8 receipt**.

For a live CF5-CF1 proof, choose and document one source-proven path:

```text
A. the same live owner produces a typed CF5-CF1 proof before W8/W9A originals leave scope
B. a bounded live owner retains the exact original receipts, with proven source/currentness
C. a source-proven typed handoff carries original owned receipts once to the qualifier
```

If no such path exists without hashed-source edits, emit `HOLD_CF5_CF1_ORIGINAL_RECEIPT_RETAINED_PROOF_UNAVAILABLE`. A CF2 joined JSON with a W8 SHA is **not** sufficient by itself to recreate an original receipt or a same-Queue lease.

For path B/C require bounded retention, exact generation key, once-only consumption, cancel/error retirement, no unbounded per-token ledger and no return of borrowed mapped GPU slices past unmap.

---

## 10. W9A measured status distinct from routing

Record both:

```text
W8 numerical: NotMeasured | MeasuredPass | MeasuredFail | Unavailable
W9A selected route: actual Headwise/TensorCube/rollback route enum
W9A effective admission: actual result and rollback/commit receipt
```

Examples:

```text
W8 MeasuredPass + TensorCubeSampledAudit -> parity-qualified positive leg
W8 MeasuredPass + policy/fault reject     -> measured pass, route rejected
W8 MeasuredFail + HeadwiseRollbackReplay -> valid negative/control leg
W8 missing callback                      -> PHYSICAL HOLD/FAIL, not numeric PASS
W8 unsampled                             -> NotMeasured, no W8 callback proof demanded
```

Do not change current `context_parity_pass`, `eligibility`, `route_id`, `candidate_copy_submit_count`, rollback or pre-sampler behavior.

---

## 11. Exact source digests and actual binary authority

Every physical record must carry:

```text
CF5 full parent ZIP SHA-256
Cargo.lock SHA-256
19-input shared-LM training source digest
CF5/CF1 runtime source digest (including any added Rust/WGSL)
actual built binary SHA-256
actual Device / Queue / adapter identity where available
original W8 compare+finalize shader SHA-256
W8 and W9A receipt seals
checkpoint weight SHA-256 / manifest seal
```

The current CF5 source-only projected runtime digest:

```text
5fdfafa7df13132da4ea53cdf60e2204ce805d940fbf557baac6c0dc8a2cbd1f
```

is an input baseline, **not a physically executed binary hash**. Recompute actual runtime digest after any code changes. Do not copy this string into a new-source receipt as though it describes changed bytes.

---

## 12. Proposed opt-in live campaign API

**Proposed, not present in CF5 parent**:

```rust
// Sketch only. Actual owner types/constructors must be derived from code.
enum HeadwiseCf5Cf1CampaignMode {
    Disabled,
    ObserveNaturalSampled,
    RequireScopedQualification,
}

struct HeadwiseCf5Cf1LiveReceipt {
    source_identity: Cf5Cf1SourceIdentity,
    invocation: HeadwiseR3Cf2NativeInvocation,
    original_w8_digest: Option<String>,
    original_w9a_digest: String,
    checkpoint: Cf5Cf1CheckpointAdmission,
    w8: Cf5Cf1W8Observation,
    join: Cf5Cf1JoinAdmission,
    physical_completion: Option<Cf5Cf1CompletionObservation>,
    first_hold_or_failure: Option<String>,
    production_promoted: bool,
}
```

Start with **ObserveNaturalSampled**. `RequireScopedQualification` may be permitted only at a new qualification-only boundary that has actually consumed the current live owner evidence. It does **not** turn the historical `HeadwiseR3Cf2JoinMode::RequireMeasuredJoin` into a production-ready mode.

No global mutable observer, TLS state, fake runtime handle, process-wide GPU proof cache or automatic promotion on scope entry.

---

## 13. Receipt schema and output discipline

Proposed filename:

```text
headwise_r3_cf5_cf1_live_sampled_physical_receipt.json
```

Fields (with `None` for absent evidence):

```text
schema, patch_id, parent_sha256, cargo_lock_sha256
runtime_source_digest, training_source_digest, binary_sha256
checkpoint_manifest_seal, checkpoint_weights_sha256
checkpoint_domain_relationship, native_checkpoint_load_observed
model_instance, model_epoch, tokenizer_digest, session/step/layer
attention_generation, policy_generation, candidate_nonce
native_device_binding, native_queue_binding
w9a_eligibility_digest, sampled_audit, actual_route
original_w8_receipt_sha256, original_w9a_receipt_sha256
original_cf2_join_sha256, physical_v2_schema
w8_status_words_count, compare_dispatch, finalize_dispatch
queue_submits, queue_callback_registered, queue_callback_observed
map_callback_observed, gpu_compare_marker, gpu_finalize_marker
w8_numerical_status, mismatch_count, first_mismatch, max_abs, max_rel
expected/observed_eligible_layers, expected/observed_sampled_layers
owner_current_before_after, released_after_completion
fixture_only, natural_live_invocation, physical_qualified
first_failure_class, pass_token, receipt_sha256
cf3_p0b_physical, p0c_quality, aof_cf5_c_selected_consumer
cf5_d_active=false, production_promoted=false
```

Use separate artifacts for SOURCE preflight, runtime campaign progress, and physical-completed receipt. Never issue a physical-completed file on preflight or from raw disk audit alone. Publish via a bounded fresh output directory with once-only atomic finalization and byte/checksum verification; no silent overwrite.

---

## 14. Native physical test matrix

| Case | Must observe | Required classification |
|---|---|---|
| N0 | Default Headwise, W9A disabled | `NotSelected` |
| N1 | W9A enabled, canary not eligible | `NotSelected` |
| N2 | Eligible, unsampled TensorCube canary | `NotMeasured` |
| N3 | Naturally sampled W8 numerical PASS | `MeasuredPass` + callbacks + same-call join |
| N4 | Naturally sampled W8 numerical FAIL | `MeasuredFail`, actual rollback/quarantine |
| N5 | W8 measured PASS + W9A effective reject | Numerical PASS separate from route reject |
| N6 | Sampled comparator returns error | `MeasurementUnavailable` or explicit failure |
| N7 | Map callback failure / queue callback absent | Physical failure, no forged completed receipt |
| N8 | Device lost before completion | Terminal HOLD/FAIL, no premature resource reuse |
| N9 | Different model/session/step/layer/nonce | Stale/wrong-source rejection |
| N10 | Policy generation changes in-flight | Rejected, no cross-policy join |
| N11 | Missing checkpoint or wrong digest domain | Live-lineage HOLD |
| N12 | Repeated fresh sessions and eligible layers | Bounded coverage, no duplicate join |
| N13 | EOS / cancellation / stop / emit failure | Canonical token/KV/stop behavior preserved |
| N14 | Wrong Queue/owner/input completion generation | Fail-closed currentness |

Never claim the matrix ran because the static validator contains corresponding tests. For device-loss cases requiring external fault stimulation, mark **NOT_RUN** unless physically observed; negative source mutations are not GPU failure reproduction.

A N3 PASS cannot erase a N4 measured mismatch; classify each leg and any aggregate according to its defined scenario.

---

## 15. Layer/step cardinality and evidence truth

Freeze before execution:

```text
expected model layer count
eligible layer count/source
sampled layer count/source
per-step selected W9A route and exact layer indexes
per-layer W8 original receipt expected when sampled
per-layer original W9A receipt expected
per-layer CF2 join receipt expected in Observe mode
```

A legitimate `NotSelected`/`Unsampled` layer is not missing W8 evidence, but it **cannot** contribute to the sampled-PASS denominator. Missing an actually selected sampled layer is HOLD/FAIL, not zero mismatch. One selected layer's PASS cannot be projected onto all layers/depths.

---

## 16. Canonical decode/lifecycle invariants

CF5-CF1 changes no:

```text
canonical KV owner, append, commit or rollback
Headwise selected context semantic math
TensorCube candidate math and GQA mapping
AOF FuturePool or prefix acceptance
EOS / stop-sequence / cancellation / emit ACK
W9A route eligibility or sampling policy
W9A pre-sampler commit/rollback policy
W8 existing tolerances or status ABI
```

Retirement applies to the actual owner generation. `Drop` of Rust objects, JSON receipt serialization and successful `PollType::Wait` do not prove all dependent input leases are reusable. Record the specific owner whose retirement is observed.

When a terminal failure occurs after some canonical publication, preserve already-published canonical state without duplicate token/KV commit. Distinguish cancel before publication from cancel after partial publication.

---

## 17. Source touchpoints and no unnecessary rewrites

### Confirmed existing owners

```text
crates/burn_webgpu_backend/src/attention_interconnect_w8_context_parity.rs
crates/model_core/src/headwise_r3_cf2_native_join.rs
crates/model_core/src/native_wgpu.rs   [19-input training digest member]
crates/model_core/src/aof_r1_admission.rs
crates/orchestrator_local/src/headwise_r3_cf5_physical_join.rs
crates/orchestrator_local/src/headwise_r3_cf4_p0c_physical_receipt.rs
crates/orchestrator_local/src/bin/ash_headwise_r3_cf5_physical_join_gate.rs
crates/orchestrator_local/src/bin/ash_headwise_r3_cf4_p0c_gate.rs
crates/orchestrator_local/src/bin/ash_attn_decode_w9a_physical_gate.rs
```

### Proposed narrow additions (create only where necessary)

```text
crates/orchestrator_local/src/headwise_r3_cf5_cf1_live_qualification.rs
crates/orchestrator_local/src/bin/ash_headwise_r3_cf5_cf1_live_gate.rs
tools/validate_ash_headwise_r3_cf5_cf1_live_static.py
```

Existing CF5 source `preflight`/`audit` APIs remain; the proposed new `--run` must not be advertised as already implemented. Avoid touching `native_wgpu.rs` unless the exact live authority seam cannot otherwise be established and an explicit new-lineage decision is made. No global refactor of Headwise, W8/W9A or AOF systems in CF1.

---

## 18. Source/static negative gates

Reject at least:

```text
NATIVE_ORIGINAL_W8_NOT_ACTUALLY_SAMPLED
JOIN_FROM_DISK_AS_LIVE_PERMIT
W8_V1_RECEIPT_UPGRADED_TO_V2
MAP_CALLBACK_AS_QUEUE_CALLBACK
GPU_STATUS_MARKER_AS_CALLBACK
SYNTHETIC_QUEUE_SUBMISSION_ORDINAL
W9A_CONFIG_DIGEST_AS_TRAINED_HEAD_CHECKPOINT_PROOF
OLD_CHECKPOINT_MANIFEST_RESEALED_NEW_SOURCE
WRONG_MODEL_OR_TOKENIZER_SOURCE
WRONG_DEVICE_OR_QUEUE_OWNER
STALE_SESSION_EPOCH_OR_NONCE
POLICY_GENERATION_CHANGED_IN_FLIGHT
DUPLICATE_SAMPLED_LAYER_JOIN
MISSING_APPLICABLE_SAMPLED_LAYER
PRECOMPLETION_RESOURCE_REUSE
CF3_EXACT_F32_USED_AS_W8_TOLERANCE
UNAUTHORIZED_TOLERANCE_RELAXATION
FULL_CONTEXT_D2H_ADDED
EXTRA_SAMPLED_W8_COMPARATOR
PRODUCTION_DEFAULT_REQUIRE_MEASURED_JOIN_ENABLED
CF5_D_ACTIVE_PREMATURE
```

Historical CF2 static `no_unobserved_queue_callback` is superseded by CF5 v2 callback semantics; preserve its old versioned receipt compatibility, but do not relabel the old 40/41 test as PASS for new source.

---

## 19. Native build and shader qualification

The following existing steps may be run on the **exact parent source** after restoring real external workspace dependency paths (including `vendor/sherpa-rs-main/crates/sherpa-rs`). No dummy crate:

```powershell
python .\tools\validate_ash_headwise_r3_cf5_physical_join_static.py --negative-tests
python .\tools\validate_ash_headwise_r3_cf4_p0c_static.py --negative-tests
python .\tools\validate_ash_headwise_r3_cf3_p0b_physical_static.py --negative-tests
cargo metadata --format-version 1 --locked
cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo check -p model_core --lib --release --locked -j 1
cargo check -p orchestrator_local --lib --release --locked -j 1
cargo build -p orchestrator_local --bin ash_headwise_r3_cf5_physical_join_gate --features orchestrator_aof_r1_audit_bins --release --locked -j 1
cargo build -p orchestrator_local --bin ash_headwise_r3_cf4_p0c_gate --features orchestrator_aof_r1_audit_bins --release --locked -j 1
cargo test -p model_core --lib headwise_r3_cf2 --release --locked -j 1
cargo test -p burn_webgpu_backend --lib attention_interconnect_w8 --release --locked -j 1
```

Validate the exact W8 `attention_interconnect_w8_context_compare.wgsl`, `attention_interconnect_w8_first_mismatch_finalize.wgsl` and any modified WGSL under native Naga/WGPU26. Distinguish shader parsing, pipeline validation, dispatch and numeric result.

**Proposed successor commands after code implementation, NOT currently runnable:**

```powershell
# Only after a real CF5-CF1 binary + static tool exist
python .\tools\validate_ash_headwise_r3_cf5_cf1_live_static.py --negative-tests
cargo build -p orchestrator_local --bin ash_headwise_r3_cf5_cf1_live_gate --features orchestrator_aof_r1_audit_bins --release --locked -j 1
.\target\release\ash_headwise_r3_cf5_cf1_live_gate.exe --preflight <ACTUAL_CAMPAIGN_JSON>
.\target\release\ash_headwise_r3_cf5_cf1_live_gate.exe --run <ACTUAL_CAMPAIGN_JSON>
```

Do not infer executable success from the specification. Existing `ash_headwise_r3_cf5_physical_join_gate --audit` remains an **audit-only** tool, not a shortcut to physical PASS.

---

## 20. Required physical run sequence

```text
G0  Freeze exact parent/source/Cargo.lock/output campaign and numerical policy
G1  cargo metadata, release Rust checks and tests; Naga/WGPU pipeline gates
G2  Real P0-C fresh two-rank head-only training + checkpoint manifests
G3  Real native evaluator four-horizon quality + Queue completion receipts
G4  Bind the actually loaded live model/head and W9A config digest domains
G5  Start fresh real NativeWgpuModel session + CF2 Observe before decode
G6  Exercise eligible W9A sampled route naturally; original W8 callback/map
G7  Consume original W8/W9A typed proof in same live owner/generation
G8  Verify W8 numerical result separately from W9A selected route
G9  Verify layer/step coverage, rollback, duplicate/stale and retirement
G10 Publish one scoped CF5-CF1 receipt with exact first failure/source
```

If G2/G3 is unmaterialized, later steps may produce explicitly labeled diagnostics but no **live-current-head physical PASS**. If the natural session never samples, stop with `HOLD_CF5_CF1_NATURAL_SAMPLED_ROUTE_NOT_OBSERVED`. If G7 cannot be implemented without hashed-source mutation, stop with `HOLD_CF5_CF1_NATIVE_LIVE_SEAM_UNAVAILABLE` and separately approve new lineage work.

---

## 21. Physical PASS scope and failure classes

### Positive scoped token (reserved, NOT yet issued)

```text
PASS_HEADWISE_R3_CF5_CF1_CURRENT_LINEAGE_LIVE_W8_W9A_SAME_CALL_PHYSICAL
```

Only for the **exact actual model/session/selected layer set** when:

```text
SOURCE      exact original W8 and CF2 same-invocation W9A code
STATIC      all current and negative gates valid
COMPILE     actual Rust release target qualified
NAGA        exact shaders/pipelines validated
CHECKPOINT  legitimate real current-lineage checkpoint + manifest
LIVE LOAD   the checkpoint was actually loaded/current in this session
W9A         natural eligible sampled selected route observed
W8          original matched comparison completed, numeric PASS
CALLBACK    same Queue callback and MAP callback both actually observed
GPU STATUS  128-byte compare/finalize marker, finite and full coverage
CURRENTNESS model/session/step/layer/nonce/policy/device/queue match
LIFETIME    original owners current through completion, retirement valid
RECEIPT     sealed exact binary/source/weights/invocation proof
```

A valid measured **failure/rollback** leg may be reported as its own negative/control PASS, but never as `W8 numeric PASS`.

Required HOLD/failure classes:

```text
HOLD_CF5_CF1_CURRENT_HEAD_CHECKPOINT_NOT_MATERIALIZED
HOLD_CF5_CF1_W9A_CHECKPOINT_DOMAIN_UNBOUND
HOLD_CF5_CF1_NATIVE_LIVE_SEAM_UNAVAILABLE
HOLD_CF5_CF1_ORIGINAL_RECEIPT_RETAINED_PROOF_UNAVAILABLE
HOLD_CF5_CF1_NATURAL_SAMPLED_ROUTE_NOT_OBSERVED
HOLD_CF5_CF1_INCOMPLETE_SELECTED_LAYER_COVERAGE
HOLD_CF5_CF1_BINARY_OR_SOURCE_NOT_EXACT
FAIL_CF5_CF1_W8_CALLBACK_OR_MAP_UNOBSERVED
FAIL_CF5_CF1_W8_STATUS_OR_NUMERICAL_DRIFT
FAIL_CF5_CF1_W8_W9A_INVOCATION_OR_DIGEST_DRIFT
FAIL_CF5_CF1_DEVICE_QUEUE_OR_OWNER_DRIFT
FAIL_CF5_CF1_DUPLICATE_JOIN_OR_EARLY_RETIREMENT
FAIL_CF5_CF1_CHECKPOINT_MANIFEST_OR_SOURCE_MISMATCH
FAIL_CF5_CF1_PREMATURE_PRODUCTION_OR_CF5D_PROMOTION
```

No `PASS` when the source or physical authority for a mandatory field is `None`/`UNKNOWN`.

---

## 22. Performance and cost attribution (non-promoting)

Report only actual observations:

```text
sampled W8 compare/finalize dispatch count
W8 Queue submit / callback register / callback completed
W8 128-byte status D2H and map callback count
W8 blocking poll/callback wait wall
the selected production decode wall (if actually measured)
W9A canary/audit selection cardinality and outcome
CF2 joined ledger entries / peak / retirement
VRAM transient allocation peak (if measured)
full-context D2H count, extra W8 comparator count
binary/source/device/queue identity for each sample
```

The sampled route's existing MAP wait is a known source-level cost; no measurable speedup follows merely from new callback evidence. No hidden CPU fallback or numeric tolerance relaxation.

---

## 23. Completion and successor law

**CF5-CF1 completion is only a scoped live same-invocation W8/W9A physical qualification,** not an all-Headwise closure.

Independent gates remain:

```text
HEADWISE-R3-CF3-P0B  independent selected Short32/Long64 output GPU parity
HEADWISE-R3-CF4-P0C  real two-rank checkpoint lineage + quality + evaluator Queue
HEADWISE-R3-CF5-CF1  real natural sampled W8/W9A same-call GPU evidence
AOF-R1-CF5-C       native selected Headwise/TensorCube capacity consumer parity
AOF-R1-CF5-D       canonical capacity-strided ACTIVE (separate later approval)
```

After CF5-CF1 PHYSICAL has legitimately completed, the next **specification** may be `HEADWISE-R3-CF6 INDEPENDENT AGGREGATE PHYSICAL CLOSURE` to combine independently sealed status axes and precise coverage, without recomputing or inventing missing evidence. Neither CF5-CF1 nor CF6 implicitly enables AOF CF5-D.

**Final invariant:**

```text
ACTUAL CURRENT-LINEAGE LOADED HEAD
+
NATURAL SELECTED LIVE W9A SAMPLED INVOCATION
+
ORIGINAL W8 V2 NUMERICAL + QUEUE/MAP GPU COMPLETION
+
ORIGINAL W9A ROUTE RECEIPT
+
SAME-CALL SAME-OWNER/GENERATION CF2 JOIN
+
BOUNDED PROVENANCE + RESOURCE RETIREMENT
=
EXACT-SCOPE CF5-CF1 LIVE PHYSICAL QUALIFICATION

NOT = CF3 SELECTED-OUTPUT PHYSICAL
NOT = P0-C QUALITY AUTOMATIC PROMOTION
NOT = AOF CF5-C SELECTED CAPACITY CONSUMER
NOT = AOF CF5-D ACTIVE
NOT = GENERAL HEADWISE PRODUCTION CUTOVER
NOT = PERFORMANCE IMPROVEMENT
```

**Document state:** specification drafted from the actual CF5 full code-only ZIP, CF5 bake report/manifest and the previously established P0-C/CF3 contracts. This file is a new proposal; no code modification, Rust/Naga execution, live checkpoint generation, GPU run or GitHub commit is represented as completed.

---

## 24. Exact SOURCE bake annex (2026-10-09)

### 24.1 Evidence boundary

**PARTIAL SOURCE BAKE, NOT PHYSICAL CLOSURE.** The source implements a scoped read-only `NativeWgpuModel` audit adapter and an opt-in source-only preflight CLI. It does not construct a true natural native W9A generation session, reconstruct a missing full original W8 owned receipt, or prove P0-C head-only weights are actually loaded into the live model. Therefore CF5-CF1 A5/A6 **remain HOLD** and no physical PASS token is emitted. No Rust COMPILE, Naga, GPU campaign, checkpoint training, native load, physical callback observation or performance measurement was executed.

### 24.2 Exact source and packaging

| Artifact | SHA-256 | Entries / CRC |
|---|---|---|
| Parent CF5 full ZIP | `7f4e3186befe8313c34923a7ad03475e803e19724737a7b16e68466ce10d7447` | 8,767 / PASS |
| CF5-CF1 full code-only ZIP | `97b5002b4bfc664e55c384d5fcd70e808f6b79c68f6ab3454b24247ab544f372` | 8,770 / PASS |
| CF5-CF1 overlay code-only ZIP | `fc6f446f5c0ee12a0f395029cd2b7e42869f1f331b1568aff26e9a152838df6f` | 5 / PASS |

Actual delta relative to the exact parent:

```text
MOD crates/model_core/src/aof_r1_admission.rs
MOD crates/orchestrator_local/Cargo.toml
ADD crates/orchestrator_local/src/headwise_r3_cf5_cf1_live_qualification.rs
ADD crates/orchestrator_local/src/bin/ash_headwise_r3_cf5_cf1_live_gate.rs
ADD tools/validate_ash_headwise_r3_cf5_cf1_live_static.py
DEL 0
```

The original 19-input training-source set, `native_wgpu.rs`, original W8 comparator/shaders, CF2 join source, CF5 audit source and P0-C evaluator are byte-identical to the parent. The `aof_r1_admission.rs` runtime-source digest now includes the opt-in CF5-CF1 Rust module and binary. Its **SOURCE-only projected digest** on these exact bytes is:

`a53f1c993abbb3fb7a04b671522768c824e57854da500220d7b7ed62d212d014`

This is **not** a compiled binary hash, runtime observation or native adapter identity. The 19-input training digest remains:

`0b10d1d645ce22356ca4c44bc9e0e4c4ef109f6daf9d143175cd5c9cc1a41094`

### 24.3 Implemented SOURCE surfaces

`headwise_r3_cf5_cf1_live_qualification.rs::observe_native_step(&NativeWgpuModel, &Cf5Cf1StepRequest)` borrows an actual live native model supplied by its owner and observes the existing native W9A route receipt and bounded CF2 same-call join ledger. It validates original W9A receipt seal, CF2 join receipt seal, model instance/epoch, session/step/layer, source digest, policy generation/nonce, sampled status, distinct W8 Queue/Map/GPU status sources, and actual `PhysicalWgpuRuntimeBindingR1` captured from current runtime handles. It rejects duplicate/incomplete requested diagnostic layer observations and performs a final model/handle currentness check.

**Limits:** The caller-supplied list of expected layer indices is **diagnostic only**; it is not evidence of the full eligible model layer cardinality. The CF2 compact join does not retain the full owned W8 GPU receipt or prove the input Q/K/V leases have been retired. The loaded head-only checkpoint is not established merely by a W9A configuration checkpoint digest or by a verified base-model binding. Consequently every audit record keeps `same_call_physical_join_qualified=false`, `original_w8_full_receipt_retained=false`, `original_input_lease_retirement_observed=None`, `checkpoint_digest_domain_relationship=UNKNOWN`, `physical_pass_token=None`.

`ash_headwise_r3_cf5_cf1_live_gate` accepts:

```powershell
ash_headwise_r3_cf5_cf1_live_gate.exe --preflight <repo-root> <exact-parent.zip> <fresh-output-dir>
```

This requires the exact parent archive SHA, matches embedded build source bytes against the checkout, reports runtime/training source identities, and uses once-only receipt publication. It **does not** initialize a GPU Device. Its `--run <native-campaign.json>` currently returns `HOLD_CF5_CF1_NATIVE_LIVE_SEAM_UNAVAILABLE`. No caller JSON string or disk receipt can authorize a physical session. An actual native generation owner must invoke the scoped `observe_native_step()` seam and expose the original W8 receipt and loaded head checkpoint under a distinct, explicitly approved follow-up before physical promotion can be considered. The caller cannot synthesize those authorities in CF5-CF1.

### 24.4 Executed static and regression tests

```text
CF5-CF1 STATIC                54/54 PASS
CF5-CF1 negative mutations    39/39 rejected
Exact-parent byte delta       2 MOD / 3 ADD / 0 DEL
P0-A STATIC                   60/60 PASS
P0-B STATIC                   45/45 PASS
P0-C STATIC                   44/44 PASS
CF5 parent STATIC             51/51 PASS
CF2 historical                40/41 (superseded always-None callback gate; not rewritten)
Rust COMPILE                  NOT_RUN (rustc/cargo not installed)
Native Naga                   NOT_RUN
Real W8/W9A GPU               NOT_RUN
P0-C trained checkpoint       NOT_PROVIDED
CF5-CF1 PHYSICAL PASS         HOLD
AOF CF5-D ACTIVE              false
Production promoted           false
```

Static negative mutation rejection does not count as actual GPU device-loss, stale-resource, callback-order or numerical behavior. The scope of in-process model inspection is SOURCE only until an actual caller invokes it.

### 24.5 Windows next-execution commands (NOT_RUN)

Run only with the exact external workspace dependency restored, without a dummy crate:

```powershell
python .\tools\validate_ash_headwise_r3_cf5_cf1_live_static.py --negative-tests
cargo metadata --format-version 1 --locked
cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo check -p model_core --lib --release --locked -j 1
cargo check -p orchestrator_local --lib --release --locked -j 1
cargo build -p orchestrator_local --bin ash_headwise_r3_cf5_cf1_live_gate --features orchestrator_aof_r1_audit_bins --release --locked -j 1
cargo test -p orchestrator_local --bin ash_headwise_r3_cf5_cf1_live_gate --features orchestrator_aof_r1_audit_bins --release --locked -j 1
.\target\release\ash_headwise_r3_cf5_cf1_live_gate.exe --preflight . <EXACT_CF5_PARENT_ZIP_PATH> <FRESH_OUTPUT_DIR>
```

`--run` is NOT an available physical GPU campaign. It returns an explicit HOLD by design. Do not report `PASS_HEADWISE_R3_CF5_CF1_CURRENT_LINEAGE_LIVE_W8_W9A_SAME_CALL_PHYSICAL` until the unimplemented live owner/retained receipt/checkpoint gates plus real native hardware matrix have been separately completed. The next actionable engineering blocker is **the natural W9A selected-session producer/owner handoff**, without silently changing the 19-input training digest or global mode.

**GitHub boundary:** the intended GitHub commit contains this specification and factual SOURCE-bake annex only; the code-only archives remain separate user artifacts. A spec commit is not evidence of source being committed to the repository.
