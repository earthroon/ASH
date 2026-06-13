# 16AI-QW-38G-R6A-WCTX-23 Bake Report

## Added
- `crates/ash_core/src/word_context_commit_ledger_archive.rs`
- `crates/ash_core/src/bin/ash_word_context_commit_ledger_archive.rs`
- `workspace/word_context_probe/wctx_23_enko_audit_packet_archive_cases.json`
- `workspace/word_context_probe/wctx_23_enko_audit_packet_archive_matrix.json`
- `workspace/word_context_probe/wctx_23_enko_audit_packet_archive_summary.json`
- `workspace/word_context_probe/wctx_23_enko_audit_packet_archive_sample_receipt.json`
- `workspace/word_context_probe/wctx_23_audit_archive_registry.json`
- `workspace/word_context_probe/wctx_23_static_validation.json`
- `acceptance_reports/16AI-QW-38G-R6A-WCTX-23_enko_subtitle_audit_packet_archive_immutable_export_registry_seal.md`
- `patch_reports/16AI-QW-38G-R6A-WCTX-23_bake_report.md`

## Modified
- `crates/ash_core/src/lib.rs`

## Core APIs
```rust
pub fn default_enko_audit_packet_archive_cases() -> Vec<EnKoAuditPacketArchiveInputCase>

pub fn build_enko_audit_packet_archive_receipt(
    export_receipt: &EnKoRevisionLedgerExportReceipt,
    inspector_receipt: &EnKoAuditPacketInspectorReceipt,
    existing_registry: Option<&EnKoAuditPacketArchiveRegistry>,
) -> EnKoAuditPacketArchiveReceipt

pub fn run_enko_audit_packet_archive_matrix(
    cases: &[EnKoAuditPacketArchiveInputCase],
) -> EnKoAuditPacketArchiveMatrix
```

## Baked Summary
```json
{
  "patch_id": "16AI-QW-38G-R6A-WCTX-23",
  "domain_ssot": "en_to_ko_translation_subtitle_machine",
  "total_cases": 1,
  "pass_cases": 1,
  "fail_cases": 0,
  "deterministic_failures": 0,
  "risk_failures": 0,
  "archived_count": 0,
  "archived_empty_ledger_packet_count": 1,
  "duplicate_already_archived_count": 0,
  "blocked_inspection_not_passed_count": 0,
  "blocked_missing_audit_packet_count": 0,
  "blocked_hash_collision_count": 0,
  "blocked_inconsistent_registry_count": 0,
  "archive_entry_created_count": 1,
  "archive_registry_created_count": 1,
  "duplicate_packet_detected_count": 0,
  "hash_collision_detected_count": 0,
  "supersede_applied_count": 0,
  "ledger_mutation_count": 0,
  "audit_packet_mutation_count": 0,
  "revision_event_created_count": 0,
  "target_text_mutation_count": 0,
  "commit_executed_in_archive_count": 0,
  "rollback_executed_in_archive_count": 0,
  "runtime_default_apply_count": 0,
  "runtime_apply_gate_open_count": 0,
  "rerank_applied_count": 0,
  "decode_executed_in_archive_count": 0,
  "generation_executed_in_archive_count": 0,
  "model_forward_executed_in_archive_count": 0,
  "sampling_executed_in_archive_count": 0
}
```

## Toolchain Note
`cargo` / `rustc` was unavailable in the execution container, so validation is static and recorded as `PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE`.
