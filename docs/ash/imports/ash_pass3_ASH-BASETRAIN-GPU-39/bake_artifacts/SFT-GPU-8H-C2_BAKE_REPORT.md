# SFT-GPU-8H-C2 Bake Report

Implemented the actual pass1 GPU projection smoke path using the existing Burn/WGPU tensor backend:

- stages `W_group [Vg,H]` only, never full lm_head `[V,H]`
- stages `B_group [Vg,R]`
- computes base projection and LoRA projection with GPU tensor matmul
- reduces group-local logits into partial max / sum-exp / target capture
- updates pass1 partial buffers for the smoke group
- adds CPU fixture parity for target capture and math contract

Note: this is the first actual GPU projection smoke. It is not yet the fused raw WGSL/CubeCL kernel and still has a group-local readback for C2 smoke validation. The full logits buffer and full lm_head buffer remain forbidden.
