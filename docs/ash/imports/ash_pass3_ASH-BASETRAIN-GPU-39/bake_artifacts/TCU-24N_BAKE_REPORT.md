# TCU-24N Bake Report

## Commit

`TCU-24N — Guarded Apply Attempt Preflight / Recovery Candidate Re-entry Gate`

## Source SSOT

`ash_pass3_TCU-24M_qwave_backend_recovery_quarantine_release_candidate_baked.zip`

## Files added

```text
crates/burn_webgpu_backend/src/qwave_backend_apply_preflight.rs
crates/burn_webgpu_backend/tests/tcu_24n_qwave_apply_preflight_config_gate.rs
crates/burn_webgpu_backend/tests/tcu_24n_qwave_apply_preflight_source_recovery_gate.rs
crates/burn_webgpu_backend/tests/tcu_24n_qwave_apply_preflight_reentry_gate.rs
crates/burn_webgpu_backend/tests/tcu_24n_qwave_apply_preflight_pointer_guard.rs
crates/burn_webgpu_backend/tests/tcu_24n_qwave_apply_preflight_rollback_preflight.rs
crates/burn_webgpu_backend/tests/tcu_24n_qwave_apply_preflight_no_apply_or_release.rs
crates/orchestrator_local/src/tcu_24n_qwave_apply_preflight_report.rs
crates/orchestrator_local/src/bin/tcu_24n_qwave_apply_preflight_audit.rs
crates/orchestrator_local/tests/tcu_24n_qwave_apply_preflight_report.rs
```

## Files updated

```text
crates/burn_webgpu_backend/src/lib.rs
crates/orchestrator_local/src/lib.rs
```

## Runtime JSON generated

```text
workspace/runtime/tensorcube/ash_qwave_apply_preflight_config_latest.json
workspace/runtime/tensorcube/ash_qwave_apply_preflight_source_recovery_gate_latest.json
workspace/runtime/tensorcube/ash_qwave_apply_preflight_reentry_gate_latest.json
workspace/runtime/tensorcube/ash_qwave_apply_preflight_pointer_guard_latest.json
workspace/runtime/tensorcube/ash_qwave_apply_preflight_rollback_preflight_latest.json
workspace/runtime/tensorcube/ash_qwave_apply_preflight_report_latest.json
```

## Sealed result

`PASS_STATIC_TCU_24N_WITH_NATIVE_TESTS_NOT_RUN`
