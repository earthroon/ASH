# 16AI-QW-38G-R6A-KV-ROLLBACK-01 Report

## Patch
Forked Replay Restore Verification Seal

## SSOT
KVSnapshotRef + TokenLedger + PositionState + ForkedReplayReceipt.

## Implemented
- Added `crates/model_core/src/kv_rollback01_forked_replay.rs`.
- Added `KvRollback01Mode`: Off / PlanOnly / ForkedReplayProbe / StrictForkedReplayProbe.
- Added replay input semantics and fork capability structures.
- Added forked replay result, verification grade, main-state fingerprint, summary aggregation.
- Added `KvRollbackForkedReplayRuntime` and `KvRollbackForkedReplayState` traits for backend wiring.
- Connected `sampler_parity::append_receipt()` to the KV-ROLLBACK-01 observe hook.
- Preserved `behavior_change=false` and `probe_only=true` contracts.
- Added workspace receipt schema, placeholder JSONL, summary, probe prompts, and acceptance report.

## Runtime status
Static bake only. Cargo/rustc were not available in this container, so cargo check, unit tests, runtime smoke, and forked replay were not executed.

## Next
`16AI-QW-38G-R6A-SALAD-03B — Rollback Controlled Execute / KV-Restored Safe Resample Seal` after forked replay receipt proves `restore_verified_for_salad03b=true`.
