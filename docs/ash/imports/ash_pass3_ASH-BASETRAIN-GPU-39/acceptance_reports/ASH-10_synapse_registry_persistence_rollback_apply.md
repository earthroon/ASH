# ASH-10 Synapse Registry Persistence / Rollback Apply

## Status
PASS_STATIC / PASS_ASH_SYNAPSE_REGISTRY_PERSISTENCE_ROLLBACK_APPLY

## Sealed
- synapse registry snapshot persistence
- AdapterSynapseStatusPatch apply
- current_adapter pointer
- promoted_adapter pointer
- rollback_adapter pointer
- rollback apply report
- orchestrator persistence bridge

## Pointer policy
- Promote updates current/promoted and preserves previous current as rollback
- Reject does not update current/promoted
- PendingManualReview does not update current/promoted
- RollbackRequired restores rollback target or records explicit base-only requirement

## Guards
- no promotion without decision
- rejected adapter cannot become current/promoted
- rollback-required adapter cannot remain current
- missing rollback target must not silently fallback
- from_status mismatch fails
- manifest/model paths required for current/promoted pointers
- Python validator forbidden

## Boundary
ash_core decides.
artifact_store persists.
orchestrator_local coordinates.
runtime later consumes current pointer.
