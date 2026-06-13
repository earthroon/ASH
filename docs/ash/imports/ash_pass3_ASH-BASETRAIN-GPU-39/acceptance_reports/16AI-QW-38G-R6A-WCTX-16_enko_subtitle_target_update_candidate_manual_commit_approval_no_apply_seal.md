# 16AI-QW-38G-R6A-WCTX-16 Acceptance Report

## Seal
EN-KO Subtitle Target Update Candidate Manual Commit Approval / No-Apply Seal

## Domain SSOT
`en_to_ko_translation_subtitle_machine`

## Static Result
`PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE`

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

## Confirmed invariants
- NoUpdateCandidate receipts are produced for the current default WCTX-15 line.
- No automatic approval is created.
- `single_cue_commit_gate_open_count = 0`.
- `immediate_apply_gate_open_count = 0`.
- `target_text_mutation_count = 0`.
- `target_subtitle_commit_count = 0`.
- `runtime_default_apply_count = 0`.
- No decode/generation/model-forward/sampling is executed in commit approval.

## Toolchain note
The current container does not expose `cargo`/`rustc`; runtime compilation must be reproduced locally with:

```bash
cargo run -p ash_core --bin ash_word_context_target_commit_approval
```
