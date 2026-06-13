# SFT-GPU-8F — A-SFT native_dump compute-level batched hidden provider seal

## Status

PASS_STATIC / PENDING_RUNTIME

## SSOT

- `crates/lora_train/src/sft_feature_store.rs`
- `crates/lora_train/src/a_sft_batched_hidden_provider.rs`
- `crates/model_core/src/native_wgpu.rs`
- `crates/lora_train/src/config.rs`
- `configs/ash_ko_short_sft_lm_head_lora_v1b_native_dump.json`

## Implemented contract

- Preserves `atlas_token_grouped` grouping from SFT-GPU-8E.
- Removes the native dump hot-path loop that called `teacher.forward_hidden_ids(&item.example.full_ids)` per example.
- Adds `ASftBatchedHiddenProvider` with `NativeWgpuBatched` and explicit `ReferencePerExampleFallback` modes.
- Adds `NativeWgpuModel::forward_hidden_padded_batch(...)` for `[batch,max_seq]` token input and `[batch,max_seq,hidden]` flattened hidden output.
- Slices feature-store writes by each shifted `input_ids.len()` so padded positions are never written.
- Adds config seals: `hidden_provider`, `require_compute_batched_hidden`, `forbid_per_example_forward`.
- Progress report now records `batch_provider`, `compute_level_batched_hidden`, `per_example_forward_loop_removed`, `fallback_used`, `hidden_shape_policy`, `row_order_policy`, and `sample_id_policy`.

## Runtime acceptance gate

Runtime PASS requires:

- `compute_level_batched_hidden=true`
- `fallback_used=false`
- `prompt_loss_tokens=0`
- `response_loss_tokens>0`
- `feature_store_manifest.target_key=lm_head`
- no hidden length mismatch
- no fallback when `forbid_per_example_forward=true`

## Runtime status

Not executed in this bake environment. Target Rust/WGPU runtime must run:

```powershell
cargo run -p lora_train --bin lora_train -- configs/ash_ko_short_sft_lm_head_lora_v1b_native_dump.json 1
```
