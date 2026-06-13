# 16AI-QW-38G-R6A-WCTX-MOCK-15 Acceptance Report

## Acceptance Contract

`WCTX-MOCK-15` passes when the negative matrix satisfies:

- `total_cases >= 20`
- `expectation_mismatched_cases == 0`
- `all_negative_cases_blocked == true`
- `chain_indexed_unexpected_count == 0`
- `runtime_apply_leak_detected_count >= 3`
- `production_safe_leak_detected_count >= 1`
- `mock_mislabeled_as_runtime_detected_count >= 1`
- `no_runtime_decode_executed == true`
- `no_generation_executed == true`
- `no_model_forward_executed == true`
- `no_sampling_executed == true`
- `no_checkpoint_apply == true`
- `no_weight_commit == true`
- `no_promotion == true`

## Implemented Acceptance Logic

The CLI exits with code `1` if `matrix.summary.acceptance_pass == false`.

## Status

**Static bake:** PASS  
**Rust compile/run:** NOT RUN — container has no `cargo` / `rustc`.

## SSOT

- Domain SSOT: `en_to_ko_translation_subtitle_machine`
- State owner: `crates/ash_core/src/word_context_mock_negative_chain_matrix.rs`
- Execution entry: `crates/ash_core/src/bin/ash_word_context_mock_negative_chain_matrix.rs`
- Existing validator used: `crates/ash_core/src/word_context_mock_wctx_e2e_chain_index.rs`

## Repro Command

```bash
cargo check -p ash_core --bin ash_word_context_mock_negative_chain_matrix
cargo run -p ash_core --bin ash_word_context_mock_negative_chain_matrix
```
