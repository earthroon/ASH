# 16AI-QW-38G-R6A-WCTX-14 Acceptance Report

## Patch
- `16AI-QW-38G-R6A-WCTX-14`
- `EN-KO Subtitle Decode Candidate Human Review Approval / No-Target-Commit Seal`

## Domain SSOT
- `en_to_ko_translation_subtitle_machine`
- Ash is an EN-to-KO translation subtitle-machine domain component.

## Status
- `PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE`

## Added Rust artifacts
- `crates/ash_core/src/word_context_decode_review_approval.rs`
- `crates/ash_core/src/bin/ash_word_context_decode_review_approval.rs`

## Modified Rust artifacts
- `crates/ash_core/src/lib.rs`

## Receipt artifacts
- `workspace/word_context_probe/wctx_14_enko_decode_review_approval_cases.json`
- `workspace/word_context_probe/wctx_14_enko_decode_review_approval_matrix.json`
- `workspace/word_context_probe/wctx_14_enko_decode_review_approval_summary.json`
- `workspace/word_context_probe/wctx_14_enko_decode_review_approval_sample_receipt.json`
- `workspace/word_context_probe/wctx_14_static_validation.json`

## Static matrix summary
```json
{
  "total_cases": 24,
  "pass_cases": 24,
  "fail_cases": 0,
  "pending_count": 0,
  "approved_for_target_update_candidate_count": 0,
  "no_candidate_count": 24,
  "approval_valid_count": 24,
  "target_update_candidate_gate_open_count": 0,
  "target_commit_gate_open_count": 0,
  "no_candidate_approved_count": 0,
  "auto_approved_count": 0,
  "target_text_mutation_count": 0,
  "target_subtitle_commit_count": 0,
  "runtime_default_apply_count": 0,
  "rerank_applied_count": 0
}
```

## Acceptance checks
- PASS: WCTX-13 review receipt input is supported.
- PASS: `NoCandidateAvailable` reviews become `NoCandidate` approval decisions.
- PASS: NoCandidate does not open `target_update_candidate_gate`.
- PASS: NoCandidate is not promoted to `ApprovedForTargetUpdateCandidate`.
- PASS: human/manual approval structures are present.
- PASS: `can_commit_target_update=false` is sealed.
- PASS: `can_apply_to_runtime=false` is sealed.
- PASS: `target_text_mutated=false` is sealed.
- PASS: `target_subtitle_committed=false` is sealed.
- PASS: `runtime_default_apply=false` is sealed.
- PASS: approval phase does not execute decode/generation/model_forward/sampling.

## Toolchain note
`cargo` / `rustc` were not available in the bake container, so this acceptance is static. Run locally with:

```bash
cargo run -p ash_core --bin ash_word_context_decode_review_approval
```
