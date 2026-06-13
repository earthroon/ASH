# 16AI-QW-38G-R6A-WCTX-18 Bake Report

## Added
- `crates/ash_core/src/word_context_target_rollback.rs`
- `crates/ash_core/src/bin/ash_word_context_target_rollback.rs`
- `workspace/word_context_probe/wctx_18_enko_target_rollback_cases.json`
- `workspace/word_context_probe/wctx_18_enko_target_rollback_matrix.json`
- `workspace/word_context_probe/wctx_18_enko_target_rollback_summary.json`
- `workspace/word_context_probe/wctx_18_enko_target_rollback_sample_receipt.json`
- `workspace/word_context_probe/wctx_18_static_validation.json`

## Modified
- `crates/ash_core/src/lib.rs`

## Core APIs
- `default_enko_single_cue_target_rollback_commit_receipts()`
- `build_enko_single_cue_target_rollback_receipt(...)`
- `run_enko_single_cue_target_rollback_matrix(...)`

## Default Matrix
```json
{
  "patch_id": "16AI-QW-38G-R6A-WCTX-18",
  "domain_ssot": "en_to_ko_translation_subtitle_machine",
  "total_cases": 24,
  "pass_cases": 24,
  "fail_cases": 0,
  "deterministic_failures": 0,
  "risk_failures": 0,
  "reverted_count": 0,
  "blocked_no_commit_count": 24,
  "blocked_commit_not_applied_count": 0,
  "blocked_missing_commit_patch_count": 0,
  "blocked_missing_rollback_snapshot_count": 0,
  "blocked_rollback_hash_mismatch_count": 0,
  "blocked_cue_boundary_violation_count": 0,
  "rollback_patch_created_count": 0,
  "rollback_executed_count": 0,
  "target_restored_to_original_count": 0,
  "target_text_mutation_count": 0,
  "multiple_cue_mutation_detected_count": 0,
  "rollback_missing_count": 0,
  "rollback_hash_mismatch_count": 0,
  "runtime_default_apply_count": 0,
  "runtime_apply_gate_open_count": 0,
  "rerank_applied_count": 0,
  "decode_executed_in_rollback_count": 0,
  "generation_executed_in_rollback_count": 0,
  "model_forward_executed_in_rollback_count": 0,
  "sampling_executed_in_rollback_count": 0
}
```

## Default SSOT Result
- WCTX-17 default line: `BlockedNoUpdateCandidate`
- WCTX-18 default line: `BlockedNoCommit`
- No rollback patch is created.
- No target text mutation is performed.
- Runtime default apply remains disabled.

## Local Validation Command
```bash
cargo run -p ash_core --bin ash_word_context_target_rollback
```

## Validation Limitation
`cargo` / `rustc` are unavailable in this container, so this bake is sealed as `PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE`.
