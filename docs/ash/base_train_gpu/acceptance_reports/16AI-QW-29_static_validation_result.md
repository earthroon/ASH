# 16AI-QW-29 Static Validation Result

STATIC_VALIDATION: PASS

## File existence

- module: True
- tests: True
- lib.rs: True
- acceptance report: True
- bake report: True

## Required symbol scan

- QWaveRuntimeShadowEvalReceipt: True
- QWaveRuntimeShadowRollbackRef: True
- QWaveRuntimeShadowRoutingHintRef: True
- QWaveRuntimeShadowPromptSet: True
- QWaveRuntimeShadowOutputSnapshot: True
- QWaveRuntimeShadowOutputPairResult: True
- QWaveRuntimeShadowOutputDiffReport: True
- QWaveRuntimeKoreanPromptShadowEvalReport: True
- QWaveRuntimeShadowDeterminismReport: True
- QWaveRuntimeShadowNoMutationReport: True
- QWaveRuntimeShadowEvalOutcome: True
- QWaveRuntimeShadowEvalRecommendation: True
- AcceptedRuntimeShadowEval: True
- RejectedMissingQw28RollbackLedgerReceipt: True
- RejectedRollbackLedgerNotReady: True
- RejectedRuntimeHintNotCandidateOnly: True
- RejectedNonShadowOutput: True
- RejectedProductionVisibleOutput: True
- RejectedSamplerConfigChanged: True
- RejectedProductionSamplerMutation: True
- RejectedRuntimeApply: True
- RejectedCurrentPointerMutation: True
- RejectedAdapterPointerMutation: True
- RejectedBackendSwitch: True

## lib.rs export scan

- pub mod qwave_runtime_shadow_eval: True
- QWaveRuntimeShadowEvalReceipt: True
- build_qwave_runtime_shadow_eval_receipt: True

## Balance

- {: 0
- (: 0
- [: 0

## Test count: 51

## Native Rust test

NATIVE_RUST_TEST: NOT_RUN_TOOLCHAIN_UNAVAILABLE
