# ASH-16 Bake Report

## Commit
ASH-16 — Weighted LoRA Synapse Graph / Delta-K Priority Router

## Baked from
- SSOT input zip: `ash_pass3_ASH-15_streaming_telemetry_final_output_merge_baked.zip`
- Patch contract: ASH-16 weighted LoRA synapse graph / Delta-K priority router spec

## Files changed
- `crates/ash_core/src/adapter_synapse.rs`
- `crates/ash_core/src/weighted_synapse_router.rs`
- `crates/ash_core/src/runtime_router.rs`
- `crates/ash_core/src/lib.rs`
- `crates/ash_core/tests/ash_16_weighted_synapse_router.rs`
- `crates/orchestrator_local/src/ash_16_synapse_route_report.rs`
- `crates/orchestrator_local/src/bin/ash_16_weighted_synapse_audit.rs`
- `crates/orchestrator_local/src/lib.rs`
- `crates/orchestrator_local/tests/ash_16_synapse_route_report.rs`
- `acceptance_reports/ASH-16_weighted_lora_synapse_graph_delta_k_router.md`
- `bake_artifacts/ASH-16_BAKE_REPORT.md`
- `bake_artifacts/ASH-16_STATIC_AUDIT_RESULT.md`

## Sealed behavior
- Adapter registry now supports `edges` with serde default for legacy registry compatibility.
- Weighted route formula uses existing `adapter.runtime_scale` plus edge runtime weight, Delta-K factor, and ranker hint factor.
- Delta-K priority factor is range-gated and deterministic.
- Ranker system is not reimplemented; score hints/snapshot ids are consumed as input.
- Inhibitory edges record their effect explicitly in candidate traces.
- Base-only explicit route bypasses the graph and returns an empty selected adapter set.
- Missing adapter ids and overweight routes reject instead of auto-healing or clamping.

## Validation note
The current execution container does not provide `cargo`/`rustc`, so Rust compile/test execution could not be run here. Static file-level validation was run by script and recorded in `ASH-16_STATIC_AUDIT_RESULT.md`. Run the Rust-native commands in the project environment for final compile confirmation.
