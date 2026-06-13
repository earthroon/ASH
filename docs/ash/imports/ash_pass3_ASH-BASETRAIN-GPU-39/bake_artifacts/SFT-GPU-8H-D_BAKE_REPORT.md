# SFT-GPU-8H-D Bake Report

## Scope
Baked global CE reduce kernel smoke path on top of SFT-GPU-8H-C2.

## Added
- `crates/lora_train/src/lm_head_vocab_atlas_gpu_reduce.rs`
- `tools/validate_sft_gpu_8h_d_static.py`
- `acceptance_reports/SFT-GPU-8H-D_global_ce_reduce_kernel.md`

## Modified
- `crates/lora_train/src/lib.rs`
- `crates/lora_train/src/lm_head_vocab_atlas.rs`

## Contract
- all vocab tile groups are dispatched through pass1 before reduce
- partial CE buffers are reduced into global CE state
- `target_seen_count == 1` is enforced per active token
- full logits buffer and logits readback remain forbidden
- path stops explicitly before 8H-E gradient kernel

## Runtime stop
`SFT-GPU-8H-D sealed global CE reduce kernel; pass2 GPU gradient is scheduled for SFT-GPU-8H-E`
