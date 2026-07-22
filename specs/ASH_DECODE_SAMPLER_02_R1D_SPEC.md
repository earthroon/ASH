# ASH-DECODE-SAMPLER-02-R1D

## Minimum-New-Token EOS Single-Owner Guard /
## Sampler-Transition EOS Authority /
## EOS03 and EOS03A Shadow-Parity Rebind /
## No Rerun Policy Mutation /
## Duplicate EOS Ownership Zero Seal

---

# 0. Patch identity

```text
patch_id=ASH-DECODE-SAMPLER-02-R1D
parent_patch_id=ASH-DECODE-SAMPLER-02-R1C
patch_class=decode_eos_transition_authority_hardening
runtime_schema=ash.decode.sampler.02.r1d.minimum_new_token_eos_single_owner.runtime_artifact.v1
primary_artifact=workspace/runtime/decode/ash_decode_sampler_02_r1d_minimum_new_token_eos_single_owner_runtime_artifact.json
local_manifest=workspace/runtime/decode/ash_decode_sampler_02_r1d_local_manifest.json
r1a_spec_commit=6e5f461dd036e9a05a63977f3acb0a2d46cd6e4d
r1b_spec_commit=782aad4b002f4b7d2c7a5c4b8b4eb5329f826d21
r1c_spec_commit=348f39b410bea042781ba19aa79b65b3cc950bf7
parent_r1c_archive_sha256=125ffd45c739174197ab2030dbaae6423fb6039dfc59e37eab8b55beeee4957c
```

Required parent evidence:

```text
workspace/runtime/decode/ash_decode_sampler_02_r1a_typed_policy_final_sampling_ownership_runtime_artifact.json
workspace/runtime/decode/ash_decode_sampler_02_r1a_local_manifest.json
workspace/runtime/decode/ash_decode_sampler_02_r1b_structure_sampling_bias_suppression_runtime_artifact.json
workspace/runtime/decode/ash_decode_sampler_02_r1b_local_manifest.json
workspace/runtime/decode/ash_decode_sampler_02_r1c_greedy_control_contamination_runtime_artifact.json
workspace/runtime/decode/ash_decode_sampler_02_r1c_local_manifest.json
```

The R1D audit gate must hash-validate all parent manifests and their referenced primary artifacts. Copied PASS strings are not evidence.

---

# 1. Current-source truth

Before R1D, minimum-new-token EOS responsibility is distributed across several executable surfaces:

```text
decode_transition_guard threshold comparison
decode_state step-local EOS ban construction
R1C greedy hard-safety local EOS boolean
EOS03 request-wide EOS ban plus second inference
EOS03A suppression/restore receipt marked as enforcement
post-commit repetition-guard EOS replacement
```

This produces more than one component capable of deciding whether EOS may be selected, committed, or emitted.

Current pre-R1D truth:

```text
minimum_new_token_eos_authority_count>1
transition_threshold_source_count>1
step_local_eos_ban_owner_present=true
greedy_local_eos_guard_boolean_present=true
orchestrator_eos_rerun_owner_present=true
orchestrator_hardcoded_eos_token_id_present=true
post_commit_eos_materialization_owner_present=true
eos03_shadow_only=false
eos03a_shadow_only=false
no_rerun_policy_mutation_proven=false
duplicate_eos_ownership_zero_proven=false
```

Stop-sequence termination may also consume `min_new_tokens`, but it is not EOS eligibility ownership and remains a separate concern.

---

# 2. Purpose and ownership boundary

R1D establishes exactly one executable owner:

```text
SamplerTransitionEosAuthority
```

Canonical flow:

```text
request min_new_tokens
+ active transition profile floor
-> immutable EOS run contract
-> step-local EOS eligibility decision
-> greedy or sampled selection mask
-> post-commit EOS materialization decision
-> finish-reason legality
-> runtime telemetry
-> EOS01/EOS03/EOS03A shadow verification
```

Required final ownership truth:

```text
minimum_new_token_eos_authority_count=1
duplicate_eos_owner_count=0
orchestrator_eos_enforcement_count=0
eos_guard_rerun_count=0
request_wide_eos_ban_for_min_new_tokens_count=0
```

---

# 3. Scope

In scope:

```text
canonical threshold resolution
single EOS run contract
selection-time EOS eligibility
step-local mask derivation
transition-reason derivation
R1C hard-safety provenance binding
sampled-path authority binding
post-commit EOS replacement authorization
finish-reason legality
EOS01/EOS03/EOS03A shadow-only rebind
no EOS rerun
no rerun policy mutation
duplicate-owner static and runtime gates
local Rust audit matrix
local receipts and manifest
```

