# 16AI-QW-11 Static Validation Result

## Environment

- `cargo`: command not found
- `rustc`: command not found

## Static checks

- [x] module file exists
- [x] test file exists
- [x] lib mod export
- [x] lib pub use export
- [x] QWaveSftFeatureExportInput
- [x] QWaveSftFeatureSchema
- [x] QWaveSftTokenAlignment
- [x] QWaveSftFeatureAxisMap
- [x] QWaveSftFeatureBatchMatrix
- [x] QWaveSftFeatureExportPolicy
- [x] QWaveSftFeatureExportPlan
- [x] QWaveSftFeatureExportManifest
- [x] QWaveSftFeatureExportReceipt
- [x] QWaveSftFeatureExportError
- [x] build_qwave_sft_feature_export_plan
- [x] build_qwave_sft_feature_export_receipt
- [x] build_qwave_sft_feature_export_plan_and_receipt
- [x] TokenIdMutationForbidden
- [x] DirectLogitMutationForbidden
- [x] LossFunctionMutationForbidden
- [x] LoraRoutingHintCreationForbidden
- [x] BackendQWaveSwitchForbidden
- [x] QWaveGraphRecomputeForbidden
- [x] TokenizerRerunForbidden
- [x] test count == 10
- [x] src braces balanced
- [x] test braces balanced

## Native test status

Native Rust tests were not executed because the container does not provide `cargo` or `rustc`.
