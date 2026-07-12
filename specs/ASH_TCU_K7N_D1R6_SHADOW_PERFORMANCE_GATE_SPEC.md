# ASH-TCU-K7N-D1R6 SPEC

## Shadow Performance Gate

## 1. Identity

- Patch: `ASH-TCU-K7N-D1R6_SHADOW_PERFORMANCE_GATE`
- Status: `PASS_ASH_TCU_K7N_D1R6_SHADOW_PERFORMANCE_GATE_GPU_TIMESTAMP_VALID_BURN_BASELINE_COMPARED_NO_CATASTROPHIC_REGRESSION_NO_OUTPUT_COMMIT_NO_ROUTE_PROMOTION`
- Path: `specs/ASH_TCU_K7N_D1R6_SHADOW_PERFORMANCE_GATE_SPEC.md`
- Next: `ASH-TCU-K7N-D1R7_MULTI_SHAPE_PERFORMANCE_MATRIX`

D1R6 measures the bit-exact D1R5 fixture on one authoritative Burn WGPU Device and Queue. It compares the actual Burn `Tensor<InferenceBackend>::matmul` path against the canonical TensorCube K6P shader without adopting either shadow output.

## 2. Parent SSOT

```text
patch=ASH-TCU-K7N-D1R5_NUMERICAL_PARITY_GATE
execution=d1r5-5d4e541766f315af0896
eligibility=eligible_for_d1r6_shadow_performance_gate
numerical_parity_passed=true
exact_bit_match_count=16
failing_element_count=0
output_authority=burn
runtime_output_changed=false
```

Parent manifest:

`workspace/runtime/tensorcube/ash_tensorcube_k7n_d1r5_local_manifest_latest.json`

Parent final seal:

`workspace/runtime/tensorcube/ash_tensorcube_k7n_d1r5_final_seal_latest.json`

## 3. Fixture

```text
fixture_id=ash_tcu_k7n_d1r3_fixture_m1_n16_k4_v1
M=1
N=16
K=4
workgroup=16x16x1
dispatch=1x1x1
reference_digest=a4916905d1827029e2e74aeb8d156698b1e1ea0d27134492fb382e76489ed200
```

The fixture inputs, shape, stride-aware RHS view, and canonical TensorCube shader identity must remain unchanged.

## 4. Runtime Authority

Required authority:

`ash.runtime_wgpu_type_authority.burn_runtime.wgpu26.v1`

Required resources:

```text
burn_runtime_context_count=1
tensorcube_extra_device_count=0
tensorcube_extra_queue_count=0
same_device=true
same_queue=true
```

Required features:

```text
TIMESTAMP_QUERY=true
TIMESTAMP_QUERY_INSIDE_ENCODERS=true
TIMESTAMP_QUERY_INSIDE_PASSES=true
SHADER_INT64=true
```

CPU wall-clock alone cannot produce PASS.

## 5. Strict Fixture Registration

```text
fixture_handle_registration_count=2
primitive_handle_map_hits=2
primitive_handle_map_misses=0
raw_borrows=2
host_uploads=0
metadata_only=0
```

No host-upload fallback is allowed.

## 6. Benchmark Authorities

Burn baseline authority:

`burn_cubecl_matmul_fixture_path`

Concrete baseline operation:

```rust
lhs.clone().matmul(rhs_logical.clone())
```

TensorCube authority:

```text
route=ash_tcu_vocab_atlas_tile_projection_f32_rhs_strided_view_v1
shader=canonical K6P WGSL
workgroup=16x16x1
dispatch=1x1x1
```

A no-op, CPU loop, precomputed output, alternate WGSL, or relabeled TensorCube kernel is forbidden.

## 7. Timing Topology

TensorCube timing uses `ComputePassTimestampWrites`, so the recorded interval contains the measured compute pass.

Burn timing uses two timestamp markers on the same authoritative Queue surrounding one real Burn matmul submission. This is a queue-bracketed Burn GPU interval because the public Burn path does not expose its internal compute-pass descriptor.

Both measurements use the same timestamp period and Queue clock domain. This patch does not promote the ratio to a generalized production speedup claim.

Projection output readback is forbidden. Only timestamp query resolve and timestamp staging map are allowed.

## 8. Phase Separation

The following CPU metrics are recorded separately:

```text
burn_pipeline_creation_cpu_ns
tensorcube_pipeline_creation_cpu_ns
burn_preparation_cpu_ns
tensorcube_preparation_cpu_ns
```

They are not merged into GPU sample durations.

Benchmark resources may be reused only within the D1R6 lexical execution. Persistent pipeline cache, Registry storage, and cross-process handle reuse are forbidden.

## 9. Warmup and Measured Cardinality

Warmup order:

