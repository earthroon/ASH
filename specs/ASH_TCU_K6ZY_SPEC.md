# ASH-TCU-K6ZY SPEC

## Title

Operator Approval Token And Gated Apply Candidate / Pending Queue To Explicit Approval Receipt / Apply Permission Armed But Not Executed / No Default Adoption No Production Replacement Seal

## Patch ID

```txt
ASH-TCU-K6ZY
```

## Status Target

```txt
PASS_ASH_TCU_K6ZY_OPERATOR_APPROVAL_TOKEN_AND_GATED_APPLY_CANDIDATE_NO_DEFAULT_ADOPTION_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Parent Patch

```txt
ASH-TCU-K6ZX
```

## Required Prior Status

```txt
PASS_ASH_TCU_K6ZX_ROLLBACK_REHEARSAL_AND_APPLY_DRYRUN_NO_DEFAULT_ADOPTION_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Required Prior Verdict

```txt
rollback_rehearsal_and_apply_dryrun_passed_no_default_adoption
```

## Purpose

`ASH-TCU-K6ZY` uses the K6ZX rollback rehearsal and apply dryrun evidence as the required parent state and creates an explicit operator approval token for the K6ZW apply queue candidate.

K6ZX proved that the queued candidate can enter a rehearsal namespace, perform non-committing splice rehearsal, perform shadow route swap, restore through rollback rehearsal, and pass post-rollback restore checks without persistent route mutation.

K6ZY is the first patch in this chain allowed to set:

```txt
operator_approval_granted = true
```

K6ZY may arm the gated apply candidate.

K6ZY must not execute apply, open persistent runtime splice, change default route, replace production route, or expose user-visible output.

K6ZY must not bind base_train, weight atlas, GPU streaming, loss/backward, optimizer, weight commit, safetensors mutation, or checkpoint finalization.

## Current K6ZX Baseline

K6ZX established:

```txt
apply_dryrun_started = true
apply_dryrun_completed = true
apply_dryrun_passed = true
rollback_rehearsal_completed = true
post_rollback_restore_check_passed = true
dryrun_namespace_created = true
dryrun_namespace_isolated = true
non_committing_runtime_splice_rehearsal_completed = true
shadow_route_swap_rehearsal_completed = true
operator_approval_granted = false
apply_execution_started = false
apply_execution_completed = false
persistent_runtime_splice_opened = false
default_route_registry_mutated = false
production_route_registry_mutated = false
user_visible_route_mutated = false
recommended_next_patch = ASH-TCU-K6ZY_OPERATOR_APPROVAL_TOKEN_AND_GATED_APPLY_CANDIDATE_NO_DEFAULT_ADOPTION
```

K6ZY must treat this as the required parent condition.

## SSOT

### SSOT Owner

```txt
workspace/runtime/tensorcube/ash_tensorcube_k6zy_operator_approval_token_latest.json
```

### Secondary Receipts

```txt
workspace/runtime/tensorcube/ash_tensorcube_k6zy_prior_k6zx_dryrun_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zy_operator_identity_packet_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zy_operator_approval_token_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zy_approval_scope_binding_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zy_gated_apply_candidate_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zy_apply_permission_armed_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zy_apply_execution_not_started_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zy_no_default_adoption_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zy_no_production_replacement_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zy_no_user_visible_adoption_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zy_no_persistent_route_mutation_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zy_verdict_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zy_static_checks_latest.json
artifacts/ASH_TCU_K6ZY_LOCAL_MANIFEST.json
```

## State Ownership

### K6ZY owns

```txt
prior_k6zx_dryrun_receipt
operator_identity_packet
operator_approval_token
approval_scope_binding
gated_apply_candidate
apply_permission_armed_guard
apply_execution_not_started_guard
no_default_adoption_guard
no_production_replacement_guard
no_user_visible_adoption_guard
no_persistent_route_mutation_guard
```

### K6ZY does not own

