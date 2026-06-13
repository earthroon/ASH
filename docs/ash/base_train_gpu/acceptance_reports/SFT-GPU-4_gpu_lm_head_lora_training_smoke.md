# SFT-GPU-4 Acceptance

## Status

PENDING STATIC BAKE

## Scope

GPU lm_head LoRA training smoke.

## Required Contract

- `target_key = lm_head`
- `artifact_family = module_lora`
- `loss_on = response_only`
- `prompt_loss_tokens = 0`
- `response_loss_tokens > 0`
- trainable tensors are limited to `lm_head.lora_A` and `lm_head.lora_B`
- base model, tokenizer, and base `lm_head.weight` remain frozen
- WGPU/autodiff backend is required
- CPU training fallback is fail-closed

## Implemented Files

- `crates/lora_train/src/gpu_lm_head_lora_smoke.rs`
- `crates/lora_train/src/training.rs`
- `crates/lora_train/src/lib.rs`
- `docs/A_SFT_GPU_DIRECT_LINE.md`

## Gates

- [x] SFT-GPU-3 mask stats are reused and validated before training smoke
- [x] `lm_head` direct-line plan is required
- [x] unsupported/non-WGPU backend fails closed
- [x] prompt labels with `IGNORE_INDEX=-100` are filtered out before CE
- [x] response-token hidden rows are selected for CE
- [x] base `lm_head.weight` is loaded from the full checkpoint
- [x] `TrainableModuleLoraAdapter` is initialized with real base lm_head weight
- [x] optimizer step updates only the LoRA adapter module
- [x] LoRA B norm must change for PASS
- [x] NaN/Inf loss fails closed
- [x] report records `gpu_training_steps > 0` and `cpu_training_steps = 0`

## Known Boundary

Raw gradient norm extraction is not sealed here; the smoke uses Burn autodiff and adapter norm movement as the update proof. Adapter artifact writing is intentionally deferred to SFT-GPU-5.

## Non-goals

- full transformer backward
- q/v/o LoRA training
- safetensors/manifest persistence
- runtime reload/logits delta verification
- generation quality comparison
