# 16AI-QW-38G-R6A-WCTX-MOCK-14 Bake Report

## Added

- `crates/ash_core/src/word_context_mock_wctx_e2e_chain_index.rs`
- `crates/ash_core/src/bin/ash_word_context_mock_wctx_e2e_chain_index.rs`
- `workspace/word_context_probe/wctx_mock_14_enko_mock_wctx_e2e_chain_index_cases.json`
- `workspace/word_context_probe/wctx_mock_14_enko_mock_wctx_e2e_chain_index_matrix.json`
- `workspace/word_context_probe/wctx_mock_14_enko_mock_wctx_e2e_chain_index_summary.json`
- `workspace/word_context_probe/wctx_mock_14_enko_mock_wctx_e2e_chain_index_sample_receipt.json`
- `workspace/word_context_probe/wctx_mock_14_chain_index.json`
- `workspace/word_context_probe/wctx_mock_14_static_validation.json`

## Modified

- `crates/ash_core/src/lib.rs`

## Summary

MOCK-14 indexes MOCK-01 through MOCK-13 as an end-to-end read-only path closure. It verifies source-key continuity, stage counts, per-cue closure, aggregate audit/archive closure, and no production/runtime mutation.

## Static result

```json
{
  "patch_id": "16AI-QW-38G-R6A-WCTX-MOCK-14",
  "domain_ssot": "en_to_ko_translation_subtitle_machine",
  "total_cases": 1,
  "pass_cases": 1,
  "fail_cases": 0,
  "deterministic_failures": 0,
  "risk_failures": 0,
  "chain_indexed_count": 1,
  "blocked_missing_stage_count": 0,
  "blocked_receipt_count_mismatch_count": 0,
  "blocked_stage_status_mismatch_count": 0,
  "blocked_source_key_mismatch_count": 0,
  "blocked_duplicate_receipt_key_count": 0,
  "blocked_cue_chain_missing_count": 0,
  "blocked_aggregate_chain_missing_count": 0,
  "blocked_non_empty_audit_closure_missing_count": 0,
  "blocked_archive_closure_missing_count": 0,
  "blocked_mutation_invariant_breach_count": 0,
  "blocked_runtime_apply_gate_open_count": 0,
  "blocked_mock_mislabeled_as_runtime_count": 0,
  "stage_count": 13,
  "total_indexed_receipt_count": 90,
  "per_cue_chain_count": 12,
  "per_cue_chain_closed_count": 12,
  "aggregate_chain_count": 1,
  "aggregate_chain_closed_count": 1,
  "receipt_link_count": 72,
  "source_key_mismatch_count": 0,
  "duplicate_receipt_key_count": 0,
  "non_empty_audit_closure_verified_count": 1,
  "archive_query_closure_verified_count": 1,
  "total_revision_events_seen": 24,
  "total_commit_events_seen": 12,
  "total_revert_events_seen": 12,
  "registry_entry_count": 1,
  "non_empty_entry_count": 1,
  "empty_ledger_entry_count": 0,
  "runtime_decode_executed_count": 0,
  "generation_executed_count": 0,
  "model_forward_executed_count": 0,
  "sampling_executed_count": 0,
  "production_target_text_mutation_count": 0,
  "production_subtitle_store_mutation_count": 0,
  "runtime_default_apply_count": 0,
  "runtime_apply_gate_open_count": 0,
  "runtime_apply_executed_count": 0,
  "rerank_applied_count": 0,
  "mock_mislabeled_as_runtime_count": 0,
  "production_safe_true_count": 0
}
```
