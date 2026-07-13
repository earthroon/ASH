# ASH-TCU-K7N-D1R6-R3 SPEC

## Paired Batch Common-Mode Drift and Sync Cadence Repair

## 1. Identity

- Patch: `ASH-TCU-K7N-D1R6-R3_PAIRED_BATCH_COMMON_MODE_DRIFT_AND_SYNC_CADENCE_REPAIR`
- PASS: `PASS_ASH_TCU_K7N_D1R6_R3_PAIRED_BATCH_COMMON_MODE_DRIFT_AND_SYNC_CADENCE_REPAIR_EQUAL_SYNC_CADENCE_PAIRED_LOG_RATIO_VALID_NO_OUTPUT_COMMIT_NO_ROUTE_PROMOTION`
- Next: `ASH-TCU-K7N-D1R7_MULTI_SHAPE_PERFORMANCE_MATRIX`

## 2. Parent SSOT

```text
D1R5 execution=d1r5-5d4e541766f315af0896
numerical_parity_passed=true
exact_bit_match_count=16
failing_element_count=0
output_authority=burn
runtime_output_changed=false

D1R6-R2 execution=d1r6r2-fail-9f8bf037a0ec12d4e841
measurement_valid=false
evidence_written_before_return=true
failed_gates=[burn_batch_median_nmad,tensorcube_batch_median_nmad,burn_batch_median_drift,tensorcube_batch_median_drift]
```

R2 remains failed. Its post-hoc paired ratios are design evidence only and cannot be reused as R3 PASS evidence.

## 3. Repaired Measurement Authority

One adjacent pair is the R3 measurement unit.

```text
even pair: Burn -> TensorCube
odd pair: TensorCube -> Burn

Burn operations per sync interval=1
TensorCube operations per sync interval=1
Burn completion observations per operation=1
TensorCube completion observations per operation=1
Burn in-flight depth=1
TensorCube in-flight depth=1
sync_cadence_equivalent=true
```

Burn authority:

```text
burn_baseline_authority=burn_cubecl_matmul_fixture_path
burn_timing_authority=cubecl_compute_client_device_profile_scope
profile_span_count_per_logical_operation=1
attribution_scope=complete_logical_operation_device_profile
external_burn_marker_timing_used=false
```

TensorCube authority:

```text
tensorcube_timing_authority=canonical_compute_pass_timestamp_scope
dispatches per operation=1
timestamp pairs per operation=1
workgroup=16x16x1
dispatch=1x1x1
```

The TensorCube eight-dispatch cohort path is not used by R3. Each TensorCube operation resolves and maps its own two timestamps before scratch reuse.

## 4. Runtime and Fixture

```text
runtime=one authoritative Burn WGPU Device and Queue
wgpu authority=ash.runtime_wgpu_type_authority.burn_runtime.wgpu26.v1
features=TIMESTAMP_QUERY,TIMESTAMP_QUERY_INSIDE_ENCODERS,TIMESTAMP_QUERY_INSIDE_PASSES,SHADER_INT64
fixture=ash_tcu_k7n_d1r3_fixture_m1_n16_k4_v1
shape=M1/N16/K4
reference_digest=a4916905d1827029e2e74aeb8d156698b1e1ea0d27134492fb382e76489ed200
handle-map hits=2
handle-map misses=0
host uploads=0
```

Projection output is never copied or mapped.

## 5. Cardinality

```text
warmup pairs=128
measured batches=32
pairs per batch=64
measured pairs=2048
Burn operations=2048
TensorCube operations=2048
Burn-first pairs per batch=32
TensorCube-first pairs per batch=32
invalid pairs=0
invalid batches=0
```

No trimming, winsorization, spike replacement, batch deletion or retry-until-PASS is allowed.

## 6. Paired Comparative SSOT

For pair `j`:

```text
B_j=Burn device-profile duration
T_j=TensorCube compute-pass duration
R_j=B_j/T_j
D_j=ln(B_j)-ln(T_j)
```

`D_j` is the paired comparative authority. Pair-member CPU gap is recorded separately and excluded from GPU duration.

For each batch:

```text
batch median log ratio=median(D_j for 64 pairs)
batch paired ratio=exp(batch median log ratio)
```

Overall:

```text
overall median log ratio=median(32 batch median log ratios)
overall paired ratio=exp(overall median log ratio)
```

## 7. Paired Stability

```text
paired scaled log MAD=1.4826*median(abs(batch_log_ratio-overall_median_log_ratio))
paired scaled log MAD<=ln(1.15)=0.13976194237515863

paired drift ratio=exp(abs(first_8_log_ratio_median-last_8_log_ratio_median))
paired drift ratio<=1.20

paired order bias ratio=exp(abs(burn_first_log_ratio_median-tensorcube_first_log_ratio_median))
paired order bias ratio<=1.15
```

