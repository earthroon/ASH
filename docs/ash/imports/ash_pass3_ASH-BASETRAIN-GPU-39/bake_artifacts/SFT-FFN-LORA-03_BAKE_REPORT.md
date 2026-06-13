# SFT-FFN-LORA-03 Bake Report

## Patch

SFT-FFN-LORA-03 — LoRA Optimizer Step Candidate / Adapter Weight Update Guard

## Base

Baked on top of `ash_pass3_SFT-FFN-LORA-02_ffn_down_projection_lora_gradient_receipt_baked.zip`.

## Added

- `crates/ash_core/src/sft_ffn_lora_optimizer.rs`
- `crates/ash_core/tests/sft_ffn_lora_03_optimizer_step_candidate.rs`
- `crates/burn_webgpu_backend/src/ffn_lora_optimizer.rs`
- `acceptance_reports/SFT-FFN-LORA-03_lora_optimizer_step_candidate.md`
- `bake_artifacts/SFT-FFN-LORA-03_BAKE_REPORT.md`
- `bake_artifacts/SFT-FFN-LORA-03_STATIC_VALIDATION.txt`

## Modified

- `crates/ash_core/src/lib.rs`
- `crates/burn_webgpu_backend/src/lib.rs`

## Opened

- LoRA optimizer step candidate
- LoRA buffer write for candidate update
- LoRA optimizer step candidate evidence
- LoRA weight pre/post digest
- LoRA update digest
- LoRA update norm recording
- Optimizer state mutation evidence

## Closed

- LoRA texture update
- SFT training in core
- Gradient write in core
- Optimizer step in core
- Artifact write
- Runtime attach
- Promotion apply
- Current pointer update

## Validation

Static validation completed in the current environment. `cargo`, `rustc`, and `rustfmt` were not available here, so compile/runtime validation remains pending for the local environment.
