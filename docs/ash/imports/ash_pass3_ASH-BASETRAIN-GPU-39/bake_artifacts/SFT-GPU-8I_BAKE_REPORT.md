# SFT-GPU-8I Bake Report

## Status
PASS_STATIC

## Added
- `lm_head_vocab_atlas_gpu_adamw.rs`
- `lm_head_vocab_atlas_gpu_multistep.rs`
- `lm_head_vocab_atlas_gpu_checkpoint.rs`
- config schema for AdamW / multi-step / guards / checkpoint
- `multi_step_train` config block
- static validation script

## Runtime behavior
After 8H-H runtime delta verify succeeds, the 8I path writes:
- `multi_step_train_report.json/.md`
- `loss_trace.json`
- `training_state.json`
- `optimizer_state.safetensors.json`
- interval checkpoint reports

## Limitation
This 8I bake seals the AdamW multi-step control/checkpoint SSOT from the 8H-G single train-step metrics. Full repeated all-group GPU redispatch is staged for 8I-B once this control loop compiles in the target environment.
