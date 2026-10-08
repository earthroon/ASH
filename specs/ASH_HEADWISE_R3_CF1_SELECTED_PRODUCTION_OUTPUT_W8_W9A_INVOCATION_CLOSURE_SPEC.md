# HEADWISE-R3-CF1
## SELECTED PRODUCTION OUTPUT QUALIFICATION + W8/W9A SAME-INVOCATION EVIDENCE CLOSURE

**Patch ID:** `HEADWISE-R3-CF1`  
**Direct parent:** `HEADWISE-R3 SUBGROUP32 ADMISSION + W9A PARITY EVIDENCE TRUTH`  
**Successor:** `AOF-R1-CF5-C-R4` only after the applicable selected Headwise/TensorCube consumers are qualified; otherwise a narrower CF1 follow-up  
**Class:** GPU production-output proof, callback provenance, native comparison provenance, checkpoint lineage qualification  
**Status (2026-10-09): PARTIAL SOURCE BAKE / STATIC 42/42 PASS, 21/21 negative-source rejections.** Selected production shader bounded fixture and W8 receipt validation are implemented as SOURCE candidates, but canonical reference provenance, W8→W9A exact same-invocation join and physical execution remain **HOLD / NOT_RUN**. Full CF1 PASS and production promotion are forbidden.

## 0. Exact parent and evidence boundary

Parent code-only artifact:

`ASH_PASS3_HEADWISE_R3_SUBGROUP32_ADMISSION_W9A_PARITY_EVIDENCE_TRUTH_CODE_ONLY.zip`

Parent ZIP SHA-256:

`752184f8e7ea4d25e647c3c5e8f2ea0e8863a6dfd2478a2cb5490b01037e7c9b`

Parent file count: `8,743`.

Parent evidence:

- HEADWISE-R3 SOURCE/STATIC `37/37 PASS`; negative mutations `22/22 rejected`.
- HEADWISE-R1 `38/38 PASS` and HEADWISE-R2 `22/22 PASS`, both SOURCE/STATIC only.
- Existing 19-input head training digest `e20f93b19bcb8a93a96809a28d2faf5c72c68896da060002d36a43e2286b8283`.
- Legacy CF5-C-R1 gate `64/66 FAIL` under the HEADWISE-R2 selected causal/full-staged policy supersession, not a newly passing gate.
- Rust COMPILE, Naga, real GPU PHYSICAL, selected-output numeric parity and W8/W9A same-invocation binding all `NOT_RUN` or `UNKNOWN`.

These states shall not be upgraded because the present CF1 source is written or a static validator passes.

## 1. Scope declaration

```text
HEADWISE-R3-CF1

+ R1 SCORE POLICY / R2 CHUNKED VISIBILITY PRESERVATION
+ R3 SHORT32 / LONG64 PROXY TOPOLOGY WITNESS PRESERVATION
+ PROXY CONFIGURED-VALUE / PHYSICALLY-OBSERVED-VALUE SEPARATION
+ MAP CALLBACK / QUEUE COMPLETION PROVENANCE SEPARATION

+ EXACT SELECTED PRODUCTION PIPELINE BINDING
+ SHORT32 AND LONG64 SELECTED-PRODUCTION OUTPUT-WRITE WITNESS
+ QUALIFICATION-ONLY BOUNDED OUTPUT SENTINEL CHECK
+ EXISTING SELECTED OUTPUT FINITE-GUARD CONTINUITY
+ SCORE-POLICY / VISIBILITY-MATCHED NUMERICAL PARITY
+ NO PROXY-PASS-TO-PRODUCTION-PASS PROMOTION

+ REAL W8 BACKEND COMPARATOR RECEIPT CAPTURE
+ EXACT W8 INVOCATION → W9A SESSION/STEP/LAYER JOIN
+ W8 COMPARISON COMPLETION / IDENTITY / DIGEST CHECK
+ W9A NOT_MEASURED / MEASURED_PASS / MEASURED_FAIL TRUTH
+ LEGACY W9A ROUTING / PRE-SAMPLER POLICY PRESERVATION

+ HEAD TRAINING CHECKPOINT DIGEST PRESERVATION FIRST
+ EXPLICIT LINEAGE MIGRATION HOLD IF NATIVE_SEAM REQUIRES CHANGE
+ NO FULL CONTEXT HOST READBACK
+ NO NEW PER-TOKEN DIAGNOSTIC GPU WAIT
+ NO CF5-D ACTIVE / PRODUCTION DEFAULT / PERFORMANCE PROMOTION
```

### Non-goals

- Do not change Headwise-R1 `LegacyTextDensityAdjusted` default to `CanonicalGqa`.
- Do not change Headwise-R2 `LegacyFullStaged` default to `CausalSnapshotBound`.
- Do not change original W9A canary/audit/rollback selection rules or existing `context_parity_pass` routing gate.
- Do not activate CF5 capacity-strided canonical KV consumers or rewrite token/KV/stop/emit publication.
- Do not treat the presence of a shader source as Naga/runtime execution.
- Do not infer physical GPU bandwidth, kernel execution time or tokens/s changes from a source patch.

## 2. SOURCE-confirmed parent callsites

**Selected production dispatcher:**

