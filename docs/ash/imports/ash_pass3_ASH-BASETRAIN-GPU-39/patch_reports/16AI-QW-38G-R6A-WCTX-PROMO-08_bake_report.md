# WCTX-PROMO-08 Bake Report

## Patch
`16AI-QW-38G-R6A-WCTX-PROMO-08`

## Title
`RT02 Real TopK Shadow Selection / No Decode No Candidate Commit Seal`

## Baked files
- `crates/ash_core/src/word_context_promo_08_rt02_real_topk_shadow_selection.rs`
- `crates/ash_core/src/bin/ash_word_context_promo_08_rt02_real_topk_shadow_selection.rs`
- `crates/ash_core/src/lib.rs`
- `acceptance_reports/16AI-QW-38G-R6A-WCTX-PROMO-08.md`
- `patch_reports/16AI-QW-38G-R6A-WCTX-PROMO-08_bake_report.md`
- `WCTX_PROMO_08_STATIC_CHECKS.txt`
- `WCTX_PROMO_08_BAKE_MANIFEST.json`

## Contract
This bake binds RT-02 shadow token selection to PROMO-05 real top-k trace and PROMO-07 RT01 output shape evidence. It creates only a shadow selected token candidate. It blocks committed selected token fields, runtime token append, sequence mutation, decode, decoded surface, candidate text, RT-03 creation, queues, approval, commit, runtime apply, training/backward/optimizer/weight/delta mutation.

## Static build note
The current container does not provide `cargo` or `rustc`, so this bake is sealed as `BAKED_STATIC_NO_CARGO`.
