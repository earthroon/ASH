# ASH-DECODE-SAMPLER-01

## Active Inference Entrypoint Trace
## Generation Route SSOT
## Greedy-to-Sampled Policy Rebind
## Existing CPU Oracle Sampler Wiring
## Fixed-Seed Sampling Receipt
## Top-P-Only Baseline
## Min-P Incremental Probe
## No Silent Greedy Fallback
## No Model Quality Overclaim Seal

---

## 0. Patch identity

```text
patch_id=ASH-DECODE-SAMPLER-01
runtime_schema=ash.decode.sampler.01.active_route_rebind.runtime_artifact.v1
primary_artifact=workspace/runtime/decode/ash_decode_sampler_01_active_route_rebind_runtime_artifact.json
```

Repository safety parent:

```text
parent_patch_id=ASH-TCU-REPLACE-05
parent_schema=ash.tcu.replace.05.prepared_transition_store_audit.runtime_artifact.v1
parent_semantic_digest=8f07e8290afed460375f5d91d086ae017f9564e7181409cc9980acc01ef22c6f
parent_execution_digest=ee4ad94302bfa1b73656c750788057d4ed7025e17ee88a422ca8d1d202f8ddde
parent_spec_commit=859cd70fb1380b8e6c2706794b71ddaa6b98ed49
```

Parent safety state:

```text
repository_ready_for_replace_06=true
replace_06_readiness_scope=consumed_prepared_transition_apply_sandbox_contract_only
active_transition_apply_readiness=false
active_route_ownership_readiness=false
production_replacement_readiness=false
```

Primary code surfaces:

```text
crates/model_core/src/active_generation_route.rs
crates/model_core/src/generation_sampling.rs
crates/model_core/src/cpu_oracle_sampler.rs
crates/orchestrator_local/src/infer_entry.rs
crates/orchestrator_local/src/bin/ash_decode_sampler_01_active_route_audit.rs
```

---

# 1. Problem statement

ASH already contains a CPU oracle sampler with temperature, top-k, top-p, min-p, deterministic seed selection, transition-guard evaluation, explicit recovery modes, and candidate-set telemetry.

The blocking problem is not absence of a sampler. The blocking problem is route ownership and evidence:

```text
which inference entrypoint received the request
which typed policy owned the sampling parameters
whether free-form fields overrode that policy
whether the runtime requested sampled decode
whether sampled decode was actually applied
whether the runtime silently fell back to greedy or another backend
whether a selected token came from a clean sampled candidate set or a recovery path
```

A direct edit to `NativeWgpuModel::greedy_generate_legacy` is insufficient because that function is not proven to be the active user inference route for every request.

---

# 2. Evidence classes

R1 distinguishes three evidence classes.

## 2.1 Static active-entrypoint binding

The Cargo audit inspects the orchestrator source and proves that the typed sampler policy is bound at:

```text
orchestrator_local::infer_entry::handle_infer_run
→ runtime::run_standard_infer_with_decode
```

Evidence status:

```text
static_source_binding_not_language_inference_execution
```

This does not prove that a real model request ran.

## 2.2 Executed synthetic CPU-oracle probe

The Cargo audit executes the existing `sample_with_cpu_oracle` function using deterministic synthetic logits.

Evidence status:

```text
executed_synthetic_logits
```

This proves sampler mechanics, fixed-seed replay, top-p/min-p separation, and recovery classification. It does not prove model-language quality.

## 2.3 Runtime request receipt

A real orchestrator inference request carrying `decodeSamplerPolicy` emits:

```text
ash_decode_sampler_01_active_route_receipt.json
```

Evidence status:

```text
runtime_result_observed
```

The current `StandardInferResult` summary proves requested/applied sampled decode and fallback mode. It does not expose a per-step CPU-vs-GPU selected-token source, so the receipt must state:

```text
selected_sampler_backend_evidence_status=runtime_summary_does_not_expose_step_source
cpu_oracle_active_runtime_proven=false
```

No artifact may silently upgrade this to active CPU-oracle execution proof.

---

# 3. Generation route SSOT

Introduce typed policy and route identities in `model_core::active_generation_route`.

## 3.1 Policy IDs

```rust
pub enum DecodeSamplerPolicyId {
    GreedyControl,
    TopPOnlyBaseline,
    TopPMinPProbe,
}
```

