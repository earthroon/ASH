# ASH-TCU-K6ZW SPEC

## Title

Apply Queue Entry / Operator Gate / Logical16 Native WGPU Parity Candidate To Explicit Apply Queue / No Default Adoption No Production Replacement Seal

## Patch ID

```txt
ASH-TCU-K6ZW
```

## Status Target

```txt
PASS_ASH_TCU_K6ZW_APPLY_QUEUE_ENTRY_OPERATOR_GATE_NO_DEFAULT_ADOPTION_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Parent Patch

```txt
ASH-TCU-K6ZV
```

## Required Prior Status

```txt
PASS_ASH_TCU_K6ZV_LOGICAL16_NATIVE_WGPU_STRICT_PARITY_NO_CPU_RUNTIME_SELECTION_NO_APPLY_QUEUE_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Required Prior Verdict

```txt
logical16_native_wgpu_strict_parity_pass_no_cpu_runtime_selection_no_apply_queue
```

## Purpose

`ASH-TCU-K6ZW` uses the K6ZV logical16 native WGPU strict parity evidence as the required parent state and creates an explicit apply queue candidate behind an operator gate.

K6ZV proved that the logical 16x16 TensorCube path can execute through native WGPU strict parity without CPU runtime selection.

K6ZW is the first patch in this chain allowed to create an apply queue candidate.

K6ZW does not execute the apply candidate. K6ZW does not change the default route. K6ZW does not replace production route. K6ZW does not open user-visible adoption.

K6ZW does not bind base_train, weight atlas, GPU streaming, loss/backward, optimizer, weight commit, safetensors mutation, or checkpoint finalization.

## Current K6ZV Baseline

K6ZV established:

```txt
logical16_native_wgpu_strict_parity_passed = true
native_wgpu_dispatch_evidence_valid = true
native_wgpu_dispatch_executed = true
cpu_reference_used_for_parity = true
cpu_reference_used_for_runtime_selection = false
diagnostic_readback_only = true
apply_queue_ready = false
production_replacement_executed = false
global_default_route_changed = false
performance_claim_allowed = false
recommended_next_patch = ASH-TCU-K6ZW_APPLY_QUEUE_ENTRY_OPERATOR_GATE_NO_DEFAULT_ADOPTION
```

K6ZW must treat this as the required parent condition.

## SSOT

### SSOT Owner

```txt
workspace/runtime/tensorcube/ash_tensorcube_k6zw_apply_queue_entry_latest.json
```

### Secondary Receipts

```txt
workspace/runtime/tensorcube/ash_tensorcube_k6zw_prior_k6zv_native_parity_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zw_apply_candidate_descriptor_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zw_operator_gate_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zw_apply_queue_entry_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zw_apply_queue_non_execution_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zw_no_default_adoption_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zw_no_production_replacement_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zw_no_user_visible_adoption_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zw_rollback_binding_packet_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zw_verdict_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zw_static_checks_latest.json
artifacts/ASH_TCU_K6ZW_LOCAL_MANIFEST.json
```

## State Ownership

### K6ZW owns

```txt
apply_candidate_descriptor
operator_gate
apply_queue_entry
apply_queue_non_execution_guard
no_default_adoption_guard
no_production_replacement_guard
no_user_visible_adoption_guard
rollback_binding_packet
```

### K6ZW does not own

```txt
TensorCube candidate creation
K6P row-major candidate emit
K6ZQ limited production-shadow bind
K6ZR original runtime monitor
K6ZS promotion review
K6ZT provenance rebind
K6ZU fresh runtime replay evidence closure
K6ZV native WGPU strict parity execution
operator approval grant
apply execution
runtime splice
production route replacement
default route adoption
user-visible adoption
base_train route binding
weight atlas construction
GPU streaming
training execution
loss/backward execution
optimizer step
weight commit
safetensors mutation
checkpoint finalization
```

## Source Inputs

K6ZW must read and validate the latest K6ZV receipts:

```txt
workspace/runtime/tensorcube/ash_tensorcube_k6zv_prior_k6zu_replay_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zv_logical16_tile_mode_contract_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zv_native_wgpu_adapter_preflight_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zv_native_dispatch_plan_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zv_cpu_reference_parity_oracle_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zv_native_wgpu_parity_result_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zv_no_cpu_runtime_selection_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zv_diagnostic_readback_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zv_no_apply_queue_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zv_no_production_replacement_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zv_verdict_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zv_static_checks_latest.json
artifacts/ASH_TCU_K6ZV_LOCAL_MANIFEST.json
```