Out of scope:

```text
typed scalar ownership changes
structure-bias changes
greedy purity redesign outside EOS provenance
stop-sequence ownership migration
repetition detector redesign
checkpoint/model/tokenizer binding
persistent session
single model load
live progress and timeout
default policy promotion
model quality comparison
production promotion
```

---

# 4. Canonical module and types

Add:

```text
crates/model_core/src/minimum_new_token_eos_authority.rs
```

Required canonical types:

```rust
pub enum MinimumNewTokenEosAuthorityId {
    SamplerTransition,
}

pub enum MinimumNewTokenThresholdSource {
    RequestDecodeContract,
    TransitionProfileFloor,
    RequestAndTransitionFloor,
    DefaultZero,
}

pub struct MinimumNewTokenEosRunContract {
    pub schema: String,
    pub authority_id: MinimumNewTokenEosAuthorityId,
    pub eos_token_id: u32,
    pub requested_min_new_tokens: usize,
    pub transition_floor_min_new_tokens: usize,
    pub effective_min_new_tokens: usize,
    pub threshold_source: MinimumNewTokenThresholdSource,
    pub request_id: Option<String>,
    pub decode_policy_id: Option<DecodeSamplerPolicyId>,
    pub sampling_contract_digest: Option<String>,
    pub contract_digest: String,
}

pub enum EosMaterializationSite {
    PrefillSelection,
    DecodeStepSelection,
    SampledSelection,
    GreedyHardSafetySelection,
    PostCommitRepetitionGuard,
    ExplicitRuntimeSafetyStop,
}

pub enum EosEligibility {
    Allowed,
    BlockedBeforeMinimum,
    NotEosCandidate,
}

pub struct MinimumNewTokenEosDecisionReceipt {
    pub authority_id: MinimumNewTokenEosAuthorityId,
    pub contract_digest: String,
    pub site: EosMaterializationSite,
    pub step_index: usize,
    pub generated_count_before_selection: usize,
    pub candidate_token_id: u32,
    pub eos_token_id: u32,
    pub effective_min_new_tokens: usize,
    pub eligibility: EosEligibility,
    pub eos_mask_required: bool,
    pub eos_materialization_allowed: bool,
    pub reason: String,
}
```

Run summary requirements:

```text
authority_id
authority_instance_count
decision_count
eos_candidate_count
eos_blocked_before_minimum_count
eos_allowed_after_minimum_count
illegal_eos_committed_count
illegal_eos_emitted_count
post_commit_eos_denied_count
duplicate_owner_observation_count
authority_missing_count
```

---

# 5. Threshold SSOT

Resolve once per generation run:

```text
effective_min_new_tokens=
max(requested_min_new_tokens, active_transition_floor)
```

The transition floor contributes only while the transition profile is active. An inactive profile contributes zero, even if its config type has a non-zero default.

Threshold provenance:

```text
request only                    -> request_decode_contract
transition floor only           -> transition_profile_floor
both non-zero                   -> request_and_transition_floor
both zero                       -> default_zero
```

The resolved threshold is immutable after generation begins.

---

# 6. Generated-count convention

Every route uses:

```text
generated_count_before_selection
```

Definition:

```text
number of generated tokens already committed before evaluating the current candidate
prompt tokens excluded
current candidate excluded
```

EOS eligibility:

```text
generated_count_before_selection >= effective_min_new_tokens
```

Required boundaries:

```text
min=0 count=0 -> allowed
min=1 count=0 -> blocked
min=1 count=1 -> allowed
min=8 count=7 -> blocked
min=8 count=8 -> allowed
```

Forbidden substitutes:

```text
step+1
candidate snapshot length
emitted character length
prompt-inclusive tail length
```

---

# 7. Canonical authority API

Required production functions:

```rust
pub fn build_minimum_new_token_eos_run_contract(...)
    -> MinimumNewTokenEosRunContract;

pub fn decide_minimum_new_token_eos(
    contract: &MinimumNewTokenEosRunContract,
    site: EosMaterializationSite,
    step_index: usize,
    generated_count_before_selection: usize,
    candidate_token_id: u32,
) -> MinimumNewTokenEosDecisionReceipt;

pub fn derive_step_local_eos_mask(...)
    -> (Vec<u32>, MinimumNewTokenEosDecisionReceipt);

pub fn summarize_minimum_new_token_eos_run(...)
    -> MinimumNewTokenEosRunSummary;

pub fn classify_minimum_new_token_eos_shadow_parity(...)
    -> MinimumNewTokenEosShadowParityReceipt;
```

