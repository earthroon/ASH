# SFT-FFN-TEX-ATLAS-03 Bake Report

## Commit

SFT-FFN-TEX-ATLAS-03 — Batched Token Texture FFN Dispatch / Atlas Group Parallel Seal

## Added

- `crates/ash_core/src/sft_ffn_texture_atlas_batched_dispatch.rs`
- `crates/ash_core/tests/sft_ffn_tex_atlas_03_batched_dispatch.rs`
- `crates/burn_webgpu_backend/src/ffn_texture_atlas_batched_dispatch.rs`
- `crates/burn_webgpu_backend/src/shaders/ffn_texture_atlas_batched_projection.wgsl`
- `acceptance_reports/SFT-FFN-TEX-ATLAS-03_batched_token_texture_ffn_dispatch.md`
- `bake_artifacts/SFT-FFN-TEX-ATLAS-03_BAKE_REPORT.md`
- `bake_artifacts/SFT-FFN-TEX-ATLAS-03_STATIC_VALIDATION.txt`

## Modified

- `crates/ash_core/src/lib.rs`

## Opened

- Batched texture FFN dispatch smoke path
- Adapter-scoped token group seal
- Input hidden group digest recording
- Output group digest recording
- Dispatch shape digest recording
- Scratch budget evidence recording

## Kept Closed

- Batched dispatch for training
- Batched dispatch for production
- Batched dispatch as default
- SFT training in core
- Gradient write in core
- Optimizer step in core
- Trainable LoRA texture update
- Runtime attach
- Promotion apply
- Current pointer update

## Notes

This bake keeps the backend shader as a shell/spec artifact and does not wire it as the default production path. Runtime GPU validation remains pending.
