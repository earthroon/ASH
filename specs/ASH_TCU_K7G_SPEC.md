# ASH-TCU-K7G SPEC

## Title

Post Default Adoption Health And Rollback-Ready Guard / Default Route Candidate Health Probe / Default Pointer Integrity / No Production Replacement No Weight Mutation Seal

## Patch ID

```txt
ASH-TCU-K7G
```

## Status Target

```txt
PASS_ASH_TCU_K7G_POST_DEFAULT_ADOPTION_HEALTH_AND_ROLLBACK_READY_GUARD_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Parent Patch

```txt
ASH-TCU-K7F
```

## Required Prior Status

```txt
PASS_ASH_TCU_K7F_DIRECT_DEFAULT_ADOPTION_EXECUTION_CANDIDATE_ROUTE_NO_SHADOW_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Required Prior Verdict

```txt
direct_default_adoption_execution_completed_candidate_route_became_default
```

## Purpose

`ASH-TCU-K7G` uses the K7F direct default adoption execution result as the required parent state.

K7F consumed the single-use direct adoption token and promoted the candidate route to default. K7F proved that only the default route registry changed, while production, user-visible route, assistant output, runtime decode output, model weights, optimizer state, safetensors, checkpoint, shadow path, and performance claims remained sealed.

K7G verifies the newly adopted default route after adoption.

K7G may run quarantined default-route health probes.

K7G may verify the default route still points to the adopted candidate.

K7G may verify the previous default rollback pointer.

K7G may write post-adoption health telemetry.

K7G must not replace production, open user-visible execution, mutate weights, run training, run loss/backward, run optimizer step, mutate safetensors, finalize checkpoint, claim performance improvement, or execute rollback.

K7G only proves that rollback remains available if needed.

## Current K7F Baseline

K7F established:

```txt
candidate_route_promoted_to_default = true
default_adoption_executed = true
default_route_registry_mutated = true
global_default_route_changed = true
direct_default_adoption_execution_started = true
direct_default_adoption_execution_completed = true
direct_default_adoption_used_single_use_token = true
direct_default_adoption_used_shadow_rehearsal = false
token_consumed_before = false
token_consumed_after = true
token_consumption_count = 1
post_adoption_default_route_integrity_check_passed = true
post_adoption_default_route_points_to_candidate = true
default_route_registry_diff_only_default_route_changed = true
shadow_execution_started = false
shadow_default_route_created = false
production_replacement_executed = false
production_route_registry_mutated = false
user_visible_adoption_executed = false
assistant_message_output_changed = false
runtime_decode_output_changed = false
model_weights_mutated = false
optimizer_state_mutated = false
safetensors_checkpoint_mutated = false
performance_claim_allowed = false
rollback_pointer_guard_created = true
previous_default_route_restore_pointer_created = true
```

K7G must treat this as the required parent condition.

## SSOT

### SSOT Owner

```txt
workspace/runtime/tensorcube/ash_tensorcube_k7g_post_default_adoption_health_latest.json
```

### Secondary Receipts

```txt
workspace/runtime/tensorcube/ash_tensorcube_k7g_prior_k7f_default_adoption_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7g_default_route_pointer_integrity_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7g_post_adoption_health_probe_plan_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7g_post_adoption_health_probe_execution_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7g_health_probe_output_quarantine_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7g_health_probe_digest_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7g_rollback_pointer_integrity_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7g_post_adoption_abort_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7g_no_second_default_adoption_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7g_no_production_replacement_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7g_no_user_visible_execution_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7g_no_weight_mutation_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7g_no_performance_claim_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7g_static_checks_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7g_verdict_latest.json
artifacts/ASH_TCU_K7G_LOCAL_MANIFEST.json
```

## State Ownership

K7G owns prior K7F default adoption receipt validation, default route pointer integrity, post-adoption health probe plan, post-adoption health probe execution, health probe output quarantine, health probe digest, rollback pointer integrity, post-adoption abort guard, no-second-default-adoption guard, and no-production/no-user-visible/no-weight/no-performance guards.

K7G does not own second default adoption execution, production route replacement, user-visible execution, assistant output mutation, runtime decode output mutation, base_train route binding, weight atlas construction, GPU streaming promotion, training, loss/backward, optimizer, weight commit, safetensors mutation, checkpoint finalization, rollback execution, or production performance claim.

## Source Inputs

K7G must read and validate the latest K7F receipts:

