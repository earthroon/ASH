# STAGE3-C3 Native Readback Surgery

This patch turns the native trace slot state machine into a real readback-driven flow.

## What changed
- `NativeTraceSlot` now owns staging/readback buffers and byte lengths.
- `submit_native_trace_job()` now:
  - computes native trace tensors,
  - borrows same-device raw WGPU buffers,
  - allocates MAP_READ staging buffers,
  - encodes `copy_buffer_to_buffer`,
  - submits the command queue,
  - returns a `NativeTraceGpuTicket`.
- `is_native_trace_ready()` now:
  - requests `map_async` exactly once,
  - polls the raw WGPU device,
  - checks callback-backed readiness flags,
  - returns readiness only.
- `collect_native_trace_result()` now:
  - reads mapped staging buffers,
  - converts bytes to `f32`,
  - stitches `CapturedModuleIo` from flat buffers,
  - unmaps and clears slot staging ownership.
- `poll_trace_slot()` now only performs:
  - `is_ready`
  - `collect_result`
  - `Submitted -> Ready` transition.

## Important behavior
- Native trace submit now requires a same-device raw bridge and zero-copy buffer candidates.
- If raw borrowing is unavailable, the native submit path errors and the bridge-level fallback may engage.
- This environment could not run `cargo check`, so compile/runtime validation must be done in the user's local workspace.
