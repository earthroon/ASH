# Stage3-C2 Step1/Step2 Patch Report

## Applied scope
- `crates/model_core/src/lib.rs`
- `crates/lora_train/src/bridge.rs`

## Step1
- `submit_module_trace_padded_batch()` no longer performs immediate native capture.
- It now seals slot state as `Submitted` with:
  - `submit_at`
  - `poll_count`
  - `request`
  - `padded_token_ids`
  - `gpu_ticket`

## Step2
- Added `poll_trace_slot(slot_id)`.
- Poll transitions `Submitted -> Ready` by invoking the existing native padded capture seam.
- `try_collect_ready_module_trace()` and `try_collect_any_ready_module_trace()` were updated for the `Ready { ready_at, .. }` state.

## Bridge compatibility seam
- `ModuleLocalCaptureRuntime::capture_padded_batch()` now does:
  - `submit_module_trace_padded_batch()`
  - `poll_trace_slot()`
  - `try_collect_ready_module_trace()`
- This preserves pre-C2 behavior while moving the state transition boundary out of submit.

## Important limitation
- This is **not** true async readback yet.
- `poll_trace_slot()` still performs the native capture work synchronously.
- The value of this patch is that the slot state machine is now structurally correct for the next cut.

## Next cut
- Replace synchronous work inside `poll_trace_slot()` with real in-flight GPU readback / staging / readiness checks.
