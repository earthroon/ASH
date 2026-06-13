# 16AI-QW-15 static validation result

STATIC_VALIDATION: PASS
NATIVE_RUST_TEST: NOT_RUN_TOOLCHAIN_UNAVAILABLE

- [x] file_exists:crates/lora_train/src/qwave_curriculum_metadata.rs
- [x] file_exists:crates/lora_train/tests/qwave_curriculum_metadata.rs
- [x] file_exists:crates/lora_train/src/lib.rs
- [x] file_exists:acceptance_reports/16AI-QW-15_qwave_curriculum_metadata_bridge.md
- [x] file_exists:bake_artifacts/16AI-QW-15_BAKE_REPORT.md
- [x] lib_exports_module:qwave_curriculum_metadata
- [x] lib_exports_build_receipt
- [x] contains:QWaveCurriculumMetadataReceipt
- [x] contains:QWaveCurriculumMetadataEntry
- [x] contains:QWaveCurriculumMetadataSummary
- [x] contains:QWaveCurriculumDifficultyBand
- [x] contains:QWaveCurriculumDifficultyReason
- [x] contains:QWaveCurriculumSourceSampleSummary
- [x] contains:QWaveCurriculumWeightCandidateRef
- [x] contains:AcceptedMetadataOnly
- [x] contains:RejectedCurriculumApply
- [x] contains:RejectedBatchReorder
- [x] contains:RejectedSchedulerMutation
- [x] contains:RejectedSampleWeightApply
- [x] contains:RejectedLossRewrite
- [x] contains:RejectedGradientScaling
- [x] contains:RejectedOptimizerMutation
- [x] contains:RejectedDirectLogitMutation
- [x] contains:RejectedTokenIdMutation
- [x] contains:RejectedVocabAugmentation
- [x] contains:RejectedEmbeddingResize
- [x] contains:RejectedNewTokenCreation
- [x] contains:RejectedLoraRoutingFinalization
- [x] contains:RejectedAdapterPointerMutation
- [x] contains:RejectedSamplerMutation
- [x] contains:RejectedBackendSwitch
- [x] contains:metadata_only: true
- [x] contains:applied_curriculum_count: 0
- [x] contains:curriculum_order_unchanged: true
- [x] contains:batch_order_unchanged: true
- [x] contains:scheduler_unchanged: true
- [x] contains:loss_unchanged: true
- [x] contains:gradients_unchanged: true
- [x] contains:optimizer_unchanged: true
- [x] test_count_at_least_30
- [x] test_count_exact:50
- [x] brace_balance:qwave_curriculum_metadata.rs
- [x] paren_balance:qwave_curriculum_metadata.rs
- [x] square_balance:qwave_curriculum_metadata.rs
- [x] brace_balance:qwave_curriculum_metadata.rs
- [x] paren_balance:qwave_curriculum_metadata.rs
- [x] square_balance:qwave_curriculum_metadata.rs
- [x] brace_balance:lib.rs
- [x] paren_balance:lib.rs
- [x] square_balance:lib.rs

## Toolchain

```txt
cargo: command not found
rustc: command not found
```
