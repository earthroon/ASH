# 16AI-QW-38G-R6A-WCTX-MOCK-13 Acceptance Report

## Patch

`16AI-QW-38G-R6A-WCTX-MOCK-13`  
`EN-KO Subtitle Mock Audit Archive Query Replay / Non-Empty Registry Inspector Seal`

## SSOT

`en_to_ko_translation_subtitle_machine`

## Acceptance Result

PASS static validation.

## Confirmed Invariants

```text
RegistrySummary=QueryOk
EntryByPacketHash=EntryFound
EntryByPacketId=EntryFound
NonEmptyRegistryEntry=EntryFound via WCTX-24 EntryById inspection
DuplicateEvidence=NoDuplicateEvidence
CollisionEvidence=NoCollisionEvidence
ImmutableRegistryInspector=ImmutableRegistryPass
registry_entry_count=1
non_empty_entry_count=1
empty_ledger_entry_count=0
revision_ledger_audit_packet_entry_found=true
empty_ledger_entry_detected=false
archive_entry_kind=RevisionLedgerAuditPacket
packet_hash_present=true
manifest_key_present=true
total_revision_events_seen=24
total_commit_events_seen=12
total_revert_events_seen=12
source_query_receipt_index_count=5
duplicate_packet_detected=false
hash_collision_detected=false
immutable_registry=true
registry_read_only=true
entry_immutable=true
entry_read_only=true
archive_registry_mutated=false
archive_entry_created_during_query=false
archive_entry_deleted_during_query=false
archive_entry_superseded_during_query=false
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

MOCK-13 replays the MOCK-12 non-empty immutable archive registry through WCTX-24 archive query logic. It creates seven read-only query receipts and verifies that the archived entry remains a non-empty `RevisionLedgerAuditPacket`, not an empty-ledger archive entry.

## Toolchain Note

Rust toolchain was unavailable in the current container, so this bake includes static Rust source, deterministic probe JSON, summary JSON, sample receipt JSON, and static validation receipt.