Canonical wire names:

```text
greedy_control
top_p_only_baseline
top_p_min_p_probe
```

## 3.2 Entrypoints

```rust
pub enum GenerationEntrypoint {
    StandardInfer,
    StandardInferWithDecodePolicy,
    NativeWgpuDirect,
    TensorCubeDecodeAudit,
    SamplerAudit,
    UnitTest,
}
```

## 3.3 Model backend identity

```rust
pub enum GenerationModelBackend {
    ReferenceModel,
    NativeWgpuModel,
    SyntheticLogitFixture,
}
```

Synthetic fixtures must never be labeled as actual model execution.

## 3.4 Generation function identity

```rust
pub enum GenerationFunction {
    ReferenceGreedy,
    ReferenceSampledCpuOracle,
    NativeWgpuLegacyGreedy,
    NativeWgpuCachedGreedy,
    NativeWgpuCachedSampledCpuOracle,
    NativeWgpuStreamingSampledCpuOracle,
    SyntheticGreedyControl,
    SyntheticCpuOracleProbe,
}
```

## 3.5 Sampler backend identity

```rust
pub enum GenerationSamplerBackend {
    GreedyArgmax,
    CpuOracleSampler,
}
```

The active generation route decision must have exactly one owner:

```text
generation_route_owner_count=1
```

A sampled policy resolving to `GreedyArgmax` fails with:

```text
SampledPolicyResolvedToGreedy
```

---

# 4. Typed request policy

The orchestrator accepts:

```text
decodeSamplerPolicy
```

or:

```text
decode_sampler_policy
```

The typed policy is the sampling parameter SSOT whenever present.

## 4.1 Greedy control

```text
temperature=0.0
top_k=0
top_p=1.0
min_p=0.0
```

## 4.2 Top-p-only baseline

```text
temperature=0.80
top_k=0
top_p=0.90
min_p=0.0
seed=request-owned fixed seed
```

## 4.3 Top-p plus min-p probe

```text
temperature=0.80
top_k=0
top_p=0.90
min_p=0.05
seed=same request-owned fixed seed
```

The top-p baseline and min-p probe must differ in exactly one canonical field:

```text
min_p_probe_config_difference_count=1
min_p_probe_changed_field=min_p
```

---

# 5. Free-form conflict gate

When a typed policy is present, conflicting free-form values are forbidden.

Checked free-form surfaces include:

```text
temperature
topP / top_p
topK / top_k
minP / min_p / samplingMinP / sampling_min_p
```

Required:

```text
freeform_parameter_conflict_count=0
```

Any mismatch fails before inference:

```text
ASH-DECODE-SAMPLER-01 typed policy conflicts with N free-form sampler field(s)
```

No last-write-wins behavior is permitted.

---

# 6. Existing CPU oracle reuse

The patch must call the existing function:

```rust
sample_with_cpu_oracle(logits, config, context)
```

It must not introduce a second top-p or min-p implementation.

Required static counts:

```text
existing_cpu_oracle_direct_wiring_count=1
duplicate_top_p_implementation_count=0
duplicate_min_p_implementation_count=0
```

The existing sampler remains the algorithm SSOT for:

```text
temperature scaling
banned-token filtering
early blocked EOS filtering
optional semantic-prior handling
transition guard handling
top-k cutoff
min-p cutoff
softmax normalization
top-p cutoff
post-cut renormalization
fixed-seed deterministic draw
explicit recovery
```

---

# 7. Experiment isolation

The top-p baseline changes sampling selection policy only.

Required zero changes:

```text
repetition_penalty_change_count=0
semantic_prior_mutation_count=0
transition_penalty_activation_change_count=0
morphological_penalty_activation_count=0
qwave_sampler_mutation_count=0
candidate_rerank_mutation_count=0
```

Existing salad retry logic must not alter temperature, top-p, top-k, or min-p for a typed sampler-policy request.

Required source contract:

```text
salad retry may execute only when typed sampler policy is absent
```

EOS safety reruns may preserve and rebind the typed decode override, but may not silently switch policy.

---

# 8. Fixed-seed contract

Canonical seed chain:

```text
request seed
→ typed policy override seed
→ GenerationSamplingConfig.seed
→ CpuOracleContext.seed
→ sampling receipt seed
```

