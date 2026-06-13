# 16AI-QW-38G-R6A-WCTX-MOCK-03 Bake Report

## Added files
- `crates/ash_core/src/word_context_mock_candidate_approval_fixture.rs`
- `crates/ash_core/src/bin/ash_word_context_mock_candidate_approval_fixture.rs`
- `workspace/word_context_probe/wctx_mock_03_enko_mock_candidate_approval_fixture_cases.json`
- `workspace/word_context_probe/wctx_mock_03_enko_mock_candidate_approval_fixture_matrix.json`
- `workspace/word_context_probe/wctx_mock_03_enko_mock_candidate_approval_fixture_summary.json`
- `workspace/word_context_probe/wctx_mock_03_enko_mock_candidate_approval_fixture_sample_receipt.json`
- `workspace/word_context_probe/wctx_mock_03_static_validation.json`
- `acceptance_reports/16AI-QW-38G-R6A-WCTX-MOCK-03_enko_subtitle_mock_candidate_human_approval_fixture_no_target_commit_seal.md`
- `patch_reports/16AI-QW-38G-R6A-WCTX-MOCK-03_bake_report.md`

## Modified files
- `crates/ash_core/src/lib.rs`

## Core API
```rust
pub fn default_enko_mock_candidate_approval_fixture_replay_receipts(
) -> Vec<EnKoMockCandidateReviewReplayReceipt>

pub fn build_enko_mock_candidate_approval_fixture_receipt(
    replay_receipt: &EnKoMockCandidateReviewReplayReceipt,
) -> EnKoMockCandidateApprovalFixtureReceipt

pub fn run_enko_mock_candidate_approval_fixture_matrix(
    replay_receipts: &[EnKoMockCandidateReviewReplayReceipt],
) -> EnKoMockCandidateApprovalFixtureMatrix
```

## Static summary
```json
{
  "approval_fixture_created_count": 12,
  "approval_receipt_created_count": 12,
  "approved_for_target_update_candidate_count": 12,
  "approval_valid_count": 12,
  "can_proceed_to_target_update_candidate_count": 12,
  "target_update_candidate_gate_open_count": 12,
  "can_commit_target_update_count": 0,
  "target_commit_gate_open_count": 0,
  "actual_human_approval_created_count": 0,
  "production_approval_created_count": 0,
  "target_update_candidate_created_count": 0,
  "target_text_mutation_count": 0,
  "runtime_default_apply_count": 0
}
```

## Notes
The container has no `cargo` or `rustc`; this bake includes static validation artifacts and a local run command for toolchain-backed verification.
