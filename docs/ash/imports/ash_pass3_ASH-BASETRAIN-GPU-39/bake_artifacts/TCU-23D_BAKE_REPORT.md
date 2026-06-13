# TCU-23D Bake Report

## Commit

`TCU-23D — TensorCube 8x8 MicroTile Native Dispatch / Readback Telemetry Seal`

## Base SSOT

`ash_pass3_TCU-23C_tensorcube_8x8_microtile_native_wgpu_smoke_baked.zip`

## Added Files

```text
crates/burn_webgpu_backend/src/tensorcube_atlas_microtile_dispatch_telemetry.rs
crates/burn_webgpu_backend/tests/tcu_23d_dispatch_telemetry_config_gate.rs
crates/burn_webgpu_backend/tests/tcu_23d_dispatch_phase_event_seal.rs
crates/burn_webgpu_backend/tests/tcu_23d_readback_telemetry_shape.rs
crates/burn_webgpu_backend/tests/tcu_23d_telemetry_notrun_status.rs
crates/burn_webgpu_backend/tests/tcu_23d_no_benchmark_or_production_dispatch.rs
crates/orchestrator_local/src/tcu_23d_tensorcube_microtile_dispatch_telemetry_report.rs
crates/orchestrator_local/src/bin/tcu_23d_tensorcube_microtile_dispatch_telemetry_audit.rs
crates/orchestrator_local/tests/tcu_23d_tensorcube_microtile_dispatch_telemetry_report.rs
workspace/runtime/tensorcube/ash_tensorcube_microtile_dispatch_telemetry_config_latest.json
workspace/runtime/tensorcube/ash_tensorcube_microtile_dispatch_phase_telemetry_latest.json
workspace/runtime/tensorcube/ash_tensorcube_microtile_readback_telemetry_latest.json
workspace/runtime/tensorcube/ash_tensorcube_microtile_dispatch_telemetry_report_latest.json
acceptance_reports/TCU-23D_tensorcube_8x8_microtile_native_dispatch_readback_telemetry.md
bake_artifacts/TCU-23D_BAKE_REPORT.md
bake_artifacts/TCU-23D_STATIC_AUDIT_RESULT.md
```

## Modified Files

```text
crates/burn_webgpu_backend/src/lib.rs
crates/orchestrator_local/src/lib.rs
```

## Sealed Policy

```text
TCU-23D telemetry is observational.
It does not optimize, promote, benchmark, or mutate runtime behavior.
```

## Static Status

`PASS_STATIC_TCU_23D_WITH_NATIVE_TESTS_NOT_RUN`
