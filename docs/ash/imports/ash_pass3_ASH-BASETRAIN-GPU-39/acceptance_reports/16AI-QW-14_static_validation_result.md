# 16AI-QW-14 static validation result

STATIC_VALIDATION: PASS
NATIVE_RUST_TEST: NOT_RUN_TOOLCHAIN_UNAVAILABLE

- [x] file_exists:crates/lora_train/src/qwave_sample_weight_candidate.rs
- [x] file_exists:crates/lora_train/tests/qwave_sample_weight_candidate.rs
- [x] file_exists:crates/lora_train/src/lib.rs
- [x] file_exists:acceptance_reports/16AI-QW-14_qwave_gated_sample_weight_candidate.md
- [x] lib_exports_module:qwave_sample_weight_candidate
- [x] lib_exports_build_receipt
- [x] contains:QWaveSampleWeightCandidateReceipt
- [x] contains:QWaveSampleWeightCandidateEntry
- [x] contains:QWaveSampleWeightCandidateSummary
- [x] contains:QWaveSampleWeightCandidateReason
- [x] contains:QWaveSampleWeightCandidateReviewStatus
- [x] contains:QWaveSampleWeightSourceSampleSummary
- [x] contains:AcceptedCandidateOnly
- [x] contains:RejectedSampleWeightApply
- [x] contains:RejectedLossRewrite
- [x] contains:RejectedGradientScaling
- [x] contains:RejectedOptimizerMutation
- [x] contains:RejectedSchedulerMutation
- [x] contains:RejectedDirectLogitMutation
- [x] contains:RejectedTokenIdMutation
- [x] contains:RejectedVocabAugmentation
- [x] contains:RejectedEmbeddingResize
- [x] contains:RejectedNewTokenCreation
- [x] contains:RejectedLoraRoutingFinalization
- [x] contains:RejectedAdapterPointerMutation
- [x] contains:RejectedSamplerMutation
- [x] contains:RejectedBackendSwitch
- [x] contains:candidate_only: true
- [x] contains:sample_weights_unchanged: true
- [x] contains:loss_unchanged: true
- [x] contains:gradients_unchanged: true
- [x] contains:applied_sample_weight_count: 0
- [x] test_count_at_least_25
- [x] test_count_exact
- [x] brace_balance:qwave_sample_weight_candidate.rs
- [x] paren_balance:qwave_sample_weight_candidate.rs
- [x] square_balance:qwave_sample_weight_candidate.rs
- [x] brace_balance:qwave_sample_weight_candidate.rs
- [x] paren_balance:qwave_sample_weight_candidate.rs
- [x] square_balance:qwave_sample_weight_candidate.rs
- [x] brace_balance:lib.rs
- [x] paren_balance:lib.rs
- [x] square_balance:lib.rs

## Toolchain

```txt
cargo: command not found
rustc: command not found
```
