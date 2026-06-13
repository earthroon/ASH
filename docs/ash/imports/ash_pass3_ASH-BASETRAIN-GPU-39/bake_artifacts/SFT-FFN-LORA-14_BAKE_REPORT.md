# SFT-FFN-LORA-14 Bake Report

## Patch

SFT-FFN-LORA-14 — Multi-Adapter Current Registry / Slot Health Arbitration Seal

## Base

Baked on top of `ash_pass3_SFT-FFN-LORA-13_rollback_drill_baked.zip`.

## Added

- `crates/ash_core/src/sft_ffn_lora_slot_arbitration.rs`
- `crates/ash_core/tests/sft_ffn_lora_14_slot_arbitration.rs`
- `crates/burn_webgpu_backend/src/ffn_lora_slot_arbitration.rs`
- `crates/burn_webgpu_backend/tests/ffn_lora_slot_arbitration.rs`
- `acceptance_reports/SFT-FFN-LORA-14_slot_arbitration.md`
- `bake_artifacts/SFT-FFN-LORA-14_BAKE_REPORT.md`
- `bake_artifacts/SFT-FFN-LORA-14_STATIC_VALIDATION.txt`
- `bake_artifacts/SFT-FFN-LORA-14_FILE_DIGESTS.sha256`

## Modified

- `crates/ash_core/src/lib.rs`
- `crates/burn_webgpu_backend/src/lib.rs`

## Opened

- multi-adapter current registry snapshot
- slot health arbitration
- rollback readiness comparison
- fallback readiness comparison
- textureLoad guard table
- active adapter recommendation
- demotion recommendation candidate
- quarantine recommendation candidate
- no mutation guard

## Closed

- current pointer update
- promotion apply rerun
- rollback execution
- demotion apply
- quarantine apply
- SFT training execution in core
- gradient write in core
- optimizer step in core
- textureSample weight fetch

## Validation

Static file checks were performed in the baking environment. `cargo`, `rustc`, and `rustfmt` are not available in this environment, so runtime compilation must be verified locally.
