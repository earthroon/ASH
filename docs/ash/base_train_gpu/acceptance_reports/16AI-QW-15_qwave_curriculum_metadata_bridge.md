# 16AI-QW-15 — QWave Curriculum Metadata Bridge / Korean Structure Difficulty Seal

## 0. Base

```txt
Base ZIP: ash_pass3_16AI-QW-14_qwave_gated_sample_weight_candidate_baked.zip
Patch: 16AI-QW-15
Status: STATIC_VALIDATION_PASS / NATIVE_RUST_TEST_NOT_RUN_TOOLCHAIN_UNAVAILABLE
```

## 1. Input SSOT

```txt
crates/lora_train/src/qwave_feature_coverage_telemetry.rs
crates/lora_train/src/qwave_sample_weight_candidate.rs
QWaveFeatureCoverageTelemetryReceipt-derived sample summaries
QWaveSampleWeightCandidateReceipt-derived candidate refs
```

## 2. New SSOT

```txt
crates/lora_train/src/qwave_curriculum_metadata.rs
QWaveCurriculumMetadataReceipt
```

## 3. Implemented contract

QW-15 consumes QW-13 telemetry metadata and QW-14 candidate-only references, then generates metadata-only curriculum difficulty records.

```txt
QW-13 Telemetry Receipt
+ QW-14 Sample Weight Candidate Receipt
+ source sample summaries
+ candidate refs
+ curriculum policy
→ QWaveCurriculumMetadataEntry[]
→ QWaveCurriculumMetadataSummary
→ QWaveCurriculumMetadataManifest
→ QWaveCurriculumMetadataReceipt
```

## 4. Metadata-only seal

Implemented default policy:

```txt
metadata_only = true
easy_threshold = 0.30
medium_threshold = 0.55
hard_threshold = 0.78
allow_operator_review_queue = true
```

Implemented unchanged manifest flags:

```txt
curriculum_order_unchanged = true
batch_order_unchanged = true
scheduler_unchanged = true
sample_weights_unchanged = true
loss_unchanged = true
gradients_unchanged = true
optimizer_unchanged = true
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
RejectedMissingQw14CandidateReceipt
RejectedMissingSampleSummaries
RejectedMissingCandidateRefs
RejectedBatchSizeMismatch
RejectedCandidateRefMismatch
RejectedNonFiniteValues
RejectedCurriculumApply
RejectedBatchReorder
RejectedSchedulerMutation
RejectedSampleWeightApply
RejectedLossRewrite
RejectedGradientScaling
RejectedOptimizerMutation
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

## 6. Difficulty calculation

Implemented components:

```txt
korean_structure_component = korean_structure_ratio * korean_structure_weight
coda_closure_component = mean(closure_mean, pressure_mean) * coda_closure_weight
transition_component = mean(transition_energy_mean, flow_continuity_mean) * transition_weight
eojeol_sentence_component = mean(eojeol_binding_mean, sentence_closure_mean) * eojeol_sentence_weight
coverage_confidence_component = mean(qwave_coverage_mean, candidate_ref.confidence) * coverage_confidence_weight
noise_penalty_component = protected + special + unknown penalties
```

Implemented score:

```txt
difficulty_score = clamp(
  korean_structure_component
  + coda_closure_component
  + transition_component
  + eojeol_sentence_component
  + coverage_confidence_component
  - noise_penalty_component,
  0.0,
  1.0
)
```

## 7. Difficulty bands

Implemented bands:

```txt
Easy
Medium
Hard
Dense
ProtectedOrNoisy
```

Band selection is metadata-only. It does not reorder batches, mutate schedules, apply sample weights, or rewrite loss.

## 8. Candidate ref boundary

QW-14 candidate refs are accepted only if they are still candidate-only and unapplied.

```txt
candidate_only = true
applied_to_loss = false
applied_to_optimizer = false
applied_to_scheduler = false
```

Applied QW-14 candidate references are rejected as candidate ref mismatch.

## 9. Test coverage

```txt
test_count: 50
PASS paths: QW-13 consume, QW-14 consume, entry generation, component calculation, difficulty bands, metadata-only manifest, deterministic receipt
FAIL paths: missing receipts, missing summaries, missing refs, batch mismatch, candidate ref mismatch, non-finite values, all mutation requests
```

## 10. Judgment

### 확정

```txt
QW-15 creates metadata-only Korean structure difficulty records and seals unchanged trainer behavior.
```

### 추정

```txt
Closure and pressure are used as the current coda/closure proxy until a dedicated coda_density telemetry axis is added later.
```

### 판단불가

```txt
Native Rust compile/test could not be executed because cargo/rustc are unavailable in this environment.
```
