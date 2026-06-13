# ASH-40 Bake Report

## SSOT
Source: ASH-39 baked worktree.

## Implemented files
- crates/ash_core/src/plasticity_promotion_gate.rs
- crates/ash_core/src/plasticity_runtime_reentry.rs
- crates/ash_core/src/runtime_adapter_pointer_snapshot.rs
- crates/ash_core/src/plasticity_reentry_lineage.rs
- crates/orchestrator_local/src/ash_40_plasticity_promotion_gate_report.rs
- crates/orchestrator_local/src/bin/ash_40_plasticity_promotion_gate_audit.rs
- crates/ash_core/tests/ash_40_plasticity_promotion_gate.rs
- crates/ash_core/tests/ash_40_plasticity_runtime_reentry.rs
- crates/ash_core/tests/ash_40_runtime_adapter_pointer_snapshot.rs
- crates/ash_core/tests/ash_40_plasticity_reentry_lineage.rs
- crates/orchestrator_local/tests/ash_40_plasticity_promotion_gate_report.rs
- acceptance_reports/ASH-40_plasticity_promotion_gate_runtime_reentry.md

## Sealed behavior
- ASH-39 promotion evidence is validated before runtime re-entry candidate generation.
- Replay/smoke/perf/telemetry/event routing failures generate explicit blockers.
- Routing policy and specialization records are required by default.
- Rollback snapshot is required by default for ReadyForExplicitApply.
- Re-entry candidates preserve requires_explicit_apply=true and runtime_apply_started=false.
- ASH-40 creates candidates and lineage evidence only; it does not mutate runtime or registry state.

## Runtime boundary
No runtime attach, hot reload, current pointer update, adapter registry mutation, SFT execution, or JSONL export is performed.

## Verification
Static audit and zip integrity checks were performed in this environment. Rust cargo/rustc/rustfmt are unavailable in the container, so compile-time verification must be run in the project Rust environment.
