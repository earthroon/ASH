# Module-local pipeline stage2 patch

## What changed
- Extended the stage1 prepare path so each prepared module-local batch now includes a **fully padded flat token buffer** (`padded_token_ids`) instead of only jagged `Vec<Vec<u32>>` payloads.
- Added `ReferenceModel::capture_module_io_padded_batch(...)` in `crates/model_core/src/lib.rs`.
- Refactored the existing batched capture path so both
  - `capture_module_io_ids_batch(...)`, and
  - the new prepadded entrypoint
  funnel through the same internal padded-batch execution seam.
- Updated `crates/lora_train/src/bridge.rs` so the module-local capture loop calls the new prepadded model-core entrypoint directly.

## Intended impact
- Remove the extra `Vec<Vec<u32>> -> PaddedTokenBatch` reconstruction that still remained between stage1 prepare and model_core capture.
- Reduce per-batch CPU overhead and allocation churn immediately before teacher capture.
- Keep stage1 prep/write overlap intact while tightening the handoff seam into model_core.

## What is still not changed
- No native WGPU trace hook yet.
- Capture still happens as a single worker path; this patch only reduces CPU-side batch marshaling overhead.
- Padded token buffers are still cloned into model_core-owned storage; the seam is cleaner, but not yet zero-copy.

## Validation status
- File-level patch applied successfully.
- This environment still did not provide `cargo`/`rustc`, so compile validation could not be run here.
- Treat this as a stage2 code patch package pending local `cargo check`.