K6ZW may read prior TensorCube candidate metadata only as configuration source:

```txt
workspace/runtime/tensorcube/ash_tensorcube_k6zs_promotion_review_config_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zu_shadow_replay_config_latest.json
```

K6ZW must not recompute K6ZV parity evidence. K6ZW must not treat K6ZV evidence as production replacement approval.

## Candidate Route

K6ZW must preserve the K6ZV candidate metadata:

```txt
candidate_route = ash_tcu_k6p_row_major_emit_candidate_v1
candidate_dtype = f32
candidate_output_layout = row_major
candidate_shape = [256, 256, 32]
tile_mode = Tile16LogicalFromTile8
physical_tile_rows = 8
physical_tile_cols = 8
logical_tile_rows = 16
logical_tile_cols = 16
physical_tile_count_per_logical_tile = 4
creates_contiguous_physical_16x16_kernel = false
new_vtc16_wgsl_created = false
base_row_major_emit_patch = ASH-TCU-K6P
base_limited_production_shadow_bind_patch = ASH-TCU-K6ZQ
base_limited_production_shadow_runtime_monitor_patch = ASH-TCU-K6ZR
base_promotion_review_patch = ASH-TCU-K6ZS
base_provenance_closure_patch = ASH-TCU-K6ZT
base_runtime_replay_patch = ASH-TCU-K6ZU
base_native_parity_patch = ASH-TCU-K6ZV
```

K6ZW must not mutate candidate shape, dtype, route, layout, or tile mode.

## Apply Candidate Descriptor

K6ZW must create a descriptor for the explicit apply queue candidate:

```txt
apply_candidate_id = ash_tcu_k6zw_logical16_native_wgpu_candidate_v1
apply_candidate_kind = logical16_native_wgpu_tensorcube_candidate
candidate_route = ash_tcu_k6p_row_major_emit_candidate_v1
candidate_source_patch = ASH-TCU-K6ZV
candidate_evidence_status = PASS_ASH_TCU_K6ZV_LOGICAL16_NATIVE_WGPU_STRICT_PARITY_NO_CPU_RUNTIME_SELECTION_NO_APPLY_QUEUE_NO_PRODUCTION_REPLACEMENT_SEAL
candidate_apply_scope = candidate_only
operator_gate_required = true
operator_approval_granted = false
apply_execution_allowed = false
```

## Apply Queue Semantics

K6ZW may set:

```txt
apply_queue_candidate_created = true
apply_queue_entry_created = true
apply_queue_ready = true
apply_queue_state = pending_operator_review
operator_gate_required = true
operator_approval_granted = false
```

K6ZW must not set:

```txt
apply_execution_started = true
apply_execution_completed = true
runtime_splice_opened = true
production_replacement_executed = true
default_adoption_executed = true
user_visible_adoption_executed = true
```

## Operator Gate Semantics

K6ZW must create an explicit operator gate:

```txt
operator_gate_id = ash_tcu_k6zw_operator_gate_v1
operator_gate_required = true
operator_gate_state = pending
operator_approval_granted = false
operator_approval_source = none
operator_approval_timestamp = null
operator_approval_signature_present = false
```

K6ZW must not infer operator approval from prior pass status, K6ZV parity pass, apply queue entry creation, absence of failures, or default flag value.

## Rollback Binding

K6ZW must bind rollback information before creating the queue entry.

```txt
rollback_plan_bound = true
rollback_target_route = current_default_route
rollback_scope = tensorcube_candidate_route_only
rollback_execution_required_before_apply = false
rollback_rehearsal_required_next = true
rollback_executed = false
```

K6ZW does not execute rollback. K6ZW only binds rollback metadata to the apply queue candidate.

## Explicit Non-Scope

K6ZW does not enable:

```txt
operator approval grant
apply execution
runtime splice
production route replacement
default route adoption
user-visible output adoption
performance claim
base_train route binding
weight atlas construction
GPU streaming
loss/backward
optimizer
weight commit
safetensors mutation
checkpoint finalization
```

## Guard Requirements

### Prior K6ZV Native Parity Guard

K6ZW must verify:

```txt
required_prior_patch = ASH-TCU-K6ZV
required_prior_pass = true
k6zv_logical16_native_wgpu_strict_parity_passed = true
k6zv_native_wgpu_dispatch_evidence_valid = true
k6zv_cpu_reference_used_for_runtime_selection = false
k6zv_apply_queue_ready = false
k6zv_production_replacement_executed = false
k6zv_global_default_route_changed = false
```

