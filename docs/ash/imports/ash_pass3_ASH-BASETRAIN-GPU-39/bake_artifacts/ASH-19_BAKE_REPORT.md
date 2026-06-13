# ASH-19 Bake Report

## Commit
ASH-19 — Explicit Synapse Proposal Apply Gate / Soft Ensemble Composer

## Status
BAKED_STATIC

## Source SSOT
ash_pass3_ASH-18_coactivation_ledger_hebbian_path_cost_update_baked.zip

## Added
- crates/ash_core/src/synapse_proposal_apply_gate.rs
- crates/ash_core/src/soft_ensemble_composer.rs
- crates/orchestrator_local/src/ash_19_synapse_apply_report.rs
- crates/orchestrator_local/src/bin/ash_19_synapse_apply_soft_ensemble_audit.rs
- crates/ash_core/tests/ash_19_synapse_proposal_apply_gate.rs
- crates/ash_core/tests/ash_19_soft_ensemble_composer.rs
- crates/orchestrator_local/tests/ash_19_synapse_apply_report.rs
- acceptance_reports/ASH-19_synapse_proposal_apply_gate_soft_ensemble.md
- bake_artifacts/ASH-19_STATIC_AUDIT_RESULT.md

## Modified
- crates/ash_core/src/lib.rs
- crates/orchestrator_local/src/lib.rs

## Sealed behavior
- proposal apply gate requires explicit apply
- proposal_set.applied=true is rejected
- DryRun never emits patched registry
- ApplyToClone patches cloned registry only
- original registry is kept unchanged
- old_weight mismatch is rejected
- inhibitory edge creation validates adapters, self-edge, duplicate edge, confidence and fail evidence
- path instability proposals are skipped when no cost store exists
- SoftEnsemble sums ASH-17 path probability mass by adapter
- SoftEnsemble normalizes total ensemble weight without individual silent clamp
- base-only ensemble remains empty

## Not run
Rust compile/tests were not run because cargo/rustc are unavailable in the container.

## Intended verification
```bash
cargo test -p ash_core ash_19_synapse_proposal_apply_gate
cargo test -p ash_core ash_19_soft_ensemble_composer
cargo test -p orchestrator_local ash_19_synapse_apply_report
cargo run -p orchestrator_local --bin ash_19_synapse_apply_soft_ensemble_audit
```
