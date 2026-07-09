# ASH-TCU-K7F SPEC

## Title

Direct Default Adoption Execution / Consume Single-Use Direct Adoption Token / Candidate Route Becomes Default / No Shadow / No Production Replacement No Weight Mutation Seal

## Patch ID

```txt
ASH-TCU-K7F
```

## Status Target

```txt
PASS_ASH_TCU_K7F_DIRECT_DEFAULT_ADOPTION_EXECUTION_CANDIDATE_ROUTE_NO_SHADOW_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Parent Patch

```txt
ASH-TCU-K7E
```

## Required Prior Status

```txt
PASS_ASH_TCU_K7E_OPERATOR_REVIEW_TOKEN_FOR_DIRECT_DEFAULT_ADOPTION_NO_SHADOW_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Required Prior Verdict

```txt
direct_default_adoption_operator_token_created_no_shadow_no_execution
```

## Purpose

`ASH-TCU-K7F` uses the K7E direct default adoption token as the required parent state.

K7E created a verified operator identity packet, direct default adoption scope, and single-use direct default adoption token. K7E explicitly excluded shadow rehearsal and proved that default adoption execution had not started.

K7F is the first patch allowed to consume the single-use direct default adoption token and execute direct default adoption.

K7F may change the default route registry.

K7F may promote the candidate route to default route.

K7F may write default adoption execution receipts.

K7F must consume the single-use token exactly once.

K7F must not run shadow rehearsal, create shadow default route, replace production route, open user-visible execution, mutate model weights, run training, run loss/backward, run optimizer step, mutate safetensors, finalize checkpoint, or claim production performance improvement.

## Current K7E Baseline

K7E established:

```txt
direct_default_adoption_token_created = true
direct_default_adoption_token_granted = true
direct_default_adoption_token_scope = direct_default_adoption_only
direct_default_adoption_token_single_use = true
direct_default_adoption_token_consumed = false
direct_default_adoption_token_reuse_allowed = false
direct_default_adoption_token_replay_protected = true
direct_default_adoption_token_signature_present = true
default_adoption_execution_allowed_next = true
default_adoption_execution_started = false
default_adoption_executed = false
candidate_route_promoted_to_default = false
default_route_registry_mutated = false
shadow_rehearsal_allowed = false
shadow_rehearsal_started = false
shadow_default_route_created = false
shadow_default_namespace_created = false
shadow_default_probe_executed = false
production_replacement_executed = false
user_visible_adoption_executed = false
model_weights_mutated = false
optimizer_state_mutated = false
safetensors_checkpoint_mutated = false
performance_claim_allowed = false
recommended_next_patch = ASH-TCU-K7F_DIRECT_DEFAULT_ADOPTION_EXECUTION_CANDIDATE_ROUTE_NO_PRODUCTION_REPLACEMENT
```

K7F must treat this as the required parent condition.

## SSOT

### SSOT Owner

```txt
workspace/runtime/tensorcube/ash_tensorcube_k7f_direct_default_adoption_execution_latest.json
```

