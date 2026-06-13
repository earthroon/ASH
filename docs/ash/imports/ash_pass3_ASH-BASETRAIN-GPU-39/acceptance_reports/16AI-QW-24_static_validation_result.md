# 16AI-QW-24 Static Validation Result

STATIC_VALIDATION: PASS  
NATIVE_RUST_TEST: NOT_RUN_TOOLCHAIN_UNAVAILABLE

## Checked Files

- `crates/lora_train/src/qwave_conditioned_sft_smoke.rs`: present
- `crates/lora_train/tests/qwave_conditioned_sft_smoke.rs`: present
- `crates/lora_train/src/lib.rs`: export block present
- `acceptance_reports/16AI-QW-24_qwave_conditioned_sft_smoke.md`: present
- `bake_artifacts/16AI-QW-24_BAKE_REPORT.md`: present

## Required Symbols

- `QWaveConditionedSftSmokeReceipt`: present
- `QWaveConditionedSftSmokeSnapshot`: present
- `QWaveConditionedSftLossReport`: present
- `QWaveConditionedSftGradientReport`: present
- `QWaveConditionedAdapterDeltaReport`: present
- `QWaveConditionedNoRegressionReport`: present
- `QWaveConditionedSftTrainCandidateRef`: present
- `AcceptedConditionedSftSmoke`: present
- `RejectedMissingQw23TrainCandidateReceipt`: present
- `RejectedTrainCandidateNotGradientIsolated`: present
- `RejectedNonSandboxedSmoke`: present
- `RejectedNonFiniteLoss`: present
- `RejectedNonFiniteGradient`: present
- `RejectedQWaveFeatureGradientConnected`: present
- `RejectedBaseModelGradientConnected`: present
- `RejectedAdapterDeltaZero`: present
- `RejectedAdapterDeltaOutOfBounds`: present
- `RejectedTokenIdsChanged`: present
- `RejectedVocabChanged`: present
- `RejectedEmbeddingsChanged`: present
- `RejectedBaseModelChanged`: present
- `RejectedProductionStateChanged`: present
- `RejectedLossRegression`: present
- `RejectedGradientRegression`: present

## Structural Checks

- Test functions: 54
- Brace balance: PASS
- lib.rs module export: PASS
- Native cargo test: NOT RUN, toolchain unavailable
