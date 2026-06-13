# ASH-38 Adapter Specialization / Event Tag Routing

## Status
PASS_ADAPTER_SPECIALIZATION_EVENT_TAG_ROUTING

## Sealed
- AshAdapterSpecializationMode
- AshAdapterEventTagKind
- AshAdapterEventRoutingAction
- AshAdapterSpecializationConfidenceClass
- AshEventTagAdapterAffinity
- AshEventTagAdapterAvoidance
- AshAdapterActivationPolicy
- AshAdapterEventSpecializationRecord
- AshAdapterEventSpecializationRegistry
- AshEventTagRoutingPolicy
- AshAdapterSpecializationPlanningReport
- SFT objective to event tag mapping
- adapter affinity calculation
- adapter avoidance calculation
- conflict detection
- routing policy candidate generation

## Policy
- ASH-38 does not run SFT.
- ASH-38 does not export JSONL.
- ASH-38 does not mutate adapter registry.
- ASH-38 does not change current pointer.
- ASH-38 does not auto-apply runtime routing.
- MetadataOnly signal can influence routing hints only.
- Conflicts require manual review.
- Runtime smoke may be required before routing readiness.
- No Python validator.

## Boundary
ash_core computes specialization registry candidates.
orchestrator_local reports specialization evidence.
artifact_store preserves optional routing policy snapshots.
ASH-39 evaluates outcome after SFT/runtime re-entry.