### Apply Queue Entry Guard

K6ZW must verify:

```txt
apply_queue_candidate_created = true
apply_queue_entry_created = true
apply_queue_ready = true
apply_queue_state = pending_operator_review
apply_execution_started = false
apply_execution_completed = false
selected_next_patch_executed = false
```

### Operator Gate Guard

K6ZW must verify:

```txt
operator_gate_required = true
operator_gate_state = pending
operator_approval_granted = false
operator_approval_signature_present = false
operator_approval_source = none
```

### Apply Queue Non-Execution Guard

K6ZW must verify:

```txt
apply_execution_allowed = false
apply_execution_started = false
apply_execution_completed = false
runtime_splice_opened = false
candidate_output_commit_executed = false
shadow_output_commit_executed = false
```

### No Default Adoption Guard

K6ZW must verify:

```txt
default_adoption_allowed = false
default_adoption_executed = false
global_default_route_changed = false
default_route_registry_mutated = false
```

### No Production Replacement Guard

K6ZW must verify:

```txt
production_replacement_allowed = false
production_replacement_executed = false
production_route_state_changed = false
broad_rollout_state_changed = false
runtime_splice_opened = false
```

### No User-Visible Adoption Guard

K6ZW must verify:

```txt
user_visible_adoption_allowed = false
user_visible_adoption_executed = false
assistant_message_output_changed = false
runtime_decode_output_changed = false
```

### No Performance Claim Guard

K6ZW must verify:

```txt
performance_claim_allowed = false
benchmark_claim_promoted = false
apply_queue_entry_promoted_to_performance_claim = false
```

K6ZW may say the candidate is queued for operator review. K6ZW must not claim production performance superiority.

## Implementation Files

```txt
crates/burn_webgpu_backend/src/tensorcube_k6zw_prior_k6zv_native_parity_receipt.rs
crates/burn_webgpu_backend/src/tensorcube_k6zw_apply_candidate_descriptor.rs
crates/burn_webgpu_backend/src/tensorcube_k6zw_operator_gate.rs
crates/burn_webgpu_backend/src/tensorcube_k6zw_apply_queue_entry.rs
crates/burn_webgpu_backend/src/tensorcube_k6zw_apply_queue_non_execution_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k6zw_no_default_adoption_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k6zw_no_production_replacement_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k6zw_no_user_visible_adoption_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k6zw_rollback_binding_packet.rs
crates/burn_webgpu_backend/src/tensorcube_k6zw_verdict.rs
crates/burn_webgpu_backend/src/tensorcube_k6zw_contract_audit.rs
crates/orchestrator_local/src/ash_tcu_k6zw_apply_queue_entry_operator_gate_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k6zw_apply_queue_entry_operator_gate_audit.rs
```

## Test Files

```txt
crates/burn_webgpu_backend/tests/ash_tcu_k6zw_prior_k6zv_native_parity_receipt.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zw_apply_candidate_descriptor.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zw_operator_gate.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zw_apply_queue_entry.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zw_apply_queue_non_execution_guard.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zw_no_default_adoption_guard.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zw_no_production_replacement_guard.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zw_no_user_visible_adoption_guard.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zw_rollback_binding_packet.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zw_verdict.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zw_contract_audit.rs
```

## Rust Module Export Requirements

### burn_webgpu_backend lib exports

```rust
pub mod tensorcube_k6zw_prior_k6zv_native_parity_receipt;
pub mod tensorcube_k6zw_apply_candidate_descriptor;
pub mod tensorcube_k6zw_operator_gate;
pub mod tensorcube_k6zw_apply_queue_entry;
pub mod tensorcube_k6zw_apply_queue_non_execution_guard;
pub mod tensorcube_k6zw_no_default_adoption_guard;
pub mod tensorcube_k6zw_no_production_replacement_guard;
pub mod tensorcube_k6zw_no_user_visible_adoption_guard;
pub mod tensorcube_k6zw_rollback_binding_packet;
pub mod tensorcube_k6zw_verdict;
pub mod tensorcube_k6zw_contract_audit;
```

### orchestrator_local lib exports

```rust
pub mod ash_tcu_k6zw_apply_queue_entry_operator_gate_report;
```

## CLI

### Binary

```txt
ash_tcu_k6zw_apply_queue_entry_operator_gate_audit
```

### Command

```powershell
cargo run --manifest-path ./crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_tcu_k6zw_apply_queue_entry_operator_gate_audit -- --repo-root <repo> --require-k6zv-pass --require-native-wgpu-parity --create-apply-queue-entry --require-operator-gate --operator-approval-granted false --bind-rollback-plan --no-apply-execution --no-default-adoption --no-production-replacement --no-user-visible-adoption
```

