# ASH-22 Bake Report

## Commit
ASH-22 — Hard Negative Replay Integration for Synapse Suppression

## SSOT
Input SSOT: ASH-21 baked tree.
New evidence SSOT: AshHardNegativeReplayBuffer / AshHardNegativeReplayReport.

## Files Added
- crates/ash_core/src/hard_negative_replay.rs
- crates/ash_core/src/synapse_suppression.rs
- crates/orchestrator_local/src/ash_22_hard_negative_replay_report.rs
- crates/orchestrator_local/src/bin/ash_22_hard_negative_replay_audit.rs
- crates/ash_core/tests/ash_22_hard_negative_replay.rs
- crates/ash_core/tests/ash_22_synapse_suppression.rs
- crates/orchestrator_local/tests/ash_22_hard_negative_replay_report.rs
- acceptance_reports/ASH-22_hard_negative_replay_synapse_suppression.md
- bake_artifacts/ASH-22_STATIC_AUDIT_RESULT.md

## Files Modified
- crates/ash_core/src/lib.rs
- crates/orchestrator_local/src/lib.rs

## Static Notes
- No registry mutation path was added.
- No current pointer mutation path was added.
- Suppression candidates keep requires_explicit_apply=true.
- Hebbian proposal bridge keeps applied=false.
- No Python validator was added.

## Runtime Verification
The current container does not provide cargo/rustc, so Rust-native tests were not executed here.
Run:

```bash
cargo test -p ash_core ash_22_hard_negative_replay
cargo test -p ash_core ash_22_synapse_suppression
cargo test -p orchestrator_local ash_22_hard_negative_replay_report
cargo run -p orchestrator_local --bin ash_22_hard_negative_replay_audit
```
