# ASH-TCU-K7C SPEC

## Title

Canary Route Rollback Rehearsal Window / Repeated Canary Route Restore And Integrity Check / Route Snapshot Digest / No Default Adoption No Production Replacement Seal

## Patch ID

```txt
ASH-TCU-K7C
```

## Status Target

```txt
PASS_ASH_TCU_K7C_CANARY_ROUTE_ROLLBACK_REHEARSAL_WINDOW_NO_DEFAULT_ADOPTION_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Parent Patch

```txt
ASH-TCU-K7B
```

## Required Prior Status

```txt
PASS_ASH_TCU_K7B_INTERNAL_CANARY_STABILITY_WINDOW_NO_DEFAULT_ADOPTION_NO_PRODUCTION_REPLACEMENT_SEAL
```

## Required Prior Verdict

```txt
internal_canary_stability_window_passed_no_default_adoption
```

## Purpose

`ASH-TCU-K7C` uses the K7B internal canary stability window result as the required parent state.

K7B proved that the candidate route can survive a bounded internal canary stability window of 4 rounds x 32 cases, with no drift, no abort, no output leak, no route mutation, no weight mutation, and no performance claim.

K7C extends this from repeated canary execution stability into repeated canary route rollback rehearsal.

K7C may snapshot the internal canary route binding, rehearse temporary unbind and restore inside the internal diagnostic namespace, run post-restore integrity probes, and write rollback window telemetry.

K7C must not change the default route, replace production route, expose user-visible output, promote candidate output into assistant response output, claim performance improvement, bind base_train, construct weight atlas, promote GPU streaming, run loss/backward, run optimizer, commit weights, mutate safetensors, or finalize checkpoint.

## Current K7B Baseline

K7B established:

```txt
repeated_canary_execution_completed = true
repeated_canary_execution_total_case_count = 128
repeated_canary_execution_round_count = 4
repeated_canary_execution_cases_per_round = 32
canary_drift_detected = false
canary_digest_mismatch_count = 0
canary_digest_unstable_round_count = 0
abort_threshold_abort_required = false
stability_output_quarantine_enabled = true
stability_telemetry_fail_count = 0
stability_telemetry_output_leak_count = 0
stability_telemetry_route_mutation_count = 0
stability_telemetry_weight_mutation_count = 0
performance_claim_allowed = false
default_route_registry_mutated = false
production_route_registry_mutated = false
user_visible_route_mutated = false
model_weights_mutated = false
optimizer_state_mutated = false
safetensors_checkpoint_mutated = false
recommended_next_patch = ASH-TCU-K7C_CANARY_ROUTE_ROLLBACK_REHEARSAL_WINDOW_NO_DEFAULT_ADOPTION
```

K7C must treat this as the required parent condition.

## SSOT

### SSOT Owner

```txt
workspace/runtime/tensorcube/ash_tensorcube_k7c_canary_route_rollback_window_latest.json
```

### Secondary Receipts

```txt
workspace/runtime/tensorcube/ash_tensorcube_k7c_prior_k7b_stability_receipt_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7c_rollback_window_config_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7c_canary_route_snapshot_series_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7c_canary_route_unbind_rehearsal_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7c_canary_route_restore_rehearsal_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7c_post_restore_integrity_probe_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7c_rollback_round_digest_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7c_rollback_drift_digest_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7c_rollback_abort_threshold_policy_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7c_rollback_abort_threshold_eval_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7c_rollback_output_quarantine_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7c_rollback_telemetry_summary_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7c_no_default_adoption_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7c_no_production_replacement_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7c_no_user_visible_adoption_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7c_no_weight_mutation_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7c_no_performance_claim_guard_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7c_verdict_latest.json
workspace/runtime/tensorcube/ash_tensorcube_k7c_static_checks_latest.json
artifacts/ASH_TCU_K7C_LOCAL_MANIFEST.json
```

## State Ownership

### K7C owns

```txt
prior_k7b_stability_receipt
rollback_window_config
canary_route_snapshot_series
canary_route_unbind_rehearsal
canary_route_restore_rehearsal
post_restore_integrity_probe
rollback_round_digest
rollback_drift_digest
rollback_abort_threshold_policy
rollback_abort_threshold_eval
rollback_output_quarantine
rollback_telemetry_summary
no_default_adoption_guard
no_production_replacement_guard
no_user_visible_adoption_guard
no_weight_mutation_guard
no_performance_claim_guard
```

### K7C does not own

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

K7C must read and validate the latest K7B receipts:

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

K7C may read K7A internal canary bind receipts as historical evidence only. K7C must not recompute K7B stability execution or expand K7A/K7B internal diagnostic namespace scope.

## Candidate Route

K7C must preserve the exact internal canary candidate route binding:

```txt
internal_canary_namespace_id = ash_tcu_k7a_internal_canary_namespace_v1
internal_canary_namespace_scope = internal_diagnostic_only
candidate_route_bound_to_internal_canary = true
candidate_route_bound_to_default = false
candidate_route_bound_to_production = false
candidate_route_bound_to_user_visible = false
```

K7C must not mutate candidate route, dtype, layout, tile mode, or evidence status.

## Rollback Window Config

K7C must create a bounded rollback rehearsal window:

```txt
rollback_window_config_created = true
rollback_window_scope = internal_diagnostic_only
rollback_window_round_count = 4
rollback_window_cases_per_round = 32
rollback_window_total_case_count = 128
rollback_window_seed_base = ash_tcu_k7c_canary_rollback_window_seed_v1
rollback_window_user_visible = false
rollback_window_can_mutate_default = false
rollback_window_can_mutate_production = false
rollback_window_can_mutate_user_visible = false
rollback_window_can_mutate_weights = false
```

K7C must fail if round count exceeds 4, total case count exceeds 128, user-visible output is opened, or default/production/user-visible/weight mutation is allowed.

## Canary Route Snapshot Series

K7C must snapshot the internal canary route state before each rollback rehearsal round:

```txt
canary_route_snapshot_series_created = true
canary_route_snapshot_count = 4
canary_route_snapshot_scope = internal_diagnostic_only
canary_route_snapshot_hash_present = true
canary_route_snapshot_used_for_restore = true
canary_route_snapshot_contains_default_route = false
canary_route_snapshot_contains_production_route = false
canary_route_snapshot_contains_user_visible_route = false
```

Each snapshot must include round index, namespace id, candidate route id, digest hash, restore target, and `snapshot_user_visible=false`.

## Canary Route Unbind Rehearsal

K7C may rehearse temporary unbind inside the internal diagnostic namespace only:

```txt
canary_route_unbind_rehearsal_started = true
canary_route_unbind_rehearsal_completed = true
canary_route_unbind_rehearsal_scope = internal_diagnostic_only
canary_route_unbind_round_count = 4
canary_route_unbind_from_internal_canary = true
canary_route_unbound_from_default = false
canary_route_unbound_from_production = false
canary_route_unbound_from_user_visible = false
```

This is not default, production, or user-visible route mutation.

## Canary Route Restore Rehearsal

K7C must restore the internal canary route after each unbind rehearsal:

```txt
canary_route_restore_rehearsal_started = true
canary_route_restore_rehearsal_completed = true
canary_route_restore_rehearsal_scope = internal_diagnostic_only
canary_route_restore_round_count = 4
canary_route_restore_used_snapshot = true
canary_route_restored_to_internal_canary = true
canary_route_restored_to_default = false
canary_route_restored_to_production = false
canary_route_restored_to_user_visible = false
```

K7C must fail if any restore round leaves the internal canary namespace unbound.

## Post-Restore Integrity Probe

K7C must run a post-restore integrity probe after every restore round:

```txt
post_restore_integrity_probe_started = true
post_restore_integrity_probe_completed = true
post_restore_integrity_probe_scope = internal_diagnostic_only
post_restore_integrity_probe_round_count = 4
post_restore_integrity_probe_cases_per_round = 32
post_restore_integrity_probe_total_case_count = 128
post_restore_integrity_probe_passed = true
post_restore_integrity_probe_output_quarantined = true
post_restore_integrity_probe_user_visible = false
```

## Rollback Round Digest

K7C must write a digest per rollback rehearsal round:

```txt
rollback_round_digest_created = true
rollback_round_digest_count = 4
rollback_round_digest_scope = internal_diagnostic_only
rollback_round_digest_contains_raw_output = false
rollback_round_digest_user_visible = false
```

Expected round values: unbind completed, restore completed, post-restore probe passed, output quarantined, route mutation false, output leak false, weight mutation false.

## Rollback Drift Digest

K7C must compute a rollback drift digest across the window:

```txt
rollback_drift_digest_created = true
rollback_drift_digest_scope = internal_diagnostic_only
rollback_drift_round_count = 4
rollback_drift_total_case_count = 128
rollback_drift_detected = false
rollback_digest_mismatch_count = 0
rollback_unstable_round_count = 0
rollback_drift_promoted_to_performance_claim = false
```

Rollback drift digest may compare diagnostic hashes. It must not contain raw candidate output or become a performance claim.

## Rollback Abort Threshold Policy And Eval

K7C must define and evaluate strict rollback abort thresholds:

```txt
rollback_abort_threshold_policy_created = true
rollback_abort_threshold_scope = internal_diagnostic_only
rollback_abort_threshold_max_restore_fail_count = 0
rollback_abort_threshold_max_probe_fail_count = 0
rollback_abort_threshold_max_output_leak_count = 0
rollback_abort_threshold_max_route_mutation_count = 0
rollback_abort_threshold_max_weight_mutation_count = 0
rollback_abort_threshold_max_unstable_round_count = 0
rollback_abort_threshold_eval_completed = true
rollback_abort_restore_fail_count = 0
rollback_abort_probe_fail_count = 0
rollback_abort_output_leak_count = 0
rollback_abort_route_mutation_count = 0
rollback_abort_weight_mutation_count = 0
rollback_abort_unstable_round_count = 0
rollback_abort_required = false
```

If rollback abort is required, K7C must not pass.

## Rollback Output Quarantine

K7C must quarantine all rollback rehearsal output:

```txt
rollback_output_quarantine_enabled = true
rollback_output_quarantine_scope = internal_diagnostic_only
rollback_output_committed_to_assistant = false
rollback_output_committed_to_decode = false
rollback_output_promoted_to_user_visible = false
rollback_output_promoted_to_production = false
rollback_output_promoted_to_default = false
rollback_output_contains_raw_text = false
```

## Rollback Telemetry Summary

K7C must write a rollback telemetry summary:

```txt
rollback_telemetry_summary_created = true
rollback_telemetry_scope = internal_diagnostic_only
rollback_telemetry_round_count = 4
rollback_telemetry_total_case_count = 128
rollback_telemetry_restore_fail_count = 0
rollback_telemetry_probe_fail_count = 0
rollback_telemetry_output_leak_count = 0
rollback_telemetry_route_mutation_count = 0
rollback_telemetry_weight_mutation_count = 0
rollback_telemetry_unstable_round_count = 0
rollback_telemetry_abort_required = false
rollback_telemetry_promoted_to_performance_claim = false
```

Telemetry may include diagnostic counts and digest hashes. It must not include user-visible generated output or claim production performance.

## Implementation Files

```txt
crates/burn_webgpu_backend/src/tensorcube_k7c_prior_k7b_stability_receipt.rs
crates/burn_webgpu_backend/src/tensorcube_k7c_rollback_window_config.rs
crates/burn_webgpu_backend/src/tensorcube_k7c_canary_route_snapshot_series.rs
crates/burn_webgpu_backend/src/tensorcube_k7c_canary_route_unbind_rehearsal.rs
crates/burn_webgpu_backend/src/tensorcube_k7c_canary_route_restore_rehearsal.rs
crates/burn_webgpu_backend/src/tensorcube_k7c_post_restore_integrity_probe.rs
crates/burn_webgpu_backend/src/tensorcube_k7c_rollback_round_digest.rs
crates/burn_webgpu_backend/src/tensorcube_k7c_rollback_drift_digest.rs
crates/burn_webgpu_backend/src/tensorcube_k7c_rollback_abort_threshold_policy.rs
crates/burn_webgpu_backend/src/tensorcube_k7c_rollback_abort_threshold_eval.rs
crates/burn_webgpu_backend/src/tensorcube_k7c_rollback_output_quarantine.rs
crates/burn_webgpu_backend/src/tensorcube_k7c_rollback_telemetry_summary.rs
crates/burn_webgpu_backend/src/tensorcube_k7c_no_default_adoption_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7c_no_production_replacement_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7c_no_user_visible_adoption_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7c_no_weight_mutation_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7c_no_performance_claim_guard.rs
crates/burn_webgpu_backend/src/tensorcube_k7c_verdict.rs
crates/burn_webgpu_backend/src/tensorcube_k7c_contract_audit.rs
crates/orchestrator_local/src/ash_tcu_k7c_canary_route_rollback_rehearsal_window_report.rs
crates/orchestrator_local/src/bin/ash_tcu_k7c_canary_route_rollback_rehearsal_window_audit.rs
```

## CLI

```powershell
cargo run --manifest-path ./crates/orchestrator_local/Cargo.toml --features orchestrator_tcu_audit_bins --bin ash_tcu_k7c_canary_route_rollback_rehearsal_window_audit -- --repo-root <repo> --require-k7b-pass --require-stability-window-passed --create-rollback-window --snapshot-canary-route-series --run-canary-route-unbind-rehearsal --run-canary-route-restore-rehearsal --run-post-restore-integrity-probe --write-rollback-round-digest --write-rollback-drift-digest --evaluate-rollback-abort-threshold --quarantine-rollback-output --write-rollback-telemetry --no-default-adoption --no-production-replacement --no-user-visible-adoption --no-weight-mutation --no-performance-claim
```

## PASS Markers

```txt
PASS_ASH_TCU_K7C_PRIOR_K7B_STABILITY_RECEIPT
PASS_ASH_TCU_K7C_ROLLBACK_WINDOW_CONFIG
PASS_ASH_TCU_K7C_CANARY_ROUTE_SNAPSHOT_SERIES
PASS_ASH_TCU_K7C_CANARY_ROUTE_UNBIND_REHEARSAL
PASS_ASH_TCU_K7C_CANARY_ROUTE_RESTORE_REHEARSAL
PASS_ASH_TCU_K7C_POST_RESTORE_INTEGRITY_PROBE
PASS_ASH_TCU_K7C_ROLLBACK_ROUND_DIGEST
PASS_ASH_TCU_K7C_ROLLBACK_DRIFT_DIGEST
PASS_ASH_TCU_K7C_ROLLBACK_ABORT_THRESHOLD_POLICY
PASS_ASH_TCU_K7C_ROLLBACK_ABORT_THRESHOLD_EVAL
PASS_ASH_TCU_K7C_ROLLBACK_OUTPUT_QUARANTINE
PASS_ASH_TCU_K7C_ROLLBACK_TELEMETRY_SUMMARY
PASS_ASH_TCU_K7C_NO_DEFAULT_ADOPTION
PASS_ASH_TCU_K7C_NO_PRODUCTION_REPLACEMENT
PASS_ASH_TCU_K7C_NO_USER_VISIBLE_ADOPTION
PASS_ASH_TCU_K7C_NO_WEIGHT_MUTATION
PASS_ASH_TCU_K7C_NO_PERFORMANCE_CLAIM
PASS_ASH_TCU_K7C_CANARY_ROUTE_ROLLBACK_REHEARSAL_WINDOW_NO_DEFAULT_ADOPTION_NO_PRODUCTION_REPLACEMENT_SEAL
```

## FAIL Markers

```txt
FAIL_ASH_TCU_K7C_MISSING_K7B_PRIOR_VERDICT
FAIL_ASH_TCU_K7C_K7B_REQUIRED_STATUS_NOT_MET
FAIL_ASH_TCU_K7C_K7B_STABILITY_WINDOW_NOT_PASSED
FAIL_ASH_TCU_K7C_K7B_CANARY_DRIFT_DETECTED
FAIL_ASH_TCU_K7C_K7B_ABORT_REQUIRED
FAIL_ASH_TCU_K7C_ROLLBACK_WINDOW_NOT_CREATED
FAIL_ASH_TCU_K7C_ROLLBACK_WINDOW_UNBOUNDED
FAIL_ASH_TCU_K7C_SNAPSHOT_SERIES_MISSING
FAIL_ASH_TCU_K7C_SNAPSHOT_HASH_MISSING
FAIL_ASH_TCU_K7C_UNBIND_REHEARSAL_NOT_COMPLETED
FAIL_ASH_TCU_K7C_RESTORE_REHEARSAL_NOT_COMPLETED
FAIL_ASH_TCU_K7C_ROUTE_NOT_RESTORED_TO_INTERNAL_CANARY
FAIL_ASH_TCU_K7C_POST_RESTORE_PROBE_NOT_COMPLETED
FAIL_ASH_TCU_K7C_POST_RESTORE_PROBE_FAILED
FAIL_ASH_TCU_K7C_ROLLBACK_ROUND_DIGEST_MISSING
FAIL_ASH_TCU_K7C_ROLLBACK_DRIFT_DIGEST_MISSING
FAIL_ASH_TCU_K7C_ROLLBACK_DRIFT_DETECTED
FAIL_ASH_TCU_K7C_ROLLBACK_ABORT_THRESHOLD_POLICY_MISSING
FAIL_ASH_TCU_K7C_ROLLBACK_ABORT_THRESHOLD_EVAL_MISSING
FAIL_ASH_TCU_K7C_ROLLBACK_ABORT_REQUIRED
FAIL_ASH_TCU_K7C_ROLLBACK_OUTPUT_NOT_QUARANTINED
FAIL_ASH_TCU_K7C_ROLLBACK_OUTPUT_LEAKED_TO_ASSISTANT
FAIL_ASH_TCU_K7C_ROLLBACK_OUTPUT_LEAKED_TO_DECODE
FAIL_ASH_TCU_K7C_ROLLBACK_OUTPUT_PROMOTED_TO_USER_VISIBLE
FAIL_ASH_TCU_K7C_ROLLBACK_OUTPUT_PROMOTED_TO_PRODUCTION
FAIL_ASH_TCU_K7C_DEFAULT_ROUTE_MUTATED
FAIL_ASH_TCU_K7C_PRODUCTION_ROUTE_MUTATED
FAIL_ASH_TCU_K7C_USER_VISIBLE_ROUTE_MUTATED
FAIL_ASH_TCU_K7C_WEIGHT_MUTATION_DETECTED
FAIL_ASH_TCU_K7C_PERFORMANCE_CLAIM_ALLOWED
```

## Recommended Next Patch

```txt
ASH-TCU-K7D
Internal Canary Promotion Readiness Packet /
Candidate Route Readiness Without Adoption /
No Default Adoption No Production Replacement Seal
```

## Final Seal

```txt
ASH-TCU-K7C does not make TensorCube production-ready.

ASH-TCU-K7C only converts K7B from:
internal_canary_stability_window_passed_no_default_adoption

into:
canary_route_rollback_rehearsal_window_passed_no_default_adoption

without changing default route, replacing production route, exposing user-visible output, binding base_train, training, optimizer, or weight mutation.
```
