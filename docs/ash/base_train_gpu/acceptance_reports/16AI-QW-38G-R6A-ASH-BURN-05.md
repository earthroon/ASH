# 16AI-QW-38G-R6A-ASH-BURN-05

## Title
Burn Backend Route Promotion Candidate / No Production Default Change Seal

## SSOT
Backend route promotion candidate is a candidate-only stage. It binds the BURN-04 strict probe result, BURN-03 raw handle evidence, and backend route policy into a route candidate without changing production default, mutating active backend pointers, executing sandbox/shadow commit, replacing executor, triggering forward execution, or emitting output.

## Receipt
```json
{
  "patch_id": "16AI-QW-38G-R6A-ASH-BURN-05",
  "title": "Burn Backend Route Promotion Candidate / No Production Default Change Seal",
  "burn04_strict_probe_required": true,
  "burn04_strict_probe_respected": true,
  "burn03_raw_handle_evidence_required": true,
  "burn03_raw_handle_evidence_respected": true,
  "backend_route_policy_inventory_required": true,
  "backend_route_policy_inventory_present": true,
  "same_device_bridge_strict_probe_executed": true,
  "probe_result_digest_bound": true,
  "backend_device_queue_parity_checked": true,
  "backend_device_queue_parity_digest_bound": true,
  "backend_route_promotion_candidate_allowed": true,
  "backend_route_promotion_candidate_created": true,
  "candidate_backend_id_present": true,
  "candidate_backend_id_digest_bound": true,
  "candidate_backend_route_digest_bound": true,
  "candidate_route_source_matches_burn04_probe": true,
  "candidate_route_source_matches_burn03_raw_handle_evidence": true,
  "candidate_route_source_matches_backend_policy": true,
  "candidate_backend_family_webgpu": true,
  "candidate_backend_family_same_device_raw_bridge": true,
  "candidate_backend_family_vendor_scaffold": true,
  "candidate_bound_as_route_candidate": true,
  "candidate_bound_as_active_backend": false,
  "candidate_bound_as_production_default": false,
  "candidate_bound_as_forward_executor": false,
  "backend_route_candidate_scheduled_for_sandbox": true,
  "production_default_change_allowed": false,
  "production_default_changed": false,
  "backend_default_promotion_allowed": false,
  "backend_default_promoted": false,
  "active_backend_pointer_mutation_allowed": false,
  "active_backend_pointer_mutated": false,
  "backend_route_promotion_allowed": false,
  "backend_route_promotion_executed": false,
  "qwave_backend_active_route_mutated": false,
  "qwave_backend_production_route_mutated": false,
  "backend_apply_sandbox_allowed": false,
  "backend_apply_sandbox_executed": false,
  "backend_shadow_commit_allowed": false,
  "backend_shadow_commit_executed": false,
  "backend_rollback_ledger_mutated": false,
  "executor_replaced": false,
  "forward_execution_triggered": false,
  "inference_execution_triggered": false,
  "tensor_data_materialized": false,
  "tensor_buffer_written": false,
  "runtime_apply_executed": false,
  "runtime_sequence_mutated": false,
  "runtime_token_append_executed": false,
  "cargo_dependency_rewritten": false,
  "cargo_feature_activated": false,
  "vendor_source_mutated": false,
  "production_output_emitted": false,
  "final_response_emitted": false,
  "receipt_key": "ash-burn05-backend-route-promotion-candidate:5fe479a5d5b041c5e9320ebfded5bec1f495d88662e2abb10d2542f8576469fc",
  "receipt_digest": "16dfb05e12fe0c9514667cbd63d59cb80f7956499d67eef73a2fa79f4d6f8336",
  "status": "PASS_ASH_BURN_05_BACKEND_ROUTE_PROMOTION_CANDIDATE_NO_PRODUCTION_DEFAULT_CHANGE",
  "verdict": "PASS_ASH_BURN_05_BACKEND_ROUTE_PROMOTION_CANDIDATE_NO_PRODUCTION_DEFAULT_CHANGE"
}
```

