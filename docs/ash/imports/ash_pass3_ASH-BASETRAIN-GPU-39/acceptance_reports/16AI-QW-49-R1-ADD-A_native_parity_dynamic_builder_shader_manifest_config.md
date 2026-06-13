# QW-49-R1-ADD-A — Native Parity Dynamic Builder / Shader Manifest Config Seal

## 확정

- Static parity builder and native parity builder are split.
- Failed WGPU execution has a distinct builder path and is not conflated with StaticReceiptOnly.
- Native parity builder does not accept `parity_pass` as an input contract; it derives pass/fail from GPU execution, readback, compared count, tolerance, and NaN/Inf guards.
- Static builder is allowed to emit `PENDING_GPU_EXECUTION` but is forbidden to emit PASS.
- WGSL shader paths are moved into `configs/qwave_wgpu_shader_manifest.toml`.
- Shader manifest receipt records path, role, entry point, required flag, file existence, byte length, and SHA256.

## SSOT

State belongs to:

- `crates/lora_train/src/wgpu_parity_report_builder.rs`
- `crates/lora_train/src/wgpu_shader_manifest.rs`
- `crates/lora_train/src/wgpu_shader_config.rs`
- `configs/qwave_wgpu_shader_manifest.toml`
- `artifacts/wgpu_shader_manifest/`

## No Mutation Guard

This patch does not mutate router state, ranker state, adapter registry, runtime pointer, production adapter artifact, or base model.

## Judgment

This is a structural hardening bake. Native WGPU execution is still the responsibility of QW-49-R1 runner; this patch prevents static receipt evidence from being reused as native execution evidence.
