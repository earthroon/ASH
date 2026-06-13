# TCU-24F Bake Report

## Result

`PASS_STATIC_TCU_24F_WITH_NATIVE_TESTS_NOT_RUN`

## Added files

```text
crates/burn_webgpu_backend/src/qwave_atlas_telemetry.rs
crates/burn_webgpu_backend/tests/tcu_24f_qwave_atlas_telemetry_config_gate.rs
crates/burn_webgpu_backend/tests/tcu_24f_qwave_atlas_telemetry_event_chain.rs
crates/burn_webgpu_backend/tests/tcu_24f_qwave_atlas_readback_summary.rs
crates/burn_webgpu_backend/tests/tcu_24f_qwave_atlas_notrun_telemetry.rs
crates/burn_webgpu_backend/tests/tcu_24f_qwave_atlas_no_benchmark_or_selection.rs
crates/orchestrator_local/src/tcu_24f_qwave_atlas_telemetry_report.rs
crates/orchestrator_local/src/bin/tcu_24f_qwave_atlas_telemetry_audit.rs
crates/orchestrator_local/tests/tcu_24f_qwave_atlas_telemetry_report.rs
```

## Runtime artifacts

```text
workspace/runtime/tensorcube/ash_qwave_atlas_telemetry_config_latest.json
workspace/runtime/tensorcube/ash_qwave_atlas_dispatch_events_latest.json
workspace/runtime/tensorcube/ash_qwave_atlas_readback_summary_latest.json
workspace/runtime/tensorcube/ash_qwave_atlas_telemetry_report_latest.json
```

## Guard flags

```text
benchmark_mode_enabled = false
fastest_candidate_selection_allowed = false
production_default_changed = false
direct_replacement_allowed = false
tensorcube_matmul_replacement_enabled = false
subgroup_fast_path_enabled = false
```

## Native test status

Native Rust tests were not run because the container does not provide `cargo` / `rustc`.
