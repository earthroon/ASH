# SFT-FFN-LORA-04 Bake Report

## Commit

SFT-FFN-LORA-04 — Updated Adapter Delta Smoke / Pre-Post Weight Diff Seal

## Added

- `crates/ash_core/src/sft_ffn_lora_delta_smoke.rs`
- `crates/ash_core/tests/sft_ffn_lora_04_updated_adapter_delta_smoke.rs`
- `crates/burn_webgpu_backend/src/ffn_lora_delta_smoke.rs`
- `acceptance_reports/SFT-FFN-LORA-04_updated_adapter_delta_smoke.md`
- `bake_artifacts/SFT-FFN-LORA-04_BAKE_REPORT.md`
- `bake_artifacts/SFT-FFN-LORA-04_STATIC_VALIDATION.txt`

## Modified

- `crates/ash_core/src/lib.rs`
- `crates/burn_webgpu_backend/src/lib.rs`

## Opened

- updated adapter delta smoke
- pre/post LoRA delta digest
- pre/post hybrid output digest
- delta diff digest
- hybrid output diff digest
- delta diff norm recording
- hybrid output diff norm recording
- side effect guard

## Closed

- artifact write
- runtime attach
- promotion apply
- current pointer update
- LoRA texture update
- SFT training in core
- gradient write in core
- optimizer step in core

## Local Runtime Validation

`cargo`, `rustc`, and `rustfmt` were unavailable in this environment. Static validation only.
