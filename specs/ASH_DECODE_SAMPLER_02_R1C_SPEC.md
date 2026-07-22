# ASH-DECODE-SAMPLER-02-R1C

## Greedy-Control Contamination Gate /
## Raw Argmax and Selected Token Identity /
## Selector-Rerank-Safety Intervention Accounting /
## Sampled Backend Non-Entry /
## Greedy Purity Verdict Seal

---

## 0. Identity and parent binding

```text
patch_id=ASH-DECODE-SAMPLER-02-R1C
parent_patch_id=ASH-DECODE-SAMPLER-02-R1B
runtime_schema=ash.decode.sampler.02.r1c.greedy_control_contamination.runtime_artifact.v1
primary_artifact=workspace/runtime/decode/ash_decode_sampler_02_r1c_greedy_control_contamination_runtime_artifact.json
local_manifest=workspace/runtime/decode/ash_decode_sampler_02_r1c_local_manifest.json
parent_r1a_spec_commit=6e5f461dd036e9a05a63977f3acb0a2d46cd6e4d
parent_r1b_spec_commit=782aad4b002f4b7d2c7a5c4b8b4eb5329f826d21
parent_r1b_archive_sha256=0d368f1ef9adc523d031675c06b9e07be361bb4c1a831a8a141659e30b604f55
```

R1C must hash-validate the R1A and R1B parent manifests and their referenced primary artifacts. Copied PASS strings are not evidence.

---

## 1. Current-source truth

R1A established typed sampling ownership. R1B proved zero mutation of typed-policy locked scalar fields. R1C closes the remaining token-authority gap.

Current decode surfaces include raw argmax, GPU adjusted argmax, structure rerank, QW-54F rerank, QW-55A selector, sampled backends, CPU oracle paths, recovery/fallback paths, and post-commit repetition-guard replacement. Existing telemetry does not prove the complete chain:

```text
raw model argmax
-> hard-safety-authorized argmax
-> post-soft-penalty argmax
-> post-rerank top1
-> selector-selected token
-> committed token
-> emitted token
```

Runtime also currently risks classifying typed `greedy_control` as sampled when it checks whether optional scalar fields are present. Canonical greedy values are present as `Some(0.0)`, `Some(1.0)`, `Some(0)`, and `Some(0.0)`, so execution mode must be derived from typed policy identity, not `Option::is_some()`.

---

## 2. Purpose

For every typed `GreedyControl` step, R1C proves:

```text
execution_mode=greedy_control
requested_sampled_decode=false
sampled_decode_applied=false
raw_argmax_evidence_present=true
selector_selected_token_id=hard_safety_authorized_argmax_token_id
committed_token_id=selector_selected_token_id
sampled_backend_entry_count=0
cpu_oracle_sampler_entry_count=0
sampled_recovery_entry_count=0
legacy_fallback_entry_count=0
forbidden_soft_intervention_entry_count=0
forbidden_rerank_entry_count=0
forbidden_selector_entry_count=0
```

Allowed hard safety may change the authorized token only with explicit provenance. Post-commit safety replacement must preserve selector identity and record the emitted token separately.

---

## 3. Typed execution-mode SSOT

Add to `model_core`:

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum DecodeExecutionMode {
    GreedyControl,
    Sampled,
    LegacyGreedy,
    LegacySampled,
}