Synthetic audit seed:

```text
424242
```

For identical logits, context, policy, and seed:

```text
fixed_seed_output_mismatch_count=0
fixed_seed_step_receipt_mismatch_count=0
```

The seed must enter policy, route, and step digests.

---

# 9. Effective sampled step

A step counts as genuinely sampled only when all conditions hold:

```text
sampler_applied=true
apply_mode=cpu_oracle_sampler
active_softmax_renormalized=true
candidate_empty_recovered=false
recovery_mode=null
active_count_after_top_p>0
```

Canonical helper:

```rust
pub fn effective_sampled_step(
    result: &CpuOracleSampleResult,
) -> bool
```

The following must not pass as clean sampling:

```text
sampler_applied=true with candidate recovery
active-top1 recovery
valid-global-top1 recovery
empty-logits recovery
no-candidate-after-guard recovery
no-candidate-after-min-p recovery
no-candidate-after-top-p recovery
```

---

# 10. Recovery and fallback

Recovery is observable evidence, not clean baseline success.

A negative fixture must ban all synthetic candidates and prove:

```text
candidate_empty_recovered=true
effective_sampled_step=false
```

Clean top-p and min-p runs require:

```text
clean_top_p_recovery_count=0
clean_min_p_recovery_count=0
```

For a real typed sampled request, the orchestrator requires:

```text
requested_sampled_decode=true
sampled_decode_applied=true
fallback_decode_mode=null
```

Otherwise it writes the runtime route receipt and fails closed:

```text
ASH-DECODE-SAMPLER-01 sampled route failed closed
```

No sampled request may silently become:

```text
cpu_greedy_fallback
cpu_greedy_16AC_safe_generation
greedy legacy route
unreceipted backend switch
```

---

# 11. Runtime route receipt

Schema:

```text
ash.decode.sampler.01.active_inference_route_receipt.v1
```

Required fields:

```text
patch_id
request_id
request_entrypoint
runtime_entrypoint
model_backend
requested_sampler_policy
resolved_sampler_policy
temperature
top_k
top_p
min_p
seed
freeform_parameter_conflict_count
requested_sampled_decode
sampled_decode_applied
fallback_decode_mode
route_evidence_status
selected_sampler_backend_evidence_status
cpu_oracle_active_runtime_proven
fallback_allowed
no_silent_greedy_fallback
model_quality_claimed
model_quality_status
pass
```

The receipt proves route application and fallback truth. It does not claim language quality.

---

# 12. Synthetic route audit

The Cargo audit uses:

```text
entrypoint=sampler_audit
model_backend=synthetic_logit_fixture
generation_function=synthetic_cpu_oracle_probe
```

It must not label synthetic logits as `StandardInfer` or `NativeWgpuModel` execution.

Required runs:

```text
GreedyControl once
TopPOnlyBaseline twice with same seed
TopPMinPProbe twice with same seed
recovery negative fixture once
```

Required results:

```text
greedy effective sampled step=false
both top-p steps effective sampled=true
both min-p steps effective sampled=true
fixed-seed mismatch counts=0
clean recovery counts=0
negative recovery fixture effective sampled=false
```

---

# 13. Behavior and quality boundary

The synthetic Cargo audit has no language surface and must report:

```text
behavior_observation=insufficient_evidence
reason=synthetic_logit_route_probe_only_no_language_surface_adjudication
loop_break_claimed=false
sentence_surface_claimed=false
```

Every artifact must report:

```text
model_quality_claimed=false
model_quality_status=not_adjudicated_sampler_route_probe_only
translation_quality_claimed=false
korean_grammar_claimed=false
sft_alignment_claimed=false
production_decode_ready_claimed=false
```

A later real prompt probe may classify:

```text
A loop broken and sentence surface observed
B loop broken but sentence surface not observed
C sampling applied and loop persists
D sampled policy not applied
E recovery or fallback observed
```

Sampler-01 itself does not adjudicate those outcomes from synthetic logits.

---

# 14. Replacement-chain isolation

Generation sampling route and TensorCube replacement route are separate domains.

Required zero values:

```text
runtime_snapshot_mutation_count=0
runtime_context_replacement_count=0
replacement_active_route_mutation_count=0
default_route_mutation_count=0
route_registry_mutation_count=0
route_epoch_increment_count=0
production_replacement_execution_count=0
```

Weight and tokenizer safety:

```text
model_weight_mutation_count=0
optimizer_step_count=0
training_step_count=0
tokenizer_manifest_mutation_count=0
vocabulary_mutation_count=0
```

---

# 15. Required predicates

```text
ASH_DECODE_SAMPLER_01_PARENT_BINDING_PASS
ASH_DECODE_SAMPLER_01_ACTIVE_ENTRYPOINT_TRACED
ASH_DECODE_SAMPLER_01_ROUTE_SINGLE_OWNER
ASH_DECODE_SAMPLER_01_EXISTING_CPU_ORACLE_REUSED
ASH_DECODE_SAMPLER_01_TOP_P_BASELINE_EXACT
ASH_DECODE_SAMPLER_01_MIN_P_PROBE_EXACT
ASH_DECODE_SAMPLER_01_MIN_P_ONLY_DIFFERENCE
ASH_DECODE_SAMPLER_01_FIXED_SEED_REPLAY
ASH_DECODE_SAMPLER_01_EFFECTIVE_SAMPLING_PROVEN
ASH_DECODE_SAMPLER_01_NO_SILENT_GREEDY_FALLBACK
ASH_DECODE_SAMPLER_01_MODEL_QUALITY_NOT_ADJUDICATED
ASH_DECODE_SAMPLER_01_NO_REPLACEMENT_ROUTE_MUTATION
ASH_DECODE_SAMPLER_01_STATIC_CHECKS_PASS
```

`ACTIVE_ENTRYPOINT_TRACED` means the active entrypoint contract is statically bound in the audit. It does not mean a real model generation was executed by the Cargo audit.

---

# 16. Required runtime outputs

```text
workspace/runtime/decode/
  ash_decode_sampler_01_active_route_rebind_runtime_artifact.json
  ash_decode_sampler_01_parent_binding_receipt.json
  ash_decode_sampler_01_active_entrypoint_trace.json
  ash_decode_sampler_01_generation_route_decision.json
  ash_decode_sampler_01_route_environment_receipt.json
  ash_decode_sampler_01_greedy_control_config.json
  ash_decode_sampler_01_top_p_baseline_config.json
  ash_decode_sampler_01_min_p_probe_config.json
  ash_decode_sampler_01_config_difference_audit.json
  ash_decode_sampler_01_fixed_seed_replay_receipt.json
  ash_decode_sampler_01_greedy_control_run_receipt.json
  ash_decode_sampler_01_top_p_baseline_run_receipt.json
  ash_decode_sampler_01_min_p_probe_run_receipt.json
  ash_decode_sampler_01_effective_sampling_audit.json
  ash_decode_sampler_01_recovery_and_fallback_audit.json
  ash_decode_sampler_01_behavior_observation_receipt.json
  ash_decode_sampler_01_model_quality_claim_guard.json
  ash_decode_sampler_01_runtime_snapshot_guard.json
  ash_decode_sampler_01_replacement_route_guard.json
  ash_decode_sampler_01_weight_and_tokenizer_guard.json
  ash_decode_sampler_01_static_checks.json
  ash_decode_sampler_01_verdict.json
```

Real inference requests additionally emit:

```text
ash_decode_sampler_01_active_route_receipt.json
```

at the request-configured or workspace-default path.

---

# 17. Readiness

Cargo audit PASS readiness:

```text
active_inference_entrypoint_trace_ready=true
active_inference_trace_evidence_status=static_source_binding
active_language_inference_execution_proven=false

generation_route_ssot_ready=true
cpu_oracle_sampler_wiring_ready=true
cpu_oracle_probe_evidence_status=executed_synthetic_logits
fixed_seed_sampling_ready=true
top_p_baseline_ready=true
min_p_probe_ready=true
no_silent_greedy_fallback_ready=true
```

Promotion remains false:

```text
sampled_decode_default_promotion_ready=false
model_quality_promotion_ready=false
production_decode_promotion_ready=false
```

Next review scope:

```text
repository_ready_for_decode_sampler_02=true
decode_sampler_02_readiness_scope=prompt_corpus_behavioral_gate_and_sampled_decode_promotion_review_only
```

