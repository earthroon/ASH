# 16AI-QW-11 Bake Report

## Baked on top of

`ash_pass3_16AI-QW-10_qwave_graph_serialization_diagnostic_baked.zip`

## Added files

- `crates/tokenizer_core/src/hangul_qwave_sft_feature_export.rs`
- `crates/tokenizer_core/tests/hangul_qwave_sft_feature_export.rs`
- `acceptance_reports/16AI-QW-11_qwave_sft_feature_export.md`
- `acceptance_reports/16AI-QW-11_static_validation_result.md`
- `bake_artifacts/16AI-QW-11_BAKE_REPORT.md`

## Modified files

- `crates/tokenizer_core/src/lib.rs`

## Seal

This bake adds the QWave SFT feature export layer. It turns QWave trace-aligned token spans into a deterministic `batch × sequence × qwave_feature_dim` side-channel feature matrix with feature and coverage masks.

## Forbidden side effects

- token id mutation
- vocab augmentation
- embedding resize
- new token creation
- direct logit mutation
- loss function mutation
- LoRA routing hint creation
- backend QWave switch
- QWave graph recompute
- tokenizer rerun

## Runtime status

Native Rust tests were not executed in this container because `cargo` / `rustc` are unavailable.
