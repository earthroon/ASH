# 16AI-QW-09 Bake Report

## Baked From

`ash_pass3_16AI-QW-08_qwave_tokenizer_shadow_run_no_regression_baked.zip`

## Added / Updated

- `crates/tokenizer_core/src/hangul_qwave_regression_fixtures.rs`
- `crates/tokenizer_core/tests/hangul_qwave_regression_fixtures.rs`
- `acceptance_reports/16AI-QW-09_pulse_vector_regression_fixtures.md`
- `acceptance_reports/16AI-QW-09_static_validation_result.md`
- `bake_artifacts/16AI-QW-09_BAKE_REPORT.md`
- `crates/tokenizer_core/src/lib.rs`

## SSOT

- `QWaveKoreanMinimalPairFixture`
- `QWaveKoreanMinimalPairSnapshot`
- `QWaveKoreanMinimalPairRegressionReport`
- `QWaveKoreanMinimalPairRegressionReceipt`

## Guard Summary

QW-09 validates coda, particle, ending, and addressivity minimal-pair contrast assertions while preserving QW-08 shadow no-regression boundaries. It rejects fixture autofill, expected assertion mutation, byte/unknown fallback regression, protected wrapper leak, surface reconstruction mismatch, token id mutation, vocab augmentation, embedding resize, new token creation, and backend QWave switch.

## Runtime Status

Native Rust test execution was not available in this container because `cargo` and `rustc` were not installed. Static validation was performed instead.