Only this authority may decide whether EOS is blocked or materialized due to `min_new_tokens`.

---

# 8. Selection-path binding

All prefill and decode paths must derive step-local EOS masks from the authority contract.

Required active surfaces:

```text
greedy prefill
greedy decode step
sampled prefill
sampled decode step
CPU oracle fallback through authority-derived banned IDs
R1C greedy hard-safety through authority decision receipt
```

The old `eos_restore_step_local_banned_token_ids` owner is removed. Transition guard receives the canonical decision receipt and may classify `EosBeforeMinNewTokens`, but must not recompute the threshold.

For blocked EOS:

```text
eligibility=blocked_before_minimum
eos_mask_required=true
committed_token_id!=eos_token_id
emitted_token_id!=eos_token_id
```

For non-EOS candidates:

```text
eligibility=not_eos_candidate
selection identity unaffected
```

---

# 9. Greedy-control binding

R1C hard-safety must receive the authority decision receipt rather than a local boolean.

Required provenance:

```text
minimum_new_token_eos_authority:<contract_digest>
```

Greedy purity remains valid only when:

```text
hard-safety EOS intervention is authority-backed
contract digest matches the active run contract
no sampled backend enters
no soft penalty or rerank controls top1
```

---

# 10. Post-commit EOS materialization

Repetition guard and explicit runtime safety stops may not append or replace with EOS directly.

Required flow:

```text
post-commit safety trigger
-> authority decision at PostCommitRepetitionGuard or ExplicitRuntimeSafetyStop
-> authorized EOS write or non-EOS safety finish
```

At or after the threshold:

```text
EOS replacement allowed
explicit post-commit intervention receipt emitted
```

Before the threshold:

```text
EOS write forbidden
finish_reason=SafetyStopRepetitionGuard
natural EOS must not be claimed
```

---

# 11. EOS01/EOS03/EOS03A shadow-only rebind

All three orchestrator audits consume runtime authority evidence. They may not own enforcement.

Remove from EOS03:

```text
second run_standard_infer_with_decode call
decode override reconstruction
request-wide EOS ban injection
result replacement
hard-coded EOS token id
```

Required shadow receipt truth:

```text
enforcement_patch=false
audit_only=true
shadow_verifier=true
rerun_attempted=false
request_wide_eos_ban_used=false
policy_mutation_count=0
result_replacement_count=0
runtime_authority_id=sampler_transition
runtime_contract_digest
shadow_contract_digest
step_parity_match_count
step_parity_mismatch_count
finish_reason_parity
```

EOS03A verifies suppression before the threshold and restore eligibility at or after the threshold. It proves eligibility, not that the model must naturally select EOS.

EOS01 must also read runtime EOS token identity, threshold, decisions, and run summary. Hard-coded `EOS=2` and independent threshold comparison are forbidden.

---

# 12. No rerun policy mutation

For an R1D-governed request:

```text
standard_infer_execution_count=1
eos_guard_rerun_count=0
```

The following remain unchanged from initial request to final result:

```text
decode policy id
sampling owner
policy definition digest
sampling request contract digest
temperature
top_p
top_k
min_p
seed
max_new_tokens
stop sequences
adapter selection
model/checkpoint request identity
```

Required zeros:

```text
rerun_policy_mutation_count=0
rerun_seed_mutation_count=0
rerun_sampling_scalar_mutation_count=0
rerun_min_new_token_mutation_count=0
second_infer_result_replacement_count=0
```

---

# 13. Duplicate ownership zero seal

The Rust gate inventories all code sites that can:

```text
compare EOS eligibility against min_new_tokens
add/remove EOS in a selection ban mask
replace or append EOS as a safety stop
rerun inference after early EOS
hard-code EOS identity for this guard
```

Every executable site must either be inside the canonical authority module or delegate without making its own eligibility decision.

Required static truth:

```text
canonical_eos_authority_definition_count=1
direct_min_new_token_eos_comparison_outside_authority_count=0
direct_eos_mask_mutation_outside_authority_count=0
direct_post_commit_eos_write_without_authority_count=0
eos_guard_infer_rerun_call_count=0
orchestrator_hardcoded_eos_enforcement_count=0
duplicate_eos_owner_count=0
```

