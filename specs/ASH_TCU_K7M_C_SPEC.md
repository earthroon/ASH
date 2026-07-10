# ASH-TCU-K7M-C SPEC

## Title

Execution Evidence Binding / Actual WGPU Queue Submit Dispatch Readback CPU Burn Comparison / Current Capability Evidence / No Historical Event Backfill No Route Mutation Seal

## Patch ID

```txt
ASH-TCU-K7M-C
```

## Status Target

```txt
PASS_ASH_TCU_K7M_C_EXECUTION_EVIDENCE_BINDING_ACTUAL_GPU_MEASUREMENT_NO_HISTORICAL_BACKFILL_NO_ROUTE_MUTATION_SEAL
```

## Parent

```txt
ASH-TCU-K7M-B
```

Required prior status:

```txt
PASS_ASH_TCU_K7M_B_LEGACY_RECEIPT_TRUTH_RECLASSIFICATION_NO_LEGACY_VALUE_REWRITE_NO_RUNTIME_MUTATION_SEAL
```

Required prior verdict:

```txt
legacy_receipt_truth_reclassified_by_read_only_sidecar_overlay
```

## Purpose

K7M-C performs a new, directly observed TensorCube WGPU execution and binds the resulting execution, readback, CPU parity, and Burn parity evidence to the K7M-A evidence schema.

K7M-C proves only current capability. It must not use a new run as proof of a historical K6ZV through K7L event, rewrite legacy receipts or K7M-B annotations, claim route mutation, claim runtime decode or assistant output change, execute rollback, mutate weights, or promote a performance claim.

## Canonical Fixture

Use the existing K6P row-major execution path:

```txt
candidate_id = ash_tcu_k6p_row_major_emit_candidate_v1
M = 256
N = 256
K = 32
input_dtype = f32
accumulator_dtype = f32
output_dtype = f32
output_layout = row_major
output_element_count = 65536
```

K7M-C must not introduce an optimized replacement kernel.

## SSOT

```txt
workspace/runtime/tensorcube/ash_tensorcube_k7m_c_execution_evidence_bundle_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_c_execution_evidence_binding_index_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_c_current_capability_evidence_latest.json
```

Secondary receipts:

```txt
workspace/runtime/tensorcube/ash_tensorcube_k7m_c_prior_k7m_b_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_c_execution_recipe_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_c_adapter_device_identity_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_c_queue_submit_evidence_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_c_dispatch_evidence_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_c_readback_evidence_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_c_cpu_comparison_evidence_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_c_burn_comparison_evidence_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_c_protected_claim_binding_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_c_historical_backfill_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_c_no_route_mutation_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_c_no_runtime_output_claim_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_c_no_weight_mutation_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_c_no_performance_claim_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_c_static_checks_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7m_c_verdict_latest.json
artifacts/ASH_TCU_K7M_C_LOCAL_MANIFEST.json
```

## Required Actual Evidence

### Execution identity

A unique per-run execution ID and reproducible recipe digest are required. The execution ID must include runtime entropy or a monotonic/timestamp component and must not be a constant.

### Adapter and device identity

Record adapter name, backend, driver/device information available from wgpu, normalized adapter/device fingerprints, and relevant compute/storage limits. Unavailable optional fields must be marked unavailable rather than invented.

### Queue submission

Required fields:

```txt
command_encoder_created = true
compute_pass_created = true
command_buffer_finished = true
queue_submit_count >= 1
submitted_command_buffer_count >= 1
queue_submission_completed = true
device_poll_completed = true
submission_digest is present
```

A CLI flag cannot satisfy queue submission evidence.

### Dispatch

Required fields:

```txt
dispatch_encoded = true
dispatch_submitted = true
dispatch_x > 0
dispatch_y > 0
dispatch_z > 0
total_workgroup_count > 0
expected_output_element_count = 65536
dispatch_digest is present
```

### Readback

Required fields:

```txt
readback_copy_encoded = true
readback_map_requested = true
readback_map_completed = true
mapped_byte_count = expected_byte_count
measured_element_count = 65536
output_digest is present
readback_digest is present
nan_count = 0
positive_infinity_count = 0
negative_infinity_count = 0
output_all_finite = true
```

### CPU comparison

Use the existing K6P tolerance policy. Require comparison completed, 65536 elements checked, zero mismatches, and parity passed.

### Burn comparison

Require Burn baseline execution, comparison completed, 65536 elements checked, zero mismatches, and parity passed.

## K7M-A Evidence Binding

Create and validate four typed evidence records:

```txt
native_wgpu_dispatch_executed -> ExecutedGpu / Executed
gpu_output_measured -> MeasuredReadback / Measured
cpu_parity_passed -> ComparedAgainstCpu / Compared
burn_parity_passed -> ComparedAgainstBurn / Compared
```

Each record must carry the actual execution ID and the required dispatch/readback digests and must pass `validate_protected_claim`.

K7M-C must not satisfy route mutation, runtime output change, assistant output change, or rollback protected claims.

## Historical Backfill Boundary

K7M-C may reference K7M-B annotations only as current capability references.

