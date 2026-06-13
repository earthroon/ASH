# TCU-24K Bake Report

Baked from: `ash_pass3_TCU-24J_qwave_backend_apply_candidate_current_pointer_guard_baked.zip`

Added files:
- `crates/burn_webgpu_backend/src/qwave_backend_apply_sandbox.rs`
- `crates/orchestrator_local/src/tcu_24k_qwave_apply_sandbox_report.rs`
- `crates/orchestrator_local/src/bin/tcu_24k_qwave_apply_sandbox_audit.rs`
- TCU-24K tests for config gate, source candidate gate, runtime slot, smoke receipt, pointer non-mutation, and rollback readiness
- runtime/tensorcube JSON artifacts
- acceptance report and static audit

Result: PASS_STATIC_TCU_24K_WITH_NATIVE_TESTS_NOT_RUN

Native cargo tests were not run in this container.
