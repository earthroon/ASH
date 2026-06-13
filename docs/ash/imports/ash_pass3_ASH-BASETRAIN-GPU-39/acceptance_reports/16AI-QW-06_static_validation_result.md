# 16AI-QW-06 Static Validation Result

## Result

PASS_STATIC

## Checks

- PASS: `crates/tokenizer_core/src/hangul_qwave_sentence_graph.rs` — exists
- PASS: `crates/tokenizer_core/tests/hangul_qwave_sentence_graph.rs` — exists
- PASS: `acceptance_reports/16AI-QW-06_sentence_qwave_transition_graph.md` — exists
- PASS: `bake_artifacts/16AI-QW-06_BAKE_REPORT.md` — exists
- PASS: `crates/tokenizer_core/src/lib.rs` — exists
- PASS: `crates/tokenizer_core/src/hangul_qwave_sentence_graph.rs` — braces_balanced
- PASS: `crates/tokenizer_core/tests/hangul_qwave_sentence_graph.rs` — braces_balanced
- PASS: `crates/tokenizer_core/src/hangul_qwave_sentence_graph.rs` — contains_receipt_builder
- PASS: `crates/tokenizer_core/src/hangul_qwave_sentence_graph.rs` — contains_integrated_builder
- PASS: `crates/tokenizer_core/src/hangul_qwave_sentence_graph.rs` — forbids_tokenizer_dp
- PASS: `crates/tokenizer_core/src/hangul_qwave_sentence_graph.rs` — forbids_sft_lora
- PASS: `crates/tokenizer_core/src/hangul_qwave_sentence_graph.rs` — has_policy
- PASS: `crates/tokenizer_core/src/hangul_qwave_sentence_graph.rs` — has_graph_types
- PASS: `crates/tokenizer_core/tests/hangul_qwave_sentence_graph.rs` — has_10_tests
- PASS: `crates/tokenizer_core/tests/hangul_qwave_sentence_graph.rs` — tests_missing_receipts
- PASS: `crates/tokenizer_core/tests/hangul_qwave_sentence_graph.rs` — tests_dp_mutation
- PASS: `crates/tokenizer_core/src/lib.rs` — exports_module
- PASS: `crates/tokenizer_core/src/lib.rs` — exports_public_api

## Native Test Status

`cargo` and `rustc` are not available in this container, so native Rust tests were not executed here.
