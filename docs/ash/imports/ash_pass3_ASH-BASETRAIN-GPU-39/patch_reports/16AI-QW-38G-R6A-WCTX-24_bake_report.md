# 16AI-QW-38G-R6A-WCTX-24 Bake Report

## Patch

`16AI-QW-38G-R6A-WCTX-24` — EN-KO Subtitle Audit Archive Query / Immutable Registry Inspector Seal

## Files Added

```text
crates/ash_core/src/word_context_commit_ledger_archive_query.rs
crates/ash_core/src/bin/ash_word_context_commit_ledger_archive_query.rs
workspace/word_context_probe/wctx_24_enko_audit_archive_query_cases.json
workspace/word_context_probe/wctx_24_enko_audit_archive_query_matrix.json
workspace/word_context_probe/wctx_24_enko_audit_archive_query_summary.json
workspace/word_context_probe/wctx_24_enko_audit_archive_query_sample_receipt.json
workspace/word_context_probe/wctx_24_static_validation.json
acceptance_reports/16AI-QW-38G-R6A-WCTX-24_enko_subtitle_audit_archive_query_immutable_registry_inspector_seal.md
patch_reports/16AI-QW-38G-R6A-WCTX-24_bake_report.md
```

## Files Modified

```text
crates/ash_core/src/lib.rs
```

## Core API

```rust
pub fn default_enko_audit_archive_query_cases() -> Vec<EnKoAuditArchiveQueryInputCase>

pub fn build_enko_audit_archive_query_receipt(
    archive_receipt: &EnKoAuditPacketArchiveReceipt,
    query_input: EnKoAuditArchiveQueryInput,
) -> EnKoAuditArchiveQueryReceipt

pub fn run_enko_audit_archive_query_matrix(
    cases: &[EnKoAuditArchiveQueryInputCase],
) -> EnKoAuditArchiveQueryMatrix
```

## Baked Default Cases

```text
RegistrySummary             -> QueryOk
EmptyLedgerEntries          -> EmptyLedgerEntryFound
EntryByPacketHash           -> EntryFound
EntryByPacketId             -> EntryFound
DuplicateEvidence           -> NoDuplicateEvidence
CollisionEvidence           -> NoCollisionEvidence
ImmutableRegistryInspector  -> ImmutableRegistryPass
```

## Safety Invariants

```text
archive_registry_mutated=false
archive_entry_created=false
archive_entry_deleted=false
archive_entry_superseded=false
audit_packet_mutated=false
ledger_mutated=false
revision_event_created=false
target_text_mutated=false
runtime_default_apply=false
rerank_applied=false
```

## Validation

Static validation passed with `PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE` because the current environment does not provide a Rust toolchain.
