# ASH-21 Bake Report

## Commit
ASH-21 — Composite Adapter Promotion / Rollback Gate

## SSOT
Input archive: ASH-20 phase-field synapse penalty / imaginary action baked tree.

## Implemented files
- `crates/ash_core/src/composite_promotion_gate.rs`
- `crates/ash_core/src/composite_rollback_gate.rs`
- `crates/orchestrator_local/src/ash_21_composite_promotion_report.rs`
- `crates/orchestrator_local/src/bin/ash_21_composite_promotion_rollback_audit.rs`
- `crates/ash_core/tests/ash_21_composite_promotion_gate.rs`
- `crates/ash_core/tests/ash_21_composite_rollback_gate.rs`
- `crates/orchestrator_local/tests/ash_21_composite_promotion_report.rs`

## Modified files
- `crates/ash_core/src/lib.rs`
- `crates/orchestrator_local/src/lib.rs`

## Sealed behavior
- Composite profile creation from ASH-19 SoftEnsemble route.
- ASH-20 phase route evidence check before promotion.
- Base-only route promotion rejection.
- PromoteToCurrent previous stable pointer requirement.
- Rollback only to previous stable pointer.
- No fallback pointer invention.
- No LoRA tensor merge.
- No Python validator.

## Verification note
This environment does not provide `cargo` or `rustc`; Rust-native commands must be run in the project environment.
