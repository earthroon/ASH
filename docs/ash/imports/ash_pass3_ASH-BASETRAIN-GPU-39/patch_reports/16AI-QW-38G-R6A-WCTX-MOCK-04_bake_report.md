# 16AI-QW-38G-R6A-WCTX-MOCK-04 Bake Report

## Added files
- `crates/ash_core/src/word_context_mock_target_update_candidate_replay.rs`
- `crates/ash_core/src/bin/ash_word_context_mock_target_update_candidate_replay.rs`
- `workspace/word_context_probe/wctx_mock_04_enko_mock_target_update_candidate_replay_cases.json`
- `workspace/word_context_probe/wctx_mock_04_enko_mock_target_update_candidate_replay_matrix.json`
- `workspace/word_context_probe/wctx_mock_04_enko_mock_target_update_candidate_replay_summary.json`
- `workspace/word_context_probe/wctx_mock_04_enko_mock_target_update_candidate_replay_sample_receipt.json`
- `workspace/word_context_probe/wctx_mock_04_static_validation.json`
- `acceptance_reports/16AI-QW-38G-R6A-WCTX-MOCK-04_enko_subtitle_mock_approved_target_update_candidate_replay_manual_commit_gate_seal.md`
- `patch_reports/16AI-QW-38G-R6A-WCTX-MOCK-04_bake_report.md`

## Modified files
- `crates/ash_core/src/lib.rs`

## Core API
```rust
pub fn default_enko_mock_target_update_candidate_replay_approval_fixture_receipts(
) -> Vec<EnKoMockCandidateApprovalFixtureReceipt>

pub fn build_enko_mock_target_update_candidate_replay_receipt(
    approval_fixture_receipt: &EnKoMockCandidateApprovalFixtureReceipt,
) -> EnKoMockTargetUpdateCandidateReplayReceipt

pub fn run_enko_mock_target_update_candidate_replay_matrix(
    approval_fixture_receipts: &[EnKoMockCandidateApprovalFixtureReceipt],
) -> EnKoMockTargetUpdateCandidateReplayMatrix
```

## Static summary
```json
{
  "total_cases": 12,
  "pass_cases": 12,
  "fail_cases": 0,
  "target_update_candidate_replayed_count": 12,
  "target_update_candidate_receipt_created_count": 12,
  "candidate_created_count": 12,
  "payload_created_count": 12,
  "manual_commit_review_gate_open_count": 12,
  "target_commit_gate_open_count": 0,
  "runtime_apply_gate_open_count": 0,
  "target_update_candidate_committed_count": 0,
  "target_text_mutation_count": 0,
  "target_subtitle_commit_count": 0,
  "actual_human_approval_used_count": 0,
  "production_candidate_created_count": 0,
  "runtime_decode_executed_count": 0,
  "generation_executed_count": 0,
  "model_forward_executed_count": 0,
  "sampling_executed_count": 0,
  "runtime_default_apply_count": 0,
  "rerank_applied_count": 0,
  "mock_mislabeled_as_runtime_count": 0
}
```

## Notes
The container has no `cargo` or `rustc`; this bake includes static validation artifacts and a local run command for toolchain-backed verification.
