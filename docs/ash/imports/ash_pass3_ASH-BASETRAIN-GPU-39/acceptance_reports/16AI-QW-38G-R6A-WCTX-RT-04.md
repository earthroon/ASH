# 16AI-QW-38G-R6A-WCTX-RT-04 Acceptance

## Verdict

`BAKED_STATIC_NO_CARGO`

## Acceptance Intent

RT-04 must bind RT-03 token surface evidence without creating candidate text, candidate envelopes, review queue inserts, commits, runtime apply, or training-side effects.

## Expected Local Outputs

```text
workspace/word_context_probe/wctx_rt_04_one_step_decoded_surface_bind_cases.json
workspace/word_context_probe/wctx_rt_04_one_step_decoded_surface_bind_receipts.json
workspace/word_context_probe/wctx_rt_04_one_step_decoded_surface_bind_matrix.json
workspace/word_context_probe/wctx_rt_04_one_step_decoded_surface_bind_summary.json
workspace/word_context_probe/wctx_rt_04_one_step_decoded_surface_bind_sample_receipt.json
```

## Required Local Summary Fields

```text
acceptance_pass == true
surface_receipt_bind_accepted_count >= 4
no_candidate_text == true
no_candidate_envelope_finalized == true
no_review_queue_inserted == true
no_runtime_apply_executed == true
no_training_executed == true
no_backward_executed == true
no_weight_commit_executed == true
```

## Static Evidence

See `WCTX_RT_04_STATIC_CHECKS.txt` and `WCTX_RT_04_BAKE_MANIFEST.json`.
