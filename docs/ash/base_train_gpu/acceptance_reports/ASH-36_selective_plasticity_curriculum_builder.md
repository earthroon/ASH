# ASH-36 Selective Plasticity Curriculum Builder

## Status
PASS_SELECTIVE_PLASTICITY_CURRICULUM_BUILDER

## Sealed
- AshSelectivePlasticityCurriculumMode
- AshCurriculumBucketKind
- AshAdapterTrainingIntentKind
- AshCurriculumSampleRole
- AshCurriculumSampleRef
- AshCurriculumBucket
- AshAdapterTrainingIntentPlan
- AshCurriculumSampleWeightPlan
- AshSelectivePlasticityCurriculum
- AshSelectivePlasticityCurriculumReport
- sample ledger to curriculum mapping
- bucket builder
- adapter intent aggregation
- metadata-only signal handling
- curriculum weight calculation

## Policy
- ASH-36 does not export JSONL
- ASH-36 does not run SFT
- ASH-36 does not mutate sample ledger
- ASH-36 does not mutate adapter registry
- MetadataOnly samples are signal-only
- Excluded samples do not enter training buckets
- Ambiguous samples require manual review
- Curriculum is ASH-37 input, not final dataset
- No Python validator

## Boundary
ash_core computes curriculum candidate.
orchestrator_local reports curriculum evidence.
artifact_store preserves optional curriculum snapshots.
ASH-37 builds event-weighted SFT plan.