## 8. Absolute/Common-Mode Separation

Burn and TensorCube absolute raw statistics, batch-median NMAD and first/last drift remain diagnostics.

Valid path A:

```text
Burn absolute stability passed
TensorCube absolute stability passed
paired stability passed
paired_comparative_validity=valid_absolute_environment_stable
```

Valid path B:

```text
Burn absolute stability failed
TensorCube absolute stability failed
Pearson correlation of log batch medians>=0.90
drift directions agree
paired stability passed
paired_comparative_validity=valid_common_mode_environment_drift
```

Absolute instability without proven common-mode coupling is `invalid_common_mode_unproven`.

## 9. Performance Classification

```text
paired_ratio_p05=nearest-rank 5th percentile of 2048 pair ratios

non-regression:
overall_paired_ratio>=0.6666666666666666
AND paired_ratio_p05>=0.5

catastrophic regression:
overall_paired_ratio<0.5
OR paired_ratio_p05<0.3333333333333333

resolution floor=max(1000,timestamp_period_ns*32)
```

Classification order:

```text
timestamp/cadence validity
-> paired comparative validity
-> catastrophic regression
-> resolution limited
-> paired non-regression
-> bounded regression
```

Eligible classifications:

```text
non_regression_absolute_stable
non_regression_common_mode_drift
resolution_limited
```

## 10. Failure Evidence and Isolation

After benchmark start, raw pairs, paired batches, dispersion, drift, order bias, absolute statistics, common-mode correlation, failed gates and final seal are written before error return.

```text
projection_output_readback_count=0
numerical_parity_rerun_count=0
shadow_output_commit_authorized=false
shadow_output_committed=false
production_promotion_authorized=false
production_route_enabled=false
route_mutation_count=0
registry_write_count=0
output_authority=burn
runtime_output_changed=false
```

## 11. Audit Command

