# 16AI-QW-13 Bake Report

## Patch

```txt
16AI-QW-13 — QWave Feature Coverage Telemetry / Batch Korean Structure Ratio Seal
```

## Base

```txt
ash_pass3_16AI-QW-12_sft_qwave_feature_intake_baked.zip
```

## Files Added

```txt
crates/lora_train/src/qwave_feature_coverage_telemetry.rs
crates/lora_train/tests/qwave_feature_coverage_telemetry.rs
acceptance_reports/16AI-QW-13_qwave_feature_coverage_telemetry.md
acceptance_reports/16AI-QW-13_static_validation_result.md
bake_artifacts/16AI-QW-13_BAKE_REPORT.md
```

## Files Modified

```txt
crates/lora_train/src/lib.rs
```

## New Export Surface

```txt
build_qwave_feature_coverage_telemetry_plan
build_qwave_feature_coverage_telemetry_plan_and_receipt
build_qwave_feature_coverage_telemetry_receipt
evaluate_qwave_feature_coverage_telemetry_rejection
QWaveFeatureCoverageTelemetryInput
QWaveFeatureCoverageTelemetryPolicy
QWaveFeatureCoverageRequestedMutations
QWaveFeatureCoverageTokenSummary
QWaveFeatureCoverageSampleSummary
QWaveFeatureCoverageBatchSummary
QWaveKoreanStructureRatioSummary
QWaveFeatureCoverageTelemetryManifest
QWaveFeatureCoverageTelemetryPlan
QWaveFeatureCoverageTelemetryReceipt
QWaveFeatureCoverageTelemetryDecision
QWaveFeatureCoverageTelemetryError
```

## Guard Result

```txt
QW-12 intake receipt guard: IMPLEMENTED
read-only side-channel guard: IMPLEMENTED
shape guard: IMPLEMENTED
finite guard: IMPLEMENTED
telemetry-only manifest: IMPLEMENTED
sample weight apply reject: IMPLEMENTED
curriculum apply reject: IMPLEMENTED
direct logit/loss/token/vocab/embedding mutation reject: IMPLEMENTED
optimizer/sampler/backend switch reject: IMPLEMENTED
```

## Static Validation

```txt
STATIC_VALIDATION: PASS
NATIVE_RUST_TEST: NOT_RUN_TOOLCHAIN_UNAVAILABLE
```

## Next Patch

```txt
16AI-QW-14 — QWave-Gated Sample Weight Candidate / No Loss Rewrite Seal
```