- `crates/burn_webgpu_backend/src/headwise_atlas.rs`
- `HeadwiseAtlasDispatcher::production_pipeline_bundle(long_kv_tiled)` chooses the actual shader module and compiled pipeline.
- `encode_prepared_into_output_lease_with_route()` chooses the actual route, calls `enforce_r3_subgroup_selected_family(long_kv_tiled)`, creates the pipeline/bind group and encodes the actual output dispatch.
- `dispatch_prepared_into_output_lease()` submits a command buffer; separate device-guarded routes already encode a finite guard and completion ticket.

**Proxy qualification:**

- `crates/burn_webgpu_backend/src/headwise_r3_subgroup_admission.rs`
- `run_r3_subgroup_family_probe()` writes width/lane/local-index words in a separate 32/64-workgroup proxy shader, reads a bounded staging buffer, and stores a dispatcher-local receipt.
- Its `actual_workgroup_size` is assigned `family.workgroup_size()` by Rust, not decoded from a GPU-observed workgroup-size field.
- Its `completion_callback_observed=true` follows a successful `map_async` callback. It does not currently install an independent `Queue::on_submitted_work_done` callback.
- The receipt correctly keeps `selected_production_output_qualified=false` and `pass_token=None`.

**W8 comparator:**

- `crates/burn_webgpu_backend/src/attention_interconnect_w8_context_parity.rs`
- `AttentionInterconnectW8BackendParityReceipt` contains `invocation_identity_digest`, pipeline identity, compare coverage, mismatch and finite counts, first mismatch, completion observation, `pass`, and sealed digest.

**W9A selected route:**

- `crates/model_core/src/native_wgpu.rs::compare_attention_decode_w9a_contexts()` invokes W8 and receives a local receipt during sampled audit.
- `crates/model_core/src/attention_decode_w9a_production_runtime.rs::AttentionDecodeW9ALayerRouteReceipt` binds `decode_session_id`, `decode_session_epoch`, `decode_step`, `layer_index`, route and sampled audit, but not W8's invocation identity.
- `crates/model_core/src/headwise_r3_w9a_parity_evidence.rs` correctly returns `NotMeasured` or `MeasurementUnavailable` without manufacturing `MeasuredPass`.

## 3. CF1-A0: Proxy receipt truth repair

Current `actual_workgroup_size` shall not be used as evidence of an observed WGPU value without a producer.

A replacement schema (or a strict backward-compatible extension) shall distinguish:

```rust
struct HeadwiseR3Cf1ProxyWitness {
    configured_workgroup_size: u32,
    gpu_observed_subgroup_widths: Vec<u32>, // bounded 1–2 subgroup entries
    observed_invocation_count: u32,
    gpu_lane_mapping_pass: bool,
    map_callback_observed: bool,
    queue_completion_callback_observed: Option<bool>,
    selected_production_output_qualified: bool, // remains false for proxy
}
```

- `configured_workgroup_size` originates from the selected family/entry point.
- `gpu_observed_subgroup_widths` is calculated only from actual mapped words; none observed means `UNKNOWN/HOLD`, never `[32]` by literal.
- A successful mapping may provide dependency-ordering evidence for the readback; do not mislabel it as the observation of a callback that was never registered.
- If an existing field is retained for compatibility, classify its origin explicitly and prohibit it from satisfying `selected_production_output_qualified`.
- Existing R3 proxy canary remains audit evidence and a first-dispatch guard, not a substitute for this CF1's selected output witness.

**Semantic classification:** telemetry schema/source truth change, not numerical or routing change.

## 4. CF1-A1: Exact selected production pipeline authority

Proof shall bind to the **real pipeline chosen by** `production_pipeline_bundle(long_kv_tiled)`, not a newly compiled proxy whose source happens to resemble it.

Required in-memory authority key:

```text
same Device owner + Queue owner
selected Short32 or LongGqa2_64 family
exact shader source SHA-256
actual WGSL entry point (`main`)
workgroup geometry (32 or 64)
selected Headwise kernel route / route-LUT digest
R1 score policy + ABI layout revision
R2 visibility policy + causal-position epoch when relevant
selected pipeline object/generation or equivalent exact currentness
qualification fixture shape/layout domain
```

If selected shader bytes, pipeline, score ABI, Device/Queue, route geometry or owned dispatcher generation changes, invalidate the live proof. Disk JSON cannot recreate live `Qualified` state.

`HeadwiseR3SubgroupFamily::selected_shader_source()` may provide source bytes, but a digest alone does **not** prove the already cached `ComputePipeline` is the same runtime object.

## 5. CF1-A2: Qualification-only selected output witness

Use the **actual selected Headwise production pipeline and bind layout** with a fresh bounded qualification output buffer. This is not a separate approximate reimplementation of the attention math.

One qualification fixture shall:

1. Create an actual Q/K/V fixture with declared finite values, selected shape, correct GQA grouping and matched causal snapshot.
2. Allocate a fresh candidate output with all logical output scalars initialized to a deliberately invalid bit-pattern sentinel, e.g. a quiet-NaN representation whose result cannot qualify as finite.
3. Encode the selected production shader (Short32/Long64) into that output and record actual route, pipeline and output identity.
4. Observe GPU submission, actual operation completion and correct staging-buffer lifecycle.
5. Run a bounded GPU status reduction over the **same output**, checking per-logical-scalar sentinel survival, visited/coverage count, NaN/infinity count, output bounds, first missing/mismatching location, and optional reference parity.
6. Read back only the fixed-size status/evidence record. No entire context buffer readback.
7. Retire qualification output and staging resources before reusing their slots.