### Optional report input

```powershell
cargo run --manifest-path ./crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_tcu_k6zw_apply_queue_entry_operator_gate_audit -- --repo-root <repo> --k6zv-report-json <k6zv-report-json-or-log> --require-k6zv-pass --require-native-wgpu-parity --create-apply-queue-entry --require-operator-gate --operator-approval-granted false --bind-rollback-plan --no-apply-execution --no-default-adoption --no-production-replacement --no-user-visible-adoption
```

## Required Output JSON Shape

```json
{
  "patch_id": "ASH-TCU-K6ZW",
  "status": "PASS_ASH_TCU_K6ZW_APPLY_QUEUE_ENTRY_OPERATOR_GATE_NO_DEFAULT_ADOPTION_NO_PRODUCTION_REPLACEMENT_SEAL",
  "prior_k6zv_native_parity_receipt": {
    "pass": true,
    "k6zv_required": true,
    "k6zv_valid": true,
    "k6zv_status": "PASS_ASH_TCU_K6ZV_LOGICAL16_NATIVE_WGPU_STRICT_PARITY_NO_CPU_RUNTIME_SELECTION_NO_APPLY_QUEUE_NO_PRODUCTION_REPLACEMENT_SEAL",
    "k6zv_logical16_native_wgpu_strict_parity_passed": true,
    "k6zv_native_wgpu_dispatch_evidence_valid": true,
    "k6zv_cpu_reference_used_for_runtime_selection": false,
    "k6zv_apply_queue_ready": false,
    "k6zv_production_replacement_executed": false
  },
  "apply_candidate_descriptor": {
    "pass": true,
    "apply_candidate_id": "ash_tcu_k6zw_logical16_native_wgpu_candidate_v1",
    "apply_candidate_kind": "logical16_native_wgpu_tensorcube_candidate",
    "candidate_route": "ash_tcu_k6p_row_major_emit_candidate_v1",
    "candidate_source_patch": "ASH-TCU-K6ZV",
    "operator_gate_required": true,
    "operator_approval_granted": false,
    "apply_execution_allowed": false
  },
  "operator_gate": {
    "pass": true,
    "operator_gate_required": true,
    "operator_gate_state": "pending",
    "operator_approval_granted": false,
    "operator_approval_signature_present": false,
    "operator_approval_source": "none"
  },
  "apply_queue_entry": {
    "pass": true,
    "apply_queue_candidate_created": true,
    "apply_queue_entry_created": true,
    "apply_queue_ready": true,
    "apply_queue_state": "pending_operator_review",
    "apply_execution_started": false,
    "apply_execution_completed": false
  },
  "verdict": {
    "pass": true,
    "verdict": "apply_queue_entry_created_pending_operator_review_no_default_adoption",
    "recommended_next_patch": "ASH-TCU-K6ZX_ROLLBACK_REHEARSAL_AND_APPLY_DRYRUN_NO_DEFAULT_ADOPTION"
  }
}
```

## PASS Markers

```txt
PASS_ASH_TCU_K6ZW_PRIOR_K6ZV_NATIVE_PARITY_RECEIPT
PASS_ASH_TCU_K6ZW_APPLY_CANDIDATE_DESCRIPTOR
PASS_ASH_TCU_K6ZW_OPERATOR_GATE
PASS_ASH_TCU_K6ZW_APPLY_QUEUE_ENTRY
PASS_ASH_TCU_K6ZW_APPLY_QUEUE_NON_EXECUTION_GUARD
PASS_ASH_TCU_K6ZW_NO_DEFAULT_ADOPTION
PASS_ASH_TCU_K6ZW_NO_PRODUCTION_REPLACEMENT
PASS_ASH_TCU_K6ZW_NO_USER_VISIBLE_ADOPTION
PASS_ASH_TCU_K6ZW_ROLLBACK_BINDING_PACKET
PASS_ASH_TCU_K6ZW_APPLY_QUEUE_ENTRY_OPERATOR_GATE_NO_DEFAULT_ADOPTION_NO_PRODUCTION_REPLACEMENT_SEAL
```

## FAIL Markers

