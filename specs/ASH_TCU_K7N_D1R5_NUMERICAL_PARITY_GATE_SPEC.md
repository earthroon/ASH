# ASH-TCU-K7N-D1R5 SPEC

## Numerical Parity Gate

## 1. Identity

- Patch: `ASH-TCU-K7N-D1R5_NUMERICAL_PARITY_GATE`
- Status: `PASS_ASH_TCU_K7N_D1R5_NUMERICAL_PARITY_GATE_16_OF_16_WITHIN_ABS_1E_NEG5_REL_1E_NEG5_NO_OUTPUT_COMMIT`
- Path: `specs/ASH_TCU_K7N_D1R5_NUMERICAL_PARITY_GATE_SPEC.md`
- Class: offline deterministic CPU-reference numerical parity gate
- Next: `ASH-TCU-K7N-D1R6_SHADOW_PERFORMANCE_GATE`

D1R5 consumes immutable D1R4 readback evidence. It performs no Device creation, runtime preparation, TensorCube dispatch, Queue submission, buffer copy, map, or GPU readback.

## 2. Parent SSOT

Required parent:

```text
patch=ASH-TCU-K7N-D1R4_SHADOW_COMPLETION_AND_READBACK_GATE
execution=d1r4-2144d3b52d1c987397a6
eligibility=eligible_for_d1r5_numerical_parity_gate
fixture_id=ash_tcu_k7n_d1r3_fixture_m1_n16_k4_v1
gpu_completion_observed=true
readback_byte_length=64
readback_f32_count=16
finite_count=16
non_finite_count=0
parity_state=not_evaluated
output_authority=burn
runtime_output_changed=false
```

Parent manifest: `workspace/runtime/tensorcube/ash_tensorcube_k7n_d1r4_local_manifest_latest.json`

Parent final seal: `workspace/runtime/tensorcube/ash_tensorcube_k7n_d1r4_final_seal_latest.json`

Required parent digests:

```text
raw_bytes_digest=a4916905d1827029e2e74aeb8d156698b1e1ea0d27134492fb382e76489ed200
value_bits_digest=a4916905d1827029e2e74aeb8d156698b1e1ea0d27134492fb382e76489ed200
```

## 3. Immutable Evidence Resolution

D1R5 resolves the D1R4 artifact row named `runtime_readback_receipt` through the parent manifest.

Required checks:

1. `immutable_path` is under `artifacts/tensorcube/k7n_d1r4/d1r4-2144d3b52d1c987397a6/`.
2. The immutable file SHA-256 matches the manifest row.
3. `value_bits` contains exactly sixteen u32 words.
4. Each word is encoded little-endian into exactly 64 bytes.
5. The reconstructed digest matches both parent digests.
6. Console output and digest-only reconstruction are forbidden input sources.

## 4. Reference Authority

Reference authority: `cpu_scalar_f32_fixed_k_order_v1`

Fixture:

```text
M=1
N=16
K=4
LHS=[1.0,-2.0,0.5,3.0]
```

Stored RHS row formula:

```text
rhs[n,0]=n+1
rhs[n,1]=-(n+2)
rhs[n,2]=(n+3)*0.25
rhs[n,3]=n*2+1
n=0..15
```

Reference loop uses an `f32` accumulator and fixed `k=0,1,2,3` order. `f64` accumulation, `mul_add`, SIMD, parallel reduction, Burn reference execution, and TensorCube reference execution are forbidden.

Canonical f32 bits:

```text
41060000 418c0000 41d50000 420f0000
42338000 42580000 427c8000 42908000
42a2c000 42b50000 42c74000 42d98000
42ebc000 42fe0000 43082000 43114000
```

Canonical reference digest:

`a4916905d1827029e2e74aeb8d156698b1e1ea0d27134492fb382e76489ed200`

The scalar-calculated bits must match the canonical literal bits and digest before observed values are evaluated.

## 5. Tolerance Contract

```text
absolute_tolerance=1.0e-5
relative_tolerance=1.0e-5
error_measurement_dtype=f64
adaptive_retry_allowed=false
vendor_specific_threshold_allowed=false
```

Element predicate:

```text
abs_error=abs(observed-reference)
scale=max(abs(observed),abs(reference))
rel_error=0 when scale=0, otherwise abs_error/scale
pass=(abs_error<=1e-5) OR (rel_error<=1e-5)
```

Tolerance widening after observation is forbidden. Exact f32 bit equality and signed-zero differences are recorded separately from tolerance parity.

## 6. Expected Current Result

```text
element_count=16
passing_element_count=16
failing_element_count=0
exact_bit_match_count=16
exact_bit_mismatch_count=0
signed_zero_mismatch_count=0
maximum_absolute_error=0.0
maximum_relative_error=0.0
first_mismatch_index=null
mismatch_indices=[]
numerical_parity_passed=true
```

These values must be calculated from immutable D1R4 `value_bits`; the specification is not an authority to emit them without evaluation.

## 7. Zero GPU and Zero Commit Boundary

```text
device_creation_count=0
queue_creation_count=0
runtime_preparation_count=0
tensorcube_dispatch_count=0
queue_submit_count=0
buffer_copy_count=0
map_async_count=0
gpu_readback_count=0
shadow_output_commit_count=0
downstream_output_commit_count=0
route_mutation_count=0
registry_write_count=0
model_weight_mutation_count=0
shadow_output_commit_authorized=false
shadow_output_committed=false
output_authority=burn
runtime_output_changed=false
```

## 8. Required Files

Backend-independent parity modules:

