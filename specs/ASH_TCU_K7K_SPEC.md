# ASH-TCU-K7K SPEC

## Title

User-Visible Post Activation Health Guard / Bounded User-Visible Smoke Verification / Output Scope Clamp / Rollback-Ready No Production Replacement Seal

## Patch ID

```txt
ASH-TCU-K7K
```

## Status Target

```txt
PASS_ASH_TCU_K7K_USER_VISIBLE_POST_ACTIVATION_HEALTH_GUARD_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Parent Patch

```txt
ASH-TCU-K7J
```

## Required Prior Status

```txt
PASS_ASH_TCU_K7J_USER_VISIBLE_ACTIVATION_EXECUTION_CONSUME_TOKEN_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Required Prior Verdict

```txt
user_visible_activation_execution_completed_default_route_opened
```

## Purpose

`ASH-TCU-K7K` uses the K7J user-visible activation execution result as the required parent state.

K7J consumed the single-use user-visible activation token, opened the user-visible layer, mutated only the user-visible route registry, emitted bounded activation output, and proved production/default/weights/performance/rollback execution stayed sealed.

K7K verifies the health of the newly opened user-visible route.

K7K may run bounded user-visible smoke verification.

K7K may verify that the user-visible route still points to the adopted default route and candidate.

K7K may verify that user-visible output remains bounded and does not contain raw diagnostic, training, weight, internal receipt JSON, debug trace, or unbounded probe content.

K7K may verify rollback readiness for both default route and user-visible route.

K7K must not create a new activation token.

K7K must not execute a second user-visible activation.

K7K must not mutate the user-visible route registry again.

K7K must not mutate the default route registry.

K7K must not replace production.

K7K must not mutate model weights.

K7K must not run training, loss/backward, optimizer step, safetensors mutation, or checkpoint finalization.

K7K must not claim production performance improvement.

K7K must not execute rollback.

## Current K7J Baseline

K7J established:

```txt
user_visible_activation_execution_started = true
user_visible_activation_execution_completed = true
user_visible_activation_used_single_use_token = true
activation_token_consumed_before = false
activation_token_consumed_after = true
activation_token_consumption_count = 1
activation_token_scope = user_visible_default_route_activation_only
user_visible_route_mutated = true
candidate_route_promoted_to_user_visible = true
user_visible_layer_opened = true
user_visible_output_layer_points_to_default_route = true
user_visible_output_emitted = true
assistant_message_output_changed = true
runtime_decode_output_changed = true
user_visible_route_registry_diff_only_user_visible_route_changed = true
post_activation_user_visible_route_integrity_passed = true
post_activation_user_visible_route_points_to_default = true
post_activation_user_visible_route_points_to_candidate = true
activation_output_scope = user_visible_activation_smoke_only
activation_output_contains_raw_training_data = false
activation_output_contains_weight_dump = false
activation_output_contains_unbounded_probe_output = false
activation_output_promoted_to_production = false
activation_output_promoted_to_performance_claim = false
production_replacement_executed = false
production_route_registry_mutated = false
default_route_registry_mutated_by_k7j = false
global_default_route_changed_by_k7j = false
model_weights_mutated = false
optimizer_state_mutated = false
safetensors_checkpoint_mutated = false
performance_claim_allowed = false
rollback_pointer_integrity_passed = true
previous_default_route_restore_pointer_created = true
previous_user_visible_route_restore_pointer_created = true
rollback_execution_started = false
recommended_next_patch = ASH-TCU-K7K_USER_VISIBLE_POST_ACTIVATION_HEALTH_GUARD_NO_PRODUCTION_REPLACEMENT
```

K7K must treat this as the required parent condition.

## SSOT

### SSOT Owner

```txt
workspace/runtime/tensorcube/ash_tensorcube_k7k_user_visible_post_activation_health_latest.json
```

### Secondary Receipts

