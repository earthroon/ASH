# 16AI-QW-38G-R6A-WCTX-MOCK-06 Bake Report

## Patch
`16AI-QW-38G-R6A-WCTX-MOCK-06`

## Title
EN-KO Subtitle Mock Approved Single-Cue Commit Replay / Target Apply Receipt Seal

## Files Added

```text
crates/ash_core/src/word_context_mock_single_cue_commit_replay.rs
crates/ash_core/src/bin/ash_word_context_mock_single_cue_commit_replay.rs
workspace/word_context_probe/wctx_mock_06_enko_mock_single_cue_commit_replay_cases.json
workspace/word_context_probe/wctx_mock_06_enko_mock_single_cue_commit_replay_matrix.json
workspace/word_context_probe/wctx_mock_06_enko_mock_single_cue_commit_replay_summary.json
workspace/word_context_probe/wctx_mock_06_enko_mock_single_cue_commit_replay_sample_receipt.json
workspace/word_context_probe/wctx_mock_06_static_validation.json
acceptance_reports/16AI-QW-38G-R6A-WCTX-MOCK-06_enko_subtitle_mock_approved_single_cue_commit_replay_target_apply_receipt_seal.md
patch_reports/16AI-QW-38G-R6A-WCTX-MOCK-06_bake_report.md
```

## Files Modified

```text
crates/ash_core/src/lib.rs
```

## Core APIs

```rust
pub fn default_enko_mock_single_cue_commit_replay_commit_approval_fixture_receipts(
) -> Vec<EnKoMockCommitApprovalFixtureReceipt>

pub fn build_enko_mock_single_cue_commit_replay_receipt(
    commit_approval_fixture_receipt: &EnKoMockCommitApprovalFixtureReceipt,
) -> EnKoMockSingleCueCommitReplayReceipt

pub fn run_enko_mock_single_cue_commit_replay_matrix(
    commit_approval_fixture_receipts: &[EnKoMockCommitApprovalFixtureReceipt],
) -> EnKoMockSingleCueCommitReplayMatrix
```

## Invariants

```text
single_cue_commit_replayed=true
single_cue_commit_receipt_created=true
single_cue_commit_status=Committed
commit_patch_created=true
rollback_snapshot_created=true
target_text_mutated_in_receipt=true
target_subtitle_committed_in_receipt=true
candidate_applied_to_target_in_receipt=true
production_target_text_mutated=false
production_subtitle_store_mutated=false
single_cue_only=true
runtime_default_apply=false
runtime_apply_executed=false
rerank_applied=false
```

## Result
MOCK-06 opens the WCTX-17 committed receipt path for the mock line while preserving production store isolation. It creates rollback snapshots for every committed mock cue and does not enable runtime apply, rerank, or production promotion.
