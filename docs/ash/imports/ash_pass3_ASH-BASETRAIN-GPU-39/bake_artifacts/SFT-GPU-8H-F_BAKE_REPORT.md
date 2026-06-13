# SFT-GPU-8H-F Bake Report

## Baked from
`ash_pass3_SFT-GPU-8H-E_pass2_gpu_gradient_kernel_baked.zip`

## Added
- `crates/lora_train/src/lm_head_vocab_atlas_gpu_update.rs`
- config schema for `lm_head_vocab_atlas.gpu_parallel.update`
- train-from-features handoff after 8H-E pass2 gradient
- update report writer for `vocab_atlas_gpu_update_report.json/.md`
- static validator `tools/validate_sft_gpu_8h_f_static.py`

## Runtime path
8H-B bridge -> 8H-C/C2 all-group pass1 -> 8H-D CE reduce -> 8H-E pass2 grad -> 8H-F gradient reduce/update -> explicit 8H-G stop.

## Guarded invariants
- no full logits buffer
- no full lm_head weight buffer
- no logits readback
- update must be finite
- A/B delta norms must move when configured
