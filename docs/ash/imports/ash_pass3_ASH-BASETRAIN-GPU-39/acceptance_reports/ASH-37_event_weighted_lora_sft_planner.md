# ASH-37 Event-Weighted LoRA SFT Planner

## Status
PASS_EVENT_WEIGHTED_LORA_SFT_PLANNER

## Sealed
- AshEventWeightedSftPlannerMode
- AshSftObjectiveKind
- AshSftPlannedSampleRole
- AshSftDatasetMaterializationKind
- AshSftTargetModulePolicy
- AshSftPlannedSampleRef
- AshSftSampleSelectionPolicy
- AshSftLossWeightPolicy
- AshAdapterSftTargetPlan
- AshSftDatasetMaterializationRequirement
- AshSftTrainingRunManifestCandidate
- AshEventWeightedLoraSftPlan
- AshEventWeightedSftPlanningReport
- curriculum to adapter SFT plan mapping
- sample selection policy
- loss weight policy
- dataset materialization requirement
- training manifest candidate

## Policy
- ASH-37 does not export JSONL.
- ASH-37 does not run SFT.
- ASH-37 does not mutate ASH-36 curriculum.
- ASH-37 does not mutate ASH-35 sample ledger.
- MetadataOnly samples are SignalOnly.
- SignalOnly samples never become training text.
- Holdout samples are not used for training.
- Training manifest candidates keep `requires_explicit_training=true`.
- Training manifest candidates keep `training_started=false`.
- No Python validator.

## Boundary
ash_core computes event-weighted SFT plan candidates.
orchestrator_local reports planning evidence.
artifact_store may preserve optional plan snapshots.
ASH-41 or later materializes datasets.
ASH-42 or later starts training behind an explicit gate.
