# STAGE3 C2 STEP4 REPORT

## Summary
- Replaced the synchronous `capture_padded_batch(...)` flow in `bridge.rs` with a true submit/poll/collect dispatcher loop.
- Added `SubmittedModuleLocalCapture` handle types for native in-flight slots and reference-ready fallback captures.
- Main module-local extraction loop now maintains `prepared_pending` and `in_flight` queues and only packs batches after `poll_submitted_capture(...)` reports ready and `try_collect_submitted_capture(...)` returns captures.

## Intent
This stage completes the bridge-side part of Stage3-C2:
- `submit` no longer blocks the loop until captures are available.
- `poll` is now the gating step for readiness.
- `collect` is only attempted after readiness.

## Notes
- This patch does not yet make native readback fully asynchronous at the GPU level. It completes the bridge dispatcher seam so that the already-separated `submit / is_ready / collect_result` model-core API is actually used as intended.
- Cargo/rustc were not available in the container, so compilation was not verified here.
