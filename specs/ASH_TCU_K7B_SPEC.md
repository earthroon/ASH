# ASH-TCU-K7B SPEC

## Title

Internal Canary Stability Window / Repeated Canary Probe Window And Abort Threshold / Drift Digest And Quarantined Telemetry / No Default Adoption No Production Replacement Seal

## Patch ID

```txt
ASH-TCU-K7B
```

## Status Target

```txt
PASS_ASH_TCU_K7B_INTERNAL_CANARY_STABILITY_WINDOW_NO_DEFAULT_ADOPTION_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Parent Patch

```txt
ASH-TCU-K7A
```

## Required Prior Status

```txt
PASS_ASH_TCU_K7A_INTERNAL_CANARY_BIND_CANDIDATE_ROUTE_NO_DEFAULT_ADOPTION_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Required Prior Verdict

```txt
internal_canary_bind_candidate_route_passed_no_default_adoption
```

## Purpose

`ASH-TCU-K7B` uses the K7A internal canary bind result as the required parent state.

K7A bound the candidate route to an internal diagnostic canary namespace, executed 32 diagnostic canary cases, quarantined all canary output, compared against the default oracle without mutating default route, wrote telemetry, and proved no abort was required.

K7B extends this from a single internal canary run into a bounded repeated stability window.

K7B may execute repeated internal canary probe rounds, compute diagnostic drift digests across rounds, evaluate abort thresholds across the stability window, and write a canary stability telemetry summary.

K7B must quarantine all probe outputs.

K7B must not change the default route, replace production route, expose user-visible output, promote candidate output into assistant response output, claim performance improvement, bind base_train, construct weight atlas, promote GPU streaming, run loss/backward, run optimizer, commit weights, mutate safetensors, or finalize checkpoint.

## Current K7A Baseline

K7A established:

```txt
internal_canary_namespace_created = true
candidate_route_bound_to_internal_canary = true
internal_canary_execution_completed = true
internal_canary_execution_case_count = 32
canary_output_quarantine_enabled = true
canary_default_oracle_compare_completed = true
canary_telemetry_packet_created = true
canary_telemetry_case_count = 32
canary_telemetry_fail_count = 0
canary_abort_required = false
default_route_registry_mutated = false
production_route_registry_mutated = false
user_visible_route_mutated = false
model_weights_mutated = false
optimizer_state_mutated = false
safetensors_checkpoint_mutated = false
recommended_next_patch = ASH-TCU-K7B_INTERNAL_CANARY_STABILITY_WINDOW_NO_DEFAULT_ADOPTION
```

K7B must treat this as the required parent condition.

## SSOT

### SSOT Owner

```txt
workspace/runtime/tensorcube/ash_tensorcube_k7b_internal_canary_stability_window_latest.json
```

### Secondary Receipts

```txt
workspace/runtime/tensorcube/ash_tensorcube_k7b_prior_k7a_canary_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7b_stability_window_config_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7b_repeated_canary_probe_plan_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7b_repeated_canary_execution_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7b_canary_round_digest_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7b_canary_drift_digest_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7b_abort_threshold_policy_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7b_abort_threshold_eval_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7b_stability_output_quarantine_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7b_default_oracle_window_compare_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7b_stability_telemetry_summary_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7b_no_default_adoption_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7b_no_production_replacement_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7b_no_user_visible_adoption_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7b_no_weight_mutation_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7b_no_performance_claim_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7b_verdict_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7b_static_checks_latest.json
artifacts/ASH_TCU_K7B_LOCAL_MANIFEST.json
```

## State Ownership

### K7B owns

```txt
prior_k7a_canary_receipt
stability_window_config
repeated_canary_probe_plan
repeated_canary_execution
canary_round_digest
canary_drift_digest
abort_threshold_policy
abort_threshold_eval
stability_output_quarantine
default_oracle_window_compare
stability_telemetry_summary
no_default_adoption_guard
no_production_replacement_guard
no_user_visible_adoption_guard
no_weight_mutation_guard
no_performance_claim_guard
```

### K7B does not own

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

K7B must read and validate the latest K7A receipts:

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

K7B may read K6ZZ candidate apply receipts as historical evidence only.

K7B must not recompute K6ZZ candidate apply.

K7B must not expand K7A internal canary namespace scope.

## Candidate Route

K7B must preserve the exact K7A canary binding:

```txt
internal_canary_namespace_id = ash_tcu_k7a_internal_canary_namespace_v1
internal_canary_namespace_scope = internal_diagnostic_only
candidate_route_bound_to_internal_canary = true
candidate_route_bound_to_default = false
candidate_route_bound_to_production = false
candidate_route_bound_to_user_visible = false
```

