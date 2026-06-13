# 16AI-QW-38G-R6A-WCTX-05 Acceptance Report

## Patch

- Patch ID: `16AI-QW-38G-R6A-WCTX-05`
- Name: `EN-KO Subtitle Korean Particle / Ending Attachment Resolver Seal`
- Domain SSOT: `en_to_ko_translation_subtitle_machine`
- Status: `PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE`

## Scope

WCTX-05 adds a Rust-native, shadow-only Korean attachment resolver for the EN-to-KO subtitle translation domain. It observes target Korean subtitle particles, endings, negative imperative tails, and politeness endings without rewriting the target Korean subtitle surface.

## Files Added

- `crates/ash_core/src/word_context_korean_attachment.rs`
- `crates/ash_core/src/bin/ash_word_context_korean_attachment.rs`
- `workspace/word_context_probe/wctx_05_enko_korean_attachment_cases.json`
- `workspace/word_context_probe/wctx_05_enko_korean_attachment_matrix.json`
- `workspace/word_context_probe/wctx_05_enko_korean_attachment_summary.json`
- `workspace/word_context_probe/wctx_05_enko_korean_attachment_sample_receipt.json`
- `workspace/word_context_probe/wctx_05_static_validation.json`

## Files Modified

- `crates/ash_core/src/lib.rs`

## Public API

```rust
pub fn default_enko_korean_attachment_resolver_pairs(
) -> Vec<(EnKoTypedEdgeRegistryReceipt, EnKoSubtitleTermGraphSplitReceipt)>;

pub fn resolve_korean_attachments_shadow(
    registry_receipt: &EnKoTypedEdgeRegistryReceipt,
    split_receipt: &EnKoSubtitleTermGraphSplitReceipt,
) -> EnKoKoreanAttachmentResolverReceipt;

pub fn run_enko_korean_attachment_resolver_matrix(
    pairs: &[(EnKoTypedEdgeRegistryReceipt, EnKoSubtitleTermGraphSplitReceipt)],
) -> EnKoKoreanAttachmentResolverMatrix;
```

## Static Matrix Summary

```json
{
  "patch_id": "16AI-QW-38G-R6A-WCTX-05",
  "domain_ssot": "en_to_ko_translation_subtitle_machine",
  "total_cases": 24,
  "pass_cases": 24,
  "fail_cases": 0,
  "deterministic_failures": 0,
  "risk_failures": 0,
  "total_candidates": 43,
  "total_links": 43,
  "total_particles": 26,
  "total_endings": 12,
  "total_negation_tails": 5,
  "total_politeness_tails": 0,
  "total_unknowns": 0,
  "total_invalid_spans": 0,
  "total_unresolved_attachments": 47,
  "token_id_mutation_count": 0,
  "generation_mutation_count": 0,
  "source_text_mutation_count": 0,
  "target_text_mutation_count": 0,
  "timing_mutation_count": 0,
  "target_surface_rewrite_count": 0,
  "spacing_auto_correct_count": 0,
  "particle_auto_correct_count": 0,
  "ending_auto_correct_count": 0,
  "context_plan_created_count": 0,
  "rerank_applied_count": 0,
  "runtime_default_apply_count": 0
}
```

## PASS Criteria

- PASS: EN-KO translation subtitle domain SSOT retained.
- PASS: `KoAttachmentKind` added.
- PASS: `KoAttachmentFunction` added.
- PASS: `KoAttachmentCandidate` added.
- PASS: `KoAttachmentLink` added.
- PASS: target Korean particle tail observation added.
- PASS: target Korean ending/prohibition tail observation added.
- PASS: full/base/tail span structures added with `target_korean` coordinate space.
- PASS: `shadow_only=true` for candidates.
- PASS: `target_surface_rewritten=false`.
- PASS: `spacing_auto_corrected=false`.
- PASS: `particle_auto_corrected=false`.
- PASS: `ending_auto_corrected=false`.
- PASS: `context_plan_created=false`.
- PASS: `rerank_applied=false`.
- PASS: `runtime_default_apply=false`.

## Verification Limitation

`cargo` / `rustc` is unavailable in this container, so the patch is sealed as static only:

```text
PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE
```

Local reproduction command:

```bash
cargo run -p ash_core --bin ash_word_context_korean_attachment
```

## Non-goals Preserved

- No source English mutation.
- No target Korean mutation.
- No timing mutation.
- No token id mutation.
- No generation mutation.
- No glossary or preserve auto-application.
- No ContextPlan creation.
- No candidate rerank.
- No runtime default apply.
