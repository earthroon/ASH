# 16AI-QW-18 Bake Report

## Patch

`16AI-QW-18 — QWave SFT Ablation Eval / Baseline vs Feature Side-channel Seal`

## Base

`ash_pass3_16AI-QW-17_qwave_sft_train_dry_run_baked.zip`

## Added Files

- `crates/lora_train/src/qwave_sft_ablation_eval.rs`
- `crates/lora_train/tests/qwave_sft_ablation_eval.rs`
- `acceptance_reports/16AI-QW-18_qwave_sft_ablation_eval.md`
- `acceptance_reports/16AI-QW-18_static_validation_result.md`
- `bake_artifacts/16AI-QW-18_BAKE_REPORT.md`

## Modified Files

- `crates/lora_train/src/lib.rs`

## Implemented SSOT

- `QWaveSftAblationEvalInput`
- `QWaveSftAblationEvalPolicy`
- `QWaveSftAblationEvalRequestedMutations`
- `QWaveSftAblationGroupKind`
- `QWaveSftAblationGroupSnapshot`
- `QWaveSftAblationMetricSnapshot`
- `QWaveSftKoreanEvalMetricSnapshot`
- `QWaveSftAblationComparisonReport`
- `QWaveSftAblationOutcome`
- `QWaveSftAblationRecommendation`
- `QWaveSftAblationEvalManifest`
- `QWaveSftAblationEvalPlan`
- `QWaveSftAblationEvalReceipt`

## Implemented Guards

- QW-17 dry-run receipt guard
- Baseline group kind guard
- Eval-only ablation group guard
- Finite metrics guard
- Minimum eval sample guard
- Auto-promotion reject guard
- Sample weight / curriculum / runtime apply reject guard
- Loss / gradient / optimizer / scheduler / adapter / sampler / backend mutation reject guard

## Test Fixture Count

35 static Rust test functions added in `crates/lora_train/tests/qwave_sft_ablation_eval.rs`.

## Native Test Status

`NATIVE_RUST_TEST: NOT_RUN_TOOLCHAIN_UNAVAILABLE`
