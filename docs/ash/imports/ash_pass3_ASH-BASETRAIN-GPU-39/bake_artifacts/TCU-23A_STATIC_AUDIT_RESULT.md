# TCU-23A Static Audit Result

## Status

`PASS_STATIC_TCU_23A_WITH_NATIVE_TESTS_NOT_RUN`

## Static checks passed

- `crates/burn_webgpu_backend/src/tensorcube_atlas_microtile.rs` exists.
- `crates/burn_webgpu_backend/src/lib.rs` exports `tensorcube_atlas_microtile`.
- `crates/orchestrator_local/src/lib.rs` exports `tcu_23a_tensorcube_atlas_microtile_report`.
- WGSL fixtures exist:
  - `tensorcube_atlas_microtile_8x8_vec4_ref.wgsl`
  - `tensorcube_atlas_microtile_8x8_workgroup_ref.wgsl`
  - `tensorcube_atlas_microtile_8x8_subgroup_exp.wgsl`
- Runtime JSON artifacts exist under `workspace/runtime/tensorcube/`.
- `layout.tile_rows == 8`.
- `layout.tile_cols == 8`.
- `layout.vec4_per_tile == 16`.
- `layout.bytes_per_tile == 256`.
- `creates_contiguous_16x16_tile == false`.
- `sft_pass1_direct_replacement_allowed == false`.
- `runtime_inference_direct_replacement_allowed == false`.
- `subgroup_fast_path_enabled_by_default == false`.
- `qwave_stride_audit.stride_policy == ExistingMismatchObserved`.
- `qwave_stride_audit.silent_patch_allowed == false`.
- Existing `qwave_tensor_f16.wgsl` still declares `TILE_STRIDE` while `tile_idx` uses `TILE_X`; this was recorded as audit warning only.

## Native tests

Rust-native tests were not executed in this container because `cargo` / `rustc` are unavailable.

Run in a Rust-capable environment:

```bash
cargo test -p burn_webgpu_backend tcu_23a_tensorcube_atlas_microtile_layout
cargo test -p burn_webgpu_backend tcu_23a_tensorcube_atlas_microtile_group_schedule
cargo test -p burn_webgpu_backend tcu_23a_tensorcube_existing_mimic_inventory
cargo test -p burn_webgpu_backend tcu_23a_qwave_tile_stride_audit
cargo test -p orchestrator_local tcu_23a_tensorcube_atlas_microtile_report
cargo run -p orchestrator_local --bin tcu_23a_tensorcube_atlas_microtile_audit
```

## Guardrail result

TCU-23A does not replace SFT-GPU pass1, runtime inference, backend policy, LoRA hot reload, or safe tensor mode behavior.
