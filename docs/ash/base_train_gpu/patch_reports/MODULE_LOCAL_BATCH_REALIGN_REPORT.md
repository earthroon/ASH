# Module-local batch realignment patch

## What changed

### 1) Real batch-owner path for module-local capture
- File: `crates/model_core/src/lib.rs`
- Added batch-state helpers:
  - `PaddedTokenBatch`
  - `BatchedHidden`
  - `build_padded_token_batch`
  - `embed_token_batch`
  - `rms_norm_batched`
  - `linear_apply_batched`
  - `apply_reference_loras_batched`
  - `causal_attention_batched`
  - `add_batched`
  - `silu_mul_batched`
  - `capture_module_from_batched_hidden`
- Replaced `ReferenceModel::capture_module_io_ids_batch(...)` from fake sequential loop to a real batch-owner execution path over padded `[B, T, H]` buffers.
- Supported trace targets remain aligned with the existing single-sample path:
  - `layers.N.attn.q_proj`
  - `layers.N.attn.o_proj`
  - `layers.N.ffn.up_proj`

### 2) Dump-only branch ordering fix
- File: `crates/lora_train/src/bin/lora_train.rs`
- `bridge_dump_only && module_local` now exits through `extract_module_local_feature_store_from_jsonl_paths(...)` first, instead of falling through the module-local bundle/training path.

### 3) Timing instrumentation
- File: `crates/lora_train/src/bridge.rs`
- Added timing split logs for:
  - `capture_sec`
  - `pack_sec`
  - `write_sec`
- This should make it obvious whether the stall is in trace capture, row packing, or shard write.

### 4) Safer config defaults for measurement
- File: `configs/tinyllama_1p1b_v4_lora_run02_fresh.json`
- Added:
  - `"module_local_teacher_batch_size": 1`
- Raised frequent save/eval intervals to reduce measurement noise while testing the dump path.

## Important note
- I could not run `cargo check` in this environment because the container does not have `cargo` or `rustc` installed.
- JSON validity for the modified config was checked successfully.
- Rust source was patched structurally and reviewed textually, but compile success is **not** verified inside this container.

## Files changed
- `crates/model_core/src/lib.rs`
- `crates/lora_train/src/bin/lora_train.rs`
- `crates/lora_train/src/bridge.rs`
- `configs/tinyllama_1p1b_v4_lora_run02_fresh.json`

## Included diff files
- `patch_reports/lib.rs.diff`
- `patch_reports/lora_train.rs.diff`
- `patch_reports/bridge.rs.diff`
- `patch_reports/tinyllama_1p1b_v4_lora_run02_fresh.json.diff`
