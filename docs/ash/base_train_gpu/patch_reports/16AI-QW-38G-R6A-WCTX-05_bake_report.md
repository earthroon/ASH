# 16AI-QW-38G-R6A-WCTX-05 Bake Report

## Seal

`16AI-QW-38G-R6A-WCTX-05 — EN-KO Subtitle Korean Particle / Ending Attachment Resolver Seal`

## Domain SSOT

`Ash = EN-to-KO translation subtitle machine`

## Bake Result

WCTX-05 was baked on top of WCTX-04. The patch adds a target-Korean, surface-preserving attachment resolver that observes Korean particles, endings, negative imperative tails, and politeness endings without modifying subtitle text.

## Added Rust Module

`crates/ash_core/src/word_context_korean_attachment.rs`

Defines:

- `KoAttachmentKind`
- `KoAttachmentFunction`
- `KoAttachmentSpan`
- `KoAttachmentCandidate`
- `KoAttachmentLink`
- `EnKoKoreanAttachmentResolverRisk`
- `EnKoKoreanAttachmentResolverReceipt`
- `EnKoKoreanAttachmentResolverMatrix`

## Added Runner

`crates/ash_core/src/bin/ash_word_context_korean_attachment.rs`

Writes:

- `workspace/word_context_probe/wctx_05_enko_korean_attachment_cases.json`
- `workspace/word_context_probe/wctx_05_enko_korean_attachment_matrix.json`
- `workspace/word_context_probe/wctx_05_enko_korean_attachment_summary.json`
- `workspace/word_context_probe/wctx_05_enko_korean_attachment_sample_receipt.json`

## Mutation Guard

All application gates remain closed:

```text
token_id_mutated=false
generation_mutated=false
source_text_mutated=false
target_text_mutated=false
timing_mutated=false
target_surface_rewritten=false
spacing_auto_corrected=false
particle_auto_corrected=false
ending_auto_corrected=false
context_plan_created=false
rerank_applied=false
runtime_default_apply=false
```

## Next Patch

Recommended next patch:

`16AI-QW-38G-R6A-WCTX-06 — EN-KO Subtitle ContextPlan Shadow Builder / CueWindow Budget Gate Seal`
