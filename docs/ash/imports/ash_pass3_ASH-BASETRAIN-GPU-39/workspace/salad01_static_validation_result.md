# SALAD-01 Static Validation Result

- Patch: `16AI-QW-38G-R6A-SALAD-01`
- Adjudication: `PASS_STATIC_BAKE_PENDING_LOCAL_RUNTIME_REPLAY`
- Cargo check: not executed (`cargo/rustc unavailable in bake container`)

## Checks

- PASS: `decode_stability_module_present`
- PASS: `safe_profile_constant_present`
- PASS: `greedy_profile_constant_present`
- PASS: `word_salad_audit_present`
- PASS: `ash_core_exports_decode_stability`
- PASS: `derive_gate_applies_safe_policy`
- PASS: `gate_audit_exports_profile`
- PASS: `runtime_ashgate_event_exports_profile`
- PASS: `decision_policy_uses_stable_profile`
- PASS: `profile_registry_artifact_present`
- PASS: `receipt_artifact_present`
- PASS: `comparison_artifact_present`
- FAIL: `cargo_available`
- FAIL: `rustc_available`
- PASS: `no_model_artifact_changes_listed`

## Model Mutation

- model artifact changes listed: `0`
