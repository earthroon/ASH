# 16AI-QW-15 Bake Report

## Patch

```txt
16AI-QW-15 — QWave Curriculum Metadata Bridge / Korean Structure Difficulty Seal
```

## Base

```txt
ash_pass3_16AI-QW-14_qwave_gated_sample_weight_candidate_baked.zip
```

## Files added

```txt
crates/lora_train/src/qwave_curriculum_metadata.rs
crates/lora_train/tests/qwave_curriculum_metadata.rs
acceptance_reports/16AI-QW-15_qwave_curriculum_metadata_bridge.md
acceptance_reports/16AI-QW-15_static_validation_result.md
bake_artifacts/16AI-QW-15_BAKE_REPORT.md
```

## Files modified

```txt
crates/lora_train/src/lib.rs
```

## New SSOT

```txt
QWaveCurriculumMetadataReceipt
```

## Implemented structures

```txt
QWaveCurriculumMetadataInput
QWaveCurriculumSourceSampleSummary
QWaveCurriculumWeightCandidateRef
QWaveCurriculumMetadataPolicy
QWaveCurriculumMetadataRequestedMutations
QWaveCurriculumDifficultyBand
QWaveCurriculumDifficultyReason
QWaveCurriculumMetadataEntry
QWaveCurriculumMetadataSummary
QWaveCurriculumMetadataManifest
QWaveCurriculumMetadataPlan
QWaveCurriculumMetadataReceipt
```

## Implemented functions

```txt
build_qwave_curriculum_metadata_plan
build_qwave_curriculum_metadata_receipt
build_qwave_curriculum_metadata_plan_and_receipt
evaluate_qwave_curriculum_metadata_rejection
```

## Guard seal

```txt
curriculum apply: rejected
batch reorder: rejected
scheduler mutation: rejected
sample weight apply: rejected
loss rewrite: rejected
gradient scaling: rejected
optimizer mutation: rejected
direct logit mutation: rejected
token id mutation: rejected
vocab augmentation: rejected
embedding resize: rejected
new token creation: rejected
LoRA routing finalization: rejected
adapter pointer mutation: rejected
sampler mutation: rejected
backend switch: rejected
```

## Metadata-only seal

```txt
metadata_only: true
applied_curriculum_count: 0
curriculum_order_unchanged: true
batch_order_unchanged: true
scheduler_unchanged: true
sample_weights_unchanged: true
loss_unchanged: true
gradients_unchanged: true
optimizer_unchanged: true
```

## Validation

```txt
STATIC_VALIDATION: PASS
NATIVE_RUST_TEST: NOT_RUN_TOOLCHAIN_UNAVAILABLE
```
