# SFT-GPU-8H-B GPU buffer bridge seal

## Status
PASS_STATIC / PASS_BRIDGE_SEAL

## Scope
This commit does not implement the pass1 projection kernel yet. It seals the GPU-resident buffer bridge required by `projection=gpu_parallel_vocab_atlas`.

## Sealed bridge
- `crates/lora_train/src/lm_head_vocab_atlas_gpu_bridge.rs`
- `GpuLmHeadVocabAtlasBridgeConfig`
- `GpuLmHeadVocabAtlasBufferLayout`
- `GpuLmHeadVocabAtlasBridge`
- `compact_active_sft_rows(...)`
- `build_gpu_lm_head_vocab_atlas_bridge(...)`
- `validate_gpu_bridge_memory_policy(...)`
- `write_gpu_bridge_report(...)`

## Sealed buffers
- hidden: `[active_tokens, hidden_size]`
- labels: `[active_tokens]`
- loss_mask: `[active_tokens]`
- source_row_indices: `[active_tokens]`
- LoRA A: `[rank, hidden_size]`
- LoRA B: `[vocab_size, rank]`
- running_max: `[active_tokens]`
- running_sum_exp: `[active_tokens]`
- target_logit: `[active_tokens]`
- target_seen: `[active_tokens]`
- loss: `[active_tokens]`
- grad_A: `[rank, hidden_size]`
- grad_B: `[vocab_size, rank]`
- tile_group_meta: `[group_count, 6]`

## Guards
- Full `lm_head.weight [vocab, hidden]` GPU buffer remains forbidden.
- Full logits `[tokens, vocab]` buffer remains forbidden.
- Logits readback is forbidden.
- Readback policy is `loss_and_report_only`.
- Tile group weight bytes must not exceed `max_group_weight_bytes`.
- Tile group weight bytes must not recreate the forbidden full vocab buffer.
- Active compact rows must preserve response-only SFT: `prompt_loss_tokens == 0`, `response_loss_tokens > 0`.

## Runtime behavior
When `gpu_parallel.required=true`, the training entry now creates and reports the GPU buffer bridge, then stops explicitly with:

`SFT-GPU-8H-B sealed GPU buffer bridge; pass1 GPU kernel is scheduled for SFT-GPU-8H-C`

## Next
SFT-GPU-8H-C: pass1 GPU tile group projection + partial logsumexp kernel.
