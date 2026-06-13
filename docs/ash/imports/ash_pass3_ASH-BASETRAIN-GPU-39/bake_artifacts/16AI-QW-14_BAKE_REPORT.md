# 16AI-QW-14 Bake Report

## Patch

```txt
16AI-QW-14 — QWave-Gated Sample Weight Candidate / No Loss Rewrite Seal
```

## Base

```txt
ash_pass3_16AI-QW-13_qwave_feature_coverage_telemetry_baked.zip
```

## Files added

```txt
crates/lora_train/src/qwave_sample_weight_candidate.rs
crates/lora_train/tests/qwave_sample_weight_candidate.rs
acceptance_reports/16AI-QW-14_qwave_gated_sample_weight_candidate.md
acceptance_reports/16AI-QW-14_static_validation_result.md
bake_artifacts/16AI-QW-14_BAKE_REPORT.md
```

## Files modified

```txt
crates/lora_train/src/lib.rs
```

## New SSOT

```txt
QWaveSampleWeightCandidateReceipt
```

## Implemented structures

```txt
QWaveSampleWeightCandidateInput
QWaveSampleWeightSourceSampleSummary
QWaveSampleWeightCandidatePolicy
QWaveSampleWeightCandidateRequestedMutations
QWaveSampleWeightCandidateReason
QWaveSampleWeightCandidateReviewStatus
QWaveSampleWeightCandidateEntry
QWaveSampleWeightCandidateSummary
QWaveSampleWeightCandidateManifest
QWaveSampleWeightCandidatePlan
QWaveSampleWeightCandidateReceipt
```

## Implemented functions

```txt
build_qwave_sample_weight_candidate_plan
build_qwave_sample_weight_candidate_receipt
build_qwave_sample_weight_candidate_plan_and_receipt
evaluate_qwave_sample_weight_candidate_rejection
```

## Guard seal

```txt
sample weight apply: rejected
loss rewrite: rejected
gradient scaling: rejected
optimizer mutation: rejected
scheduler mutation: rejected
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

## Candidate-only seal

```txt
candidate_only = true
applied_to_loss = false
applied_to_optimizer = false
applied_to_scheduler = false
applied_sample_weight_count = 0
```

## Test coverage

```txt
crates/lora_train/tests/qwave_sample_weight_candidate.rs
36 tests declared
```

## Validation

```txt
STATIC_VALIDATION: PASS
NATIVE_RUST_TEST: NOT_RUN_TOOLCHAIN_UNAVAILABLE
```

## Recommended native validation

```bash
cargo test -p lora_train qwave_sample_weight_candidate
cargo test -p lora_train
```

## Next patch

```txt
16AI-QW-15 — QWave Curriculum Metadata Bridge / Korean Structure Difficulty Seal
```
