# ASH-TCU-K7I SPEC

## Title

User-Visible Activation Token / Single-Use Operator Approval For User-Visible Default Route Execution / No Execution Yet / No Production Replacement No Weight Mutation Seal

## Patch ID

```txt
ASH-TCU-K7I
```

## Status Target

```txt
PASS_ASH_TCU_K7I_USER_VISIBLE_ACTIVATION_TOKEN_NO_EXECUTION_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Parent Patch

```txt
ASH-TCU-K7H
```

## Required Prior Status

```txt
PASS_ASH_TCU_K7H_DEFAULT_ROUTE_USER_VISIBLE_READINESS_GATE_NO_USER_VISIBLE_EXECUTION_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Required Prior Verdict

```txt
default_route_user_visible_readiness_gate_passed_no_execution
```

## Purpose

`ASH-TCU-K7I` uses the K7H user-visible readiness gate result as the required parent state.

K7H proved that the adopted default route passed quarantined decode readiness, decode output remained quarantined, no decode output leaked into assistant output or runtime decode output, user-visible readiness packet was created, and user-visible activation token was not created yet.

K7I is the first patch allowed to create a single-use operator approval token for later user-visible activation.

K7I does not execute user-visible activation.

K7I does not emit user-visible output.

K7I does not mutate assistant message output.

K7I does not mutate runtime decode output.

K7I does not replace production.

K7I does not mutate model weights.

K7I does not run training, loss/backward, optimizer step, safetensors mutation, or checkpoint finalization.

K7I only converts the K7H readiness packet into an armed user-visible activation-token state for the next patch.

## Current K7H Baseline

K7H established:

```txt
quarantined_decode_readiness_execution_completed = true
quarantined_decode_readiness_total_case_count = 128
quarantined_decode_readiness_fail_count = 0
quarantined_decode_readiness_abort_required = false
quarantined_decode_readiness_default_route_used = true
quarantined_decode_readiness_default_route_points_to_candidate = true
decode_output_quarantine_enabled = true
decode_output_committed_to_assistant = false
decode_output_committed_to_runtime_decode = false
decode_output_promoted_to_user_visible = false
decode_output_contains_raw_text = false
decode_output_contains_sample_text = false
decode_output_leak_detected = false
assistant_message_output_changed = false
runtime_decode_output_changed = false
user_visible_output_emitted = false
user_visible_readiness_packet_created = true
user_visible_readiness_state = ready_for_user_visible_operator_review
user_visible_readiness_requires_activation_token_next = true
user_visible_readiness_activation_token_created = false
user_visible_readiness_activation_granted = false
user_visible_readiness_execution_allowed_now = false
user_visible_readiness_output_exposed = false
user_visible_activation_token_created = false
user_visible_activation_started = false
user_visible_activation_completed = false
production_replacement_executed = false
production_route_registry_mutated = false
model_weights_mutated = false
optimizer_state_mutated = false
safetensors_checkpoint_mutated = false
performance_claim_allowed = false
rollback_pointer_integrity_passed = true
rollback_execution_started = false
recommended_next_patch = ASH-TCU-K7I_USER_VISIBLE_ACTIVATION_TOKEN_NO_PRODUCTION_REPLACEMENT
```

K7I must treat this as the required parent condition.

## SSOT

### SSOT Owner

```txt
workspace/runtime/tensorcube/ash_tensorcube_k7i_user_visible_activation_token_latest.json
```

### Secondary Receipts

```txt
workspace/runtime/tensorcube/ash_tensorcube_k7i_prior_k7h_readiness_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7i_operator_identity_packet_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7i_user_visible_activation_scope_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7i_user_visible_activation_token_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7i_single_use_activation_token_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7i_no_user_visible_execution_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7i_no_assistant_output_mutation_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7i_no_runtime_decode_mutation_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7i_no_production_replacement_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7i_no_default_route_mutation_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7i_no_weight_mutation_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7i_no_performance_claim_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7i_rollback_pointer_still_available_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7i_static_checks_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7i_verdict_latest.json
artifacts/ASH_TCU_K7I_LOCAL_MANIFEST.json
```

## State Ownership

K7I owns prior K7H readiness receipt validation, operator identity packet, user-visible activation scope, user-visible activation token, single-use activation token guard, no-user-visible-execution guard, no-assistant-output-mutation guard, no-runtime-decode-mutation guard, no-production-replacement guard, no-default-route-mutation guard, no-weight-mutation guard, no-performance-claim guard, and rollback pointer still available guard.

K7I does not own user-visible activation execution, assistant message output mutation, runtime decode output mutation, production route replacement, default route registry mutation, second default adoption, base_train route binding, weight atlas construction, GPU streaming promotion, training, loss/backward, optimizer, weight commit, safetensors mutation, checkpoint finalization, rollback execution, or production performance claim.

