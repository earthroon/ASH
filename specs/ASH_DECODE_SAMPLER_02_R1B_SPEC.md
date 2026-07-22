# ASH-DECODE-SAMPLER-02-R1B

## Structure-Routing Sampling Bias Source Suppression /
## Locked-Field Mutation Attempt Zero Seal

---

# 0. Patch identity

```text
patch_id=ASH-DECODE-SAMPLER-02-R1B
parent_patch_id=ASH-DECODE-SAMPLER-02-R1A
patch_class=decode_sampling_policy_ownership_hardening
runtime_schema=ash.decode.sampler.02.r1b.structure_sampling_bias_suppression.runtime_artifact.v1
primary_artifact=workspace/runtime/decode/ash_decode_sampler_02_r1b_structure_sampling_bias_suppression_runtime_artifact.json
local_manifest=workspace/runtime/decode/ash_decode_sampler_02_r1b_local_manifest.json
```

Parent code archive:

```text
archive=ash_pass3_ASH-DECODE-SAMPLER-02-R1A-R2_incoming_id_scope_compile_closure_code_baked_no_spec_no_runtime_artifacts_no_manifest.zip
archive_sha256=ee3ba3000b0bc8cab83f572d91b4c7970d65f59ca6b34081308139ce2b8c9308
parent_source_inventory_digest=f1c2549e099de79722932c758eedf9e9219dfcab7fa65757e63fbad87d5144ad
```

Parent runtime evidence:

```text
PASS_ASH_DECODE_SAMPLER_02_R1A_TYPED_POLICY_FINAL_SAMPLING_OWNERSHIP_CANONICAL_SCALAR_SSOT_RUNTIME_IDENTITY_PROPAGATION_POST_ROUTING_DRIFT_REASSERTED_FINAL_SCALAR_PARITY_NO_DEFAULT_MUTATION_NO_MODEL_QUALITY_OVERCLAIM

primary_artifact=workspace/runtime/decode/ash_decode_sampler_02_r1a_typed_policy_final_sampling_ownership_runtime_artifact.json
manifest=workspace/runtime/decode/ash_decode_sampler_02_r1a_local_manifest.json
```

R1B must read and hash-validate the parent artifact and manifest. A copied PASS token is not sufficient evidence.

---

# 1. Current-source truth

R1A established typed-policy scalar SSOT, `SamplingOwnershipEnvelope`, the five locked fields, runtime policy identity, post-routing drift observation, final canonical reassertion, and final sampler scalar parity.

R1A intentionally allowed:

```text
attempted_locked_field_mutation_count>0
canonical_reassertion_applied=true
```

when the final sampler snapshot was repaired to the canonical policy snapshot.

The remaining scalar mutation source is `NativeWgpuModel::resolve_sampling_with_structure_prior()`. When structure routing is active it can directly rewrite:

```text
temperature
top_p
top_k
```

from the gate-derived values:

```text
sampling_temperature_bias
sampling_top_p_bias
sampling_top_k_bias
```

`min_p` and `seed` are not currently rewritten by that function, but remain typed-policy locked fields and are part of the zero-mutation proof.

The old resolution/finalization sequence is repeated across six active paths:

```text
strict_gpu_sampled_choice
select_next_token_with_sampling
generate_with_sampling_cached_with_telemetry
generate_with_sampling_streaming_with_telemetry
greedy_generate_cached_with_telemetry
greedy_generate_streaming_with_telemetry
```

Current truth before R1B:

```text
structure_bias_candidate_generation_present=true
structure_scalar_write_source_present=true
typed_policy_locked_field_write_possible=true
r1a_final_reassertion_present=true
locked_field_mutation_attempt_zero_proven=false
sampling_preparation_call_sites_centralized=false
legacy_non_typed_structure_bias_behavior_present=true
```

---

# 2. Purpose

R1B changes typed-policy structure routing from:

