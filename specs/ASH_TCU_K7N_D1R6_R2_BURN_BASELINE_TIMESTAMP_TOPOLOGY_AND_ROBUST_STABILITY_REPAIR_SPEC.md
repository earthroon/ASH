# ASH-TCU-K7N-D1R6-R2 SPEC

## Burn Baseline Timestamp Topology and Robust Stability Repair

## 1. Identity

- Patch: `ASH-TCU-K7N-D1R6-R2_BURN_BASELINE_TIMESTAMP_TOPOLOGY_AND_ROBUST_STABILITY_REPAIR`
- PASS: `PASS_ASH_TCU_K7N_D1R6_R2_BURN_BASELINE_TIMESTAMP_TOPOLOGY_AND_ROBUST_STABILITY_REPAIR_KERNEL_SCOPED_BATCH_MEDIAN_VALID_NO_OUTPUT_COMMIT_NO_ROUTE_PROMOTION`
- Next: `ASH-TCU-K7N-D1R7_MULTI_SHAPE_PERFORMANCE_MATRIX`

## 2. Parent SSOT

```text
D1R5 execution=d1r5-5d4e541766f315af0896
numerical_parity_passed=true
exact_bit_match_count=16
failing_element_count=0
output_authority=burn
runtime_output_changed=false
```

R1 diagnostic failure:

```text
failed_gates=[burn_drift,burn_coefficient_of_variation,tensorcube_coefficient_of_variation]
burn_drift_ratio=1.3891891891891892
burn_raw_cv=1.6601810663604732
tensorcube_drift_ratio=1.0106382978723405
tensorcube_raw_cv=4.409925445733738
```

## 3. Repaired Measurement Authority

Burn removes external before/after timestamp marker submissions. Each raw Burn WGPU matmul is executed inside CubeCL `ComputeClient::profile` with device timing.

```text
burn_baseline_authority=burn_cubecl_matmul_fixture_path
burn_timing_authority=cubecl_compute_client_device_profile_scope
external_burn_marker_timing_used=false
profile_span_count_per_logical_sample=1
attribution_scope=complete_logical_operation_device_profile
```

CubeCL 0.9 exposes a complete device-profile span for the logical operation but not a stable public list of every internal kernel identity and duration. R2 does not fabricate per-kernel attribution or a kernel count. TensorCube remains measured by compute-pass timestamp writes around the canonical K6P dispatch.

## 4. Runtime, Fixture and Topology

```text
runtime=one authoritative Burn WGPU Device and Queue
fixture=ash_tcu_k7n_d1r3_fixture_m1_n16_k4_v1
shape=M1/N16/K4
workgroup=16x16x1
dispatch=1x1x1
handle-map hits=2
handle-map misses=0
host uploads=0

in_flight_depth=8
samples_per_cohort=8
cohorts_per_batch=8
samples_per_batch=64
measured_batches=32
measured_samples_per_implementation=2048
warmup_samples_per_implementation=128
order=AB/BA alternating
```

Burn output handles are released after each profiled sample. TensorCube reuses one scratch sequentially inside each cohort. Projection outputs are never copied or mapped.

## 5. Robust Stability SSOT

Raw CV is diagnostics only:

```text
raw_cv_hard_gate_authorized=false
```

Hard stability uses 32 batch medians:

```text
scaled_MAD=1.4826*MAD
normalized_MAD=scaled_MAD/median
NMAD<=0.15
first/last batch-median drift<=1.20
AB/BA batch-median order bias<=1.15
valid samples per batch=64
invalid logical samples=0
invalid batches=0
```

No sample deletion, trimming, winsorization, spike replacement, or retry-until-PASS is allowed.

## 6. Failure Evidence

After benchmark start, raw samples, batch medians, raw CV, NMAD, drift, order bias, failed gates, invalid-measurement seal and local manifest are written before returning an error.

## 7. Classification and Isolation

Classification order:

```text
measurement validity
catastrophic regression
resolution limited
non-regression
bounded regression
```

Original D1R6 performance thresholds are unchanged. Eligible classifications are `non_regression` and `resolution_limited`.

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

## 8. Required Audit Command

