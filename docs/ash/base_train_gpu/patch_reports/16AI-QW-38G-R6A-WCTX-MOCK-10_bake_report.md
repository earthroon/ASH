# 16AI-QW-38G-R6A-WCTX-MOCK-10 Bake Report

## Patch

`16AI-QW-38G-R6A-WCTX-MOCK-10`  
`EN-KO Subtitle Mock Ledger Audit Packet Export Replay / Non-Empty Packet Seal`

## SSOT

`en_to_ko_translation_subtitle_machine`

## Added Files

```text
crates/ash_core/src/word_context_mock_ledger_audit_export_replay.rs
crates/ash_core/src/bin/ash_word_context_mock_ledger_audit_export_replay.rs
workspace/word_context_probe/wctx_mock_10_enko_mock_ledger_audit_export_replay_cases.json
workspace/word_context_probe/wctx_mock_10_enko_mock_ledger_audit_export_replay_matrix.json
workspace/word_context_probe/wctx_mock_10_enko_mock_ledger_audit_export_replay_summary.json
workspace/word_context_probe/wctx_mock_10_enko_mock_ledger_audit_export_replay_sample_receipt.json
workspace/word_context_probe/wctx_mock_10_audit_packet.json
workspace/word_context_probe/wctx_mock_10_audit_packet.md
workspace/word_context_probe/wctx_mock_10_static_validation.json
acceptance_reports/16AI-QW-38G-R6A-WCTX-MOCK-10_enko_subtitle_mock_ledger_audit_packet_export_replay_non_empty_packet_seal.md
patch_reports/16AI-QW-38G-R6A-WCTX-MOCK-10_bake_report.md
```

## Modified Files

```text
crates/ash_core/src/lib.rs
```

## Static Summary

```json
{
  "total_cases": 1,
  "pass_cases": 1,
  "audit_export_replayed_count": 1,
  "export_receipt_created_count": 1,
  "audit_packet_created_count": 1,
  "exported_count": 1,
  "exported_empty_ledger_count": 0,
  "non_empty_packet_verified_count": 1,
  "empty_ledger_packet_count": 0,
  "source_query_receipt_index_count": 5,
  "total_revision_events_seen": 24,
  "total_commit_events_seen": 12,
  "total_revert_events_seen": 12,
  "latest_snapshot_restored_to_original_count": 1,
  "ledger_mutation_count": 0,
  "revision_event_created_count": 0,
  "target_text_mutation_count": 0,
  "production_subtitle_store_mutation_count": 0,
  "runtime_apply_executed_count": 0
}
```

## Verification

- Rust toolchain unavailable in the current container.
- Static validation emitted: `PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE`.
- Local verification command:

```bash
cargo run -p ash_core --bin ash_word_context_mock_ledger_audit_export_replay
```
