# TCU-24E Bake Report

## Status
`PASS_STATIC_TCU_24E_WITH_NATIVE_TESTS_NOT_RUN`

## Added
- `crates/burn_webgpu_backend/src/qwave_atlas_parity.rs`
- `crates/burn_webgpu_backend/tests/tcu_24e_qwave_atlas_parity_config_gate.rs`
- `crates/burn_webgpu_backend/tests/tcu_24e_qwave_atlas_parity_fixture.rs`
- `crates/burn_webgpu_backend/tests/tcu_24e_qwave_atlas_map_comparison.rs`
- `crates/burn_webgpu_backend/tests/tcu_24e_qwave_atlas_notrun_status.rs`
- `crates/burn_webgpu_backend/tests/tcu_24e_qwave_atlas_no_production_selection.rs`
- `crates/orchestrator_local/src/tcu_24e_qwave_atlas_parity_report.rs`
- `crates/orchestrator_local/src/bin/tcu_24e_qwave_atlas_parity_audit.rs`
- `crates/orchestrator_local/tests/tcu_24e_qwave_atlas_parity_report.rs`

## Runtime JSON
- `workspace/runtime/tensorcube/ash_qwave_atlas_parity_config_latest.json`
- `workspace/runtime/tensorcube/ash_qwave_atlas_parity_fixture_latest.json`
- `workspace/runtime/tensorcube/ash_qwave_atlas_parity_comparison_latest.json`
- `workspace/runtime/tensorcube/ash_qwave_atlas_parity_report_latest.json`

## Guard
- `production_default_changed = false`
- `direct_replacement_allowed = false`
- `fastest_candidate_selection_allowed = false`
- `benchmark_mode_enabled = false`
- `tensorcube_matmul_replacement_enabled = false`
- `subgroup_fast_path_enabled = false`

## Native test note
This environment has no `cargo`/`rustc`; native Rust tests and WGPU validation were not executed here.
