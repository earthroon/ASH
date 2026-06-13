# ASH-44 Plasticity Rollback / Adapter Pointer Lineage

## Status
PASS_PLASTICITY_ROLLBACK_ADAPTER_POINTER_LINEAGE

## Sealed
- AshPlasticityRollbackMode
- AshAdapterPointerLineageEventKind
- AshPlasticityRollbackDecision
- AshPlasticityRollbackBlockerKind
- AshAdapterPointerLineageEvent
- AshAdapterPointerLineageRecord
- AshAdapterPointerLineageLedger
- AshPlasticityRollbackBlocker
- AshPlasticityRollbackCandidate
- AshPlasticityRollbackPreflightReport
- AshPlasticityRollbackLineageReport
- rollback candidate generation
- adapter pointer lineage ledger
- rollback preflight validation
- explicit rollback guard

## Policy
- ASH-44 does not execute rollback
- ASH-44 does not mutate adapter registry
- ASH-44 does not change current pointer
- ASH-44 does not hot reload runtime
- Rollback requires explicit rollback
- rollback_started must remain false
- Previous pointer snapshot is required by default
- Lineage is append-only candidate
- No Python validator

## Boundary
ash_core computes rollback lineage and preflight.
orchestrator_local reports rollback evidence.
artifact_store preserves optional lineage snapshots.
ASH-48 performs explicit apply/rollback later.