```txt
workspace/runtime/tensorcube/ash_tensorcube_k7f_prior_k7e_token_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7f_pre_adoption_default_route_snapshot_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7f_direct_default_adoption_execution_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7f_single_use_token_consumption_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7f_post_adoption_default_route_integrity_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7f_default_route_registry_diff_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7f_no_shadow_execution_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7f_no_production_replacement_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7f_no_user_visible_execution_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7f_no_weight_mutation_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7f_no_performance_claim_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7f_rollback_pointer_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7f_verdict_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7f_static_checks_latest.json
artifacts/ASH_TCU_K7F_LOCAL_MANIFEST.json
```

K7G may read K6ZZ, K7A, K7B, K7C, K7D, and K7E receipts as historical evidence only. K7G must not recompute prior canary, stability, rollback, readiness, token creation, or default adoption evidence.

## Candidate Route Lineage

K7G must preserve the adopted candidate route lineage:

```txt
candidate_route_namespace_id = ash_tcu_k6zz_candidate_route_namespace_v1
internal_canary_namespace_id = ash_tcu_k7a_internal_canary_namespace_v1
candidate_readiness_candidate_id = ash_tcu_k6zw_logical16_native_wgpu_candidate_v1
adopted_default_route = ash_tcu_k6p_row_major_emit_candidate_v1
candidate_route_promoted_to_default = true
default_adoption_executed = true
```

K7G must not mutate candidate route, dtype, layout, tile mode, or evidence status.

## Prior K7F Default Adoption Receipt

K7G must verify:

```txt
k7f_required = true
k7f_valid = true
k7f_status = PASS_ASH_TCU_K7F_DIRECT_DEFAULT_ADOPTION_EXECUTION_CANDIDATE_ROUTE_NO_SHADOW_NO_PRODUCTION_REPLACEMENT_SEAL
k7f_candidate_route_promoted_to_default = true
k7f_default_adoption_executed = true
k7f_default_route_registry_mutated = true
k7f_global_default_route_changed = true
k7f_token_consumed_after = true
k7f_token_consumption_count = 1
k7f_post_adoption_default_route_integrity_check_passed = true
k7f_default_route_registry_diff_only_default_route_changed = true
k7f_shadow_execution_started = false
k7f_production_replacement_executed = false
k7f_user_visible_adoption_executed = false
k7f_model_weights_mutated = false
k7f_rollback_pointer_guard_created = true
```

K7G must fail if K7F did not complete default adoption or if token consumption is not exactly once.

## Default Route Pointer Integrity

K7G must verify:

```txt
default_route_pointer_integrity_started = true
default_route_pointer_integrity_completed = true
default_route_pointer_integrity_passed = true
current_default_route_points_to_candidate = true
current_default_route_candidate_id = ash_tcu_k6zw_logical16_native_wgpu_candidate_v1
current_default_route = ash_tcu_k6p_row_major_emit_candidate_v1
default_route_pointer_matches_k7f_adoption = true
default_route_pointer_changed_after_k7f = false
```

K7G must fail if default route no longer points to the adopted candidate route.

## Post-Adoption Health Probe Plan And Execution

K7G must create and execute a bounded health probe plan:

```txt
post_adoption_health_probe_plan_created = true
post_adoption_health_probe_scope = default_route_diagnostic_only
post_adoption_health_probe_round_count = 4
post_adoption_health_probe_cases_per_round = 32
post_adoption_health_probe_total_case_count = 128
post_adoption_health_probe_seed_base = ash_tcu_k7g_post_default_health_seed_v1
post_adoption_health_probe_user_visible = false
post_adoption_health_probe_can_mutate_default = false
post_adoption_health_probe_can_mutate_production = false
post_adoption_health_probe_can_mutate_user_visible = false
post_adoption_health_probe_can_mutate_weights = false
post_adoption_health_probe_execution_started = true
post_adoption_health_probe_execution_completed = true
post_adoption_health_probe_default_route_used = true
post_adoption_health_probe_default_route_points_to_candidate = true
post_adoption_health_probe_fail_count = 0
post_adoption_health_probe_abort_required = false
```

This probe may use the adopted default route as a diagnostic target. The probe is health-only and must not emit assistant output, mutate runtime decode output, or claim performance improvement.

## Health Probe Output Quarantine And Digest

K7G must quarantine all probe output and write a digest:

```txt
health_probe_output_quarantine_enabled = true
health_probe_output_quarantine_scope = default_route_diagnostic_only
health_probe_output_committed_to_assistant = false
health_probe_output_committed_to_decode = false
health_probe_output_promoted_to_user_visible = false
health_probe_output_promoted_to_production = false
health_probe_output_contains_raw_text = false
health_probe_digest_created = true
health_probe_digest_scope = default_route_diagnostic_only
health_probe_digest_round_count = 4
health_probe_digest_total_case_count = 128
health_probe_digest_fail_count = 0
health_probe_digest_abort_required = false
health_probe_digest_contains_raw_output = false
health_probe_digest_promoted_to_performance_claim = false
```

