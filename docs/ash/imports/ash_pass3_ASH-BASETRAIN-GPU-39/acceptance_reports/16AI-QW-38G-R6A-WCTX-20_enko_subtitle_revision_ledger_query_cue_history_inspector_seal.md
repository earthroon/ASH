# 16AI-QW-38G-R6A-WCTX-20 Acceptance Report

## EN-KO Subtitle Revision Ledger Query / Cue History Inspector Seal

SSOT: `en_to_ko_translation_subtitle_machine`

## Result

PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE

## Implemented files

- `crates/ash_core/src/word_context_commit_ledger_query.rs`
- `crates/ash_core/src/bin/ash_word_context_commit_ledger_query.rs`
- `workspace/word_context_probe/wctx_20_enko_commit_ledger_query_cases.json`
- `workspace/word_context_probe/wctx_20_enko_commit_ledger_query_matrix.json`
- `workspace/word_context_probe/wctx_20_enko_commit_ledger_query_summary.json`
- `workspace/word_context_probe/wctx_20_enko_commit_ledger_query_sample_receipt.json`
- `workspace/word_context_probe/wctx_20_static_validation.json`

## Acceptance invariants

- Ledger query is read-only.
- Empty ledger is a valid empty result.
- Missing cue history is reported as `CueHistoryNotFound` without fabrication.
- Missing latest target is reported as `LatestTargetUnavailable` without fabrication.
- Integrity inspector reports ledger status without repair.
- `ledger_mutated=false`.
- `revision_event_created=false`.
- `target_text_mutated=false`.
- `commit_executed_in_query=false`.
- `rollback_executed_in_query=false`.
- `runtime_default_apply=false`.
- `rerank_applied=false`.
- No decode/generation/model_forward/sampling execution occurs in the query layer.

## Static matrix summary

```json
{
  "total_cases": 4,
  "pass_cases": 4,
  "fail_cases": 0,
  "empty_result_count": 1,
  "cue_history_not_found_count": 1,
  "latest_target_unavailable_count": 1,
  "integrity_pass_count": 1,
  "total_revision_events_seen": 0,
  "ledger_mutation_count": 0,
  "revision_event_created_count": 0,
  "target_text_mutation_count": 0,
  "runtime_default_apply_count": 0
}
```