```txt
workspace/runtime/tensorcube/ash_tensorcube_k7k_prior_k7j_activation_execution_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7k_user_visible_route_pointer_integrity_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7k_bounded_user_visible_smoke_plan_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7k_bounded_user_visible_smoke_execution_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7k_user_visible_output_scope_clamp_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7k_user_visible_smoke_digest_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7k_post_activation_abort_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7k_no_second_user_visible_activation_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7k_no_activation_token_recreation_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7k_no_user_visible_route_remutation_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7k_no_default_route_mutation_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7k_no_production_replacement_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7k_no_weight_mutation_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7k_no_performance_claim_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7k_rollback_pointer_still_available_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7k_static_checks_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7k_verdict_latest.json
artifacts/ASH_TCU_K7K_LOCAL_MANIFEST.json
```

## State Ownership

K7K owns prior K7J activation execution receipt validation, user-visible route pointer integrity, bounded user-visible smoke plan and execution, user-visible output scope clamp, user-visible smoke digest, post-activation abort guard, no-second-user-visible-activation guard, no-activation-token-recreation guard, no-user-visible-route-remutation guard, no-default-route-mutation guard, no-production-replacement guard, no-weight-mutation guard, no-performance-claim guard, and rollback pointer still available guard.

K7K does not own second user-visible activation execution, new user-visible activation token creation, production replacement, default route registry mutation, user-visible route registry mutation, base_train route binding, weight atlas construction, GPU streaming promotion, training, loss/backward, optimizer, weight commit, safetensors mutation, checkpoint finalization, rollback execution, or production performance claim.

## Source Inputs

