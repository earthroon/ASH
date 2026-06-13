# TCU-24N — QWave Guarded Apply Attempt Preflight / Recovery Candidate Re-entry Gate

## SSOT

- Source ZIP: `ash_pass3_TCU-24M_qwave_backend_recovery_quarantine_release_candidate_baked.zip`
- Source module: `crates/burn_webgpu_backend/src/qwave_backend_recovery_candidate.rs`
- New module: `crates/burn_webgpu_backend/src/qwave_backend_apply_preflight.rs`

## Confirmed scope

TCU-24N consumes `QWaveBackendRecoveryCandidateReport` from TCU-24M and creates:

1. `QWaveBackendApplyPreflightSourceRecoveryGate`
2. `QWaveBackendApplyPreflightPointerGuard`
3. `QWaveBackendApplyPreflightRollbackReceipt`
4. `QWaveBackendRecoveryReEntryGateRecord`
5. `QWaveBackendApplyAttemptPreflightRecord`
6. `QWaveBackendApplyPreflightReport`

## Sealed invariants

- `quarantine_released = false`
- `health_score_persistence_allowed = false`
- `apply_attempt_execution_allowed = false`
- `runtime_apply_allowed = false`
- `current_backend_pointer_mutation_allowed = false`
- `active_backend_mutation_allowed = false`
- `production_default_change_allowed = false`
- `direct_replacement_allowed = false`
- `backend_policy_mutation_allowed = false`
- `fastest_candidate_auto_apply_allowed = false`
- `tensorcube_matmul_replacement_enabled = false`
- `subgroup_fast_path_enabled = false`

## Runtime artifacts

- `workspace/runtime/tensorcube/ash_qwave_apply_preflight_config_latest.json`
- `workspace/runtime/tensorcube/ash_qwave_apply_preflight_source_recovery_gate_latest.json`
- `workspace/runtime/tensorcube/ash_qwave_apply_preflight_reentry_gate_latest.json`
- `workspace/runtime/tensorcube/ash_qwave_apply_preflight_pointer_guard_latest.json`
- `workspace/runtime/tensorcube/ash_qwave_apply_preflight_rollback_preflight_latest.json`
- `workspace/runtime/tensorcube/ash_qwave_apply_preflight_report_latest.json`

## Acceptance criteria

1. TCU-24M `QWaveBackendRecoveryCandidateReport` is used as source.
2. Source release candidate readiness is checked.
3. Source revalidation status must be `Passed` for ready path.
4. Operator recovery approval must be present for ready path.
5. Health recovery candidate must exist for ready path.
6. `quarantine_released` must remain false.
7. `health_score_persistence_allowed` must remain false.
8. Candidate backend pointer must come from source release candidate.
9. Fallback backend pointer must be `LegacyElevenBuffer`.
10. Rollback backend pointer must be `LegacyElevenBuffer`.
11. Source recovery gate receipt is created.
12. Current pointer guard receipt is created.
13. Rollback preflight receipt is created.
14. Recovery re-entry gate record is created.
15. Guarded apply attempt preflight record is created.
16. `preflight_ready` may be true.
17. `apply_attempt_execution_allowed` must remain false.
18. `quarantine_release_execution_allowed` must remain false.
19. Runtime apply is forbidden.
20. Current backend pointer mutation is forbidden.
21. Active backend mutation is forbidden.
22. Production default mutation is forbidden.
23. Backend policy mutation is forbidden.
24. TensorCube MatMul replacement is not enabled.
25. Runtime JSON artifacts are generated.

## Result

`PASS_STATIC_TCU_24N_WITH_NATIVE_TESTS_NOT_RUN`

Native Rust tests were not executed in this environment because `cargo` / `rustc` are unavailable.
