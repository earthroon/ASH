# 16AI-QW-38G-R6A-WCTX-RT-00 Bake Report

## Patch

`16AI-QW-38G-R6A-WCTX-RT-00`  
`Runtime Forward Dry Probe / No Candidate Commit No Review Insert Seal`

## SSOT

- Domain SSOT: `en_to_ko_translation_subtitle_machine`
- Base artifact: `ash_pass3_WCTX-MOCK-20_real_runtime_receipt_shape_baked.zip`
- State owner: `crates/ash_core/src/word_context_rt_forward_dry_probe.rs`

## Implemented

- Added RT-00 forward dry probe module.
- Added CLI entrypoint for deterministic JSON emission.
- Added `lib.rs` module/export surface.
- Added 3 positive forward-shape probe cases.
- Added 37 negative boundary/leak cases.
- Added request, runtime identity evidence, input shape, output shape, execution boundary, receipt, matrix, and summary types.
- Added static checks and bake manifest.

## Positive cases

- `rt00:native_wgpu_forward_shape_probe`
- `rt00:cpu_reference_forward_shape_probe`
- `rt00:external_backend_forward_shape_probe`

## Negative cases

The negative matrix covers missing upstream receipt keys, missing model/tokenizer/checkpoint/runtime-config hashes, runtime unavailable, model/checkpoint/config not bound, invalid input-token boundaries, forward-not-allowed/not-executed, missing logits shape, non-finite logits, missing logits digest, decode/generation/sampling/token-selection leaks, full-logits attachment, candidate text generation, candidate envelope finalization, review queue insertion, auto-accept, auto-commit, target mutation, runtime apply, training, backward, and weight commit.

## Boundary

RT-00 permits a narrow forward dry probe shape receipt. It still forbids decode, generation, sampling, token selection, candidate text generation, candidate envelope finalization, review queue insertion, auto-accept, auto-commit, target mutation, runtime apply, training, backward, and weight commit.

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

## Cargo status

`NOT_RUN_CONTAINER_HAS_NO_RUSTC_OR_CARGO`
