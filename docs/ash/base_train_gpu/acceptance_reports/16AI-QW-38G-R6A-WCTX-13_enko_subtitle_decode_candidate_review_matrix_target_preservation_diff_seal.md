# 16AI-QW-38G-R6A-WCTX-13 Acceptance Report

## Patch
EN-KO Subtitle Decode Candidate Review Matrix / Target Preservation Diff Seal

## Domain SSOT
`en_to_ko_translation_subtitle_machine`

## Scope
WCTX-13 consumes WCTX-12 decode staging receipts and creates review-only target preservation diffs. It does not commit candidate output, does not mutate target subtitles, does not open commit gates, and does not enable runtime default apply.

## Added Rust Surfaces
- `crates/ash_core/src/word_context_decode_review.rs`
- `crates/ash_core/src/bin/ash_word_context_decode_review.rs`

## Added Receipt Artifacts
- `workspace/word_context_probe/wctx_13_enko_decode_review_cases.json`
- `workspace/word_context_probe/wctx_13_enko_decode_review_matrix.json`
- `workspace/word_context_probe/wctx_13_enko_decode_review_summary.json`
- `workspace/word_context_probe/wctx_13_enko_decode_review_sample_receipt.json`
- `workspace/word_context_probe/wctx_13_static_validation.json`

## Static Matrix Summary
```json
{
  "total_cases": 24,
  "pass_cases": 24,
  "fail_cases": 0,
  "reviewed_count": 0,
  "no_candidate_count": 12,
  "blocked_count": 12,
  "candidate_available_count": 0,
  "target_text_mutation_count": 0,
  "target_subtitle_commit_count": 0,
  "commit_gate_open_count": 0,
  "decode_executed_in_review_count": 0,
  "generation_executed_in_review_count": 0,
  "model_forward_executed_in_review_count": 0,
  "sampling_executed_in_review_count": 0,
  "runtime_default_apply_count": 0,
  "rerank_applied_count": 0
}
```

## Acceptance Checks
- [PASS] EN-KO translation subtitle domain SSOT retained.
- [PASS] WCTX-12 decode staging receipt input supported.
- [PASS] `NoCandidateAvailable` is represented without inventing candidate output.
- [PASS] blocked WCTX-12 staging receipts remain blocked in WCTX-13 review.
- [PASS] target preservation diff receipt generated.
- [PASS] target original mutation remains false.
- [PASS] target subtitle commit remains false.
- [PASS] commit gate remains closed.
- [PASS] runtime default apply remains false.
- [PASS] review stage does not execute decode/generation/model forward/sampling.
- [PASS] matrix/summary/sample receipt artifacts generated.

## Toolchain Status
`PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE`

The current container does not provide `cargo`/`rustc`, so runtime compilation was not executed here. The patch is baked as Rust source plus deterministic static receipts.