## Rollback Pointer Integrity

K7G must verify rollback readiness:

```txt
rollback_pointer_integrity_started = true
rollback_pointer_integrity_completed = true
rollback_pointer_integrity_passed = true
previous_default_route_snapshot_available = true
previous_default_route_restore_pointer_created = true
previous_default_route_restore_scope = default_route_registry_only
rollback_pointer_user_visible = false
rollback_pointer_contains_weights = false
rollback_pointer_contains_raw_output = false
rollback_execution_started = false
rollback_execution_completed = false
```

K7G must not execute rollback. It only proves rollback can be attempted by a later patch if needed.

## Guards

### Post-Adoption Abort Guard

```txt
post_adoption_abort_guard_created = true
post_adoption_abort_on_default_pointer_mismatch = true
post_adoption_abort_on_health_probe_fail = true
post_adoption_abort_on_output_leak = true
post_adoption_abort_on_unexpected_route_mutation = true
post_adoption_abort_on_weight_mutation = true
post_adoption_abort_required = false
```

### No Second Default Adoption Guard

```txt
no_second_default_adoption_guard_created = true
second_default_adoption_allowed = false
second_default_adoption_started = false
second_default_adoption_completed = false
second_default_route_registry_mutation = false
default_route_registry_mutated_by_k7g = false
global_default_route_changed_by_k7g = false
```

### No Production Replacement Guard

```txt
production_replacement_allowed = false
production_replacement_executed = false
candidate_route_promoted_to_production = false
production_route_registry_mutated = false
production_route_state_changed = false
```

### No User-Visible Execution Guard

```txt
user_visible_execution_allowed = false
user_visible_adoption_executed = false
candidate_route_promoted_to_user_visible = false
assistant_message_output_changed = false
runtime_decode_output_changed = false
user_visible_route_mutated = false
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
health_probe_promoted_to_performance_claim = false
default_route_health_promoted_to_performance_claim = false
```

K7G may say post-default adoption health passed. K7G must not claim speed, quality, or production readiness improvement.

## Implementation Files

```txt
crates/burn_webgpu_backend/src/tensorcube_k7g_prior_k7f_default_adoption_receipt.rs
crates/burn_webgpu_backend/src/tensorcube_k7g_default_route_pointer_integrity.rs
crates/burn_webgpu_backend/src/tensorcube_k7g_post_adoption_health_probe_plan.rs
crates/burn_webgpu_backend/src/tensorcube_k7g_post_adoption_health_probe_execution.rs
crates/burn_webgpu_backend/src/tensorcube_k7g_health_probe_output_quarantine.rs
crates/burn_webgpu_backend/src/tensorcube_k7g_health_probe_digest.rs
crates/burn_webgpu_backend/src/tensorcube_k7g_rollback_pointer_integrity.rs
crates/burn_webgpu_backend/src/tensorcube_k7g_post_adoption_abort_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7g_no_second_default_adoption_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7g_no_production_replacement_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7g_no_user_visible_execution_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7g_no_weight_mutation_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7g_no_performance_claim_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7g_verdict.rs
crates/burn_webgpu_backend/src/tensorcube_k7g_contract_audit.rs
crates/orchestrator_local/src/ash_tcu_k7g_post_default_adoption_health_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7g_post_default_adoption_health_audit.rs
```

## CLI

```powershell
cargo run --manifest-path ./crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_tcu_k7g_post_default_adoption_health_audit -- --repo-root <repo> --require-k7f-pass --require-default-route-adopted --verify-default-route-pointer --create-post-adoption-health-probe-plan --run-post-adoption-health-probe --quarantine-health-probe-output --write-health-probe-digest --verify-rollback-pointer --enforce-post-adoption-abort-guard --no-second-default-adoption --no-production-replacement --no-user-visible-execution --no-weight-mutation --no-performance-claim
```

## PASS Markers