Required runtime truth:

```text
authority_id=sampler_transition
authority_instance_count=1
duplicate_owner_observation_count=0
authority_missing_count=0
```

---

# 14. Runtime propagation and route receipt

`GenerationTelemetry` owns:

```text
minimum_new_token_eos_run_contract
minimum_new_token_eos_decisions
minimum_new_token_eos_run_summary
```

`StandardInferResult` and `StandardInferCandidateOutput` propagate:

```text
eos_token_id_runtime
effective_min_new_tokens_runtime
minimum_new_token_eos_contract_digest
minimum_new_token_eos_run_contract
minimum_new_token_eos_run_summary
minimum_new_token_eos_decisions
```

The active sampler receipt remains externally flat but is internally assembled through Atlas parallel groups, including:

```text
minimum_new_token_eos_authority
eos_guard_rerun_count
eos_guard_policy_mutation_count
duplicate_eos_owner_count
```

Request-side reconstruction of runtime EOS decisions is forbidden.

---

# 15. Finish-reason legality

Add a non-EOS safety finish reason:

```text
SafetyStopRepetitionGuard
```

When post-commit EOS is denied before the threshold, generation stops with this reason and does not append EOS. Runtime reranking must treat it as a safety/interrupted class, not successful natural EOS.

---

# 16. Local Rust audit gate

Add:

```text
crates/orchestrator_local/src/bin/ash_decode_sampler_02_r1d_minimum_new_token_eos_single_owner_gate.rs
```

Arguments:

```text
--repo-root
--r1a-parent-artifact
--r1a-parent-manifest
--r1b-parent-artifact
--r1b-parent-manifest
--r1c-parent-artifact
--r1c-parent-manifest
--out-dir
```

The gate uses production contract, decision, mask, summary, and shadow-parity functions without loading a model.

Required deterministic matrix:

```text
8 threshold-source cases
16 selection-boundary cases
8 post-commit cases
8 shadow and negative-control cases
minimum_case_count=40
```

Negative controls include wrong EOS identity, wrong contract digest, simulated rerun mutation, duplicate owner, and unaccounted post-commit replacement.

---

# 17. Local artifacts

Rust locally creates:

```text
workspace/runtime/decode/
  ash_decode_sampler_02_r1d_minimum_new_token_eos_single_owner_runtime_artifact.json
  ash_decode_sampler_02_r1d_local_manifest.json
  ash_decode_sampler_02_r1d_parent_binding_receipt.json
  ash_decode_sampler_02_r1d_source_inventory_receipt.json
  ash_decode_sampler_02_r1d_eos_owner_inventory.json
  ash_decode_sampler_02_r1d_threshold_resolution_matrix.json
  ash_decode_sampler_02_r1d_selection_boundary_matrix.json
  ash_decode_sampler_02_r1d_post_commit_eos_matrix.json
  ash_decode_sampler_02_r1d_eos03_shadow_parity_receipt.json
  ash_decode_sampler_02_r1d_eos03a_shadow_parity_receipt.json
  ash_decode_sampler_02_r1d_no_rerun_policy_mutation_receipt.json
  ash_decode_sampler_02_r1d_duplicate_owner_zero_receipt.json
  ash_decode_sampler_02_r1d_finish_reason_legality_receipt.json
  ash_decode_sampler_02_r1d_static_checks.json
  ash_decode_sampler_02_r1d_no_default_mutation_guard.json
  ash_decode_sampler_02_r1d_model_quality_claim_guard.json
  ash_decode_sampler_02_r1d_verdict.json
```

Per-case outputs:

```text
workspace/runtime/decode/r1d/cases/<case_id>/
  request.json
  eos_run_contract.json
  eos_decision.json
  shadow_parity.json
  case_result.json
  stdout.jsonl
  stderr.log
```

Generated artifacts, manifests, receipts, and case directories are excluded from the source bake archive.

---

# 18. Canonical failures

