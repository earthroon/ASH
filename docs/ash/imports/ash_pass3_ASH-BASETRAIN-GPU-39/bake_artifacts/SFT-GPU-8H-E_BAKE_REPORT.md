# SFT-GPU-8H-E Bake Report

## Baked changes
- Added `crates/lora_train/src/lm_head_vocab_atlas_gpu_pass2_grad.rs`.
- Added pass2 gradient config, layout, buffers, report, fixture parity, policy validation, dispatch smoke, and report writer.
- Connected 8H-D global CE reduce output to 8H-E pass2 gradient smoke path.
- Added group iteration for pass2 grad over all vocab tile groups.
- Preserved full logits / full lm_head weight prohibition.
- Added a support fix so pass1 group partial buffers preserve prior group rows while updating the current group row.

## Runtime handoff
Expected terminal message after 8H-E smoke:

`SFT-GPU-8H-E sealed pass2 GPU gradient kernel; partial gradient reduce/update is scheduled for SFT-GPU-8H-F`

## Not included
- Final grad_A reduce.
- A/B optimizer update.
- Adapter export.
- Runtime delta verification.
