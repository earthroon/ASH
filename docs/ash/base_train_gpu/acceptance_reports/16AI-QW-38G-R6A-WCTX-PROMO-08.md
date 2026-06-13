# 16AI-QW-38G-R6A-WCTX-PROMO-08

## RT02 Real TopK Shadow Selection / No Decode No Candidate Commit Seal

### SSOT
- Domain: `en_to_ko_translation_subtitle_machine`
- State owner: `crates/ash_core/src/word_context_promo_08_rt02_real_topk_shadow_selection.rs`
- Receipt bin: `crates/ash_core/src/bin/ash_word_context_promo_08_rt02_real_topk_shadow_selection.rs`

### Seal
`WCTX-PROMO-08` allows only RT-02 **shadow selected token candidate** creation from real top-k trace and RT-01 shape bind evidence.

It does **not** allow committed token selection, runtime token append, sequence mutation, decode, decoded surface, candidate text, RT-03 receipt creation, preview/review queue insertion, approval, commit, runtime apply, training, backward, optimizer step, weight commit, or delta stack append.

### PASS status
`PASS_WCTX_PROMO_08_RT02_REAL_TOPK_SHADOW_SELECTION_NO_DECODE_NO_CANDIDATE_COMMIT`

### Required positive invariants
- PROMO-00..07 evidence is required and respected.
- `rt02_shadow_selection_allowed = true`
- `rt02_shadow_selection_executed = true`
- `shadow_selected_token_id_present = true`
- `shadow_selected_token_in_topk_trace = true`
- `shadow_selected_token_in_vocab_range = true`
- `shadow_selected_score_finite = true`
- `committed_selected_token_id_present = false`
- `token_selection_committed = false`
- `runtime_token_append_executed = false`
- `decode_executed = false`
- `decoded_surface_created = false`
- `candidate_text_created = false`
- `rt03_receipt_created = false`

### Negative matrix coverage
The baked matrix includes guards for missing PROMO-00..07 evidence, mock/fixture/receipt-only/synthetic shadow selection, missing shadow token, token not in top-k trace, out-of-vocab token, non-finite score, RT02 key reuse with RT00/RT01/MOCK20, committed token creation, runtime token append, sequence mutation, decode, decoded surface, candidate text, draft shadow, RT03 creation, queues, approval, commit, runtime apply, generation, sampling, training, backward, optimizer step, and delta stack append.

### Static status
`BAKED_STATIC_NO_CARGO`