```text
calculate bias
-> mutate typed-policy scalar
-> detect drift
-> reassert canonical value
```

to:

```text
calculate advisory bias candidate
-> inspect ownership and locks
-> suppress writes to locked fields
-> preserve bound scalar values bitwise
-> let R1A finalization verify zero drift
```

Required typed-policy result:

```text
attempted_locked_field_mutation_count=0
locked_field_value_changed_count=0
canonical_reassertion_applied=false
runtime_initial_snapshot=post_structure_routing_snapshot
post_structure_routing_snapshot=final_sampler_snapshot
final_sampler_snapshot=request_canonical_snapshot
```

The R1A finalizer remains mandatory as an invariant gate. R1B does not delete it.

---

# 3. Scope

In scope:

```text
structure sampling bias candidate separation
ownership-aware mutation eligibility
suppression before writes to typed-policy locked fields
zero mutation-attempt runtime proof
single sampling preparation helper
six active route rebinds
suppression telemetry
R1A evidence join
legacy unlocked behavior parity
local Rust audit matrix
local manifest and receipts
```

Out of scope:

```text
removal of structure routing or prior derivation
candidate rerank removal
logit/decode penalty removal
adapter routing removal
greedy top1 contamination adjudication
minimum-new-token EOS ownership
checkpoint/model/tokenizer binding
persistent runtime session
single model load
live progress and timeout
default policy promotion
model quality comparison
production decode promotion
```

R1B suppresses only structure-routing writes to sampling scalar fields protected by ownership locks.

---

# 4. Canonical types

Add to the canonical `model_core` policy/routing surface:

```rust
#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize, Default)]
pub struct StructureSamplingBiasCandidate {
    pub temperature_delta: f32,
    pub top_p_delta: f32,
    pub top_k_bias: u32,
    pub strict_mode: bool,
    pub structure_routing_active: bool,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum StructureSamplingFieldDisposition {
    NoStructureRoute,
    NoEffectiveBias,
    AppliedUnlocked,
    SuppressedByOwnershipLock,
    AlreadyFinalizedNoReapply,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct StructureSamplingBiasResolution {
    pub schema: String,
    pub structure_routing_active: bool,
    pub already_finalized_no_reapply: bool,
    pub owner: Option<SamplingParameterOwner>,
    pub policy_id: Option<DecodeSamplerPolicyId>,
    pub input_snapshot: SamplingScalarSnapshot,
    pub output_snapshot: SamplingScalarSnapshot,
    pub candidate: StructureSamplingBiasCandidate,
    pub temperature_disposition: StructureSamplingFieldDisposition,
    pub top_p_disposition: StructureSamplingFieldDisposition,
    pub top_k_disposition: StructureSamplingFieldDisposition,
    pub min_p_disposition: StructureSamplingFieldDisposition,
    pub seed_disposition: StructureSamplingFieldDisposition,
    pub applied_unlocked_field_count: usize,
    pub suppressed_locked_field_count: usize,
    pub attempted_locked_field_mutation_count: usize,
    pub locked_field_value_changed_count: usize,
    pub output_equals_input_for_all_locked_fields: bool,
}

pub struct PreparedSamplingForTokenSelection {
    pub config: GenerationSamplingConfig,
    pub ownership_finalization: Option<SamplingOwnershipFinalization>,
    pub structure_bias_resolution: StructureSamplingBiasResolution,
}
```

Required resolution schema:

```text
ash.decode.sampler.02.r1b.structure_sampling_bias_resolution.v1
```

A bias candidate is advisory evidence. Candidate calculation is not a mutation attempt. A locked-field mutation attempt exists if code writes a different protected value, constructs a replacement config with a different protected value, applies before checking a lock, or applies and restores in the same function.

---

# 5. Canonical ownership-aware resolver

Production code must have one pure scalar resolver:

```rust
pub fn resolve_structure_sampling_bias(
    sampling: &GenerationSamplingConfig,
    candidate: StructureSamplingBiasCandidate,
) -> Result<(GenerationSamplingConfig, StructureSamplingBiasResolution)>;
```

The native model resolver derives `StructureSamplingBiasCandidate` from the existing structure-routing gate, then delegates scalar application to this canonical function.

Required operation order:

```text
1. capture input snapshot
2. validate typed-policy ownership envelope
3. read per-field locks
4. evaluate lock before assignment
5. apply candidate only to unlocked fields
6. capture output snapshot
7. compare all locked fields bitwise
8. emit resolution receipt
```

Forbidden order:

```text
apply bias -> inspect lock -> restore canonical value
```

The resolver must not call `canonical_scalars()` to disguise drift. It preserves the already-bound runtime config.

---

# 6. Per-field rules

For unlocked legacy/free-form paths, preserve the pre-R1B formulas exactly:

```text
if temperature>0:
  temperature=(temperature+temperature_delta).clamp(0.05,1.8)

if top_p>0:
  top_p=(top_p+top_p_delta).clamp(0.55,1.0)

if strict_mode:
  if top_k==0:
    top_k=max(top_k_bias,4)
  else:
    top_k=min(top_k,max(top_k_bias,4)).max(4)
else if top_k>0:
  top_k=min(top_k+top_k_bias,64)
```

For typed-policy locks:

```text
temperature output bits=input bits
top_p output bits=input bits
top_k output=input
min_p output bits=input bits
seed output=input
```

When structure routing is active, all five typed-policy fields report `suppressed_by_ownership_lock`, including `min_p` and `seed`, so the full lock contract remains explicit.

This explicitly prevents strict structure routing from changing `greedy_control.top_k=0` to `top_k>=4`.

Typed-policy requirements:

```text
all five dispositions=suppressed_by_ownership_lock
applied_unlocked_field_count=0
attempted_locked_field_mutation_count=0
locked_field_value_changed_count=0
output_equals_input_for_all_locked_fields=true
```

---

# 7. Legacy compatibility

R1B must not disable structure scalar routing for:

```text
sampling_ownership=None
owner=legacy_runtime_default
owner=freeform_request
owner=candidate_plan
```

Required compatibility matrix:

```text
inactive route identity
strict and non-strict parity
zero-temperature parity
zero-top-k non-strict parity
strict zero-to-minimum top-k parity
clamp-boundary parity
```

Required:

```text
legacy_unlocked_behavior_drift_count=0
```

No default policy is changed.

---

# 8. Single sampling preparation SSOT

Introduce one helper:

```rust
fn prepare_sampling_for_token_selection(
    &self,
    incoming: &GenerationSamplingConfig,
) -> Result<PreparedSamplingForTokenSelection>;
```

Required flow:

```text
incoming config
-> if already finalized, emit already_finalized_no_reapply and skip routing
-> ownership-aware structure resolver
-> R1A finalizer
-> R1B zero-mutation assertions
-> mark sampling_ownership_finalized=true
-> PreparedSamplingForTokenSelection
```

For typed policies:

```text
structure resolution attempted mutation count=0
structure resolution changed value count=0
ownership finalization attempted mutation count=0
canonical_reassertion_applied=false
final_sampling_scalar_parity=true
```

The helper is the only active path that combines structure scalar routing and ownership finalization.

The six active functions listed in Section 1 must call this helper. Required static truth:

```text
sampling_preparation_helper_definition_count=1
active_sampling_preparation_call_site_count=6
direct_structure_resolution_call_count_outside_helper=0
direct_finalizer_call_count_in_active_generation_paths_outside_helper=0
unbound_active_sampling_path_count=0
```

An already-finalized config must never receive a second structure bias application. A second application fails with `StructureSamplingBiasDoubleApplyObserved`.

---

# 9. Telemetry and runtime evidence

`GenerationTelemetry` must carry:

```text
structure_sampling_bias_resolution
structure_sampling_bias_resolution_count
structure_sampling_bias_suppressed_locked_field_count
structure_sampling_bias_applied_unlocked_field_count
structure_sampling_locked_field_mutation_attempt_count
structure_sampling_locked_field_value_changed_count
```

`StandardInferResult` and `StandardInferCandidateOutput` must propagate the final resolution receipt. `orchestrator_local` route receipts consume runtime evidence directly. Request-side reconstruction is forbidden.

Typed-policy runtime requirements:

```text
structure_sampling_bias_resolution_count>=1
structure_sampling_locked_field_mutation_attempt_count=0
structure_sampling_locked_field_value_changed_count=0
```

R1A/R1B receipt join:

```text
r1a.runtime_initial_snapshot=r1b.input_snapshot
r1a.post_structure_routing_snapshot=r1b.output_snapshot
r1a.request_canonical_snapshot=r1a.final_sampler_snapshot
r1a.attempted_locked_field_mutation_count=0
r1a.canonical_reassertion_applied=false
r1b.attempted_locked_field_mutation_count=0
r1b.locked_field_value_changed_count=0
```

---

# 10. Boundary honesty

These effects remain allowed and separately reportable:

```text
candidate rerank
candidate pool span selection
decode penalty logits adjustment
GPU penalty pass
adapter scale routing
morph adapter gain
honorific adapter gain
routing pressure
```

R1B must not claim:

```text
structure routing disabled
all structure bias removed
selected token unaffected
greedy route pure
```

Required honesty fields include:

```text
structure_route_active
sampling_scalar_bias_suppressed
candidate_rerank_active
logit_penalty_active
adapter_routing_active
selected_token_effect_not_adjudicated=true
```

Token-selection purity remains R1C scope.

---

# 11. Local Rust audit gate

Add binary:

```text
crates/orchestrator_local/src/bin/ash_decode_sampler_02_r1b_structure_sampling_bias_suppression_gate.rs
```

The binary does not require model language inference.

Arguments:

```text
--repo-root
--r1a-parent-artifact
--r1a-parent-manifest
--out-dir
```

Parent checks:

```text
parent files exist
manifest hashes parent primary artifact
parent patch id=ASH-DECODE-SAMPLER-02-R1A
parent verdict=PASS
final scalar parity=true
no default mutation=true
no model quality overclaim=true
```

Missing parent evidence causes HOLD with `R1AParentEvidenceIncomplete`.

Runtime matrix:

```text
3 typed policies
x 2 structure modes
x 2 candidate classes
x 2 execution states
=24 typed cases

plus 8 unlocked legacy/free-form parity cases
minimum total=32
```

Each typed case proves bitwise input/output identity for all locked fields, zero mutation attempts, zero changed values, no R1A repair, final parity, policy identity preservation, and contract digest preservation.

Each legacy case compares the production resolver with a test-only pre-R1B formula oracle.

---

# 12. Local artifacts

Rust locally creates:

```text
workspace/runtime/decode/
  ash_decode_sampler_02_r1b_structure_sampling_bias_suppression_runtime_artifact.json
  ash_decode_sampler_02_r1b_local_manifest.json
  ash_decode_sampler_02_r1b_parent_binding_receipt.json
  ash_decode_sampler_02_r1b_source_inventory_receipt.json
  ash_decode_sampler_02_r1b_structure_bias_source_inventory.json
  ash_decode_sampler_02_r1b_bias_candidate_derivation_receipt.json
  ash_decode_sampler_02_r1b_locked_field_suppression_receipt.json
  ash_decode_sampler_02_r1b_active_route_rebind_receipt.json
  ash_decode_sampler_02_r1b_typed_policy_zero_mutation_matrix.json
  ash_decode_sampler_02_r1b_legacy_behavior_parity_matrix.json
  ash_decode_sampler_02_r1b_already_finalized_no_reapply_receipt.json
  ash_decode_sampler_02_r1b_r1a_evidence_join_receipt.json
  ash_decode_sampler_02_r1b_static_checks.json
  ash_decode_sampler_02_r1b_no_default_mutation_guard.json
  ash_decode_sampler_02_r1b_model_quality_claim_guard.json
  ash_decode_sampler_02_r1b_verdict.json
```

