# SFT-FFN-LORA-13 Bake Report

## Patch

SFT-FFN-LORA-13 — Current Adapter Rollback Drill / Failure Recovery Simulation Seal

## Base

Baked on top of `SFT-FFN-LORA-12_post_switch_health`.

## Added

- `crates/ash_core/src/sft_ffn_lora_rollback_drill.rs`
- `crates/ash_core/tests/sft_ffn_lora_13_rollback_drill.rs`
- `crates/burn_webgpu_backend/src/ffn_lora_rollback_drill.rs`
- `crates/burn_webgpu_backend/tests/ffn_lora_rollback_drill.rs`
- `acceptance_reports/SFT-FFN-LORA-13_rollback_drill.md`
- `bake_artifacts/SFT-FFN-LORA-13_STATIC_VALIDATION.txt`
- `bake_artifacts/SFT-FFN-LORA-13_FILE_DIGESTS.sha256`

## Modified

- `crates/ash_core/src/lib.rs`
- `crates/burn_webgpu_backend/src/lib.rs`

## Opened

- rollback drill simulation
- failure injection fixture
- rollback handle resolution
- rollback simulation evidence
- fallback candidate
- demotion candidate
- quarantine candidate
- textureLoad drill guard
- no production mutation guard

## Closed

- production rollback execution
- current pointer update
- promotion apply rerun
- demotion apply
- quarantine apply
- SFT training execution in core
- gradient write in core
- optimizer step in core
- textureSample weight fetch

## Validation

Static validation only in this environment. Local Rust toolchain execution is pending.
