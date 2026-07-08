# ASH-TCU-K6ZZ SPEC

## Title

Gated Apply Execution / Candidate Route Only / Single-Use Approval Token Consumption / Candidate Runtime Route Activation / No Default Adoption No Production Replacement Seal

## Patch ID

```txt
ASH-TCU-K6ZZ
```

## Status Target

```txt
PASS_ASH_TCU_K6ZZ_GATED_APPLY_EXECUTION_CANDIDATE_ROUTE_ONLY_NO_DEFAULT_ADOPTION_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Parent Patch

```txt
ASH-TCU-K6ZY
```

## Required Prior Status

```txt
PASS_ASH_TCU_K6ZY_OPERATOR_APPROVAL_TOKEN_AND_GATED_APPLY_CANDIDATE_NO_DEFAULT_ADOPTION_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Required Prior Verdict

```txt
operator_approval_token_created_gated_apply_candidate_armed_no_default_adoption
```

## Purpose

`ASH-TCU-K6ZZ` uses the K6ZY operator approval token and armed gated apply candidate as the required parent state.

K6ZZ is the first patch in this chain allowed to consume the single-use operator approval token and execute the gated apply candidate.

K6ZZ may activate the TensorCube logical16 native WGPU candidate route in a candidate-only runtime route namespace.

K6ZZ may execute candidate-route-only apply and write candidate route activation receipts.

K6ZZ must not change the default route, replace production route, expose user-visible output, or promote candidate output into assistant response output.

K6ZZ must not bind base_train, weight atlas, GPU streaming, loss/backward, optimizer, weight commit, safetensors mutation, or checkpoint finalization.

## Current K6ZY Baseline

K6ZY established:

```txt
operator_approval_token_created = true
operator_approval_granted = true
operator_approval_source = explicit_cli
operator_approval_token_single_use = true
operator_approval_token_consumed = false
approval_scope_binding_created = true
approval_scope_candidate_id = ash_tcu_k6zw_logical16_native_wgpu_candidate_v1
approval_scope_candidate_route = ash_tcu_k6p_row_major_emit_candidate_v1
gated_apply_candidate_created = true
gated_apply_candidate_armed = true
apply_permission_armed = true
apply_permission_state = armed_pending_execution
apply_execution_allowed_next = true
apply_execution_started = false
apply_execution_completed = false
persistent_runtime_splice_opened = false
default_route_registry_mutated = false
production_route_registry_mutated = false
user_visible_route_mutated = false
recommended_next_patch = ASH-TCU-K6ZZ_GATED_APPLY_EXECUTION_CANDIDATE_ROUTE_ONLY_NO_DEFAULT_ADOPTION
```

K6ZZ must treat this as the required parent condition.

## SSOT

### SSOT Owner

```txt
workspace/runtime/tensorcube/ash_tensorcube_k6zz_gated_apply_execution_latest.json
```

### Secondary Receipts

```txt
workspace/runtime/tensorcube/ash_tensorcube_k6zz_prior_k6zy_approval_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zz_single_use_token_consumption_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zz_candidate_route_namespace_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zz_candidate_apply_execution_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zz_candidate_runtime_route_activation_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zz_candidate_route_health_probe_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zz_candidate_output_quarantine_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zz_post_apply_route_integrity_check_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zz_no_default_adoption_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zz_no_production_replacement_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zz_no_user_visible_adoption_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zz_no_persistent_route_mutation_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zz_no_weight_mutation_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zz_verdict_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k6zz_static_checks_latest.json
artifacts/ASH_TCU_K6ZZ_LOCAL_MANIFEST.json
```

## State Ownership

### K6ZZ owns

```txt
prior_k6zy_approval_receipt
single_use_token_consumption
candidate_route_namespace
candidate_apply_execution
candidate_runtime_route_activation
candidate_route_health_probe
candidate_output_quarantine
post_apply_route_integrity_check
no_default_adoption_guard
no_production_replacement_guard
no_user_visible_adoption_guard
no_persistent_route_mutation_guard
no_weight_mutation_guard
```

### K6ZZ does not own

```txt
default route adoption
production route replacement
user-visible adoption
assistant message output mutation
runtime decode output mutation
base_train route binding
weight atlas construction
GPU streaming promotion
training execution
loss/backward execution
optimizer step
weight commit
safetensors mutation
checkpoint finalization
```

## Source Inputs

K6ZZ must read and validate the latest K6ZY receipts:

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

