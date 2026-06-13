# TCU-24A Static Audit Result

Status: PASS_STATIC_TCU_24A_WITH_NATIVE_TESTS_NOT_RUN

## Static Checks

- `qwave_mega_atlas.rs` exists.
- `qwave_full_mega_atlas.wgsl` exists.
- `SHADER_QWAVE_FULL_MEGA_ATLAS` exists.
- `dispatch_mega_atlas_candidate()` exists.
- Legacy `dispatch_gpu()` path is preserved.
- Default `dispatch()` still calls legacy `dispatch_gpu()` first.
- `qwave_full_mega_atlas.wgsl` uses one output atlas binding.
- TCU-24A runtime JSON artifacts exist.

## Native Tests

Not run: cargo/rustc unavailable in the bake container.