## Source Inputs

K7I must read and validate the latest K7H receipts:

```txt
workspace/runtime/tensorcube/ash_tensorcube_k7h_prior_k7g_health_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7h_default_route_decode_readiness_plan_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7h_quarantined_decode_readiness_execution_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7h_decode_output_quarantine_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7h_decode_leak_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7h_decode_readiness_digest_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7h_user_visible_readiness_packet_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7h_no_user_visible_activation_token_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7h_no_user_visible_execution_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7h_no_production_replacement_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7h_no_weight_mutation_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7h_no_performance_claim_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7h_rollback_pointer_still_available_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7h_verdict_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7h_static_checks_latest.json
artifacts/ASH_TCU_K7H_LOCAL_MANIFEST.json
```

K7I may read K6ZZ, K7A, K7B, K7C, K7D, K7E, K7F, and K7G receipts as historical evidence only. K7I must not recompute default adoption, K7G health, K7H decode readiness, or rollback.

## Adopted Default Route Lineage

K7I must preserve:

```txt
candidate_route_namespace_id = ash_tcu_k6zz_candidate_route_namespace_v1
internal_canary_namespace_id = ash_tcu_k7a_internal_canary_namespace_v1
candidate_readiness_candidate_id = ash_tcu_k6zw_logical16_native_wgpu_candidate_v1
current_default_route = ash_tcu_k6p_row_major_emit_candidate_v1
current_default_route_points_to_candidate = true
default_adoption_executed = true
post_default_adoption_health_passed = true
user_visible_readiness_state = ready_for_user_visible_operator_review
rollback_pointer_integrity_passed = true
```

K7I must not mutate candidate route, dtype, layout, tile mode, default route pointer, runtime decode output, assistant output, or evidence status.

## Prior K7H Readiness Receipt

K7I must verify:

```txt
k7h_required = true
k7h_valid = true
k7h_status = PASS_ASH_TCU_K7H_DEFAULT_ROUTE_USER_VISIBLE_READINESS_GATE_NO_USER_VISIBLE_EXECUTION_NO_PRODUCTION_REPLACEMENT_SEAL
k7h_quarantined_decode_readiness_execution_completed = true
k7h_quarantined_decode_readiness_total_case_count = 128
k7h_quarantined_decode_readiness_fail_count = 0
k7h_quarantined_decode_readiness_abort_required = false
k7h_decode_output_quarantine_enabled = true
k7h_decode_output_leak_detected = false
k7h_assistant_message_output_changed = false
k7h_runtime_decode_output_changed = false
k7h_user_visible_output_emitted = false
k7h_user_visible_readiness_packet_created = true
k7h_user_visible_readiness_state = ready_for_user_visible_operator_review
k7h_user_visible_readiness_requires_activation_token_next = true
k7h_user_visible_activation_token_created = false
k7h_user_visible_activation_started = false
k7h_user_visible_activation_completed = false
k7h_production_replacement_executed = false
k7h_model_weights_mutated = false
k7h_performance_claim_allowed = false
k7h_rollback_pointer_integrity_passed = true
k7h_rollback_execution_started = false
```

K7I must fail if K7H did not pass decode readiness, if output leaked, if readiness packet is missing, if activation token was already created, or if rollback pointer is unavailable.

## Operator Identity Packet

K7I must create an explicit operator identity packet:

```txt
operator_identity_packet_created = true
operator_identity_scope = user_visible_activation_review
operator_identity_verified = true
operator_identity_signature_present = true
operator_identity_replay_protected = true
operator_identity_user_visible = false
```

## User-Visible Activation Scope

K7I must create a user-visible activation scope receipt:

```txt
user_visible_activation_scope_created = true
user_visible_activation_scope = user_visible_default_route_activation_only
user_visible_activation_candidate_id = ash_tcu_k6zw_logical16_native_wgpu_candidate_v1
user_visible_activation_default_route = ash_tcu_k6p_row_major_emit_candidate_v1
user_visible_activation_requires_default_route = true
user_visible_activation_requires_readiness_packet = true
user_visible_activation_requires_quarantined_decode_pass = true
user_visible_activation_production_replacement_allowed = false
user_visible_activation_default_route_mutation_allowed = false
user_visible_activation_weight_mutation_allowed = false
user_visible_activation_runtime_decode_mutation_allowed = false
user_visible_activation_assistant_output_mutation_allowed_now = false
```

## User-Visible Activation Token

K7I must create a single-use activation token:

```txt
user_visible_activation_token_created = true
user_visible_activation_token_granted = true
user_visible_activation_token_source = explicit_operator_review
user_visible_activation_token_scope = user_visible_default_route_activation_only
user_visible_activation_token_single_use = true
user_visible_activation_token_consumed = false
user_visible_activation_token_reuse_allowed = false
user_visible_activation_token_replay_protected = true
user_visible_activation_token_signature_present = true
user_visible_activation_token_bound_to_default_route = true
user_visible_activation_token_bound_route = ash_tcu_k6p_row_major_emit_candidate_v1
```