```powershell
cargo run --manifest-path .\crates\orchestrator_local\Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k7n_d1r6r2_burn_baseline_timestamp_topology_and_robust_stability_repair -- `
  --repo-root "D:\1111113232\DUST\1\ash_pass3" `
  --require-d1r5-pass `
  --require-d1r5-execution d1r5-5d4e541766f315af0896 `
  --require-d1r6r1-stability-diagnostic-failure `
  --require-d1r6r2-performance-eligibility `
  --require-parent-numerical-parity-passed `
  --require-parent-exact-bit-match-count 16 `
  --require-parent-failing-element-count 0 `
  --require-parent-output-authority burn `
  --require-fixture-id ash_tcu_k7n_d1r3_fixture_m1_n16_k4_v1 `
  --require-fixture-m 1 --require-fixture-n 16 --require-fixture-k 4 `
  --require-reference-digest a4916905d1827029e2e74aeb8d156698b1e1ea0d27134492fb382e76489ed200 `
  --execution-mode shadow_performance_topology_repair_audit `
  --require-runtime-device-authority burn_wgpu_runtime `
  --require-runtime-queue-authority burn_wgpu_runtime `
  --require-wgpu-authority ash.runtime_wgpu_type_authority.burn_runtime.wgpu26.v1 `
  --require-timestamp-query-supported `
  --require-timestamp-query-inside-encoders `
  --require-timestamp-query-inside-passes `
  --require-shader-int64-enabled `
  --reject-wall-clock-only-performance-pass `
  --create-one-authoritative-burn-runtime-context `
  --reject-extra-tensorcube-device --reject-extra-tensorcube-queue `
  --register-two-fixture-primitives `
  --require-primitive-handle-map-hits 2 --require-primitive-handle-map-misses 0 `
  --require-host-upload-count 0 `
  --bind-actual-burn-cubecl-matmul `
  --require-burn-baseline-authority burn_cubecl_matmul_fixture_path `
  --instrument-actual-burn-cubecl-device-profile `
  --reject-external-burn-marker-timing `
  --preflight-burn-profile-plan `
  --require-burn-profile-span-count-at-least 1 `
  --require-complete-burn-operation-attribution `
  --reject-burn-profile-plan-drift --reject-cross-sample-fusion `
  --measure-complete-burn-profile-span-per-logical-sample `
  --record-burn-profile-envelope-diagnostics `
  --bind-canonical-tensorcube-kernel `
  --require-tensorcube-route ash_tcu_vocab_atlas_tile_projection_f32_rhs_strided_view_v1 `
  --require-workgroup-geometry 16x16x1 --require-dispatch-geometry 1x1x1 `
  --require-tensorcube-kernel-count 1 `
  --require-in-flight-depth 8 --require-samples-per-cohort 8 `
  --require-cohorts-per-batch 8 --require-samples-per-batch 64 `
  --release-resources-after-each-cohort `
  --reject-unbounded-burn-output-retention `
  --require-sequential-tensorcube-scratch-reuse `
  --warmup-burn-count 128 --warmup-tensorcube-count 128 `
  --require-warmup-order burn_tensorcube_tensorcube_burn `
  --require-measured-batch-count 32 `
  --require-measured-sample-count-per-implementation 2048 `
  --alternate-measurement-order-ab-ba `
  --require-device-profile-scoped-gpu-time `
  --exclude-pipeline-creation-from-gpu-time `
  --exclude-preparation-from-gpu-time `
  --exclude-query-readback-from-gpu-time `
  --record-secondary-cpu-timings `
  --resolve-and-read-timestamp-queries `
  --require-timestamp-readback-only `
  --require-no-projection-output-readback `
  --retain-all-valid-samples --reject-outlier-deletion `
  --write-failure-evidence-before-return `
  --compute-raw-sample-diagnostics `
  --record-raw-coefficient-of-variation `
  --disable-raw-cv-as-hard-gate `
  --compute-32-batch-medians --require-valid-samples-per-batch 64 `
  --compute-scaled-median-absolute-deviation --require-mad-scale-factor 1.4826 `
  --compute-normalized-batch-median-mad `
  --require-batch-median-nmad-at-most 0.15 `
  --compute-batch-median-first-last-drift `
  --require-batch-median-drift-ratio-at-most 1.20 `
  --compute-batch-median-ab-ba-order-bias `
  --require-batch-median-order-bias-ratio-at-most 1.15 `
  --compute-tail-diagnostics `
  --require-zero-invalid-logical-samples --require-zero-invalid-batches `
  --classify-measurement-validity `
  --require-resolution-floor-min-ns 1000 `
  --require-resolution-floor-timestamp-multiplier 32 `
  --compute-median-speedup-ratio --compute-p95-speedup-ratio `
  --compute-median-and-p95-deltas `
  --require-non-regression-median-ratio-at-most 1.50 `
  --require-non-regression-median-delta-ns-at-most 5000 `
  --require-non-regression-p95-ratio-at-most 2.00 `
  --require-non-regression-p95-delta-ns-at-most 10000 `
  --require-catastrophic-median-ratio-over 2.00 `
  --require-catastrophic-median-delta-ns-over 10000 `
  --require-catastrophic-p95-ratio-over 3.00 `
  --require-catastrophic-p95-delta-ns-over 20000 `
  --classify-performance-result `
  --allow-resolution-limited-next-stage `
  --reject-bounded-regression-next-stage `
  --reject-catastrophic-regression `
  --require-no-numerical-parity-rerun `
  --require-no-shadow-output-commit --require-no-downstream-output-commit `
  --require-no-route-promotion --require-no-registry-write `
  --verify-burn-output-authority `
  --verify-registry-unchanged --verify-route-bindings-unchanged `
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
  --write-shadow-performance-repair-receipts `
  --write-final-seal `
  --no-runtime-output-change --no-route-mutation `
  --no-weight-mutation --no-production-claim
```

## 9. PASS Boundary

```text
measurement_valid=true
external_burn_marker_timing_used=false
raw_cv_hard_gate_authorized=false
burn_batch_median_nmad<=0.15
tensorcube_batch_median_nmad<=0.15
burn_batch_median_drift_ratio<=1.20
tensorcube_batch_median_drift_ratio<=1.20
burn_batch_median_order_bias_ratio<=1.15
tensorcube_batch_median_order_bias_ratio<=1.15
performance_classification=non_regression|resolution_limited
shadow_output_committed=false
production_promotion_authorized=false
output_authority=burn
runtime_output_changed=false
```

R2 PASS authorizes only `ASH-TCU-K7N-D1R7_MULTI_SHAPE_PERFORMANCE_MATRIX`.