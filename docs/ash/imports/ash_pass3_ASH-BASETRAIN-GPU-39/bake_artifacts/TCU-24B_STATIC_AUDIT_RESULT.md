# TCU-24B Static Audit Result

Status: PASS_STATIC_TCU_24B_WITH_NATIVE_TESTS_NOT_RUN

## Static Checks

- qwave_tile_atlas.rs exists.
- qwave_full_tile_atlas8x8.wgsl exists.
- qwave_dispatch.rs includes SHADER_QWAVE_FULL_TILE_ATLAS8X8.
- qwave_dispatch.rs exposes dispatch_tile_atlas8x8_candidate().
- qwave_full_tile_atlas8x8.wgsl uses workgroup_id.x as tile_id.
- qwave_full_tile_atlas8x8.wgsl uses local_invocation_id for local pixel coordinates.
- qwave_full_tile_atlas8x8.wgsl writes to scalar qwave_tile_atlas.
- Vec4 packing is not enabled.
- Production default is not changed.
- Legacy QWave path remains preserved.
- TCU-24A flat mega-atlas path remains preserved.

## Native Tests

Not run in this container: cargo/rustc are unavailable.