K6ZZ may read K6ZX dryrun/rollback receipts as rollback evidence source only. K6ZZ must not recompute K6ZX dryrun or rollback evidence. K6ZZ must not expand the K6ZY approval scope.

## Candidate Route

K6ZZ must preserve the exact candidate scope from K6ZY:

```txt
apply_candidate_id = ash_tcu_k6zw_logical16_native_wgpu_candidate_v1
apply_candidate_kind = logical16_native_wgpu_tensorcube_candidate
candidate_route = ash_tcu_k6p_row_major_emit_candidate_v1
candidate_source_patch = ASH-TCU-K6ZV
candidate_apply_scope = candidate_only
approval_scope_candidate_id = ash_tcu_k6zw_logical16_native_wgpu_candidate_v1
approval_scope_candidate_route = ash_tcu_k6p_row_major_emit_candidate_v1
approval_scope_default_adoption_allowed = false
approval_scope_production_replacement_allowed = false
approval_scope_user_visible_adoption_allowed = false
```

K6ZZ must not mutate candidate route, dtype, layout, tile mode, or evidence status.

## Single-Use Token Consumption

K6ZZ must consume the K6ZY approval token exactly once.

Required token fields:

```txt
operator_approval_token_present = true
operator_approval_token_single_use = true
operator_approval_token_consumed_before = false
operator_approval_token_consumed_after = true
operator_approval_token_consumption_recorded = true
operator_approval_token_reuse_allowed = false
operator_approval_token_replay_detected = false
operator_approval_token_consumption_scope = gated_apply_candidate_only
```

K6ZZ must fail if the token was already consumed, if token scope does not match the candidate, or if token scope escalates to default, production, or user-visible adoption.

## Candidate Route Namespace

K6ZZ must create or open a candidate-only runtime route namespace:

```txt
candidate_route_namespace_created = true
candidate_route_namespace_id = ash_tcu_k6zz_candidate_route_namespace_v1
candidate_route_namespace_scope = candidate_only
candidate_route_namespace_persistent = true
candidate_route_namespace_default_visible = false
candidate_route_namespace_production_visible = false
candidate_route_namespace_user_visible = false
```

`candidate_route_namespace_persistent = true` is allowed only for the candidate namespace.

It must not alias default route registry, production route registry, user-visible runtime route, assistant message output route, or base_train route registry.

## Candidate Apply Execution

K6ZZ may execute the gated apply candidate only inside the candidate route namespace:

```txt
apply_execution_started = true
apply_execution_completed = true
apply_execution_passed = true
apply_execution_scope = candidate_route_only
apply_execution_used_operator_token = true
apply_execution_used_single_use_token = true
apply_execution_mutated_default_route = false
apply_execution_mutated_production_route = false
apply_execution_mutated_user_visible_route = false
```

K6ZZ must not set default adoption, production replacement, user-visible adoption, persistent runtime splice, assistant message output change, runtime decode output change, or weight commit.

## Candidate Runtime Route Activation

K6ZZ may activate the candidate route as candidate-only:

```txt
candidate_runtime_route_activation_started = true
candidate_runtime_route_activation_completed = true
candidate_runtime_route_active = true
candidate_runtime_route_id = ash_tcu_k6zz_candidate_route_namespace_v1
candidate_runtime_route_scope = candidate_only
candidate_runtime_route_default_selected = false
candidate_runtime_route_production_selected = false
candidate_runtime_route_user_visible_selected = false
```

This is not default adoption, production replacement, or user-visible selection.

## Candidate Route Health Probe

K6ZZ must execute a candidate-only health probe after candidate activation:

```txt
candidate_route_health_probe_started = true
candidate_route_health_probe_completed = true
candidate_route_health_probe_passed = true
candidate_route_health_probe_scope = candidate_only
candidate_route_health_probe_user_visible = false
candidate_route_health_probe_output_quarantined = true
```

The health probe may produce diagnostic output. The diagnostic output must be quarantined.

## Candidate Output Quarantine

K6ZZ must quarantine any candidate output:

```txt
candidate_output_quarantine_enabled = true
candidate_output_quarantine_scope = candidate_route_only
candidate_output_committed_to_assistant = false
candidate_output_committed_to_decode = false
candidate_output_promoted_to_user_visible = false
candidate_output_promoted_to_production = false
```

K6ZZ must not leak candidate output into assistant messages, runtime decode output, default route, or production route.

## Post-Apply Route Integrity Check

K6ZZ must verify after candidate apply:

```txt
post_apply_route_integrity_check_passed = true
default_route_registry_unchanged = true
production_route_registry_unchanged = true
user_visible_route_unchanged = true
base_train_route_registry_unchanged = true
candidate_route_namespace_active = true
operator_approval_token_consumed_after = true
```

## Guard Requirements

K6ZZ must verify prior K6ZY approval, token consumption, candidate namespace, candidate apply execution, candidate health probe, output quarantine, post-apply route integrity, no default adoption, no production replacement, no user-visible adoption, no weight mutation, and no performance claim.

## Implementation Files

```txt
crates/burn_webgpu_backend/src/tensorcube_k6zz_prior_k6zy_approval_receipt.rs
crates/burn_webgpu_backend/src/tensorcube_k6zz_single_use_token_consumption.rs
crates/burn_webgpu_backend/src/tensorcube_k6zz_candidate_route_namespace.rs
crates/burn_webgpu_backend/src/tensorcube_k6zz_candidate_apply_execution.rs
crates/burn_webgpu_backend/src/tensorcube_k6zz_candidate_runtime_route_activation.rs
crates/burn_webgpu_backend/src/tensorcube_k6zz_candidate_route_health_probe.rs
crates/burn_webgpu_backend/src/tensorcube_k6zz_candidate_output_quarantine.rs
crates/burn_webgpu_backend/src/tensorcube_k6zz_post_apply_route_integrity_check.rs
crates/burn_webgpu_backend/src/tensorcube_k6zz_no_default_adoption_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k6zz_no_production_replacement_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k6zz_no_user_visible_adoption_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k6zz_no_persistent_route_mutation_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k6zz_no_weight_mutation_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k6zz_verdict.rs
crates/burn_webgpu_backend/src/tensorcube_k6zz_contract_audit.rs
crates/orchestrator_local/src/ash_tcu_k6zz_gated_apply_execution_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k6zz_gated_apply_execution_audit.rs
```

## Test Files

```txt
crates/burn_webgpu_backend/tests/ash_tcu_k6zz_prior_k6zy_approval_receipt.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zz_single_use_token_consumption.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zz_candidate_route_namespace.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zz_candidate_apply_execution.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zz_candidate_runtime_route_activation.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zz_candidate_route_health_probe.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zz_candidate_output_quarantine.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zz_post_apply_route_integrity_check.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zz_no_default_adoption_guard.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zz_no_production_replacement_guard.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zz_no_user_visible_adoption_guard.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zz_no_persistent_route_mutation_guard.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zz_no_weight_mutation_guard.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zz_verdict.rs
crates/burn_webgpu_backend/tests/ash_tcu_k6zz_contract_audit.rs
```

## CLI

```powershell
cargo run --manifest-path ./crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_tcu_k6zz_gated_apply_execution_audit -- --repo-root <repo> --require-k6zy-pass --require-operator-approval-token --require-gated-apply-armed --consume-single-use-token --create-candidate-route-namespace --execute-candidate-apply --activate-candidate-runtime-route --run-candidate-health-probe --quarantine-candidate-output --verify-post-apply-route-integrity --no-default-adoption --no-production-replacement --no-user-visible-adoption --no-weight-mutation --no-performance-claim
```

## PASS Markers

```txt
PASS_ASH_TCU_K6ZZ_PRIOR_K6ZY_APPROVAL_RECEIPT
PASS_ASH_TCU_K6ZZ_SINGLE_USE_TOKEN_CONSUMPTION
PASS_ASH_TCU_K6ZZ_CANDIDATE_ROUTE_NAMESPACE
PASS_ASH_TCU_K6ZZ_CANDIDATE_APPLY_EXECUTION
PASS_ASH_TCU_K6ZZ_CANDIDATE_RUNTIME_ROUTE_ACTIVATION
PASS_ASH_TCU_K6ZZ_CANDIDATE_ROUTE_HEALTH_PROBE
PASS_ASH_TCU_K6ZZ_CANDIDATE_OUTPUT_QUARANTINE
PASS_ASH_TCU_K6ZZ_POST_APPLY_ROUTE_INTEGRITY_CHECK
PASS_ASH_TCU_K6ZZ_NO_DEFAULT_ADOPTION
PASS_ASH_TCU_K6ZZ_NO_PRODUCTION_REPLACEMENT
PASS_ASH_TCU_K6ZZ_NO_USER_VISIBLE_ADOPTION
PASS_ASH_TCU_K6ZZ_NO_WEIGHT_MUTATION
PASS_ASH_TCU_K6ZZ_GATED_APPLY_EXECUTION_CANDIDATE_ROUTE_ONLY_NO_DEFAULT_ADOPTION_NO_PRODUCTION_REPLACEMENT_SEAL
```

