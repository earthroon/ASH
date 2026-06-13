# TCU-24B — QWave 8x8 Tile Atlas Addressing / 1D Tile Dispatch Candidate

## Status

PASS_TCU_24B_QWAVE_TILE_ATLAS8X8_CANDIDATE

## Scope

TCU-24B extends the TCU-24A flat QWave mega-atlas candidate into a scalar 8x8 tile-addressed atlas candidate. It adds 1D tile_id dispatch while preserving QWave math, the legacy 11-buffer path, and the TCU-24A flat mega-atlas candidate path.

## Acceptance

- QWave 8x8 tile atlas layout is defined.
- tile_width and tile_height are fixed to 8.
- tile_cols is ceil(width / 8).
- tile_rows is ceil(height / 8).
- tile_count is tile_cols * tile_rows.
- scalar_per_tile is 64.
- scalar_per_map is tile_count * 64.
- scalar_total is 11 * tile_count * 64.
- map ordering reuses TCU-24A QWaveMegaAtlasMapKind.
- pixel x/y is convertible into tile_id/local_x/local_y.
- map_id/tile_id/local_y/local_x computes scalar atlas offsets.
- qwave_full_tile_atlas8x8.wgsl is added.
- The shader uses workgroup_id.x as tile_id.
- The shader preserves workgroup_size(8, 8, 1).
- The shader restores tile_x/tile_y and pixel x/y inside WGSL.
- Tail lanes outside width/height return without writing.
- QWave math is not changed.
- Output write destination changes to the tile atlas only.
- qwave_dispatch.rs exposes dispatch_tile_atlas8x8_candidate().
- Legacy dispatch_gpu path is preserved.
- TCU-24A flat mega-atlas candidate path is preserved.
- dispatch() default remains legacy.
- Vec4F32 packing is disabled.
- TensorCube MatMul replacement is disabled.
- Production default is not changed.

## Safety Flags

```text
qwave_math_changed = false
production_default_changed = false
direct_replacement_allowed = false
dispatch_is_1d_tile_id = true
tile8x8_atlas_enabled = true
vec4_packing_enabled = false
tensorcube_matmul_replacement_enabled = false
```

## Runtime Artifacts

- workspace/runtime/tensorcube/ash_qwave_tile_atlas8x8_layout_latest.json
- workspace/runtime/tensorcube/ash_qwave_tile_atlas8x8_address_samples_latest.json
- workspace/runtime/tensorcube/ash_qwave_tile_atlas8x8_candidate_report_latest.json
