# 16AI-QW-38G-R6A-ASH-BURN-06

## Title
Burn Backend Apply Sandbox Execution / No Production Commit Seal

## SSOT
Backend apply sandbox execution validates the BURN-05 route candidate in isolation. Sandbox forward/inference/tensor probes are allowed only inside the sandbox receipt. Production commit, production default backend change, active backend pointer mutation, shadow commit, rollback ledger mutation, runtime output, and final response emission remain sealed off.

## Receipt
```json
{
  "burn05_route_candidate_required": true,
  "burn05_route_candidate_respected": true,
  "burn04_strict_probe_required": true,
  "burn04_strict_probe_respected": true,
  "backend_route_promotion_candidate_created": true,
  "candidate_backend_id_present": true,
  "candidate_backend_id_digest": "d8072c9ecdf787cb2284f74db91e84744a804b50c8bddf92228b554cc31a0172",
  "candidate_backend_id_digest_bound": true,
  "candidate_backend_route_digest": "3e923b56a85c36f14535b3008fc2df0a1c3eb5999ab1186c6c274754c94cf175",
  "candidate_backend_route_digest_bound": true,
  "candidate_bound_as_route_candidate": true,
  "candidate_bound_as_active_backend": false,
  "candidate_bound_as_production_default": false,
  "source_is_real_burn05_candidate": true,
  "source_is_mock_report": false,
  "source_is_fixture_report": false,
  "source_is_synthetic": false,
  "backend_apply_sandbox_allowed": true,
  "backend_apply_sandbox_executed": true,
  "sandbox_backend_route_bound": true,
  "sandbox_backend_route_digest": "ad2572a3194889bef31cf7d00380b05f9bbd441109b109a1e88839c1b12a1079",
  "sandbox_backend_route_digest_bound": true,
  "sandbox_execution_plan_present": true,
  "sandbox_execution_plan_digest": "3aced287f8fb436dce236229beca89bcf8a6431afb1ddc7a0314e3125d5529a5",
  "sandbox_execution_plan_digest_bound": true,
  "sandbox_execution_receipt_created": true,
  "sandbox_execution_receipt_digest": "4c4e2c620035f68176c6b7ab7aa4c2bb6b2561001f4b94f62c82e125892d2b13",
  "sandbox_execution_receipt_digest_bound": true,
  "sandbox_result_digest": "5660a741637e98fa73b94be3bbc61a6824afc959d7414c86a12504cd0b775a0e",
  "sandbox_result_digest_bound": true,
  "sandbox_result_matches_candidate_route": true,
  "sandbox_result_matches_burn04_probe": true,
  "sandbox_result_matches_backend_policy": true,
  "sandbox_forward_probe_allowed": true,
  "sandbox_forward_probe_executed": true,
  "sandbox_inference_probe_allowed": true,
  "sandbox_inference_probe_executed": true,
  "sandbox_tensor_probe_allowed": true,
  "sandbox_tensor_probe_executed": true,
  "sandbox_tensor_shape_digest_bound": true,
  "sandbox_tensor_dtype_digest_bound": true,
  "sandbox_backend_device_digest_bound": true,
  "sandbox_backend_queue_digest_bound": true,
  "sandbox_forward_result_digest": "61fcb1dea977d79b3706a339cad16af2367e38b4b2a5346753ce6c5605f3a10e",
  "sandbox_forward_result_digest_bound": true,
  "sandbox_forward_committed_to_runtime": false,
  "sandbox_forward_promoted_to_production": false,
  "fallback_pressure_probe_allowed": true,
  "fallback_pressure_probe_executed": true,
  "cpu_fallback_detected": false,
  "host_upload_fallback_detected": false,
  "backend_route_fallback_detected": false,
  "fallback_pressure_digest": "d1585574535e6da75639f68539b1956d8d698e994f5ca5bb9265925afa9fefaa",
  "fallback_pressure_digest_bound": true,
  "fallback_pressure_within_sandbox_limit": true,
  "fallback_pressure_promoted_to_route_failure": false,
  "sandbox_failure_detected": false,
  "sandbox_failure_digest": "f71070a902623cc5db80bd266e471eb50479da8ac064b355cf2a5eccae6453b3",
  "sandbox_failure_digest_bound": true,
  "sandbox_failure_committed_to_rollback_ledger": false,
  "production_commit_allowed": false,
  "production_commit_executed": false,
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
  "sandbox_result_inferred_as_production_commit": false,
  "backend_shadow_commit_allowed": false,
  "backend_shadow_commit_executed": false,
  "shadow_commit_receipt_created": false,
  "rollback_ledger_mutation_allowed": false,
  "rollback_ledger_mutated": false,
  "rollback_entry_created": false,
  "sandbox_result_scheduled_for_shadow_review": true,
  "sandbox_result_committed_to_shadow": false,
  "shadow_commit_inferred_from_sandbox": false,
  "rollback_ledger_inferred_from_sandbox": false,
  "runtime_apply_executed": false,
  "runtime_sequence_mutated": false,
  "runtime_token_append_executed": false,
  "runtime_output_created": false,
  "production_output_emit_allowed": false,
  "production_output_emitted": false,
  "final_response_emit_allowed": false,
  "final_response_emitted": false,
  "sandbox_output_visible_externally": false,
  "sandbox_output_committed_to_runtime": false,
  "cargo_dependency_rewrite_allowed": false,
  "cargo_dependency_rewritten": false,
  "cargo_feature_activation_allowed": false,
  "cargo_feature_activated": false,
  "burn_raw_access_local_default_change_allowed": false,
  "burn_raw_access_local_default_changed": false,
  "vendor_source_mutation_allowed": false,
  "vendor_source_mutated": false,
  "upstream_real_insert_apply_allowed": false,
  "upstream_real_insert_applied": false,
  "lockfile_mutation_allowed": false,
  "lockfile_mutated": false,
  "model_weight_mutated": false,
  "optimizer_step_executed": false,
  "delta_stack_append_executed": false,
  "receipt_key": "ash-burn06-backend-apply-sandbox-execution:1c7bcfaaeed8dda6fe0f8509e433eceb1993b91863afef925a17a1826f503eb6",
  "receipt_digest": "0349598763c1ab33e6b24eb3d7853cdd8e89de75fed9d47d5ecb8b8b612c6091",
  "status": "PASS_ASH_BURN_06_BACKEND_APPLY_SANDBOX_EXECUTION_NO_PRODUCTION_COMMIT",
  "verdict": "PASS_ASH_BURN_06_BACKEND_APPLY_SANDBOX_EXECUTION_NO_PRODUCTION_COMMIT"
}
```

