# ASH-32 Bake Report

## Commit
ASH-32 — Replay-to-Hebbian Feedback Bridge

## SSOT
Input SSOT: ASH-31 baked zip.

## Added
- crates/ash_core/src/replay_hebbian_feedback.rs
- crates/ash_core/src/replay_feedback_proposals.rs
- crates/orchestrator_local/src/ash_32_replay_hebbian_feedback_report.rs
- crates/orchestrator_local/src/bin/ash_32_replay_hebbian_feedback_audit.rs
- crates/ash_core/tests/ash_32_replay_hebbian_feedback.rs
- crates/ash_core/tests/ash_32_replay_feedback_proposals.rs
- crates/orchestrator_local/tests/ash_32_replay_hebbian_feedback_report.rs
- acceptance_reports/ASH-32_replay_to_hebbian_feedback_bridge.md

## Modified
- crates/ash_core/src/lib.rs
- crates/orchestrator_local/src/lib.rs

## Policy Seals
- replay Fail / BlockPromotion / telemetry regression results are converted into feedback events.
- feedback events can produce ASH-18-compatible Hebbian proposal sets.
- all replay-derived proposals keep requires_explicit_apply=true and applied=false.
- ledger patch candidates are appendable evidence only and never mutate the source ledger.
- registry/current pointer mutation remains forbidden.
- Python validator remains absent.

## Runtime Notes
The execution container does not provide cargo/rustc, so Rust compilation was not executed here. Static audit and zip integrity checks were performed.
