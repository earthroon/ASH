# 16AI-QW-38G-R6A-WCTX-RT-05 Acceptance Report

## Verdict
`STATIC_ACCEPTANCE_PREPARED`

## Acceptance Criteria Encoded
- `total_cases >= 42`
- `accepted_cases >= 4`
- `blocked_cases >= 38`
- all upstream key absence cases blocked
- tokenizer identity mismatch blocked
- empty/too-short/too-long/non-contiguous surface chain cases blocked
- missing step receipt, out-of-range token, missing/invalid surface, unsafe special token, and missing chain digest blocked
- joined surface text, decoded text, candidate text, and candidate envelope finalization blocked
- review queue insert, auto accept, auto commit, target mutation, runtime apply blocked
- training, backward, and weight commit blocked
- accepted cases preserve no joined surface text, no decoded text, no candidate text, no candidate envelope finalization, no review insert, no commit, no runtime apply

## Local Verification
```bash
cargo check -p ash_core --bin ash_word_context_rt_controlled_multi_step_decode_shadow
cargo run -p ash_core --bin ash_word_context_rt_controlled_multi_step_decode_shadow
```

## Expected Outputs
```text
workspace/word_context_probe/wctx_rt_05_controlled_multi_step_decode_shadow_cases.json
workspace/word_context_probe/wctx_rt_05_controlled_multi_step_decode_shadow_receipts.json
workspace/word_context_probe/wctx_rt_05_controlled_multi_step_decode_shadow_matrix.json
workspace/word_context_probe/wctx_rt_05_controlled_multi_step_decode_shadow_summary.json
workspace/word_context_probe/wctx_rt_05_controlled_multi_step_decode_shadow_sample_receipt.json
```
