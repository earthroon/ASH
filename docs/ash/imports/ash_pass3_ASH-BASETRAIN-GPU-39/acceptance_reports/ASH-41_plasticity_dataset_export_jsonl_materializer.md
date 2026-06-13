# ASH-41 Plasticity Dataset Export / JSONL Materializer

## Status
PASS_PLASTICITY_DATASET_EXPORT_JSONL_MATERIALIZER

## Sealed
- AshPlasticityDatasetExportMode
- AshPlasticityJsonlFormatKind
- AshPlasticityDatasetSplitKind
- AshPlasticityJsonlRecord
- AshPlasticityDatasetManifest
- AshPlasticityDatasetArtifact
- AshPlasticityDatasetExportFailure
- AshPlasticityDatasetExportReport
- planned sample to JSONL record materialization
- train/holdout split protection
- metadata-only / signal-only exclusion
- dataset manifest checksum contract
- dataset artifact readiness contract

## Policy
- ASH-41 does not run SFT
- ASH-41 does not mutate adapter registry
- ASH-41 does not change current pointer
- ASH-41 does not modify LoRA tensors
- MetadataOnly and SignalOnly samples are not exported as text
- Holdout samples are not used for training
- Raw text is not fabricated
- Dataset artifacts require explicit training later
- training_started remains false
- No Python validator

## Boundary
ash_core defines dataset export contracts and deterministic JSONL/manifest evidence.
orchestrator_local exposes audit/report helpers.
artifact_store may preserve optional dataset artifact snapshots.
ASH-42 executes training later.
