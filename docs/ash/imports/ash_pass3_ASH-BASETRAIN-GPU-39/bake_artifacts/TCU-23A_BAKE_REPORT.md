# TCU-23A Bake Report

## Commit

`TCU-23A — TensorCube 8x8 Atlas MicroTile Kernel / Existing TensorCore-Mimic Consolidation`

## Source SSOT

`ash_pass3_TCU-22_tensorcube_backend_policy_update_candidate_feature_gated_apply_baked.zip`

## Added files

```text
crates/burn_webgpu_backend/src/tensorcube_atlas_microtile.rs
crates/burn_webgpu_backend/src/shaders/tensorcube_atlas_microtile_8x8_vec4_ref.wgsl
crates/burn_webgpu_backend/src/shaders/tensorcube_atlas_microtile_8x8_workgroup_ref.wgsl
crates/burn_webgpu_backend/src/shaders/tensorcube_atlas_microtile_8x8_subgroup_exp.wgsl
crates/burn_webgpu_backend/tests/tcu_23a_tensorcube_atlas_microtile_layout.rs
crates/burn_webgpu_backend/tests/tcu_23a_tensorcube_atlas_microtile_group_schedule.rs
crates/burn_webgpu_backend/tests/tcu_23a_tensorcube_existing_mimic_inventory.rs
crates/burn_webgpu_backend/tests/tcu_23a_qwave_tile_stride_audit.rs
crates/orchestrator_local/src/tcu_23a_tensorcube_atlas_microtile_report.rs
crates/orchestrator_local/src/bin/tcu_23a_tensorcube_atlas_microtile_audit.rs
crates/orchestrator_local/tests/tcu_23a_tensorcube_atlas_microtile_report.rs
workspace/runtime/tensorcube/ash_tensorcube_atlas_microtile_layout_latest.json
workspace/runtime/tensorcube/ash_tensorcube_atlas_microtile_inventory_latest.json
workspace/runtime/tensorcube/ash_tensorcube_atlas_microtile_group_schedule_latest.json
workspace/runtime/tensorcube/ash_tensorcube_atlas_microtile_kernel_report_latest.json
acceptance_reports/TCU-23A_tensorcube_8x8_atlas_microtile_kernel_consolidation.md
bake_artifacts/TCU-23A_BAKE_REPORT.md
bake_artifacts/TCU-23A_STATIC_AUDIT_RESULT.md
```

## Modified files

```text
crates/burn_webgpu_backend/src/lib.rs
crates/orchestrator_local/src/lib.rs
```

## Baked behavior

- Defines `TensorCubeTile8x8Layout` as the physical tile SSOT.
- Defines `Vec4F32` as the default atlas packing.
- Defines logical 16x16 macro grouping with no contiguous 16x16 physical tile.
- Adds CPU scalar 8x8 and grouped 16x16 reference helpers.
- Adds vec4 reference WGSL fixture.
- Adds workgroup reference WGSL fixture with pack-owner writeback to avoid vec4 component write races.
- Adds subgroup experimental seam fixture, disabled by default.
- Adds existing TensorCore-mimic inventory.
- Adds QWave tile stride mismatch audit without silent patch.

## Native validation

`cargo` and `rustc` are not available in the current container, so Rust-native tests were not executed here.

Static artifact audit was run by shell inspection and recorded in `TCU-23A_STATIC_AUDIT_RESULT.md`.