```txt
FAIL_ASH_TCU_K6ZW_MISSING_K6ZV_PRIOR_VERDICT
FAIL_ASH_TCU_K6ZW_K6ZV_REQUIRED_STATUS_NOT_MET
FAIL_ASH_TCU_K6ZW_K6ZV_NATIVE_PARITY_NOT_PASSED
FAIL_ASH_TCU_K6ZW_K6ZV_NATIVE_DISPATCH_EVIDENCE_INVALID
FAIL_ASH_TCU_K6ZW_K6ZV_CPU_RUNTIME_SELECTION_USED
FAIL_ASH_TCU_K6ZW_APPLY_CANDIDATE_DESCRIPTOR_INVALID
FAIL_ASH_TCU_K6ZW_OPERATOR_GATE_MISSING
FAIL_ASH_TCU_K6ZW_OPERATOR_APPROVAL_ALREADY_GRANTED
FAIL_ASH_TCU_K6ZW_APPLY_QUEUE_ENTRY_NOT_CREATED
FAIL_ASH_TCU_K6ZW_APPLY_QUEUE_NOT_READY
FAIL_ASH_TCU_K6ZW_APPLY_EXECUTION_STARTED
FAIL_ASH_TCU_K6ZW_APPLY_EXECUTION_COMPLETED
FAIL_ASH_TCU_K6ZW_RUNTIME_SPLICE_OPENED
FAIL_ASH_TCU_K6ZW_DEFAULT_ADOPTION_EXECUTED
FAIL_ASH_TCU_K6ZW_DEFAULT_ROUTE_CHANGED
FAIL_ASH_TCU_K6ZW_PRODUCTION_REPLACEMENT_EXECUTED
FAIL_ASH_TCU_K6ZW_USER_VISIBLE_ADOPTION_OPENED
FAIL_ASH_TCU_K6ZW_ROLLBACK_PLAN_NOT_BOUND
FAIL_ASH_TCU_K6ZW_PERFORMANCE_CLAIM_ALLOWED
```

## Static Checks

```txt
required_prior_patch = ASH-TCU-K6ZV
required_prior_pass = true
k6zv_native_wgpu_dispatch_evidence_valid = true
k6zv_logical16_native_wgpu_strict_parity_passed = true
apply_queue_candidate_created = true
apply_queue_entry_created = true
apply_queue_ready = true
apply_queue_state = pending_operator_review
operator_gate_required = true
operator_approval_granted = false
apply_execution_started = false
apply_execution_completed = false
runtime_splice_opened = false
default_adoption_executed = false
production_replacement_executed = false
user_visible_adoption_executed = false
rollback_plan_bound = true
```

## Acceptance Criteria

```txt
1. K6ZV prior verdict exists.
2. K6ZV prior verdict status matches required PASS marker.
3. K6ZV native WGPU strict parity passed.
4. K6ZV native dispatch evidence is valid.
5. K6ZV did not use CPU reference for runtime selection.
6. K6ZW creates an apply candidate descriptor.
7. K6ZW creates an explicit apply queue entry.
8. K6ZW marks apply_queue_ready as true.
9. K6ZW sets apply queue state to pending_operator_review.
10. K6ZW creates an operator gate.
11. K6ZW does not grant operator approval.
12. K6ZW does not start apply execution.
13. K6ZW does not complete apply execution.
14. K6ZW does not open runtime splice.
15. K6ZW does not change default route.
16. K6ZW does not execute production replacement.
17. K6ZW does not open user-visible adoption.
18. K6ZW binds rollback plan metadata.
19. K6ZW does not execute rollback.
20. K6ZW does not allow performance claim.
21. K6ZW recommends K6ZX as the next patch.
```

## Non-Mutation Seal

K6ZW must not write, mutate, or finalize:

```txt
model weights
optimizer state
safetensors checkpoint
runtime decode output
assistant message output
default route registry
production route registry
runtime splice state
base_train state
```

K6ZW may write:

```txt
apply queue candidate receipt
operator gate receipt
rollback binding receipt
```

## Recommended Next Patch

```txt
ASH-TCU-K6ZX
Rollback Rehearsal And Apply Dryrun /
Apply Queue Candidate To Non-Committing Runtime Splice Rehearsal
No Default Adoption No Production Replacement Seal
```

## Final Seal

```txt
ASH-TCU-K6ZW does not make TensorCube production-ready.

ASH-TCU-K6ZW only converts K6ZV from:
logical16_native_wgpu_strict_parity_pass_no_cpu_runtime_selection_no_apply_queue

into:
apply_queue_entry_created_pending_operator_review_no_default_adoption

without executing apply, opening runtime splice, replacing production route, changing default route, user-visible adoption, base_train, training, optimizer, or weight mutation.
```
