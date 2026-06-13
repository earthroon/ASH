# Stage3-C2 Step1/2/3 report

## Scope
- model_core native trace ring state expanded to support submit/poll/collect seam separation
- submit path no longer performs immediate capture
- poll path now calls `is_native_trace_ready()` and only then `collect_native_trace_result()`
- bridge native-first runtime updated to poll a short window before falling back to reference capture

## What changed
1. `NativeTraceGpuTicket` expanded with submit metadata and readiness flags.
2. `NativeTraceRing` now allocates `submit_serial` values.
3. Added `submit_native_trace_job(...)`.
4. Added `is_native_trace_ready(...)`.
5. Added `collect_native_trace_result(...)`.
6. `submit_module_trace_padded_batch(...)` now stores `Submitted` state only.
7. `poll_trace_slot(...)` now performs `is_ready -> collect_result -> Ready transition`.
8. `bridge.rs` now polls up to 4 times before native-first path falls back to reference capture.

## Important limitation
This is a seam split, not a full non-blocking GPU readback implementation yet.
`is_native_trace_ready(...)` currently acts as a structural readiness gate and `collect_native_trace_result(...)` still reuses the current native padded capture path for result assembly. The next step is wiring `gpu_ticket` to real staging/readback completion signals.
