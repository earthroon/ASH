# ASH-TCU-K7J SPEC

## Title

User-Visible Activation Execution / Consume Single-Use User-Visible Activation Token / Default Route Opens To User-Visible Layer / No Production Replacement No Weight Mutation Seal

## Patch ID

```txt
ASH-TCU-K7J
```

## Status Target

```txt
PASS_ASH_TCU_K7J_USER_VISIBLE_ACTIVATION_EXECUTION_CONSUME_TOKEN_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Parent Patch

```txt
ASH-TCU-K7I
```

## Required Prior Status

```txt
PASS_ASH_TCU_K7I_USER_VISIBLE_ACTIVATION_TOKEN_NO_EXECUTION_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Required Prior Verdict

```txt
user_visible_activation_token_created_no_execution
```

## Purpose

`ASH-TCU-K7J` uses the K7I user-visible activation token as the required parent state.

K7I created a single-use user-visible activation token, bound it to the adopted default route, proved the token was unconsumed, and kept user-visible execution closed.

K7J is the first patch allowed to consume that single-use activation token and execute user-visible activation.

K7J may mutate the user-visible route registry.

K7J may bind the user-visible layer to the adopted default route.

K7J may mark user-visible activation as completed.

K7J may open the default route to the user-visible layer.

K7J must consume the activation token exactly once.

K7J must not mutate the default route registry.

K7J must not replace production.

K7J must not mutate model weights.

K7J must not run training, loss/backward, optimizer step, safetensors mutation, or checkpoint finalization.

K7J must not claim production performance improvement.

K7J must not execute rollback.

## Current K7I Baseline

K7I established:

```txt
user_visible_activation_token_created = true
user_visible_activation_token_granted = true
user_visible_activation_token_scope = user_visible_default_route_activation_only
user_visible_activation_token_single_use = true
user_visible_activation_token_consumed = false
user_visible_activation_token_bound_to_default_route = true
user_visible_activation_token_bound_route = ash_tcu_k6p_row_major_emit_candidate_v1
activation_token_consumed_before = false
activation_token_consumed_after = false
activation_token_reuse_allowed = false
activation_token_replay_detected = false
user_visible_execution_allowed_next = true
user_visible_execution_started = false
user_visible_activation_started = false
user_visible_activation_completed = false
user_visible_output_emitted = false
user_visible_route_mutated = false
assistant_message_output_changed = false
runtime_decode_output_changed = false
production_replacement_executed = false
production_route_registry_mutated = false
default_route_registry_mutated_by_k7i = false
current_default_route_points_to_candidate = true
current_default_route = ash_tcu_k6p_row_major_emit_candidate_v1
model_weights_mutated = false
optimizer_state_mutated = false
safetensors_checkpoint_mutated = false
performance_claim_allowed = false
rollback_pointer_integrity_passed = true
rollback_execution_started = false
recommended_next_patch = ASH-TCU-K7J_USER_VISIBLE_ACTIVATION_EXECUTION_CONSUME_TOKEN_NO_PRODUCTION_REPLACEMENT
```

K7J must treat this as the required parent condition.

## SSOT

### SSOT Owner

```txt
workspace/runtime/tensorcube/ash_tensorcube_k7j_user_visible_activation_execution_latest.json
```

### Secondary Receipts

```txt
workspace/runtime/tensorcube/ash_tensorcube_k7j_prior_k7i_activation_token_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7j_pre_activation_user_visible_route_snapshot_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7j_user_visible_activation_execution_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7j_single_use_activation_token_consumption_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7j_user_visible_route_registry_diff_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7j_post_activation_user_visible_route_integrity_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7j_activation_output_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7j_no_production_replacement_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7j_no_default_route_mutation_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7j_no_weight_mutation_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7j_no_performance_claim_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7j_rollback_pointer_still_available_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7j_static_checks_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7j_verdict_latest.json
artifacts/ASH_TCU_K7J_LOCAL_MANIFEST.json
```

## State Ownership

K7J owns prior K7I activation token receipt validation, pre-activation user-visible route snapshot, user-visible activation execution, single-use activation token consumption, user-visible route registry diff, post-activation user-visible route integrity, activation output guard, no-production-replacement guard, no-default-route-mutation guard, no-weight-mutation guard, no-performance-claim guard, and rollback pointer still available guard.

K7J does not own production route replacement, default route registry mutation, second default adoption, base_train route binding, weight atlas construction, GPU streaming promotion, training, loss/backward, optimizer, weight commit, safetensors mutation, checkpoint finalization, rollback execution, or production performance claim.

## Source Inputs

