# SFT-FFN-TEX-ATLAS-06 Bake Report

## Commit

SFT-FFN-TEX-ATLAS-06 — Hybrid Base Texture + LoRA Buffer Delta Path / SFT Adapter Seal

## Added

- `crates/ash_core/src/sft_ffn_texture_atlas_hybrid_lora.rs`
- `crates/ash_core/tests/sft_ffn_tex_atlas_06_hybrid_lora.rs`
- `crates/burn_webgpu_backend/src/ffn_texture_atlas_hybrid_lora.rs`
- `crates/burn_webgpu_backend/src/shaders/ffn_texture_atlas_hybrid_lora.wgsl`
- `acceptance_reports/SFT-FFN-TEX-ATLAS-06_hybrid_base_texture_lora_buffer_delta.md`

## Modified

- `crates/ash_core/src/lib.rs`
- `crates/burn_webgpu_backend/src/lib.rs`

## Opened

- hybrid LoRA delta smoke path
- LoRA buffer read
- base texture output reference
- LoRA delta digest recording
- hybrid output digest recording
- delta norm recording

## Closed

- hybrid LoRA training path
- hybrid LoRA production path
- hybrid LoRA default path
- LoRA buffer write
- LoRA optimizer step
- LoRA texture update
- SFT training in core
- gradient write in core
- optimizer step in core
- runtime attach
- promotion apply
- current pointer update

## Notes

This bake intentionally treats frozen base FFN weights as texture-atlas inputs and LoRA A/B as storage-buffer inputs. It does not promote the hybrid path to production and does not perform optimizer updates.
