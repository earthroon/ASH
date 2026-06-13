# 16AI-QW-38G-R6A-WCTX-RT-08 Bake Report

## Patch

- `16AI-QW-38G-R6A-WCTX-RT-08`
- `Candidate Draft Shadow Receipt Bind / No Review Queue Insert No Commit Seal`
- SSOT: `en_to_ko_translation_subtitle_machine`

## Implemented

- Added `word_context_rt_candidate_draft_shadow_receipt_bind.rs`.
- Added CLI `ash_word_context_rt_candidate_draft_shadow_receipt_bind.rs`.
- Exported the module from `crates/ash_core/src/lib.rs`.
- Added deterministic fixture matrix with 4 accepted draft-receipt bind cases and 42 blocked leak/missing-key cases.

## Boundary

RT-08 binds RT-07 candidate text draft-shadow receipts as draft evidence only. It blocks new draft generation, production candidate text, candidate envelope finalization, candidate id issuance, review queue insertion, review receipt finalization, auto accept, commit, target mutation, runtime apply, production subtitle mutation, training, backward, and weight commit.

## Static status

```text
module_exists: True
bin_exists: True
lib_export_present: True
module_brace_balance: 0
bin_brace_balance: 0
positive_case_count: 4
negative_case_count: 42
total_case_count: 46
rt07_draft_receipt_bind_present: True
draft_text_digest_check_present: True
surface_chain_digest_check_present: True
quality_hint_guard_present: True
review_queue_block_present: True
review_queue_receipt_finalized_block_present: True
candidate_envelope_block_present: True
candidate_id_block_present: True
runtime_apply_block_present: True
production_subtitle_block_present: True
training_block_present: True
backward_block_present: True
weight_commit_block_present: True
acceptance_pass_field_present: True
output_paths_present: True
cargo_present: False
```

## Cargo status

`NOT_RUN_CONTAINER_HAS_NO_RUSTC_OR_CARGO`
