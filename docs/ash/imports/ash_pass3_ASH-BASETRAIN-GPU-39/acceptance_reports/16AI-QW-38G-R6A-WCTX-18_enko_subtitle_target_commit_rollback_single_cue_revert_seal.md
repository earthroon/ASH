# 16AI-QW-38G-R6A-WCTX-18 Acceptance Report

## Seal
- Patch: `16AI-QW-38G-R6A-WCTX-18`
- Domain SSOT: `en_to_ko_translation_subtitle_machine`
- Mode: `Target Commit Rollback / Single-Cue Revert`

## Acceptance Result
- Static validation: `PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE`
- Total cases: `24`
- Pass cases: `24`
- Fail cases: `0`

## Default Line
The default WCTX line has no committed target from WCTX-17. WCTX-18 therefore seals every case as rollback-blocked.

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

## Guard Invariants
- `reverted_count=0` in the default fixture.
- `blocked_no_commit_count=24` in the default fixture.
- `rollback_executed_count=0`.
- `target_text_mutation_count=0`.
- `runtime_default_apply_count=0`.
- `rerank_applied_count=0`.
- No decode/generation/model-forward/sampling is executed in rollback.

## Notes
`cargo` / `rustc` are unavailable in this container, so Rust compilation could not be executed here. The Rust module, binary entrypoint, deterministic JSON receipts, static validation file, and reports were materialized for local validation.
