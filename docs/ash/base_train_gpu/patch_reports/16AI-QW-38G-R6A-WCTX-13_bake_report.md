# 16AI-QW-38G-R6A-WCTX-13 Bake Report

## Patch
EN-KO Subtitle Decode Candidate Review Matrix / Target Preservation Diff Seal

## Baked From
`ash_pass3_16AI-QW-38G-R6A-WCTX-12_enko_subtitle_decode_candidate_staging_no_commit_execution_gate_baked.zip`

## Domain SSOT
`en_to_ko_translation_subtitle_machine`

## Files Added
- `crates/ash_core/src/word_context_decode_review.rs`
- `crates/ash_core/src/bin/ash_word_context_decode_review.rs`
- `workspace/word_context_probe/wctx_13_enko_decode_review_cases.json`
- `workspace/word_context_probe/wctx_13_enko_decode_review_matrix.json`
- `workspace/word_context_probe/wctx_13_enko_decode_review_summary.json`
- `workspace/word_context_probe/wctx_13_enko_decode_review_sample_receipt.json`
- `workspace/word_context_probe/wctx_13_static_validation.json`
- `acceptance_reports/16AI-QW-38G-R6A-WCTX-13_enko_subtitle_decode_candidate_review_matrix_target_preservation_diff_seal.md`
- `patch_reports/16AI-QW-38G-R6A-WCTX-13_bake_report.md`

## Files Modified
- `crates/ash_core/src/lib.rs`

## Core APIs
```rust
pub fn default_enko_decode_candidate_review_staging_receipts() -> Vec<EnKoDecodeStagingReceipt>;

pub fn build_enko_decode_candidate_review_receipt(
    staging_receipt: &EnKoDecodeStagingReceipt,
) -> EnKoDecodeCandidateReviewReceipt;

pub fn run_enko_decode_candidate_review_matrix(
    staging_receipts: &[EnKoDecodeStagingReceipt],
) -> EnKoDecodeCandidateReviewMatrix;
```

## No-Commit Invariants
- `target_text_mutated=false`
- `target_subtitle_committed=false`
- `commit_gate_open=false`
- `runtime_default_apply=false`
- `rerank_applied=false`
- `decode_executed_in_review=false`
- `generation_executed_in_review=false`
- `model_forward_executed_in_review=false`
- `sampling_executed_in_review=false`

## Static Validation
The default WCTX-12 detached staging line has no candidate target text, so WCTX-13 correctly records `NoCandidateAvailable` for staged receipts rather than inventing a candidate.

Status: `PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE`.