K7B must not mutate candidate route, dtype, layout, tile mode, or evidence status.

## Stability Window Config

K7B must create a bounded stability window:

```txt
stability_window_config_created = true
stability_window_scope = internal_diagnostic_only
stability_window_round_count = 4
stability_window_cases_per_round = 32
stability_window_total_case_count = 128
stability_window_seed_base = ash_tcu_k7b_internal_canary_stability_seed_v1
stability_window_user_visible = false
stability_window_can_mutate_routes = false
stability_window_can_mutate_weights = false
```

K7B must fail if round count exceeds 4, total case count exceeds 128, user visible is true, route mutation is allowed, or weight mutation is allowed.

## Repeated Canary Probe Plan

K7B must create a deterministic repeated probe plan:

```txt
repeated_canary_probe_plan_created = true
repeated_canary_probe_plan_seeded = true
repeated_canary_probe_plan_round_count = 4
repeated_canary_probe_plan_cases_per_round = 32
repeated_canary_probe_plan_total_case_count = 128
repeated_canary_probe_plan_scope = internal_diagnostic_only
repeated_canary_probe_plan_user_visible = false
```

Each round must have a stable deterministic round seed:

```txt
round_0_seed = ash_tcu_k7b_internal_canary_stability_seed_v1_round_0
round_1_seed = ash_tcu_k7b_internal_canary_stability_seed_v1_round_1
round_2_seed = ash_tcu_k7b_internal_canary_stability_seed_v1_round_2
round_3_seed = ash_tcu_k7b_internal_canary_stability_seed_v1_round_3
```

Probe plan inputs must be synthetic or diagnostic. K7B must not use live user conversations as probe input.

## Repeated Canary Execution

K7B may execute repeated internal canary probes through the candidate route:

```txt
repeated_canary_execution_started = true
repeated_canary_execution_completed = true
repeated_canary_execution_scope = internal_diagnostic_only
repeated_canary_execution_round_count = 4
repeated_canary_execution_cases_per_round = 32
repeated_canary_execution_total_case_count = 128
repeated_canary_execution_candidate_route_used = true
repeated_canary_execution_default_route_mutated = false
repeated_canary_execution_production_route_mutated = false
repeated_canary_execution_user_visible_route_mutated = false
```

K7B must not expose any repeated canary output to user-visible surfaces.

## Canary Round Digest

K7B must write a digest per canary round:

```txt
canary_round_digest_created = true
canary_round_digest_count = 4
canary_round_digest_scope = internal_diagnostic_only
canary_round_digest_user_visible = false
canary_round_digest_contains_raw_output = false
```

Required round digest fields:

```txt
round_index
round_seed
round_case_count
round_fail_count
round_output_quarantined
round_digest_hash_present
round_route_mutation_detected
round_output_leak_detected
round_weight_mutation_detected
```

Expected round values:

```txt
round_case_count = 32
round_fail_count = 0
round_output_quarantined = true
round_route_mutation_detected = false
round_output_leak_detected = false
round_weight_mutation_detected = false
```

## Canary Drift Digest

K7B must compute a stability drift digest across rounds:

```txt
canary_drift_digest_created = true
canary_drift_digest_scope = internal_diagnostic_only
canary_drift_round_count = 4
canary_drift_total_case_count = 128
canary_drift_detected = false
canary_digest_mismatch_count = 0
canary_digest_unstable_round_count = 0
canary_drift_promoted_to_performance_claim = false
```

Drift digest may compare diagnostic hashes. Drift digest must not contain raw candidate output or become a performance claim.

## Abort Threshold Policy

K7B must define abort thresholds:

```txt
abort_threshold_policy_created = true
abort_threshold_scope = internal_diagnostic_only
abort_threshold_max_fail_count = 0
abort_threshold_max_output_leak_count = 0
abort_threshold_max_route_mutation_count = 0
abort_threshold_max_weight_mutation_count = 0
abort_threshold_max_unstable_round_count = 0
abort_threshold_abort_on_any_default_mutation = true
abort_threshold_abort_on_any_production_mutation = true
abort_threshold_abort_on_any_user_visible_mutation = true
```

K7B is strict. Any leak, route mutation, weight mutation, or unstable round requires abort.

## Abort Threshold Eval

K7B must evaluate the stability window against the abort threshold policy:

```txt
abort_threshold_eval_started = true
abort_threshold_eval_completed = true
abort_threshold_fail_count = 0
abort_threshold_output_leak_count = 0
abort_threshold_route_mutation_count = 0
abort_threshold_weight_mutation_count = 0
abort_threshold_unstable_round_count = 0
abort_threshold_abort_required = false
```

If abort is required, K7B must not pass.

## Stability Output Quarantine

K7B must quarantine all repeated canary output:

```txt
stability_output_quarantine_enabled = true
stability_output_quarantine_scope = internal_diagnostic_only
stability_output_committed_to_assistant = false
stability_output_committed_to_decode = false
stability_output_promoted_to_user_visible = false
stability_output_promoted_to_production = false
stability_output_promoted_to_default = false
stability_output_contains_raw_text = false
```

## Default Oracle Window Compare

K7B may compare candidate canary round digests against default route oracle digests:

```txt
default_oracle_window_compare_started = true
default_oracle_window_compare_completed = true
default_oracle_window_compare_scope = diagnostic_only
default_route_used_as_oracle = true
default_route_mutated_by_oracle = false
candidate_route_selected_as_default = false
oracle_output_user_visible = false
oracle_digest_contains_raw_output = false
```

This comparison is not parity promotion, performance promotion, or default adoption.

## Stability Telemetry Summary

K7B must write a stability telemetry summary:

```txt
stability_telemetry_summary_created = true
stability_telemetry_scope = internal_diagnostic_only
stability_telemetry_round_count = 4
stability_telemetry_total_case_count = 128
stability_telemetry_fail_count = 0
stability_telemetry_output_leak_count = 0
stability_telemetry_route_mutation_count = 0
stability_telemetry_weight_mutation_count = 0
stability_telemetry_unstable_round_count = 0
stability_telemetry_abort_required = false
stability_telemetry_promoted_to_performance_claim = false
```

Telemetry may include diagnostic counts and digest hashes. Telemetry must not include user-visible generated output or claim production performance.

## Implementation Files

```txt
crates/burn_webgpu_backend/src/tensorcube_k7b_prior_k7a_canary_receipt.rs
crates/burn_webgpu_backend/src/tensorcube_k7b_stability_window_config.rs
crates/burn_webgpu_backend/src/tensorcube_k7b_repeated_canary_probe_plan.rs
crates/burn_webgpu_backend/src/tensorcube_k7b_repeated_canary_execution.rs
crates/burn_webgpu_backend/src/tensorcube_k7b_canary_round_digest.rs
crates/burn_webgpu_backend/src/tensorcube_k7b_canary_drift_digest.rs
crates/burn_webgpu_backend/src/tensorcube_k7b_abort_threshold_policy.rs
crates/burn_webgpu_backend/src/tensorcube_k7b_abort_threshold_eval.rs
crates/burn_webgpu_backend/src/tensorcube_k7b_stability_output_quarantine.rs
crates/burn_webgpu_backend/src/tensorcube_k7b_default_oracle_window_compare.rs
crates/burn_webgpu_backend/src/tensorcube_k7b_stability_telemetry_summary.rs
crates/burn_webgpu_backend/src/tensorcube_k7b_no_default_adoption_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7b_no_production_replacement_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7b_no_user_visible_adoption_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7b_no_weight_mutation_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7b_no_performance_claim_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7b_verdict.rs
crates/burn_webgpu_backend/src/tensorcube_k7b_contract_audit.rs
crates/orchestrator_local/src/ash_tcu_k7b_internal_canary_stability_window_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7b_internal_canary_stability_window_audit.rs
```

## CLI

```powershell
cargo run --manifest-path ./crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_tcu_k7b_internal_canary_stability_window_audit -- --repo-root <repo> --require-k7a-pass --require-internal-canary-bound --create-stability-window --create-repeated-canary-plan --run-repeated-canary --write-round-digest --write-drift-digest --evaluate-abort-threshold --quarantine-stability-output --compare-default-oracle-window --write-stability-telemetry --no-default-adoption --no-production-replacement --no-user-visible-adoption --no-weight-mutation --no-performance-claim
```

## PASS Markers

```txt
PASS_ASH_TCU_K7B_PRIOR_K7A_CANARY_RECEIPT
PASS_ASH_TCU_K7B_STABILITY_WINDOW_CONFIG
PASS_ASH_TCU_K7B_REPEATED_CANARY_PROBE_PLAN
PASS_ASH_TCU_K7B_REPEATED_CANARY_EXECUTION
PASS_ASH_TCU_K7B_CANARY_ROUND_DIGEST
PASS_ASH_TCU_K7B_CANARY_DRIFT_DIGEST
PASS_ASH_TCU_K7B_ABORT_THRESHOLD_POLICY
PASS_ASH_TCU_K7B_ABORT_THRESHOLD_EVAL
PASS_ASH_TCU_K7B_STABILITY_OUTPUT_QUARANTINE
PASS_ASH_TCU_K7B_DEFAULT_ORACLE_WINDOW_COMPARE
PASS_ASH_TCU_K7B_STABILITY_TELEMETRY_SUMMARY
PASS_ASH_TCU_K7B_NO_DEFAULT_ADOPTION
PASS_ASH_TCU_K7B_NO_PRODUCTION_REPLACEMENT
PASS_ASH_TCU_K7B_NO_USER_VISIBLE_ADOPTION
PASS_ASH_TCU_K7B_NO_WEIGHT_MUTATION
PASS_ASH_TCU_K7B_NO_PERFORMANCE_CLAIM
PASS_ASH_TCU_K7B_INTERNAL_CANARY_STABILITY_WINDOW_NO_DEFAULT_ADOPTION_NO_PRODUCTION_REPLACEMENT_SEAL
```

