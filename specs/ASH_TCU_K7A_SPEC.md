# ASH-TCU-K7A SPEC

## Title

Internal Canary Bind / Candidate Route To Limited Internal Canary / Quarantined Diagnostic Output Only / No Default Adoption No Production Replacement Seal

## Patch ID

```txt
ASH-TCU-K7A
```

## Status Target

```txt
PASS_ASH_TCU_K7A_INTERNAL_CANARY_BIND_CANDIDATE_ROUTE_NO_DEFAULT_ADOPTION_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Parent Patch

```txt
ASH-TCU-K6ZZ
```

## Required Prior Status

```txt
PASS_ASH_TCU_K6ZZ_GATED_APPLY_EXECUTION_CANDIDATE_ROUTE_ONLY_NO_DEFAULT_ADOPTION_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Required Prior Verdict

```txt
gated_apply_execution_candidate_route_only_passed_no_default_adoption
```

## Purpose

`ASH-TCU-K7A` uses the K6ZZ candidate-route-only apply success as the required parent state.

K6ZZ consumed the single-use operator approval token, executed candidate-route-only apply, activated the candidate runtime route, ran candidate health probe, quarantined candidate output, and proved no default, production, user-visible, or weight mutation.

K7A is the first patch allowed to bind the activated candidate route to an internal canary namespace.

K7A may run limited internal diagnostic canary probes, collect telemetry, and compare candidate canary output against the existing default route as a diagnostic oracle.

K7A must quarantine all candidate output.

K7A must not change the default route, replace production route, expose user-visible output, promote candidate output into assistant response output, bind base_train, construct weight atlas, promote GPU streaming, run loss/backward, run optimizer, commit weights, mutate safetensors, or finalize checkpoint.

## Current K6ZZ Baseline

K6ZZ established:

```txt
operator_approval_token_consumed_after = true
apply_execution_started = true
apply_execution_completed = true
apply_execution_passed = true
apply_execution_scope = candidate_route_only
candidate_route_namespace_created = true
candidate_route_namespace_scope = candidate_only
candidate_runtime_route_active = true
candidate_runtime_route_scope = candidate_only
candidate_route_health_probe_passed = true
candidate_output_quarantine_enabled = true
post_apply_route_integrity_check_passed = true
default_route_registry_mutated = false
production_route_registry_mutated = false
user_visible_route_mutated = false
model_weights_mutated = false
optimizer_state_mutated = false
safetensors_checkpoint_mutated = false
recommended_next_patch = ASH-TCU-K7A_INTERNAL_CANARY_BIND_CANDIDATE_ROUTE_NO_DEFAULT_ADOPTION
```

K7A must treat this as the required parent condition.

## SSOT

### SSOT Owner

```txt
workspace/runtime/tensorcube/ash_tensorcube_k7a_internal_canary_bind_latest.json
```

### Secondary Receipts

```txt
workspace/runtime/tensorcube/ash_tensorcube_k7a_prior_k6zz_candidate_apply_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7a_internal_canary_namespace_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7a_candidate_route_canary_bind_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7a_canary_probe_budget_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7a_internal_canary_probe_plan_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7a_internal_canary_execution_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7a_canary_output_quarantine_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7a_canary_default_oracle_compare_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7a_canary_telemetry_packet_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7a_canary_abort_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7a_no_default_adoption_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7a_no_production_replacement_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7a_no_user_visible_adoption_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7a_no_weight_mutation_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7a_verdict_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7a_static_checks_latest.json
artifacts/ASH_TCU_K7A_LOCAL_MANIFEST.json
```

## State Ownership

### K7A owns

```txt
prior_k6zz_candidate_apply_receipt
internal_canary_namespace
candidate_route_canary_bind
canary_probe_budget
internal_canary_probe_plan
internal_canary_execution
canary_output_quarantine
canary_default_oracle_compare
canary_telemetry_packet
canary_abort_guard
no_default_adoption_guard
no_production_replacement_guard
no_user_visible_adoption_guard
no_weight_mutation_guard
```

### K7A does not own

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

K7A must read and validate the latest K6ZZ receipts:

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

K7A may read K6ZX rollback rehearsal receipts as rollback evidence source only.

K7A must not recompute K6ZZ apply execution.

K7A must not expand K6ZZ candidate route scope.

## Candidate Route

K7A must preserve the exact K6ZZ candidate route:

