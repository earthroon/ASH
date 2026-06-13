# Module-local pipeline stage1 patch

## What changed
- Reworked `extract_module_local_feature_store_from_jsonl_paths` into a staged pipeline.
- Added a **prepare stage thread** that reads JSONL, tokenizes prompt/response, applies BOS/EOS, truncates to `max_seq_len`, and emits pre-batched work units.
- Added an **async shard writer thread** so capture no longer blocks on safetensors shard flush.
- Kept the **teacher capture on the main thread** to minimize SSOT breakage while still overlapping prep/write with capture.
- Added prep/write queue logging:
  - `[bridge][module_local][prep] ...`
  - `[bridge][module_local][queue] ...`
  - `[bridge][module_local][write] ...`
- Included stage1-style prepared batch metadata (`seq_lens`, `max_batch_seq_len`) so batch prep is no longer done ad hoc inside the capture loop.

## Intended impact
- Reduce GPU/teacher idle time caused by synchronous JSONL reading and tokenization.
- Reduce capture stalls caused by synchronous shard writing.
- Preserve existing manifest / target-key / dim-validation behavior as much as possible.

## Not changed yet
- Capture still runs on the main extraction thread.
- No native WGPU trace hook yet.
- No fully padded tensor handoff into model_core yet; this patch stops at stage1 batch preparation metadata.

## Validation status
- File-level patch applied successfully.
- Container environment did **not** have `cargo`/`rustc`, so compile validation could not be run here.
- Treat this as a code patch package that still needs a local `cargo check` on the user's machine.