This token permits only the next patch to attempt user-visible activation. It does not execute activation, emit output, replace production, mutate runtime decode output, mutate assistant output, or mutate weights.

## Guards

### Single-Use Activation Token Guard

```txt
single_use_activation_token_guard_created = true
activation_token_single_use = true
activation_token_consumed_before = false
activation_token_consumed_after = false
activation_token_reuse_allowed = false
activation_token_replay_detected = false
activation_token_scope = user_visible_default_route_activation_only
activation_token_bound_to_default_route = true
```

### No User-Visible Execution Guard

```txt
no_user_visible_execution_guard_created = true
user_visible_execution_allowed_next = true
user_visible_execution_started = false
user_visible_execution_completed = false
user_visible_activation_started = false
user_visible_activation_completed = false
user_visible_adoption_executed = false
user_visible_output_emitted = false
candidate_route_promoted_to_user_visible = false
user_visible_route_mutated = false
```

### No Assistant Output Mutation Guard

```txt
assistant_output_mutation_guard_created = true
assistant_message_output_changed = false
assistant_message_output_emitted = false
assistant_message_output_contains_decode_probe = false
assistant_message_output_contains_raw_activation_sample = false
```

### No Runtime Decode Mutation Guard

```txt
runtime_decode_mutation_guard_created = true
runtime_decode_output_changed = false
runtime_decode_output_committed = false
runtime_decode_output_contains_probe = false
runtime_decode_output_contains_activation_sample = false
```

### No Production Replacement Guard

```txt
production_replacement_allowed = false
production_replacement_executed = false
candidate_route_promoted_to_production = false
production_route_registry_mutated = false
production_route_state_changed = false
```

### No Default Route Mutation Guard

```txt
default_route_mutation_guard_created = true
default_route_registry_mutated_by_k7i = false
global_default_route_changed_by_k7i = false
current_default_route_points_to_candidate = true
current_default_route = ash_tcu_k6p_row_major_emit_candidate_v1
```

### No Weight Mutation Guard

```txt
model_weights_mutated = false
optimizer_state_mutated = false
safetensors_checkpoint_mutated = false
weight_commit_executed = false
checkpoint_finalized = false
```

### No Performance Claim Guard

```txt
performance_claim_allowed = false
benchmark_claim_promoted = false
user_visible_activation_token_promoted_to_performance_claim = false
operator_token_promoted_to_performance_claim = false
```

### Rollback Pointer Still Available Guard

```txt
rollback_pointer_still_available_guard_created = true
rollback_pointer_integrity_passed = true
previous_default_route_restore_pointer_created = true
previous_default_route_restore_scope = default_route_registry_only
rollback_execution_started = false
rollback_execution_completed = false
rollback_pointer_contains_weights = false
rollback_pointer_contains_raw_output = false
```

## Implementation Files

```txt
crates/burn_webgpu_backend/src/tensorcube_k7i_prior_k7h_readiness_receipt.rs
crates/burn_webgpu_backend/src/tensorcube_k7i_operator_identity_packet.rs
crates/burn_webgpu_backend/src/tensorcube_k7i_user_visible_activation_scope.rs
crates/burn_webgpu_backend/src/tensorcube_k7i_user_visible_activation_token.rs
crates/burn_webgpu_backend/src/tensorcube_k7i_single_use_activation_token_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7i_no_user_visible_execution_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7i_no_assistant_output_mutation_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7i_no_runtime_decode_mutation_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7i_no_production_replacement_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7i_no_default_route_mutation_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7i_no_weight_mutation_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7i_no_performance_claim_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7i_rollback_pointer_still_available_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7i_verdict.rs
crates/burn_webgpu_backend/src/tensorcube_k7i_contract_audit.rs
crates/orchestrator_local/src/ash_tcu_k7i_user_visible_activation_token_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7i_user_visible_activation_token_audit.rs
```

## CLI

```powershell
cargo run --manifest-path ./crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_tcu_k7i_user_visible_activation_token_audit -- --repo-root <repo> --require-k7h-pass --require-user-visible-readiness --create-operator-identity-packet --create-user-visible-activation-scope --create-user-visible-activation-token --enforce-single-use-activation-token --no-user-visible-execution --no-assistant-output-mutation --no-runtime-decode-mutation --no-production-replacement --no-default-route-mutation --no-weight-mutation --no-performance-claim --verify-rollback-pointer
```

## PASS Markers

