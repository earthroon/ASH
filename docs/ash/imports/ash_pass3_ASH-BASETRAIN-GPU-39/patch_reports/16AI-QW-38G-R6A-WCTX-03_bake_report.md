# 16AI-QW-38G-R6A-WCTX-03 Bake Report

## Patch

`16AI-QW-38G-R6A-WCTX-03 — EN-KO Subtitle CurrentCue / CueWindow / Stable TermGraph Split Seal`

## Domain SSOT

`en_to_ko_translation_subtitle_machine`

## What changed

Added a Rust-native graph split layer that consumes WCTX-02 EN-KO subtitle QWave shadow bridge receipts and separates subtitle term context into:

1. `CurrentCueTermGraph`
2. `CueWindowTermGraph`
3. `StableTermGraphCandidate`
4. `GlossaryContractGraphView`

## What did not change

- No generation path mutation.
- No token id mutation.
- No source English mutation.
- No target Korean subtitle mutation.
- No timing mutation.
- No glossary auto-apply.
- No stable graph promotion.
- No ContextPlan creation.
- No candidate rerank.
- No runtime default apply.

## Added files

- `crates/ash_core/src/word_context_term_graph.rs`
- `crates/ash_core/src/bin/ash_word_context_term_graph_split.rs`
- `workspace/word_context_probe/wctx_03_enko_term_graph_cases.json`
- `workspace/word_context_probe/wctx_03_enko_term_graph_matrix.json`
- `workspace/word_context_probe/wctx_03_enko_term_graph_summary.json`
- `workspace/word_context_probe/wctx_03_enko_term_graph_sample_receipt.json`
- `workspace/word_context_probe/wctx_03_static_validation.json`
- `acceptance_reports/16AI-QW-38G-R6A-WCTX-03_enko_subtitle_currentcue_cuewindow_stable_termgraph_split_seal.md`

## Modified files

- `crates/ash_core/src/lib.rs`

## Verification state

`PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE`

The local bake environment lacks `cargo`/`rustc`, so the Rust module was not compiled here. Static matrix artifacts were generated and sealed to preserve the intended graph split invariants.

## Next patch

`16AI-QW-38G-R6A-WCTX-04 — EN-KO Subtitle Typed TermGraph Edge Registry / Relation Confidence Seal`
