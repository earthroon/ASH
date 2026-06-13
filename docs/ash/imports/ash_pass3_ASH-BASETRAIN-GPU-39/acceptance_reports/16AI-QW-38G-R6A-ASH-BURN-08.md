# 16AI-QW-38G-R6A-ASH-BURN-08

## Title
Burn Production Backend Default Promotion Gate / No Silent Default Switch Seal

## SSOT
Production backend default promotion gate creates an explicit switch gate only. It binds shadow commit, shadow review, default-switch preflight, and rollback plan evidence, but it cannot silently switch defaults, mutate active backend pointer, execute production forward, mutate runtime sequence, or emit production output.

## Receipt
```json
{
  "preflight_pass": true,
  "preflight_warn": false,
  "preflight_fail": false,
  "fallback_pressure_within_promotion_limit": true,
  "sandbox_failure_detected": false,
  "shadow_review_status_pass": true,
  "shadow_review_status_warn": false,
  "shadow_review_status_fail": false,
  "burn07_shadow_commit_required": true,
  "burn07_shadow_commit_respected": true,
  "burn06_sandbox_execution_required": true,
  "burn06_sandbox_execution_respected": true,
  "backend_shadow_commit_executed": true,
  "shadow_commit_receipt_created": true,
  "shadow_commit_receipt_digest": "a40edfe69f4bdf86bf560d0c22a1b2a0b2f64f4c52ecef6ae3ed1f541efe8e8c",
  "shadow_commit_receipt_digest_bound": true,
  "shadow_backend_route_digest": "532ce84f33214d482ef7f2c48637309a839b40f8dc2fce82b2bdfd013c757aa4",
  "shadow_backend_route_digest_bound": true,
  "shadow_review_created": true,
  "shadow_review_digest": "af5af28a780547dafc2d34dca61ddb37f599211b8a516d126d56ce68a9e0b980",
  "shadow_review_digest_bound": true,
  "shadow_review_scheduled_for_production_gate": true,
  "shadow_review_auto_promoted_to_production_gate": false,
  "source_is_real_burn07_shadow_receipt": true,
  "source_is_mock_report": false,
  "source_is_fixture_report": false,
  "source_is_synthetic": false,
  "production_default_promotion_gate_allowed": true,
  "production_default_promotion_gate_created": true,
  "production_default_promotion_gate_digest": "f521d2945e388fdfc8d4867d3dbc5fde6cda1b459b04678ec03222a965248078",
  "production_default_promotion_gate_digest_bound": true,
  "gate_source_matches_shadow_commit": true,
  "gate_source_matches_shadow_review": true,
  "gate_source_matches_sandbox_result": true,
  "explicit_operator_default_switch_required": true,
  "default_switch_operator_identity_required": true,
  "default_switch_timestamp_required": true,
  "target_production_backend_required": true,
  "gate_bound_as_promotion_gate": true,
  "gate_bound_as_default_switch": false,
  "gate_bound_as_active_backend_pointer": false,
  "gate_bound_as_production_output": false,
  "default_switch_preflight_required": true,
  "default_switch_preflight_created": true,
  "default_switch_preflight_digest": "695a9e99109496bbebf3c52c0d88637955f939fd56376c809365a79cfbd537cb",
  "default_switch_preflight_digest_bound": true,
  "shadow_backend_route_digest_bound_for_preflight": true,
  "target_production_backend_digest": "7c7cc3db9d1e38c9e4ab8760d92f70591aca956728ab5a99ac7941c16fb97f1f",
  "target_production_backend_digest_bound": true,
  "fallback_pressure_digest": "81add87abef0fc6452cb1112027b5a51450208136a65a80b08759e7e9a66d56f",
  "fallback_pressure_digest_bound": true,
  "rollback_plan_required": true,
  "rollback_plan_created": true,
  "rollback_plan_digest": "99367427171cebebe462dc3437dfeb3e94d75a6de52f02a95141a393c71db66b",
  "rollback_plan_digest_bound": true,
  "silent_default_switch_allowed": false,
  "silent_default_switch_executed": false,
  "implicit_default_switch_allowed": false,
  "implicit_default_switch_executed": false,
  "automatic_default_switch_allowed": false,
  "automatic_default_switch_executed": false,
  "default_switch_inferred_from_shadow_commit": false,
  "default_switch_inferred_from_shadow_review": false,
  "default_switch_inferred_from_preflight_pass": false,
  "default_switch_inferred_from_gate_created": false,
  "default_switch_requires_explicit_operator_action": true,
  "default_switch_requires_receipt_stage": true,
  "production_default_change_allowed": false,
  "production_default_changed": false,
  "backend_default_promotion_allowed": false,
  "backend_default_promoted": false,
  "production_commit_allowed": false,
  "production_commit_executed": false,
  "active_backend_pointer_mutation_allowed": false,
  "active_backend_pointer_mutated": false,
  "backend_route_promotion_allowed": false,
  "backend_route_promotion_executed": false,
  "qwave_backend_active_route_mutated": false,
  "qwave_backend_production_route_mutated": false,
  "production_gate_inferred_as_default_change": false,
  "preflight_inferred_as_default_change": false,
  "rollback_target_previous_backend_digest": "f8eb974e037749739f4c199bda334c18ddd6895fcb139387bdd0644b398b86c7",
  "rollback_target_previous_backend_digest_bound": true,
  "rollback_target_shadow_backend_digest_bound": true,
  "rollback_ledger_mutation_allowed": false,
  "rollback_ledger_mutated": false,
  "rollback_entry_creation_allowed": false,
  "rollback_entry_created": false,
  "rollback_plan_bound_as_plan": true,
  "rollback_plan_bound_as_ledger_entry": false,
  "production_forward_execution_allowed": false,
  "production_forward_execution_triggered": false,
  "production_inference_execution_allowed": false,
  "production_inference_execution_triggered": false,
  "runtime_apply_executed": false,
  "runtime_sequence_mutated": false,
  "runtime_token_append_executed": false,
  "runtime_output_created": false,
  "production_output_emit_allowed": false,
  "production_output_emitted": false,
  "final_response_emit_allowed": false,
  "final_response_emitted": false,
  "promotion_gate_output_visible_externally": false,
  "promotion_gate_committed_to_runtime": false,
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
  "receipt_key": "ash-burn08-production-backend-default-promotion-gate:2c1b219d324724c185d84f399389bae9303f8a76d20ceb1bcf723294b347a804",
  "receipt_digest": "3f70cba04f2f551a591e87fc80cc0879cd2f930fcfed34827bdc5bb6175e5e7e",
  "status": "PASS_ASH_BURN_08_PRODUCTION_BACKEND_DEFAULT_PROMOTION_GATE_NO_SILENT_DEFAULT_SWITCH",
  "verdict": "PASS_ASH_BURN_08_PRODUCTION_BACKEND_DEFAULT_PROMOTION_GATE_NO_SILENT_DEFAULT_SWITCH"
}
```

