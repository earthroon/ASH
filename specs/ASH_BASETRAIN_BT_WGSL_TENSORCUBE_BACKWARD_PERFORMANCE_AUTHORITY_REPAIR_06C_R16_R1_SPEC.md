# ASH-BASETRAIN-BT-WGSL-TENSORCUBE-BACKWARD-PERFORMANCE-AUTHORITY-REPAIR-06C-R16-R1

## Revision

- Patch ID: `ASH-BASETRAIN-BT-WGSL-TENSORCUBE-BACKWARD-PERFORMANCE-AUTHORITY-REPAIR-06C-R16-R1`
- Build revision: `bt-wgsl-tensorcube-backward-performance-authority-repair-06c-r16-r1`
- Physical correctness parent: `ASH-BASETRAIN-BT-WGSL-TENSORCUBE-BACKWARD-MATMUL-ACCELERATION-06C-R16`
- Downstream consumer: `ASH-BASETRAIN-BT-WGSL-STRUCTURAL-DELTAQ-GATE-PROJECTOR-BACKWARD-06C-R17`
- Proof ledger: `HOLD`

## SSOT

R16-R1 does not change R16 backward mathematics, F32 arithmetic, 16x16x16 TensorCube tile semantics, seven-role scope, exact parity rules, or canonical gradient outputs. It replaces only the performance qualification authority. Semantic and TensorCube benchmark dispatches are fully prepared before timing. Performance samples use GPU timestamps written at compute-pass begin/end, sum only compute-pass durations, and compare complete seven-role suites using paired `oracle_total - candidate_total` samples. TensorCube correctness authority is independent from performance qualification. R17 depends only on correctness authority and cannot be blocked by a noisy or slower performance result.

## Frozen correctness parent

Required R16 evidence:

- seven-role `dX` bit-exact parity
- seven-role `dW` bit-exact parity
- E2E `dInputHiddenTotal` bit-exact parity
- zero nonfinite publication
- double-run reproducibility
- zero production gradient/weight payload readback
- existing R16 F32 16x16x16 TensorCube equations and reduction order unchanged

R16-R1 publishes:

`tensorCubeBackwardCorrectnessAuthority = true`

Performance is not a prerequisite for that authority.

## Authority split

Three independent states are defined:

1. `TensorCubeBackwardCorrectnessAuthority`
   - exact parity, finite status, completion, reproducibility
2. `TensorCubeBackwardPerformanceQualification`
   - hardware/software/geometry-specific timing classification
3. `TensorCubeBackwardPreferredBackend`
   - `TENSORCUBE` only when qualification is `FASTER_PROMOTABLE`; otherwise `SEMANTIC`

The legacy mixed `tensorCubeBackwardComputeAuthority` is compatibility/audit state only and is no longer an R17 dependency.

## Legacy timer retirement

R16 promotion must not use `HeadwiseTexture05ExecutorTimer` executor-envelope timing.

Retired promotion topology:

`timestamp submit -> host operation/pipeline creation/submissions/poll -> timestamp submit`

R16-R1 requires:

- pipeline creation outside timed region
- bind-group creation outside timed region
- scratch allocation outside timed region
- status polling outside timed region
- no cross-submission begin/end interval as performance authority

## Prepared performance objects

The implementation provides prepared semantic and TensorCube role profiles for exactly:

1. DOWN
2. GATE
3. UP
4. OPROJ
5. Q
6. K
7. V

Preparation owns/reuses:

- shader module/pipelines
- bind group layout and bind groups
- uniform parameter buffers
- benchmark-only output scratch
- compact status storage
- per-role timestamp query set, resolve buffer and staging buffer
- exact role geometry and pipeline identity digests

Prepared scratch is non-publishing and cannot replace canonical R16 gradient outputs.

## Timing authority

Each actual compute pass uses `wgpu26::ComputePassTimestampWrites` with beginning and end query indices.

One role timing is:

`role_compute_ns = sum(each actual compute-pass duration)`

Timestamp resolve, staging copy, map, and `device.poll()` occur outside timed compute passes.

Promotion timing scope is exactly:

`compute_pass_internal_timestamp_sum`

Aggregate mode is exactly:

`paired_seven_role_compute_pass_delta`

## Warmup and paired sampling

- prepared warmup pairs: 2
- timed paired samples: 9
- minimum admitted paired sample count: 7

Order alternates:

- sample 0: ORACLE -> CANDIDATE
- sample 1: CANDIDATE -> ORACLE
- repeat

Per-role timings are diagnostics only.

For each sample `s`:

`OracleTotal_s = sum(7 semantic role compute durations)`

`CandidateTotal_s = sum(7 TensorCube role compute durations)`

`Delta_s = OracleTotal_s - CandidateTotal_s`

Positive delta means TensorCube is faster.

## Paired statistics

Canonical statistics:

`DeltaMedian = median(Delta_s)`

