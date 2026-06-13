# 16AI-QW-38G-R6A-WCTX-16 Bake Report

## Added files
- `crates/ash_core/src/word_context_target_commit_approval.rs`
- `crates/ash_core/src/bin/ash_word_context_target_commit_approval.rs`
- `workspace/word_context_probe/wctx_16_enko_target_commit_approval_cases.json`
- `workspace/word_context_probe/wctx_16_enko_target_commit_approval_matrix.json`
- `workspace/word_context_probe/wctx_16_enko_target_commit_approval_summary.json`
- `workspace/word_context_probe/wctx_16_enko_target_commit_approval_sample_receipt.json`
- `workspace/word_context_probe/wctx_16_static_validation.json`
- `acceptance_reports/16AI-QW-38G-R6A-WCTX-16_enko_subtitle_target_update_candidate_manual_commit_approval_no_apply_seal.md`

## Modified files
- `crates/ash_core/src/lib.rs`

## Current default line
WCTX-15 produced `BlockedNoCandidate` for all 24 default cases. WCTX-16 therefore seals all 24 cases as `NoUpdateCandidate`, with no single-cue commit gate opened.

## Summary
```json
{
  "patch_id": "16AI-QW-38G-R6A-WCTX-16",
  "domain_ssot": "en_to_ko_translation_subtitle_machine",
  "total_cases": 24,
  "pass_cases": 24,
  "fail_cases": 0,
  "deterministic_failures": 0,
  "risk_failures": 0,
  "pending_count": 0,
  "approved_for_single_cue_commit_count": 0,
  "rejected_count": 0,
  "needs_revision_count": 0,
  "no_update_candidate_count": 24,
  "approval_valid_count": 24,
  "single_cue_commit_gate_open_count": 0,
  "immediate_apply_gate_open_count": 0,
  "runtime_apply_gate_open_count": 0,
  "no_candidate_commit_approved_count": 0,
  "invalid_candidate_commit_approved_count": 0,
  "auto_approved_count": 0,
  "operator_approval_missing_count": 0,
  "checklist_incomplete_count": 0,
  "target_text_mutation_count": 0,
  "target_subtitle_commit_count": 0,
  "runtime_default_apply_count": 0,
  "rerank_applied_count": 0,
  "decode_executed_in_commit_approval_count": 0,
  "generation_executed_in_commit_approval_count": 0,
  "model_forward_executed_in_commit_approval_count": 0,
  "sampling_executed_in_commit_approval_count": 0
}
```

## Verification
Static artifacts were generated successfully. Rust compilation was not executed because this container does not provide `cargo`/`rustc`.
