# TCU-24A — QWave Mega Atlas Output Buffer / Legacy 11-Map Consolidation

## Status

PASS_TCU_24A_QWAVE_MEGA_ATLAS_CANDIDATE

## Completed

- Added `qwave_mega_atlas.rs` with fixed 11-map ordering, flat scalar atlas layout, map ranges, offset calculation, atlas/deatlasize helpers, buffer plan, and candidate report.
- Added `qwave_full_mega_atlas.wgsl` that preserves the legacy QWave math and redirects output writes through `atlas_write(map_id, pixel_index, value)`.
- Added `SHADER_QWAVE_FULL_MEGA_ATLAS` and `dispatch_mega_atlas_candidate()` sidecar path in `qwave_dispatch.rs`.
- Consolidated candidate output/readback plan from 11 buffers to 1 output atlas buffer and 1 readback buffer.
- Preserved legacy `dispatch_gpu()` and default `dispatch()` behavior.

## Guardrails

- QWave math changed: false
- Production default changed: false
- Legacy path preserved: true
- Direct replacement allowed: false
- Tile8x8 atlas enabled: false
- Vec4 packing enabled: false
- TensorCube MatMul replacement enabled: false

## Runtime Artifacts

- `workspace/runtime/tensorcube/ash_qwave_mega_atlas_layout_latest.json`
- `workspace/runtime/tensorcube/ash_qwave_mega_atlas_map_offsets_latest.json`
- `workspace/runtime/tensorcube/ash_qwave_mega_atlas_candidate_report_latest.json`
