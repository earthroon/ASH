# SFT-GPU-8H-E pass2 GPU gradient kernel

## Status
PASS_STATIC / PASS_PASS2_GPU_GRAD_KERNEL_SMOKE

## Sealed
- `lora_mid`: `[active_tokens, rank]`
- `grad_lora_mid_partial`: `[group_count, active_tokens, rank]`
- `grad_B`: `[vocab_size, rank]`
- pass2 policy guard for no full logits buffer
- group-local target one-hot subtraction report
- mean-loss normalization report

## Guards
- full logits buffer forbidden
- logits readback forbidden
- readback policy remains `loss_and_report_only`
- gradient finite checks required
- target subtraction must occur across the complete vocab partition

## Scope
This commit seals pass2 softmax-gradient and LoRA partial-gradient buffers. It does not perform final partial-gradient reduce or A/B update.

## Next
SFT-GPU-8H-F partial gradient reduce + update kernel.
