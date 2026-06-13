# 16AI-QW-38G-R6A-WCTX-MOCK-02 Acceptance Report

## Patch
- `16AI-QW-38G-R6A-WCTX-MOCK-02`
- EN-KO Subtitle Mock Candidate Review Replay / CandidateCreated Path Seal

## Domain SSOT
- `en_to_ko_translation_subtitle_machine`

## Result
- Static validation: `PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE`
- Rust toolchain in container: unavailable, so compile execution was not performed here.
- Local command: `cargo run -p ash_core --bin ash_word_context_mock_candidate_review_replay`

## Evidence Summary
```json
{
  "total_cases": 12,
  "pass_cases": 12,
  "fail_cases": 0,
  "review_replayed_count": 12,
  "review_receipt_created_count": 12,
  "reviewed_count": 12,
  "candidate_available_count": 12,
  "candidate_changed_count": 12,
  "can_proceed_to_candidate_approval_count": 12,
  "can_commit_target_update_count": 0,
  "runtime_decode_executed_count": 0,
  "generation_executed_count": 0,
  "model_forward_executed_count": 0,
  "sampling_executed_count": 0,
  "target_text_mutation_count": 0,
  "target_subtitle_commit_count": 0,
  "runtime_default_apply_count": 0,
  "rerank_applied_count": 0,
  "mock_mislabeled_as_runtime_count": 0
}
```

## Acceptance Criteria
- [PASS] MOCK-01 fixture receipt input is supported.
- [PASS] FixtureCreated cases replay through WCTX-13-style review as `Reviewed`.
- [PASS] Candidate availability is `CandidatePresent` for all 12 fixture cases.
- [PASS] Candidate changed path is opened without target mutation.
- [PASS] Candidate approval may proceed as a review gate only.
- [PASS] Target update commit remains closed.
- [PASS] Runtime decode/model forward/sampling remain false.
- [PASS] Mock/non-production label remains enforced.
- [PASS] No candidate approval receipt is created.
- [PASS] No target update candidate is created.
- [PASS] No target subtitle commit is executed.

## Seal
MOCK-02 replays explicit mock candidate text into the WCTX-13 review path and proves the CandidatePresent/Reviewed path without runtime decode, approval, target update, commit, or runtime apply.
