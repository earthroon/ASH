# SFT-FFN-LORA-11 Bake Report

## Commit

SFT-FFN-LORA-11 — Current Pointer Switch / Rollback Commit Seal + TextureLoad Weight Fetch Guard

## Base

Baked on top of SFT-FFN-LORA-10 / GPU-SAFETY-01 line.

## Added

- `crates/ash_core/src/sft_ffn_lora_current_pointer_switch.rs`
- `crates/ash_core/src/sft_ffn_texture_load_guard.rs`
- `crates/ash_core/tests/sft_ffn_lora_11_current_pointer_switch.rs`
- `crates/ash_core/tests/sft_ffn_texture_load_guard_01.rs`
- `crates/burn_webgpu_backend/src/ffn_lora_current_pointer_switch.rs`
- `crates/burn_webgpu_backend/src/ffn_texture_load_guard.rs`
- `crates/burn_webgpu_backend/tests/ffn_texture_load_guard_01.rs`
- `acceptance_reports/SFT-FFN-LORA-11_current_pointer_switch.md`

## Modified

- `crates/ash_core/src/lib.rs`
- `crates/burn_webgpu_backend/src/lib.rs`

## Opened

- current pointer switch
- promotion apply commit
- rollback commit
- failure recovery path
- slot ready mark
- approved ASH binding
- textureLoad weight fetch guard

## Kept Closed

- unreviewed adapter attach
- textureSample weight fetch
- sampler based weight fetch
- normalized UV weight fetch
- SFT training execution in core
- gradient write in core
- optimizer step in core

## Notes

The FFN shader scan confirms executable FFN WGSL weight atlas paths use `textureLoad` with integer texel coordinates and mip level 0. Existing `textureSample` mentions in FFN shader files are comments only; no `textureSample(` call is present in the targeted FFN weight shader bodies.