```txt
real apply execution
persistent runtime splice
default route adoption
production route replacement
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

K6ZY must read and validate the latest K6ZX receipts:

```txt
workspace/runtime/tensorcube/ash_tensorcube_k6zx_prior_k6zw_apply_queue_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zx_dryrun_rehearsal_namespace_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zx_shadow_route_snapshot_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zx_non_committing_runtime_splice_rehearsal_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zx_shadow_route_swap_rehearsal_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zx_rollback_rehearsal_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zx_post_rollback_restore_check_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zx_operator_gate_still_pending_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zx_no_default_adoption_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zx_no_production_replacement_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zx_no_user_visible_adoption_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zx_no_persistent_route_mutation_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zx_verdict_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zx_static_checks_latest.json
artifacts/ASH_TCU_K6ZX_LOCAL_MANIFEST.json
```

K6ZY may read K6ZW apply queue receipts as queue source metadata.

K6ZY must not recompute K6ZX dryrun or rollback evidence.

K6ZY must not treat successful K6ZX dryrun as automatic approval.

## Candidate Route

K6ZY must preserve the K6ZW apply candidate descriptor:

```txt
apply_candidate_id = ash_tcu_k6zw_logical16_native_wgpu_candidate_v1
apply_candidate_kind = logical16_native_wgpu_tensorcube_candidate
candidate_route = ash_tcu_k6p_row_major_emit_candidate_v1
candidate_source_patch = ASH-TCU-K6ZV
candidate_apply_scope = candidate_only
base_apply_queue_patch = ASH-TCU-K6ZW
base_dryrun_patch = ASH-TCU-K6ZX
```

K6ZY must not mutate candidate route, dtype, layout, tile mode, or evidence status.

## Operator Identity Packet

K6ZY must create an operator identity packet:

```txt
operator_identity_packet_created = true
operator_identity_source = explicit_cli
operator_identity_present = true
operator_identity_hash_present = true
operator_identity_signature_present = true
operator_identity_timestamp_present = true
operator_identity_replay_protected = true
```

K6ZY must reject anonymous approval, implicit approval, and approval inferred from prior PASS markers.

## Operator Approval Token

K6ZY may create an approval token only when an explicit approval flag and identity packet are present.

Required token fields:

```txt
operator_approval_token_created = true
operator_approval_granted = true
operator_approval_source = explicit_cli
operator_approval_signature_present = true
operator_approval_timestamp_present = true
operator_approval_replay_protected = true
operator_approval_scope = gated_apply_candidate_only
operator_approval_token_consumed = false
operator_approval_token_single_use = true
```

K6ZY must not create a reusable operator approval token, global approval token, or production approval.

## Approval Scope Binding

K6ZY must bind the approval token to one exact candidate:

```txt
approval_scope_binding_created = true
approval_scope_patch = ASH-TCU-K6ZY
approval_scope_candidate_id = ash_tcu_k6zw_logical16_native_wgpu_candidate_v1
approval_scope_candidate_route = ash_tcu_k6p_row_major_emit_candidate_v1
approval_scope_parent_dryrun_patch = ASH-TCU-K6ZX
approval_scope_default_adoption_allowed = false
approval_scope_production_replacement_allowed = false
approval_scope_user_visible_adoption_allowed = false
```

The approval token must not authorize default route mutation, production route replacement, user-visible adoption, weight mutation, base_train binding, optimizer state mutation, safetensors mutation, or checkpoint finalization.

## Gated Apply Candidate

K6ZY may arm the apply candidate:

```txt
gated_apply_candidate_created = true
gated_apply_candidate_armed = true
apply_permission_armed = true
apply_permission_state = armed_pending_execution
apply_execution_allowed_next = true
apply_execution_started = false
apply_execution_completed = false
apply_permission_consumed = false
```

This is a next-patch permission, not current-patch execution.

K6ZY must not execute the armed candidate.

## Apply Permission Semantics

K6ZY may set:

```txt
apply_permission_armed = true
apply_permission_state = armed_pending_execution
operator_approval_granted = true
```

K6ZY must not set:

```txt
apply_execution_started = true
apply_execution_completed = true
runtime_splice_opened = true
persistent_runtime_splice_opened = true
default_adoption_executed = true
production_replacement_executed = true
user_visible_adoption_executed = true
```

## Explicit Non-Scope

K6ZY does not enable:

```txt
real apply execution
persistent runtime splice
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

