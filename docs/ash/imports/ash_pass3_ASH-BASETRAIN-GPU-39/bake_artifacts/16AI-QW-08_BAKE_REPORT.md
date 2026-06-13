# 16AI-QW-08 Bake Report

## Baked From

- Base artifact: `ash_pass3_16AI-QW-07_qwave_tokenizer_dp_cost_bridge_baked.zip`

## Added / Modified Files

- `crates/tokenizer_core/src/hangul_qwave_shadow_run.rs`
- `crates/tokenizer_core/tests/hangul_qwave_shadow_run.rs`
- `acceptance_reports/16AI-QW-08_qwave_tokenizer_shadow_run_no_regression.md`
- `acceptance_reports/16AI-QW-08_static_validation_result.md`
- `bake_artifacts/16AI-QW-08_BAKE_REPORT.md`
- `crates/tokenizer_core/src/lib.rs`

## SSOT

- `QWaveTokenizerShadowRunPlan`
- `QWaveTokenizerShadowDiff`
- `QWaveTokenizerShadowRunReceipt`

## Sealed Contract

QW-08 consumes QW-07 DP bridge evidence and compares a baseline tokenizer run with a QWave-adjusted shadow tokenizer run. Shadow token ids may differ from baseline, but committed token ids must remain unchanged. The seal rejects byte fallback regression, unknown token regression, protected wrapper leak, surface reconstruction mismatch, special token boundary mismatch, vocab augmentation, embedding resize, new token creation, runtime tokenizer mutation, SFT export, LoRA routing hint creation, and backend QWave switch.

## Runtime Status

Native Rust tests were not executed in this container because `cargo`/`rustc` are unavailable. Static validation was performed instead.