```powershell
cargo run --manifest-path .\crates\orchestrator_local\Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k7n_d1r6r3_paired_batch_common_mode_drift_and_sync_cadence_repair -- `
  --repo-root "D:\1111113232\DUST\1\ash_pass3" `
  --require-d1r5-pass `
  --require-d1r5-execution d1r5-5d4e541766f315af0896 `
  --require-d1r6r2-invalid-measurement `
  --require-d1r6r2-execution d1r6r2-fail-9f8bf037a0ec12d4e841 `
  --require-d1r6r2-evidence-written-before-return `
  --require-d1r6r3-performance-eligibility `
  --require-parent-numerical-parity-passed `
  --require-parent-exact-bit-match-count 16 `
  --require-parent-failing-element-count 0 `
  --require-parent-output-authority burn `
  --require-fixture-id ash_tcu_k7n_d1r3_fixture_m1_n16_k4_v1 `
  --require-fixture-m 1 `
  --require-fixture-n 16 `
  --require-fixture-k 4 `
  --require-reference-digest a4916905d1827029e2e74aeb8d156698b1e1ea0d27134492fb382e76489ed200 `
  --execution-mode paired_common_mode_sync_cadence_repair_audit `
  --require-runtime-device-authority burn_wgpu_runtime `
  --require-runtime-queue-authority burn_wgpu_runtime `
  --require-wgpu-authority ash.runtime_wgpu_type_authority.burn_runtime.wgpu26.v1 `
  --require-timestamp-query-supported `
  --require-timestamp-query-inside-encoders `
  --require-timestamp-query-inside-passes `
  --require-shader-int64-enabled `
  --reject-wall-clock-only-performance-pass `
  --create-one-authoritative-burn-runtime-context `
  --reject-extra-tensorcube-device `
  --reject-extra-tensorcube-queue `
  --register-two-fixture-primitives `
  --require-primitive-handle-map-hits 2 `
  --require-primitive-handle-map-misses 0 `
  --require-host-upload-count 0 `
  --bind-actual-burn-cubecl-matmul `
  --require-burn-baseline-authority burn_cubecl_matmul_fixture_path `
  --instrument-burn-cubecl-device-profile-per-operation `
  --require-burn-profile-span-count-per-operation 1 `
  --require-complete-burn-operation-attribution `
  --reject-external-burn-marker-timing `
  --bind-canonical-tensorcube-kernel `
  --require-tensorcube-route ash_tcu_vocab_atlas_tile_projection_f32_rhs_strided_view_v1 `
  --require-workgroup-geometry 16x16x1 `
  --require-dispatch-geometry 1x1x1 `
  --require-tensorcube-dispatch-count-per-operation 1 `
  --require-tensorcube-timestamp-pair-count-per-operation 1 `
  --require-burn-operations-per-sync-interval 1 `
  --require-tensorcube-operations-per-sync-interval 1 `
  --require-burn-completion-per-operation `
  --require-tensorcube-completion-per-operation `
  --require-burn-in-flight-depth 1 `
  --require-tensorcube-in-flight-depth 1 `
  --require-sync-cadence-equivalent `
  --release-burn-output-after-each-profile `
  --require-sequential-tensorcube-scratch-reuse-after-completion `
  --warmup-pair-count 128 `
  --require-measured-batch-count 32 `
  --require-pairs-per-batch 64 `
  --require-measured-pair-count 2048 `
  --alternate-pair-member-order `
  --require-pair-adjacency `
  --reject-unrelated-work-between-pair-members `
  --reject-artificial-pair-delay `
  --record-pair-member-gap-cpu-time `
  --require-device-profile-scoped-gpu-time `
  --require-timestamp-readback-only `
  --require-no-projection-output-readback `
  --retain-all-valid-pairs `
  --reject-outlier-deletion `
  --write-failure-evidence-before-return `
  --compute-pair-burn-over-tensorcube-ratio `
  --compute-pair-log-ratio `
  --require-positive-finite-pair-durations `
  --compute-32-paired-batches `
  --require-valid-pairs-per-batch 64 `
  --require-burn-first-pairs-per-batch 32 `
  --require-tensorcube-first-pairs-per-batch 32 `
  --compute-overall-median-log-ratio `
  --compute-overall-paired-ratio `
  --compute-paired-log-mad `
  --require-mad-scale-factor 1.4826 `
  --require-paired-scaled-log-mad-at-most 0.13976194237515863 `
  --compute-paired-first-last-drift `
  --require-paired-drift-ratio-at-most 1.20 `
  --compute-pair-order-bias `
  --require-paired-order-bias-ratio-at-most 1.15 `
  --compute-absolute-latency-diagnostics `
  --compute-absolute-batch-median-nmad `
  --compute-absolute-first-last-drift `
  --compute-log-latency-correlation `
  --require-common-mode-correlation-at-least 0.90 `
  --require-common-mode-drift-direction-agreement `
  --classify-absolute-environment-stability `
  --classify-paired-comparative-validity `
  --compute-paired-log-ratio-p05 `
  --require-paired-median-ratio-at-least 0.6666666666666666 `
  --require-paired-p05-ratio-at-least 0.5 `
  --require-catastrophic-paired-median-ratio-below 0.5 `
  --require-catastrophic-paired-p05-ratio-below 0.3333333333333333 `
  --require-resolution-floor-min-ns 1000 `
  --require-resolution-floor-timestamp-multiplier 32 `
  --classify-performance-result `
  --allow-common-mode-drift-comparative-pass `
  --allow-resolution-limited-next-stage `
  --reject-common-mode-unproven `
  --reject-bounded-regression-next-stage `
  --reject-catastrophic-regression `
  --require-no-numerical-parity-rerun `
  --require-no-shadow-output-commit `
  --require-no-downstream-output-commit `
  --require-no-route-promotion `
  --require-no-registry-write `
  --verify-burn-output-authority `
  --verify-registry-unchanged `
  --verify-route-bindings-unchanged `
  --verify-route-epoch-unchanged `
  --verify-d1r5-parity-contract-unchanged `
  --verify-d1r4-readback-contract-unchanged `
  --verify-d1r3-dispatch-contract-unchanged `
  --verify-d1r2-preparation-contract-unchanged `
  --verify-d1r1-admission-contract-unchanged `
  --verify-d0r3-candidate-contract-unchanged `
  --verify-k6p-canonical-source-unchanged `
  --verify-vocab-atlas-burn-computation-preserved `
  --verify-model-weights-unchanged `
  --write-paired-common-mode-repair-receipts `
  --write-final-seal `
  --no-runtime-output-change `
  --no-route-mutation `
  --no-weight-mutation `
  --no-production-claim
```

## 12. PASS Boundary

```text
sync_cadence_equivalent=true
measured_pair_count=2048
measured_batch_count=32
paired_scaled_log_mad<=0.13976194237515863
paired_drift_ratio<=1.20
paired_order_bias_ratio<=1.15
paired_comparative_validity=valid_absolute_environment_stable|valid_common_mode_environment_drift
performance_classification=non_regression_absolute_stable|non_regression_common_mode_drift|resolution_limited
shadow_output_committed=false
production_promotion_authorized=false
output_authority=burn
runtime_output_changed=false
```

R3 PASS authorizes only `ASH-TCU-K7N-D1R7_MULTI_SHAPE_PERFORMANCE_MATRIX`. It does not authorize production routing, Burn replacement, generalized speedup claims, full-vocabulary claims or production readiness.
