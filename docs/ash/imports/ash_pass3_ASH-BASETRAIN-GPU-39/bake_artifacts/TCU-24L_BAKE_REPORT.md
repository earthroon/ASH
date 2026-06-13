# TCU-24L Bake Report

## Baked from

`ash_pass3_TCU-24K_qwave_runtime_guarded_backend_switch_smoke_apply_sandbox_baked.zip`

## Added

- `crates/burn_webgpu_backend/src/qwave_backend_rollback_ledger.rs`
- `crates/burn_webgpu_backend/tests/tcu_24l_qwave_rollback_ledger_config_gate.rs`
- `crates/burn_webgpu_backend/tests/tcu_24l_qwave_rollback_ledger_failure_classification.rs`
- `crates/burn_webgpu_backend/tests/tcu_24l_qwave_rollback_ledger_demotion_record.rs`
- `crates/burn_webgpu_backend/tests/tcu_24l_qwave_rollback_ledger_quarantine_record.rs`
- `crates/burn_webgpu_backend/tests/tcu_24l_qwave_rollback_ledger_no_runtime_mutation.rs`
- `crates/burn_webgpu_backend/tests/tcu_24l_qwave_rollback_ledger_operator_review.rs`
- `crates/orchestrator_local/src/tcu_24l_qwave_rollback_ledger_report.rs`
- `crates/orchestrator_local/src/bin/tcu_24l_qwave_rollback_ledger_audit.rs`
- `crates/orchestrator_local/tests/tcu_24l_qwave_rollback_ledger_report.rs`

## Runtime artifacts

- `workspace/runtime/tensorcube/ash_qwave_rollback_ledger_config_latest.json`
- `workspace/runtime/tensorcube/ash_qwave_rollback_failure_classification_latest.json`
- `workspace/runtime/tensorcube/ash_qwave_rollback_demotion_record_latest.json`
- `workspace/runtime/tensorcube/ash_qwave_rollback_quarantine_record_latest.json`
- `workspace/runtime/tensorcube/ash_qwave_rollback_operator_review_receipt_latest.json`
- `workspace/runtime/tensorcube/ash_qwave_rollback_ledger_report_latest.json`

## Native test status

Native Rust tests were not run in this container because `cargo`/`rustc` are unavailable.

Static seal: `PASS_STATIC_TCU_24L_WITH_NATIVE_TESTS_NOT_RUN`
