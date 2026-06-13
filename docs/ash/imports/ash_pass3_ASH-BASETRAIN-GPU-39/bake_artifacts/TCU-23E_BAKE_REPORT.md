# TCU-23E Bake Report

## Commit

`TCU-23E — TensorCube 8x8 MicroTile Readback-Free Timing Probe / Benchmark Guard`

## Base SSOT

`ash_pass3_TCU-23D_tensorcube_8x8_microtile_native_dispatch_readback_telemetry_baked.zip`

## Added files

```text
crates/burn_webgpu_backend/src/tensorcube_atlas_microtile_timing_probe.rs

crates/burn_webgpu_backend/tests/tcu_23e_timing_probe_config_gate.rs
crates/burn_webgpu_backend/tests/tcu_23e_readback_free_probe_guard.rs
crates/burn_webgpu_backend/tests/tcu_23e_timing_sample_summary.rs
crates/burn_webgpu_backend/tests/tcu_23e_timestamp_query_feature_gate.rs
crates/burn_webgpu_backend/tests/tcu_23e_no_production_selection.rs

crates/orchestrator_local/src/tcu_23e_tensorcube_microtile_timing_probe_report.rs
crates/orchestrator_local/src/bin/tcu_23e_tensorcube_microtile_timing_probe_audit.rs
crates/orchestrator_local/tests/tcu_23e_tensorcube_microtile_timing_probe_report.rs

workspace/runtime/tensorcube/ash_tensorcube_microtile_timing_probe_config_latest.json
workspace/runtime/tensorcube/ash_tensorcube_microtile_vec4_timing_probe_latest.json
workspace/runtime/tensorcube/ash_tensorcube_microtile_workgroup_timing_probe_latest.json
workspace/runtime/tensorcube/ash_tensorcube_microtile_timing_probe_report_latest.json

acceptance_reports/TCU-23E_tensorcube_8x8_microtile_readback_free_timing_probe.md
bake_artifacts/TCU-23E_BAKE_REPORT.md
bake_artifacts/TCU-23E_STATIC_AUDIT_RESULT.md
```

## Modified files

```text
crates/burn_webgpu_backend/src/lib.rs
crates/orchestrator_local/src/lib.rs
```

## Seal

```text
Readback-free timing is performance observation only.
Correctness authority remains TCU-23B/23C/23D parity and readback telemetry.
```

## Native test status

`cargo` / `rustc` are unavailable in this container, so native Rust tests were not executed.
