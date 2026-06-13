# SFT-GPU-8H-F partial gradient reduce + update kernel

## Status
PASS_STATIC / PASS_GRADIENT_REDUCE_UPDATE_KERNEL_SMOKE

## Sealed
- `grad_lora_mid`: `[active_tokens, rank]`
- `grad_A`: `[rank, hidden_size]`
- `grad_B`: `[vocab_size, rank]`
- LoRA A update via `sgd_smoke`
- LoRA B update via `sgd_smoke`

## Guards
- full logits buffer forbidden
- logits readback forbidden
- NaN update forbidden
- `update_mode=sgd_smoke` required
- nonzero A/B delta norm required when configured

## Runtime handoff
This stage closes the first loss -> gradient -> LoRA A/B delta loop for the GPU-parallel lm_head vocab atlas path.

## Next
SFT-GPU-8H-G timing profiler / adapter export / no-readback discipline.