### Secondary Receipts

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
workspace/runtime/tensorcube/ash_tensorcube_k7f_static_checks_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7f_verdict_latest.json
artifacts/ASH_TCU_K7F_LOCAL_MANIFEST.json
```

## State Ownership

K7F owns prior K7E token receipt validation, pre-adoption default route snapshot, direct default adoption execution, single-use token consumption, post-adoption default route integrity, default route registry diff, no-shadow/no-production/no-user-visible/no-weight/no-performance guards, and rollback pointer guard.

K7F does not own production route replacement, user-visible execution, assistant message output mutation, runtime decode output mutation, base_train route binding, weight atlas construction, GPU streaming promotion, training execution, loss/backward execution, optimizer step, weight commit, safetensors mutation, checkpoint finalization, shadow default rehearsal, or production performance claim.

## Source Inputs

K7F must read and validate the latest K7E receipts:

```txt
workspace/runtime/tensorcube/ash_tensorcube_k7e_prior_k7d_readiness_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7e_operator_identity_packet_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7e_direct_default_adoption_scope_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7e_direct_default_adoption_token_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7e_single_use_token_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7e_no_shadow_rehearsal_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7e_default_adoption_non_execution_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7e_no_production_replacement_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7e_no_user_visible_execution_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7e_no_weight_mutation_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7e_no_performance_claim_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7e_verdict_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7e_static_checks_latest.json
artifacts/ASH_TCU_K7E_LOCAL_MANIFEST.json
```

K7F may read K6ZZ, K7A, K7B, K7C, and K7D receipts as historical evidence only.

K7F must not recompute prior canary, stability, rollback, readiness, or token creation evidence.

K7F must not create any shadow rehearsal receipt.

## Candidate Route Lineage

K7F must preserve the exact candidate route lineage:

```txt
candidate_route_namespace_id = ash_tcu_k6zz_candidate_route_namespace_v1
internal_canary_namespace_id = ash_tcu_k7a_internal_canary_namespace_v1
candidate_readiness_candidate_id = ash_tcu_k6zw_logical16_native_wgpu_candidate_v1
candidate_readiness_route = ash_tcu_k6p_row_major_emit_candidate_v1
direct_default_adoption_scope = direct_default_adoption_only
```

K7F must promote only this candidate route to default. K7F must not promote any shadow route, production route, or user-visible route.

## Pre-Adoption Default Route Snapshot

K7F must create a pre-adoption snapshot:

```txt
pre_adoption_default_route_snapshot_created = true
pre_adoption_default_route_snapshot_scope = default_route_registry_only
pre_adoption_default_route_snapshot_hash_present = true
pre_adoption_default_route_snapshot_restore_pointer_created = true
pre_adoption_default_route_snapshot_user_visible = false
pre_adoption_default_route_snapshot_contains_weights = false
pre_adoption_default_route_snapshot_contains_raw_output = false
```

This snapshot is for rollback pointer evidence only and must not contain model weights or generated output.

## Direct Default Adoption Execution

K7F must execute direct default adoption:

```txt
direct_default_adoption_execution_started = true
direct_default_adoption_execution_completed = true
direct_default_adoption_execution_scope = default_route_registry_only
direct_default_adoption_used_single_use_token = true
direct_default_adoption_used_shadow_rehearsal = false
direct_default_adoption_candidate_id = ash_tcu_k6zw_logical16_native_wgpu_candidate_v1
direct_default_adoption_route = ash_tcu_k6p_row_major_emit_candidate_v1
candidate_route_promoted_to_default = true
default_adoption_executed = true
default_route_registry_mutated = true
global_default_route_changed = true
```

K7F must not execute production replacement or user-visible output.

## Single-Use Token Consumption

K7F must consume the token exactly once:

```txt
single_use_token_consumption_created = true
token_consumed_before = false
token_consumed_after = true
token_consumption_count = 1
token_single_use = true
token_reuse_allowed = false
token_replay_detected = false
token_scope = direct_default_adoption_only
token_consumed_by_patch = ASH-TCU-K7F
```

K7F must fail if the token was consumed before, remains unconsumed after, is consumed more than once, has a broader scope, allows reuse, or detects replay.

## Post-Adoption Default Route Integrity

K7F must verify post-adoption route integrity:

```txt
post_adoption_default_route_integrity_check_started = true
post_adoption_default_route_integrity_check_completed = true
post_adoption_default_route_integrity_check_passed = true
post_adoption_default_route_points_to_candidate = true
post_adoption_default_route_candidate_id = ash_tcu_k6zw_logical16_native_wgpu_candidate_v1
post_adoption_default_route = ash_tcu_k6p_row_major_emit_candidate_v1
post_adoption_default_route_user_visible_output_executed = false
post_adoption_default_route_production_replacement_executed = false
```

This integrity check validates route selection only. It must not execute decode output, assistant output, or production serving.

## Default Route Registry Diff

K7F must write a registry diff:

```txt
default_route_registry_diff_created = true
default_route_registry_diff_scope = default_route_registry_only
default_route_registry_diff_expected_mutation = true
default_route_registry_diff_only_default_route_changed = true
default_route_registry_diff_production_changed = false
default_route_registry_diff_user_visible_changed = false
default_route_registry_diff_weight_changed = false
default_route_registry_diff_contains_raw_output = false
```

The only allowed mutation is default route pointer replacement.

## Guards

### No Shadow Execution Guard

```txt
no_shadow_execution_guard_created = true
shadow_execution_allowed = false
shadow_execution_started = false
shadow_execution_completed = false
shadow_default_route_created = false
shadow_default_namespace_created = false
shadow_default_probe_executed = false
shadow_default_receipt_written = false
direct_default_adoption_used_shadow_rehearsal = false
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
direct_default_adoption_promoted_to_performance_claim = false
default_route_integrity_promoted_to_performance_claim = false
```

### Rollback Pointer Guard

```txt
rollback_pointer_guard_created = true
previous_default_route_snapshot_available = true
previous_default_route_restore_pointer_created = true
previous_default_route_restore_scope = default_route_registry_only
rollback_pointer_user_visible = false
rollback_pointer_contains_weights = false
rollback_pointer_contains_raw_output = false
```

K7F does not execute rollback. K7F only creates the restore pointer for a future rollback patch if needed.

## Implementation Files

```txt
crates/burn_webgpu_backend/src/tensorcube_k7f_prior_k7e_token_receipt.rs
crates/burn_webgpu_backend/src/tensorcube_k7f_pre_adoption_default_route_snapshot.rs
crates/burn_webgpu_backend/src/tensorcube_k7f_direct_default_adoption_execution.rs
crates/burn_webgpu_backend/src/tensorcube_k7f_single_use_token_consumption.rs
crates/burn_webgpu_backend/src/tensorcube_k7f_post_adoption_default_route_integrity.rs
crates/burn_webgpu_backend/src/tensorcube_k7f_default_route_registry_diff.rs
crates/burn_webgpu_backend/src/tensorcube_k7f_no_shadow_execution_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7f_no_production_replacement_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7f_no_user_visible_execution_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7f_no_weight_mutation_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7f_no_performance_claim_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7f_rollback_pointer_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7f_verdict.rs
crates/burn_webgpu_backend/src/tensorcube_k7f_contract_audit.rs
crates/orchestrator_local/src/ash_tcu_k7f_direct_default_adoption_execution_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7f_direct_default_adoption_execution_audit.rs
```

## CLI

```powershell
cargo run --manifest-path ./crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_tcu_k7f_direct_default_adoption_execution_audit -- --repo-root <repo> --require-k7e-pass --require-direct-default-adoption-token --snapshot-pre-adoption-default-route --consume-direct-default-adoption-token --execute-direct-default-adoption --verify-post-adoption-default-route --write-default-route-registry-diff --exclude-shadow-execution --no-production-replacement --no-user-visible-execution --no-weight-mutation --no-performance-claim --create-rollback-pointer
```

## PASS Markers

```txt
PASS_ASH_TCU_K7F_PRIOR_K7E_TOKEN_RECEIPT
PASS_ASH_TCU_K7F_PRE_ADOPTION_DEFAULT_ROUTE_SNAPSHOT
PASS_ASH_TCU_K7F_DIRECT_DEFAULT_ADOPTION_EXECUTION
PASS_ASH_TCU_K7F_SINGLE_USE_TOKEN_CONSUMPTION
PASS_ASH_TCU_K7F_POST_ADOPTION_DEFAULT_ROUTE_INTEGRITY
PASS_ASH_TCU_K7F_DEFAULT_ROUTE_REGISTRY_DIFF
PASS_ASH_TCU_K7F_NO_SHADOW_EXECUTION
PASS_ASH_TCU_K7F_NO_PRODUCTION_REPLACEMENT
PASS_ASH_TCU_K7F_NO_USER_VISIBLE_EXECUTION
PASS_ASH_TCU_K7F_NO_WEIGHT_MUTATION
PASS_ASH_TCU_K7F_NO_PERFORMANCE_CLAIM
PASS_ASH_TCU_K7F_ROLLBACK_POINTER_GUARD
PASS_ASH_TCU_K7F_DIRECT_DEFAULT_ADOPTION_EXECUTION_CANDIDATE_ROUTE_NO_SHADOW_NO_PRODUCTION_REPLACEMENT_SEAL
```

## FAIL Markers

```txt
FAIL_ASH_TCU_K7F_MISSING_K7E_PRIOR_VERDICT
FAIL_ASH_TCU_K7F_K7E_REQUIRED_STATUS_NOT_MET
FAIL_ASH_TCU_K7F_DIRECT_DEFAULT_ADOPTION_TOKEN_MISSING
FAIL_ASH_TCU_K7F_DIRECT_DEFAULT_ADOPTION_TOKEN_NOT_GRANTED
FAIL_ASH_TCU_K7F_TOKEN_ALREADY_CONSUMED
FAIL_ASH_TCU_K7F_TOKEN_NOT_SINGLE_USE
FAIL_ASH_TCU_K7F_TOKEN_SCOPE_TOO_BROAD
FAIL_ASH_TCU_K7F_PRE_ADOPTION_DEFAULT_ROUTE_SNAPSHOT_MISSING
FAIL_ASH_TCU_K7F_DIRECT_DEFAULT_ADOPTION_NOT_STARTED
FAIL_ASH_TCU_K7F_DIRECT_DEFAULT_ADOPTION_NOT_COMPLETED
FAIL_ASH_TCU_K7F_DIRECT_DEFAULT_ADOPTION_DID_NOT_USE_TOKEN
FAIL_ASH_TCU_K7F_TOKEN_NOT_CONSUMED_AFTER_EXECUTION
FAIL_ASH_TCU_K7F_TOKEN_CONSUMED_MORE_THAN_ONCE
FAIL_ASH_TCU_K7F_CANDIDATE_ROUTE_NOT_PROMOTED_TO_DEFAULT
FAIL_ASH_TCU_K7F_DEFAULT_ADOPTION_NOT_EXECUTED
FAIL_ASH_TCU_K7F_DEFAULT_ROUTE_NOT_MUTATED
FAIL_ASH_TCU_K7F_GLOBAL_DEFAULT_ROUTE_NOT_CHANGED
FAIL_ASH_TCU_K7F_POST_ADOPTION_DEFAULT_ROUTE_INTEGRITY_FAILED
FAIL_ASH_TCU_K7F_DEFAULT_ROUTE_REGISTRY_DIFF_MISSING
FAIL_ASH_TCU_K7F_DEFAULT_ROUTE_DIFF_CONTAINS_UNEXPECTED_MUTATION
FAIL_ASH_TCU_K7F_SHADOW_EXECUTION_STARTED
FAIL_ASH_TCU_K7F_SHADOW_DEFAULT_ROUTE_CREATED
FAIL_ASH_TCU_K7F_PRODUCTION_REPLACEMENT_EXECUTED
FAIL_ASH_TCU_K7F_PRODUCTION_ROUTE_MUTATED
FAIL_ASH_TCU_K7F_USER_VISIBLE_EXECUTION_OPENED
FAIL_ASH_TCU_K7F_USER_VISIBLE_ROUTE_MUTATED
FAIL_ASH_TCU_K7F_ASSISTANT_OUTPUT_CHANGED
FAIL_ASH_TCU_K7F_RUNTIME_DECODE_OUTPUT_CHANGED
FAIL_ASH_TCU_K7F_WEIGHT_MUTATION_DETECTED
FAIL_ASH_TCU_K7F_PERFORMANCE_CLAIM_ALLOWED
FAIL_ASH_TCU_K7F_ROLLBACK_POINTER_MISSING
```

## Recommended Next Patch

```txt
ASH-TCU-K7G
Post Default Adoption Health And Rollback-Ready Guard /
Default Route Candidate Health Probe /
No Production Replacement No Weight Mutation Seal
```

## Final Seal

```txt
ASH-TCU-K7F executes direct default adoption.

ASH-TCU-K7F converts K7E from:
direct_default_adoption_operator_token_created_no_shadow_no_execution

into:
direct_default_adoption_execution_completed_candidate_route_became_default

without running shadow rehearsal, replacing production route, exposing user-visible output, binding base_train, training, optimizer, or weight mutation.
```
