# TCU-24M — QWave Backend Recovery / Quarantine Release Candidate Acceptance Report

## SSOT
- Source: TCU-24L `QWaveBackendRollbackLedgerReport`.
- New module: `crates/burn_webgpu_backend/src/qwave_backend_recovery_candidate.rs`.
- Role: create operator-reviewed recovery and quarantine release candidate records.

## Accepted scope
- Reads failure kind, severity, demotion action, quarantine record, and health score from TCU-24L.
- Creates operator recovery review receipt.
- Creates revalidation evidence receipt for new parity and new sandbox smoke evidence.
- Creates health recovery candidate without persisting health score.
- Creates quarantine release candidate without releasing quarantine.
- Keeps fallback and rollback backend pointer as `LegacyElevenBuffer`.

## Explicitly forbidden
- No quarantine release execution.
- No health score persistence.
- No runtime apply.
- No current backend pointer mutation.
- No active backend mutation.
- No production default change.
- No direct replacement.
- No backend policy mutation.
- No fastest candidate auto apply.
- No TensorCube MatMul replacement.
- No subgroup fast path.

## Runtime artifacts
- `workspace/runtime/tensorcube/ash_qwave_recovery_candidate_config_latest.json`
- `workspace/runtime/tensorcube/ash_qwave_recovery_operator_review_receipt_latest.json`
- `workspace/runtime/tensorcube/ash_qwave_recovery_revalidation_evidence_latest.json`
- `workspace/runtime/tensorcube/ash_qwave_recovery_health_candidate_latest.json`
- `workspace/runtime/tensorcube/ash_qwave_quarantine_release_candidate_latest.json`
- `workspace/runtime/tensorcube/ash_qwave_recovery_candidate_report_latest.json`

## Static status
`PASS_STATIC_TCU_24M_WITH_NATIVE_TESTS_NOT_RUN`