pub fn resolve_decode_execution_mode(
    sampling: &GenerationSamplingConfig,
) -> Result<DecodeExecutionMode>;
```

Resolution:

```text
TypedPolicyFinal + GreedyControl        -> GreedyControl
TypedPolicyFinal + TopPOnlyBaseline     -> Sampled
TypedPolicyFinal + TopPMinPProbe        -> Sampled
no typed policy + sampled scalar values -> LegacySampled
no typed policy + greedy scalar values  -> LegacyGreedy
```

Forbidden:

```text
greedy_control -> generate_with_sampling_* -> internal greedy delegation
```

An accidental typed-greedy sampled entrypoint must fail closed with `GreedyControlSampledEntrypointObserved`.

---

## 4. Raw greedy authority boundary

The raw authority is the model/backend last-logits row after model-forward and attached adapters, but before decode-side masks, repetition penalties, GPU penalties, structure/QW reranks, explicit selectors, sampling, fallback, or output replacement.

Typed greedy must preserve the raw logits snapshot, apply only provenance-backed hard-safety masks to a separate selection surface, and compare the two argmax identities.

Allowed hard safety:

```text
banned-token hard mask
minimum-new-token EOS hard block
post-commit repetition-guard EOS replacement
stop-sequence termination without token replacement
```

Forbidden passing-route interventions:

```text
repetition penalty
GPU penalty pass
structure candidate rerank
QW-54F recent-token rerank
QW-55A explicit selector
GPU sampler
CPU oracle sampler
sampler strict demotion
sampled recovery
legacy sampled fallback
```

A forbidden route contaminates greedy purity even when it returns the same token as raw argmax.

---

## 5. Canonical telemetry

Add canonical enums and receipts in `model_core::greedy_control_purity`:

```text
GreedySelectionBackend
GreedyInterventionClass
GreedyInterventionKind
GreedyInterventionReceipt
GreedyStepPurityVerdict
GreedyStepPurityReceipt
GreedyRunPurityVerdict
GreedyRunPuritySummary
BannedTokenReason
BannedTokenProvenanceEntry
```

Required step identities:

```text
raw_argmax_token_id
raw_argmax_logit
raw_argmax_source
hard_safety_authorized_argmax_token_id
post_soft_penalty_argmax_token_id
post_rerank_top1_token_id
selector_selected_token_id
committed_token_id
emitted_token_id
```

Step verdicts:

```text
greedy_pure_raw_argmax
greedy_pure_hard_safety_intervention
greedy_pure_post_commit_safety_stop
greedy_contaminated_soft_penalty
greedy_contaminated_rerank
greedy_contaminated_explicit_selector
greedy_contaminated_sampled_backend
greedy_contaminated_recovery_fallback
greedy_route_identity_mismatch
greedy_evidence_missing
```

Run verdicts:

```text
greedy_verified
greedy_verified_with_hard_safety
greedy_verified_with_post_commit_safety_stop
greedy_contaminated
greedy_evidence_missing
not_greedy_control
```

Route purity and token-identity purity are separate booleans. A soft intervention makes route purity false even when token identity remains unchanged.

---

## 6. Dedicated production route

Typed greedy must use a dedicated authority path:

```text
model forward
-> preserve raw logits
-> derive EOS/request ban provenance
-> apply hard-safety masks only
-> raw argmax and safety-authorized argmax
-> classify greedy step
-> commit selector token
-> account post-commit replacement
```

Required production functions include:

```text
resolve_decode_execution_mode
apply_greedy_control_hard_safety_masks
select_greedy_control_token_with_hard_safety
classify_greedy_step
summarize_greedy_run
record_post_commit_safety_override
```

Typed greedy must fail closed when structure routing, GPU penalty coefficients, QW-55A, sampled wrappers, CPU oracle, recovery, or fallback enter the authority route. Legacy and sampled policies retain their existing behavior.

---

## 7. Runtime and orchestrator propagation

`GenerationTelemetry`, `StandardInferResult`, and `StandardInferCandidateOutput` must propagate:

```text
decode_execution_mode
greedy_step_purity_receipts
greedy_run_purity_summary
sampled_backend_entry_count
cpu_oracle_sampler_entry_count
sampled_recovery_entry_count
legacy_fallback_entry_count
```

The orchestrator route receipt remains externally flat but is internally assembled through Atlas parallel groups:

```text
identity
policy_scalars
ownership
structure_bias
route_evidence
execution_mode
greedy_authority
sampled_backend_non_entry
invariants
verdict
```

Runtime evidence must be consumed directly. Request-side reconstruction of greedy purity is forbidden.

---

## 8. Post-commit safety accounting

When repetition guard replaces a committed token with EOS:

```text
selector_selected_token_id=<greedy authority token>
committed_token_id=<greedy authority token>
emitted_token_id=<EOS>
intervention=repetition_guard_eos_replacement
```

This may yield `greedy_pure_post_commit_safety_stop` only when the replacement is provenance-backed. Unrecorded output replacement fails with `GreedyPostCommitOverrideUnaccounted`.

---

## 9. Local Rust audit gate

Add binary:

```text
ash_decode_sampler_02_r1c_greedy_control_contamination_gate
```

Arguments:

```text
--repo-root
--r1a-parent-artifact
--r1a-parent-manifest
--r1b-parent-artifact
--r1b-parent-manifest
--out-dir
```

The gate does not require a model or checkpoint. It uses the same production execution-mode resolver and purity classifier against a deterministic 32-case matrix:

```text
8 execution-mode identity cases
8 positive greedy-control cases
16 contamination/evidence negative controls
```

Negative controls must include same-token soft penalty, changed-token soft penalty, GPU penalty, structure rerank, QW-54F, QW-55A, GPU sampler, CPU oracle, sampled recovery, legacy fallback, missing raw evidence, missing safety provenance, and unaccounted post-commit replacement.

Rust creates the runtime artifact, all receipts, per-case outputs, verdict, and local manifest under `workspace/runtime/decode`. Generated files are not committed or baked into the source ZIP.

---

## 10. PASS formula

```text
PASS =
  r1a_parent_binding_pass
  && r1b_parent_binding_pass
  && compile_truth_pass
  && typed_execution_mode_ssot_present
  && greedy_control_requested_sampled_decode_false
  && greedy_control_sampled_decode_applied_false
  && greedy_control_sampled_wrapper_entry_count==0
  && raw_argmax_evidence_missing_count==0
  && safety_provenance_missing_count==0
  && selector_authorized_argmax_mismatch_count==0
  && committed_selector_mismatch_count==0
  && unaccounted_post_commit_override_count==0
  && sampled_backend_entry_count==0
  && cpu_oracle_sampler_entry_count==0
  && sampled_recovery_entry_count==0
  && legacy_fallback_entry_count==0
  && forbidden_soft_intervention_entry_count==0
  && forbidden_rerank_entry_count==0
  && forbidden_selector_entry_count==0
  && negative_control_unexpected_pass_count==0
  && default_sampler_policy_mutation_count==0
  && model_quality_claim_count==0
