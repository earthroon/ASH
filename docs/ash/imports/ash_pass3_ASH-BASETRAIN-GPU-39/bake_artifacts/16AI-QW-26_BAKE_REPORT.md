# 16AI-QW-26 Bake Report

## Patch

`16AI-QW-26 — QWave Long-run SFT Telemetry / Drift & Overfit Guard Seal`

## Base ZIP

`ash_pass3_16AI-QW-25_qwave_korean_minimal_pair_eval_baked.zip`

## Added / modified files

- Added: `crates/lora_train/src/qwave_long_run_sft_telemetry.rs`
- Added: `crates/lora_train/tests/qwave_long_run_sft_telemetry.rs`
- Modified: `crates/lora_train/src/lib.rs`
- Added: `acceptance_reports/16AI-QW-26_qwave_long_run_sft_telemetry.md`
- Added: `acceptance_reports/16AI-QW-26_static_validation_result.md`
- Added: `bake_artifacts/16AI-QW-26_BAKE_REPORT.md`

## Implemented SSOT

- `QWaveLongRunSftTelemetryInput`
- `QWaveLongRunKoreanEvalRef`
- `QWaveLongRunTelemetryWindow`
- `QWaveLongRunSftTelemetrySnapshot`
- `QWaveLongRunDriftScoreReport`
- `QWaveLongRunOverfitGuardReport`
- `QWaveLongRunNonKoreanRegressionReport`
- `QWaveLongRunAdapterDeltaDriftReport`
- `QWaveLongRunKoreanEvalDriftReport`
- `QWaveLongRunSftTelemetryManifest`
- `QWaveLongRunSftTelemetryPlan`
- `QWaveLongRunSftTelemetryReceipt`

## Implemented guards

- QW-25 Korean eval receipt guard
- Korean eval no-regression source guard
- Telemetry window guard
- Min train/eval step guard
- Sandboxed telemetry guard
- Telemetry-only source guard
- Finite telemetry guard
- Loss/gradient/QWave coverage drift guard
- Adapter delta drift guard
- Korean eval drift guard
- Non-Korean regression guard
- Overfit guard
- Base/token/vocab/embedding unchanged guard
- Adapter/current/artifact pointer unchanged guard
- Production state unchanged guard
- Training promotion/runtime apply rejection guard

## Static validation

STATIC_VALIDATION: PASS

## Native Rust validation

NATIVE_RUST_TEST: NOT_RUN_TOOLCHAIN_UNAVAILABLE

Recommended native command:

```bash
cargo test -p lora_train qwave_long_run_sft_telemetry
```

## Seal

QW-26 creates long-run telemetry evidence only. It does not perform training promotion, production training apply, runtime apply, pointer mutation, tokenizer mutation, or silent fallback.
