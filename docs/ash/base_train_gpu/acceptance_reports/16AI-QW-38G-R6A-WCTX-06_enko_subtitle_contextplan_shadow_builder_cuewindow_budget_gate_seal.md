# 16AI-QW-38G-R6A-WCTX-06 Acceptance Report

## Seal
EN-KO Subtitle ContextPlan Shadow Builder / CueWindow Budget Gate Seal

## Domain SSOT
`en_to_ko_translation_subtitle_machine`

## Status
`PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE`

## Confirmed static invariants
- ContextPlan is created as shadow receipt only.
- `context_plan_created=true`.
- `context_plan_applied=false`.
- `prompt_mutated=false`.
- `rerank_applied=false`.
- `runtime_default_apply=false`.
- Source English, target Korean, timing, token ids, and generation state are not mutated.
- Budget gate emits accepted and dropped item counts with deterministic receipt keys.

## Matrix summary
```json
{
  "patch_id": "16AI-QW-38G-R6A-WCTX-06",
  "domain_ssot": "en_to_ko_translation_subtitle_machine",
  "total_cases": 24,
  "pass_cases": 24,
  "fail_cases": 0,
  "deterministic_failures": 0,
  "risk_failures": 0,
  "total_candidate_items": 348,
  "total_accepted_items": 281,
  "total_dropped_items": 67,
  "total_critical_items": 24,
  "total_high_items": 96,
  "total_medium_items": 96,
  "total_low_items": 65,
  "budget_truncated_count": 19,
  "budget_overflow_count": 0,
  "context_plan_created_count": 24,
  "context_plan_applied_count": 0,
  "prompt_mutation_count": 0,
  "rerank_applied_count": 0,
  "runtime_default_apply_count": 0,
  "source_text_mutation_count": 0,
  "target_text_mutation_count": 0,
  "timing_mutation_count": 0,
  "glossary_auto_apply_count": 0,
  "preserve_auto_apply_count": 0,
  "particle_auto_correct_count": 0,
  "ending_auto_correct_count": 0
}
```

## Toolchain note
The bake environment does not include `cargo`/`rustc`; runtime compile/test must be replayed in a Rust-enabled local environment.
