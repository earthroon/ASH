# TCU-24G Bake Report

## SSOT

Input SSOT: `ash_pass3_TCU-24F_qwave_atlas_dispatch_readback_telemetry_seal_baked.zip`

## Files added

- `crates/burn_webgpu_backend/src/qwave_atlas_timing_probe.rs`
- `crates/burn_webgpu_backend/tests/tcu_24g_qwave_atlas_timing_config_gate.rs`
- `crates/burn_webgpu_backend/tests/tcu_24g_qwave_atlas_timing_guard.rs`
- `crates/burn_webgpu_backend/tests/tcu_24g_qwave_atlas_timing_sample_summary.rs`
- `crates/burn_webgpu_backend/tests/tcu_24g_qwave_atlas_timestamp_query_gate.rs`
- `crates/burn_webgpu_backend/tests/tcu_24g_qwave_atlas_no_production_selection.rs`
- `crates/orchestrator_local/src/tcu_24g_qwave_atlas_timing_probe_report.rs`
- `crates/orchestrator_local/src/bin/tcu_24g_qwave_atlas_timing_probe_audit.rs`
- `crates/orchestrator_local/tests/tcu_24g_qwave_atlas_timing_probe_report.rs`

## Runtime outputs

- `workspace/runtime/tensorcube/ash_qwave_atlas_timing_probe_config_latest.json`
- `workspace/runtime/tensorcube/ash_qwave_atlas_timing_probe_samples_latest.json`
- `workspace/runtime/tensorcube/ash_qwave_atlas_timing_probe_summary_latest.json`
- `workspace/runtime/tensorcube/ash_qwave_atlas_timing_probe_report_latest.json`

## Safety flags

- `readback_enabled = false`
- `output_validation_enabled = false`
- `benchmark_result_is_advisory_only = true`
- `fastest_candidate_selection_allowed = false`
- `production_default_changed = false`
- `direct_replacement_allowed = false`
- `backend_router_enabled = false`
- `tensorcube_matmul_replacement_enabled = false`
- `subgroup_fast_path_enabled = false`

## Native status

Rust/WGPU native tests were not executed in this container.