Required:

```text
status.did_selected_shader_execute == physically observed
status.expected_output_elements > 0
status.observed_output_elements == status.expected_output_elements
status.unwritten_sentinel_count == 0
status.non_finite_count == 0
status.out_of_bounds_count == 0
status.actual_submission_observed == true
status.actual_completion_observed == true
```

The concrete sentinel and reduction mechanics must be verified with actual buffer initialization/usage, storage binding rules and Naga. A `finite_guard_pass` on a zero-filled output alone cannot prove that the shader wrote every expected element.

**Fixture authority limitation:** a successful single-size fixture proves that selected pipeline/shape's output; it is not automatic proof of every batch, position or long-KV band. Publish its explicit coverage domain.

## 6. CF1-A3: Selected output numerical qualification

Qualification compares real selected Headwise output with a reference that has **the same score and visibility semantics**.

- For `CanonicalGqa`, compare to canonical Burn GQA under equivalent Q/K/V, layout and causal policy.
- For `LegacyTextDensityAdjusted`, either compare to a reference that executes exactly the same TextDensity multiplier/order, or report numeric parity `UNQUALIFIED`; do not compare different models' math and relax tolerance until it passes.
- For chunked Q>1, use matching `LegacyFullStaged` or `CausalSnapshotBound` visibility on both sides. Do not call R2 causal mode's full-stage result a parity reference.
- Short32 and Long64 shall each have actual selected route coverage. Long64 also proves the selected subgroup ID/lane→query-head mapping for that exact compiled shader.
- Record finite counts, output coverage, observed maximum absolute/relative error, mismatch count, first mismatch and the pre-existing applicable tolerance authority. Do not invent a new global acceptance threshold.

A qualification-only readback/reduction is allowed. It must be separately accounted for and **not** added to ordinary per-token hot path without an explicitly justified policy.

## 7. CF1-A4: Strict selected-production mode integration

Current `HeadwiseR3SubgroupAdmissionMode::RequireSelectedProductionOutput` fails with:

`HOLD_HEADWISE_R3_SELECTED_PRODUCTION_OUTPUT_NOT_QUALIFIED`

CF1 shall allow it to proceed only after a **live, current, actual selected-production proof** exists.

Suggested lifecycle:

```text
Unknown
→ ProxyObserved
→ SelectedPipelineQualifiedFixturePending
→ SelectedOutputWrittenAndCompared
→ SelectedOutputQualified
→ SelectedProductionDispatchEligible
```

Failure transitions lead to explicit `Rejected` or `PendingResourceRetirement`; never force `Qualified` from proxy receipt data or from a time delay.

A normal production dispatch still requires its existing output guard and real completion/publication contract. A fixture PASS alone does not prove that a subsequent production output's bytes were written; bind the actual dispatch receipt + finite-guard coverage + generation to the qualified selected pipeline.

Do not introduce a recursive attempt to dispatch the qualifier through an admission guard that requires qualification of itself. Keep a narrowly scoped, nonpublishing fixture authority distinct from canonical Headwise publication.

Default Headwise/R1/R2 policies and R3 `RequireFamilyTopologyProbe` default remain unchanged. CF1's strict selected-production admission is explicit/opt-in until separately promoted.

## 8. CF1-A5: Lifetime and no-hidden-hot-path-cost law

The preflight is bounded by selected pipeline/route identity and occurs at qualification boundaries, not on every generated token.

Record separately:

```text
qualifier_submit_count
qualifier_status_readback_count
qualifier_map_callback_count
qualifier_queue_completion_callback_count (None when not observed)
qualifier_wall_ns
normal_selected_dispatch_count
normal_hot_path_extra_submit_count
normal_hot_path_extra_d2h_bytes
normal_hot_path_extra_exact_wait_count
```

Qualification-time I/O shall not be falsely merged into normal token throughput. A queue completion can be proven through the correct WGPU completion/retirement authority, but the receipt must state which mechanism was observed.

On map/submit/validation/device-loss failure, retain in-flight owners until safe retirement or explicit terminal quarantine. No unproven reuse and no success-shaped zero counter.

## 9. CF1-B0: Existing W8 comparator receipt authority

`AttentionInterconnectW8BackendParityReceipt` is already an actual-source result type; do not duplicate W8 context math merely to fill W9A telemetry.

Required original fields for B:

```text
invocation_identity_digest
pipeline_identity.identity_digest
context_element_count
compared_scalar_count
mismatch_count
max_absolute_error / max_relative_error
first_mismatch
non_finite / mapping / causal violation counts
queue_submit_count
compact_status_readback_count
full_context_readback_count
comparison_completion_observed
pass
receipt_digest
```

The receipt must validate its original digest domain and its actual operation completion. A `pass=true` field without correct invocation binding is not sufficient evidence for a W9A layer.

## 10. CF1-B1: Exact native W8→W9A join contract

The local `native_wgpu.rs::compare_attention_decode_w9a_contexts()` receives W8's parity receipt during a `w9a_sampled_audit` branch. The eventual W9A layer receipt is sealed later in the same native function, but currently lacks a W8 invocation reference.

A valid join must be established at a **real common in-memory call boundary** and bind:

```text
model owner + model-instance epoch
source/runtimes digest
DecodeSessionID + session_epoch
DecodeStep + layer_index
attention-invocation generation
W8 invocation_identity_digest
W8 backend comparator receipt_digest
W8 actual completion observation
W9A route and sampled_audit flag
W9A existing sealed layer receipt_digest
Device/Queue owner (when physically identifiable)
```

