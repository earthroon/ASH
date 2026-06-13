# Same-device raw logits bridge priority-3 patch

## What this patch adds
- `crates/burn_webgpu_backend/src/gpu_sampling.rs`
- `GpuSamplingRuntime` that can consume a `RawWgpuBufferLease`
- `dispatch_sample_raw_lease(...)`
- `dispatch_sample_cpu_logits(...)` fallback helper
- `gpu_sampling_select.wgsl` compute pass that binds the logits lease directly
- placeholder WGSL files for later `noise/top_k/top_p` passes

## What it means
This patch upgrades the seam from a **last-logits raw lease entrypoint** into a **backend runtime that can actually consume that lease**.

The runtime is same-device-ready because it binds `RawWgpuBufferLease` directly via `as_binding_resource()`.

## Current limitation
- This is still a priority-3 scaffold/runtime patch, not the final sampling path.
- `gpu_sampling_select.wgsl` currently performs a temperature-scaled argmax-like selection over the bound logits buffer.
- `noise`, `top_k`, and `top_p` shaders are placeholders in this patch.
- `model_core` does not call this runtime yet.

## Why this is the correct priority-3 patch
Priority-1 opened runtime handles.
Priority-2 opened the last-logits raw lease seam.
Priority-3 gives the backend a concrete runtime that can consume the raw lease directly, which is the prerequisite for wiring same-device GPU sampling into `model_core`.
