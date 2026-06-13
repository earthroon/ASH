# SFT-GPU-8G1 Compile Initializer Fix

## Status

PASS_STATIC_PATCHED

## Fixed

- Added `lm_head_vocab_atlas: None` to the manual `LoraTrainConfig` initializer in `crates/lora_train/src/pipeline.rs`.
- Updated `tools/validate_sft_gpu_8g_static.py` to guard this initializer so the same compile break does not silently return.

## Reason

Rust error `E0063` reported that `LoraTrainConfig` had a new field, but `build_config_from_specs()` still constructed the struct without initializing `lm_head_vocab_atlas`.

## Validation

`python tools/validate_sft_gpu_8g_static.py` reports 19 static passes.

## Runtime

Not executed in this sandbox. Run the same target command in the Rust/WGPU environment.
