# 16AI-QW-38G-R6A-WCTX-17 Bake Report

## Added
- `crates/ash_core/src/word_context_target_commit.rs`
- `crates/ash_core/src/bin/ash_word_context_target_commit.rs`
- `workspace/word_context_probe/wctx_17_enko_target_commit_cases.json`
- `workspace/word_context_probe/wctx_17_enko_target_commit_matrix.json`
- `workspace/word_context_probe/wctx_17_enko_target_commit_summary.json`
- `workspace/word_context_probe/wctx_17_enko_target_commit_sample_receipt.json`
- `workspace/word_context_probe/wctx_17_static_validation.json`

## Modified
- `crates/ash_core/src/lib.rs`

## Core APIs
- `default_enko_single_cue_target_commit_pairs()`
- `build_enko_single_cue_target_commit_receipt(...)`
- `run_enko_single_cue_target_commit_matrix(...)`

## Default Matrix
```json
{
  "patch_id": "16AI-QW-38G-R6A-WCTX-17",
  "domain_ssot": "en_to_ko_translation_subtitle_machine",
  "total_cases": 24,
  "pass_cases": 24,
  "fail_cases": 0,
  "deterministic_failures": 0,
  "risk_failures": 0,
  "committed_count": 0,
  "blocked_no_update_candidate_count": 24,
  "blocked_approval_pending_count": 0,
  "blocked_approval_rejected_count": 0,
  "blocked_needs_revision_count": 0,
  "blocked_invalid_approval_count": 0,
  "blocked_commit_gate_closed_count": 0,
  "blocked_missing_payload_count": 0,
  "blocked_missing_rollback_count": 0,
  "blocked_cue_boundary_violation_count": 0,
  "commit_patch_created_count": 0,
  "rollback_snapshot_created_count": 0,
  "target_subtitle_commit_count": 0,
  "target_text_mutation_count": 0,
  "candidate_applied_to_target_count": 0,
  "multiple_cue_mutation_detected_count": 0,
  "runtime_default_apply_count": 0,
  "runtime_apply_gate_open_count": 0,
  "rerank_applied_count": 0,
  "decode_executed_in_commit_count": 0,
  "generation_executed_in_commit_count": 0,
  "model_forward_executed_in_commit_count": 0,
  "sampling_executed_in_commit_count": 0
}
```
