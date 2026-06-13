# ASH-16 Weighted LoRA Synapse Graph / Delta-K Priority Router

## Status
PASS_STATIC / PASS_WEIGHTED_LORA_SYNAPSE_DELTA_K_ROUTER

## Sealed
- `AshAdapterSynapseEdgeKind`
- `AshAdapterSynapseEdge`
- `AshAdapterSynapseRegistry.edges`
- `AshRankerScoreHint`
- `AshWeightedSynapseRouterInput`
- `AshWeightedAdapterRouteCandidate`
- `AshWeightedSynapseRoutePlan`
- `validate_adapter_synapse_graph`
- `compute_delta_k_priority_factor`
- `build_weighted_synapse_route_plan`
- `validate_weighted_synapse_route_plan`
- orchestrator ASH-16 route report DTO
- Rust-native audit bin

## Policy
- LoRA composition is weight-based.
- Delta-K decides priority and conflict preference.
- Existing ranker is reused through score hints and snapshot ids.
- Existing adapter runtime scale is preserved as the base runtime weight.
- Inhibitory edges must leave explicit candidate/report traces.
- BaseOnlyExplicit bypasses the synapse graph.
- Missing adapter ids are surfaced, not auto-created.
- Overweight routes reject instead of silently clamping.
- Python validator is forbidden.

## Boundary
- `ash_core` owns graph typing, graph validation, and weighted route judgement.
- `runtime` remains the attachment/inference execution owner.
- `orchestrator_local` owns route report/audit output.
- `artifact_store` remains the correct persistence boundary for registry snapshots and evidence reports.

## Repro commands
```bash
cargo test -p ash_core ash_16_weighted_synapse_router
cargo test -p orchestrator_local ash_16_synapse_route_report
cargo run -p orchestrator_local --bin ash_16_weighted_synapse_audit
```

## Expected audit log
```txt
[ash_core][ASH-16] PASS_WEIGHTED_LORA_SYNAPSE_DELTA_K_ROUTER
```