### Prior K6ZX Dryrun Guard

K6ZY must verify:

```txt
required_prior_patch = ASH-TCU-K6ZX
required_prior_pass = true
k6zx_apply_dryrun_passed = true
k6zx_rollback_rehearsal_completed = true
k6zx_post_rollback_restore_check_passed = true
k6zx_operator_approval_granted = false
k6zx_apply_execution_started = false
k6zx_persistent_runtime_splice_opened = false
k6zx_default_route_registry_mutated = false
k6zx_production_route_registry_mutated = false
k6zx_user_visible_route_mutated = false
```

### Explicit Operator Approval Guard

K6ZY must verify:

```txt
operator_identity_packet_created = true
operator_identity_present = true
operator_identity_signature_present = true
operator_approval_token_created = true
operator_approval_granted = true
operator_approval_source = explicit_cli
operator_approval_signature_present = true
operator_approval_replay_protected = true
operator_approval_token_single_use = true
```

### Approval Scope Guard

K6ZY must verify:

```txt
approval_scope_binding_created = true
approval_scope_candidate_id = ash_tcu_k6zw_logical16_native_wgpu_candidate_v1
approval_scope_candidate_route = ash_tcu_k6p_row_major_emit_candidate_v1
approval_scope_default_adoption_allowed = false
approval_scope_production_replacement_allowed = false
approval_scope_user_visible_adoption_allowed = false
```

### Apply Permission Armed Guard

K6ZY must verify:

```txt
gated_apply_candidate_created = true
gated_apply_candidate_armed = true
apply_permission_armed = true
apply_permission_state = armed_pending_execution
apply_execution_allowed_next = true
apply_execution_started = false
apply_execution_completed = false
apply_permission_consumed = false
```

### Apply Execution Not Started Guard

K6ZY must verify:

```txt
apply_execution_started = false
apply_execution_completed = false
runtime_splice_opened = false
persistent_runtime_splice_opened = false
candidate_output_commit_executed = false
```

### No Persistent Route Mutation Guard

K6ZY must verify:

```txt
default_route_registry_mutated = false
production_route_registry_mutated = false
user_visible_route_mutated = false
base_train_route_registry_mutated = false
runtime_decode_output_changed = false
assistant_message_output_changed = false
```

### No Default Adoption Guard

K6ZY must verify:

```txt
default_adoption_allowed = false
default_adoption_executed = false
global_default_route_changed = false
default_route_registry_mutated = false
```

### No Production Replacement Guard

K6ZY must verify:

```txt
production_replacement_allowed = false
production_replacement_executed = false
production_route_state_changed = false
production_route_registry_mutated = false
persistent_runtime_splice_opened = false
```

### No User-Visible Adoption Guard

K6ZY must verify:

```txt
user_visible_adoption_allowed = false
user_visible_adoption_executed = false
assistant_message_output_changed = false
runtime_decode_output_changed = false
```

### No Performance Claim Guard

K6ZY must verify:

```txt
performance_claim_allowed = false
benchmark_claim_promoted = false
approval_token_promoted_to_performance_claim = false
```

K6ZY may say approval token is created and gated apply candidate is armed. K6ZY must not claim production performance superiority.

## Implementation Files