## FAIL Markers

```txt
FAIL_ASH_TCU_K6ZZ_MISSING_K6ZY_PRIOR_VERDICT
FAIL_ASH_TCU_K6ZZ_K6ZY_REQUIRED_STATUS_NOT_MET
FAIL_ASH_TCU_K6ZZ_OPERATOR_APPROVAL_TOKEN_MISSING
FAIL_ASH_TCU_K6ZZ_OPERATOR_APPROVAL_NOT_GRANTED
FAIL_ASH_TCU_K6ZZ_OPERATOR_TOKEN_NOT_SINGLE_USE
FAIL_ASH_TCU_K6ZZ_OPERATOR_TOKEN_ALREADY_CONSUMED
FAIL_ASH_TCU_K6ZZ_OPERATOR_TOKEN_REPLAY_DETECTED
FAIL_ASH_TCU_K6ZZ_APPROVAL_SCOPE_MISMATCH
FAIL_ASH_TCU_K6ZZ_APPROVAL_SCOPE_ESCALATED_TO_DEFAULT
FAIL_ASH_TCU_K6ZZ_APPROVAL_SCOPE_ESCALATED_TO_PRODUCTION
FAIL_ASH_TCU_K6ZZ_APPROVAL_SCOPE_ESCALATED_TO_USER_VISIBLE
FAIL_ASH_TCU_K6ZZ_GATED_APPLY_NOT_ARMED
FAIL_ASH_TCU_K6ZZ_CANDIDATE_ROUTE_NAMESPACE_NOT_CREATED
FAIL_ASH_TCU_K6ZZ_CANDIDATE_APPLY_NOT_EXECUTED
FAIL_ASH_TCU_K6ZZ_CANDIDATE_RUNTIME_ROUTE_NOT_ACTIVE
FAIL_ASH_TCU_K6ZZ_CANDIDATE_ROUTE_HEALTH_PROBE_FAILED
FAIL_ASH_TCU_K6ZZ_CANDIDATE_OUTPUT_NOT_QUARANTINED
FAIL_ASH_TCU_K6ZZ_DEFAULT_ROUTE_MUTATED
FAIL_ASH_TCU_K6ZZ_PRODUCTION_ROUTE_MUTATED
FAIL_ASH_TCU_K6ZZ_USER_VISIBLE_ROUTE_MUTATED
FAIL_ASH_TCU_K6ZZ_DEFAULT_ADOPTION_EXECUTED
FAIL_ASH_TCU_K6ZZ_PRODUCTION_REPLACEMENT_EXECUTED
FAIL_ASH_TCU_K6ZZ_USER_VISIBLE_ADOPTION_OPENED
FAIL_ASH_TCU_K6ZZ_WEIGHT_MUTATION_DETECTED
FAIL_ASH_TCU_K6ZZ_PERFORMANCE_CLAIM_ALLOWED
```

## Acceptance Criteria

K6ZZ is accepted only if K6ZY prior status is valid, approval token is single-use and unconsumed before K6ZZ, token is consumed exactly once, candidate-only route namespace is created, candidate-route-only apply executes, candidate runtime route activates, candidate health probe passes, output is quarantined, route integrity passes, no default/production/user-visible route mutates, no weights or optimizer/checkpoint state mutate, and K7A is recommended.

## Recommended Next Patch

```txt
ASH-TCU-K7A
Internal Canary Bind / Candidate Route To Limited Internal Canary /
Quarantined Diagnostic Output Only /
No Default Adoption No Production Replacement Seal
```

## Final Seal

```txt
ASH-TCU-K6ZZ does not make TensorCube production-ready.

ASH-TCU-K6ZZ only converts K6ZY from:
operator_approval_token_created_gated_apply_candidate_armed_no_default_adoption

into:
gated_apply_execution_candidate_route_only_passed_no_default_adoption

without changing default route, replacing production route, exposing user-visible output, binding base_train, training, optimizer, or weight mutation.
```
