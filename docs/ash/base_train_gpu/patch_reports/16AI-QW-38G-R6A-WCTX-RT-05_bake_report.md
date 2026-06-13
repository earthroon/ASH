# 16AI-QW-38G-R6A-WCTX-RT-05 Bake Report

## Title
Controlled Multi-Step Decode Shadow / No Candidate Commit Seal

## Status
`BAKED_STATIC_NO_CARGO`

## SSOT
- domain_ssot: `en_to_ko_translation_subtitle_machine`
- base artifact: `ash_pass3_WCTX-RT-04_one_step_decoded_surface_bind_baked.zip`
- state owner: `crates/ash_core/src/word_context_rt_controlled_multi_step_decode_shadow.rs`

## Implemented
- Added RT-05 multi-step surface shadow module.
- Added CLI writer for deterministic JSON matrix artifacts.
- Added lib.rs export surface.
- Added positive fixture cases for two-step, four-step, EOS-observed, and Hangul surface chains.
- Added negative matrix covering upstream key gaps, tokenizer drift, surface-chain shape defects, joined/decoded/candidate text leaks, review/commit/runtime apply leaks, and train/backward/weight-commit leaks.

## Boundary Seal
RT-05 may arrange multiple token surfaces into a shadow chain and produce a chain digest. It must not join the surfaces into decoded text or candidate text. It must not finalize a candidate envelope, insert into review queue, auto accept, auto commit, mutate target text, runtime apply, train, run backward, or commit weights.

## Static Checks
```text
module_exists: True
bin_exists: True
lib_export_present: True
module_brace_balance: 0
bin_brace_balance: 0
positive_case_count: 4
negative_case_count: 37
total_case_count: 42
surface_chain_shadow_present: True
chain_digest_present: True
joined_surface_block_present: True
decoded_text_block_present: True
candidate_text_block_present: True
candidate_envelope_block_present: True
review_queue_block_present: True
runtime_apply_block_present: True
training_block_present: True
backward_block_present: True
weight_commit_block_present: True
acceptance_pass_field_present: True
output_paths_present: True
cargo_present: False
```

## Cargo
`NOT_RUN_CONTAINER_HAS_NO_RUSTC_OR_CARGO`