```txt
crates/burn_webgpu_backend/src/tensorcube_k6zy_prior_k6zx_dryrun_receipt.rs
crates/burn_webgpu_backend/src/tensorcube_k6zy_operator_identity_packet.rs
crates/burn_webgpu_backend/src/tensorcube_k6zy_operator_approval_token.rs
crates/burn_webgpu_backend/src/tensorcube_k6zy_approval_scope_binding.rs
crates/burn_webgpu_backend/src/tensorcube_k6zy_gated_apply_candidate.rs
crates/burn_webgpu_backend/src/tensorcube_k6zy_apply_permission_armed_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k6zy_apply_execution_not_started_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k6zy_no_default_adoption_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k6zy_no_production_replacement_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k6zy_no_user_visible_adoption_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k6zy_no_persistent_route_mutation_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k6zy_verdict.rs
crates/burn_webgpu_backend/src/tensorcube_k6zy_contract_audit.rs
crates/orchestrator_local/src/ash_tcu_k6zy_operator_approval_token_gated_apply_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k6zy_operator_approval_token_gated_apply_audit.rs
```

## Test Files

```txt
crates/burn_webgpu_backend/tests/ash_tcu_k6zy_prior_k6zx_dryrun_receipt.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zy_operator_identity_packet.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zy_operator_approval_token.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zy_approval_scope_binding.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zy_gated_apply_candidate.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zy_apply_permission_armed_guard.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zy_apply_execution_not_started_guard.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zy_no_default_adoption_guard.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zy_no_production_replacement_guard.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zy_no_user_visible_adoption_guard.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zy_no_persistent_route_mutation_guard.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zy_verdict.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zy_contract_audit.rs
```

## CLI

### Binary

```txt
ash_tcu_k6zy_operator_approval_token_gated_apply_audit
```

### Command

```powershell
cargo run --manifest-path ./crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_tcu_k6zy_operator_approval_token_gated_apply_audit -- --repo-root <repo> --require-k6zx-pass --require-apply-dryrun-passed --require-rollback-rehearsal-passed --create-operator-identity-packet --grant-operator-approval-token --operator-approval-source explicit_cli --bind-approval-scope --arm-gated-apply-candidate --allow-apply-execution-next --no-apply-execution-now --no-default-adoption --no-production-replacement --no-user-visible-adoption --no-persistent-route-mutation
```

## Required Output JSON Shape

```json
{
  "patch_id": "ASH-TCU-K6ZY",
  "status": "PASS_ASH_TCU_K6ZY_OPERATOR_APPROVAL_TOKEN_AND_GATED_APPLY_CANDIDATE_NO_DEFAULT_ADOPTION_NO_PRODUCTION_REPLACEMENT_SEAL",
  "operator_approval_token": {
    "operator_approval_token_created": true,
    "operator_approval_granted": true,
    "operator_approval_source": "explicit_cli",
    "operator_approval_signature_present": true,
    "operator_approval_replay_protected": true,
    "operator_approval_token_single_use": true,
    "operator_approval_token_consumed": false
  },
  "gated_apply_candidate": {
    "gated_apply_candidate_created": true,
    "gated_apply_candidate_armed": true,
    "apply_permission_armed": true,
    "apply_permission_state": "armed_pending_execution",
    "apply_execution_allowed_next": true,
    "apply_execution_started": false,
    "apply_execution_completed": false
  },
  "verdict": {
    "pass": true,
    "verdict": "operator_approval_token_created_gated_apply_candidate_armed_no_default_adoption",
    "recommended_next_patch": "ASH-TCU-K6ZZ_GATED_APPLY_EXECUTION_CANDIDATE_ROUTE_ONLY_NO_DEFAULT_ADOPTION"
  }
}
```

## PASS Markers

```txt
PASS_ASH_TCU_K6ZY_PRIOR_K6ZX_DRYRUN_RECEIPT
PASS_ASH_TCU_K6ZY_OPERATOR_IDENTITY_PACKET
PASS_ASH_TCU_K6ZY_OPERATOR_APPROVAL_TOKEN
PASS_ASH_TCU_K6ZY_APPROVAL_SCOPE_BINDING
PASS_ASH_TCU_K6ZY_GATED_APPLY_CANDIDATE
PASS_ASH_TCU_K6ZY_APPLY_PERMISSION_ARMED
PASS_ASH_TCU_K6ZY_APPLY_EXECUTION_NOT_STARTED
PASS_ASH_TCU_K6ZY_NO_DEFAULT_ADOPTION
PASS_ASH_TCU_K6ZY_NO_PRODUCTION_REPLACEMENT
PASS_ASH_TCU_K6ZY_NO_USER_VISIBLE_ADOPTION
PASS_ASH_TCU_K6ZY_NO_PERSISTENT_ROUTE_MUTATION
PASS_ASH_TCU_K6ZY_OPERATOR_APPROVAL_TOKEN_AND_GATED_APPLY_CANDIDATE_NO_DEFAULT_ADOPTION_NO_PRODUCTION_REPLACEMENT_SEAL
```

