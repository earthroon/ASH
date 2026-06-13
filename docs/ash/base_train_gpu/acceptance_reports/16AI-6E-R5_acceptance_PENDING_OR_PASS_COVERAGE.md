# 16AI-6E-R5 Acceptance

Status: PENDING_RUNTIME

Scope:
- coverage_mode: report_only
- generation: false
- token_ids_mutated: false
- committed_prompt_ids: baseline
- vocab_augmented: false
- new_token_ids_created: false

## Acceptance Criteria

- [ ] AC-16AI-6E-R5-1 6E JSON and R4 delta summary are read.
- [ ] AC-16AI-6E-R5-2 R4 PASS_DELTA_REPORT status is checked or recorded.
- [ ] AC-16AI-6E-R5-3 selected_pieces / selected_surfaces / lookup_status equivalents are collected.
- [ ] AC-16AI-6E-R5-4 piece coverage_class is computed.
- [ ] AC-16AI-6E-R5-5 ExactCovered / VariantCovered / FallbackEncoded / LookupMiss / UnknownUsed are separated.
- [ ] AC-16AI-6E-R5-6 coverage_score is computed.
- [ ] AC-16AI-6E-R5-7 fallback/lookup miss pieces are risk-classified.
- [ ] AC-16AI-6E-R5-8 CJI/fallback pattern is extracted.
- [ ] AC-16AI-6E-R5-9 merge_candidates are generated or explicitly empty.
- [ ] AC-16AI-6E-R5-10 no new token ids are created.
- [ ] AC-16AI-6E-R5-11 vocab is not modified.
- [ ] AC-16AI-6E-R5-12 generation=false is preserved.
- [ ] AC-16AI-6E-R5-13 token_ids_mutated=false is preserved.
- [ ] AC-16AI-6E-R5-14 committed_prompt_ids=baseline is preserved.

## Runtime note

This acceptance file is upgraded by `af16ai6e_r5_cji_coverage_extract` after local runtime execution.
