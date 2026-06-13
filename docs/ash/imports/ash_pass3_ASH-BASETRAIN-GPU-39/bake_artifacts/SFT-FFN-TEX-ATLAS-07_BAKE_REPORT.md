# SFT-FFN-TEX-ATLAS-07 Bake Report

## Patch

SFT-FFN-TEX-ATLAS-07 — Hybrid Delta Timing Probe / Base Texture + LoRA Buffer Compare Seal

## Added

- `crates/ash_core/src/sft_ffn_texture_atlas_hybrid_timing.rs`
- `crates/ash_core/tests/sft_ffn_tex_atlas_07_hybrid_timing.rs`
- `crates/burn_webgpu_backend/src/ffn_texture_atlas_hybrid_timing.rs`
- `acceptance_reports/SFT-FFN-TEX-ATLAS-07_hybrid_delta_timing_probe.md`

## Modified

- `crates/ash_core/src/lib.rs`
- `crates/burn_webgpu_backend/src/lib.rs`

## Opened

- hybrid timing probe execution
- texture base only timing receipt
- LoRA delta only timing receipt
- texture hybrid timing receipt
- storage hybrid baseline timing receipt
- hybrid vs storage compare evidence
- LoRA delta overhead metric
- hybrid speedup ratio recording

## Kept Closed

- hybrid path promotion candidate
- hybrid path default switch
- hybrid LoRA delta path for training
- hybrid LoRA delta path for production
- LoRA buffer write
- LoRA optimizer step
- LoRA texture update
- SFT training execution in core
- gradient write in core
- optimizer step in core
- runtime attach
- promotion apply
- current pointer update

## SSOT

SFT-FFN-TEX-ATLAS-07 compares texture-base-only, LoRA-delta-only, texture-base-plus-LoRA, and storage-base-plus-LoRA timing evidence and seals speedup, regression, and LoRA delta overhead without promoting the hybrid path.
