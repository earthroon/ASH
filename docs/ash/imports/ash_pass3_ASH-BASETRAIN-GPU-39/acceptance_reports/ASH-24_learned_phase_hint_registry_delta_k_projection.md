# ASH-24 Learned Phase Hint Registry / Delta-K Phase Projection

## Status
PASS_LEARNED_PHASE_HINT_REGISTRY_DELTA_K_PROJECTION

## Sealed
- AshPhaseProjectionMethod
- AshPhaseHintEvidenceKind
- AshPhaseHintEvidence
- AshLearnedAdapterPhaseHint
- AshLearnedEdgePhaseHint
- AshPhaseHintRegistry
- AshPhaseProjectionConfig
- AshPhaseHintProjectionReport
- Delta-K to phase projection
- circular phase mean
- coactivation evidence extraction
- hard negative repulsion evidence
- weight telemetry amplitude evidence
- phase registry to ASH-20 input conversion

## Policy
- Phase hints are learned evidence, not tensor mutation.
- Phase hint registry is separate from adapter registry.
- Candidate registry does not mutate previous registry.
- Delta-K projection records clamp warnings.
- Hard negatives reduce confidence or create repulsion evidence.
- ASH-23 weights can influence amplitude through an ash_core evidence input mirror, avoiding runtime -> ash_core dependency inversion.
- Missing evidence returns NOOP, not fabricated high-confidence hints.
- No Python validator.

## Boundary
ash_core computes phase hint registry.
runtime emits weight telemetry only.
orchestrator_local reports projection evidence.
artifact_store preserves phase hint snapshots.
