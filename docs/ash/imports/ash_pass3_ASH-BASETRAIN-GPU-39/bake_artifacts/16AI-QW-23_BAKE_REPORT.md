# 16AI-QW-23 Bake Report

Patch: 16AI-QW-23 -- QWave Conditioning Train Candidate / Gradient Isolation Seal
Base ZIP: ash_pass3_16AI-QW-22_qwave_conditioning_projection_dry_run_baked.zip

## Files added / modified

- Added: crates/lora_train/src/qwave_conditioning_train_candidate.rs
- Added: crates/lora_train/tests/qwave_conditioning_train_candidate.rs
- Modified: crates/lora_train/src/lib.rs
- Added: acceptance_reports/16AI-QW-23_qwave_conditioning_train_candidate_gradient_isolation.md
- Added: acceptance_reports/16AI-QW-23_static_validation_result.md
- Added: bake_artifacts/16AI-QW-23_BAKE_REPORT.md

## Implemented SSOT

- QWaveConditioningTrainCandidateInput
- QWaveConditioningTrainSourceProjectionRef
- QWaveConditioningGradientBoundary
- QWaveConditioningGradientFlowPolicy
- QWaveConditioningGradientIsolationSnapshot
- QWaveConditioningGradientBoundaryReport
- QWaveConditioningTrainCandidateEntry
- QWaveConditioningTrainCandidateManifest
- QWaveConditioningTrainCandidatePlan
- QWaveConditioningTrainCandidateReceipt

## Guard result

- QWave feature gradient: blocked
- Projection layer active gradient: blocked
- LoRA adapter active gradient: blocked
- LoRA A/B active gradient: blocked
- Adapter pointer gradient: blocked
- Base model gradient: blocked
- Optimizer/scheduler gradient: blocked
- Loss backward: blocked
- Optimizer step: blocked
- Train graph attachment: blocked
- Gradient leak: rejected
- Train candidate only: enforced

## Validation

STATIC_VALIDATION: PASS
NATIVE_RUST_TEST: NOT_RUN_TOOLCHAIN_UNAVAILABLE
