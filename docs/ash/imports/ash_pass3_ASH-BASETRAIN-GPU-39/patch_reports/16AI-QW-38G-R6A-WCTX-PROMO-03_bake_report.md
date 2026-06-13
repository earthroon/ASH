# WCTX-PROMO-03 Bake Report

## Patch

`16AI-QW-38G-R6A-WCTX-PROMO-03`

`Runtime Tokenized Input Bridge / No Candidate Text No Decode Seal`

## Files Added

- `crates/ash_core/src/word_context_promo_03_runtime_tokenized_input_bridge.rs`
- `crates/ash_core/src/bin/ash_word_context_promo_03_runtime_tokenized_input_bridge.rs`
- `acceptance_reports/16AI-QW-38G-R6A-WCTX-PROMO-03.md`
- `patch_reports/16AI-QW-38G-R6A-WCTX-PROMO-03_bake_report.md`
- `WCTX_PROMO_03_STATIC_CHECKS.txt`
- `WCTX_PROMO_03_BAKE_MANIFEST.json`

## Files Modified

- `crates/ash_core/src/lib.rs`

## Gate Contract

- `encode_allowed = true`
- `encode_executed = true`
- `forward_allowed = false`
- `forward_executed = false`
- `decode_allowed = false`
- `decode_executed = false`
- `candidate_text_allowed = false`
- `candidate_text_created = false`
- `preview_queue_insert_allowed = false`
- `runtime_apply_allowed = false`
- `weight_commit_allowed = false`

## Static Result

`BAKED_STATIC_NO_CARGO`

No cargo/rustc executable is available in the bake container. Static file existence, export presence, brace balance, case count, and required block string checks were performed.
