# TCU-24F Static Audit Result

## Result

`PASS_STATIC_TCU_24F_WITH_NATIVE_TESTS_NOT_RUN`

## Static checks performed

- `qwave_atlas_telemetry.rs` exists.
- `QWaveAtlasTelemetryConfig` exists.
- `QWaveAtlasTelemetryEvent` exists.
- `QWaveAtlasReadbackSummary` exists.
- `QWaveAtlasTelemetryReport` exists.
- `build_qwave_atlas_telemetry_report_from_parity()` exists.
- `build_qwave_atlas_telemetry_default_report()` exists.
- Orchestrator audit report and bin exist.
- Runtime JSON artifacts exist.
- Acceptance and bake report artifacts exist.

## Native checks not run

```bash
cargo test -p burn_webgpu_backend tcu_24f_qwave_atlas_telemetry_config_gate
cargo test -p burn_webgpu_backend tcu_24f_qwave_atlas_telemetry_event_chain
cargo test -p burn_webgpu_backend tcu_24f_qwave_atlas_readback_summary
cargo test -p burn_webgpu_backend tcu_24f_qwave_atlas_notrun_telemetry
cargo test -p burn_webgpu_backend tcu_24f_qwave_atlas_no_benchmark_or_selection
cargo test -p orchestrator_local tcu_24f_qwave_atlas_telemetry_report
cargo run -p orchestrator_local --bin tcu_24f_qwave_atlas_telemetry_audit
```

Reason: `cargo` / `rustc` unavailable in the current container.
