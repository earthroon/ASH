# Stage3 C123 Report

## Scope
Implemented the priority-1/2/3 native trace slot state machine groundwork on top of stage3_c.

### Included
1. `trace_ring` added to `NativeWgpuModel`
2. `submit_module_trace_padded_batch()` added
3. `try_collect_ready_module_trace()` and `try_collect_any_ready_module_trace()` added

## What changed

### model_core
- Added `PendingTraceBatchMeta`
- Added `TraceSlotState`
- Added `NativeTraceSlot`
- Added `NativeTraceRing`
- Added `trace_ring: NativeTraceRing` to `NativeWgpuModel`
- Initialized `trace_ring` in `NativeWgpuModel::from_full_checkpoints()`
- Added native slot submission / collection APIs

### bridge
- `ModuleLocalCaptureRuntime::capture_padded_batch(...)` now takes `&mut self`
- Native-first path now uses:
  - `submit_module_trace_padded_batch()`
  - `try_collect_ready_module_trace()`
- Existing reference fallback is preserved
- Main module-local extraction loop now holds `teacher_runtime` as mutable and passes `batch_index`

## Important limitation
This patch establishes the slot/ring API and bridge compatibility seam, but it does **not yet** implement real asynchronous GPU readback. Native submission still transitions to `Ready` immediately after the synchronous native capture call. The next patch should replace that internal immediate-ready step with actual in-flight staging/readback and polling.
