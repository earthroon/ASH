# 16AI-QW-38G-R6A-WCTX-RT-10 Acceptance Report

## Acceptance Target

`Preview Queue Receipt Bind / No Approval No Commit Seal`

## SSOT

- `domain_ssot = en_to_ko_translation_subtitle_machine`
- Upstream: `RT-09 Review Queue Insert Candidate Preview`
- Current authority: preview queue receipt bind only.

## Acceptance Criteria Baked

- `total_cases >= 58`
- `accepted_cases >= 4`
- `blocked_cases >= 54`
- `expectation_mismatched_cases == 0`
- Preview queue receipt bind accepted cases are present.
- Approval receipt, commit receipt, production review queue receipt, production review queue insert, auto accept, auto commit, candidate envelope finalization, candidate id issuance, commit candidate creation, committed target creation, target mutation, runtime apply, production subtitle mutation, training, backward, and weight commit are blocked.

## Local Commands

```bash
cargo check -p ash_core --bin ash_word_context_rt_preview_queue_receipt_bind
cargo run -p ash_core --bin ash_word_context_rt_preview_queue_receipt_bind
```

## Expected Outputs

```text
workspace/word_context_probe/wctx_rt_10_preview_queue_receipt_bind_cases.json
workspace/word_context_probe/wctx_rt_10_preview_queue_receipt_bind_receipts.json
workspace/word_context_probe/wctx_rt_10_preview_queue_receipt_bind_matrix.json
workspace/word_context_probe/wctx_rt_10_preview_queue_receipt_bind_summary.json
workspace/word_context_probe/wctx_rt_10_preview_queue_receipt_bind_sample_receipt.json
```

## Container Status

`cargo` and `rustc` were not available in this container, so this bake is sealed as `BAKED_STATIC_NO_CARGO`.