K7J must read and validate the latest K7I receipts:

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
workspace/runtime/tensorcube/ash_tensorcube_k7i_verdict_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7i_static_checks_latest.json
artifacts/ASH_TCU_K7I_LOCAL_MANIFEST.json
```

K7J may read K6ZZ, K7A, K7B, K7C, K7D, K7E, K7F, K7G, and K7H receipts as historical evidence only. K7J must not recompute default adoption, K7G health, K7H decode readiness, recreate K7I activation token, or execute rollback.

## Adopted Default Route Lineage

K7J must preserve:

```txt
candidate_route_namespace_id = ash_tcu_k6zz_candidate_route_namespace_v1
internal_canary_namespace_id = ash_tcu_k7a_internal_canary_namespace_v1
candidate_readiness_candidate_id = ash_tcu_k6zw_logical16_native_wgpu_candidate_v1
current_default_route = ash_tcu_k6p_row_major_emit_candidate_v1
current_default_route_points_to_candidate = true
default_adoption_executed = true
post_default_adoption_health_passed = true
user_visible_readiness_state = ready_for_user_visible_operator_review
user_visible_activation_token_bound_route = ash_tcu_k6p_row_major_emit_candidate_v1
```

K7J must not mutate candidate route, dtype, layout, tile mode, default route pointer, model weights, or evidence status.

## Prior K7I Activation Token Receipt

K7J must verify:

```txt
k7i_required = true
k7i_valid = true
k7i_status = PASS_ASH_TCU_K7I_USER_VISIBLE_ACTIVATION_TOKEN_NO_EXECUTION_NO_PRODUCTION_REPLACEMENT_SEAL
k7i_user_visible_activation_token_created = true
k7i_user_visible_activation_token_granted = true
k7i_user_visible_activation_token_scope = user_visible_default_route_activation_only
k7i_user_visible_activation_token_single_use = true
k7i_user_visible_activation_token_consumed = false
k7i_user_visible_activation_token_bound_to_default_route = true
k7i_user_visible_activation_token_bound_route = ash_tcu_k6p_row_major_emit_candidate_v1
k7i_user_visible_execution_allowed_next = true
k7i_user_visible_execution_started = false
k7i_user_visible_output_emitted = false
k7i_user_visible_route_mutated = false
k7i_assistant_message_output_changed = false
k7i_runtime_decode_output_changed = false
k7i_production_replacement_executed = false
k7i_default_route_registry_mutated_by_k7i = false
k7i_model_weights_mutated = false
k7i_rollback_pointer_integrity_passed = true
```

K7J must fail if token is missing, not granted, already consumed, reusable, replayed, scoped too broadly, or not bound to the current default route.

## Pre-Activation User-Visible Route Snapshot

K7J must create a pre-activation snapshot:

```txt
pre_activation_user_visible_route_snapshot_created = true
pre_activation_user_visible_route_snapshot_scope = user_visible_route_registry_only
pre_activation_user_visible_route_snapshot_hash_present = true
pre_activation_user_visible_route_snapshot_restore_pointer_created = true
pre_activation_user_visible_route_snapshot_contains_weights = false
pre_activation_user_visible_route_snapshot_contains_raw_output = false
pre_activation_user_visible_route_snapshot_contains_assistant_message = false
```

This snapshot is for rollback evidence only. It must not contain model weights, raw decode output, or assistant message output.

## User-Visible Activation Execution

K7J must execute user-visible activation:

```txt
user_visible_activation_execution_started = true
user_visible_activation_execution_completed = true
user_visible_activation_execution_scope = user_visible_route_registry_only
user_visible_activation_used_single_use_token = true
user_visible_activation_token_bound_to_default_route = true
user_visible_activation_default_route = ash_tcu_k6p_row_major_emit_candidate_v1
user_visible_activation_candidate_id = ash_tcu_k6zw_logical16_native_wgpu_candidate_v1
user_visible_route_mutated = true
candidate_route_promoted_to_user_visible = true
user_visible_layer_opened = true
user_visible_output_layer_points_to_default_route = true
user_visible_output_emitted = true
assistant_message_output_changed = true
runtime_decode_output_changed = true
production_replacement_executed = false
production_route_registry_mutated = false
default_route_registry_mutated_by_k7j = false
global_default_route_changed_by_k7j = false
```

K7J may open the user-visible output layer because this is the activation execution patch. K7J must not mutate production or default route.

## Single-Use Activation Token Consumption

K7J must consume the activation token exactly once:

```txt
single_use_activation_token_consumption_created = true
activation_token_consumed_before = false
activation_token_consumed_after = true
activation_token_consumption_count = 1
activation_token_single_use = true
activation_token_reuse_allowed = false
activation_token_replay_detected = false
activation_token_scope = user_visible_default_route_activation_only
activation_token_consumed_by_patch = ASH-TCU-K7J
activation_token_bound_to_default_route = true
```

K7J must fail if token was already consumed, remains unconsumed after execution, is consumed more than once, scope is too broad, reuse is allowed, replay is detected, or token is not bound to the default route.

## User-Visible Route Registry Diff

K7J must write a route registry diff:

```txt
user_visible_route_registry_diff_created = true
user_visible_route_registry_diff_scope = user_visible_route_registry_only
user_visible_route_registry_diff_expected_mutation = true
user_visible_route_registry_diff_only_user_visible_route_changed = true
user_visible_route_registry_diff_default_changed = false
user_visible_route_registry_diff_production_changed = false
user_visible_route_registry_diff_weight_changed = false
user_visible_route_registry_diff_contains_raw_output = false
user_visible_route_registry_diff_contains_assistant_message = false
```

The only allowed route mutation is the user-visible route pointer opening to the current default route.

## Post-Activation User-Visible Route Integrity

K7J must verify:

```txt
post_activation_user_visible_route_integrity_started = true
post_activation_user_visible_route_integrity_completed = true
post_activation_user_visible_route_integrity_passed = true
post_activation_user_visible_route_points_to_default = true
post_activation_user_visible_route_points_to_candidate = true
post_activation_user_visible_default_route = ash_tcu_k6p_row_major_emit_candidate_v1
post_activation_user_visible_candidate_id = ash_tcu_k6zw_logical16_native_wgpu_candidate_v1
post_activation_default_route_unchanged = true
post_activation_production_route_unchanged = true
```

## Activation Output Guard

K7J must mark activation output as opened but bounded:

```txt
activation_output_guard_created = true
user_visible_output_emitted = true
assistant_message_output_changed = true
runtime_decode_output_changed = true
activation_output_scope = user_visible_activation_smoke_only
activation_output_contains_raw_training_data = false
activation_output_contains_weight_dump = false
activation_output_contains_unbounded_probe_output = false
activation_output_promoted_to_production = false
activation_output_promoted_to_performance_claim = false
```

K7J may produce a bounded user-visible smoke output marker. K7J must not include raw training data, weight dump, or unbounded diagnostic output in receipts.

## Guards

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
default_route_registry_mutated_by_k7j = false
global_default_route_changed_by_k7j = false
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
user_visible_activation_promoted_to_performance_claim = false
activation_output_promoted_to_performance_claim = false
```

