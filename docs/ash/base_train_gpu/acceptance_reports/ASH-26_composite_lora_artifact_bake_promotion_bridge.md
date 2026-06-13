# ASH-26 Composite LoRA Artifact Bake / Promotion Bridge

## Status
PASS_COMPOSITE_LORA_ARTIFACT_BAKE_PROMOTION_BRIDGE

## Sealed
- AshCompositeArtifactBakeMode
- AshCompositeBakeExecutionStatus
- AshCompositeTensorMergePolicy
- AshLoraTensorKeyPair
- AshTensorBakeCompatibilityReport
- AshCompositeModuleBakeResult
- AshCompositeLoraBakedArtifact
- AshCompositeArtifactBakeConfig
- AshCompositeLoraBakeReport
- AshCompositeArtifactPromotionBridge
- AshCompositeBakeQuarantineReport
- dry-run bake validation
- staged composite artifact bake contract
- concatenated-rank LoRA merge policy trace
- staged manifest emission
- checksum calculation
- promotion bridge candidate

## Policy
- ASH-26 may create staged artifact payloads and manifests.
- ASH-26 does not change current runtime pointer.
- ASH-26 does not train LoRA.
- ASH-26 does not mutate base checkpoint.
- RuntimeStackOnlyPlan cannot emit safetensors.
- Missing tensor keys are blockers.
- Shape mismatch is a blocker.
- Checksums must be real after bake and cannot remain ASH-25 placeholders.
- Promotion bridge requires smoke test and manual promotion.
- No Python validator.

## Boundary
ash_core defines bake/bridge contracts and staged bake helpers.
orchestrator_local runs audit/report.
artifact_store preserves staged artifact outputs.
runtime consumes only after later smoke/promotion gate.
