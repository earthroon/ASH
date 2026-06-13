# ASH-40 Plasticity Promotion Gate / Runtime Re-entry

## Status
PASS_PLASTICITY_PROMOTION_GATE_RUNTIME_REENTRY

## Sealed
- AshPlasticityPromotionGateMode
- AshPlasticityPromotionDecision
- AshPlasticityRuntimeReentryStatus
- AshPlasticityPromotionBlockerKind
- AshPlasticityPromotionBlocker
- AshRuntimeAdapterPointerSnapshot
- AshPlasticityRuntimeReentryMapping
- AshPlasticityRuntimeReentryCandidate
- AshPlasticityReentryLineageEvent
- AshPlasticityAdapterRollbackLineageCandidate
- AshPlasticityPromotionGateConfig
- AshPlasticityPromotionGateReport
- promotion gate validation
- runtime re-entry candidate generation
- rollback snapshot candidate generation
- re-entry lineage candidate generation

## Policy
- ASH-40 does not run SFT
- ASH-40 does not export JSONL
- ASH-40 does not mutate adapter registry
- ASH-40 does not change current pointer
- ASH-40 does not auto-apply runtime routing
- Re-entry candidate requires explicit apply
- runtime_apply_started must remain false
- Rollback snapshot is required by default
- Replay/smoke/perf/telemetry blockers prevent promotion
- No Python validator

## Boundary
ash_core computes promotion gate and re-entry candidates.
orchestrator_local reports gate evidence.
artifact_store preserves optional re-entry snapshots.
ASH-43 applies event tag runtime router integration later.