This readiness opens a corpus evaluation, not production sampled-decode promotion.

---

# 18. Static checks

Required:

```text
generation_route_owner_count=1
existing_cpu_oracle_direct_wiring_count=1
typed_policy_parser_owner_count=1
typed_policy_override_owner_count=1
silent_greedy_fallback_guard_count>=1
legacy_argmax_replaced_count=0
duplicate_top_p_implementation_count=0
duplicate_min_p_implementation_count=0
```

Module hashes must be recorded for:

```text
cpu_oracle_sampler.rs
generation_sampling.rs
active_generation_route.rs
infer_entry.rs
```

Physical paths, timestamps, process IDs, and output directories are excluded from semantic digests.

---

# 19. Tests

Required model-core tests:

```text
top_p_baseline_uses_cpu_oracle_and_is_effective
fixed_seed_is_deterministic
min_p_probe_differs_only_by_min_p
candidate_recovery_is_not_effective_sampling
```

Required integration behavior:

```text
typed top-p policy produces exact override
typed min-p policy changes only min_p
typed policy rejects conflicting free-form fields
typed policy disables salad parameter retry
sampled runtime fallback fails closed
runtime receipt records fallback truth
greedy control remains explicit
```

---

# 20. PASS and HOLD

PASS marker:

```text
PASS_ASH_DECODE_SAMPLER_01_ACTIVE_INFERENCE_ENTRYPOINT_TRACE_CONTRACT_BOUND_GENERATION_ROUTE_SSOT_ESTABLISHED_GREEDY_TO_SAMPLED_POLICY_REBOUND_EXISTING_CPU_ORACLE_SAMPLER_WIRED_SYNTHETIC_LOGIT_PROBE_EXECUTED_FIXED_SEED_SAMPLING_REPLAY_PROVEN_TOP_P_ONLY_BASELINE_EXECUTED_MIN_P_INCREMENTAL_PROBE_EXECUTED_EFFECTIVE_SAMPLED_STEPS_PROVEN_NO_CANDIDATE_RECOVERY_NO_SILENT_GREEDY_FALLBACK_NO_SILENT_BACKEND_SWITCH_BEHAVIOR_OBSERVED_WITHOUT_MODEL_QUALITY_OVERCLAIM_NO_TENSORCUBE_REPLACEMENT_ROUTE_MUTATION_NO_PRODUCTION_REPLACEMENT
```

HOLD marker:

```text
HOLD_ASH_DECODE_SAMPLER_01_ACTIVE_ROUTE_SAMPLER_APPLICATION_FIXED_SEED_RECOVERY_OR_EXPERIMENT_ISOLATION_INCOMPLETE
```

Recommended next patch:

```text
ASH-DECODE-SAMPLER-02
Prompt Corpus Behavioral Gate /
Greedy-vs-Top-P-vs-Min-P Comparative Evaluation /
Loop-Break Rate /
Sentence-Surface Preservation /
Candidate Distribution Health /
CPU-GPU Sampled Decode Parity /
Sampled Policy Promotion Review /
No Production Quality Overclaim Seal
```

---

# Final seal

Sampler-01 passes only when the repository can truthfully state:

```text
The active orchestrator inference entrypoint has a typed sampler-policy binding.

The typed policy is the sampling-parameter SSOT.

Conflicting free-form sampling fields fail closed.

The existing CPU oracle sampler is reused.

No duplicate top-p or min-p implementation was added.

Top-p-only and top-p-plus-min-p profiles are distinct and deterministic.

The min-p probe changes only min-p.

Candidate recovery cannot pass as a clean sampled step.

A sampled runtime request cannot silently fall back to greedy.

The Cargo audit executed synthetic logits, not a language model.

The Cargo audit does not claim active CPU-oracle model execution.

A real runtime receipt records requested/applied sampling and fallback truth.

The current runtime summary does not expose per-step CPU-vs-GPU source, and the receipt says so.

No model quality, translation quality, Korean grammar, SFT alignment, or production readiness claim is made.

No repetition-penalty change is mixed into the top-p baseline.

No morphological, QWave, rerank, or rollback mutation is activated.

No TensorCube runtime snapshot or replacement route changes.

No model weights or tokenizer state change.

No production replacement occurs.
```
