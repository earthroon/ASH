# Same-device raw logits bridge priority-1 patch

## What this patch adds
- `crates/burn_webgpu_backend/src/device_handles.rs`
- `NativeWgpuRuntimeHandles`
- `try_extract_runtime_handles(&WgpuDevice)`
- `try_build_same_device_raw_bridge(&WgpuDevice)`
- `vendor_fork_scaffold/burn-wgpu-local/src/runtime_handles.rs`
- `NativeWgpuModel::same_device_runtime_handles()`
- `NativeWgpuModel::same_device_raw_bridge()`

## What it means
This is the seam-opening patch for same-device raw logits work.
It does **not** complete same-device GPU sampling by itself.

## Current limitation
The default/local extraction hook returns `None` until the local burn/wgpu fork wires real raw device/queue extraction.
That is intentional: this patch establishes the SSOT seam without pretending extraction already works.
