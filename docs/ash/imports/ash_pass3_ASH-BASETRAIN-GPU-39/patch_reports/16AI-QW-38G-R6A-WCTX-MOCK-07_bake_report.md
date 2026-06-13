# 16AI-QW-38G-R6A-WCTX-MOCK-07 Bake Report

## Patch
`16AI-QW-38G-R6A-WCTX-MOCK-07`

## Title
EN-KO Subtitle Mock Single-Cue Commit Rollback Replay / Revert Receipt Seal

## Files Added

```text
crates/ash_core/src/word_context_mock_single_cue_rollback_replay.rs
crates/ash_core/src/bin/ash_word_context_mock_single_cue_rollback_replay.rs
workspace/word_context_probe/wctx_mock_07_enko_mock_single_cue_rollback_replay_cases.json
workspace/word_context_probe/wctx_mock_07_enko_mock_single_cue_rollback_replay_matrix.json
workspace/word_context_probe/wctx_mock_07_enko_mock_single_cue_rollback_replay_summary.json
workspace/word_context_probe/wctx_mock_07_enko_mock_single_cue_rollback_replay_sample_receipt.json
workspace/word_context_probe/wctx_mock_07_static_validation.json
acceptance_reports/16AI-QW-38G-R6A-WCTX-MOCK-07_enko_subtitle_mock_single_cue_commit_rollback_replay_revert_receipt_seal.md
patch_reports/16AI-QW-38G-R6A-WCTX-MOCK-07_bake_report.md
```

## Files Modified

```text
crates/ash_core/src/lib.rs
```

## Core APIs

```rust
pub fn default_enko_mock_single_cue_rollback_replay_commit_replay_receipts(
) -> Vec<EnKoMockSingleCueCommitReplayReceipt>

pub fn build_enko_mock_single_cue_rollback_replay_receipt(
    commit_replay_receipt: &EnKoMockSingleCueCommitReplayReceipt,
) -> EnKoMockSingleCueRollbackReplayReceipt

pub fn run_enko_mock_single_cue_rollback_replay_matrix(
    commit_replay_receipts: &[EnKoMockSingleCueCommitReplayReceipt],
) -> EnKoMockSingleCueRollbackReplayMatrix
```

## Invariants

```text
single_cue_rollback_replayed=true
single_cue_rollback_receipt_created=true
single_cue_rollback_status=Reverted
rollback_patch_created=true
rollback_executed_in_receipt=true
target_restored_to_original_in_receipt=true
target_text_mutated_in_receipt=true
rollback_snapshot_used=true
rollback_hash_mismatch=false
production_target_text_mutated=false
production_subtitle_store_mutated=false
single_cue_only=true
runtime_default_apply=false
runtime_apply_executed=false
rerank_applied=false
```

## Result
MOCK-07 closes the mock rollback replay path by feeding the MOCK-06 WCTX-17 `Committed` receipt into WCTX-18 rollback logic. It creates `Reverted` evidence for all 12 mock cues while preserving production store isolation and runtime-apply closure.
