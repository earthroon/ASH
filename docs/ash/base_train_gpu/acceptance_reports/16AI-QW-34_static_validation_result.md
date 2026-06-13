# 16AI-QW-34 Static Validation Result

STATIC_VALIDATION: PASS
NATIVE_RUST_TEST: NOT_RUN_TOOLCHAIN_UNAVAILABLE

## Files checked
- crates/lora_train/src/qwave_canary_telemetry_monitor.rs
- crates/lora_train/tests/qwave_canary_telemetry_monitor.rs
- crates/lora_train/src/lib.rs
- acceptance_reports/16AI-QW-34_qwave_canary_telemetry_monitor.md
- bake_artifacts/16AI-QW-34_BAKE_REPORT.md

## Required symbols checked
- QWaveCanaryTelemetryMonitorReceipt
- QWaveCanaryTelemetryExecutionRef
- QWaveCanaryTelemetryRollbackDisableRef
- QWaveCanaryTelemetrySnapshot
- QWaveCanaryKoreanQualityDriftReport
- QWaveCanaryNonKoreanRegressionReport
- QWaveCanarySamplerParityReport
- QWaveCanaryOutputHealthReport
- QWaveCanaryRollbackTriggerReport
- QWaveCanaryExpansionOrRollbackReviewEntry
- QWaveCanaryTelemetryEligibilityReport
- QWaveCanaryTelemetryMonitorRecommendation
- QWaveCanaryTelemetryMonitorReviewStatus
- QWaveCanaryTelemetryMonitorNextStage
- AcceptedCanaryTelemetryMonitor
- AcceptedExpansionReviewCandidate
- AcceptedHoldCanary
- AcceptedRollbackReviewCandidate
- RejectedMissingQw33CanaryExecutionReceipt
- RejectedCanaryExecutionSourceInvalid
- RejectedRollbackDisableNotReady
- RejectedIncompleteTelemetry
- RejectedNonFiniteTelemetry
- RejectedKoreanQualityRegression
- RejectedNonKoreanRegression
- RejectedAutoExpansion
- RejectedAutoRollback
- RejectedFullProductionEnable

## Test count
- qwave_canary_telemetry_monitor tests: 55
