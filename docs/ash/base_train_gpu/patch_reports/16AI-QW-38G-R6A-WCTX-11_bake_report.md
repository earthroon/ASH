# 16AI-QW-38G-R6A-WCTX-11 Bake Report

## Added
- `crates/ash_core/src/word_context_runtime_preflight.rs`
- `crates/ash_core/src/bin/ash_word_context_runtime_preflight.rs`
- `workspace/word_context_probe/wctx_11_enko_runtime_preflight_cases.json`
- `workspace/word_context_probe/wctx_11_enko_runtime_preflight_matrix.json`
- `workspace/word_context_probe/wctx_11_enko_runtime_preflight_summary.json`
- `workspace/word_context_probe/wctx_11_enko_runtime_preflight_sample_receipt.json`
- `workspace/word_context_probe/wctx_11_static_validation.json`

## Modified
- `crates/ash_core/src/lib.rs`

## Static result
- total_cases = 24
- pass_cases = 24
- preflight_pass_count = 12
- preflight_blocked_count = 12
- can_proceed_to_decode_candidate_count = 12
- can_apply_to_runtime_count = 0
- decode_executed_count = 0
- generation_executed_count = 0
- model_forward_executed_count = 0
- sampling_executed_count = 0
- runtime_default_apply_count = 0

## Toolchain note
`cargo` / `rustc` were unavailable in the container, so validation is static only.
