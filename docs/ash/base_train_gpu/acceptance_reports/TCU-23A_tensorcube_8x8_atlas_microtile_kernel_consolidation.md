# TCU-23A — TensorCube 8x8 Atlas MicroTile Kernel / Existing TensorCore-Mimic Consolidation

## Status

`PASS_TCU_23A_TENSORCUBE_ATLAS_MICROTILE_CONSOLIDATION`

## SSOT

TCU-23A uses the TCU-22 baked tree as SSOT and adds a consolidation layer for existing TensorCore-like fragments.

## Accepted scope

TCU-23A is not a production dispatch replacement. It is a layout seal, inventory seal, schedule seal, and reference-consolidation commit.

## Confirmed layout

- Physical tile size: `8x8`
- Scalar kind: `F32`
- Packing kind: `Vec4F32`
- Scalar count per tile: `64`
- `vec4<f32>` count per row: `2`
- `vec4<f32>` count per tile: `16`
- Bytes per tile: `256`
- Row stride: `2 vec4`
- Tile stride: `16 vec4`
- Logical 16x16 grouping is allowed.
- Physical contiguous 16x16 tile creation remains forbidden.

## Existing mimic inventory sealed

TCU-23A records these existing pieces as related but not directly replaceable:

1. `crates/burn_webgpu_backend/src/shaders/headwise_atlas_attention_vec4_f16_packed.wgsl`
2. `crates/burn_webgpu_backend/src/shaders/headwise_atlas_attention_subgroup_exp.wgsl`
3. `crates/burn_webgpu_backend/src/shaders/qwave_tensor_f16.wgsl`
4. `crates/burn_webgpu_backend/src/native_atlas_ffn.rs`
5. `crates/lora_train/src/lm_head_vocab_atlas_gpu_bridge.rs`

Every inventory item has `direct_replacement_allowed = false`.

## Grouped logical 16x16 schedule

The logical 16x16 macro tile is represented only as four 8x8 output tiles:

```text
C00 = A00*B00 + A01*B10
C01 = A00*B01 + A01*B11
C10 = A10*B00 + A11*B10
C11 = A10*B01 + A11*B11
```

This expands to eight `MatMulAccumulate8x8` steps and never creates a contiguous 16x16 physical tile.

## QWave stride audit

`qwave_tensor_f16.wgsl` currently declares:

```text
TILE_STRIDE = TILE_X + 1
TILE_AREA = TILE_STRIDE * TILE_Y
tile_idx(tx, ty) = ty * TILE_X + tx
```

TCU-23A records this as `ExistingMismatchObserved` and sets `silent_patch_allowed = false`.

No silent QWave shader patch is applied in this commit.

## Guardrails

TCU-23A keeps these doors closed:

- No production TensorCube dispatch replacement.
- No SFT-GPU pass1 direct replacement.
- No runtime inference direct replacement.
- No backend policy mutation.
- No LoRA attach/detach or hot reload connection.
- No safe tensor mode direct apply.
- No subgroup fast path default activation.
- No physical contiguous 16x16 tile creation.

## Runtime artifacts

- `workspace/runtime/tensorcube/ash_tensorcube_atlas_microtile_layout_latest.json`
- `workspace/runtime/tensorcube/ash_tensorcube_atlas_microtile_inventory_latest.json`
- `workspace/runtime/tensorcube/ash_tensorcube_atlas_microtile_group_schedule_latest.json`
- `workspace/runtime/tensorcube/ash_tensorcube_atlas_microtile_kernel_report_latest.json`

## Native tests to run in Rust environment

```bash
cargo test -p burn_webgpu_backend tcu_23a_tensorcube_atlas_microtile_layout
cargo test -p burn_webgpu_backend tcu_23a_tensorcube_atlas_microtile_group_schedule
cargo test -p burn_webgpu_backend tcu_23a_tensorcube_existing_mimic_inventory
cargo test -p burn_webgpu_backend tcu_23a_qwave_tile_stride_audit
cargo test -p orchestrator_local tcu_23a_tensorcube_atlas_microtile_report
cargo run -p orchestrator_local --bin tcu_23a_tensorcube_atlas_microtile_audit
```

## Final note

TCU-23A consolidates the existing atlas/vector/workgroup/subgroup pieces into an 8x8 microtile SSOT. It does not claim TensorCore hardware MMA access.
