# 16AI-QW-38G-R6A-WCTX-MOCK-05 Bake Report

## Patch
`16AI-QW-38G-R6A-WCTX-MOCK-05`

## Title
EN-KO Subtitle Mock Target Update Candidate Commit Approval Fixture / No-Apply Seal

## Files Added

```text
crates/ash_core/src/word_context_mock_commit_approval_fixture.rs
crates/ash_core/src/bin/ash_word_context_mock_commit_approval_fixture.rs
workspace/word_context_probe/wctx_mock_05_enko_mock_commit_approval_fixture_cases.json
workspace/word_context_probe/wctx_mock_05_enko_mock_commit_approval_fixture_matrix.json
workspace/word_context_probe/wctx_mock_05_enko_mock_commit_approval_fixture_summary.json
workspace/word_context_probe/wctx_mock_05_enko_mock_commit_approval_fixture_sample_receipt.json
workspace/word_context_probe/wctx_mock_05_static_validation.json
acceptance_reports/16AI-QW-38G-R6A-WCTX-MOCK-05_enko_subtitle_mock_target_update_candidate_commit_approval_fixture_no_apply_seal.md
patch_reports/16AI-QW-38G-R6A-WCTX-MOCK-05_bake_report.md
```

## Files Modified

```text
crates/ash_core/src/lib.rs
```

## Core APIs

```rust
pub fn default_enko_mock_commit_approval_fixture_target_update_replay_receipts(
) -> Vec<EnKoMockTargetUpdateCandidateReplayReceipt>

pub fn build_enko_mock_commit_approval_fixture_receipt(
    target_update_replay_receipt: &EnKoMockTargetUpdateCandidateReplayReceipt,
) -> EnKoMockCommitApprovalFixtureReceipt

pub fn run_enko_mock_commit_approval_fixture_matrix(
    target_update_replay_receipts: &[EnKoMockTargetUpdateCandidateReplayReceipt],
) -> EnKoMockCommitApprovalFixtureMatrix
```

## Invariants

```text
commit_approval_fixture_created=true
commit_approval_receipt_created=true
commit_approval_decision=ApprovedForSingleCueCommit
approval_valid=true
can_proceed_to_single_cue_commit=true
can_apply_now=false
single_cue_commit_gate_open=true
immediate_apply_gate_open=false
runtime_apply_gate_open=false
target_text_mutated=false
target_subtitle_committed=false
actual_human_approval_created=false
production_commit_approval_created=false
runtime_default_apply=false
rerank_applied=false
```

## Result
MOCK-05 opens the WCTX-17 single-cue commit receipt gate for the mock path while preserving No-Apply. It does not mutate target subtitle text, does not perform runtime application, and does not promote the mock fixture to production approval.