**Forbidden joins:** by timestamp proximity, row ordering, same model alone, reused request ID, disk filename, a latest-receipt singleton, or a bare assertion of same invocation.

Proposed nonpublishing sidecar evidence structure:

```rust
struct HeadwiseR3Cf1W8W9ALayerJoin {
    decode_session_id: String,
    decode_session_epoch: u64,
    decode_step: u64,
    layer_index: u32,
    w8_invocation_identity_digest: String,
    w8_comparator_receipt_digest: String,
    w9a_layer_receipt_digest: String,
    comparator_completed: bool,
    comparator_pass: bool,
    join_provenance: JoinProvenance,
}
```

`JoinProvenance` is a typed source of actual linkage, not a user-written string.

## 11. CF1-B2: Head-training checkpoint lineage decision

**Preferred Path A: digest preserved.** A true outer-scope / backend receipt observer can bind the natural W8 call to the exact W9A layer event without editing any of the existing 19 training-hashed files. Verify all 19 bytes are unchanged and revalidate the original checkpoints strictly.

**Conditional Path B: explicit lineage migration required.** If the only safe and exact seam requires changing `crates/model_core/src/native_wgpu.rs` or another of the 19 hashed source inputs, stop. Draft a separately authorized checkpoint lineage migration (new source digest, new manifest, newly qualified checkpoint) before using those changes in production. No manifest digest rewrite, legacy checkpoint validation relaxation, or shadow copy of the same invocation by assumption.

**Evidence limit:** the existing W8 `invocation_identity_digest` alone cannot determine the W9A `decode_step/layer_index` because the W9A receipt currently contains no such W8 ID. The join cannot be reconstructed from two unrelated sealed JSON receipts.

Explicit decision states:

```text
SAME_SOURCE_NATIVE_JOIN_PROVEN
NEEDS_EXPLICIT_CHECKPOINT_LINEAGE_MIGRATION
HOLD_NO_AUTHORITATIVE_JOIN_SEAM
```

## 12. CF1-B3: W9A measured classification

Retain the old routing/commit field `context_parity_pass` and existing W9A selection/canary probabilities unchanged.

New evidence-only outcome:

```rust
enum W9AContextParityEvidence {
    NotMeasured,
    MeasuredPass,
    MeasuredFail,
    MeasurementUnavailable,
}
```

| Selected route / observation | Valid CF1 evidence |
|---|---|
| HeadwiseDefault, no W8 invocation | `NotMeasured` |
| TensorCubeActualCanary, non-sampled | `NotMeasured` |
| TensorCubeSampledAudit, matching W8 completed PASS | `MeasuredPass` |
| TensorCubeSampledAudit, matching W8 completed FAIL | `MeasuredFail` |
| HeadwiseRollbackReplay with completed real W8 | Bind its actual PASS/FAIL independently of rollback routing status |
| Sampled/rollback with missing or wrong W8 receipt | `MeasurementUnavailable` or `FAIL` on identity corruption |

`MeasuredPass` requires all checked fields to match and an actual, completed W8 comparator. `context_parity_pass=true`, `candidate_error=None`, zero mismatch counters, or `sampled_audit=true` by themselves never create `MeasuredPass`.

`MeasuredFail` remains a measured negative observation, not a physically qualified *parity PASS*. The existing W9A rollback route must keep its semantics.

## 13. CF1-B4: No route-policy mutation

CF1-B is an observability and provenance patch:

- No change to `AttentionDecodeW9APreSamplerCommitInput::context_parity_pass` or its existing consumption.
- No automatic W9A selection, demotion, rollback or sampler-policy change.
- No reclassification of HeadwiseDefault as sampled TensorCube parity.
- No appended re-run of full model forward for W8 measurement.
- No full candidate/Headwise context host readback.
- No new W8 comparison in non-sampled token paths solely to fabricate coverage.
- A requested sampled audit with unjoinable W8 evidence remains explicit HOLD/FAIL in *measurement qualification*, even when legacy routing accepted the candidate.

## 14. Independent live identities / receipts

CF1-A and CF1-B shall create distinct receipts, bound to one source tree and runtime binary:

```text
headwise_r3_cf1_selected_production_output_receipt.json
headwise_r3_cf1_w8_w9a_invocation_binding_receipt.json
headwise_r3_cf1_qualification_aggregate.json
```

A/B receipts are independent. A PASS never implies B PASS. Aggregation may emit an overall PASS only when both applicable sides have true physical evidence. No unsupported family, layer, or route may be silently omitted.

Minimum A receipt:

```text
schema; source_digest; binary_sha256; GPU adapter/device/queue owner
selected pipeline family; exact shader digest; score policy; visibility policy
pipeline/generation; route; tested shape/ranges
proxy configured vs physically observed fields + callback type
qualification output sentinel / expected / visited / unwritten / finite counts
matched reference identifier / tolerances / compared_count / mismatch
submit / completion / staging retirement identity
selected_output_qualified; no_hot_path_extra_readback
status; first_failure_code; receipt_sha256
```

Minimum B receipt:

