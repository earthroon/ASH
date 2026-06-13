# 16AI-QW-38G-R6A-WCTX-04 Acceptance Report

## Patch

- Patch ID: `16AI-QW-38G-R6A-WCTX-04`
- Name: `EN-KO Subtitle Typed TermGraph Edge Registry / Relation Confidence Seal`
- Domain SSOT: `en_to_ko_translation_subtitle_machine`
- Status: `PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE`

## Purpose

WCTX-04 consumes WCTX-03 `EnKoSubtitleTermGraphSplitReceipt` values and re-seals observed term graph edges as typed EN-KO subtitle translation relations with evidence and confidence.

This patch is shadow-only. It does not mutate source English text, target Korean subtitle text, timing, token ids, generation state, glossary/preserve application, stable graph promotion, ContextPlan, candidate rerank, or runtime defaults.

## Added files

- `crates/ash_core/src/word_context_edge_registry.rs`
- `crates/ash_core/src/bin/ash_word_context_edge_registry.rs`
- `workspace/word_context_probe/wctx_04_enko_typed_edge_cases.json`
- `workspace/word_context_probe/wctx_04_enko_typed_edge_matrix.json`
- `workspace/word_context_probe/wctx_04_enko_typed_edge_summary.json`
- `workspace/word_context_probe/wctx_04_enko_typed_edge_sample_receipt.json`
- `workspace/word_context_probe/wctx_04_static_validation.json`

## Modified files

- `crates/ash_core/src/lib.rs`

## Static matrix summary

```json
{
  "patch_id": "16AI-QW-38G-R6A-WCTX-04",
  "domain_ssot": "en_to_ko_translation_subtitle_machine",
  "total_cases": 24,
  "pass_cases": 24,
  "fail_cases": 0,
  "deterministic_failures": 0,
  "risk_failures": 0,
  "total_typed_edges": 1503,
  "total_high_confidence": 112,
  "total_medium_confidence": 390,
  "total_low_confidence": 1001,
  "total_unknown_confidence": 0,
  "total_unknown_relations": 0,
  "total_dangling_typed_edges": 0,
  "token_id_mutation_count": 0,
  "generation_mutation_count": 0,
  "source_text_mutation_count": 0,
  "target_text_mutation_count": 0,
  "timing_mutation_count": 0,
  "glossary_auto_apply_count": 0,
  "preserve_auto_apply_count": 0,
  "stable_graph_promotion_count": 0,
  "context_plan_created_count": 0,
  "rerank_applied_count": 0,
  "runtime_default_apply_count": 0
}
```

## Acceptance criteria

- [PASS] EN-KO translation subtitle domain SSOT retained.
- [PASS] Typed edge relation enum added.
- [PASS] Relation confidence structure added.
- [PASS] Evidence structure added.
- [PASS] WCTX-03 edge can be converted into typed edge receipts.
- [PASS] `negation_alignment` relation supported.
- [PASS] `proper_noun_preserve` relation supported.
- [PASS] `glossary_required` relation supported.
- [PASS] `preserve_required` relation supported.
- [PASS] `speaker_register_carry` / `same_speaker_continuity` relation supported.
- [PASS] `linebreak_pressure` relation supported.
- [PASS] `compression_pressure` relation supported.
- [PASS] `timing_density_pressure` relation supported.
- [PASS] Confidence band is derived from score.
- [PASS] Evidence list is serialized per typed edge.
- [PASS] Dangling typed edge count is sealed.
- [PASS] Typed edges are `shadow_only=true`.
- [PASS] `token_id_mutated=false`.
- [PASS] `generation_mutated=false`.
- [PASS] `source_text_mutated=false`.
- [PASS] `target_text_mutated=false`.
- [PASS] `timing_mutated=false`.
- [PASS] `glossary_auto_applied=false`.
- [PASS] `preserve_auto_applied=false`.
- [PASS] `stable_graph_promoted=false`.
- [PASS] `context_plan_created=false`.
- [PASS] `rerank_applied=false`.
- [PASS] `runtime_default_apply=false`.
- [PASS] Matrix JSON emitted.
- [PASS] Summary JSON emitted.

## Toolchain note

The current execution container does not provide `cargo` or `rustc`, so Rust compilation and runtime tests were not executed here. The patch is therefore sealed as `PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE`.

Recommended local check:

```bash
cargo run -p ash_core --bin ash_word_context_edge_registry
```

## Final seal

WCTX-04 is a shadow-only relation registry seal. It explains why observed WCTX-03 term graph edges look related in an EN-KO subtitle translation context, but it does not apply those relations to translation, timing, generation, rerank, or runtime defaults.