### Rollback Pointer Still Available Guard

```txt
rollback_pointer_still_available_guard_created = true
rollback_pointer_integrity_passed = true
previous_default_route_restore_pointer_created = true
previous_default_route_restore_scope = default_route_registry_only
previous_user_visible_route_restore_pointer_created = true
previous_user_visible_route_restore_scope = user_visible_route_registry_only
rollback_execution_started = false
rollback_execution_completed = false
rollback_pointer_contains_weights = false
rollback_pointer_contains_raw_output = false
```

K7J must not execute rollback.

## Implementation Files

```txt
crates/burn_webgpu_backend/src/tensorcube_k7j_prior_k7i_activation_token_receipt.rs
crates/burn_webgpu_backend/src/tensorcube_k7j_pre_activation_user_visible_route_snapshot.rs
crates/burn_webgpu_backend/src/tensorcube_k7j_user_visible_activation_execution.rs
crates/burn_webgpu_backend/src/tensorcube_k7j_single_use_activation_token_consumption.rs
crates/burn_webgpu_backend/src/tensorcube_k7j_user_visible_route_registry_diff.rs
crates/burn_webgpu_backend/src/tensorcube_k7j_post_activation_user_visible_route_integrity.rs
crates/burn_webgpu_backend/src/tensorcube_k7j_activation_output_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7j_no_production_replacement_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7j_no_default_route_mutation_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7j_no_weight_mutation_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7j_no_performance_claim_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7j_rollback_pointer_still_available_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7j_verdict.rs
crates/burn_webgpu_backend/src/tensorcube_k7j_contract_audit.rs
crates/orchestrator_local/src/ash_tcu_k7j_user_visible_activation_execution_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7j_user_visible_activation_execution_audit.rs
```

## CLI

```powershell
cargo run --manifest-path ./crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_tcu_k7j_user_visible_activation_execution_audit -- --repo-root <repo> --require-k7i-pass --require-user-visible-activation-token --snapshot-pre-activation-user-visible-route --consume-user-visible-activation-token --execute-user-visible-activation --write-user-visible-route-registry-diff --verify-post-activation-user-visible-route --enforce-activation-output-guard --no-production-replacement --no-default-route-mutation --no-weight-mutation --no-performance-claim --verify-rollback-pointer
```

## PASS Markers

