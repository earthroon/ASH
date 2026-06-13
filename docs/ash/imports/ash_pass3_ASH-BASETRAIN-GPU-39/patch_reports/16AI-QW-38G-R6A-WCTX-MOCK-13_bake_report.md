# 16AI-QW-38G-R6A-WCTX-MOCK-13 Bake Report

## Patch

`16AI-QW-38G-R6A-WCTX-MOCK-13`  
`EN-KO Subtitle Mock Audit Archive Query Replay / Non-Empty Registry Inspector Seal`

## SSOT

`en_to_ko_translation_subtitle_machine`

## Added Files

```text
crates/ash_core/src/word_context_mock_audit_archive_query_replay.rs
crates/ash_core/src/bin/ash_word_context_mock_audit_archive_query_replay.rs
workspace/word_context_probe/wctx_mock_13_enko_mock_audit_archive_query_replay_cases.json
workspace/word_context_probe/wctx_mock_13_enko_mock_audit_archive_query_replay_matrix.json
workspace/word_context_probe/wctx_mock_13_enko_mock_audit_archive_query_replay_summary.json
workspace/word_context_probe/wctx_mock_13_enko_mock_audit_archive_query_replay_sample_receipt.json
workspace/word_context_probe/wctx_mock_13_static_validation.json
acceptance_reports/16AI-QW-38G-R6A-WCTX-MOCK-13_enko_subtitle_mock_audit_archive_query_replay_non_empty_registry_inspector_seal.md
patch_reports/16AI-QW-38G-R6A-WCTX-MOCK-13_bake_report.md
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
  "audit_archive_query_replayed_count": 1,
  "query_receipts_created_count": 7,
  "registry_summary_query_ok_count": 1,
  "entry_by_packet_hash_found_count": 1,
  "entry_by_packet_id_found_count": 1,
  "non_empty_entry_found_count": 1,
  "no_duplicate_evidence_count": 1,
  "no_collision_evidence_count": 1,
  "immutable_registry_pass_count": 1,
  "registry_entry_count": 1,
  "non_empty_entry_count": 1,
  "empty_ledger_entry_count": 0,
  "revision_ledger_audit_packet_entry_found_count": 1,
  "empty_ledger_entry_detected_count": 0,
  "total_revision_events_seen": 24,
  "total_commit_events_seen": 12,
  "total_revert_events_seen": 12,
  "source_query_receipt_index_count": 5,
  "archive_registry_mutation_count": 0,
  "archive_entry_created_during_query_count": 0,
  "audit_packet_mutation_count": 0,
  "ledger_mutation_count": 0,
  "target_text_mutation_count": 0,
  "runtime_apply_executed_count": 0
}
```

## Verification

- Rust toolchain unavailable in the current container.
- Static validation emitted: `PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE`.
- Local verification command:

```bash
cargo run -p ash_core --bin ash_word_context_mock_audit_archive_query_replay
```
