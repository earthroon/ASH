# 16AF-R static forbidden path scan

Scanned files:
- crates/model_core/src/bin/af16r_runtime_parity.rs
- crates/model_core/src/native_atlas_ffn_probe.rs
- crates/burn_webgpu_backend/src/native_atlas_ffn.rs

Forbidden patterns:
- Tensor.matmul
- fused_matmul_autotune
- LocalTuner
- RawWgpuBufferLease
- into_contiguous_aligned
- burn_cubecl_fusion

Matches:
