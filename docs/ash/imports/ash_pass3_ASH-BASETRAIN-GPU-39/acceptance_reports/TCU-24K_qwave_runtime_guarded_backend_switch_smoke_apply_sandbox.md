# TCU-24K — QWave Runtime Guarded Backend Switch Smoke / Apply Sandbox

## SSOT

Baked from `ash_pass3_TCU-24J_qwave_backend_apply_candidate_current_pointer_guard_baked.zip`.

## Acceptance Criteria

- TCU-24J `QWaveBackendApplyCandidateReport` is consumed as the source.
- A sandbox/shadow runtime slot is created for the proposed backend pointer only.
- The real `current_backend_pointer` remains unchanged.
- The real active backend remains unchanged.
- The sandbox backend pointer may resolve the proposed backend for smoke only.
- The rollback backend pointer remains `LegacyElevenBuffer`.
- Adapter-unavailable smoke is recorded as `SmokeNotRunAdapterUnavailable`, not as a contract failure.
- Smoke failure is demotable and bound to rollback readiness.
- Persistent runtime apply is forbidden.
- Production default mutation is forbidden.
- Backend policy mutation is forbidden.
- TensorCube MatMul replacement and subgroup fast path remain disabled.

## Result

PASS_STATIC_TCU_24K_WITH_NATIVE_TESTS_NOT_RUN
