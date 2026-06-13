# 16AI-QW-38G-R6A-WCTX-RT-03 Acceptance Report

## Acceptance Criteria
- `total_cases >= 37`
- `accepted_cases >= 4`
- `blocked_cases >= 33`
- `one_step_decode_smoke_accepted_count >= 4`
- `no_new_token_selection == true`
- `no_selection_commit == true`
- `no_sequence_decode == true`
- `no_multi_token_decode == true`
- `no_decoded_text == true`
- `no_candidate_text == true`
- `no_candidate_envelope_finalized == true`
- `no_review_queue_inserted == true`
- `no_auto_accept_executed == true`
- `no_auto_commit_executed == true`
- `no_target_mutation_executed == true`
- `no_runtime_apply_executed == true`
- `no_training_executed == true`
- `no_backward_executed == true`
- `no_weight_commit_executed == true`

## Local Verification Commands

```bash
cargo check -p ash_core --bin ash_word_context_rt_controlled_decode_one_step_smoke
cargo run -p ash_core --bin ash_word_context_rt_controlled_decode_one_step_smoke
```

## Expected Outputs
- `workspace/word_context_probe/wctx_rt_03_controlled_decode_one_step_cases.json`
- `workspace/word_context_probe/wctx_rt_03_controlled_decode_one_step_receipts.json`
- `workspace/word_context_probe/wctx_rt_03_controlled_decode_one_step_matrix.json`
- `workspace/word_context_probe/wctx_rt_03_controlled_decode_one_step_summary.json`
- `workspace/word_context_probe/wctx_rt_03_controlled_decode_one_step_sample_receipt.json`