```txt
PASS_ASH_TCU_K7J_PRIOR_K7I_ACTIVATION_TOKEN_RECEIPT
PASS_ASH_TCU_K7J_PRE_ACTIVATION_USER_VISIBLE_ROUTE_SNAPSHOT
PASS_ASH_TCU_K7J_USER_VISIBLE_ACTIVATION_EXECUTION
PASS_ASH_TCU_K7J_SINGLE_USE_ACTIVATION_TOKEN_CONSUMPTION
PASS_ASH_TCU_K7J_USER_VISIBLE_ROUTE_REGISTRY_DIFF
PASS_ASH_TCU_K7J_POST_ACTIVATION_USER_VISIBLE_ROUTE_INTEGRITY
PASS_ASH_TCU_K7J_ACTIVATION_OUTPUT_GUARD
PASS_ASH_TCU_K7J_NO_PRODUCTION_REPLACEMENT
PASS_ASH_TCU_K7J_NO_DEFAULT_ROUTE_MUTATION
PASS_ASH_TCU_K7J_NO_WEIGHT_MUTATION
PASS_ASH_TCU_K7J_NO_PERFORMANCE_CLAIM
PASS_ASH_TCU_K7J_ROLLBACK_POINTER_STILL_AVAILABLE
PASS_ASH_TCU_K7J_USER_VISIBLE_ACTIVATION_EXECUTION_CONSUME_TOKEN_NO_PRODUCTION_REPLACEMENT_SEAL
```

## FAIL Markers

```txt
FAIL_ASH_TCU_K7J_MISSING_K7I_PRIOR_VERDICT
FAIL_ASH_TCU_K7J_K7I_REQUIRED_STATUS_NOT_MET
FAIL_ASH_TCU_K7J_USER_VISIBLE_ACTIVATION_TOKEN_MISSING
FAIL_ASH_TCU_K7J_USER_VISIBLE_ACTIVATION_TOKEN_NOT_GRANTED
FAIL_ASH_TCU_K7J_TOKEN_ALREADY_CONSUMED
FAIL_ASH_TCU_K7J_TOKEN_NOT_SINGLE_USE
FAIL_ASH_TCU_K7J_TOKEN_SCOPE_TOO_BROAD
FAIL_ASH_TCU_K7J_TOKEN_NOT_BOUND_TO_DEFAULT_ROUTE
FAIL_ASH_TCU_K7J_PRE_ACTIVATION_USER_VISIBLE_ROUTE_SNAPSHOT_MISSING
FAIL_ASH_TCU_K7J_USER_VISIBLE_ACTIVATION_NOT_STARTED
FAIL_ASH_TCU_K7J_USER_VISIBLE_ACTIVATION_NOT_COMPLETED
FAIL_ASH_TCU_K7J_USER_VISIBLE_ACTIVATION_DID_NOT_USE_TOKEN
FAIL_ASH_TCU_K7J_TOKEN_NOT_CONSUMED_AFTER_EXECUTION
FAIL_ASH_TCU_K7J_TOKEN_CONSUMED_MORE_THAN_ONCE
FAIL_ASH_TCU_K7J_USER_VISIBLE_ROUTE_NOT_MUTATED
FAIL_ASH_TCU_K7J_CANDIDATE_ROUTE_NOT_PROMOTED_TO_USER_VISIBLE
FAIL_ASH_TCU_K7J_USER_VISIBLE_LAYER_NOT_OPENED
FAIL_ASH_TCU_K7J_USER_VISIBLE_OUTPUT_NOT_EMITTED
FAIL_ASH_TCU_K7J_USER_VISIBLE_ROUTE_REGISTRY_DIFF_MISSING
FAIL_ASH_TCU_K7J_USER_VISIBLE_ROUTE_DIFF_CONTAINS_UNEXPECTED_MUTATION
FAIL_ASH_TCU_K7J_POST_ACTIVATION_USER_VISIBLE_ROUTE_INTEGRITY_FAILED
FAIL_ASH_TCU_K7J_PRODUCTION_REPLACEMENT_EXECUTED
FAIL_ASH_TCU_K7J_PRODUCTION_ROUTE_MUTATED
FAIL_ASH_TCU_K7J_DEFAULT_ROUTE_MUTATED
FAIL_ASH_TCU_K7J_WEIGHT_MUTATION_DETECTED
FAIL_ASH_TCU_K7J_PERFORMANCE_CLAIM_ALLOWED
FAIL_ASH_TCU_K7J_ROLLBACK_EXECUTION_STARTED
```

## Recommended Next Patch

```txt
ASH-TCU-K7K
User-Visible Post Activation Health Guard /
Bounded User-Visible Smoke Verification /
Rollback-Ready No Production Replacement Seal
```

## Final Seal

```txt
ASH-TCU-K7J executes user-visible activation.

ASH-TCU-K7J converts K7I from:
user_visible_activation_token_created_no_execution

into:
user_visible_activation_execution_completed_default_route_opened

without replacing production route, changing default route again, mutating weights, executing rollback, binding base_train, training, optimizer, safetensors mutation, checkpoint mutation, or performance claim.
```