## Positive cases
- CASE-POS-ASH-BURN-05-00: BURN-04 strict probe present, route promotion candidate created, production default changed false -> PASS.
- CASE-POS-ASH-BURN-05-01: candidate source matches BURN-04 probe / BURN-03 raw handle / backend policy, candidate route digest bound -> PASS.
- CASE-POS-ASH-BURN-05-02: route candidate scheduled for sandbox, sandbox execution false, shadow commit false -> PASS_WITH_WARN.
- CASE-POS-ASH-BURN-05-03: candidate bound as route candidate, not active backend, not production default, not forward executor -> PASS.

## Warn cases
- WARN_ASH_BURN_05_ROUTE_CANDIDATE_CREATED_SANDBOX_REQUIRED: route candidate exists and sandbox is required next, but sandbox has not executed in BURN-05.
- WARN_ASH_BURN_05_STRICT_PROBE_SUCCESS_NOT_DEFAULT_BACKEND: strict probe success and route candidate are not production default backend.

## Negative cases
- FAIL_BURN04_STRICT_PROBE_MISSING
- FAIL_BURN03_RAW_HANDLE_EVIDENCE_MISSING
- FAIL_BACKEND_ROUTE_POLICY_INVENTORY_MISSING
- FAIL_STRICT_PROBE_RESULT_DIGEST_MISSING
- FAIL_BACKEND_ROUTE_PROMOTION_CANDIDATE_NOT_CREATED
- FAIL_CANDIDATE_BACKEND_ID_MISSING
- FAIL_CANDIDATE_BACKEND_ROUTE_DIGEST_MISSING
- FAIL_CANDIDATE_ROUTE_SOURCE_MISMATCH_BURN04_PROBE
- FAIL_CANDIDATE_ROUTE_SOURCE_MISMATCH_BURN03_RAW_HANDLE
- FAIL_CANDIDATE_ROUTE_SOURCE_MISMATCH_BACKEND_POLICY
- FAIL_ROUTE_CANDIDATE_PROMOTED_TO_ACTIVE_BACKEND
- FAIL_ROUTE_CANDIDATE_PROMOTED_TO_PRODUCTION_DEFAULT
- FAIL_ROUTE_CANDIDATE_PROMOTED_TO_FORWARD_EXECUTOR
- FAIL_PRODUCTION_DEFAULT_CHANGED_TOO_EARLY
- FAIL_BACKEND_DEFAULT_PROMOTED_TOO_EARLY
- FAIL_ACTIVE_BACKEND_POINTER_MUTATED_TOO_EARLY
- FAIL_BACKEND_ROUTE_PROMOTED_TOO_EARLY
- FAIL_QWAVE_BACKEND_ACTIVE_ROUTE_MUTATED_TOO_EARLY
- FAIL_BACKEND_APPLY_SANDBOX_EXECUTED_TOO_EARLY
- FAIL_BACKEND_SHADOW_COMMIT_EXECUTED_TOO_EARLY
- FAIL_BACKEND_ROLLBACK_LEDGER_MUTATED_TOO_EARLY
- FAIL_EXECUTOR_REPLACED_TOO_EARLY
- FAIL_FORWARD_EXECUTION_TRIGGERED_TOO_EARLY
- FAIL_INFERENCE_EXECUTION_TRIGGERED_TOO_EARLY
- FAIL_TENSOR_DATA_MATERIALIZED_TOO_EARLY
- FAIL_TENSOR_BUFFER_WRITTEN_TOO_EARLY
- FAIL_RUNTIME_APPLY_EXECUTED_TOO_EARLY
- FAIL_RUNTIME_SEQUENCE_MUTATED_TOO_EARLY
- FAIL_RUNTIME_TOKEN_APPEND_EXECUTED_TOO_EARLY
- FAIL_CARGO_DEPENDENCY_REWRITTEN_TOO_EARLY
- FAIL_VENDOR_FEATURE_ACTIVATED_TOO_EARLY
- FAIL_VENDOR_SOURCE_MUTATED_TOO_EARLY
- FAIL_PRODUCTION_OUTPUT_EMITTED_TOO_EARLY
- FAIL_FINAL_RESPONSE_EMITTED_TOO_EARLY
