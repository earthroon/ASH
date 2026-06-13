# 16AI-QW-38G-R6A-WCTX-03 Acceptance Report

## Patch

`16AI-QW-38G-R6A-WCTX-03 — EN-KO Subtitle CurrentCue / CueWindow / Stable TermGraph Split Seal`

## Domain SSOT

`en_to_ko_translation_subtitle_machine`

Ash is scoped as an English-to-Korean translation subtitle-machine domain component. WCTX-03 uses cue-centered subtitle context, not generic conversation turn context.

## Status

`PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE`

The container used for this bake does not expose `cargo` or `rustc`, so compile/runtime execution was not performed here. Static source files, JSON receipts, mutation guards, and deterministic matrix artifacts were generated and sealed.

## Implemented Files

- `crates/ash_core/src/word_context_term_graph.rs`
- `crates/ash_core/src/bin/ash_word_context_term_graph_split.rs`
- `crates/ash_core/src/lib.rs`
- `workspace/word_context_probe/wctx_03_enko_term_graph_cases.json`
- `workspace/word_context_probe/wctx_03_enko_term_graph_matrix.json`
- `workspace/word_context_probe/wctx_03_enko_term_graph_summary.json`
- `workspace/word_context_probe/wctx_03_enko_term_graph_sample_receipt.json`
- `workspace/word_context_probe/wctx_03_static_validation.json`

## SSOT Additions

- `EnKoSubtitleTermGraphNode`
- `EnKoSubtitleTermGraphEdge`
- `CurrentCueTermGraph`
- `CueWindowTermGraph`
- `StableTermGraphCandidate`
- `GlossaryContractGraphView`
- `EnKoSubtitleTermGraphSplitReceipt`
- `EnKoSubtitleTermGraphSplitMatrix`

## Graph Layers

- `CurrentCueGraph`: center cue only.
- `CueWindowGraph`: cue window around the center cue, default radius 2.
- `StableTermGraphCandidate`: repeated or contract-like terms only; `promoted=false`.
- `GlossaryContractGraphView`: glossary/preserve contract observation only; `auto_applied=false`.

## Mutation Guard

The following invariants are sealed as false:

- `token_id_mutated`
- `generation_mutated`
- `source_text_mutated`
- `target_text_mutated`
- `timing_mutated`
- `glossary_auto_applied`
- `stable_graph_promoted`
- `byte_leak_observed`

## Static Matrix Summary

```json
{
  "patch_id": "16AI-QW-38G-R6A-WCTX-03",
  "domain_ssot": "en_to_ko_translation_subtitle_machine",
  "total_cases": 24,
  "pass_cases": 24,
  "fail_cases": 0,
  "deterministic_failures": 0,
  "risk_failures": 0,
  "total_current_nodes": 243,
  "total_current_edges": 235,
  "total_window_nodes": 1153,
  "total_window_edges": 1194,
  "total_stable_candidates": 190,
  "total_glossary_contract_nodes": 38,
  "total_dangling_nodes": 0,
  "total_dangling_edges": 0,
  "total_unknown_edges": 0,
  "token_id_mutation_count": 0,
  "generation_mutation_count": 0,
  "source_text_mutation_count": 0,
  "target_text_mutation_count": 0,
  "timing_mutation_count": 0,
  "glossary_auto_apply_count": 0,
  "stable_graph_promotion_count": 0
}
```

## Acceptance Criteria

- PASS: EN-KO translation subtitle domain SSOT maintained.
- PASS: WCTX-02 receipt path is the upstream input.
- PASS: CurrentCueGraph is center-cue scoped.
- PASS: CueWindowGraph is cue-window scoped.
- PASS: StableTermGraphCandidate remains candidate-only.
- PASS: GlossaryContractGraphView remains view-only.
- PASS: No dangling edges in static matrix.
- PASS: No token/generation/source/target/timing mutation flags.
- PASS: No glossary auto-apply.
- PASS: No stable graph promotion.

## Reproduction Command

When Rust toolchain is available:

```bash
cargo run -p ash_core --bin ash_word_context_term_graph_split
```

or crate-local:

```bash
cargo run --bin ash_word_context_term_graph_split
```
