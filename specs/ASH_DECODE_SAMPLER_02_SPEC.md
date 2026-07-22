# ASH-DECODE-SAMPLER-02

## Prompt Corpus Behavioral Gate /
## Greedy-vs-Top-P-vs-Min-P Comparative Evaluation /
## Loop-Break Rate /
## Sentence-Surface Preservation /
## Candidate Distribution Health /
## CPU-GPU Sampled Decode Parity Evidence /
## Sampled Policy Promotion Review /
## No Default Policy Mutation /
## No Model Quality Overclaim Seal

---

## 0. Patch identity

```text
patch_id=ASH-DECODE-SAMPLER-02
runtime_schema=ash.decode.sampler.02.prompt_corpus_behavioral_gate.runtime_artifact.v1
primary_artifact=workspace/runtime/decode/ash_decode_sampler_02_prompt_corpus_behavioral_gate_runtime_artifact.json
```

Parent:

```text
parent_patch_id=ASH-DECODE-SAMPLER-01
parent_schema=ash.decode.sampler.01.active_route_rebind.runtime_artifact.v1
parent_semantic_inventory_digest=44d8d034e15ca27706efa04b66d4fe3c9465fa13b78a54d815c5ca36d4d26d04
parent_execution_artifact_digest=790b728c78cdb303b41564e0f10870876cfa5c971820a0e9ec73f4ed51d93589
parent_spec_commit=7ba898ac145723bf6f5ea70d74de9d46e2a1d9f1
```

Parent readiness:

```text
repository_ready_for_decode_sampler_02=true
decode_sampler_02_readiness_scope=prompt_corpus_behavioral_gate_and_sampled_decode_promotion_review_only
sampled_decode_default_promotion_ready=false
model_quality_promotion_ready=false
production_decode_promotion_ready=false
```

Primary code surfaces:

```text
crates/orchestrator_local/src/decode_sampler_corpus_gate.rs
crates/orchestrator_local/src/bin/ash_decode_sampler_02_prompt_corpus_behavioral_gate.rs
crates/orchestrator_local/src/lib.rs
crates/orchestrator_local/Cargo.toml
```

---

# 1. Purpose

Sampler-01 established typed generation-policy ownership and executed the existing CPU oracle sampler using deterministic synthetic logits. It did not prove actual model-language inference, actual loop break, sentence-surface preservation, candidate distribution health, or CPU-GPU parity readiness.

Sampler-02 executes an immutable prompt corpus through the canonical orchestrator request-file entrypoint under:

```text
greedy_control
top_p_only_baseline
top_p_min_p_probe
```

It measures behavior and emits a promotion review. It never mutates the default sampling policy.

---

# 2. Evidence classes

## 2.1 Actual language inference

For every corpus case and policy, the audit launches:

```text
target/debug/orchestrator_local[.exe] --request-file <request.json>
```

Required evidence:

```text
matching type=response line
response ok=true
outputPath exists
output artifact parses
Sampler-01 route receipt exists and passes
```

This is actual model-language execution, not synthetic-logit execution.

## 2.2 Behavioral heuristics

Loop and sentence-surface metrics are deterministic structural heuristics. They may classify repetition and malformed surfaces, but they do not prove translation fidelity, semantics, grammar, SFT alignment, or production quality.

## 2.3 Candidate distribution

The request enables `candidatePoolSnapshotTopN`. The audit reads runtime candidate snapshots when exposed. Missing snapshots remain explicit:

```text
candidate_snapshots_not_exposed
distribution_health_pass=null
```

No values may be reconstructed or guessed.

## 2.4 CPU-GPU parity

Sampler-02 reads canonical runtime parity-gate fields when present:

```text
gpu_sampling_parity_gate_allowed
gpu_sampling_parity_gate_insufficient_evidence
gpu_sampling_parity_gate_action
gpu_sampling_parity_gate_reason_codes
```

This patch does not force two independent CPU/GPU generations. Therefore:

```text
exact_cpu_gpu_token_parity_execution_count=0
exact_cpu_gpu_token_parity_ready=false
```

Runtime parity evidence may influence promotion review, but must not be mislabeled exact dual-backend parity.

---

# 3. Corpus manifest SSOT

Schema:

```text
ash.decode.sampler.02.prompt_corpus_manifest.v1
```

Canonical fields:

```text
corpus_id
runtime_profile_path
max_new_tokens
seed
candidate_pool_top_n
cases[]
```

Each case owns:

```text
case_id
task
input
glossary[]
tm[]
expected_language
tags[]
```

Required:

```text
case_count>=3
unique non-empty case_id
non-empty task
non-empty input
max_new_tokens>0
```

If the requested manifest path is absent, the audit writes and immediately binds a built-in smoke corpus containing translation, subtitle, Korean freeform, and loop-pressure cases. The manifest SHA-256 enters the runtime artifact.

---

# 4. Three-policy matrix

For every case execute exactly:

```text
GreedyControl
TopPOnlyBaseline
TopPMinPProbe
```

Required:

```text
expected_run_count=corpus_case_count*3
executed_run_count=expected_run_count
```

Inherited policy profiles:

```text
GreedyControl:
  temperature=0.0
  top_k=0
  top_p=1.0
  min_p=0.0

TopPOnlyBaseline:
  temperature=0.80
  top_k=0
  top_p=0.90
  min_p=0.0

TopPMinPProbe:
  temperature=0.80
  top_k=0
  top_p=0.90
  min_p=0.05
```

Shared inputs:

```text
corpus case
runtime profile
max_new_tokens
seed
glossary
translation memory
candidate snapshot top-N
```

No repetition-penalty, QWave, morphological-penalty, rerank, or model-weight change belongs to this patch.

---

# 5. Orchestrator freshness

The audit must not silently use a stale `target/debug/orchestrator_local` binary. Default behavior rebuilds the current source before corpus execution:

```text
cargo build --manifest-path crates/orchestrator_local/Cargo.toml --bin orchestrator_local
```

When automatic build is disabled, an explicitly supplied binary must exist or the audit fails closed.

---

# 6. Per-run request contract

Generated requests contain:

```text
cmd=run.start
payload.kind=infer
payload.input
payload.task
payload.glossary
payload.tm
payload.maxNewTokens
payload.seed
payload.decodeSamplerPolicy
payload.decodeSampler01ReceiptPath
payload.candidatePoolSnapshotTopN
```

Typed policy remains the sampling parameter SSOT. Conflicting free-form sampling fields, salad parameter mutation, silent backend switch, and silent greedy fallback are forbidden.

---

# 7. Runtime route PASS

Sampled policies require:

```text
requested_sampled_decode=true
sampled_decode_applied=true
fallback_decode_mode=null
Sampler-01 route receipt pass=true
```

Greedy control requires:

```text
fallback_decode_mode=null
Sampler-01 route receipt pass=true
```

Any sampled route failure fails Sampler-02.

---

# 8. Loop analysis

Loop analysis uses generated suffix IDs only:

```text
generated_tail_ids=generated_ids[prompt_ids.len()..]
```

Metrics:

```text
tail_token_count
unique_token_count
unique_token_ratio
max_same_token_run
repeated_bigram_occurrence_count
repeated_trigram_occurrence_count
repeated_bigram_ratio
```

Loop reasons:

```text
same_token_run_ge_4
repeated_bigram_ratio_ge_0_35
unique_token_ratio_le_0_30
repeated_trigram_occurrence_ge_3
```

Only greedy loop cases enter the loop-break denominator:

```text
top_p_loop_break_rate=top_p_loop_break_count/greedy_loop_case_count
min_p_loop_break_rate=min_p_loop_break_count/greedy_loop_case_count
```

When greedy has no detected loop, the rates remain null rather than being guessed.

---

# 9. Sentence-surface preservation

Per output measure:

```text
char_count
non_whitespace_char_count
word_count
hangul_syllable_count
hangul_letter_ratio
replacement_character_count
control_character_count
max_same_char_run
terminal_punctuation_present
sentence_surface_score
sentence_surface_pass
```

Structural failure reasons include:

```text
surface_too_short
word_count_lt_2
replacement_character_present
control_character_present
same_char_run_ge_6
korean_surface_ratio_lt_0_25
token_loop_detected
```

A sampled regression is counted when greedy passes the structural surface gate and the sampled result fails it. This metric is not BLEU, COMET, semantic fidelity, or human preference.

---

# 10. Candidate-distribution health

When candidate snapshots exist, collect canonical numeric fields matching entropy, top-1 probability, and candidate count.