```text
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r5_fixture_reference.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r5_reference_self_check.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r5_observed_evidence.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r5_tolerance_contract.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r5_element_parity.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r5_aggregate_metrics.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r5_parity_receipt.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r5_parity_error.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r5_contract_audit.rs
crates/burn_webgpu_backend/src/tensorcube_k7n_d1r5_verdict.rs
```

Model contract: `crates/model_core/src/vocab_atlas_numerical_parity_contract.rs`

Orchestrator:

```text
crates/orchestrator_local/src/ash_tcu_k7n_d1r5_numerical_parity_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7n_d1r5_numerical_parity_gate.rs
```

## 9. Required Audit Command

```powershell
cargo run --manifest-path .\crates\orchestrator_local\Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_tcu_k7n_d1r5_numerical_parity_gate -- `
  --repo-root "D:\1111113232\DUST\1\ash_pass3" `
  --require-d1r4-pass `
  --require-d1r4-execution d1r4-2144d3b52d1c987397a6 `
  --require-d1r5-parity-eligibility `
  --require-parent-fixture-id ash_tcu_k7n_d1r3_fixture_m1_n16_k4_v1 `
  --require-parent-gpu-completion-observed `
  --require-parent-readback-byte-length 64 `
  --require-parent-readback-f32-count 16 `
  --require-parent-finite-count 16 `
  --require-parent-non-finite-count 0 `
  --require-parent-parity-state not_evaluated `
  --require-parent-output-authority burn `
  --require-observed-raw-digest a4916905d1827029e2e74aeb8d156698b1e1ea0d27134492fb382e76489ed200 `
  --require-observed-value-bits-digest a4916905d1827029e2e74aeb8d156698b1e1ea0d27134492fb382e76489ed200 `
  --load-immutable-d1r4-readback-evidence `
  --reject-console-value-parsing `
  --validate-observed-value-count 16 `
  --reconstruct-observed-bytes-little-endian `
  --validate-observed-byte-length 64 `
  --verify-observed-digests `
  --build-cpu-scalar-f32-reference `
  --require-reference-authority cpu_scalar_f32_fixed_k_order_v1 `
  --require-reference-m 1 `
  --require-reference-n 16 `
  --require-reference-k 4 `
  --require-fixed-k-order `
  --reject-f64-reference-accumulation `
  --reject-mul-add-reference `
  --reject-simd-reference `
  --reject-burn-reference `
  --reject-tensorcube-reference `
  --verify-canonical-reference-vector `
  --verify-canonical-reference-bits `
  --require-reference-digest a4916905d1827029e2e74aeb8d156698b1e1ea0d27134492fb382e76489ed200 `
  --require-absolute-tolerance 0.00001 `
  --require-relative-tolerance 0.00001 `
  --verify-fixed-tolerance-contract `
  --compare-elementwise-absolute-and-relative `
  --require-element-count 16 `
  --record-exact-bit-matches `
  --record-signed-zero-diagnostics `
  --record-mismatch-indices `
  --record-maximum-errors `
  --require-passing-element-count 16 `
  --require-failing-element-count 0 `
  --require-exact-bit-match-count 16 `
  --require-exact-bit-mismatch-count 0 `
  --require-maximum-absolute-error 0.0 `
  --require-maximum-relative-error 0.0 `
  --require-empty-mismatch-indices `
  --require-numerical-parity-passed `
  --require-no-device-creation `
  --require-no-queue-creation `
  --require-no-runtime-preparation `
  --require-no-tensorcube-dispatch `
  --require-no-queue-submit `
  --require-no-buffer-copy `
  --require-no-map-async `
  --require-no-gpu-readback `
  --require-no-shadow-output-commit `
  --require-no-downstream-output-commit `
  --verify-burn-output-authority `
  --classify-d1r5-parity-eligibility `
  --verify-registry-unchanged `
  --verify-route-bindings-unchanged `
  --verify-route-epoch-unchanged `
  --verify-d1r4-readback-contract-unchanged `
  --verify-d1r3-dispatch-contract-unchanged `
  --verify-d1r2-preparation-contract-unchanged `
  --verify-d1r1-admission-contract-unchanged `
  --verify-d0r3-candidate-contract-unchanged `
  --verify-k6p-canonical-source-unchanged `
  --verify-vocab-atlas-burn-computation-preserved `
  --verify-model-weights-unchanged `
  --write-numerical-parity-receipts `
  --write-final-seal `
  --no-runtime-output-change `
  --no-route-mutation `
  --no-weight-mutation `
  --no-performance-claim
```

## 10. PASS Marker

```text
PASS_ASH_TCU_K7N_D1R5_NUMERICAL_PARITY_GATE_16_OF_16_WITHIN_ABS_1E_NEG5_REL_1E_NEG5_NO_OUTPUT_COMMIT
```

## 11. PASS Verdict

```text
the_d1r4_tensorcube_readback_was_validated_against_an_independent_fixed_order_f32_cpu_scalar_reference_with_all_sixteen_elements_within_absolute_1e_neg5_or_relative_1e_neg5_tolerance_all_sixteen_f32_bit_patterns_exactly_matching_zero_absolute_and_relative_error_and_candidate_eligible_for_d1r6_shadow_performance_gate_without_gpu_reexecution_output_commit_route_mutation_or_burn_authority_change
```

Expected eligibility: `eligible_for_d1r6_shadow_performance_gate`.

## 12. Non-Authorization and Next State

D1R5 PASS does not authorize production TensorCube routing, output commit, Burn replacement, merged-logits substitution, sampler substitution, Registry registration, route mutation, generalized multi-shape parity, performance claims, or production promotion.

Only the following patch is authorized next:

`ASH-TCU-K7N-D1R6_SHADOW_PERFORMANCE_GATE`
