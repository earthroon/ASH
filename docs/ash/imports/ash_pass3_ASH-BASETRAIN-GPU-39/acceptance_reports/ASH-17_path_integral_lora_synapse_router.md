# ASH-17 Path Integral LoRA Synapse Router

## Status
PASS_STATIC / PASS_PATH_INTEGRAL_LORA_SYNAPSE_ROUTER

## Sealed
- AshPathIntegralSelectionMode
- AshPathIntegralSynapseRouterInput
- AshSynapsePathStep
- AshSynapsePathCandidate
- AshPathIntegralSynapseRoutePlan
- deterministic beam path generation
- path action calculation
- softmin probability normalization
- BestPath selection
- base-only bypass
- ASH-16 graph reuse
- ASH-15 telemetry bridge preservation fields

## Policy
- ASH-16 graph is the input SSOT.
- LoRA route selection is path-action based.
- Random sampling is not enabled by default.
- BestPath is the default selection mode.
- SoftEnsemble is reserved for later commits.
- Delta-K mismatch contributes to action cost.
- Existing ranker is reused through hints/snapshots only.
- Inhibitory edges penalize full paths and leave inhibited traces.
- Missing adapters are surfaced, not auto-created.
- No silent clamp.
- No Python validator.

## Boundary
- ash_core decides path route.
- runtime executes selected attachments.
- orchestrator_local reports route evidence.
- artifact_store preserves registry and route snapshots.

## Validation commands
```bash
cargo test -p ash_core ash_17_path_integral_synapse_router
cargo test -p orchestrator_local ash_17_path_integral_synapse_report
cargo run -p orchestrator_local --bin ash_17_path_integral_synapse_audit
```

## Expected log
```txt
[ash_core][ASH-17] PASS_PATH_INTEGRAL_LORA_SYNAPSE_ROUTER
```