Metrics:

```text
snapshot_count
entropy_observation_count
mean_entropy
top1_probability_observation_count
mean_top1_probability
candidate_count_observation_count
mean_candidate_count
collapsed_step_count
```

A step is conservatively marked collapsed when observed evidence includes:

```text
top1_probability>=0.98
or
candidate_count<=1
```

Missing distribution evidence blocks automatic promotion but does not invalidate successful behavioral execution.

---

# 11. CPU-GPU parity evidence

Promotion-eligible runtime parity evidence requires:

```text
parity_gate_allowed=true
insufficient_evidence=false
```

Sampler-02 always records:

```text
exact_token_parity_executed=false
exact_token_parity_pass=null
```

Sampler-02 may PASS its evaluation contract while exact parity remains open. Default-policy promotion remains false when parity evidence is incomplete.

---

# 12. Behavioral comparison

A structural composite may be used only for relative triage:

```text
0.55*sentence_surface_score
+0.35*no_loop_score
+0.10*runtime_route_pass
```

A delta greater than 0.05 is required to mark a sampled policy better for a case.

Metrics:

```text
top_p_better_case_count
min_p_better_case_count
unchanged_case_count
```

The composite is not model-quality adjudication.

---

# 13. Promotion review

Statuses:

```text
review_recommends_candidate_promotion_not_applied
hold_no_default_promotion
```

Candidate recommendation requires:

```text
all runtime routes pass
sampled fallback count=0
sentence-surface pass rate>=0.80
sampled surface regression count=0
at least one behavioral improvement case
candidate-distribution evidence complete and healthy
runtime CPU-GPU parity evidence promotion-eligible
```

Even when review readiness becomes true, this patch does not apply promotion.

Required always false:

```text
model_quality_promotion_ready=false
production_decode_promotion_ready=false
```

---

# 14. PASS semantics

Patch PASS means:

```text
parent binding exact
corpus manifest valid
all corpus×policy runs executed
actual model-language artifacts observed
sampled routes applied without fallback
loop metrics emitted
sentence-surface metrics emitted
candidate-distribution evidence reported honestly
CPU-GPU parity evidence reported honestly
promotion review emitted
no default-policy mutation
no replacement-route mutation
no model-quality overclaim
```

Patch PASS does not require sampled output to be better than greedy. A poor result is valid measured evidence and must not be hidden as a tooling failure.

---

# 15. Safety and honesty

Required false:

```text
model_quality_claimed
translation_quality_claimed
korean_grammar_claimed
sft_alignment_claimed
production_decode_ready_claimed
```

Required zero:

```text
runtime_snapshot_mutation_count
runtime_context_replacement_count
replacement_active_route_mutation_count
default_route_mutation_count
route_registry_mutation_count
route_epoch_increment_count
production_replacement_execution_count
default_sampler_policy_mutation_count
model_weight_mutation_count
tokenizer_mutation_count
training_step_count
optimizer_step_count
```

---

# 16. Required predicates

```text
ASH_DECODE_SAMPLER_02_PARENT_BINDING_PASS
ASH_DECODE_SAMPLER_02_CORPUS_MANIFEST_VALID
ASH_DECODE_SAMPLER_02_THREE_POLICY_MATRIX_COMPLETE
ASH_DECODE_SAMPLER_02_ACTUAL_LANGUAGE_INFERENCE_EXECUTED
ASH_DECODE_SAMPLER_02_ALL_RUNTIME_ROUTES_PASS
ASH_DECODE_SAMPLER_02_NO_SAMPLED_FALLBACK
ASH_DECODE_SAMPLER_02_LOOP_BREAK_RATE_MEASURED
ASH_DECODE_SAMPLER_02_SENTENCE_SURFACE_MEASURED
ASH_DECODE_SAMPLER_02_PROMOTION_NOT_AUTO_APPLIED
ASH_DECODE_SAMPLER_02_MODEL_QUALITY_NOT_OVERCLAIMED
ASH_DECODE_SAMPLER_02_NO_REPLACEMENT_ROUTE_MUTATION
ASH_DECODE_SAMPLER_02_STATIC_CHECKS_PASS
```

---

# 17. Runtime outputs

