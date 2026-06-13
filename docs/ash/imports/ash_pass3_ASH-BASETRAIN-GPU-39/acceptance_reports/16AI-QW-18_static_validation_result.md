# 16AI-QW-18 Static Validation Result

## Summary
- file exists `crates/lora_train/src/qwave_sft_ablation_eval.rs`: PASS
- file exists `crates/lora_train/tests/qwave_sft_ablation_eval.rs`: PASS
- file exists `acceptance_reports/16AI-QW-18_qwave_sft_ablation_eval.md`: PASS
- file exists `acceptance_reports/16AI-QW-18_static_validation_result.md`: PASS
- file exists `bake_artifacts/16AI-QW-18_BAKE_REPORT.md`: PASS
- required symbol/string `QWaveSftAblationEvalReceipt`: PASS
- required symbol/string `QWaveSftAblationGroupSnapshot`: PASS
- required symbol/string `QWaveSftAblationMetricSnapshot`: PASS
- required symbol/string `QWaveSftKoreanEvalMetricSnapshot`: PASS
- required symbol/string `QWaveSftAblationComparisonReport`: PASS
- required symbol/string `QWaveSftAblationOutcome`: PASS
- required symbol/string `QWaveSftAblationRecommendation`: PASS
- required symbol/string `AcceptedEvalOnlyAblation`: PASS
- required symbol/string `RejectedMissingQw17DryRunReceipt`: PASS
- required symbol/string `RejectedBaselineGroupKindMismatch`: PASS
- required symbol/string `RejectedGroupNotEvalOnly`: PASS
- required symbol/string `RejectedNonFiniteMetrics`: PASS
- required symbol/string `RejectedInsufficientEvalSamples`: PASS
- required symbol/string `RejectedAutoPromotion`: PASS
- required symbol/string `RejectedSampleWeightApply`: PASS
- required symbol/string `RejectedCurriculumApply`: PASS
- required symbol/string `RejectedLossRewrite`: PASS
- required symbol/string `RejectedGradientScaling`: PASS
- required symbol/string `RejectedOptimizerMutation`: PASS
- required symbol/string `RejectedSchedulerMutation`: PASS
- required symbol/string `RejectedDirectLogitMutation`: PASS
- required symbol/string `RejectedRuntimeApply`: PASS
- required symbol/string `RejectedBackendSwitch`: PASS
- lib.rs module export: PASS
- lib.rs public use export: PASS
- test function count >= 35: PASS (35)
- brace balance: PASS (131 / 131)
- paren balance: PASS (277 / 277)

## Native Rust Test
NATIVE_RUST_TEST: NOT_RUN_TOOLCHAIN_UNAVAILABLE

Recommended command:

```bash
cargo test -p lora_train qwave_sft_ablation_eval
```

## Final
STATIC_VALIDATION: PASS