```txt
candidate_route_namespace_id = ash_tcu_k6zz_candidate_route_namespace_v1
candidate_route_namespace_scope = candidate_only
candidate_runtime_route_active = true
candidate_runtime_route_scope = candidate_only
candidate_runtime_route_default_selected = false
candidate_runtime_route_production_selected = false
candidate_runtime_route_user_visible_selected = false
```

K7A must not mutate candidate route, dtype, layout, tile mode, or evidence status.

## Internal Canary Namespace

K7A must create an internal canary namespace:

```txt
internal_canary_namespace_created = true
internal_canary_namespace_id = ash_tcu_k7a_internal_canary_namespace_v1
internal_canary_namespace_scope = internal_diagnostic_only
internal_canary_namespace_persistent = true
internal_canary_namespace_default_visible = false
internal_canary_namespace_production_visible = false
internal_canary_namespace_user_visible = false
```

The internal canary namespace may persist as diagnostic state.

It must not alias default route registry, production route registry, user-visible runtime route, assistant message output route, runtime decode output route, or base_train route registry.

## Candidate Route Canary Bind

K7A may bind the K6ZZ candidate route into the internal canary namespace:

```txt
candidate_route_canary_bind_started = true
candidate_route_canary_bind_completed = true
candidate_route_canary_bind_scope = internal_diagnostic_only
candidate_route_bound_to_internal_canary = true
candidate_route_bound_to_default = false
candidate_route_bound_to_production = false
candidate_route_bound_to_user_visible = false
```

This is not default adoption, production replacement, or user-visible adoption.

## Canary Probe Budget

K7A must create a bounded probe budget:

```txt
canary_probe_budget_created = true
canary_probe_budget_scope = internal_diagnostic_only
canary_probe_budget_max_cases = 32
canary_probe_budget_exhaustive = false
canary_probe_budget_user_visible = false
canary_probe_budget_can_mutate_routes = false
canary_probe_budget_can_mutate_weights = false
```

K7A must fail if canary execution attempts unbounded probes or routes canary probes to user-visible output.

## Internal Canary Probe Plan

K7A must create a deterministic internal probe plan:

```txt
internal_canary_probe_plan_created = true
internal_canary_probe_plan_seeded = true
internal_canary_probe_plan_seed = ash_tcu_k7a_internal_canary_seed_v1
internal_canary_probe_plan_case_count = 32
internal_canary_probe_plan_scope = internal_diagnostic_only
internal_canary_probe_plan_user_visible = false
```

Probe plan inputs must be synthetic or diagnostic. K7A must not use live user conversations as canary input.

## Internal Canary Execution

K7A may execute internal canary probes through the candidate route:

```txt
internal_canary_execution_started = true
internal_canary_execution_completed = true
internal_canary_execution_scope = internal_diagnostic_only
internal_canary_execution_case_count = 32
internal_canary_execution_candidate_route_used = true
internal_canary_execution_default_route_mutated = false
internal_canary_execution_production_route_mutated = false
internal_canary_execution_user_visible_route_mutated = false
```

K7A must not expose any canary output to user-visible surfaces.

## Canary Output Quarantine

K7A must quarantine all canary output:

```txt
canary_output_quarantine_enabled = true
canary_output_quarantine_scope = internal_diagnostic_only
canary_output_committed_to_assistant = false
canary_output_committed_to_decode = false
canary_output_promoted_to_user_visible = false
canary_output_promoted_to_production = false
canary_output_promoted_to_default = false
```

## Canary Default Oracle Compare

K7A may compare candidate canary results against default route output as a diagnostic oracle:

```txt
canary_default_oracle_compare_started = true
canary_default_oracle_compare_completed = true
canary_default_oracle_compare_scope = diagnostic_only
default_route_used_as_oracle = true
default_route_mutated_by_oracle = false
candidate_route_selected_as_default = false
oracle_output_user_visible = false
```

This comparison is not parity promotion, performance promotion, or default adoption.

## Canary Telemetry Packet

K7A must write canary telemetry:

```txt
canary_telemetry_packet_created = true
canary_telemetry_scope = internal_diagnostic_only
canary_telemetry_case_count = 32
canary_telemetry_fail_count = 0
canary_telemetry_abort_required = false
canary_telemetry_promoted_to_performance_claim = false
```

Telemetry may include diagnostic pass/fail counts. Telemetry must not include user-visible generated output.

## Canary Abort Guard

K7A must define abort conditions:

```txt
canary_abort_guard_created = true
canary_abort_on_route_mutation = true
canary_abort_on_output_leak = true
canary_abort_on_weight_mutation = true
canary_abort_on_unbounded_probe = true
canary_abort_required = false
```

