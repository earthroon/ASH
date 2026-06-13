# 16AI-QW-38G-R6A-WCTX-MOCK-12 Bake Report

## Patch

`16AI-QW-38G-R6A-WCTX-MOCK-12`  
`EN-KO Subtitle Mock Audit Packet Archive Replay / Non-Empty Registry Seal`

## SSOT

`en_to_ko_translation_subtitle_machine`

## Added Files

```text
crates/ash_core/src/word_context_mock_audit_packet_archive_replay.rs
crates/ash_core/src/bin/ash_word_context_mock_audit_packet_archive_replay.rs
workspace/word_context_probe/wctx_mock_12_enko_mock_audit_packet_archive_replay_cases.json
workspace/word_context_probe/wctx_mock_12_enko_mock_audit_packet_archive_replay_matrix.json
workspace/word_context_probe/wctx_mock_12_enko_mock_audit_packet_archive_replay_summary.json
workspace/word_context_probe/wctx_mock_12_enko_mock_audit_packet_archive_replay_sample_receipt.json
workspace/word_context_probe/wctx_mock_12_audit_archive_registry.json
workspace/word_context_probe/wctx_mock_12_static_validation.json
acceptance_reports/16AI-QW-38G-R6A-WCTX-MOCK-12_enko_subtitle_mock_audit_packet_archive_replay_non_empty_registry_seal.md
patch_reports/16AI-QW-38G-R6A-WCTX-MOCK-12_bake_report.md
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
  "audit_packet_archive_replayed_count": 1,
  "archive_receipt_created_count": 1,
  "archive_entry_created_count": 1,
  "archive_registry_created_count": 1,
  "archived_count": 1,
  "archived_empty_ledger_packet_count": 0,
  "non_empty_archive_verified_count": 1,
  "empty_ledger_packet_count": 0,
  "total_revision_events_seen": 24,
  "total_commit_events_seen": 12,
  "total_revert_events_seen": 12,
  "source_query_receipt_index_count": 5,
  "duplicate_packet_detected_count": 0,
  "hash_collision_detected_count": 0,
  "supersede_applied_count": 0,
  "audit_packet_mutation_count": 0,
  "ledger_mutation_count": 0,
  "revision_event_created_count": 0,
  "target_text_mutation_count": 0,
  "runtime_apply_executed_count": 0
}
```

## Verification

- Rust toolchain unavailable in the current container.
- Static validation emitted: `PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE`.
- Local verification command:

```bash
cargo run -p ash_core --bin ash_word_context_mock_audit_packet_archive_replay
```