```text
64 Burn
64 TensorCube
64 TensorCube
64 Burn
```

Warmup totals:

```text
Burn=128
TensorCube=128
```

Measured configuration:

```text
batches=32
samples_per_batch_per_implementation=64
Burn measured samples=2048
TensorCube measured samples=2048
```

Batch order alternates AB/BA:

```text
even batch: Burn -> TensorCube
odd batch: TensorCube -> Burn
```

All valid samples are retained. Outlier deletion, trimming, winsorization, and result-seeking reruns are forbidden.

## 10. Timestamp Validation

Each sample contains:

```text
begin_ticks
end_ticks
delta_ticks
timestamp_period_ns
dispatch_gpu_ns
valid
invalid_reason
```

Required validity:

```text
end_ticks >= begin_ticks
delta_ticks > 0
timestamp_period_ns > 0
dispatch_gpu_ns finite
```

PASS requires exactly 2048 valid and zero invalid samples for each implementation.

## 11. Statistics

For Burn and TensorCube separately:

```text
minimum
maximum
mean
median
p95
p99
standard deviation
coefficient of variation
first-quartile median
last-quartile median
drift ratio
first-position median
second-position median
order-bias ratio
```

Median uses the average of the middle pair. p95 and p99 use nearest-rank over ascending values. Ties use canonical tensor/batch order.

Required stability thresholds:

```text
order_bias_ratio <= 1.15
drift_ratio <= 1.20
coefficient_of_variation <= 0.25
```

A threshold violation yields `invalid_measurement` and no PASS marker.

## 12. Resolution Floor

```text
resolution_floor_ns=max(1000,timestamp_period_ns*32)
```

When both medians are below the floor:

```text
performance_classification=resolution_limited
```

Resolution-limited is eligible for D1R7 but is not a speedup claim.

## 13. Classification Order

```text
measurement validity
-> catastrophic regression
-> resolution limited
-> non-regression
-> bounded regression
```

Non-regression requires both median and p95 predicates.

```text
TensorCube median <= Burn median * 1.50
OR median delta <= 5000 ns

TensorCube p95 <= Burn p95 * 2.00
OR p95 delta <= 10000 ns
```

Catastrophic median regression:

```text
TensorCube median > Burn median * 2.00
AND median delta > 10000 ns
```

Catastrophic p95 regression:

```text
TensorCube p95 > Burn p95 * 3.00
AND p95 delta > 20000 ns
```

Eligible classifications:

```text
non_regression
resolution_limited
```

Blocked classifications:

```text
bounded_regression
catastrophic_regression
invalid_measurement
```

## 14. Isolation

Required zero state:

```text
projection_output_readback_count=0
numerical_parity_rerun_count=0
shadow_output_commit_authorized=false
shadow_output_committed=false
production_promotion_authorized=false
production_route_enabled=false
route_mutation_count=0
registry_write_count=0
runtime_output_changed=false
output_authority=burn
```

D1R6 may read timestamp buffers only. It must not map Burn or TensorCube projection output.

## 15. Required Files

Backend:

```text
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r6_execution_mode.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r6_benchmark_config.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r6_benchmark_resources.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r6_burn_baseline.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r6_tensorcube_benchmark.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r6_timestamp_queries.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r6_gpu_sample.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r6_statistics.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r6_order_bias.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r6_drift_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r6_resolution_floor.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r6_performance_classification.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r6_performance_receipt.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r6_performance_error.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r6_runtime_benchmark.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r6_contract_audit.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r6_verdict.rs
```

Model contract:

`crates/model_core/src/vocab_atlas_shadow_performance_contract.rs`

Orchestrator:

```text
crates/orchestrator_local/src/ash_tcu_k7n_d1r6_shadow_performance_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7n_d1r6_shadow_performance_gate.rs
```

## 16. Required Audit Command

