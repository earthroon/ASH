# 16AI-QW-38G-R6A-WCTX-02 Bake Report

## Domain SSOT
`en_to_ko_translation_subtitle_machine`

## What changed
- Added `word_context_subtitle_qwave.rs`.
- Added `ash_word_context_subtitle_qwave_shadow` runner.
- Exported the module from `ash_core`.
- Generated WCTX-02 EN-KO subtitle shadow cases, matrix, summary, and sample receipt.

## What did not change
- No token id mutation.
- No generation mutation.
- No source English mutation.
- No target Korean mutation.
- No timing mutation.
- No runtime default apply.
- No LexGraph long-term write.
- No ContextPlan creation.
- No candidate rerank.

## Static result
```json
{
  "patch_id": "16AI-QW-38G-R6A-WCTX-02",
  "domain_ssot": "en_to_ko_translation_subtitle_machine",
  "total_cases": 24,
  "pass_cases": 24,
  "fail_cases": 0,
  "deterministic_failures": 0,
  "source_span_failures": 0,
  "target_span_failures": 0,
  "timing_preservation_failures": 0,
  "risk_failures": 0,
  "token_id_mutation_count": 0,
  "generation_mutation_count": 0,
  "source_text_mutation_count": 0,
  "target_text_mutation_count": 0,
  "timing_mutation_count": 0,
  "total_source_candidates": 122,
  "total_target_candidates": 92,
  "total_timing_candidates": 24,
  "total_word_context_hits": 238,
  "total_unknown_relations": 0
}
```

## Reproduction command
```bash
cargo run -p ash_core --bin ash_word_context_subtitle_qwave_shadow
```

## Status
`PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE`
