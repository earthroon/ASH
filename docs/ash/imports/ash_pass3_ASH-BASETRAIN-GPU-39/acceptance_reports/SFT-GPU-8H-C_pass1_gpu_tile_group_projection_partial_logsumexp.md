# SFT-GPU-8H-C pass1 GPU tile group projection + partial logsumexp kernel

## Status
PASS_STATIC / PASS_PASS1_BUFFER_AND_STAGING_SEAL

## Sealed
- `lm_head_vocab_atlas_gpu_pass1.rs` added.
- `partial_max`: `[group_count, active_tokens]`
- `partial_sum_exp`: `[group_count, active_tokens]`
- `partial_target_logit`: `[group_count, active_tokens]`
- `partial_target_seen`: `[group_count, active_tokens]`
- group-local target capture policy sealed.
- bounded `W_group` staging sealed.
- bounded `B_group` staging sealed.
- full logits buffer forbidden.
- logits readback forbidden.
- full lm_head weight buffer remains forbidden.

## Runtime behavior
When `projection=gpu_parallel_vocab_atlas` and `gpu_parallel.required=true`, the train path now:
1. Builds the 8H-B GPU buffer bridge.
2. Builds 8H-C pass1 partial CE buffers.
3. Stages the first vocab group under `max_group_weight_bytes` as a guard smoke.
4. Writes `vocab_atlas_gpu_pass1_report.json/.md`.
5. Stops explicitly before the actual pass1 projection kernel.

## Next
SFT-GPU-8H-C2 actual pass1 GPU projection kernel, then SFT-GPU-8H-D global CE reduce kernel.