## Positive cases
- CASE-POS-ASH-BURN-06-00: BURN-05 route candidate present, sandbox execution receipt created, production commit false -> PASS.
- CASE-POS-ASH-BURN-06-01: sandbox forward/inference/tensor probe executed, sandbox result digest bound, runtime output false -> PASS.
- CASE-POS-ASH-BURN-06-02: fallback pressure probe executed, within sandbox limit, no production default change -> PASS.
- CASE-POS-ASH-BURN-06-03: sandbox result scheduled for shadow review, shadow commit false, rollback ledger mutation false -> PASS_WITH_WARN.

## Warn cases
- WARN_ASH_BURN_06_SANDBOX_RESULT_SHADOW_REVIEW_REQUIRED: sandbox result exists and shadow review is required, but shadow commit is not executed in BURN-06.
- WARN_ASH_BURN_06_SANDBOX_FALLBACK_PRESSURE_DETECTED_NO_PRODUCTION_COMMIT: fallback pressure is detected outside the sandbox limit and production commit remains sealed.

## Negative cases
- FAIL_BURN05_ROUTE_CANDIDATE_MISSING
- FAIL_BURN04_STRICT_PROBE_MISSING
- FAIL_CANDIDATE_BACKEND_ROUTE_DIGEST_MISSING
- FAIL_SANDBOX_EXECUTION_NOT_EXECUTED
- FAIL_SANDBOX_EXECUTION_RECEIPT_MISSING
- FAIL_SANDBOX_RESULT_DIGEST_MISSING
- FAIL_SANDBOX_RESULT_MISMATCH_CANDIDATE_ROUTE
- FAIL_SANDBOX_RESULT_MISMATCH_BURN04_PROBE
- FAIL_SANDBOX_RESULT_MISMATCH_BACKEND_POLICY
- FAIL_SANDBOX_FORWARD_PROBE_NOT_EXECUTED
- FAIL_SANDBOX_INFERENCE_PROBE_NOT_EXECUTED
- FAIL_SANDBOX_TENSOR_PROBE_NOT_EXECUTED
- FAIL_SANDBOX_EXECUTION_FAILED_NO_PRODUCTION_COMMIT
- FAIL_SANDBOX_PROMOTED_TO_PRODUCTION_COMMIT
- FAIL_SANDBOX_PROMOTED_TO_PRODUCTION_DEFAULT
- FAIL_SANDBOX_PROMOTED_TO_ACTIVE_BACKEND_POINTER
- FAIL_SANDBOX_PROMOTED_TO_BACKEND_ROUTE
- FAIL_BACKEND_DEFAULT_PROMOTED_TOO_EARLY
- FAIL_ACTIVE_BACKEND_POINTER_MUTATED_TOO_EARLY
- FAIL_PRODUCTION_DEFAULT_CHANGED_TOO_EARLY
- FAIL_BACKEND_ROUTE_PROMOTED_TOO_EARLY
- FAIL_BACKEND_SHADOW_COMMIT_EXECUTED_TOO_EARLY
- FAIL_ROLLBACK_LEDGER_MUTATED_TOO_EARLY
- FAIL_SANDBOX_FORWARD_COMMITTED_TO_RUNTIME
- FAIL_SANDBOX_FORWARD_PROMOTED_TO_PRODUCTION
- FAIL_RUNTIME_APPLY_EXECUTED_TOO_EARLY
- FAIL_RUNTIME_SEQUENCE_MUTATED_TOO_EARLY
- FAIL_RUNTIME_TOKEN_APPEND_EXECUTED_TOO_EARLY
- FAIL_PRODUCTION_OUTPUT_EMITTED_TOO_EARLY
- FAIL_FINAL_RESPONSE_EMITTED_TOO_EARLY
- FAIL_CARGO_DEPENDENCY_REWRITTEN_TOO_EARLY
- FAIL_VENDOR_FEATURE_ACTIVATED_TOO_EARLY
- FAIL_VENDOR_SOURCE_MUTATED_TOO_EARLY
