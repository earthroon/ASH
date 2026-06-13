# TCU-24D — QWave Workgroup Shared-Memory Stencil Staging / Tile Halo Contract

## Status
PASS_STATIC_TCU_24D_WITH_NATIVE_TESTS_NOT_RUN

## Scope
- Added QWave stencil halo SSOT with 8x8 core tile and radius-2 halo.
- Added 12x12 workgroup staging contract for derived DeltaInput / Energy / Mag2 samples.
- Added staged Vec4 tile atlas WGSL candidate preserving TCU-24C pack-owner output writes.
- Added candidate dispatch entry without changing default QWave dispatch.

## Guard Rails
- QWave math changed: false
- Production default changed: false
- Direct replacement allowed: false
- TensorCube MatMul replacement enabled: false
- Subgroup fast path enabled: false
- Legacy / flat atlas / scalar tile atlas / Vec4 tile atlas paths preserved.

## Native Test Status
Native Rust/WGPU tests were not executed in this container because cargo/rustc is unavailable.