## Positive cases
- CASE-POS-ASH-BURN-08-00: BURN-07 shadow commit present, production default promotion gate created, production default changed false -> PASS.
- CASE-POS-ASH-BURN-08-01: shadow review digest bound, rollback plan digest bound, default switch preflight created, silent switch false -> PASS.
- CASE-POS-ASH-BURN-08-02: gate bound as promotion gate, not default switch, not active backend pointer, not production output -> PASS.
- CASE-POS-ASH-BURN-08-03: operator switch required, production default not changed -> PASS_WITH_WARN.

## Warn cases
- WARN_ASH_BURN_08_PRODUCTION_GATE_CREATED_OPERATOR_SWITCH_REQUIRED: production gate exists and explicit operator switch is required before default change.
- WARN_ASH_BURN_08_FALLBACK_PRESSURE_REVIEW_REQUIRED_NO_DEFAULT_SWITCH: fallback pressure requires review and default switch remains sealed.

## Negative cases
- FAIL_BURN07_SHADOW_COMMIT_MISSING
- FAIL_BURN06_SANDBOX_EXECUTION_MISSING
- FAIL_SHADOW_REVIEW_DIGEST_MISSING
- FAIL_SHADOW_BACKEND_ROUTE_DIGEST_MISSING
- FAIL_PRODUCTION_DEFAULT_PROMOTION_GATE_NOT_CREATED
- FAIL_PRODUCTION_GATE_DIGEST_MISSING
- FAIL_DEFAULT_SWITCH_PREFLIGHT_MISSING
- FAIL_ROLLBACK_PLAN_MISSING
- FAIL_GATE_PROMOTED_TO_DEFAULT_SWITCH
- FAIL_GATE_PROMOTED_TO_ACTIVE_BACKEND_POINTER
- FAIL_GATE_PROMOTED_TO_PRODUCTION_OUTPUT
- FAIL_SILENT_DEFAULT_SWITCH_EXECUTED
- FAIL_IMPLICIT_DEFAULT_SWITCH_EXECUTED
- FAIL_AUTOMATIC_DEFAULT_SWITCH_EXECUTED
- FAIL_DEFAULT_SWITCH_INFERRED_FROM_SHADOW_COMMIT
- FAIL_DEFAULT_SWITCH_INFERRED_FROM_SHADOW_REVIEW
- FAIL_DEFAULT_SWITCH_INFERRED_FROM_PREFLIGHT_PASS
- FAIL_DEFAULT_SWITCH_INFERRED_FROM_GATE_CREATED
- FAIL_PRODUCTION_DEFAULT_CHANGED_TOO_EARLY
- FAIL_BACKEND_DEFAULT_PROMOTED_TOO_EARLY
- FAIL_PRODUCTION_COMMIT_EXECUTED_TOO_EARLY
- FAIL_ACTIVE_BACKEND_POINTER_MUTATED_TOO_EARLY
- FAIL_BACKEND_ROUTE_PROMOTED_TOO_EARLY
- FAIL_ROLLBACK_LEDGER_MUTATED_TOO_EARLY
- FAIL_ROLLBACK_ENTRY_CREATED_TOO_EARLY
- FAIL_PRODUCTION_FORWARD_EXECUTED_TOO_EARLY
- FAIL_PRODUCTION_INFERENCE_EXECUTED_TOO_EARLY
- FAIL_RUNTIME_APPLY_EXECUTED_TOO_EARLY
- FAIL_RUNTIME_SEQUENCE_MUTATED_TOO_EARLY
- FAIL_RUNTIME_TOKEN_APPEND_EXECUTED_TOO_EARLY
- FAIL_PRODUCTION_OUTPUT_EMITTED_TOO_EARLY
- FAIL_FINAL_RESPONSE_EMITTED_TOO_EARLY
- FAIL_CARGO_DEPENDENCY_REWRITTEN_TOO_EARLY
- FAIL_VENDOR_FEATURE_ACTIVATED_TOO_EARLY
- FAIL_VENDOR_SOURCE_MUTATED_TOO_EARLY
