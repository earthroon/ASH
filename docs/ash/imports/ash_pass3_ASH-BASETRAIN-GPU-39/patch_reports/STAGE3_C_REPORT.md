# Stage3 C patch report

## Scope
- Keep native/reference runtime capture on the main thread to avoid `Send` risk around `NativeWgpuModel`.
- Introduce a **captured completion queue** between capture and shard accumulation.
- Move shard buffer packing and shard queueing into a dedicated **packer thread**.
- Preserve the existing async writer thread from stage1/stage2.

## What changed
- Added `CapturedModuleLocalRow` and `CapturedModuleLocalBatch` in `crates/lora_train/src/bridge.rs`.
- Added `captured_tx/captured_rx` bounded queue with `module_local_trace_slots = 2`.
- Main capture loop now:
  - consumes prepared batches,
  - runs `teacher_runtime.capture_padded_batch(...)`,
  - validates dims,
  - assigns `sample_id`,
  - sends captured payload to the packer queue.
- New packer thread now:
  - owns `ModuleLocalFeatureShardBuffer`,
  - pushes rows,
  - freezes shards,
  - forwards frozen shards to the writer queue.
- Final completion log now includes `queued_shards`.

## Intent
This stage overlaps:
- prepare (thread)
- capture (main/native-first runtime)
- pack/freeze (thread)
- write (thread)

without moving `NativeWgpuModel` itself across threads.

## Risk notes
- Compile not validated in this environment.
- `NativeWgpuModel` stays on the main thread by design in this patch.
- This is a safer stage3-C seam than attempting a full capture-worker ownership transfer immediately.
