# SFT-FFN-TEX-ATLAS-04A Bake Report

## Commit

SFT-FFN-TEX-ATLAS-04A — Atomic Active Token Compaction / Padding Skip Counter Seal

## Added

- `crates/ash_core/src/sft_ffn_texture_atlas_atomic_compaction.rs`
- `crates/ash_core/tests/sft_ffn_tex_atlas_04a_atomic_compaction.rs`
- `crates/burn_webgpu_backend/src/ffn_texture_atlas_atomic_compaction.rs`
- `crates/burn_webgpu_backend/src/shaders/ffn_texture_atlas_atomic_compaction.wgsl`
- `acceptance_reports/SFT-FFN-TEX-ATLAS-04A_atomic_active_token_compaction.md`
- `bake_artifacts/SFT-FFN-TEX-ATLAS-04A_BAKE_REPORT.md`
- `bake_artifacts/SFT-FFN-TEX-ATLAS-04A_STATIC_VALIDATION.txt`

## Modified

- `crates/ash_core/src/lib.rs`
- `crates/burn_webgpu_backend/src/lib.rs`

## Opened

- atomic active token compaction prepass
- global atomic active-token counter
- padding mask digest recording
- active indices digest recording
- active token count recording
- padding skip ratio recording
- counter reset receipt

## Closed

- dispatchIndirect args write
- FFN batched dispatch execution
- FFN dispatchIndirect execution
- atomic in FFN dot product
- atomic output accumulation
- SFT training execution in core
- gradient write in core
- optimizer step in core
- LoRA texture update
- runtime attach
- promotion apply
- current pointer update

## Notes

The WGSL shader shell performs active token compaction only. It does not execute FFN projection, does not write dispatchIndirect args, and does not update trainable LoRA weights.
