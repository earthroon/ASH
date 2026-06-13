# 16AI-QW-26 Static Validation Result

## Result

STATIC_VALIDATION: PASS  
NATIVE_RUST_TEST: NOT_RUN_TOOLCHAIN_UNAVAILABLE

## Checked files

- `crates/lora_train/src/qwave_long_run_sft_telemetry.rs`: PRESENT
- `crates/lora_train/tests/qwave_long_run_sft_telemetry.rs`: PRESENT
- `crates/lora_train/src/lib.rs`: EXPORTS PRESENT
- `acceptance_reports/16AI-QW-26_qwave_long_run_sft_telemetry.md`: PRESENT
- `bake_artifacts/16AI-QW-26_BAKE_REPORT.md`: PRESENT

## Required symbols

- `QWaveLongRunSftTelemetryReceipt`: PRESENT
- `QWaveLongRunKoreanEvalRef`: PRESENT
- `QWaveLongRunTelemetryWindow`: PRESENT
- `QWaveLongRunSftTelemetrySnapshot`: PRESENT
- `QWaveLongRunDriftScoreReport`: PRESENT
- `QWaveLongRunOverfitGuardReport`: PRESENT
- `QWaveLongRunNonKoreanRegressionReport`: PRESENT
- `QWaveLongRunAdapterDeltaDriftReport`: PRESENT
- `QWaveLongRunKoreanEvalDriftReport`: PRESENT
- `QWaveLongRunTelemetryOutcome`: PRESENT
- `QWaveLongRunTelemetryRecommendation`: PRESENT
- `AcceptedLongRunTelemetry`: PRESENT
- `RejectedMissingQw25KoreanEvalReceipt`: PRESENT
- `RejectedKoreanEvalRegressionSource`: PRESENT
- `RejectedInsufficientTrainSteps`: PRESENT
- `RejectedInsufficientEvalSteps`: PRESENT
- `RejectedNonFiniteTelemetry`: PRESENT
- `RejectedLossDrift`: PRESENT
- `RejectedGradientDrift`: PRESENT
- `RejectedOverfitSignal`: PRESENT
- `RejectedNonKoreanRegression`: PRESENT
- `RejectedAdapterDeltaDrift`: PRESENT
- `RejectedKoreanEvalDrift`: PRESENT

## Test count

- Test functions in `qwave_long_run_sft_telemetry.rs`: 53
- Required minimum: 40

## Brace balance

- Source brace balance: PASS
- Test brace balance: PASS

## Native Rust test

The current container has no `cargo` / `rustc` toolchain available, so native Rust tests were not executed in-container.