```text
schema; source_digest; binary_sha256; checkpoint training source digest
DecodeSessionID / epoch / step / layer; selected W9A route
actual W8 invocation digest + pipeline digest + comparator receipt digest
actual W8 completion + compare metrics + W9A layer receipt digest
join proof method + owner currentness
measured/not-measured/unavailable/fail counts
unmatched comparator count / cross-invocation mismatch count / duplicate count
status; first_failure_code; receipt_sha256
```

`None / UNKNOWN` is required for values that have not been observed. Do not substitute literal zero for unobserved counters.

## 15. Selected physical test matrix

### CF1-A / Short32

- Actual selected short shader in `CanonicalGqa` and original `LegacyTextDensityAdjusted` (each against semantically matched reference).
- `seq_q=1` first to isolate score and subgroup from chunked causal differences; later real multi-query cases where the short route is actually selected.
- Multiple finite Q/K/V inputs, identity currentness, low/medium allowed KV lengths, zero/nonzero score patterns and all expected output elements.
- Wrong subgroup width/lane/unwritten sentinel and wrong pipeline/shader/generation perturbations fail closed.

### CF1-A / Long64

- Actual selected long-v2 compiled shader under the runtime route selector.
- Exact GQA mapping and two 32-lane subgroups inside a 64-invocation workgroup.
- At least a boundary case that actually selects the long route, including route LUT and tile/tail domain.
- Finite output, no unwritten sentinel and matched reference parity, with no proxy-to-output inference.

### CF1-B / W8-W9A

- Real sampled TensorCube audit W8 comparator PASS and measured FAIL/rollback case.
- Same source, binary, model, native session, step, layer and attention-invocation identity.
- Non-sampled HeadwiseDefault and non-sampled TensorCube canary remain `NotMeasured`.
- W8 receipt missing, duplicate, stale or associated with different invocation is refused.
- Error paths (completion failure, device loss, cancellation, fallback) leave no false measured PASS.

### Cross-cut

- Fresh session, repeated session, stale source binary, GPU device/queue change and retirement reuse.
- If a route cannot be physically selected, mark `NOT_APPLICABLE` only from a hash-bound route manifest; otherwise `UNOBSERVED/HOLD`.
- Check token/text/KV/stop/emit parity for affected actual ordinary inference route; no CF5 ACTIVE.
- For D1/D2/D4 fixtures, record whether the selected runtime actually exercised the applicable Headwise/W9A route rather than treating configured depth as route coverage.

## 16. Negative / adversarial static and runtime checks

Required deterministic negatives include:

1. Probe configured workgroup size mislabeled as physically observed width.
2. `map_async` callback success mislabeled as registered Queue completion callback.
3. `selected_production_output_qualified=true` directly from proxy receipt.
4. Selected shader/pipeline digest or generation drift.
5. Short vs long family swapped by a cached proof.
6. Unwritten output left as sentinel or all-zero output falsely treated as written.
7. Output finite but numerical parity fails with correct reference.
8. Legacy TextDensity compared to canonical GQA without matching policy.
9. Chunked causal mask mismatch with R2 policy.
10. Normal dispatch uses in-flight qualification output before retirement.
11. W8 comparator receipt absent on sampled path.
12. W8 invocation belongs to another session/epoch/step/layer.
13. Duplicated W8 or W9A receipt consumed twice.
14. W8 `pass=true` with incomplete compare coverage or no completion.
15. W9A `context_parity_pass=true` without actual W8 mapped to `MeasuredPass`.
16. HeadwiseDefault non-sampled route falsely `MeasuredPass`.
17. Wrong checkpoint source digest accepted via modified validator.
18. A or B partial PASS incorrectly promoted to aggregate R3-CF1 PASS.
19. Newly inserted per-token `map_async`, full readback or extra exact-wait hidden as metrics.
20. Failed release build or physical failure represented as `PASS` in a receipt.

Static gates shall inspect actual source callsites and make counterfeiting difficult, but static tests are not proof of GPU output or W8 same-invocation execution.

## 17. Static acceptance

Add a narrow validator such as:

`tools/validate_ash_headwise_r3_cf1_selected_output_w8_w9a_static.py`

The validator shall check:

```text
R1/R2 defaults unchanged
R3 current family proxy and strict HOLD gate preserved until CF1 proof
actual selected production pipeline used in qualification
configured vs observed workgroup state separate
map callback vs Queue completion provenance separate
sentinel coverage and finite/mismatch readback represented
no global forced selected-output PASS
exact binding of W8 producer receipt and W9A layer identity
no passive NotMeasured → MeasuredPass promotion
same-source receipt lineage
training digest inputs byte-preserved OR explicit separate lineage HOLD
CF5-D ACTIVE disabled
no new per-token diagnostic data transfer/wait
```

Inherited static conflict remains explicit: HEADWISE-R2's optional causal policy contradicts two earlier CF5-C-R1 legacy-only assertions (`64/66`). CF4's older byte-preservation checker remains a separate historical conflict. Do not edit those old results to force all-green output.

## 18. Compile / Naga acceptance

Run the exact workspace on the user's Windows Rust/WGPU26 environment. The current archived workspace requires its exact external path dependency; no placeholder package or dependency-version swap is allowed.

```powershell
cargo metadata --format-version 1 --locked
cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo check -p model_core --lib --release --locked -j 1
cargo check -p orchestrator_local --lib --release --locked -j 1
cargo test -p burn_webgpu_backend --lib headwise_r3 --release --locked -j 1
cargo test -p model_core --lib headwise_r3 --release --locked -j 1
```