Per case:

```text
workspace/runtime/decode/r1b/cases/<case_id>/
  request.json
  input_sampling.json
  structure_bias_candidate.json
  structure_bias_resolution.json
  ownership_finalization.json
  case_result.json
  stdout.jsonl
  stderr.log
```

Generated artifacts and manifests are excluded from the source bake archive.

---

# 13. Static, unit, and integration gates

Static checks:

```text
structure_sampling_bias_candidate_type_count=1
structure_sampling_bias_resolution_type_count=1
pure_structure_sampling_bias_resolver_definition_count=1
native_structure_resolution_definition_count=1
sampling_preparation_helper_definition_count=1
active_sampling_preparation_call_site_count=6
direct_structure_resolution_call_count_outside_helper=0
direct_finalizer_call_count_outside_helper=0
unbound_active_sampling_path_count=0
```

Required unit coverage includes:

```text
typed greedy strict keeps top_k=0
typed sampled policies preserve temperature/top_p/top_k/min_p/seed
non-zero candidate is suppressed before assignment
zero candidate produces no mutation
already-finalized config does not reapply bias
legacy strict and non-strict formula parity
legacy clamp parity
inactive route identity
R1A finalizer reports zero mutation and reassertion=false
```

Use exact `f32::to_bits()` comparisons for locked floating-point fields.

Integration paths:

```text
typed sampled request -> bias candidate -> lock suppression -> finalizer -> selector
typed greedy top_k=0 -> strict top-k candidate >=4 -> suppression -> greedy selector
legacy unlocked config -> structure route -> exact pre-R1B scalar output
```

R1B does not yet prove greedy selected-token purity.

---

# 14. Canonical failures

```text
R1AParentEvidenceIncomplete
StructureSamplingBiasResolutionMissing
StructureSamplingBiasCandidateMissing
StructureSamplingBiasAppliedBeforeLockCheck
TypedPolicyLockedFieldMutationAttemptObserved
TypedPolicyLockedFieldValueChanged
TypedPolicyStructureBiasSuppressionMissing
TypedPolicyStructureBiasSuppressionReceiptMissing
TypedPolicyCanonicalReassertionStillRequired
StructureSamplingBiasDoubleApplyObserved
ActiveSamplingPreparationPathUnbound
DirectStructureResolutionCallOutsidePreparationSSOT
DirectOwnershipFinalizerCallOutsidePreparationSSOT
LegacyStructureSamplingBehaviorDrift
StructureRoutingBoundaryOverclaim
RuntimeEvidenceMissing
CompileTruthMissing
```

Stable failure strings are required.

---

# 15. PASS formula

```text
PASS =
  parent_r1a_binding_pass
  && compile_truth_pass
  && structure_bias_candidate_separated
  && lock_check_occurs_before_write
  && typed_policy_temperature_mutation_count==0
  && typed_policy_top_p_mutation_count==0
  && typed_policy_top_k_mutation_count==0
  && typed_policy_min_p_mutation_count==0
  && typed_policy_seed_mutation_count==0
  && attempted_locked_field_mutation_count==0
  && locked_field_value_changed_count==0
  && canonical_reassertion_applied_count==0
  && final_sampling_scalar_parity_fail_count==0
  && unbound_active_sampling_path_count==0
  && double_apply_count==0
  && legacy_unlocked_behavior_drift_count==0
  && default_policy_mutation_count==0
  && model_quality_claim_count==0
```

PASS means structure-routing bias candidates may exist, but typed-policy locks are checked before writes, protected scalar values remain bitwise unchanged, no R1A repair is needed, all active token-selection routes use one preparation SSOT, and legacy unlocked behavior remains exact.

