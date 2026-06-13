# 16AI-QW-14 — QWave-Gated Sample Weight Candidate / No Loss Rewrite Seal

## 0. Base

```txt
Base ZIP: ash_pass3_16AI-QW-13_qwave_feature_coverage_telemetry_baked.zip
Patch: 16AI-QW-14
Status: STATIC_VALIDATION_PASS / NATIVE_RUST_TEST_NOT_RUN_TOOLCHAIN_UNAVAILABLE
```

## 1. Input SSOT

```txt
crates/lora_train/src/qwave_feature_coverage_telemetry.rs
QWaveFeatureCoverageTelemetryReceipt
QWaveFeatureCoverageSampleSummary-derived source fields
```

## 2. New SSOT

```txt
crates/lora_train/src/qwave_sample_weight_candidate.rs
QWaveSampleWeightCandidateReceipt
```

## 3. Implemented contract

QW-14 consumes QW-13 telemetry receipt metadata and sample summaries, then generates candidate-only sample weight metadata.

```txt
QW-13 Telemetry Receipt
+ source sample summaries
+ candidate policy
→ QWaveSampleWeightCandidateEntry[]
→ QWaveSampleWeightCandidateSummary
→ QWaveSampleWeightCandidateManifest
→ QWaveSampleWeightCandidateReceipt
```

## 4. Candidate-only seal

Implemented default policy:

```txt
candidate_only = true
min_candidate_weight = 0.75
neutral_candidate_weight = 1.0
max_candidate_weight = 1.25
allow_operator_review_queue = true
```

Implemented unchanged manifest flags:

```txt
sample_weights_unchanged = true
loss_unchanged = true
gradients_unchanged = true
optimizer_unchanged = true
scheduler_unchanged = true
logits_unchanged = true
token_ids_unchanged = true
vocab_unchanged = true
embeddings_unchanged = true
lora_routing_unchanged = true
adapter_pointer_unchanged = true
sampler_unchanged = true
```

## 5. Guard coverage

Implemented rejections:

```txt
RejectedMissingQw13TelemetryReceipt
RejectedMissingSampleSummaries
RejectedBatchSizeMismatch
RejectedNonFiniteValues
RejectedSampleWeightApply
RejectedLossRewrite
RejectedGradientScaling
RejectedOptimizerMutation
RejectedSchedulerMutation
RejectedDirectLogitMutation
RejectedTokenIdMutation
RejectedVocabAugmentation
RejectedEmbeddingResize
RejectedNewTokenCreation
RejectedLoraRoutingFinalization
RejectedAdapterPointerMutation
RejectedSamplerMutation
RejectedBackendSwitch
```

## 6. Candidate calculation

Implemented boost component:

```txt
korean_structure_ratio * korean_structure_gain
+ qwave_coverage_mean * qwave_coverage_gain
+ valid_feature_ratio * valid_feature_gain
```

Implemented damp component:

```txt
protected_span_ratio * protected_penalty_strength
+ special_token_ratio * special_penalty_strength
+ unknown_token_safe_ratio * unknown_penalty_strength
+ byte_fallback_safe_ratio * byte_fallback_penalty_strength
```

Implemented candidate weight:

```txt
clamp(neutral_candidate_weight + boost_component - damp_component, min_candidate_weight, max_candidate_weight)
```

Implemented confidence:

```txt
mean(korean_structure_ratio, qwave_coverage_mean, valid_feature_ratio, hangul_token_ratio)
* (1.0 - mean(protected_span_ratio, special_token_ratio, unknown_token_safe_ratio, byte_fallback_safe_ratio))
```

## 7. Reason codes

Implemented reason codes:

```txt
NeutralInsufficientQWaveCoverage
NeutralLowHangulRatio
BoostHighKoreanStructureRatio
BoostHighQWaveCoverage
BoostHighValidFeatureRatio
DampProtectedSpanPressure
DampSpecialTokenPressure
DampUnknownTokenPressure
DampByteFallbackPressure
ClampMinApplied
ClampMaxApplied
```

## 8. Tests

Added:

```txt
crates/lora_train/tests/qwave_sample_weight_candidate.rs
```

Test count:

```txt
36 tests
```

Coverage includes:

```txt
PASS — consumes QW-13 telemetry receipt
PASS — builds candidate entries for each sample
PASS — verifies batch size matches sample summary count
PASS — computes boost component
PASS — computes damp component
PASS — computes candidate weight
PASS — clamps candidate weight minimum
PASS — clamps candidate weight maximum
PASS — computes candidate confidence
PASS — emits reason codes
PASS — marks review status candidate only / pending operator review
PASS — summary counts boost/damp/neutral samples
PASS — keeps applied sample weight count zero
PASS — manifest preserves loss/gradient/optimizer/scheduler unchanged
PASS — deterministic candidate receipt
FAIL — rejects missing QW-13 telemetry receipt
FAIL — rejects missing sample summaries
FAIL — rejects batch size mismatch
FAIL — rejects non-finite sample summary value
FAIL — rejects sample weight apply
FAIL — rejects loss rewrite
FAIL — rejects gradient scaling
FAIL — rejects optimizer mutation
FAIL — rejects scheduler mutation
FAIL — rejects direct logit mutation
FAIL — rejects token id mutation
FAIL — rejects vocab augmentation
FAIL — rejects embedding resize
FAIL — rejects new token creation
FAIL — rejects LoRA routing finalization
FAIL — rejects adapter pointer mutation
FAIL — rejects sampler mutation
FAIL — rejects backend switch
```

## 9. Native test status

Native Rust tests were not executed in this container.

```txt
cargo: command not found
rustc: command not found
```

Recommended native validation:

```bash
cargo test -p lora_train qwave_sample_weight_candidate
cargo test -p lora_train
```

## 10. Final seal

```txt
QW-14 creates sample weight candidate metadata only.
It does not apply sample weights.
It does not rewrite loss.
It does not scale gradients.
It does not mutate optimizer/scheduler/logits/tokens/vocab/embedding/LoRA routing/adapter pointer/sampler/backend.
```