`DeltaMAD = median(abs(Delta_s - DeltaMedian))`

Timestamp quantization bound:

`TimestampQuantizationMargin = ceil(2 * timestampPeriodNs * (oraclePassCount + candidatePassCount))`

Final uncertainty:

`PairedMargin = max(DeltaMAD, TimestampQuantizationMargin)`

The old sum of seven role-local worst-case MADs is retired.

## Performance classifications

### FASTER_PROMOTABLE

`DeltaMedian > PairedMargin`

- preferred backend: `TENSORCUBE`
- correctness authority remains true

### FASTER_BUT_INCONCLUSIVE

`0 < DeltaMedian <= PairedMargin`

- preferred backend: `SEMANTIC`
- correctness authority remains true
- R17 proceeds

### EQUIVALENT_INCONCLUSIVE

`abs(DeltaMedian) <= PairedMargin` with no decisive positive result

- preferred backend: `SEMANTIC`
- correctness authority remains true
- R17 proceeds

### MEASURABLY_SLOWER

`DeltaMedian < -PairedMargin`

- preferred backend: `SEMANTIC`
- correctness authority remains true
- R17 proceeds

### UNAVAILABLE

Used when valid in-pass timing cannot be established, including absent timestamp-query support or invalid timing identity.

- preferred backend: `SEMANTIC`
- correctness authority remains true
- R17 proceeds

## Non-promotion policy

`BTR16PerformanceNotPromotable` is retired as a production correctness failure.

There is no replacement hard failure for a valid non-promotion classification.

Performance non-promotion must never revoke bit-exact R16 correctness authority.

Malformed correctness evidence still fails closed.

## Legacy R16 receipt supersession

The historical R16 receipt keeps its original measured-acceleration meaning instead of being silently redefined. R16-R1 records `correctnessPass=true` separately from `performancePromotionSatisfied`. The legacy R16 `pass` and legacy measured-faster PASS token are present only when the repaired performance qualification is `FASTER_PROMOTABLE`. `supersededByR16R1PerformanceAuthority=true` identifies R16-R1 as the downstream authority for performance classification and continuation.

## R17 dependency rebind

R17 must require:

- R16-R1 final receipt pass
- `tensorCubeBackwardCorrectnessAuthority == true`
- `r17PerformanceDependency == false`
- preserved R16 base-path `dInputHiddenTotal`

R17 must not require:

- `FASTER_PROMOTABLE`
- TensorCube preferred-backend selection
- legacy mixed compute-authority promotion

The R17 CLI gate is renamed to:

`--require-bt-wgsl-r17-r16-tensorcube-correctness-authority-preserved`

## Qualification identity

Performance qualification is sealed to:

- adapter backend/name/vendor/device/device-type
- driver and driver-info
- timestamp period
- seven role M/N/K/tile-row geometry
- semantic shader/pipeline identity
- TensorCube shader/pipeline identity
- F32 16x16x16 TensorCube policy

A qualification result cannot silently authorize an unrelated adapter/driver/geometry identity.

## Same-operation fallback

Preferred backend policy is selected before a future operation is admitted.

If a TensorCube operation is admitted and then faults, semantic execution must not be silently substituted inside the same operation.

A pre-operation policy choice of `SEMANTIC` after non-promotion is not a fallback.

## Readback boundary

Allowed:

- timestamp query results
- compact status metadata outside timing

Forbidden:

- gradient payload readback
- weight payload readback
- activation payload readback

Required:

- `production_gradient_payload_readback = 0`
- `production_weight_payload_readback = 0`

## Required receipts

- `r16r1_correctness_authority_receipt.json`
- `r16r1_prepared_suite_receipt.json`
- `r16r1_timestamp_query_atlas_receipt.json`
- `r16r1_paired_samples_receipt.json`
- `r16r1_per_role_diagnostics_receipt.json`
- `r16r1_performance_qualification_receipt.json`
- `r16r1_legacy_timer_retirement_receipt.json`
- `r16r1_preferred_backend_receipt.json`
- `r16r1_r17_dependency_rebind_receipt.json`
- `bt_wgsl_tensorcube_backward_performance_authority_repair_06c_r16_r1_final.json`

The final receipt uses seven deterministic parallel/streaming atlas waves. No monolithic final `json!` authority is admitted.

## CLI gates

Exactly 48 R16-R1 gates are required once in the source validator, short args, full args, and resolved-args repair path:

```text
--require-bt-wgsl-r16r1-r16-physical-correctness-parent
--require-bt-wgsl-r16r1-seven-role-exact-parity-parent
--require-bt-wgsl-r16r1-e2e-dinput-exact-parity-parent
--require-bt-wgsl-r16r1-correctness-performance-authority-separation
--require-bt-wgsl-r16r1-tensorcube-correctness-authority
--require-bt-wgsl-r16r1-prepared-semantic-suite
--require-bt-wgsl-r16r1-prepared-tensorcube-suite
--require-bt-wgsl-r16r1-prepared-seven-role-suite
--require-bt-wgsl-r16r1-pipeline-creation-outside-timed-region
--require-bt-wgsl-r16r1-bindgroup-creation-outside-timed-region
--require-bt-wgsl-r16r1-scratch-allocation-outside-timed-region
--require-bt-wgsl-r16r1-status-poll-outside-timed-region
--require-bt-wgsl-r16r1-compute-pass-internal-timestamps
--require-bt-wgsl-r16r1-per-pass-timestamp-query-atlas
--require-bt-wgsl-r16r1-zero-cross-submission-envelope-authority
--require-bt-wgsl-r16r1-seven-role-whole-suite-paired-sampling
--require-bt-wgsl-r16r1-alternating-pair-order
--require-bt-wgsl-r16r1-per-role-diagnostic-timing
--require-bt-wgsl-r16r1-signed-paired-delta
--require-bt-wgsl-r16r1-paired-delta-median
--require-bt-wgsl-r16r1-paired-delta-mad
--require-bt-wgsl-r16r1-timestamp-quantization-margin
--require-bt-wgsl-r16r1-zero-summed-role-worst-case-mad
--require-bt-wgsl-r16r1-faster-promotable-verdict
--require-bt-wgsl-r16r1-faster-but-inconclusive-verdict
--require-bt-wgsl-r16r1-equivalent-inconclusive-verdict
--require-bt-wgsl-r16r1-measurably-slower-verdict
--require-bt-wgsl-r16r1-performance-unavailable-verdict
--require-bt-wgsl-r16r1-performance-nonpromotion-not-correctness-failure
--require-bt-wgsl-r16r1-preferred-backend-policy
--require-bt-wgsl-r16r1-zero-same-operation-fallback
--require-bt-wgsl-r16r1-adapter-qualification-identity
--require-bt-wgsl-r16r1-driver-qualification-identity
--require-bt-wgsl-r16r1-geometry-qualification-identity
--require-bt-wgsl-r16r1-pipeline-qualification-identity
--require-bt-wgsl-r16r1-timestamp-period-binding
--require-bt-wgsl-r16r1-performance-scratch-nonpublishing
--require-bt-wgsl-r16r1-production-payload-readback-zero
--require-bt-wgsl-r16r1-r16-mathematics-frozen
--require-bt-wgsl-r16r1-r16-seven-role-scope-frozen
--require-bt-wgsl-r16r1-r16-f32-16x16x16-policy-frozen
--require-bt-wgsl-r16r1-r17-correctness-dependency-rebind
--require-bt-wgsl-r16r1-r17-zero-performance-dependency
--require-bt-wgsl-r16r1-zero-optimizer
--require-bt-wgsl-r16r1-zero-weight-mutation
--require-bt-wgsl-r16r1-final-loss-authority-deferred
--require-bt-wgsl-r16r1-atlas-wave-streaming-receipt
--require-bt-wgsl-r16r1-zero-monolithic-final-json
```

## Expected physical summary

```text
r16_correctness_parent=1
seven_role_dx_exact_parent=1
seven_role_dw_exact_parent=1
e2e_dinput_exact_parent=1
tensorcube_backward_correctness_authority=1
correctness_performance_authority_separated=1
prepared_semantic_roles=7
prepared_tensorcube_roles=7
pipeline_creation_inside_timed_region=0
bind_group_creation_inside_timed_region=0
scratch_allocation_inside_timed_region=0
status_poll_inside_timed_region=0
compute_pass_internal_timestamp=1
cross_submission_envelope_timer=0
paired_warmup_runs=2
paired_timed_runs=9
paired_order_alternation=1
whole_suite_paired_delta_authority=1
legacy_summed_role_margin=0
delta_median_ns=<runtime>
delta_mad_ns=<runtime>
timestamp_quantization_margin_ns=<runtime>
paired_margin_ns=<runtime>
performance_qualification=<runtime>
tensorcube_preferred_backend=TENSORCUBE|SEMANTIC
performance_nonpromotion_correctness_failure=0
r17_correctness_dependency=1
r17_performance_dependency=0
same_operation_fallback=0
production_gradient_payload_readback=0
production_weight_payload_readback=0
optimizer=0
weight_mutation=0
final_loss_authority=0
receipt_atlas_waves=7
monolithic_final_json=0
proof_ledger=HOLD
```

## PASS seal

`PASS_ASH_BASETRAIN_BT_WGSL_TENSORCUBE_BACKWARD_PERFORMANCE_AUTHORITY_REPAIR_06C_R16_R1`

The full runtime token additionally seals prepared suites, compute-pass timestamps, paired statistics, correctness/performance separation, R17 dependency rebinding, zero payload readback, and proof-ledger HOLD boundaries.
