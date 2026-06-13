# 16AI-QW-38G-R6A-WCTX-MOCK-09 Acceptance Report

## SSOT
- domain_ssot: `en_to_ko_translation_subtitle_machine`
- domain: EN-KO translation subtitle machine

## Result
- status: `PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE`
- replay_status: `LedgerQueryReplayed`
- query_receipts_created_count: 5
- LedgerSummary: `QueryOk`
- CueHistoryById: `CueHistoryFound`
- LatestTargetByCueId: `LatestTargetFound`
- IntegrityInspector: `IntegrityPass`
- FullCueHistoryDump: `QueryOk`

## Ledger observations
- cue_revision_chain_count_seen: 12
- total_revision_events_seen: 24
- total_commit_events_seen: 12
- total_revert_events_seen: 12
- sample_cue_id: `WCTX03-C003`
- sample_cue_event_count: 2
- sample_cue_commit_count: 1
- sample_cue_revert_count: 1
- latest_snapshot_event_kind: `Revert`
- latest_snapshot_restored_to_original: true

## No-mutation invariants
- ledger_mutation_count: 0
- revision_event_created_count: 0
- target_text_mutation_count: 0
- production_target_text_mutation_count: 0
- production_subtitle_store_mutation_count: 0
- runtime_default_apply_count: 0
- runtime_apply_gate_open_count: 0
- runtime_apply_executed_count: 0
- rerank_applied_count: 0

## Notes
MOCK-09 reuses WCTX-20 `build_enko_revision_ledger_query_receipt()` for LedgerSummary, CueHistoryById, LatestTargetByCueId, IntegrityInspector, and FullCueHistoryDump. It reads the MOCK-08 LedgerBuilt receipt and does not mutate the ledger, target subtitle, production subtitle store, runtime state, or rerank state.
