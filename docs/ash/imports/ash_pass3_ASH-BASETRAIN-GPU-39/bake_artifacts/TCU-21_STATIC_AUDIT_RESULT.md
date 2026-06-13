# TCU-21 Static Audit Result

## Status

`PASS_STATIC_TCU_21_WITH_NATIVE_TESTS_NOT_RUN`

## Checks

- `PASS` required_files_present
- `PASS` ash_core_module_exported
- `PASS` orchestrator_module_exported
- `PASS` report_status_pass: `PASS_TCU_21_TENSORCUBE_HEALTH_RECOMMENDATION_REVIEW_RECEIPT`
- `PASS` queue_chain_valid: `True`
- `PASS` receipt_policy_candidate_allowed: `True`
- `PASS` runtime_mutation_allowed_false: `(False, False)`
- `PASS` backend_config_mutation_allowed_false: `(False, False)`
- `PASS` lora_attach_detach_allowed_false: `(False, False)`
- `PASS` safe_tensor_mode_apply_allowed_false: `(False, False)`
- `WARN` cargo_available
- `WARN` rustc_available

## Native test note

This container does not provide `cargo` or `rustc`; Rust-native tests were added but not executed in this bake environment.
