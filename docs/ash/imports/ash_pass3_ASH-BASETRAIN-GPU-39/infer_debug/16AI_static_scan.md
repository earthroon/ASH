# 16AI Static Forbidden Path Scan

Static scan over the new 16AI runner found no direct occurrences of:

- `Tensor.matmul`
- `fused_matmul_autotune`
- `LocalTuner`
- `RawWgpuBufferLease`
- `into_contiguous_aligned`
- `burn_cubecl_fusion`

16AI does not alter native FFN kernel dispatch or generation default connection state.
