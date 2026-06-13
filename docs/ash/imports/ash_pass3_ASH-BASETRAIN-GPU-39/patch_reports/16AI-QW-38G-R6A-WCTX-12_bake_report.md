# 16AI-QW-38G-R6A-WCTX-12 Bake Report

## Patch

`16AI-QW-38G-R6A-WCTX-12`  
EN-KO Subtitle Decode Candidate Staging / No-Commit Execution Gate Seal

## Source Basis

`ash_pass3_16AI-QW-38G-R6A-WCTX-11_enko_subtitle_approved_prompt_candidate_runtime_preflight_no_decode_execution_baked.zip`

## Domain SSOT

`en_to_ko_translation_subtitle_machine`

## Baked Changes

Added Rust native decode staging module:

- `word_context_decode_staging.rs`
- `ash_word_context_decode_staging.rs`

Updated module registration:

- `crates/ash_core/src/lib.rs`

Generated static receipts:

- `wctx_12_enko_decode_staging_cases.json`
- `wctx_12_enko_decode_staging_matrix.json`
- `wctx_12_enko_decode_staging_summary.json`
- `wctx_12_enko_decode_staging_sample_receipt.json`
- `wctx_12_static_validation.json`

## Sealed Invariants

```text
preflight_passed=true -> staging_status=staged
preflight_passed=false -> staging_status=blocked_preflight_not_passed
commit_gate_open=false
target_subtitle_commit_allowed=false
runtime_apply_allowed=false
candidate_output_committed=false
target_text_mutated=false
timing_mutated=false
runtime_default_apply=false
rerank_applied=false
```

## Static Result

```text
total_cases=24
pass_cases=24
staged_count=12
blocked_preflight_not_passed_count=12
candidate_output_created_count=12
candidate_output_committed_count=0
decode_executed_count=0
generation_executed_count=0
model_forward_executed_count=0
sampling_executed_count=0
commit_gate_open_count=0
runtime_default_apply_count=0
```

## Verification Status

`PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE`

The container does not provide `cargo` / `rustc`, so compile-time validation is deferred to a Rust-enabled local environment.