```

PASS does not claim model quality, unbiased logits, sampled-policy inferiority, minimum-new-token EOS final ownership, checkpoint/model/tokenizer binding, persistent sessions, single model load, or production promotion.

---

## 11. Canonical failures

```text
R1AParentEvidenceIncomplete
R1BParentEvidenceIncomplete
GreedyExecutionModeIdentityMismatch
GreedyControlMisclassifiedAsSampledRequest
GreedyControlSampledEntrypointObserved
GreedyRawArgmaxEvidenceMissing
GreedyRawArgmaxNonFinite
GreedySafetyProvenanceMissing
GreedySelectorAuthorizedArgmaxMismatch
GreedyCommittedSelectorMismatch
GreedySoftPenaltyInterventionObserved
GreedyStructureRerankInterventionObserved
GreedyQw54fRerankInterventionObserved
GreedyQw55aSelectorInterventionObserved
GreedySampledBackendEntryObserved
GreedyCpuOracleSamplerEntryObserved
GreedySampledRecoveryObserved
GreedyLegacyFallbackObserved
GreedyPostCommitOverrideUnaccounted
GreedyPurityReceiptMissing
GreedyRunPuritySummaryMissing
RuntimeGreedyEvidenceMissing
CompileTruthMissing
```

---

## 12. Code surfaces

```text
crates/model_core/src/decode_sampling_policy.rs
crates/model_core/src/decode_state.rs
crates/model_core/src/generation_sampling.rs
crates/model_core/src/generation_telemetry.rs
crates/model_core/src/greedy_control_purity.rs
crates/model_core/src/native_wgpu.rs
crates/model_core/src/lib.rs
crates/runtime/src/infer.rs
crates/runtime/src/infer/candidate_output.rs
crates/orchestrator_local/src/infer_entry.rs
crates/orchestrator_local/src/bin/ash_decode_sampler_02_r1c_greedy_control_contamination_gate.rs
crates/orchestrator_local/Cargo.toml
```

Do not create a second policy scalar table. Model core owns token authority. Orchestrator owns coordination and receipts.

---

## 13. Build and run

```powershell
cargo fmt --all -- --check
cargo check --manifest-path crates/model_core/Cargo.toml
cargo check --manifest-path crates/runtime/Cargo.toml
cargo check --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_decode_sampler_02_r1c_greedy_control_contamination_gate

cargo run --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_decode_sampler_02_r1c_greedy_control_contamination_gate `
  -- `
  --repo-root . `
  --r1a-parent-artifact workspace/runtime/decode/ash_decode_sampler_02_r1a_typed_policy_final_sampling_ownership_runtime_artifact.json `
  --r1a-parent-manifest workspace/runtime/decode/ash_decode_sampler_02_r1a_local_manifest.json `
  --r1b-parent-artifact workspace/runtime/decode/ash_decode_sampler_02_r1b_structure_sampling_bias_suppression_runtime_artifact.json `
  --r1b-parent-manifest workspace/runtime/decode/ash_decode_sampler_02_r1b_local_manifest.json `
  --out-dir workspace/runtime/decode
```

Expected PASS token:

```text
PASS_ASH_DECODE_SAMPLER_02_R1C_GREEDY_CONTROL_EXECUTION_MODE_SSOT_RAW_ARGMAX_SELECTED_TOKEN_IDENTITY_SELECTOR_RERANK_SAFETY_INTERVENTION_ACCOUNTING_SAMPLED_BACKEND_NON_ENTRY_GREEDY_PURITY_VERDICT_NO_DEFAULT_MUTATION_NO_MODEL_QUALITY_OVERCLAIM
```

Expected outputs:

```text
primary_artifact=workspace/runtime/decode/ash_decode_sampler_02_r1c_greedy_control_contamination_runtime_artifact.json
manifest=workspace/runtime/decode/ash_decode_sampler_02_r1c_local_manifest.json
```

On PASS:

```text
status=PASS
ready_for_sampler_02_r1d=true
ready_for_sampler_02_r1d_scope=minimum_new_token_eos_single_owner_guard
ready_for_default_sampler_policy_promotion=false
ready_for_production_decode_promotion=false
```
