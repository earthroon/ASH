# ASH-29 Phase Hint Confidence Decay / Registry Aging

## Status
PASS_PHASE_HINT_CONFIDENCE_DECAY_REGISTRY_AGING

## Sealed
- AshPhaseHintAgingMode
- AshPhaseHintAgingDecision
- AshPhaseHintAgingConfig
- AshPhaseHintAgingEvidenceSummary
- AshPhaseHintAgingRecord
- AshPhaseHintStaleQuarantineRecord
- AshAgedPhaseHintRegistryCandidate
- AshPhaseHintAgingReport
- confidence half-life decay
- amplitude slower decay
- smoke-pass preservation
- hard-negative accelerated decay
- replay-block accelerated decay
- stale quarantine
- candidate registry generation

## Policy
- Aging does not mutate source registry
- Aging does not alter phase_rad
- Confidence and amplitude may decay
- Quarantine is exclusion, not deletion
- Stale hints are excluded from phase input when configured
- Smoke pass slows decay but does not freeze it
- Hard negatives accelerate decay
- No phase hint is fabricated without evidence
- No Python validator

## Boundary
ash_core computes aging and candidate registry.
runtime emits smoke/telemetry evidence.
orchestrator_local reports aging evidence.
artifact_store preserves registry aging snapshots.