Every legacy binding must preserve:

```txt
historical_event_backfilled = false
legacy_annotation_rewritten = false
```

K7M-C must not modify K7M-B sidecar evidence class, authority, claim origin, policy result, or original claim value.

## No Mutation Guards

K7M-C must prove:

```txt
default_route_registry_mutated_by_k7m_c = false
user_visible_route_registry_mutated_by_k7m_c = false
production_route_registry_mutated_by_k7m_c = false
runtime_decode_output_changed_by_k7m_c = false
assistant_message_output_changed_by_k7m_c = false
rollback_execution_started_by_k7m_c = false
model_weights_mutated = false
optimizer_state_mutated = false
safetensors_checkpoint_mutated = false
performance_claim_allowed = false
```

If no central route registry exists, record the owner as unavailable and do not fabricate epoch or hash.

## Implementation Files

```txt
crates/burn_webgpu_backend/src/tensorcube_k7m_c_execution_mode.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_c_execution_identity.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_c_execution_recipe.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_c_adapter_device_identity.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_c_queue_submit_evidence.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_c_dispatch_evidence.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_c_readback_evidence.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_c_cpu_comparison_evidence.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_c_burn_comparison_evidence.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_c_binding_kind.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_c_execution_evidence_binding.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_c_current_capability_evidence.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_c_prior_k7m_b_receipt.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_c_execution_evidence_bundle.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_c_protected_claim_binding.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_c_historical_backfill_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_c_no_route_mutation_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_c_no_runtime_output_claim_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_c_no_weight_mutation_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_c_no_performance_claim_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_c_verdict.rs
crates/burn_webgpu_backend/src/tensorcube_k7m_c_contract_audit.rs
crates/orchestrator_local/src/ash_tcu_k7m_c_execution_evidence_binding_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7m_c_execution_evidence_binding_audit.rs
```

## CLI

```powershell
cargo run --manifest-path ./crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_tcu_k7m_c_execution_evidence_binding_audit -- --repo-root <repo> --require-k7m-b-pass --execute-canonical-wgpu-fixture --capture-adapter-device-identity --capture-queue-submit-evidence --capture-dispatch-evidence --capture-readback-evidence --compare-against-cpu --compare-against-burn --bind-protected-current-capability-claims --write-execution-evidence-bundle --write-execution-binding-index --reject-historical-event-backfill --no-route-mutation --no-runtime-output-claim --no-weight-mutation --no-performance-claim
```

## PASS Markers

```txt
PASS_ASH_TCU_K7M_C_PRIOR_K7M_B_RECEIPT
PASS_ASH_TCU_K7M_C_EXECUTION_RECIPE
PASS_ASH_TCU_K7M_C_ADAPTER_DEVICE_IDENTITY
PASS_ASH_TCU_K7M_C_QUEUE_SUBMIT_EVIDENCE
PASS_ASH_TCU_K7M_C_DISPATCH_EVIDENCE
PASS_ASH_TCU_K7M_C_READBACK_EVIDENCE
PASS_ASH_TCU_K7M_C_CPU_COMPARISON_EVIDENCE
PASS_ASH_TCU_K7M_C_BURN_COMPARISON_EVIDENCE
PASS_ASH_TCU_K7M_C_EXECUTED_GPU_PROTECTED_CLAIM
PASS_ASH_TCU_K7M_C_MEASURED_READBACK_PROTECTED_CLAIM
PASS_ASH_TCU_K7M_C_CPU_PARITY_PROTECTED_CLAIM
PASS_ASH_TCU_K7M_C_BURN_PARITY_PROTECTED_CLAIM
PASS_ASH_TCU_K7M_C_CURRENT_CAPABILITY_EVIDENCE
PASS_ASH_TCU_K7M_C_HISTORICAL_BACKFILL_REJECTED
PASS_ASH_TCU_K7M_C_NO_ROUTE_MUTATION
PASS_ASH_TCU_K7M_C_NO_RUNTIME_OUTPUT_CLAIM
PASS_ASH_TCU_K7M_C_NO_WEIGHT_MUTATION
PASS_ASH_TCU_K7M_C_NO_PERFORMANCE_CLAIM
PASS_ASH_TCU_K7M_C_EXECUTION_EVIDENCE_BINDING_ACTUAL_GPU_MEASUREMENT_NO_HISTORICAL_BACKFILL_NO_ROUTE_MUTATION_SEAL
```

## Static Checks

Use:

```txt
static_json_grouping = atlas_parallel_grouped_static_checks_v1
```

Static checks must derive execution, dispatch, readback, and parity values from the actual run and must not hardcode measured success fields.

## Recommended Next Patch

```txt
ASH-TCU-K7N-A
Central Route Registry SSOT / Runtime-Owned Route Epoch And Snapshot State / No Route Adoption No Production Replacement Seal
```

## Final Seal

K7M-C performs a real TensorCube WGPU execution and proves current dispatch, readback, CPU parity, and Burn parity capability. It does not rewrite history, mutate runtime routes, claim runtime output changes, execute rollback, mutate weights, or promote performance or production claims.
