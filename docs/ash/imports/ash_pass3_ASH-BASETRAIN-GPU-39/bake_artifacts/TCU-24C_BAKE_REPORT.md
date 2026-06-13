# TCU-24C Bake Report

## Result
PASS_STATIC_TCU_24C_WITH_NATIVE_TESTS_NOT_RUN

## Added
- `crates/burn_webgpu_backend/src/qwave_vec4_tile_atlas.rs`
- `crates/burn_webgpu_backend/src/shaders/qwave_full_vec4_tile_atlas8x8.wgsl`
- Vec4 tile atlas candidate dispatch in `qwave_dispatch.rs`
- Pack-owner contract tests
- Orchestrator report and audit bin
- Runtime JSON artifacts

## Preserved
- Legacy 11-buffer QWave path
- TCU-24A flat mega atlas candidate
- TCU-24B scalar tile atlas candidate
- Production default dispatch behavior

## Not Opened
- QWave math changes
- Production default replacement
- TensorCube MatMul replacement
- Subgroup fast path
- Readback-free benchmark coupling