## FAIL Markers

```txt
FAIL_ASH_TCU_K7B_MISSING_K7A_PRIOR_VERDICT
FAIL_ASH_TCU_K7B_K7A_REQUIRED_STATUS_NOT_MET
FAIL_ASH_TCU_K7B_K7A_INTERNAL_CANARY_NOT_COMPLETED
FAIL_ASH_TCU_K7B_K7A_INTERNAL_CANARY_NOT_BOUND
FAIL_ASH_TCU_K7B_K7A_CANARY_OUTPUT_NOT_QUARANTINED
FAIL_ASH_TCU_K7B_K7A_CANARY_ABORT_REQUIRED
FAIL_ASH_TCU_K7B_STABILITY_WINDOW_NOT_CREATED
FAIL_ASH_TCU_K7B_STABILITY_WINDOW_UNBOUNDED
FAIL_ASH_TCU_K7B_REPEATED_CANARY_PLAN_MISSING
FAIL_ASH_TCU_K7B_REPEATED_CANARY_NOT_EXECUTED
FAIL_ASH_TCU_K7B_REPEATED_CANARY_CASE_COUNT_MISMATCH
FAIL_ASH_TCU_K7B_CANARY_ROUND_DIGEST_MISSING
FAIL_ASH_TCU_K7B_CANARY_DRIFT_DIGEST_MISSING
FAIL_ASH_TCU_K7B_CANARY_DRIFT_DETECTED
FAIL_ASH_TCU_K7B_ABORT_THRESHOLD_POLICY_MISSING
FAIL_ASH_TCU_K7B_ABORT_THRESHOLD_EVAL_MISSING
FAIL_ASH_TCU_K7B_ABORT_THRESHOLD_REQUIRED
FAIL_ASH_TCU_K7B_STABILITY_OUTPUT_NOT_QUARANTINED
FAIL_ASH_TCU_K7B_STABILITY_OUTPUT_LEAKED_TO_ASSISTANT
FAIL_ASH_TCU_K7B_STABILITY_OUTPUT_LEAKED_TO_DECODE
FAIL_ASH_TCU_K7B_STABILITY_OUTPUT_PROMOTED_TO_USER_VISIBLE
FAIL_ASH_TCU_K7B_STABILITY_OUTPUT_PROMOTED_TO_PRODUCTION
FAIL_ASH_TCU_K7B_DEFAULT_ORACLE_MUTATED_DEFAULT_ROUTE
FAIL_ASH_TCU_K7B_DEFAULT_ROUTE_MUTATED
FAIL_ASH_TCU_K7B_PRODUCTION_ROUTE_MUTATED
FAIL_ASH_TCU_K7B_USER_VISIBLE_ROUTE_MUTATED
FAIL_ASH_TCU_K7B_WEIGHT_MUTATION_DETECTED
FAIL_ASH_TCU_K7B_PERFORMANCE_CLAIM_ALLOWED
```

## Acceptance Criteria

K7B is accepted only if K7A prior verdict is valid, internal canary completed, candidate route is bound to internal canary, output quarantine is enabled, K7A canary abort was not required, bounded stability window and deterministic repeated plan are created, 4 rounds x 32 cases execute, round digests and drift digest are written, no drift is detected, abort thresholds are evaluated, abort is not required, all repeated output is quarantined, default oracle compare does not mutate default route, stability telemetry summary is written, no default/production/user-visible route mutates, no weights or optimizer/checkpoint state mutate, no performance claim is allowed, and K7C is recommended.

## Recommended Next Patch

```txt
ASH-TCU-K7C
Canary Route Rollback Rehearsal Window /
Repeated Canary Route Restore And Integrity Check /
No Default Adoption No Production Replacement Seal
```

## Final Seal

```txt
ASH-TCU-K7B does not make TensorCube production-ready.

ASH-TCU-K7B only converts K7A from:
internal_canary_bind_candidate_route_passed_no_default_adoption

into:
internal_canary_stability_window_passed_no_default_adoption

without changing default route, replacing production route, exposing user-visible output, binding base_train, training, optimizer, or weight mutation.
```
