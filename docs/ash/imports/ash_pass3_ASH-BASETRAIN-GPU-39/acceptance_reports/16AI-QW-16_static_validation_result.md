# 16AI-QW-16 Static Validation Result

## 확정

- STATIC_VALIDATION: PASS
- Native Rust test: NOT_RUN_TOOLCHAIN_UNAVAILABLE
- `crates/lora_train/src/qwave_feature_intake_parity_smoke.rs`: PRESENT
- `crates/lora_train/tests/qwave_feature_intake_parity_smoke.rs`: PRESENT
- `crates/lora_train/src/lib.rs` module export: PRESENT
- `crates/lora_train/src/lib.rs` public re-export block: PRESENT
- `acceptance_reports/16AI-QW-16_qwave_feature_intake_cpu_gpu_parity_smoke.md`: PRESENT
- `bake_artifacts/16AI-QW-16_BAKE_REPORT.md`: PRESENT
- brace balance: PASS
- test functions detected: 47

## Required string checks

- `QWaveFeatureIntakeParityReceipt`: PASS
- `QWaveFeatureMatrixCpuLoadSnapshot`: PASS
- `QWaveFeatureMatrixGpuUploadSnapshot`: PASS
- `QWaveFeatureMatrixParityReport`: PASS
- `QWaveFeatureMaskParityReport`: PASS
- `AcceptedCpuGpuParitySmoke`: PASS
- `RejectedFeatureMatrixChecksumMismatch`: PASS
- `RejectedFeatureMaskChecksumMismatch`: PASS
- `RejectedCoverageMaskChecksumMismatch`: PASS
- `RejectedShapeMismatch`: PASS
- `RejectedDTypeMismatch`: PASS
- `RejectedLayoutMismatch`: PASS
- `RejectedStrideMismatch`: PASS
- `RejectedFiniteMismatch`: PASS
- `RejectedStatMismatch`: PASS
- `RejectedGpuWriteBufferEnabled`: PASS
- `RejectedShaderMutationEnabled`: PASS
- `RejectedSampleWeightApply`: PASS
- `RejectedCurriculumApply`: PASS
- `RejectedLossRewrite`: PASS
- `RejectedGradientScaling`: PASS
- `RejectedOptimizerMutation`: PASS
- `RejectedSchedulerMutation`: PASS
- `RejectedDirectLogitMutation`: PASS
- `RejectedBackendSwitch`: PASS

## 판단불가

- `cargo test -p lora_train qwave_feature_intake_parity_smoke`는 현재 컨테이너에 `cargo` / `rustc`가 없어 실행하지 못했다.
