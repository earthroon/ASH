# ASH-46 Plasticity Dataset Sanitizer / PromptRef Resolver

## Status
PASS_ASH_46_PLASTICITY_DATASET_MANIFEST

## Sealed
- AshPlasticityDatasetSanitizerMode
- AshPromptRefKind
- AshPromptRefResolutionStatus
- AshPromptRefResolutionIssueKind
- AshPromptRefResolutionTrace
- AshPromptRegistryRecord
- AshPlasticitySampleKind
- AshPlasticitySampleDecision
- AshPlasticityDatasetIssueKind
- AshPlasticityDatasetIssueSeverity
- AshPlasticityDatasetIssue
- AshPlasticityRawSample
- AshPlasticitySanitizedSample
- AshPlasticityQuarantineSample
- AshPlasticityDatasetSanitizationConfig
- AshPlasticityDatasetSanitizationManifest
- AshPlasticityDatasetSanitizationReport
- prompt_ref resolution
- dataset contamination detection
- train/eval leakage blocking
- duplicate and label conflict detection
- sanitized dataset candidate generation
- quarantine dataset generation

## Policy
- Missing prompt_ref cannot be silently repaired.
- Ambiguous prompt_ref cannot be accepted.
- Eval/Holdout prompt leakage blocks training.
- Label conflict cannot be averaged.
- Manual review sample cannot auto-enter training.
- LoRA pointer mismatch source is quarantined.
- Replay seal and snapshot bundle are required when configured.
- Sanitized dataset is candidate only.
- No SFT/DPO training execution.
- Runtime router config is not mutated.
- Current pointer is not changed.
- No LoRA attach/detach.
- No Python validator.

## Boundary
ASH-46 only sanitizes plasticity dataset candidates.
ASH-47 builds HardNegative Preference Dataset / DPO Bridge.
ASH-48 handles explicit runtime apply.
