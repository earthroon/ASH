# ASH-25 Composite LoRA Artifact Planner

## Status
PASS_COMPOSITE_LORA_ARTIFACT_PLANNER

## Sealed
- AshCompositeArtifactPlanningMode
- AshCompositeArtifactStrategy
- AshAdapterArtifactSourceKind
- AshCompositeAdapterArtifactDescriptor
- AshTargetModuleCompatibilityReport
- AshBaseCompatibilityReport
- AshLoraTensorCompatibilityReport
- AshCompositeBakeOperationKind
- AshCompositeBakeOperationPlan
- AshCompositeLoraArtifactManifestCandidate
- AshCompositeLoraArtifactPlan
- AshCompositeArtifactPlanningReport
- AshCompositeArtifactPlannerConfig
- AshAdapterArtifactManifestInput
- base checkpoint compatibility validation
- target module compatibility validation
- rank/dtype compatibility report
- bake operation planning
- manifest candidate planning

## Policy
- ASH-25 does not merge tensors.
- ASH-25 does not create safetensors.
- Composite profile is the planning input.
- ASH-23 profile weights become bake weights.
- ASH-24 phase confidence can block risky bake plans.
- ASH-22 hard negative evidence can block artifact plans.
- RuntimeStackOnlyPlan is not an artifact merge.
- Artifact checksum remains a placeholder until ASH-26.
- No Python validator.

## Boundary
ash_core computes artifact plan.
runtime does not execute artifact bake.
orchestrator_local reports planning evidence.
artifact_store preserves plan snapshots.
