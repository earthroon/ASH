# ASH-23 Runtime Ensemble Weight Telemetry / Attached LoRA Weight Header

## Status
PASS_ATTACHED_LORA_WEIGHT_TELEMETRY

## Sealed
- RuntimeAshLoraWeightSource
- RuntimeAshAttachedLoraWeight
- RuntimeAshAttachmentWeightTelemetry
- attached_lora_weights
- ensemble_route_id
- composite_profile_id
- weight_source
- weight_missing
- weight_mismatch_detected
- streaming telemetry header weight extension
- final orchestrator telemetry weight merge

## Policy
- attached_lora_ids are preserved.
- attached_lora_weights are added, not renamed.
- SoftEnsemble weights can become runtime telemetry.
- CompositeProfile weights can become runtime telemetry.
- Missing weights are not silently defaulted.
- BaseOnlyExplicit requires empty weights.
- AdapterEnabled requires id/weight set match at streaming/final boundary.
- Unknown weight source cannot PASS weight-aware telemetry validation.
- No Python validator is added.

## Boundary
ash_core provides route/profile weight evidence.
runtime emits weight telemetry.
orchestrator_local merges weight telemetry into final output.
artifact_store may preserve optional runtime attachment snapshots.