```txt
PASS_ASH_TCU_K7G_PRIOR_K7F_DEFAULT_ADOPTION_RECEIPT
PASS_ASH_TCU_K7G_DEFAULT_ROUTE_POINTER_INTEGRITY
PASS_ASH_TCU_K7G_POST_ADOPTION_HEALTH_PROBE_PLAN
PASS_ASH_TCU_K7G_POST_ADOPTION_HEALTH_PROBE_EXECUTION
PASS_ASH_TCU_K7G_HEALTH_PROBE_OUTPUT_QUARANTINE
PASS_ASH_TCU_K7G_HEALTH_PROBE_DIGEST
PASS_ASH_TCU_K7G_ROLLBACK_POINTER_INTEGRITY
PASS_ASH_TCU_K7G_POST_ADOPTION_ABORT_GUARD
PASS_ASH_TCU_K7G_NO_SECOND_DEFAULT_ADOPTION
PASS_ASH_TCU_K7G_NO_PRODUCTION_REPLACEMENT
PASS_ASH_TCU_K7G_NO_USER_VISIBLE_EXECUTION
PASS_ASH_TCU_K7G_NO_WEIGHT_MUTATION
PASS_ASH_TCU_K7G_NO_PERFORMANCE_CLAIM
PASS_ASH_TCU_K7G_POST_DEFAULT_ADOPTION_HEALTH_AND_ROLLBACK_READY_GUARD_NO_PRODUCTION_REPLACEMENT_SEAL
```

## FAIL Markers

```txt
FAIL_ASH_TCU_K7G_MISSING_K7F_PRIOR_VERDICT
FAIL_ASH_TCU_K7G_K7F_REQUIRED_STATUS_NOT_MET
FAIL_ASH_TCU_K7G_DEFAULT_ADOPTION_NOT_EXECUTED
FAIL_ASH_TCU_K7G_CANDIDATE_ROUTE_NOT_DEFAULT
FAIL_ASH_TCU_K7G_TOKEN_NOT_CONSUMED
FAIL_ASH_TCU_K7G_TOKEN_CONSUMPTION_COUNT_INVALID
FAIL_ASH_TCU_K7G_DEFAULT_ROUTE_POINTER_MISMATCH
FAIL_ASH_TCU_K7G_DEFAULT_ROUTE_CHANGED_AFTER_K7F
FAIL_ASH_TCU_K7G_HEALTH_PROBE_PLAN_MISSING
FAIL_ASH_TCU_K7G_HEALTH_PROBE_NOT_EXECUTED
FAIL_ASH_TCU_K7G_HEALTH_PROBE_FAILED
FAIL_ASH_TCU_K7G_HEALTH_PROBE_ABORT_REQUIRED
FAIL_ASH_TCU_K7G_HEALTH_OUTPUT_NOT_QUARANTINED
FAIL_ASH_TCU_K7G_HEALTH_OUTPUT_LEAKED_TO_ASSISTANT
FAIL_ASH_TCU_K7G_HEALTH_OUTPUT_LEAKED_TO_DECODE
FAIL_ASH_TCU_K7G_HEALTH_OUTPUT_PROMOTED_TO_USER_VISIBLE
FAIL_ASH_TCU_K7G_HEALTH_DIGEST_MISSING
FAIL_ASH_TCU_K7G_ROLLBACK_POINTER_MISSING
FAIL_ASH_TCU_K7G_ROLLBACK_POINTER_INVALID
FAIL_ASH_TCU_K7G_ROLLBACK_EXECUTION_STARTED
FAIL_ASH_TCU_K7G_POST_ADOPTION_ABORT_REQUIRED
FAIL_ASH_TCU_K7G_SECOND_DEFAULT_ADOPTION_STARTED
FAIL_ASH_TCU_K7G_SECOND_DEFAULT_ROUTE_MUTATION
FAIL_ASH_TCU_K7G_PRODUCTION_REPLACEMENT_EXECUTED
FAIL_ASH_TCU_K7G_PRODUCTION_ROUTE_MUTATED
FAIL_ASH_TCU_K7G_USER_VISIBLE_EXECUTION_OPENED
FAIL_ASH_TCU_K7G_USER_VISIBLE_ROUTE_MUTATED
FAIL_ASH_TCU_K7G_ASSISTANT_OUTPUT_CHANGED
FAIL_ASH_TCU_K7G_RUNTIME_DECODE_OUTPUT_CHANGED
FAIL_ASH_TCU_K7G_WEIGHT_MUTATION_DETECTED
FAIL_ASH_TCU_K7G_PERFORMANCE_CLAIM_ALLOWED
```

## Recommended Next Patch

```txt
ASH-TCU-K7H
Default Route User-Visible Readiness Gate /
Quarantined Decode Readiness And Output Leak Guard /
No Production Replacement No Weight Mutation Seal
```

## Final Seal

```txt
ASH-TCU-K7G does not execute another adoption.

ASH-TCU-K7G converts K7F from:
direct_default_adoption_execution_completed_candidate_route_became_default

into:
post_default_adoption_health_passed_rollback_ready_no_production_replacement

without changing default route again, replacing production route, exposing user-visible output, executing rollback, binding base_train, training, optimizer, or weight mutation.
```
