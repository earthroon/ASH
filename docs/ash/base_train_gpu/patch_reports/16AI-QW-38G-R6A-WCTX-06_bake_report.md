# 16AI-QW-38G-R6A-WCTX-06 Bake Report

## Domain SSOT
`en_to_ko_translation_subtitle_machine`

## Added
- `crates/ash_core/src/word_context_context_plan.rs`
- `crates/ash_core/src/bin/ash_word_context_context_plan_shadow.rs`
- WCTX-06 context plan matrix/summary/sample/static validation artifacts

## Changed
- `crates/ash_core/src/lib.rs` exports `word_context_context_plan`

## Scope
This patch builds a deterministic, budget-gated ContextPlan from WCTX-05 attachment receipts, WCTX-04 typed edges, and WCTX-03 cue-window graph splits. It remains shadow-only and does not mutate prompt/generation/rerank/runtime defaults.

## Validation
`PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE`

## Next recommended seal
`16AI-QW-38G-R6A-WCTX-07 — EN-KO Subtitle ContextPlan Shadow Replay / No-Prompt-Mutation Receipt Seal`
