# 16AI-QW-27 Bake Report

## Patch

`16AI-QW-27 — QWave Training Mode Promotion Gate / Operator Approval Queue Seal`

## Base

`ash_pass3_16AI-QW-26_qwave_long_run_sft_telemetry_baked.zip`

## Added / Modified Files

- `crates/lora_train/src/qwave_training_mode_promotion_gate.rs`
- `crates/lora_train/tests/qwave_training_mode_promotion_gate.rs`
- `crates/lora_train/src/lib.rs`
- `acceptance_reports/16AI-QW-27_qwave_training_mode_promotion_gate.md`
- `acceptance_reports/16AI-QW-27_static_validation_result.md`
- `bake_artifacts/16AI-QW-27_BAKE_REPORT.md`

## New SSOT Types

- `QWaveTrainingModePromotionGateInput`
- `QWaveTrainingModePromotionLongRunRef`
- `QWaveTrainingModePromotionOperatorRequest`
- `QWaveTrainingModeRollbackPrerequisite`
- `QWaveTrainingModePromotionEligibilityReport`
- `QWaveTrainingModePromotionQueueEntry`
- `QWaveTrainingModePromotionGateManifest`
- `QWaveTrainingModePromotionGatePlan`
- `QWaveTrainingModePromotionGateReceipt`

## Core Contract

QW-27 consumes the QW-26 long-run telemetry receipt and creates an operator approval queue entry for QWave training mode promotion. It is a promotion gate only. It does not apply training mode, runtime mode, current pointer changes, artifact pointer changes, adapter pointer changes, base model mutations, tokenizer mutations, or sampler changes.

## Validation

- Static validation: PASS
- Test function count: 54
- Native Rust test: NOT_RUN_TOOLCHAIN_UNAVAILABLE

## Recommended Native Check

```bash
cargo test -p lora_train qwave_training_mode_promotion_gate
```
