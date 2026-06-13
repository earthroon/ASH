# SFT-FFN-LORA-02 Bake Report

## Commit

SFT-FFN-LORA-02 — FFN Down Projection LoRA Backward Gradient Receipt / No Optimizer Step Seal

## Baked On

ash_pass3_SFT-FFN-LORA-01_ffn_down_projection_lora_target_baked.zip

## Files Added

- crates/ash_core/src/sft_ffn_lora_gradient.rs
- crates/ash_core/tests/sft_ffn_lora_02_backward_gradient_receipt.rs
- crates/burn_webgpu_backend/src/ffn_lora_gradient.rs
- acceptance_reports/SFT-FFN-LORA-02_ffn_down_projection_lora_gradient_receipt.md
- bake_artifacts/SFT-FFN-LORA-02_BAKE_REPORT.md
- bake_artifacts/SFT-FFN-LORA-02_STATIC_VALIDATION.txt

## Files Modified

- crates/ash_core/src/lib.rs
- crates/burn_webgpu_backend/src/lib.rs

## Opened

- FFN down projection LoRA backward gradient receipt
- Loss source evidence
- Backward pass evidence
- LoRA A/B gradient digest receipt
- Gradient shape contract
- Gradient norm evidence
- Weight mutation guard

## Closed

- Gradient accumulation receipt
- LoRA buffer write
- LoRA optimizer step
- LoRA texture update
- SFT training execution in core
- Gradient write in core
- Optimizer step in core
- Artifact write
- Runtime attach
- Promotion apply
- Current pointer update

## Notes

This bake adds a receipt-only gradient gate. It can accept GPU-native backward gradient evidence for the FFN down projection LoRA target, but it explicitly refuses weight mutation, optimizer step, artifact write, runtime attach, promotion, and current pointer changes.