```powershell
cargo run --manifest-path .\crates\orchestrator_local\Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k7n_d1r6_shadow_performance_gate -- `
  --repo-root "D:\1111113232\DUST\1\ash_pass3" `
  --require-d1r5-pass `
  --require-d1r5-execution d1r5-5d4e541766f315af0896 `
  --require-d1r6-performance-eligibility `
  --require-parent-numerical-parity-passed `
  --require-parent-exact-bit-match-count 16 `
  --require-parent-failing-element-count 0 `
  --require-parent-output-authority burn `
  --require-parent-runtime-output-unchanged `
  --require-fixture-id ash_tcu_k7n_d1r3_fixture_m1_n16_k4_v1 `
  --require-fixture-m 1 `
  --require-fixture-n 16 `
  --require-fixture-k 4 `
  --require-reference-digest a4916905d1827029e2e74aeb8d156698b1e1ea0d27134492fb382e76489ed200 `
  --execution-mode shadow_performance_audit `
  --require-runtime-device-authority burn_wgpu_runtime `
  --require-runtime-queue-authority burn_wgpu_runtime `
  --require-wgpu-authority ash.runtime_wgpu_type_authority.burn_runtime.wgpu26.v1 `
  --require-timestamp-query-supported `
  --require-timestamp-query-enabled `
  --require-shader-int64-enabled `
  --reject-wall-clock-only-performance-pass `
  --create-one-authoritative-burn-runtime-context `
  --reject-extra-tensorcube-device `
  --reject-extra-tensorcube-queue `
  --register-two-fixture-primitives `
  --require-primitive-handle-map-hits 2 `
  --require-primitive-handle-map-misses 0 `
  --require-host-upload-count 0 `
  --bind-burn-baseline-kernel `
  --require-burn-baseline-authority burn_cubecl_matmul_fixture_path `
  --bind-canonical-tensorcube-kernel `
  --require-tensorcube-route ash_tcu_vocab_atlas_tile_projection_f32_rhs_strided_view_v1 `
  --require-workgroup-geometry 16x16x1 `
  --require-dispatch-geometry 1x1x1 `
  --measure-burn-pipeline-creation-cpu-time `
  --measure-tensorcube-pipeline-creation-cpu-time `
  --measure-burn-preparation-cpu-time `
  --measure-tensorcube-preparation-cpu-time `
  --require-benchmark-scope-resource-reuse `
  --reject-persistent-pipeline-cache `
  --warmup-burn-count 128 `
  --warmup-tensorcube-count 128 `
  --require-warmup-order burn_tensorcube_tensorcube_burn `
  --require-measured-batch-count 32 `
  --require-measured-samples-per-batch 64 `
  --require-measured-sample-count-per-implementation 2048 `
  --alternate-measurement-order-ab-ba `
  --write-two-gpu-timestamps-per-dispatch `
  --require-query-count-per-batch 128 `
  --measure-dispatch-only-gpu-time `
  --exclude-pipeline-creation-from-gpu-time `
  --exclude-preparation-from-gpu-time `
  --exclude-query-readback-from-gpu-time `
  --record-secondary-cpu-encode-submit-time `
  --resolve-and-read-timestamp-queries `
  --require-timestamp-readback-only `
  --require-no-projection-output-readback `
  --require-zero-invalid-timestamp-samples `
  --retain-all-valid-samples `
  --reject-outlier-deletion `
  --compute-min-max-mean-median-p95-p99 `
  --compute-standard-deviation-and-cv `
  --compute-first-last-quartile-drift `
  --compute-ab-ba-order-bias `
  --require-order-bias-ratio-at-most 1.15 `
  --require-drift-ratio-at-most 1.20 `
  --require-coefficient-of-variation-at-most 0.25 `
  --require-resolution-floor-min-ns 1000 `
  --require-resolution-floor-timestamp-multiplier 32 `
  --compute-median-speedup-ratio `
  --compute-p95-speedup-ratio `
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
  --write-shadow-performance-receipts `
  --write-final-seal `
  --no-runtime-output-change `
  --no-route-mutation `
  --no-weight-mutation `
  --no-production-claim
```

## 17. PASS Marker

```text
PASS_ASH_TCU_K7N_D1R6_SHADOW_PERFORMANCE_GATE_GPU_TIMESTAMP_VALID_BURN_BASELINE_COMPARED_NO_CATASTROPHIC_REGRESSION_NO_OUTPUT_COMMIT_NO_ROUTE_PROMOTION
```

PASS requires either:

```text
performance_classification=non_regression
shadow_performance_eligibility=eligible_for_d1r7_multi_shape_performance_matrix
```

or:

```text
performance_classification=resolution_limited
shadow_performance_eligibility=eligible_for_d1r7_multi_shape_performance_matrix_resolution_limited
```

Required common state:

```text
measurement_valid=true
measured_sample_count_burn=2048
measured_sample_count_tensorcube=2048
invalid_sample_count_burn=0
invalid_sample_count_tensorcube=0
projection_output_readback_count=0
numerical_parity_rerun_count=0
shadow_output_commit_authorized=false
shadow_output_committed=false
production_promotion_authorized=false
production_route_enabled=false
output_authority=burn
runtime_output_changed=false
```

## 18. Non-Authorization

D1R6 PASS does not authorize production routing, output adoption, Burn replacement, persistent pipeline cache, generalized speedup claims, full-vocabulary claims, ragged-tail claims, route mutation, Registry promotion, or production readiness.

Only the following patch is authorized next:

`ASH-TCU-K7N-D1R7_MULTI_SHAPE_PERFORMANCE_MATRIX`
