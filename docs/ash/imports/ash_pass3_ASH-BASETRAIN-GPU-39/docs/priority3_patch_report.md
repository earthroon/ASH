# Same-device raw logits bridge priority-3 patch report

## Base
- Applied on uploaded `ash_pass3_stage7m_fork_merge_same_device_logits_bridge_priority2_patch.zip`

## Patched files
- `crates/burn_webgpu_backend/src/gpu_sampling.rs`
- `crates/burn_webgpu_backend/src/shaders/gpu_sampling_select.wgsl`
- `crates/burn_webgpu_backend/src/shaders/gpu_sampling_noise.wgsl`
- `crates/burn_webgpu_backend/src/shaders/gpu_sampling_topk.wgsl`
- `crates/burn_webgpu_backend/src/shaders/gpu_sampling_topp_scan.wgsl`
- `crates/burn_webgpu_backend/src/lib.rs`
- `docs/SAME_DEVICE_RAW_LOGITS_BRIDGE_PRIORITY3_PATCH.md`

## What this patch actually does
- Adds a backend-owned GPU sampling runtime that accepts `RawWgpuBufferLease`
- Adds a real compute pipeline and bind-group contract for consuming a bound logits buffer directly on the GPU
- Adds a CPU-logits upload fallback helper that reuses the same runtime contract
- Exports the runtime from `burn_webgpu_backend`

## What this patch does NOT do
- It does not yet connect `model_core::select_next_token_with_sampling(...)` to this runtime
- It does not yet remove `cpu_row` materialization from the hot path
- It does not yet implement exact GPU-native multinomial / top_k / top_p filtering

## Why this is the correct priority-3 patch
Priority-3 is the first patch where the backend can actually *consume* the same-device raw logits lease. That is the necessary bridge from the priority-2 entrypoint to the later model-core runtime binding patch.