K7K must read and validate the latest K7J receipts:

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
workspace/runtime/tensorcube/ash_tensorcube_k7j_verdict_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7j_static_checks_latest.json
artifacts/ASH_TCU_K7J_LOCAL_MANIFEST.json
```

K7K may read K6ZZ, K7A, K7B, K7C, K7D, K7E, K7F, K7G, K7H, and K7I receipts as historical evidence only. K7K must not recompute default adoption, K7G health, K7H decode readiness, recreate K7I token, re-execute K7J activation, or execute rollback.

## Prior K7J Activation Execution Receipt

K7K must verify:

```txt
k7j_required = true
k7j_valid = true
k7j_status = PASS_ASH_TCU_K7J_USER_VISIBLE_ACTIVATION_EXECUTION_CONSUME_TOKEN_NO_PRODUCTION_REPLACEMENT_SEAL
k7j_user_visible_activation_execution_completed = true
k7j_user_visible_activation_used_single_use_token = true
k7j_activation_token_consumed_after = true
k7j_activation_token_consumption_count = 1
k7j_user_visible_route_mutated = true
k7j_candidate_route_promoted_to_user_visible = true
k7j_user_visible_layer_opened = true
k7j_user_visible_output_emitted = true
k7j_assistant_message_output_changed = true
k7j_runtime_decode_output_changed = true
k7j_user_visible_route_registry_diff_only_user_visible_route_changed = true
k7j_post_activation_user_visible_route_integrity_passed = true
k7j_activation_output_scope = user_visible_activation_smoke_only
k7j_activation_output_contains_raw_training_data = false
k7j_activation_output_contains_weight_dump = false
k7j_activation_output_contains_unbounded_probe_output = false
k7j_activation_output_promoted_to_production = false
k7j_production_replacement_executed = false
k7j_default_route_registry_mutated_by_k7j = false
k7j_model_weights_mutated = false
k7j_performance_claim_allowed = false
k7j_rollback_pointer_integrity_passed = true
k7j_rollback_execution_started = false
```

K7K must fail if K7J activation did not complete, token consumption is not exactly once, user-visible route integrity failed, output scope was unbounded, or production/default/weights were mutated.

## User-Visible Route Pointer Integrity

K7K must verify:

```txt
user_visible_route_pointer_integrity_started = true
user_visible_route_pointer_integrity_completed = true
user_visible_route_pointer_integrity_passed = true
current_user_visible_route_points_to_default = true
current_user_visible_route_points_to_candidate = true
current_user_visible_route = ash_tcu_k6p_row_major_emit_candidate_v1
current_user_visible_candidate_id = ash_tcu_k6zw_logical16_native_wgpu_candidate_v1
user_visible_route_pointer_matches_k7j_activation = true
user_visible_route_pointer_changed_after_k7j = false
default_route_pointer_changed_after_k7j = false
production_route_pointer_changed_after_k7j = false
```

## Bounded User-Visible Smoke Plan And Execution

K7K must create and execute bounded smoke verification:

```txt
bounded_user_visible_smoke_plan_created = true
bounded_user_visible_smoke_scope = post_activation_user_visible_health_only
bounded_user_visible_smoke_round_count = 4
bounded_user_visible_smoke_cases_per_round = 16
bounded_user_visible_smoke_total_case_count = 64
bounded_user_visible_smoke_seed_base = ash_tcu_k7k_user_visible_smoke_seed_v1
bounded_user_visible_smoke_uses_user_visible_route = true
bounded_user_visible_smoke_can_mutate_user_visible_route = false
bounded_user_visible_smoke_can_mutate_default_route = false
bounded_user_visible_smoke_can_mutate_production = false
bounded_user_visible_smoke_can_mutate_weights = false
bounded_user_visible_smoke_can_emit_bounded_output = true
bounded_user_visible_smoke_can_emit_unbounded_output = false
bounded_user_visible_smoke_execution_started = true
bounded_user_visible_smoke_execution_completed = true
bounded_user_visible_smoke_execution_scope = post_activation_user_visible_health_only
bounded_user_visible_smoke_user_visible_route_used = true
bounded_user_visible_smoke_user_visible_route_points_to_default = true
bounded_user_visible_smoke_user_visible_route_points_to_candidate = true
bounded_user_visible_smoke_fail_count = 0
bounded_user_visible_smoke_abort_required = false
bounded_user_visible_smoke_output_emitted = true
bounded_user_visible_smoke_output_bounded = true
bounded_user_visible_smoke_output_promoted_to_production = false
bounded_user_visible_smoke_output_promoted_to_performance_claim = false
```

K7K may emit bounded user-visible smoke output. K7K must not claim speed, quality, production readiness, or benchmark improvement.

## User-Visible Output Scope Clamp

K7K must clamp output scope:

```txt
user_visible_output_scope_clamp_created = true
user_visible_output_scope = post_activation_user_visible_smoke_only
user_visible_output_bounded = true
user_visible_output_contains_raw_training_data = false
user_visible_output_contains_weight_dump = false
user_visible_output_contains_unbounded_probe_output = false
user_visible_output_contains_internal_receipt_json = false
user_visible_output_contains_debug_trace = false
user_visible_output_promoted_to_production = false
user_visible_output_promoted_to_performance_claim = false
```

## User-Visible Smoke Digest

K7K must write a digest:

```txt
user_visible_smoke_digest_created = true
user_visible_smoke_digest_scope = post_activation_user_visible_health_only
user_visible_smoke_digest_round_count = 4
user_visible_smoke_digest_total_case_count = 64
user_visible_smoke_digest_fail_count = 0
user_visible_smoke_digest_abort_required = false
user_visible_smoke_digest_contains_raw_output = false
user_visible_smoke_digest_contains_internal_receipt_json = false
user_visible_smoke_digest_promoted_to_performance_claim = false
```

## Guards

### Post-Activation Abort Guard

```txt
post_activation_abort_guard_created = true
post_activation_abort_on_user_visible_pointer_mismatch = true
post_activation_abort_on_smoke_fail = true
post_activation_abort_on_unbounded_output = true
post_activation_abort_on_unexpected_route_mutation = true
post_activation_abort_on_default_route_mutation = true
post_activation_abort_on_production_mutation = true
post_activation_abort_on_weight_mutation = true
post_activation_abort_required = false
```

### No Second User-Visible Activation Guard

```txt
no_second_user_visible_activation_guard_created = true
second_user_visible_activation_allowed = false
second_user_visible_activation_started = false
second_user_visible_activation_completed = false
second_user_visible_activation_token_consumed = false
second_user_visible_route_registry_mutation = false
user_visible_route_registry_mutated_by_k7k = false
```

### No Activation Token Recreation Guard

```txt
no_activation_token_recreation_guard_created = true
activation_token_recreated = false
new_user_visible_activation_token_created = false
new_user_visible_activation_token_granted = false
new_user_visible_activation_token_consumed = false
```

### No User-Visible Route Remutation Guard

```txt
no_user_visible_route_remutation_guard_created = true
user_visible_route_registry_mutated_by_k7k = false
user_visible_route_pointer_changed_after_k7j = false
current_user_visible_route_points_to_default = true
current_user_visible_route_points_to_candidate = true
```

### No Default Route Mutation Guard

```txt
default_route_mutation_guard_created = true
default_route_registry_mutated_by_k7k = false
global_default_route_changed_by_k7k = false
current_default_route_points_to_candidate = true
current_default_route = ash_tcu_k6p_row_major_emit_candidate_v1
```

### No Production Replacement Guard

```txt
production_replacement_allowed = false
production_replacement_executed = false
candidate_route_promoted_to_production = false
production_route_registry_mutated = false
production_route_state_changed = false
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
user_visible_smoke_promoted_to_performance_claim = false
post_activation_health_promoted_to_performance_claim = false
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

## Implementation Files

```txt
crates/burn_webgpu_backend/src/tensorcube_k7k_prior_k7j_activation_execution_receipt.rs
crates/burn_webgpu_backend/src/tensorcube_k7k_user_visible_route_pointer_integrity.rs
crates/burn_webgpu_backend/src/tensorcube_k7k_bounded_user_visible_smoke_plan.rs
crates/burn_webgpu_backend/src/tensorcube_k7k_bounded_user_visible_smoke_execution.rs
crates/burn_webgpu_backend/src/tensorcube_k7k_user_visible_output_scope_clamp.rs
crates/burn_webgpu_backend/src/tensorcube_k7k_user_visible_smoke_digest.rs
crates/burn_webgpu_backend/src/tensorcube_k7k_post_activation_abort_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7k_no_second_user_visible_activation_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7k_no_activation_token_recreation_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7k_no_user_visible_route_remutation_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7k_no_default_route_mutation_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7k_no_production_replacement_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7k_no_weight_mutation_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7k_no_performance_claim_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7k_rollback_pointer_still_available_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7k_verdict.rs
crates/burn_webgpu_backend/src/tensorcube_k7k_contract_audit.rs
crates/orchestrator_local/src/ash_tcu_k7k_user_visible_post_activation_health_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7k_user_visible_post_activation_health_audit.rs
```

## CLI

```powershell
cargo run --manifest-path ./crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_tcu_k7k_user_visible_post_activation_health_audit -- --repo-root <repo> --require-k7j-pass --require-user-visible-activation-executed --verify-user-visible-route-pointer --create-bounded-user-visible-smoke-plan --run-bounded-user-visible-smoke --enforce-user-visible-output-scope-clamp --write-user-visible-smoke-digest --enforce-post-activation-abort-guard --no-second-user-visible-activation --no-activation-token-recreation --no-user-visible-route-remutation --no-default-route-mutation --no-production-replacement --no-weight-mutation --no-performance-claim --verify-rollback-pointer
```

## PASS Markers

```txt
PASS_ASH_TCU_K7K_PRIOR_K7J_ACTIVATION_EXECUTION_RECEIPT
PASS_ASH_TCU_K7K_USER_VISIBLE_ROUTE_POINTER_INTEGRITY
PASS_ASH_TCU_K7K_BOUNDED_USER_VISIBLE_SMOKE_PLAN
PASS_ASH_TCU_K7K_BOUNDED_USER_VISIBLE_SMOKE_EXECUTION
PASS_ASH_TCU_K7K_USER_VISIBLE_OUTPUT_SCOPE_CLAMP
PASS_ASH_TCU_K7K_USER_VISIBLE_SMOKE_DIGEST
PASS_ASH_TCU_K7K_POST_ACTIVATION_ABORT_GUARD
PASS_ASH_TCU_K7K_NO_SECOND_USER_VISIBLE_ACTIVATION
PASS_ASH_TCU_K7K_NO_ACTIVATION_TOKEN_RECREATION
PASS_ASH_TCU_K7K_NO_USER_VISIBLE_ROUTE_REMUTATION
PASS_ASH_TCU_K7K_NO_DEFAULT_ROUTE_MUTATION
PASS_ASH_TCU_K7K_NO_PRODUCTION_REPLACEMENT
PASS_ASH_TCU_K7K_NO_WEIGHT_MUTATION
PASS_ASH_TCU_K7K_NO_PERFORMANCE_CLAIM
PASS_ASH_TCU_K7K_ROLLBACK_POINTER_STILL_AVAILABLE
PASS_ASH_TCU_K7K_USER_VISIBLE_POST_ACTIVATION_HEALTH_GUARD_NO_PRODUCTION_REPLACEMENT_SEAL
```