```text
workspace/runtime/decode/
  ash_decode_sampler_02_corpus_manifest.json
  ash_decode_sampler_02_prompt_corpus_behavioral_gate_runtime_artifact.json
  ash_decode_sampler_02_parent_binding_receipt.json
  ash_decode_sampler_02_corpus_manifest_receipt.json
  ash_decode_sampler_02_execution_matrix_receipt.json
  ash_decode_sampler_02_policy_aggregate_receipt.json
  ash_decode_sampler_02_behavioral_comparison_receipt.json
  ash_decode_sampler_02_loop_break_rate_receipt.json
  ash_decode_sampler_02_sentence_surface_preservation_receipt.json
  ash_decode_sampler_02_candidate_distribution_health_receipt.json
  ash_decode_sampler_02_cpu_gpu_parity_evidence_receipt.json
  ash_decode_sampler_02_promotion_review_receipt.json
  ash_decode_sampler_02_model_quality_claim_guard.json
  ash_decode_sampler_02_replacement_route_guard.json
  ash_decode_sampler_02_static_checks.json
  ash_decode_sampler_02_verdict.json

  runs/<case>/<policy>/
    request.json
    stdout.jsonl
    stderr.log
    sampler01_route_receipt.json
    case_policy_result.json
```

---

# 18. Readiness

On patch PASS:

```text
prompt_corpus_behavioral_gate_ready=true
greedy_top_p_min_p_comparison_ready=true
loop_break_rate_measurement_ready=true
sentence_surface_measurement_ready=true
sampled_policy_promotion_review_complete=true
repository_ready_for_decode_sampler_03=true
```

Conditional:

```text
candidate_distribution_observation_ready
cpu_gpu_parity_observation_ready
sampled_decode_default_promotion_ready
```

Required false:

```text
cpu_gpu_exact_token_parity_ready=false
model_quality_promotion_ready=false
production_decode_promotion_ready=false
```

Next scope:

```text
decode_sampler_03_readiness_scope=sampled_policy_candidate_canary_and_cpu_gpu_exact_parity_closure_only
```

---

# 19. PASS and HOLD

PASS:

```text
PASS_ASH_DECODE_SAMPLER_02_PROMPT_CORPUS_EXECUTED_GREEDY_TOP_P_MIN_P_COMPARATIVE_EVALUATION_COMPLETED_LOOP_BREAK_RATE_MEASURED_SENTENCE_SURFACE_PRESERVATION_MEASURED_CANDIDATE_DISTRIBUTION_HEALTH_OBSERVED_CPU_GPU_PARITY_EVIDENCE_BOUND_SAMPLED_POLICY_PROMOTION_REVIEWED_NO_SILENT_GREEDY_FALLBACK_NO_DEFAULT_POLICY_PROMOTION_NO_MODEL_QUALITY_OVERCLAIM_NO_TENSORCUBE_REPLACEMENT_ROUTE_MUTATION_NO_PRODUCTION_REPLACEMENT
```

HOLD:

```text
HOLD_ASH_DECODE_SAMPLER_02_CORPUS_EXECUTION_ROUTE_RECEIPT_BEHAVIORAL_METRIC_OR_SAFETY_CONTRACT_INCOMPLETE
```

Recommended next patch:

```text
ASH-DECODE-SAMPLER-03
Sampled Policy Candidate Promotion /
Canary Profile /
Runtime Receipt /
CPU-GPU Exact Parity Closure /
Rollback Boundary /
No Production Default Switch Seal
```

---

# Final seal

Sampler-02 passes only when the repository can truthfully state:

```text
An immutable prompt corpus manifest owned the evaluation inputs.
The current orchestrator binary was rebuilt from current source.
Every corpus case ran under greedy, top-p, and top-p-plus-min-p.
The runs produced actual model-language output artifacts.
Typed sampled policies reached sampled decode without silent greedy fallback.
Generated suffix token IDs owned loop analysis.
Sentence-surface preservation was measured separately from loop break.
Candidate-distribution evidence was reported present or missing without invention.
Runtime CPU-GPU parity-gate evidence was bound when present.
Exact dual-backend token parity was not falsely claimed.
A poor sampled result remained valid evidence.
A favorable sampled result did not mutate the default policy.
No model-quality, translation-quality, grammar, SFT, or production-readiness claim was made.
No TensorCube replacement route, runtime snapshot, model weight, or tokenizer state changed.
No production replacement occurred.
```
