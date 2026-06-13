# 16AI-QW-10 Bake Report

## Baked From

`ash_pass3_16AI-QW-09_pulse_vector_regression_fixtures_baked.zip`

## Added / Modified

- `crates/tokenizer_core/src/hangul_qwave_graph_serialization.rs`
- `crates/tokenizer_core/tests/hangul_qwave_graph_serialization.rs`
- `acceptance_reports/16AI-QW-10_qwave_graph_serialization_diagnostic.md`
- `acceptance_reports/16AI-QW-10_static_validation_result.md`
- `bake_artifacts/16AI-QW-10_BAKE_REPORT.md`
- `crates/tokenizer_core/src/lib.rs`

## Seal

QW-10 serializes QWave graph snapshots into stable trace receipts and a Markdown diagnostic manifest without recomputing graph values or mutating tokenizer/vocab/backend state.

## Guard Summary

- QW-09 regression receipt required
- required trace files must be created and nonempty
- trace ordering must be stable
- Markdown diagnostic required
- graph recompute forbidden
- fixture assertion mutation forbidden
- token id mutation forbidden
- vocab augmentation forbidden
- embedding resize forbidden
- new token creation forbidden
- production tokenizer commit forbidden
- SFT feature export forbidden
- LoRA routing hint creation forbidden
- backend QWave switch forbidden

## Native Test Status

`cargo` / `rustc` were not available in this container, so native Rust tests were not executed. Static validation was performed instead.