## FAIL Markers

```txt
FAIL_ASH_TCU_K7K_MISSING_K7J_PRIOR_VERDICT
FAIL_ASH_TCU_K7K_K7J_REQUIRED_STATUS_NOT_MET
FAIL_ASH_TCU_K7K_USER_VISIBLE_ACTIVATION_NOT_EXECUTED
FAIL_ASH_TCU_K7K_ACTIVATION_TOKEN_NOT_CONSUMED
FAIL_ASH_TCU_K7K_ACTIVATION_TOKEN_CONSUMPTION_COUNT_INVALID
FAIL_ASH_TCU_K7K_USER_VISIBLE_LAYER_NOT_OPENED
FAIL_ASH_TCU_K7K_USER_VISIBLE_OUTPUT_NOT_EMITTED
FAIL_ASH_TCU_K7K_USER_VISIBLE_ROUTE_POINTER_MISMATCH
FAIL_ASH_TCU_K7K_USER_VISIBLE_ROUTE_CHANGED_AFTER_K7J
FAIL_ASH_TCU_K7K_DEFAULT_ROUTE_CHANGED_AFTER_K7J
FAIL_ASH_TCU_K7K_PRODUCTION_ROUTE_CHANGED_AFTER_K7J
FAIL_ASH_TCU_K7K_BOUNDED_SMOKE_PLAN_MISSING
FAIL_ASH_TCU_K7K_BOUNDED_SMOKE_NOT_EXECUTED
FAIL_ASH_TCU_K7K_BOUNDED_SMOKE_FAILED
FAIL_ASH_TCU_K7K_BOUNDED_SMOKE_ABORT_REQUIRED
FAIL_ASH_TCU_K7K_USER_VISIBLE_OUTPUT_UNBOUNDED
FAIL_ASH_TCU_K7K_USER_VISIBLE_OUTPUT_CONTAINS_RAW_TRAINING_DATA
FAIL_ASH_TCU_K7K_USER_VISIBLE_OUTPUT_CONTAINS_WEIGHT_DUMP
FAIL_ASH_TCU_K7K_USER_VISIBLE_OUTPUT_CONTAINS_UNBOUNDED_PROBE_OUTPUT
FAIL_ASH_TCU_K7K_USER_VISIBLE_OUTPUT_CONTAINS_INTERNAL_RECEIPT_JSON
FAIL_ASH_TCU_K7K_USER_VISIBLE_SMOKE_DIGEST_MISSING
FAIL_ASH_TCU_K7K_POST_ACTIVATION_ABORT_REQUIRED
FAIL_ASH_TCU_K7K_SECOND_USER_VISIBLE_ACTIVATION_STARTED
FAIL_ASH_TCU_K7K_ACTIVATION_TOKEN_RECREATED
FAIL_ASH_TCU_K7K_USER_VISIBLE_ROUTE_REMUTATED
FAIL_ASH_TCU_K7K_DEFAULT_ROUTE_MUTATED
FAIL_ASH_TCU_K7K_PRODUCTION_REPLACEMENT_EXECUTED
FAIL_ASH_TCU_K7K_PRODUCTION_ROUTE_MUTATED
FAIL_ASH_TCU_K7K_WEIGHT_MUTATION_DETECTED
FAIL_ASH_TCU_K7K_PERFORMANCE_CLAIM_ALLOWED
FAIL_ASH_TCU_K7K_ROLLBACK_EXECUTION_STARTED
```

## Recommended Next Patch

```txt
ASH-TCU-K7L
User-Visible Rollback Rehearsal / Restore Pointer Dry-Run / No Actual Rollback No Production Replacement Seal
```

## Final Seal

```txt
ASH-TCU-K7K does not execute another activation.

ASH-TCU-K7K converts K7J from:
user_visible_activation_execution_completed_default_route_opened

into:
user_visible_post_activation_health_passed_rollback_ready_no_production_replacement

without remutating user-visible route, changing default route, replacing production route, mutating weights, executing rollback, binding base_train, training, optimizer, safetensors mutation, checkpoint mutation, or performance claim.
```
