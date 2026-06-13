# 16AI-QW-38G-R6A-DECODE-08 Bake Report

## Summary

- Added rollback-first candidate recovery policy.
- Added candidate exhaustion snapshots, rollback anchors, strict retry profiles, retry requests, and deterministic recovery receipts.
- Extended DECODE-04 risk snapshot with recovery result slots.
- Preserved production_default_apply=false.
- Blocked global top1 recovery by default.

## Static Seal

status: PASS_STATIC_ROLLBACK_FIRST_RECOVERY_CONTRACT
receipt_count: 5
rollback_retry_requested_count: 2
top1_recovery_blocked_count: 1
safe_eos_recommended_count: 1
step_integrity_skip_count: 1
rollback_executed_count: 0
model_forward_executed_count: 0
sampling_executed_count: 0

## Compile note

Rust toolchain was unavailable in the bake environment, so this patch is sealed as a static contract rather than a compiled runtime pass.
