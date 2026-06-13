# SFT-GPU-8H-C2 actual pass1 GPU projection kernel

## Status
PASS_STATIC / PASS_PASS1_GPU_KERNEL_SMOKE_READY

## Sealed
- `lm_head_vocab_atlas_gpu_pass1_kernel.rs`
- `GpuPass1KernelConfig`
- `dispatch_pass1_projection_kernel(...)`
- `cpu_reference_pass1_group(...)`
- fixture target-capture parity
- group-local Burn/WGPU tensor matmul projection smoke

## Memory discipline
- full `lm_head.weight [vocab,hidden]` buffer remains forbidden
- full logits `[active_tokens,vocab]` buffer remains forbidden
- only group-local logits are materialized for the C2 smoke bridge
- group logits readback is explicitly marked as `group_logits_readback_for_smoke=true`; it is not the final 8H-D readback discipline

## Next
SFT-GPU-8H-D global CE reduce kernel.