If abort is required, K7A must not pass.

## Implementation Files

```txt
crates/burn_webgpu_backend/src/tensorcube_k7a_prior_k6zz_candidate_apply_receipt.rs
crates/burn_webgpu_backend/src/tensorcube_k7a_internal_canary_namespace.rs
crates/burn_webgpu_backend/src/tensorcube_k7a_candidate_route_canary_bind.rs
crates/burn_webgpu_backend/src/tensorcube_k7a_canary_probe_budget.rs
crates/burn_webgpu_backend/src/tensorcube_k7a_internal_canary_probe_plan.rs
crates/burn_webgpu_backend/src/tensorcube_k7a_internal_canary_execution.rs
crates/burn_webgpu_backend/src/tensorcube_k7a_canary_output_quarantine.rs
crates/burn_webgpu_backend/src/tensorcube_k7a_canary_default_oracle_compare.rs
crates/burn_webgpu_backend/src/tensorcube_k7a_canary_telemetry_packet.rs
crates/burn_webgpu_backend/src/tensorcube_k7a_canary_abort_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7a_no_default_adoption_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7a_no_production_replacement_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7a_no_user_visible_adoption_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7a_no_weight_mutation_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7a_verdict.rs
crates/burn_webgpu_backend/src/tensorcube_k7a_contract_audit.rs
crates/orchestrator_local/src/ash_tcu_k7a_internal_canary_bind_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7a_internal_canary_bind_audit.rs
```

## Test Files

```txt
crates/burn_webgpu_backend/tests/ash_tcu_k7a_prior_k6zz_candidate_apply_receipt.rs
crates/burn_webgpu_backend/tests/ash_tcu_k7a_internal_canary_namespace.rs
crates/burn_webgpu_backend/tests/ash_tcu_k7a_candidate_route_canary_bind.rs
crates/burn_webgpu_backend/tests/ash_tcu_k7a_canary_probe_budget.rs
crates/burn_webgpu_backend/tests/ash_tcu_k7a_internal_canary_probe_plan.rs
crates/burn_webgpu_backend/tests/ash_tcu_k7a_internal_canary_execution.rs
crates/burn_webgpu_backend/tests/ash_tcu_k7a_canary_output_quarantine.rs
crates/burn_webgpu_backend/tests/ash_tcu_k7a_canary_default_oracle_compare.rs
crates/burn_webgpu_backend/tests/ash_tcu_k7a_canary_telemetry_packet.rs
crates/burn_webgpu_backend/tests/ash_tcu_k7a_canary_abort_guard.rs
crates/burn_webgpu_backend/tests/ash_tcu_k7a_no_default_adoption_guard.rs
crates/burn_webgpu_backend/tests/ash_tcu_k7a_no_production_replacement_guard.rs
crates/burn_webgpu_backend/tests/ash_tcu_k7a_no_user_visible_adoption_guard.rs
crates/burn_webgpu_backend/tests/ash_tcu_k7a_no_weight_mutation_guard.rs
crates/burn_webgpu_backend/tests/ash_tcu_k7a_verdict.rs
crates/burn_webgpu_backend/tests/ash_tcu_k7a_contract_audit.rs
```

## CLI

```powershell
cargo run --manifest-path ./crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_tcu_k7a_internal_canary_bind_audit -- --repo-root <repo> --require-k6zz-pass --require-candidate-route-active --bind-internal-canary --create-canary-probe-budget --create-canary-probe-plan --run-internal-canary --compare-default-oracle --quarantine-canary-output --write-canary-telemetry --enforce-canary-abort-guard --no-default-adoption --no-production-replacement --no-user-visible-adoption --no-weight-mutation --no-performance-claim
```

## PASS Markers