Register any new WGSL status/coverage shader in the existing Naga qualification graph. Actual Naga parser and validator PASS is required, not presence in a list.

Use existing exact native W9A physical-gate binary/CLI manifest and `--help` output to derive invocation arguments. Do not invent command-line flags or publish a fake physical receipt.

## 19. Runtime and PHYSICAL acceptance

**Physical CF1-A PASS** requires the actual selected Short/Long compiled production pipeline output to be written, finite, fully covered and numerically qualified with a matched reference; same owner/device/queue and resource completion/retirement; current selected pipeline proof not stale.

**Physical CF1-B PASS** requires at least one real completed W8 comparator joined by a proven same-invocation scope to the correct sealed W9A sampled layer, with correct measured positive/negative outcome; non-sampled routes remain unmeasured; no cross-session or duplicate matching.

A prior proxy receipt, a `context_parity_pass` bool, a zero mismatch count, or a static gate cannot satisfy either requirement.

If an exact native join cannot be implemented without changing `native_wgpu.rs`, the B arm shall return `NEEDS_EXPLICIT_CHECKPOINT_LINEAGE_MIGRATION` and the aggregate shall stay HOLD. Do not rewrite the original checkpoint manifest or pretend equivalent source bytes.

## 20. Performance attribution

CF1 is a correctness/evidence revision. Measure separately:

```text
first short-family qualifier wall time
first long-family qualifier wall time
qualification-only queue submits / map reads / exact waits
normal Headwise selected dispatch wall time
normal token latency and throughput
W8 sampled-only comparator wall and readback cost
peak GPU memory / host scratch when actually observable
```

No speedup, net overhead, or safe default-policy promotion is established by structural source inspection. Qualification-only costs must not contaminate normal decode throughput measures.

## 21. Failure classes

```text
HOLD_HEADWISE_R3_CF1_SELECTED_PIPELINE_UNQUALIFIED
FAIL_HEADWISE_R3_CF1_PROBE_FIELD_PROVENANCE_DRIFT
FAIL_HEADWISE_R3_CF1_MAP_CALLBACK_QUEUE_CALLBACK_CONFLATION
FAIL_HEADWISE_R3_CF1_SELECTED_SHADER_IDENTITY_DRIFT
FAIL_HEADWISE_R3_CF1_SELECTED_PIPELINE_GENERATION_DRIFT
FAIL_HEADWISE_R3_CF1_OUTPUT_SENTINEL_SURVIVED
FAIL_HEADWISE_R3_CF1_OUTPUT_COVERAGE_GAP
FAIL_HEADWISE_R3_CF1_OUTPUT_NONFINITE
FAIL_HEADWISE_R3_CF1_SELECTED_OUTPUT_PARITY
FAIL_HEADWISE_R3_CF1_WRONG_SCORE_OR_VISIBILITY_REFERENCE
FAIL_HEADWISE_R3_CF1_UNRETIRED_QUALIFICATION_OWNER
HOLD_HEADWISE_R3_CF1_W8_COMPARATOR_JOIN_UNAVAILABLE
FAIL_HEADWISE_R3_CF1_W8_RECEIPT_DIGEST
FAIL_HEADWISE_R3_CF1_W8_COMPARATOR_NOT_COMPLETED
FAIL_HEADWISE_R3_CF1_W8_W9A_INVOCATION_MISMATCH
FAIL_HEADWISE_R3_CF1_W8_W9A_DUPLICATE_BINDING
FAIL_HEADWISE_R3_CF1_NON_SAMPLED_MEASURED_FALSE_PASS
HOLD_HEADWISE_R3_CF1_CHECKPOINT_LINEAGE_MIGRATION_REQUIRED
FAIL_HEADWISE_R3_CF1_PARENT_SOURCE_OR_BINARY_DRIFT
FAIL_HEADWISE_R3_CF1_EARLY_ACTIVE_PROMOTION
```

Keep first failure stage, exact owner/currentness, and source identity. A missing observation is HOLD/UNKNOWN, not implicit success.

## 22. PASS tokens and partial closure

Per arm, **only after its actual physical requirements**:

```text
PASS_HEADWISE_R3_CF1_SELECTED_PRODUCTION_OUTPUT_PHYSICAL
PASS_HEADWISE_R3_CF1_W8_W9A_SAME_INVOCATION_EVIDENCE_PHYSICAL
```

Full CF1 may emit:

`PASS_HEADWISE_R3_CF1_SELECTED_OUTPUT_W8_W9A_CLOSURE`

only if:

```text
SOURCE/STATIC scope exact
+ actual Rust release COMPILE PASS
+ actual selected shader Naga PASS
+ CF1-A physical Short32 + Long64 output and parity PASS for applicable families
+ CF1-B same-native W8/W9A sampled/unsampled evidence truth PASS
+ matching source / binary / owner / queue / checkpoint lineage
+ no precompletion reuse, missing data, or duplicate receipt
+ no canonical token/KV/stop drift
+ no early CF5-D ACTIVE or Headwise/W9A policy promotion
```

A single family may have a narrower qualified result with exact applicability, but never a universal Headwise R3-CF1 PASS when another applicable family remains unobserved.

## 23. No automatic successor admission

CF1 only closes selected-output and W8/W9A evidence. It does **not** implement capacity-strided Headwise or TensorCube readers. Before `AOF-R1-CF5-C-R4` and ultimately `CF5-D ACTIVE`, separately establish actual selected-route stride-C vs visible-V attention parity, hidden-tail access rules, and canonical commit transaction invariants.

