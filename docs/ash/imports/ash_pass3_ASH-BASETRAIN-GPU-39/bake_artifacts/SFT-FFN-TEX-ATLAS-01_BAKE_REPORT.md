# SFT-FFN-TEX-ATLAS-01 Bake Report

## Commit

SFT-FFN-TEX-ATLAS-01 — Frozen FFN Weight Texture Atlas Bake / Numeric Fetch Manifest Seal

## Files Added

- `crates/ash_core/src/sft_ffn_texture_atlas.rs`
- `crates/ash_core/tests/sft_ffn_tex_atlas_01_manifest.rs`
- `acceptance_reports/SFT-FFN-TEX-ATLAS-01_frozen_ffn_weight_texture_atlas_bake.md`
- `bake_artifacts/SFT-FFN-TEX-ATLAS-01_BAKE_REPORT.md`
- `bake_artifacts/SFT-FFN-TEX-ATLAS-01_STATIC_VALIDATION.txt`

## Files Modified

- `crates/ash_core/src/lib.rs`

## Opened

- frozen FFN texture atlas bake manifest
- gate/up/down tile map seal
- atlas digest recording
- manifest digest recording
- numeric fetch policy seal
- RGB payload alpha checksum guard mode

## Closed

- shader execution
- FFN projection execution
- SFT training execution in core
- gradient write in core
- optimizer step in core
- trainable LoRA texture update
- runtime attach
- promotion apply
- current pointer update

## Local Runtime Note

This environment has no `cargo`, `rustc`, or `rustfmt`, so runtime compilation and unit tests were not executed here. Static validation artifacts are included.
