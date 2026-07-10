# ASH-TCU-K7L SPEC

## Title

User-Visible Rollback Rehearsal / Restore Pointer Dry-Run / No Actual Rollback / No Production Replacement No Weight Mutation Seal

## Patch ID

```txt
ASH-TCU-K7L
```

## Status Target

```txt
PASS_ASH_TCU_K7L_USER_VISIBLE_ROLLBACK_REHEARSAL_NO_ACTUAL_ROLLBACK_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Parent Patch

```txt
ASH-TCU-K7K
```

## Required Prior Status

```txt
PASS_ASH_TCU_K7K_USER_VISIBLE_POST_ACTIVATION_HEALTH_GUARD_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Required Prior Verdict

```txt
user_visible_post_activation_health_passed_rollback_ready_no_production_replacement
```

## Purpose

`ASH-TCU-K7L` uses the K7K user-visible post-activation health result as the required parent state.

K7K proved that the opened user-visible route is healthy, bounded smoke passed, output scope stayed clamped, no second activation occurred, no activation token was recreated, user-visible route was not remutated, and rollback pointers remained available.

K7L verifies rollback readiness without performing rollback.

K7L may rehearse restore pointer resolution.

K7L may dry-run default route restore pointer validation.

K7L may dry-run user-visible route restore pointer validation.

K7L may verify that the rollback plan can be assembled.

K7L may verify that rollback would be scoped only to route registries.

K7L must not execute actual rollback.

K7L must not mutate user-visible route registry.

K7L must not mutate default route registry.

K7L must not mutate production route registry.

K7L must not mutate model weights.

K7L must not run training, loss/backward, optimizer step, safetensors mutation, or checkpoint finalization.

K7L must not claim production performance improvement.

## Current K7K Baseline

K7K established:

```txt
bounded_user_visible_smoke_execution_completed = true
bounded_user_visible_smoke_total_case_count = 64
bounded_user_visible_smoke_fail_count = 0
bounded_user_visible_smoke_abort_required = false
bounded_user_visible_smoke_output_bounded = true
user_visible_output_scope_clamp_created = true
user_visible_output_bounded = true
user_visible_output_contains_raw_training_data = false
user_visible_output_contains_weight_dump = false
user_visible_output_contains_unbounded_probe_output = false
user_visible_output_contains_internal_receipt_json = false
user_visible_route_pointer_integrity_passed = true
current_user_visible_route_points_to_default = true
current_user_visible_route_points_to_candidate = true
user_visible_route_pointer_changed_after_k7j = false
post_activation_abort_required = false
second_user_visible_activation_started = false
activation_token_recreated = false
user_visible_route_registry_mutated_by_k7k = false
default_route_registry_mutated_by_k7k = false
production_replacement_executed = false
production_route_registry_mutated = false
model_weights_mutated = false
optimizer_state_mutated = false
safetensors_checkpoint_mutated = false
performance_claim_allowed = false
rollback_pointer_integrity_passed = true
previous_default_route_restore_pointer_created = true
previous_user_visible_route_restore_pointer_created = true
rollback_execution_started = false
recommended_next_patch = ASH-TCU-K7L_USER_VISIBLE_ROLLBACK_REHEARSAL_NO_PRODUCTION_REPLACEMENT
```

K7L must treat this as the required parent condition.

## SSOT

### SSOT Owner

```txt
workspace/runtime/tensorcube/ash_tensorcube_k7l_user_visible_rollback_rehearsal_latest.json
```

### Secondary Receipts

```txt
workspace/runtime/tensorcube/ash_tensorcube_k7l_prior_k7k_post_activation_health_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7l_rollback_rehearsal_plan_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7l_default_route_restore_pointer_dry_run_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7l_user_visible_route_restore_pointer_dry_run_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7l_restore_scope_integrity_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7l_rollback_rehearsal_digest_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7l_no_actual_rollback_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7l_no_user_visible_route_mutation_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7l_no_default_route_mutation_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7l_no_production_replacement_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7l_no_weight_mutation_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7l_no_performance_claim_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7l_static_checks_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7l_verdict_latest.json
artifacts/ASH_TCU_K7L_LOCAL_MANIFEST.json
```

## State Ownership

K7L owns prior K7K post-activation health receipt validation, rollback rehearsal plan, default route restore pointer dry-run, user-visible route restore pointer dry-run, restore scope integrity, rollback rehearsal digest, no-actual-rollback guard, no-user-visible-route-mutation guard, no-default-route-mutation guard, no-production-replacement guard, no-weight-mutation guard, and no-performance-claim guard.

