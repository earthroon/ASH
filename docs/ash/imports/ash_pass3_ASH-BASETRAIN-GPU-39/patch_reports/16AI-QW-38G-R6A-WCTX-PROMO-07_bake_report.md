# WCTX-PROMO-07 Bake Report

## Patch

`16AI-QW-38G-R6A-WCTX-PROMO-07`

## Title

`RT01 Real Forward Output Shape Bind / No Decode No Candidate Text Seal`

## Base

`ash_pass3_WCTX-PROMO-06_rt00_real_forward_receipt_rebind_baked.zip`

## Added

- `word_context_promo_07_rt01_real_forward_output_shape_bind.rs`
- `ash_word_context_promo_07_rt01_real_forward_output_shape_bind.rs`
- `acceptance_reports/16AI-QW-38G-R6A-WCTX-PROMO-07.md`
- `WCTX_PROMO_07_STATIC_CHECKS.txt`
- `WCTX_PROMO_07_BAKE_MANIFEST.json`

## Static checks

```txt
module_exists: True
bin_exists: True
lib_export_present: True
module_brace_balance: 0
bin_brace_balance: 0
positive_case_count: 4
negative_case_count: 45
total_case_count: 49
promo00_boundary_required_present: True
promo01_adapter_interface_required_present: True
promo02_identity_bundle_required_present: True
promo03_tokenized_input_required_present: True
promo04_forward_probe_required_present: True
promo05_topk_trace_required_present: True
promo06_rt00_rebind_required_present: True
rt01_shape_bind_allowed_present: True
rt01_shape_bind_executed_present: True
rt01_receipt_key_required_present: True
rt01_receipt_key_created_present: True
rt01_receipt_key_unique_from_rt00_present: True
rt01_receipt_key_unique_from_mock20_present: True
output_shape_required_present: True
output_shape_bound_present: True
output_shape_digest_required_present: True
output_shape_digest_bound_present: True
output_shape_digest_mismatch_promo04_block_present: True
output_shape_digest_mismatch_rt00_block_present: True
logits_rank_zero_block_present: True
logits_batch_dim_zero_block_present: True
logits_sequence_dim_zero_block_present: True
logits_vocab_dim_zero_block_present: True
full_logits_attachment_block_present: True
full_logits_persistence_block_present: True
selected_token_id_block_present: True
token_selection_block_present: True
sampling_block_present: True
generation_block_present: True
decode_block_present: True
decoded_surface_block_present: True
candidate_text_block_present: True
draft_shadow_block_present: True
rt02_receipt_created_block_present: True
preview_queue_insert_block_present: True
review_queue_insert_block_present: True
operator_approval_block_present: True
candidate_commit_block_present: True
runtime_apply_block_present: True
weight_commit_block_present: True
training_forward_block_present: True
backward_block_present: True
optimizer_step_block_present: True
delta_stack_append_block_present: True
mock_shape_bind_block_present: True
fixture_shape_bind_block_present: True
receipt_only_shape_bind_block_present: True
synthetic_shape_bind_block_present: True
acceptance_pass_field_present: True
output_paths_present: True
cargo_present: False
rustc_present: False
static_status: BAKED_STATIC_NO_CARGO
```

## Compile status

`BAKED_STATIC_NO_CARGO`

Cargo/rustc were not available in this container, so this bake preserves the same static-no-cargo validation mode as the previous PROMO line.
