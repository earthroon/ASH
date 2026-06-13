# TCU-24C — QWave Vec4F32 Tile Atlas / Pack-Owner Write Contract

## Status
PASS_TCU_24C_QWAVE_VEC4_TILE_ATLAS8X8_CANDIDATE

## SSOT
- Base ZIP: `ash_pass3_TCU-24B_qwave_8x8_tile_atlas_addressing_1d_dispatch_candidate_baked.zip`
- State owner: `crates/burn_webgpu_backend/src/qwave_vec4_tile_atlas.rs`
- Candidate shader: `crates/burn_webgpu_backend/src/shaders/qwave_full_vec4_tile_atlas8x8.wgsl`

## Completed Acceptance Criteria
1. TCU-24A flat mega atlas candidate is preserved.
2. TCU-24B scalar tile atlas candidate is preserved.
3. QWave Vec4F32 tile atlas layout is added.
4. `vec4_per_row = 2` and `vec4_per_tile = 16` are sealed.
5. `map_count = 11` is preserved.
6. Pixel coordinates map to `tile_id/local_x/local_y/vec4_col/component`.
7. Atlas vec4 offset uses `map_id/tile_id/local_y/vec4_col`.
8. Pack-owner write contract is added.
9. Pack owners are `local_x == 0` and `local_x == 4`.
10. Direct component write is forbidden.
11. Component race write is forbidden.
12. Workgroup scalar staging is required.
13. Tail lanes are masked/staged as zero.
14. `qwave_full_vec4_tile_atlas8x8.wgsl` is added.
15. Shader keeps `workgroup_size(8,8,1)`.
16. Shader keeps 1D `tile_id` dispatch.
17. Only pack-owner invocations write vec4 output elements.
18. QWave math is not changed.
19. Output write destination changes to Vec4 tile atlas only.
20. `qwave_dispatch.rs` has a Vec4 tile atlas candidate dispatch.
21. Legacy dispatch path is preserved.
22. TCU-24A flat atlas path is preserved.
23. TCU-24B scalar tile atlas path is preserved.
24. Default `dispatch()` remains legacy.
25. TensorCube MatMul replacement is not enabled.
26. Production default is not changed.
27. Runtime JSON artifacts were generated.

## Guard Flags
```text
qwave_math_changed = false
production_default_changed = false
direct_replacement_allowed = false
vec4_packing_enabled = true
pack_owner_write_required = true
component_race_write_forbidden = true
tensorcube_matmul_replacement_enabled = false
```

## Native Test Status
Rust-native tests were not run in this container because `cargo`/`rustc` are unavailable.