### Final law

```text
PROXY TOPOLOGY ≠ SELECTED OUTPUT
MAP CALLBACK ≠ OBSERVED QUEUE CALLBACK
CONFIGURED WORKGROUP SIZE ≠ GPU-OBSERVED SUBGROUP WIDTH
W9A ROUTING PASS ≠ MEASURED W8 CONTEXT PARITY

EXACT SELECTED PIPELINE + PHYSICAL OUTPUT COVERAGE + NUMERIC PARITY
+
EXACT W8 COMPARATOR + SAME W9A INVOCATION + COMPLETION
+
STRICT CHECKPOINT / OWNER / SOURCE LINEAGE
=
HEADWISE-R3-CF1 PHYSICAL EVIDENCE CLOSED

NOT YET = CAPACITY-STRIDED CANONICAL KV
NOT YET = CF5-D ACTIVE
NOT YET = PERFORMANCE PROMOTED
```

**Document state:** SOURCE-BAKED / STATIC-PASS only. Native Rust COMPILE, Naga, GPU PHYSICAL and full numerical admission remain NOT_RUN/HOLD. Refer to the attached exact bake report; a specification commit does not qualify the runtime.

---

## 24. Exact code-only SOURCE bake annex (2026-10-09)

The following records executed local source/ZIP checks and missing physical evidence. The complete target contract in sections 0–23 remains normative; **the physical PASS conditions have not been met**.

# HEADWISE-R3-CF1 | Selected Production Output + W8/W9A Invocation Closure

**Source-bake report, 2026-10-09 (Asia/Seoul).**

**Evidence level:** SOURCE and STATIC. **Not** a Rust compilation, native Naga, runtime or physical GPU PASS.

## 1. Exact parent and output

| Artifact | SHA-256 / contents |
|---|---|
| Parent `ASH_PASS3_HEADWISE_R3_SUBGROUP32_ADMISSION_W9A_PARITY_EVIDENCE_TRUTH_CODE_ONLY.zip` | `752184f8e7ea4d25e647c3c5e8f2ea0e8863a6dfd2478a2cb5490b01037e7c9b` (8,743 entries) |
| Baked full `ASH_PASS3_HEADWISE_R3_CF1_SELECTED_PRODUCTION_OUTPUT_W8_W9A_INVOCATION_CLOSURE_CODE_ONLY.zip` | `f335e0f9a6b7df4d16cc8ce66c8f6b3098172095203fbc7ba4ecf4cd75c0cb5b` (8,747 entries) |
| Overlay `ASH_HEADWISE_R3_CF1_SELECTED_PRODUCTION_OUTPUT_W8_W9A_INVOCATION_CLOSURE_OVERLAY_CODE_ONLY.zip` | `561f2adb9fd0cd2d6b4227228c8c59b8ccd49b86176f0796fe6a9ea039c71484` (10 entries) |
| Changes | **ADD 4 / MOD 6 / DEL 0** |
| ZIP CRC and stored-byte verification | **PASS**, full parent equivalence for all unchanged entries |

Per-file SHA-256: `HEADWISE_R3_CF1_BAKE_MANIFEST.json`.

## 2. Source implementation scope

### CF1-A0: Correct proxy provenance

- `crates/burn_webgpu_backend/src/headwise_r3_subgroup_admission.rs`: original misleading `actual_workgroup_size` replaced with actual **configured** workgroup size and explicitly **unobserved** GPU workgroup size (`None`). Actual subgroup widths are decoded from mapped GPU status and deduplicated. Source records *independent* Queue `on_submitted_work_done` callback and `map_async` callback, rather than calling map completion a queue completion. Entry is still a **proxy**, not selected production output proof.
- Existing admission mode `RequireFamilyTopologyProbe` remains default; `LegacyUnchanged` remains compatibility mode; `RequireSelectedProductionOutput` stays **HOLD**, with no fabricated success cache.
- `completion_callback_observed` now refers to a registered Queue completion callback (intentional receipt meaning correction); new schema `ash.headwise.r3.cf1.subgroup.proxy_provenance.v2`.

### CF1-A1/A2: Selected shader and finite-output fixture, SOURCE candidate

- `crates/burn_webgpu_backend/src/headwise_atlas.rs`: `qualify_r3_cf1_selected_output()` uses the **same** prepared Q/K/V, original route selection and selected production pipeline. It encodes into an explicitly *qualifier-owned* sentinel-initialized output, not canonical output. `qualification_only` permits the fixture through the strict-admission boundary **without** promoting production. It still requires a real Short32/Long64 family proxy first.
- Added `crates/burn_webgpu_backend/src/headwise_r3_cf1_selected_output.rs` and `crates/burn_webgpu_backend/src/shaders/headwise_r3_cf1_selected_output_status.wgsl`: bounded `16,384` element fixture, per-element write sentinel, finite and arithmetic-overflow checks, numerical mismatch and first mismatch, max absolute/relative error, 9-u32 status readback. Explicit qualifier Queue completion callback and map callback; no full context readback. Caller-supplied reference contract hash **is not validated as a canonical/native reference authority**; receipt includes `reference_provenance=CALLER_SUPPLIED_DIGEST_NOT_NATIVE_REFERENCE_PROOF`, `selected_output_qualified=false`, `production_promoted=false`.
- **Not closed:** real reference producer identity binding, identical score/visibility source comparison, selected kernel real output physical proof, status callback physical execution, strict live proof cache. Numerical threshold is caller supplied rather than promoted as authoritative; no pass token emitted.