```txt
PASS_ASH_TCU_K7A_PRIOR_K6ZZ_CANDIDATE_APPLY_RECEIPT
PASS_ASH_TCU_K7A_INTERNAL_CANARY_NAMESPACE
PASS_ASH_TCU_K7A_CANDIDATE_ROUTE_CANARY_BIND
PASS_ASH_TCU_K7A_CANARY_PROBE_BUDGET
PASS_ASH_TCU_K7A_INTERNAL_CANARY_PROBE_PLAN
PASS_ASH_TCU_K7A_INTERNAL_CANARY_EXECUTION
PASS_ASH_TCU_K7A_CANARY_OUTPUT_QUARANTINE
PASS_ASH_TCU_K7A_CANARY_DEFAULT_ORACLE_COMPARE
PASS_ASH_TCU_K7A_CANARY_TELEMETRY_PACKET
PASS_ASH_TCU_K7A_CANARY_ABORT_GUARD
PASS_ASH_TCU_K7A_NO_DEFAULT_ADOPTION
PASS_ASH_TCU_K7A_NO_PRODUCTION_REPLACEMENT
PASS_ASH_TCU_K7A_NO_USER_VISIBLE_ADOPTION
PASS_ASH_TCU_K7A_NO_WEIGHT_MUTATION
PASS_ASH_TCU_K7A_INTERNAL_CANARY_BIND_CANDIDATE_ROUTE_NO_DEFAULT_ADOPTION_NO_PRODUCTION_REPLACEMENT_SEAL
```

## FAIL Markers

```txt
FAIL_ASH_TCU_K7A_MISSING_K6ZZ_PRIOR_VERDICT
FAIL_ASH_TCU_K7A_K6ZZ_REQUIRED_STATUS_NOT_MET
FAIL_ASH_TCU_K7A_K6ZZ_CANDIDATE_APPLY_NOT_PASSED
FAIL_ASH_TCU_K7A_K6ZZ_CANDIDATE_ROUTE_NOT_ACTIVE
FAIL_ASH_TCU_K7A_K6ZZ_OUTPUT_NOT_QUARANTINED
FAIL_ASH_TCU_K7A_INTERNAL_CANARY_NAMESPACE_NOT_CREATED
FAIL_ASH_TCU_K7A_CANDIDATE_ROUTE_CANARY_BIND_FAILED
FAIL_ASH_TCU_K7A_CANARY_PROBE_BUDGET_MISSING
FAIL_ASH_TCU_K7A_CANARY_PROBE_BUDGET_UNBOUNDED
FAIL_ASH_TCU_K7A_INTERNAL_CANARY_PLAN_MISSING
FAIL_ASH_TCU_K7A_INTERNAL_CANARY_NOT_EXECUTED
FAIL_ASH_TCU_K7A_CANARY_OUTPUT_NOT_QUARANTINED
FAIL_ASH_TCU_K7A_CANARY_OUTPUT_LEAKED_TO_ASSISTANT
FAIL_ASH_TCU_K7A_CANARY_OUTPUT_LEAKED_TO_DECODE
FAIL_ASH_TCU_K7A_CANARY_OUTPUT_PROMOTED_TO_USER_VISIBLE
FAIL_ASH_TCU_K7A_CANARY_OUTPUT_PROMOTED_TO_PRODUCTION
FAIL_ASH_TCU_K7A_DEFAULT_ORACLE_MUTATED_DEFAULT_ROUTE
FAIL_ASH_TCU_K7A_CANARY_ABORT_REQUIRED
FAIL_ASH_TCU_K7A_DEFAULT_ROUTE_MUTATED
FAIL_ASH_TCU_K7A_PRODUCTION_ROUTE_MUTATED
FAIL_ASH_TCU_K7A_USER_VISIBLE_ROUTE_MUTATED
FAIL_ASH_TCU_K7A_WEIGHT_MUTATION_DETECTED
FAIL_ASH_TCU_K7A_PERFORMANCE_CLAIM_ALLOWED
```

## Acceptance Criteria

K7A is accepted only if K6ZZ prior verdict is valid, candidate apply passed, candidate route is active, output quarantine is enabled, internal canary namespace is created, candidate route is bound to internal canary only, bounded canary budget and deterministic plan are created, internal canary executes 32 cases, output is quarantined, default oracle compare does not mutate default route, telemetry is written, abort is not required, default/production/user-visible route registries remain unchanged, no weights or optimizer/checkpoint state mutate, no performance claim is allowed, and K7B is recommended.

## Recommended Next Patch

```txt
ASH-TCU-K7B
Internal Canary Stability Window /
Repeated Canary Probe Window And Abort Threshold /
No Default Adoption No Production Replacement Seal
```

## Final Seal

```txt
ASH-TCU-K7A does not make TensorCube production-ready.

ASH-TCU-K7A only converts K6ZZ from:
gated_apply_execution_candidate_route_only_passed_no_default_adoption

into:
internal_canary_bind_candidate_route_passed_no_default_adoption

without changing default route, replacing production route, exposing user-visible output, binding base_train, training, optimizer, or weight mutation.
```
