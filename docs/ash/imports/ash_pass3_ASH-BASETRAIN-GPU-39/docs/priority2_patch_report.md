# Same-device raw logits bridge priority-2 patch report

## Base
- Applied on uploaded `ash_pass3_stage7m_fork_merge_same_device_handles_priority1_patch.zip`

## Patched files
- `crates/model_core/src/lib.rs`
- `crates/burn_webgpu_backend/src/device_handles.rs`
- `crates/burn_webgpu_backend/src/lib.rs`
- `docs/SAME_DEVICE_RAW_LOGITS_BRIDGE_PRIORITY2_PATCH.md`

## What this patch actually does
- Adds an explicit model-core seam that tries to bridge `LastLogitsGpu.gpu_last_row` into a same-device `RawWgpuBufferLease`
- Keeps the failure mode clean: if runtime handles or raw borrow are unavailable, the bridge returns `None`
- Adds a backend helper to test whether same-device raw bridge extraction is available at all

## What this patch does NOT do
- It does not yet call a GPU sampling runtime
- It does not yet remove `cpu_row` materialization
- It does not change token selection behavior by itself

## Why this is the correct priority-2 patch
Priority-1 opened the handle seam. Priority-2 turns that seam into an actual last-logits raw lease entrypoint that later sampling/runtime patches can consume directly.
