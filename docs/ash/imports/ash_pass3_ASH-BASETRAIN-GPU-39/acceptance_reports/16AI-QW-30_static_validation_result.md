# 16AI-QW-30 Static Validation Result

```txt
STATIC_VALIDATION: PASS
NATIVE_RUST_TEST: NOT_RUN_TOOLCHAIN_UNAVAILABLE
```

## Checks
- File exists: `crates/lora_train/src/qwave_runtime_apply_gate.rs` — PASS
- Test exists: `crates/lora_train/tests/qwave_runtime_apply_gate.rs` — PASS
- `lib.rs` module export — PASS
- `lib.rs` public re-export block — PASS
- Brace balance — PASS
- Test marker count: 54 — PASS

## Required symbols
- `QWaveRuntimeApplyGateReceipt` — PASS
- `QWaveRuntimeApplyShadowEvalRef` — PASS
- `QWaveRuntimeApplyOperatorRequest` — PASS
- `QWaveRuntimeFeatureFlagActivationPlan` — PASS
- `QWaveRuntimeRollbackPointerRef` — PASS
- `QWaveRuntimeTelemetryActivationPlan` — PASS
- `QWaveRuntimeApplyEligibilityReport` — PASS
- `QWaveRuntimeApplyQueueEntry` — PASS
- `QWaveRuntimeApplyReviewStatus` — PASS
- `QWaveRuntimeApplyActivationScope` — PASS
- `QWaveRuntimeApplyNextStage` — PASS
- `AcceptedRuntimeApplyGate` — PASS
- `RejectedMissingQw29ShadowEvalReceipt` — PASS
- `RejectedShadowEvalRegressionSource` — PASS
- `RejectedShadowEvalUnsafeSource` — PASS
- `RejectedMissingOperatorRequest` — PASS
- `RejectedMissingOperatorAcknowledgement` — PASS
- `RejectedMissingFeatureFlagPlan` — PASS
- `RejectedSilentEnableAllowed` — PASS
- `RejectedAutoEnableAllowed` — PASS
- `RejectedMissingRollbackPointerRef` — PASS
- `RejectedRollbackPointerNotReady` — PASS
- `RejectedMissingTelemetryActivationPlan` — PASS
- `RejectedRuntimeTelemetryNotReady` — PASS
- `RejectedSilentEnable` — PASS
- `RejectedAutoRuntimeApply` — PASS
- `RejectedProductionSamplerMutation` — PASS
- `RejectedRuntimeGateWithoutShadowImproved` — PASS

## Native test command for Rust environment
```bash
cargo test -p lora_train qwave_runtime_apply_gate
```
