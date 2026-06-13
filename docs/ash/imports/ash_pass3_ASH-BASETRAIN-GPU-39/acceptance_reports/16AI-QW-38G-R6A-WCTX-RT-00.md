# 16AI-QW-38G-R6A-WCTX-RT-00 Acceptance Report

## Verdict

`BAKED_STATIC_NO_CARGO`

## Acceptance intent

RT-00 is the first WCTX real-runtime boundary after MOCK-20. The baked layer allows a forward dry probe receipt shape while blocking decode, candidate creation, review insertion, commit, runtime apply, and training/backward/weight-commit leakage.

## Required local commands

```bash
cargo check -p ash_core --bin ash_word_context_rt_forward_dry_probe
cargo run -p ash_core --bin ash_word_context_rt_forward_dry_probe
```

## Expected output files

```text
workspace/word_context_probe/wctx_rt_00_forward_dry_probe_cases.json
workspace/word_context_probe/wctx_rt_00_forward_dry_probe_receipts.json
workspace/word_context_probe/wctx_rt_00_forward_dry_probe_matrix.json
workspace/word_context_probe/wctx_rt_00_forward_dry_probe_summary.json
workspace/word_context_probe/wctx_rt_00_forward_dry_probe_sample_receipt.json
```

## Static checks

```text
module_exists: True
bin_exists: True
lib_export_present: True
module_brace_balance: 0
bin_brace_balance: 0
case_push_count: 40
positive_case_count: 3
negative_case_count: 37
forward_boundary_present: True
decode_block_present: True
generation_block_present: True
sampling_block_present: True
token_selection_block_present: True
candidate_text_block_present: True
review_queue_block_present: True
auto_accept_block_present: True
runtime_apply_block_present: True
training_block_present: True
backward_block_present: True
weight_commit_block_present: True
logits_shape_check_present: True
logits_digest_present: True
acceptance_pass_field_present: True
output_paths_present: True
cargo_present: False
```

## Notes

This container did not provide `cargo` or `rustc`, so compile/runtime validation was not executed here. The patch is sealed as a static bake with deterministic fixture-matrix code.