```txt
PASS_ASH_TCU_K7I_PRIOR_K7H_READINESS_RECEIPT
PASS_ASH_TCU_K7I_OPERATOR_IDENTITY_PACKET
PASS_ASH_TCU_K7I_USER_VISIBLE_ACTIVATION_SCOPE
PASS_ASH_TCU_K7I_USER_VISIBLE_ACTIVATION_TOKEN
PASS_ASH_TCU_K7I_SINGLE_USE_ACTIVATION_TOKEN_GUARD
PASS_ASH_TCU_K7I_NO_USER_VISIBLE_EXECUTION
PASS_ASH_TCU_K7I_NO_ASSISTANT_OUTPUT_MUTATION
PASS_ASH_TCU_K7I_NO_RUNTIME_DECODE_MUTATION
PASS_ASH_TCU_K7I_NO_PRODUCTION_REPLACEMENT
PASS_ASH_TCU_K7I_NO_DEFAULT_ROUTE_MUTATION
PASS_ASH_TCU_K7I_NO_WEIGHT_MUTATION
PASS_ASH_TCU_K7I_NO_PERFORMANCE_CLAIM
PASS_ASH_TCU_K7I_ROLLBACK_POINTER_STILL_AVAILABLE
PASS_ASH_TCU_K7I_USER_VISIBLE_ACTIVATION_TOKEN_NO_EXECUTION_NO_PRODUCTION_REPLACEMENT_SEAL
```

## FAIL Markers

```txt
FAIL_ASH_TCU_K7I_MISSING_K7H_PRIOR_VERDICT
FAIL_ASH_TCU_K7I_K7H_REQUIRED_STATUS_NOT_MET
FAIL_ASH_TCU_K7I_USER_VISIBLE_READINESS_NOT_READY
FAIL_ASH_TCU_K7I_K7H_DECODE_READINESS_NOT_PASSED
FAIL_ASH_TCU_K7I_K7H_DECODE_OUTPUT_LEAKED
FAIL_ASH_TCU_K7I_K7H_USER_VISIBLE_TOKEN_ALREADY_CREATED
FAIL_ASH_TCU_K7I_ROLLBACK_POINTER_MISSING
FAIL_ASH_TCU_K7I_OPERATOR_IDENTITY_PACKET_MISSING
FAIL_ASH_TCU_K7I_OPERATOR_IDENTITY_NOT_VERIFIED
FAIL_ASH_TCU_K7I_USER_VISIBLE_ACTIVATION_SCOPE_MISSING
FAIL_ASH_TCU_K7I_USER_VISIBLE_ACTIVATION_TOKEN_NOT_CREATED
FAIL_ASH_TCU_K7I_USER_VISIBLE_ACTIVATION_TOKEN_NOT_GRANTED
FAIL_ASH_TCU_K7I_TOKEN_NOT_SINGLE_USE
FAIL_ASH_TCU_K7I_TOKEN_ALREADY_CONSUMED
FAIL_ASH_TCU_K7I_TOKEN_SCOPE_TOO_BROAD
FAIL_ASH_TCU_K7I_TOKEN_NOT_BOUND_TO_DEFAULT_ROUTE
FAIL_ASH_TCU_K7I_USER_VISIBLE_EXECUTION_STARTED
FAIL_ASH_TCU_K7I_USER_VISIBLE_OUTPUT_EMITTED
FAIL_ASH_TCU_K7I_USER_VISIBLE_ROUTE_MUTATED
FAIL_ASH_TCU_K7I_ASSISTANT_OUTPUT_CHANGED
FAIL_ASH_TCU_K7I_RUNTIME_DECODE_OUTPUT_CHANGED
FAIL_ASH_TCU_K7I_PRODUCTION_REPLACEMENT_EXECUTED
FAIL_ASH_TCU_K7I_PRODUCTION_ROUTE_MUTATED
FAIL_ASH_TCU_K7I_DEFAULT_ROUTE_MUTATED
FAIL_ASH_TCU_K7I_WEIGHT_MUTATION_DETECTED
FAIL_ASH_TCU_K7I_PERFORMANCE_CLAIM_ALLOWED
FAIL_ASH_TCU_K7I_ROLLBACK_EXECUTION_STARTED
```

## Recommended Next Patch

```txt
ASH-TCU-K7J
User-Visible Activation Execution /
Consume Single-Use User-Visible Activation Token /
Default Route Output Opens To User-Visible Layer /
No Production Replacement No Weight Mutation Seal
```

## Final Seal

```txt
ASH-TCU-K7I does not expose user-visible output.

ASH-TCU-K7I only converts K7H from:
default_route_user_visible_readiness_gate_passed_no_execution

into:
user_visible_activation_token_created_no_execution

without executing user-visible output, mutating assistant output, mutating runtime decode output, replacing production route, changing default route again, executing rollback, binding base_train, training, optimizer, or weight mutation.
```
