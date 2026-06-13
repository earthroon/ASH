# 16AI-QW-38G-R6A-WCTX-MOCK-12 Acceptance Report

## Patch

`16AI-QW-38G-R6A-WCTX-MOCK-12`  
`EN-KO Subtitle Mock Audit Packet Archive Replay / Non-Empty Registry Seal`

## SSOT

`en_to_ko_translation_subtitle_machine`

## Acceptance Result

PASS static validation.

## Confirmed Invariants

```text
archive_status=Archived
archive_status != ArchivedEmptyLedgerPacket
archive_receipt_created=true
archive_entry_created=true
archive_registry_created=true
non_empty_archive_verified=true
empty_ledger_packet=false
archive_entry_kind=RevisionLedgerAuditPacket
total_revision_events_seen=24
total_commit_events_seen=12
total_revert_events_seen=12
source_query_receipt_index_count=5
duplicate_packet_detected=false
hash_collision_detected=false
supersede_applied=false
immutable_registry=true
registry_read_only=true
entry_immutable=true
entry_read_only=true
audit_packet_mutated=false
ledger_mutated=false
revision_event_created=false
target_text_mutated=false
production_subtitle_store_mutated=false
runtime_default_apply=false
runtime_apply_gate_open=false
runtime_apply_executed=false
rerank_applied=false
```

## Scope

MOCK-12 replays the MOCK-10 non-empty audit export receipt and MOCK-11 inspector pass receipt through the WCTX-23 archive path. It creates a non-empty immutable archive registry entry and keeps duplicate/hash-collision/supersede guards closed for the default case.

## Toolchain Note

Rust toolchain was unavailable in the current container, so this bake includes static Rust source, deterministic probe JSON, summary JSON, archive registry JSON, and static validation receipt.
