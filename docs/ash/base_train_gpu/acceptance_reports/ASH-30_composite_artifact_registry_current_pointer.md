# ASH-30 Composite Artifact Registry / Current Pointer Integration

## Status
PASS_COMPOSITE_ARTIFACT_REGISTRY_CURRENT_POINTER_INTEGRATION

## Sealed
- AshCompositeArtifactRegistryIntegrationMode
- AshCompositeArtifactLifecycleStatus
- AshCompositeArtifactRegistryRecord
- AshCompositeArtifactRegistry
- AshCompositeArtifactCurrentPointer
- AshCompositePointerLineageEvent
- AshCompositeArtifactPointerLineage
- AshCompositeArtifactRegistryGateConfig
- AshCompositeArtifactRegistryIntegrationInput
- AshCompositeArtifactRegistryIntegrationReport
- registry record validation
- current pointer candidate generation
- previous stable pointer snapshot
- pointer lineage append
- replay block gate
- smoke/promotion-ready gate

## Policy
- Registry registration does not imply current activation.
- Current pointer changes only by explicit RegisterAndPromoteToCurrent gate.
- Previous stable pointer snapshot is required by default.
- Replay-blocked artifacts cannot become current.
- Smoke/promotion-ready evidence is required for current promotion.
- Attached LoRA weights must be available before current promotion.
- Source registry is not mutated in-place.
- Pointer lineage is append-only evidence.
- No Python validator.

## Boundary
ash_core computes registry and pointer candidates.
runtime consumes current pointer later.
orchestrator_local reports integration evidence.
artifact_store preserves registry and pointer snapshots.
