# ASH-22 Hard Negative Replay Integration for Synapse Suppression

## Status
PASS_HARD_NEGATIVE_REPLAY_SYNAPSE_SUPPRESSION

## Sealed
- AshHardNegativeSeverity
- AshHardNegativeSource
- AshHardNegativeKind
- AshHardNegativeReplayCase
- AshHardNegativeReplayBuffer
- AshSynapseSuppressionTargetKind
- AshSynapseSuppressionActionKind
- AshSynapseSuppressionCandidate
- AshPromotionBlockEvidence
- AshRollbackTriggerEvidence
- AshHardNegativeReplayReport
- hard negative fingerprint generation
- replay buffer dedupe by fingerprint
- severity-aware replay buffer eviction
- suppression candidate generation
- Hebbian proposal bridge
- promotion block evidence
- rollback trigger evidence

## Policy
- Hard negative replay is evidence, not direct mutation.
- Suppression candidates require explicit apply.
- Registry is not mutated by ASH-22.
- Current pointer is not changed by ASH-22.
- Rollback is not automatic.
- Fingerprints ignore request_id and event_id.
- Silent fallback is Critical.
- Pass events do not become hard negatives.
- Base-only policy reject is not hard negative by default.
- Hebbian proposal bridge preserves applied=false.
- No Python validator.

## Boundary
ash_core computes replay and suppression evidence.
runtime emits inference telemetry.
orchestrator_local reports audit evidence.
artifact_store preserves replay buffer snapshots.