PASS does not mean candidate reranking, logit penalties, adapter routing, or selected-token influence is gone. It does not prove greedy contamination absence, model quality improvement, default policy promotion, or production readiness.

---

# 16. Safety and honesty

Required false:

```text
structure_routing_disabled_claimed
structure_routing_all_bias_removed_claimed
candidate_rerank_removed_claimed
logit_penalty_removed_claimed
selected_token_unchanged_claimed
greedy_contamination_absent_claimed
model_quality_claimed
translation_quality_claimed
production_decode_ready_claimed
default_sampler_policy_promoted
```

Required zero:

```text
default_sampler_policy_mutation_count
model_weight_mutation_count
tokenizer_mutation_count
checkpoint_mutation_count
training_step_count
optimizer_step_count
production_route_replacement_count
```

---

# 17. Code surfaces

```text
crates/model_core/src/decode_sampling_policy.rs
crates/model_core/src/generation_sampling.rs
crates/model_core/src/generation_telemetry.rs
crates/model_core/src/native_wgpu.rs
crates/model_core/src/lib.rs
crates/runtime/src/infer.rs
crates/runtime/src/infer/candidate_output.rs
crates/orchestrator_local/src/infer_entry.rs
crates/orchestrator_local/src/bin/ash_decode_sampler_02_r1b_structure_sampling_bias_suppression_gate.rs
crates/orchestrator_local/Cargo.toml
```

Do not create a second typed-policy scalar table. Do not move structure-routing state ownership into orchestrator.

---

# 18. Build and run

```powershell
cargo fmt --all -- --check

cargo check --manifest-path crates/model_core/Cargo.toml
cargo check --manifest-path crates/runtime/Cargo.toml
cargo check --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_decode_sampler_02_r1b_structure_sampling_bias_suppression_gate

cargo run --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_decode_sampler_02_r1b_structure_sampling_bias_suppression_gate `
  -- `
  --repo-root . `
  --r1a-parent-artifact workspace/runtime/decode/ash_decode_sampler_02_r1a_typed_policy_final_sampling_ownership_runtime_artifact.json `
  --r1a-parent-manifest workspace/runtime/decode/ash_decode_sampler_02_r1a_local_manifest.json `
  --out-dir workspace/runtime/decode
```

The Rust binary owns local creation of R1B runtime artifacts and the manifest.

Expected PASS token:

```text
PASS_ASH_DECODE_SAMPLER_02_R1B_STRUCTURE_ROUTING_SAMPLING_BIAS_SOURCE_SUPPRESSION_LOCK_CHECK_BEFORE_WRITE_LOCKED_FIELD_MUTATION_ATTEMPT_ZERO_NO_REASSERTION_REQUIRED_FINAL_SCALAR_PARITY_LEGACY_UNLOCKED_BEHAVIOR_PARITY_NO_DEFAULT_MUTATION_NO_MODEL_QUALITY_OVERCLAIM
```

Expected outputs:

```text
primary_artifact=workspace/runtime/decode/ash_decode_sampler_02_r1b_structure_sampling_bias_suppression_runtime_artifact.json
manifest=workspace/runtime/decode/ash_decode_sampler_02_r1b_local_manifest.json
```

---

# 19. Promotion boundary

On PASS:

```text
status=PASS
ready_for_sampler_02_r1c=true
ready_for_sampler_02_r1c_scope=greedy_control_contamination_gate
ready_for_default_sampler_policy_promotion=false
ready_for_production_decode_promotion=false
```

R1B closes one question:

```text
Can structure routing calculate advisory sampling bias information without ever mutating typed-policy locked scalar fields?
```

Required answer after PASS:

```text
Yes.
Bias candidates may exist.
Lock eligibility is checked before writes.
Typed-policy locked fields remain bitwise unchanged.
R1A finalization performs invariant checking and no repair.
```