## FAIL Markers

```txt
FAIL_ASH_TCU_K6ZY_MISSING_K6ZX_PRIOR_VERDICT
FAIL_ASH_TCU_K6ZY_K6ZX_REQUIRED_STATUS_NOT_MET
FAIL_ASH_TCU_K6ZY_K6ZX_APPLY_DRYRUN_NOT_PASSED
FAIL_ASH_TCU_K6ZY_K6ZX_ROLLBACK_REHEARSAL_NOT_COMPLETED
FAIL_ASH_TCU_K6ZY_K6ZX_RESTORE_CHECK_NOT_PASSED
FAIL_ASH_TCU_K6ZY_OPERATOR_IDENTITY_MISSING
FAIL_ASH_TCU_K6ZY_OPERATOR_SIGNATURE_MISSING
FAIL_ASH_TCU_K6ZY_OPERATOR_APPROVAL_TOKEN_NOT_CREATED
FAIL_ASH_TCU_K6ZY_OPERATOR_APPROVAL_NOT_GRANTED
FAIL_ASH_TCU_K6ZY_OPERATOR_APPROVAL_NOT_REPLAY_PROTECTED
FAIL_ASH_TCU_K6ZY_OPERATOR_APPROVAL_NOT_SINGLE_USE
FAIL_ASH_TCU_K6ZY_APPROVAL_SCOPE_NOT_BOUND
FAIL_ASH_TCU_K6ZY_APPROVAL_SCOPE_ESCALATED_TO_DEFAULT
FAIL_ASH_TCU_K6ZY_APPROVAL_SCOPE_ESCALATED_TO_PRODUCTION
FAIL_ASH_TCU_K6ZY_APPROVAL_SCOPE_ESCALATED_TO_USER_VISIBLE
FAIL_ASH_TCU_K6ZY_GATED_APPLY_CANDIDATE_NOT_ARMED
FAIL_ASH_TCU_K6ZY_APPLY_EXECUTION_STARTED
FAIL_ASH_TCU_K6ZY_APPLY_EXECUTION_COMPLETED
FAIL_ASH_TCU_K6ZY_RUNTIME_SPLICE_OPENED
FAIL_ASH_TCU_K6ZY_PERSISTENT_ROUTE_MUTATED
FAIL_ASH_TCU_K6ZY_DEFAULT_ADOPTION_EXECUTED
FAIL_ASH_TCU_K6ZY_PRODUCTION_REPLACEMENT_EXECUTED
FAIL_ASH_TCU_K6ZY_USER_VISIBLE_ADOPTION_OPENED
FAIL_ASH_TCU_K6ZY_PERFORMANCE_CLAIM_ALLOWED
```

## Recommended Next Patch

```txt
ASH-TCU-K6ZZ
Gated Apply Execution / Candidate Route Only /
Single-Use Approval Token Consumption /
No Default Adoption No Production Replacement Seal
```

## Final Seal

```txt
ASH-TCU-K6ZY does not make TensorCube production-ready.

ASH-TCU-K6ZY only converts K6ZX from:
rollback_rehearsal_and_apply_dryrun_passed_no_default_adoption

into:
operator_approval_token_created_gated_apply_candidate_armed_no_default_adoption

without executing apply now, opening persistent runtime splice, changing default route, replacing production route, user-visible adoption, base_train, training, optimizer, or weight mutation.
```
