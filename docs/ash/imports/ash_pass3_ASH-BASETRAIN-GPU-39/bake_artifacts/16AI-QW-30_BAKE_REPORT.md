# 16AI-QW-30 Bake Report

## Patch
`16AI-QW-30 — QWave Runtime Apply Gate / Explicit Operator-Controlled Activation Seal`

## Base
`ash_pass3_16AI-QW-29_qwave_runtime_shadow_eval_baked.zip`

## Added / modified files
```txt
crates/lora_train/src/qwave_runtime_apply_gate.rs
crates/lora_train/tests/qwave_runtime_apply_gate.rs
crates/lora_train/src/lib.rs
acceptance_reports/16AI-QW-30_qwave_runtime_apply_gate.md
acceptance_reports/16AI-QW-30_static_validation_result.md
bake_artifacts/16AI-QW-30_BAKE_REPORT.md
```

## Implemented SSOT
```txt
QWaveRuntimeApplyGateInput
QWaveRuntimeApplyShadowEvalRef
QWaveRuntimeApplyOperatorRequest
QWaveRuntimeFeatureFlagActivationPlan
QWaveRuntimeRollbackPointerRef
QWaveRuntimeTelemetryActivationPlan
QWaveRuntimeApplyEligibilityReport
QWaveRuntimeApplyQueueEntry
QWaveRuntimeApplyGateManifest
QWaveRuntimeApplyGatePlan
QWaveRuntimeApplyGateReceipt
```

## Guard summary
QW-30 consumes the QW-29 runtime shadow eval receipt and creates an explicit operator-controlled apply gate. The implementation requires feature-flag readiness, rollback pointer readiness, runtime telemetry readiness, and operator acknowledgement. It blocks silent enable and auto runtime apply.

## Static validation
```txt
STATIC_VALIDATION: PASS
NATIVE_RUST_TEST: NOT_RUN_TOOLCHAIN_UNAVAILABLE
```

## Recommended native validation
```bash
cargo test -p lora_train qwave_runtime_apply_gate
```
