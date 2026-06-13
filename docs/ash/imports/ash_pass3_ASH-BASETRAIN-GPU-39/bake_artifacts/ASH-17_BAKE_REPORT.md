# ASH-17 Bake Report

## Commit
ASH-17 — Path Integral LoRA Synapse Router

## Input SSOT
ASH-16 baked source tree.

## Implemented files
- `crates/ash_core/src/path_integral_synapse_router.rs`
- `crates/ash_core/tests/ash_17_path_integral_synapse_router.rs`
- `crates/orchestrator_local/src/ash_17_path_integral_route_report.rs`
- `crates/orchestrator_local/src/bin/ash_17_path_integral_synapse_audit.rs`
- `crates/orchestrator_local/tests/ash_17_path_integral_synapse_report.rs`
- `acceptance_reports/ASH-17_path_integral_lora_synapse_router.md`

## Modified files
- `crates/ash_core/src/lib.rs`
- `crates/orchestrator_local/src/lib.rs`

## Sealed behavior
- deterministic beam path generation over ASH-16 weighted LoRA synapse graph
- action-cost calculation for edge cost, Delta-K mismatch, ranker loss, inhibitory penalty, conflict penalty, latency, and instability hooks
- softmin probability normalization
- BestPath route selection
- BaseOnlyExplicit bypass
- invalid ranker score rejection
- Conditional edge Delta-K range pruning
- no default stochastic sampling
- no missing adapter auto-generation
- no Python validator

## Runtime note
`cargo` / `rustc` were unavailable in this container, so Rust-native tests were not executed here. Static source audit was performed and recorded in `bake_artifacts/ASH-17_STATIC_AUDIT_RESULT.md`.
