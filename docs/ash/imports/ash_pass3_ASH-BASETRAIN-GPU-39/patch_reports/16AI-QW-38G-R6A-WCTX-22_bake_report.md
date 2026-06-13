# 16AI-QW-38G-R6A-WCTX-22 Bake Report

## Patch

`16AI-QW-38G-R6A-WCTX-22`

## Name

EN-KO Subtitle Audit Packet Query / Export Inspector Seal

## SSOT

`en_to_ko_translation_subtitle_machine`

## Added

- `word_context_commit_ledger_export_inspector.rs`
- `ash_word_context_commit_ledger_export_inspector.rs`
- WCTX-22 inspector case/matrix/summary/sample receipt JSON outputs
- WCTX-22 static validation receipt
- WCTX-22 acceptance and bake reports

## Modified

- `crates/ash_core/src/lib.rs`

## Summary

WCTX-22 inspects the WCTX-21 audit packet without mutating the audit packet, ledger, target subtitle, runtime state, or rerank state. The default WCTX-21 packet is an exported empty ledger packet, so the baked inspector status is `InspectionPassEmptyLedger`.

## Static Matrix

```json
{
  "total_cases": 1,
  "pass_cases": 1,
  "inspection_pass_empty_ledger_count": 1,
  "missing_required_section_count": 0,
  "hash_mismatch_detected_count": 0,
  "ledger_mutation_count": 0,
  "audit_packet_mutation_count": 0,
  "target_text_mutation_count": 0,
  "runtime_default_apply_count": 0
}
```
