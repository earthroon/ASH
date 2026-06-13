# SFT-GPU-8H-C Bake Report

## Commit
SFT-GPU-8H-C — pass1 GPU tile group projection + partial logsumexp kernel

## Status
PASS_STATIC / PASS_PASS1_BUFFER_AND_STAGING_SEAL

## Implemented files
- `crates/lora_train/src/lm_head_vocab_atlas_gpu_pass1.rs`
- `crates/lora_train/src/lm_head_vocab_atlas.rs`
- `crates/lora_train/src/lib.rs`
- `tools/validate_sft_gpu_8h_c_static.py`
- `acceptance_reports/SFT-GPU-8H-C_pass1_gpu_tile_group_projection_partial_logsumexp.md`

## Sealed contracts
- `partial_max: [group_count, active_tokens]`
- `partial_sum_exp: [group_count, active_tokens]`
- `partial_target_logit: [group_count, active_tokens]`
- `partial_target_seen: [group_count, active_tokens]`
- full logits buffer remains forbidden
- logits readback remains forbidden
- bounded vocab group staging enforced by `max_group_weight_bytes`
- full lm_head weight buffer remains forbidden
- group-local target capture policy sealed

## Runtime behavior
For `projection=gpu_parallel_vocab_atlas` and `gpu_parallel.required=true`, train_from_features now:
1. Builds the 8H-B GPU bridge.
2. Builds 8H-C pass1 partial CE state buffers.
3. Stages the first vocab group under guard as a staging smoke.
4. Writes `vocab_atlas_gpu_pass1_report.json` and `.md`.
5. Stops explicitly before the actual pass1 projection kernel.

## Validation
- `python tools/validate_sft_gpu_8h_a_static.py` PASS
- `python tools/validate_sft_gpu_8h_b_static.py` PASS
- `python tools/validate_sft_gpu_8h_c_static.py` PASS

## Not performed in this environment
- `cargo check`
- actual WGPU/CubeCL pass1 projection kernel execution

## Next
SFT-GPU-8H-C2 — actual pass1 GPU projection kernel, then SFT-GPU-8H-D global CE reduce kernel.
