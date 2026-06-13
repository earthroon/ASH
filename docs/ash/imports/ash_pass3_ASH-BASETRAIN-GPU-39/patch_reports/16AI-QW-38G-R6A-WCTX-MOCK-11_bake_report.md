# 16AI-QW-38G-R6A-WCTX-MOCK-11 Bake Report

## Patch

`16AI-QW-38G-R6A-WCTX-MOCK-11`  
`EN-KO Subtitle Mock Audit Packet Inspector Replay / Non-Empty Packet Integrity Seal`

## SSOT

`en_to_ko_translation_subtitle_machine`

## Added Files

```text
crates/ash_core/src/word_context_mock_audit_packet_inspector_replay.rs
crates/ash_core/src/bin/ash_word_context_mock_audit_packet_inspector_replay.rs
workspace/word_context_probe/wctx_mock_11_enko_mock_audit_packet_inspector_replay_cases.json
workspace/word_context_probe/wctx_mock_11_enko_mock_audit_packet_inspector_replay_matrix.json
workspace/word_context_probe/wctx_mock_11_enko_mock_audit_packet_inspector_replay_summary.json
workspace/word_context_probe/wctx_mock_11_enko_mock_audit_packet_inspector_replay_sample_receipt.json
workspace/word_context_probe/wctx_mock_11_static_validation.json
acceptance_reports/16AI-QW-38G-R6A-WCTX-MOCK-11_enko_subtitle_mock_audit_packet_inspector_replay_non_empty_packet_integrity_seal.md
patch_reports/16AI-QW-38G-R6A-WCTX-MOCK-11_bake_report.md
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
  "audit_packet_inspection_replayed_count": 1,
  "inspector_receipt_created_count": 1,
  "inspection_pass_count": 1,
  "inspection_pass_empty_ledger_count": 0,
  "non_empty_packet_verified_count": 1,
  "inspected_as_empty_ledger_count": 0,
  "required_sections_present_count": 1,
  "empty_ledger_notice_section_present_count": 0,
  "packet_hash_verified_count": 1,
  "section_hashes_verified_count": 1,
  "source_receipt_index_valid_count": 1,
  "total_revision_events_seen": 24,
  "total_commit_events_seen": 12,
  "total_revert_events_seen": 12,
  "latest_snapshot_restored_to_original_count": 1,
  "audit_packet_mutation_count": 0,
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
cargo run -p ash_core --bin ash_word_context_mock_audit_packet_inspector_replay
```
