# 16AI-QW-38G-R6A-WCTX-MOCK-07 Acceptance Report

## Patch
`16AI-QW-38G-R6A-WCTX-MOCK-07`

## Title
EN-KO Subtitle Mock Single-Cue Commit Rollback Replay / Revert Receipt Seal

## Domain SSOT
`en_to_ko_translation_subtitle_machine`

## Acceptance Result
`PASS_STATIC_RUST_TOOLCHAIN_UNAVAILABLE`

## Verified Static Invariants

```text
[PASS] MOCK-06 SingleCueCommitReplayed receipts are accepted as source inputs
[PASS] WCTX-18 rollback logic is reused through build_enko_single_cue_target_rollback_receipt
[PASS] Reverted rollback receipts are expected for all 12 mock commit cases
[PASS] rollback_patch_created=true for all 12 cases
[PASS] rollback_executed_in_receipt=true for all 12 cases
[PASS] target_restored_to_original_in_receipt=true for all 12 cases
[PASS] target_text_mutated_in_receipt=true is allowed inside rollback receipts
[PASS] rollback_snapshot_used=true for all 12 cases
[PASS] rollback_hash_mismatch=false for all 12 cases
[PASS] production_target_text_mutated=false
[PASS] production_subtitle_store_mutated=false
[PASS] runtime_default_apply=false
[PASS] runtime_apply_gate_open=false
[PASS] runtime_apply_executed=false
[PASS] rerank_applied=false
```

## Matrix Summary

```json
{
  "total_cases": 12,
  "pass_cases": 12,
  "fail_cases": 0,
  "reverted_count": 12,
  "rollback_patch_created_count": 12,
  "target_restored_to_original_in_receipt_count": 12,
  "target_text_mutated_in_receipt_count": 12,
  "rollback_snapshot_used_count": 12,
  "rollback_hash_mismatch_count": 0,
  "production_subtitle_store_mutation_count": 0,
  "runtime_default_apply_count": 0
}
```

## Toolchain Note

The container does not expose `cargo`/`rustc`; therefore this bake includes Rust source materialization and static JSON validation, but not an executed local Rust compile.
