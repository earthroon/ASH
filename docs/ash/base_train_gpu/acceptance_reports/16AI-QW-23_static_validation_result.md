# 16AI-QW-23 Static Validation Result

STATIC_VALIDATION: PASS
NATIVE_RUST_TEST: NOT_RUN_TOOLCHAIN_UNAVAILABLE

## File presence

- crates/lora_train/src/qwave_conditioning_train_candidate.rs: PASS
- crates/lora_train/tests/qwave_conditioning_train_candidate.rs: PASS
- crates/lora_train/src/lib.rs export: PASS
- acceptance_reports/16AI-QW-23_qwave_conditioning_train_candidate_gradient_isolation.md: PASS
- bake_artifacts/16AI-QW-23_BAKE_REPORT.md: PASS

## Required symbols

- QWaveConditioningTrainCandidateReceipt: PASS
- QWaveConditioningTrainCandidateEntry: PASS
- QWaveConditioningTrainSourceProjectionRef: PASS
- QWaveConditioningGradientBoundary: PASS
- QWaveConditioningGradientBoundaryReport: PASS
- QWaveConditioningGradientIsolationSnapshot: PASS
- QWaveConditioningGradientFlowPolicy: PASS
- AcceptedTrainCandidateOnly: PASS
- AcceptedReadyForConditionedSftSmoke: PASS
- RejectedMissingQw22ProjectionDryRunReceipt: PASS
- RejectedNonDryRunProjectionSource: PASS
- RejectedProjectionOutputNotFinite: PASS
- RejectedAdapterWeightChanged: PASS
- RejectedLoraAChanged: PASS
- RejectedLoraBChanged: PASS
- RejectedGradientLeakDetected: PASS
- RejectedTrainGraphAttached: PASS
- RejectedTrainingApply: PASS
- RejectedLossBackward: PASS
- RejectedOptimizerStep: PASS
- RejectedQWaveFeatureGradient: PASS
- RejectedBaseModelGradient: PASS

## Test coverage

- test function count: 56
- required minimum: 40
- result: PASS

## Brace balance

- qwave_conditioning_train_candidate.rs: PASS
- qwave_conditioning_train_candidate.rs integration test: PASS

## Toolchain

- cargo: unavailable
- rustc: unavailable