K7L does not own actual rollback execution, user-visible route registry mutation, default route registry mutation, production route registry mutation, second user-visible activation execution, new user-visible activation token creation, base_train route binding, weight atlas construction, GPU streaming promotion, training, loss/backward, optimizer, weight commit, safetensors mutation, checkpoint finalization, or production performance claim.

## Source Inputs

K7L must read and validate the latest K7K receipts:

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
workspace/runtime/tensorcube/ash_tensorcube_k7k_verdict_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7k_static_checks_latest.json
artifacts/ASH_TCU_K7K_LOCAL_MANIFEST.json
```

K7L may read K6ZZ through K7J receipts as historical evidence only. K7L must not recompute K7J activation, recompute K7K bounded smoke, or execute rollback.

## Prior K7K Post-Activation Health Receipt

K7L must verify:

```txt
k7k_required = true
k7k_valid = true
k7k_status = PASS_ASH_TCU_K7K_USER_VISIBLE_POST_ACTIVATION_HEALTH_GUARD_NO_PRODUCTION_REPLACEMENT_SEAL
k7k_bounded_user_visible_smoke_execution_completed = true
k7k_bounded_user_visible_smoke_total_case_count = 64
k7k_bounded_user_visible_smoke_fail_count = 0
k7k_bounded_user_visible_smoke_abort_required = false
k7k_user_visible_output_bounded = true
k7k_user_visible_route_pointer_integrity_passed = true
k7k_current_user_visible_route_points_to_default = true
k7k_current_user_visible_route_points_to_candidate = true
k7k_post_activation_abort_required = false
k7k_second_user_visible_activation_started = false
k7k_activation_token_recreated = false
k7k_user_visible_route_registry_mutated_by_k7k = false
k7k_default_route_registry_mutated_by_k7k = false
k7k_production_replacement_executed = false
k7k_model_weights_mutated = false
k7k_performance_claim_allowed = false
k7k_rollback_pointer_integrity_passed = true
k7k_previous_default_route_restore_pointer_created = true
k7k_previous_user_visible_route_restore_pointer_created = true
k7k_rollback_execution_started = false
```

K7L must fail if K7K health did not pass, rollback pointers are missing, bounded smoke failed, or any route mutation occurred after K7J.

## Rollback Rehearsal Plan

K7L must create a rollback rehearsal plan:

```txt
rollback_rehearsal_plan_created = true
rollback_rehearsal_scope = dry_run_route_registry_restore_only
rollback_rehearsal_actual_rollback_allowed = false
rollback_rehearsal_default_route_restore_pointer_required = true
rollback_rehearsal_user_visible_route_restore_pointer_required = true
rollback_rehearsal_production_restore_allowed = false
rollback_rehearsal_weight_restore_allowed = false
rollback_rehearsal_contains_weights = false
rollback_rehearsal_contains_raw_output = false
rollback_rehearsal_contains_assistant_message = false
```

K7L must only assemble and validate the rehearsal plan.

## Default Route Restore Pointer Dry-Run

K7L must dry-run default route restore pointer resolution:

```txt
default_route_restore_pointer_dry_run_started = true
default_route_restore_pointer_dry_run_completed = true
default_route_restore_pointer_dry_run_passed = true
default_route_restore_pointer_available = true
default_route_restore_pointer_scope = default_route_registry_only
default_route_restore_pointer_points_to_previous_default = true
default_route_restore_pointer_contains_weights = false
default_route_restore_pointer_contains_raw_output = false
default_route_restore_pointer_would_mutate_default_route = true
default_route_restore_pointer_mutated_default_route = false
```

`would_mutate_default_route=true` is allowed because this is a dry-run description. `mutated_default_route=false` is mandatory.

## User-Visible Route Restore Pointer Dry-Run

K7L must dry-run user-visible route restore pointer resolution:

```txt
user_visible_route_restore_pointer_dry_run_started = true
user_visible_route_restore_pointer_dry_run_completed = true
user_visible_route_restore_pointer_dry_run_passed = true
user_visible_route_restore_pointer_available = true
user_visible_route_restore_pointer_scope = user_visible_route_registry_only
user_visible_route_restore_pointer_points_to_pre_activation_snapshot = true
user_visible_route_restore_pointer_contains_weights = false
user_visible_route_restore_pointer_contains_raw_output = false
user_visible_route_restore_pointer_would_mutate_user_visible_route = true
user_visible_route_restore_pointer_mutated_user_visible_route = false
```

`would_mutate_user_visible_route=true` is allowed because this is a dry-run description. `mutated_user_visible_route=false` is mandatory.

## Restore Scope Integrity

K7L must verify rollback scope boundaries:

```txt
restore_scope_integrity_created = true
restore_scope_integrity_passed = true
restore_scope_default_route_registry_only = true
restore_scope_user_visible_route_registry_only = true
restore_scope_production_route_registry_allowed = false
restore_scope_weight_restore_allowed = false
restore_scope_optimizer_restore_allowed = false
restore_scope_safetensors_restore_allowed = false
restore_scope_checkpoint_restore_allowed = false
restore_scope_contains_training_state = false
restore_scope_contains_raw_output = false
restore_scope_contains_assistant_message = false
```

K7L must fail if restore scope includes production, weights, optimizer, safetensors, checkpoint, raw output, or assistant message output.

## Rollback Rehearsal Digest

K7L must write a digest:

```txt
rollback_rehearsal_digest_created = true
rollback_rehearsal_digest_scope = dry_run_route_registry_restore_only
rollback_rehearsal_digest_default_pointer_dry_run_passed = true
rollback_rehearsal_digest_user_visible_pointer_dry_run_passed = true
rollback_rehearsal_digest_restore_scope_integrity_passed = true
rollback_rehearsal_digest_actual_rollback_executed = false
rollback_rehearsal_digest_contains_weights = false
rollback_rehearsal_digest_contains_raw_output = false
rollback_rehearsal_digest_contains_assistant_message = false
rollback_rehearsal_digest_promoted_to_performance_claim = false
```

Digest rows must include dry_run_step, restore_pointer_kind, restore_pointer_available, restore_pointer_scope, would_mutate_route_registry, actual_route_registry_mutation_detected, production_mutation_detected, weight_mutation_detected, rollback_execution_detected, and scope_integrity_passed.

## Guards

### No Actual Rollback Guard

```txt
no_actual_rollback_guard_created = true
actual_rollback_allowed = false
rollback_execution_started = false
rollback_execution_completed = false
default_route_restore_executed = false
user_visible_route_restore_executed = false
production_restore_executed = false
weight_restore_executed = false
```

### No User-Visible Route Mutation Guard

```txt
user_visible_route_mutation_guard_created = true
user_visible_route_registry_mutated_by_k7l = false
user_visible_route_pointer_changed_by_k7l = false
current_user_visible_route_points_to_default = true
current_user_visible_route_points_to_candidate = true
```

### No Default Route Mutation Guard

```txt
default_route_mutation_guard_created = true
default_route_registry_mutated_by_k7l = false
global_default_route_changed_by_k7l = false
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
rollback_rehearsal_promoted_to_performance_claim = false
restore_dry_run_promoted_to_performance_claim = false
```

K7L may say rollback rehearsal passed. K7L must not claim speed, quality, benchmark, or production readiness improvement.

## Implementation Files

```txt
crates/burn_webgpu_backend/src/tensorcube_k7l_prior_k7k_post_activation_health_receipt.rs
crates/burn_webgpu_backend/src/tensorcube_k7l_rollback_rehearsal_plan.rs
crates/burn_webgpu_backend/src/tensorcube_k7l_default_route_restore_pointer_dry_run.rs
crates/burn_webgpu_backend/src/tensorcube_k7l_user_visible_route_restore_pointer_dry_run.rs
crates/burn_webgpu_backend/src/tensorcube_k7l_restore_scope_integrity.rs
crates/burn_webgpu_backend/src/tensorcube_k7l_rollback_rehearsal_digest.rs
crates/burn_webgpu_backend/src/tensorcube_k7l_no_actual_rollback_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7l_no_user_visible_route_mutation_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7l_no_default_route_mutation_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7l_no_production_replacement_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7l_no_weight_mutation_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7l_no_performance_claim_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7l_verdict.rs
crates/burn_webgpu_backend/src/tensorcube_k7l_contract_audit.rs
crates/orchestrator_local/src/ash_tcu_k7l_user_visible_rollback_rehearsal_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7l_user_visible_rollback_rehearsal_audit.rs
```

## CLI

```powershell
cargo run --manifest-path ./crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_tcu_k7l_user_visible_rollback_rehearsal_audit -- --repo-root <repo> --require-k7k-pass --require-user-visible-post-activation-health --create-rollback-rehearsal-plan --dry-run-default-route-restore-pointer --dry-run-user-visible-route-restore-pointer --verify-restore-scope-integrity --write-rollback-rehearsal-digest --no-actual-rollback --no-user-visible-route-mutation --no-default-route-mutation --no-production-replacement --no-weight-mutation --no-performance-claim
```

## PASS Markers

```txt
PASS_ASH_TCU_K7L_PRIOR_K7K_POST_ACTIVATION_HEALTH_RECEIPT
PASS_ASH_TCU_K7L_ROLLBACK_REHEARSAL_PLAN
PASS_ASH_TCU_K7L_DEFAULT_ROUTE_RESTORE_POINTER_DRY_RUN
PASS_ASH_TCU_K7L_USER_VISIBLE_ROUTE_RESTORE_POINTER_DRY_RUN
PASS_ASH_TCU_K7L_RESTORE_SCOPE_INTEGRITY
PASS_ASH_TCU_K7L_ROLLBACK_REHEARSAL_DIGEST
PASS_ASH_TCU_K7L_NO_ACTUAL_ROLLBACK
PASS_ASH_TCU_K7L_NO_USER_VISIBLE_ROUTE_MUTATION
PASS_ASH_TCU_K7L_NO_DEFAULT_ROUTE_MUTATION
PASS_ASH_TCU_K7L_NO_PRODUCTION_REPLACEMENT
PASS_ASH_TCU_K7L_NO_WEIGHT_MUTATION
PASS_ASH_TCU_K7L_NO_PERFORMANCE_CLAIM
PASS_ASH_TCU_K7L_USER_VISIBLE_ROLLBACK_REHEARSAL_NO_ACTUAL_ROLLBACK_NO_PRODUCTION_REPLACEMENT_SEAL
```

## FAIL Markers

```txt
FAIL_ASH_TCU_K7L_MISSING_K7K_PRIOR_VERDICT
FAIL_ASH_TCU_K7L_K7K_REQUIRED_STATUS_NOT_MET
FAIL_ASH_TCU_K7L_K7K_POST_ACTIVATION_HEALTH_NOT_PASSED
FAIL_ASH_TCU_K7L_ROLLBACK_POINTER_MISSING
FAIL_ASH_TCU_K7L_ROLLBACK_REHEARSAL_PLAN_MISSING
FAIL_ASH_TCU_K7L_DEFAULT_RESTORE_POINTER_DRY_RUN_FAILED
FAIL_ASH_TCU_K7L_USER_VISIBLE_RESTORE_POINTER_DRY_RUN_FAILED
FAIL_ASH_TCU_K7L_RESTORE_SCOPE_INTEGRITY_FAILED
FAIL_ASH_TCU_K7L_RESTORE_SCOPE_INCLUDES_PRODUCTION
FAIL_ASH_TCU_K7L_RESTORE_SCOPE_INCLUDES_WEIGHTS
FAIL_ASH_TCU_K7L_RESTORE_SCOPE_INCLUDES_RAW_OUTPUT
FAIL_ASH_TCU_K7L_ROLLBACK_REHEARSAL_DIGEST_MISSING
FAIL_ASH_TCU_K7L_ACTUAL_ROLLBACK_STARTED
FAIL_ASH_TCU_K7L_ACTUAL_ROLLBACK_COMPLETED
FAIL_ASH_TCU_K7L_USER_VISIBLE_ROUTE_MUTATED
FAIL_ASH_TCU_K7L_DEFAULT_ROUTE_MUTATED
FAIL_ASH_TCU_K7L_PRODUCTION_REPLACEMENT_EXECUTED
FAIL_ASH_TCU_K7L_PRODUCTION_ROUTE_MUTATED
FAIL_ASH_TCU_K7L_WEIGHT_MUTATION_DETECTED
FAIL_ASH_TCU_K7L_PERFORMANCE_CLAIM_ALLOWED
```

## Static Checks

The static checks receipt must verify required prior K7K pass, rollback rehearsal plan creation, default/user-visible restore pointer dry-run pass, restore scope integrity pass, rollback rehearsal digest creation, no actual rollback, no user-visible route mutation, no default route mutation, no production replacement, no weight mutation, and no performance claim.

## Recommended Next Patch

```txt
ASH-TCU-K7M
User-Visible Rollback Token Or Production Readiness Decision Gate / Operator Decision Packet / No Execution No Production Replacement Seal
```

## Final Seal

```txt
ASH-TCU-K7L does not execute rollback.

ASH-TCU-K7L converts K7K from:
user_visible_post_activation_health_passed_rollback_ready_no_production_replacement

into:
user_visible_rollback_rehearsal_passed_no_actual_rollback

without mutating user-visible route, changing default route, replacing production route, mutating weights, executing rollback, binding base_train, training, optimizer, safetensors mutation, checkpoint mutation, or performance claim.
```
