# ASH-20 Phase-Field Synapse Penalty / Imaginary Action Experiment

## Status
PASS_PHASE_FIELD_SYNAPSE_PENALTY_IMAGINARY_ACTION

## Sealed
- AshPhaseFieldMode
- AshPhaseHintSource
- AshAdapterPhaseHint
- AshEdgePhaseHint
- AshPhaseFieldSynapseInput
- AshPhaseFieldPathStep
- AshPhaseFieldPathTerm
- AshPhaseFieldSynapseRoutePlan
- AshPhaseFieldSoftEnsembleReport
- phase mismatch calculation
- phase coherence calculation
- imaginary action trace
- real-valued phase penalty
- ReportOnly mode
- AdjustRoute mode
- Disabled mode
- base-only bypass

## Policy
- ASH-20 does not mutate registry.
- ASH-20 does not mutate LoRA tensors.
- Complex probability is not used directly.
- Imaginary action is trace-only.
- Real-valued phase penalty is explicit.
- ReportOnly does not alter selected route.
- AdjustRoute records before/after selected paths.
- Missing phase hints are warning or rejection by config.
- Phase hints are supplied as experimental input; no silent phase generation.
- SoftEnsemble weights are not silently rewritten by phase-field reporting.
- No Python validator.

## Boundary
ash_core computes phase route penalties.
runtime executes selected attachments.
orchestrator_local reports phase evidence.
artifact_store preserves phase snapshots.

## Verification commands
```bash
cargo test -p ash_core ash_20_phase_field_synapse
cargo test -p orchestrator_local ash_20_phase_field_report
cargo run -p orchestrator_local --bin ash_20_phase_field_synapse_audit
```
