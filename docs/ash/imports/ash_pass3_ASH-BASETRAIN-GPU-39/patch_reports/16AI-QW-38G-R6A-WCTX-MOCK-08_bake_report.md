# 16AI-QW-38G-R6A-WCTX-MOCK-08 Bake Report

## Added
- `crates/ash_core/src/word_context_mock_commit_rollback_ledger_replay.rs`
- `crates/ash_core/src/bin/ash_word_context_mock_commit_rollback_ledger_replay.rs`
- `workspace/word_context_probe/wctx_mock_08_enko_mock_commit_rollback_ledger_replay_cases.json`
- `workspace/word_context_probe/wctx_mock_08_enko_mock_commit_rollback_ledger_replay_matrix.json`
- `workspace/word_context_probe/wctx_mock_08_enko_mock_commit_rollback_ledger_replay_summary.json`
- `workspace/word_context_probe/wctx_mock_08_enko_mock_commit_rollback_ledger_replay_sample_receipt.json`
- `workspace/word_context_probe/wctx_mock_08_static_validation.json`
- `acceptance_reports/16AI-QW-38G-R6A-WCTX-MOCK-08_enko_subtitle_mock_commit_rollback_ledger_replay_ledgerbuilt_seal.md`

## Modified
- `crates/ash_core/src/lib.rs`

## Summary
MOCK-06 `Committed` receipts and MOCK-07 `Reverted` receipts are replayed through WCTX-19 ledger construction. The baked expected matrix closes as `LedgerBuilt` with 12 cue revision chains, 24 total events, 12 commit events, 12 revert events, and 12 verified parent links.