```text
R1AParentEvidenceIncomplete
R1BParentEvidenceIncomplete
R1CParentEvidenceIncomplete
MinimumNewTokenEosAuthorityMissing
MinimumNewTokenEosAuthorityCountInvalid
MinimumNewTokenEosContractMissing
MinimumNewTokenEosContractDigestMismatch
MinimumNewTokenThresholdResolutionMismatch
MinimumNewTokenCountConventionMismatch
EosSelectionPathAuthorityUnbound
EosTransitionDecisionMissing
EosTransitionDecisionMismatch
EosBlockedTokenCommitted
EosBlockedTokenEmitted
EosAllowedBoundaryIncorrect
EosPostCommitMaterializationUnauthorized
EosSafetyStopFinishReasonIllegal
Eos03EnforcementRerunStillPresent
Eos03ShadowParityMismatch
Eos03aShadowSuppressionMismatch
Eos03aShadowRestoreMismatch
EosGuardRerunPolicyMutationObserved
DuplicateEosOwnerObserved
OrchestratorHardcodedEosEnforcementObserved
RuntimeEosAuthorityEvidenceMissing
CompileTruthMissing
```

---

# 19. PASS formula

```text
PASS =
  r1a_parent_binding_pass
  && r1b_parent_binding_pass
  && r1c_parent_binding_pass
  && compile_truth_pass
  && canonical_eos_authority_definition_count==1
  && authority_instance_count==1
  && direct_min_new_token_eos_comparison_outside_authority_count==0
  && direct_eos_mask_mutation_outside_authority_count==0
  && direct_post_commit_eos_write_without_authority_count==0
  && eos_guard_infer_rerun_call_count==0
  && orchestrator_hardcoded_eos_enforcement_count==0
  && duplicate_eos_owner_count==0
  && threshold_boundary_fail_count==0
  && selection_authority_missing_count==0
  && illegal_eos_committed_count==0
  && illegal_eos_emitted_count==0
  && eos03_shadow_parity_mismatch_count==0
  && eos03a_shadow_suppression_mismatch_count==0
  && eos03a_shadow_restore_mismatch_count==0
  && rerun_policy_mutation_count==0
  && default_sampler_policy_mutation_count==0
  && model_quality_claim_count==0
```

PASS means one sampler-transition authority owns minimum-new-token EOS eligibility across greedy, sampled, prefill, decode-step, and post-commit materialization. EOS01/EOS03/EOS03A are shadow consumers only. PASS does not prove model quality, natural EOS quality, checkpoint binding, persistent sessions, single model load, or production readiness.

---

# 20. Build and run

```powershell
cargo fmt --all -- --check
cargo check --manifest-path crates/model_core/Cargo.toml
cargo check --manifest-path crates/runtime/Cargo.toml
cargo check --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_decode_sampler_02_r1d_minimum_new_token_eos_single_owner_gate

cargo run --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_decode_sampler_02_r1d_minimum_new_token_eos_single_owner_gate `
  -- `
  --repo-root . `
  --r1a-parent-artifact workspace/runtime/decode/ash_decode_sampler_02_r1a_typed_policy_final_sampling_ownership_runtime_artifact.json `
  --r1a-parent-manifest workspace/runtime/decode/ash_decode_sampler_02_r1a_local_manifest.json `
  --r1b-parent-artifact workspace/runtime/decode/ash_decode_sampler_02_r1b_structure_sampling_bias_suppression_runtime_artifact.json `
  --r1b-parent-manifest workspace/runtime/decode/ash_decode_sampler_02_r1b_local_manifest.json `
  --r1c-parent-artifact workspace/runtime/decode/ash_decode_sampler_02_r1c_greedy_control_contamination_runtime_artifact.json `
  --r1c-parent-manifest workspace/runtime/decode/ash_decode_sampler_02_r1c_local_manifest.json `
  --out-dir workspace/runtime/decode
```

Expected PASS token:

```text
PASS_ASH_DECODE_SAMPLER_02_R1D_MINIMUM_NEW_TOKEN_EOS_SINGLE_OWNER_SAMPLER_TRANSITION_AUTHORITY_EOS03_EOS03A_SHADOW_PARITY_NO_RERUN_POLICY_MUTATION_DUPLICATE_EOS_OWNERSHIP_ZERO_NO_DEFAULT_MUTATION_NO_MODEL_QUALITY_OVERCLAIM
```

Expected outputs:

```text
primary_artifact=workspace/runtime/decode/ash_decode_sampler_02_r1d_minimum_new_token_eos_single_owner_runtime_artifact.json
manifest=workspace/runtime/decode/ash_decode_sampler_02_r1d_local_manifest.json
```

On PASS:

```text
status=PASS
ready_for_sampler_02_r1e=true
ready_for_sampler_02_r1e_scope=checkpoint_model_tokenizer_binding_gate
ready_for_default_sampler_policy_promotion=false
ready_for_production_decode_promotion=false
```