### CF1-B: Original W8 receipt validation but no W9A same-call join

- Added `crates/model_core/src/headwise_r3_cf1_w8_join_evidence.rs`: verifies an original W8 receipt SHA, pipeline identity SHA, coverage and completion fields. A W8 receipt can remain a valid standalone W8 observation, but the helper explicitly reports `MeasurementUnavailable`, `w9a_same_invocation_proven=false`, and `full_cf1_pass_token=null` for W9A.
- **No modification to `crates/model_core/src/native_wgpu.rs`**: both comparator and layer receipt are local to this checkpoint-hashed file. A native same-call join without a validated new checkpoint lineage is **not implemented**. Mere text/session/step identity is not treated as a join.
- Checkpoint training source digest across the same 19 inputs stays byte-equivalent: `e20f93b19bcb8a93a96809a28d2faf5c72c68896da060002d36a43e2286b8283`.

### Registry/lineage/validation

- Backend crate exports the selected-output qualifier; model-core W9A registry exposes the W8 provenance helper.
- `aof_r1_admission.rs` includes new Rust/WGSL source bytes in the **runtime** digest without changing head training digest.
- `ash_aof_r1_cf7_cf8_cf9_gate.rs` Naga shader-list now includes the selected-output WGSL source; **Naga is not executed**.
- Added `tools/validate_ash_headwise_r3_cf1_selected_output_w8_w9a_static.py`: 42 statics and 21 negative-source mutations.

## 3. Verification matrix (actually executed)

| Evidence | Result |
|---|---|
| CF1 SOURCE / STATIC | **42/42 PASS** |
| CF1 negative source mutations | **21/21 rejected** |
| HEADWISE-R1 parent | **38/38 PASS** |
| HEADWISE-R2 parent | **22/22 PASS** |
| CF5-C-R3 parent | **60/60 PASS** |
| HEADWISE-R3 old static | **34/37 FAIL**: `pre_dispatch_gate`, `strict_rejects_proxy_only`, `proxy_mismatch_fails_closed`. R3's exact source patterns are superseded by the CF1 proxy/strict signature changes. This is **not** called a 37/37 PASS. |
| CF5-C-R1 historic parent | **64/66 FAIL**, carried HEADWISE-R2 causal/full-stage supersession. |
| Old CF1/CF2/VH6 static | historical **51/52 FAIL**, carried CF4 `aof_r1_prefix_commit.rs` byte-identity supersession. |
| Training source digest | **19 inputs unchanged** |
| Complete ZIP CRC / file-byte identity | **PASS** |
| Rust COMPILE | **NOT_RUN** (`cargo`/`rustc` unavailable) |
| WGSL Naga | **NOT_RUN** |
| Native WGPU / physical output | **NOT_RUN** |
| Actual W8/W9A same-invocation measurement | **NOT_BOUND / NOT_RUN** |
| Performance | **NOT_MEASURED** |

Static gate proves source patterns only. The new status shader's actual Naga validity and Rust buildability are **UNKNOWN** without running those tools.

## 4. Explicit semantic changes and holds

- **Changed:** R3 proxy receipt schema/meaning; `completion_callback_observed` now has a real Queue callback source. Existing default probe still costs an up-front one-time GPU submission/readback and exact wait. The qualification-only selected-output API optionally submits an additional GPU command buffer/readback only when invoked.
- **Preserved:** HEADWISE-R1 LegacyTextDensityAdjusted default; HEADWISE-R2 LegacyFullStaged default; W9A pre-sampler route policy; canonical KV, token, stop, emit and training checkpoint admission; no new default per-token comparator or promotion.
- **HOLD:** `PASS_HEADWISE_R3_CF1_SELECTED_OUTPUT_W8_W9A_CLOSURE` and `RequireSelectedProductionOutput` live admission. Proof of actual canonical reference producer, selected Short32/Long64 fixture success, W8↔W9A matching native invocation, and full GPU/retirement campaign is absent.
- **CF5-D ACTIVE:** forbidden. Do not infer speedup or numerical exactness from this ZIP.

## 5. Native validation commands (NOT_EXECUTED)

```powershell
python .\tools\validate_ash_headwise_r3_cf1_selected_output_w8_w9a_static.py --negative-tests
cargo metadata --format-version 1 --locked
cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo check -p model_core --lib --release --locked -j 1
cargo check -p orchestrator_local --lib --release --locked -j 1
cargo test -p burn_webgpu_backend --lib headwise_r3_cf1 --release --locked -j 1
cargo test -p model_core --lib headwise_r3_cf1 --release --locked -j 1
```

Then validate updated WGSL with native Naga and perform same-source real selected-production short/long GPU output parity with a canonical matched-math reference and completion, plus W8→W9A same-invocation binding under explicit checkpoint lineage. Exact path-based external `sherpa-rs` workspace input is absent from the code-only package; do not stub or silently replace it.

## Final status

`SOURCE APPLIED / STATIC PASS / ZIP PASS / COMPILE NOT_RUN / NAGA NOT_RUN / PHYSICAL NOT_RUN / W8_W9A_JOIN HOLD / FULL CF1 HOLD / PRODUCTION NOT_PROMOTED`.
