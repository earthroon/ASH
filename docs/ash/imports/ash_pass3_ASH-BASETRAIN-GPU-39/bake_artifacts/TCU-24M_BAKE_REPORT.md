# TCU-24M Bake Report

Baked from TCU-24L SSOT ZIP.

## Added
- `crates/burn_webgpu_backend/src/qwave_backend_recovery_candidate.rs`
- `crates/orchestrator_local/src/tcu_24m_qwave_recovery_candidate_report.rs`
- `crates/orchestrator_local/src/bin/tcu_24m_qwave_recovery_candidate_audit.rs`
- TCU-24M backend tests
- TCU-24M orchestrator report test
- Runtime JSON artifacts
- Acceptance report

## Contract
Recovery candidate may be created. Quarantine release may be proposed. Quarantine must not be released.

## Native test state
Cargo/rustc native execution was not available in the bake environment; static audit was performed instead.
