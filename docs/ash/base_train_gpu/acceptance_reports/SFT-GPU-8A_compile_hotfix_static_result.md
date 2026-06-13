# SFT-GPU-8A Compile Hotfix Static Result

## Status

STATIC-PASS / RUNTIME-PENDING

## Input failure log

- E0599: `TrainableModuleLoraAdapter<B>` had no `.loss(...)` method.
- E0063: `pipeline.rs::build_config_from_specs()` did not initialize newly added strict config fields.

## Patched files

- `crates/lora_train/src/gpu_lm_head_lora_smoke.rs`
- `crates/lora_train/src/pipeline.rs`

## Fixes

### 1. `gpu_lm_head_lora_smoke.rs`

Replaced the invalid `.loss(...)` call on `TrainableModuleLoraAdapter<B>` with a local response-only CE helper:

- uses `TrainableModuleLoraAdapter::forward_project(...)`
- flattens hidden states from `[batch, seq, hidden]` to `[tokens, hidden]`
- reshapes targets to `[tokens]`
- applies Burn `CrossEntropyLoss`
- keeps SFT-GPU-3 response-only filtering before CE

### 2. `pipeline.rs`

Updated `build_config_from_specs()` struct initializers after strict schema expansion:

- `LoraTrainConfig`: `family`, `mode`, `lora`, `guards`, `a_sft_native_contract`
- `DatasetConfig`: `format`, `template`, `loss_on`, `prompt_max_tokens`, `response_max_tokens`, `append_eos`
- `OptimizerConfig`: `grad_clip`
- `LoggingConfig`: `report_loss`, `report_tokens_per_sec`

## Static checks

- The invalid `.loss(...)` call in `gpu_lm_head_lora_smoke.rs` is removed.
- The local helper `lm_head_response_only_ce_loss(...)` exists.
- `CrossEntropyLoss` import exists.
- Required strict config fields are initialized in `pipeline.rs::build_config_from_specs()`.

## Runtime status

Cargo/rustc are unavailable in this sandbox, so compile execution remains pending in the user environment.

Run:

```powershell
cargo check -p lora_train
```

or:

```powershell
cargo run -p lora_train --bin lora_train -- `
  .\configs\ash_ko_short_sft_lm_head_lora_v1_smoke.json 1
```
