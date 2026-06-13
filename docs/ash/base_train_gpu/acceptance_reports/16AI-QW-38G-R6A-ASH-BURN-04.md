# 16AI-QW-38G-R6A-ASH-BURN-04

## Title
Burn Same Device Raw Bridge Strict Probe / No Backend Default Promotion Seal

## SSOT
Same-device raw bridge strict probe validates device/queue parity and identity evidence only. It does not promote backend default, mutate active backend pointer, trigger forward execution, or emit output.

## Receipt
```json
{
  "patch_id": "16AI-QW-38G-R6A-ASH-BURN-04",
  "title": "Burn Same Device Raw Bridge Strict Probe / No Backend Default Promotion Seal",
  "burn03_raw_handle_evidence_required": true,
  "burn03_raw_handle_evidence_respected": true,
  "burn02_alignment_candidate_required": true,
  "burn02_alignment_candidate_respected": true,
  "raw_handle_extraction_contract_bound": true,
  "backend_device_handle_contract_bound": true,
  "backend_queue_handle_contract_bound": true,
  "same_device_bridge_strict_probe_allowed": true,
  "same_device_bridge_strict_probe_executed": true,
  "raw_handle_extraction_probe_allowed": true,
  "raw_handle_extraction_probe_executed": true,
  "backend_device_probe_bound": true,
  "backend_queue_probe_bound": true,
  "backend_device_queue_parity_checked": true,
  "backend_device_queue_parity_digest_bound": true,
  "adapter_identity_checked": true,
  "adapter_identity_digest_bound": true,
  "device_identity_checked": true,
  "device_identity_digest_bound": true,
  "queue_identity_checked": true,
  "queue_identity_digest_bound": true,
  "probe_result_digest_bound": true,
  "generation_alignment_required": true,
  "generation_alignment_applied_for_probe": true,
  "generation_alignment_applied_as_source_mutation": false,
  "raw_bridge_generation_matches_probe_contract": true,
  "vendor_generation_matches_probe_contract": true,
  "probe_only_raw_handle_borrow_executed": true,
  "raw_handle_borrow_materialized_for_probe": true,
  "raw_handle_borrow_committed_to_registry": false,
  "backend_device_live_bound_for_probe": true,
  "backend_queue_live_bound_for_probe": true,
  "backend_device_live_bound_as_runtime_route": false,
  "backend_queue_live_bound_as_runtime_route": false,
  "raw_handle_registry_mutated": false,
  "raw_handle_borrow_released_after_probe": true,
  "backend_default_promotion_allowed": false,
  "backend_default_promoted": false,
  "backend_route_promotion_executed": false,
  "active_backend_pointer_mutated": false,
  "production_default_changed": false,
  "strict_probe_inferred_as_backend_promotion": false,
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
  "receipt_key": "ash-burn04-same-device-raw-bridge-strict-probe:3c4a08084a965c102ae207067ded3502d0a6e07d335d3afb0edeade1f407f7cd",
  "receipt_digest": "6c0667c642037dcfa7426937b4b31fc1b0974d179cca031223c0f59174a51a91",
  "status": "PASS_ASH_BURN_04_SAME_DEVICE_RAW_BRIDGE_STRICT_PROBE_NO_BACKEND_DEFAULT_PROMOTION",
  "verdict": "PASS_ASH_BURN_04_SAME_DEVICE_RAW_BRIDGE_STRICT_PROBE_NO_BACKEND_DEFAULT_PROMOTION"
}
```

## Positive cases
- CASE-POS-ASH-BURN-04-00: BURN-03 raw handle evidence present, strict probe executed, backend default promoted false -> PASS.
- CASE-POS-ASH-BURN-04-01: probe-only raw handle borrow materialized, registry not mutated, borrow released -> PASS_WITH_WARN.
- CASE-POS-ASH-BURN-04-02: generation alignment applied for probe only, source mutation false -> PASS.
- CASE-POS-ASH-BURN-04-03: probe result digest bound, forward execution false, production output false -> PASS.

## Warn cases
- WARN_ASH_BURN_04_STRICT_PROBE_SUCCESS_ROUTE_PROMOTION_STILL_REQUIRED: probe digest exists but route promotion still separate.
- WARN_ASH_BURN_04_PROBE_ONLY_BORROW_RELEASE_REQUIRED: probe-only borrow must be released and not committed to registry.

## Negative cases
- FAIL_BURN03_RAW_HANDLE_EVIDENCE_MISSING
- FAIL_BURN02_ALIGNMENT_CANDIDATE_MISSING
- FAIL_SAME_DEVICE_STRICT_PROBE_NOT_EXECUTED
- FAIL_RAW_HANDLE_EXTRACTION_PROBE_NOT_EXECUTED
- FAIL_BACKEND_DEVICE_QUEUE_PARITY_NOT_CHECKED
- FAIL_ADAPTER_IDENTITY_NOT_CHECKED
- FAIL_DEVICE_IDENTITY_NOT_CHECKED
- FAIL_QUEUE_IDENTITY_NOT_CHECKED
- FAIL_PROBE_RESULT_DIGEST_MISSING
- FAIL_GENERATION_ALIGNMENT_APPLIED_AS_SOURCE_MUTATION
- FAIL_RAW_HANDLE_BORROW_COMMITTED_TO_REGISTRY
- FAIL_RAW_HANDLE_REGISTRY_MUTATED
- FAIL_RAW_HANDLE_BORROW_NOT_RELEASED_AFTER_PROBE
- FAIL_BACKEND_DEFAULT_PROMOTED_TOO_EARLY
- FAIL_BACKEND_ROUTE_PROMOTED_TOO_EARLY
- FAIL_ACTIVE_BACKEND_POINTER_MUTATED_TOO_EARLY
- FAIL_PRODUCTION_DEFAULT_CHANGED_TOO_EARLY
- FAIL_STRICT_PROBE_INFERRED_AS_BACKEND_PROMOTION
- FAIL_CARGO_DEPENDENCY_REWRITTEN_TOO_EARLY
- FAIL_VENDOR_FEATURE_ACTIVATED_TOO_EARLY
- FAIL_VENDOR_SOURCE_MUTATED_TOO_EARLY
- FAIL_UPSTREAM_REAL_INSERT_APPLIED_TOO_EARLY
- FAIL_EXECUTOR_REPLACED_TOO_EARLY
- FAIL_FORWARD_EXECUTION_TRIGGERED_TOO_EARLY
- FAIL_INFERENCE_EXECUTION_TRIGGERED_TOO_EARLY
- FAIL_TENSOR_DATA_MATERIALIZED_TOO_EARLY
- FAIL_TENSOR_BUFFER_WRITTEN_TOO_EARLY
- FAIL_RUNTIME_APPLY_EXECUTED_TOO_EARLY
- FAIL_RUNTIME_SEQUENCE_MUTATED_TOO_EARLY
- FAIL_RUNTIME_TOKEN_APPEND_EXECUTED_TOO_EARLY
- FAIL_PRODUCTION_OUTPUT_EMITTED_TOO_EARLY
- FAIL_FINAL_RESPONSE_EMITTED_TOO_EARLY
