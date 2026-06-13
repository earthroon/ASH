# SFT-FFN-TEX-ATLAS-05 Bake Report

## Commit

SFT-FFN-TEX-ATLAS-05 — Texture FFN Timing Probe / Storage Buffer Compare Seal

## Base

Baked from `ash_pass3_SFT-FFN-TEX-ATLAS-04A_atomic_active_token_compaction_baked.zip`.

## Added

- `crates/ash_core/src/sft_ffn_texture_atlas_timing_probe.rs`
- `crates/ash_core/tests/sft_ffn_tex_atlas_05_timing_probe.rs`
- `crates/burn_webgpu_backend/src/ffn_texture_atlas_timing_probe.rs`
- `acceptance_reports/SFT-FFN-TEX-ATLAS-05_texture_ffn_timing_probe.md`
- `bake_artifacts/SFT-FFN-TEX-ATLAS-05_BAKE_REPORT.md`
- `bake_artifacts/SFT-FFN-TEX-ATLAS-05_STATIC_VALIDATION.txt`

## Modified

- `crates/ash_core/src/lib.rs`
- `crates/burn_webgpu_backend/src/lib.rs`

## Opened

- texture FFN timing probe execution
- storage baseline timing receipt
- texture padded timing receipt
- texture compacted timing receipt
- storage vs texture compare evidence
- padding skip benefit metric
- speedup ratio recording

## Closed

- texture path promotion candidate
- texture path default switch
- training dispatch
- production dispatch
- SFT training in core
- gradient write in core
- optimizer step in core
- LoRA texture update
- runtime attach
- promotion apply
- current pointer update

## Validation

This environment does not include `cargo`, `rustc`, or `rustfmt`, so runtime compilation was not performed. Static file presence and bracket-balance validation were performed.
