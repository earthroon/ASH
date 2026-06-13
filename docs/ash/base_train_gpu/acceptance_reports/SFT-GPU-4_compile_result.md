# SFT-GPU-4 Compile Result

## Status

NOT RUN IN SANDBOX

## Reason

`cargo` and `rustc` are not available in the current execution sandbox.

## Required local command

```powershell
cargo run -p lora_train --bin lora_train -- `
  .\configs\ash_ko_short_sft_lm_head_lora_v1_smoke.json 1
```

## Expected SFT-GPU-4 runtime boundary

- `[lora_train][sft_mask] prompt_loss_tokens=0 response_loss_tokens=...`
- `[lora_train][gpu_lm_head_lora] backend=...wgpu...`
- `[lora_train][gpu_lm_head_lora] smoke PASS gpu_training_steps=... cpu_training_steps=0`
