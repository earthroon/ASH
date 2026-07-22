# ASH-DECODE-SAMPLER-02-R1A

## Typed Policy Final Sampling Ownership /
## Canonical Policy Scalar SSOT /
## Request-to-Runtime Ownership Envelope /
## Locked Sampling Field Reassertion /
## Post-Routing Drift Detection /
## Retry and Rerun Policy Preservation /
## No Free-Form Rebind /
## No Default Policy Mutation /
## No Model Quality Overclaim Seal

---

## 0. Patch identity

```text
patch_id=ASH-DECODE-SAMPLER-02-R1A
runtime_schema=ash.decode.sampler.02.r1a.typed_policy_final_sampling_ownership.runtime_artifact.v1
primary_artifact=workspace/runtime/decode/ash_decode_sampler_02_r1a_typed_policy_final_sampling_ownership_runtime_artifact.json
local_manifest=workspace/runtime/decode/ash_decode_sampler_02_r1a_local_manifest.json
```

Parent:

```text
parent_patch_id=ASH-DECODE-SAMPLER-02
parent_spec_commit=eda93aa6a1b4c2d44e65314098a67492f91c8501
parent_source_inventory_digest=76d925e9379dc70dfc85943f473a5cb63aacdde8e6ce7f330d549f14c3b50a33
```

Primary code surfaces:

```text
crates/model_core/src/decode_sampling_policy.rs
crates/model_core/src/active_generation_route.rs
crates/model_core/src/generation_sampling.rs
crates/model_core/src/generation_telemetry.rs
crates/model_core/src/lib.rs
crates/runtime/src/infer.rs
crates/runtime/src/causal_lm.rs
crates/orchestrator_local/src/infer_entry.rs
crates/orchestrator_local/src/bin/ash_decode_sampler_02_r1a_typed_policy_ownership_gate.rs
crates/orchestrator_local/Cargo.toml
```

---

# 1. Current-source truth

The merged tree already accepts the typed policies:

```text
greedy_control
top_p_only_baseline
top_p_min_p_probe
```

Canonical scalar profiles already exist in `model_core`, but `orchestrator_local::infer_entry` independently reconstructs the same scalar table. The request is then reduced to optional scalar fields inside `StandardInferDecodeOverride`; policy identity, owner identity, locked-field declaration, and canonical policy digest are lost before runtime sampling configuration is built.

`NativeWgpuModel::resolve_sampling_with_structure_prior` may subsequently alter temperature, top-p, or top-k. Existing route receipts describe the orchestrator override and therefore do not prove which values the final sampler consumed.

Current state:

```text
typed_policy_request_present=true
canonical_policy_scalar_definition_present=true
orchestrator_policy_scalar_definition_duplicated=true
runtime_policy_identity_preserved=false
runtime_owner_identity_preserved=false
locked_sampling_fields_present=false
post_routing_scalar_drift_possible=true
final_sampler_scalar_parity_proven=false
```

---

# 2. Purpose

R1A establishes one final owner for typed-policy sampling scalars.

Required ownership chain:

```text
DecodeSamplerPolicyId
-> canonical scalar profile SSOT
-> request-owned ownership envelope
-> StandardInferDecodeOverride
-> GenerationSamplingConfig
-> mutable downstream routing
-> final ownership reassertion
-> sampler-consumed scalar snapshot
```

For a typed policy request:

```text
final_sampling_owner=typed_policy_final
final_sampling_owner_count=1
```

The typed policy owns exactly:

```text
temperature
top_p
top_k
min_p
seed
```

It does not take ownership of min/max token limits, stop sequences, banned tokens, candidate telemetry, transition hard blocks, model selection, checkpoint selection, or tokenizer selection.

---

# 3. Scope boundary

R1A includes:

```text
canonical policy scalar SSOT
policy identity propagation
owner identity propagation
locked-field declaration
request contract digest
post-routing drift observation
final sampler-boundary canonical reassertion
retry and EOS rerun ownership preservation
runtime result evidence
local Rust audit artifacts and manifest
```

R1A excludes:

```text
source-level removal of structure-routing bias
candidate-rerank removal
greedy-control contamination adjudication
minimum-new-token EOS ownership migration
checkpoint-model-tokenizer binding
persistent orchestrator session
single model load
live progress and timeout
default sampler promotion
model quality adjudication
```

Source-level suppression remains owned by `ASH-DECODE-SAMPLER-02-R1B`.

---

# 4. Canonical policy scalar SSOT

Introduce `crates/model_core/src/decode_sampling_policy.rs`.

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum DecodeSamplerPolicyId {
    GreedyControl,
    TopPOnlyBaseline,
    TopPMinPProbe,
}

#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
pub struct DecodeSamplerPolicyScalars {
    pub temperature: f32,
    pub top_k: u32,
    pub top_p: f32,
    pub min_p: f32,
}

impl DecodeSamplerPolicyId {
    pub fn canonical_scalars(self) -> DecodeSamplerPolicyScalars;
}
```

Canonical values:

```text
greedy_control       temperature=0.0 top_k=0 top_p=1.0 min_p=0.0
top_p_only_baseline  temperature=0.8 top_k=0 top_p=0.9 min_p=0.0
top_p_min_p_probe    temperature=0.8 top_k=0 top_p=0.9 min_p=0.05
```

All consumers must call `canonical_scalars()`. Independent policy scalar matches in orchestrator, runtime, or audit code are forbidden. Existing public import paths remain re-export compatible.

---

# 5. Ownership envelope

Required owner identity:

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum SamplingParameterOwner {
    LegacyRuntimeDefault,
    FreeformRequest,
    CandidatePlan,
    TypedPolicyFinal,
}
```

Required lock mask:

```rust
pub struct SamplingFieldLocks {
    pub temperature: bool,
    pub top_p: bool,
    pub top_k: bool,
    pub min_p: bool,
    pub seed: bool,
}
```

Required envelope:

```rust
pub struct SamplingOwnershipEnvelope {
    pub owner: SamplingParameterOwner,
    pub policy_id: Option<DecodeSamplerPolicyId>,
    pub locked_fields: SamplingFieldLocks,
    pub policy_definition_digest: String,
    pub request_sampling_contract_digest: String,
}
```

Typed policy requirements:

```text
owner=typed_policy_final
policy_id!=null
all five typed-policy fields locked
policy_definition_digest derived from canonical policy identity and exact scalar bits
request_sampling_contract_digest includes policy digest, seed, lock mask, and request identity
```

A typed request without a valid envelope fails before model inference.

---

# 6. Override and runtime propagation

Extend `StandardInferDecodeOverride` and `GenerationSamplingConfig` with `sampling_ownership: Option<SamplingOwnershipEnvelope>`.

Required propagation:

```text
request policy parse
-> canonical scalar profile
-> decode override plus envelope
-> runtime build_generation_sampling_config
-> generation configuration plus identical envelope
```

Runtime validation must verify:

```text
policy_id is known
owner is typed_policy_final
locked fields are complete
scalar bits equal canonical profile
seed equals request contract seed
policy digest matches canonical calculation
request contract digest matches the propagated request
```

No last-write-wins behavior is permitted.

---

# 7. Free-form conflict gate

When `decodeSamplerPolicy` or `decode_sampler_policy` is present, aliases of the following fields are checked before inference:

```text
temperature
topP / top_p
topK / top_k
minP / min_p / samplingMinP / sampling_min_p
seed
```

Matching aliases may be accepted. Any conflicting value fails closed before model loading or generation.

Required:

```text
freeform_parameter_conflict_count=0
conflicting_request_inference_execution_count=0
```

---

# 8. Final sampler-boundary reassertion

Introduce one finalizer in `model_core`:

```rust
pub fn finalize_sampling_ownership(
    sampling: &GenerationSamplingConfig,
) -> Result<FinalizedSamplingConfig, SamplingOwnershipError>;
```

The finalizer executes after mutable routing and immediately before any greedy or sampled selector consumes the configuration.

It must emit four snapshots:

```text
request_canonical_snapshot
runtime_initial_snapshot
post_structure_routing_snapshot
final_sampler_snapshot
```

For locked fields it must:

```text
compare exact f32 bit patterns and integer values
record every attempted drift
restore canonical typed-policy values
preserve unlocked fields
emit whether reassertion was required
prove final scalar parity
```

R1A permits observed drift attempts only when they are honestly counted and cannot survive to the sampler. R1B later requires zero source-level mutation attempts.

Required typed-policy final state:

```text
final_sampling_owner=typed_policy_final
final_sampling_owner_count=1
final_policy_id=requested_policy_id
final_sampling_scalar_parity=true
final_sampler_snapshot_digest=request_canonical_snapshot_digest
```

---

# 9. Active-path coverage

The finalizer must be bound to every active generation path that can consume typed-policy configuration, including cached and streaming sampled decode paths. A path that can reach token selection without finalization blocks PASS.

Required evidence:

```text
active_sampler_path_count
finalizer_bound_sampler_path_count
unfinalized_sampler_path_count=0
```

---

# 10. Retry and rerun preservation

Typed sampler policies are immutable across retry and safety rerun boundaries.

SALAD retry:

```text
typed_sampler_policy_present -> sampling scalar mutation unavailable
salad_typed_policy_mutation_count=0
```

EOS03/EOS03A rerun may alter only its EOS/minimum-token safety contract. It must preserve:

```text
policy_id
owner
locked_fields
canonical scalar bits
seed
policy_definition_digest
request_sampling_contract_digest
```

Any loss or silent reconstruction fails closed.

---

# 11. Runtime result and receipt truth

`StandardInferResult` must expose final runtime evidence rather than only request-side values:

```text
sampling_owner
sampling_policy_id
sampling_policy_definition_digest
sampling_request_contract_digest
request_canonical_snapshot
runtime_initial_snapshot
post_structure_routing_snapshot
final_sampler_snapshot
attempted_locked_field_mutation_count
attempted_locked_fields
canonical_reassertion_applied
final_sampling_scalar_parity
finalizer_execution_count
```

Sampler-01 and R1A route receipts must consume these runtime fields. Missing final evidence produces `TypedPolicyFinalEvidenceMissing`; it must not be reconstructed from the request.

---

# 12. Local Rust audit gate

Add:

```text
ash_decode_sampler_02_r1a_typed_policy_ownership_gate
```

The binary runs a deterministic ownership matrix without loading a model or claiming language quality.

Required matrix:

```text
3 policies x 8 ownership/drift/retry scenarios = 24 cases
```

Each case validates canonical profile, envelope propagation, drift detection, canonical reassertion, digest stability, free-form conflict behavior, and retry preservation.

The Rust binary creates all manifests and runtime artifacts locally under the requested output directory. Generated JSON is never committed with the source patch.

Per-case outputs:

```text
workspace/runtime/decode/r1a/cases/<case_id>/
  request.json
  stdout.jsonl
  stderr.log
  ownership_receipt.json
  route_receipt.json
  case_result.json
```

Top-level outputs:

```text
workspace/runtime/decode/
  ash_decode_sampler_02_r1a_typed_policy_final_sampling_ownership_runtime_artifact.json
  ash_decode_sampler_02_r1a_local_manifest.json
  ash_decode_sampler_02_r1a_parent_binding_receipt.json
  ash_decode_sampler_02_r1a_source_inventory_receipt.json
  ash_decode_sampler_02_r1a_canonical_policy_profile_receipt.json
  ash_decode_sampler_02_r1a_duplicate_definition_guard.json
  ash_decode_sampler_02_r1a_ownership_envelope_receipt.json
  ash_decode_sampler_02_r1a_freeform_conflict_matrix_receipt.json
  ash_decode_sampler_02_r1a_runtime_propagation_receipt.json
  ash_decode_sampler_02_r1a_post_routing_drift_receipt.json
  ash_decode_sampler_02_r1a_final_sampling_snapshot_receipt.json
  ash_decode_sampler_02_r1a_retry_preservation_receipt.json
  ash_decode_sampler_02_r1a_execution_matrix_receipt.json
  ash_decode_sampler_02_r1a_static_checks.json
  ash_decode_sampler_02_r1a_no_default_mutation_guard.json
  ash_decode_sampler_02_r1a_model_quality_claim_guard.json
  ash_decode_sampler_02_r1a_verdict.json
```

The local manifest hashes every top-level artifact and every per-case output.

---

# 13. Required tests

Unit tests:

```text
canonical policy scalar exactness
policy digest stability
request contract digest stability
matching free-form aliases accepted
conflicting aliases rejected
ownership envelope round trip
single-field drift restoration
multi-field drift restoration
unlocked-field preservation
missing typed envelope rejection
seed drift detection and restoration
EOS rerun ownership preservation
```

Integration tests:

```text
request -> typed policy -> canonical override -> runtime config
-> structure routing -> finalizer -> runtime summary -> route receipt
```

Assertions:

```text
requested policy equals final policy
canonical snapshot equals final sampler snapshot
runtime owner equals typed_policy_final
owner count equals one
conflicting request executes zero inference
structure mutation does not survive
EOS rerun preserves ownership
fixed-seed replay reproduces ownership and scalar digests
```

---

# 14. Canonical failure reasons

```text
TypedPolicyFreeformConflict
TypedPolicyOwnershipEnvelopeMissing
TypedPolicyOverrideCanonicalMismatch
TypedPolicySeedContractMismatch
TypedPolicyOwnershipLostAtRuntimeBoundary
TypedPolicyOwnershipLostAcrossRerun
TypedPolicyFinalizationMissing
TypedPolicyFinalScalarMismatch
TypedPolicyOwnerCountInvalid
TypedPolicyFinalEvidenceMissing
CanonicalPolicyDefinitionDuplicated
```

Stable reason strings are required. Generic replacement errors are forbidden where a canonical reason applies.

---

# 15. Required predicates

```text
ASH_DECODE_SAMPLER_02_R1A_PARENT_BINDING_PASS
ASH_DECODE_SAMPLER_02_R1A_CANONICAL_POLICY_PROFILE_SSOT
ASH_DECODE_SAMPLER_02_R1A_NO_DUPLICATE_POLICY_SCALAR_DEFINITION
ASH_DECODE_SAMPLER_02_R1A_TYPED_POLICY_OWNER_COUNT_ONE
ASH_DECODE_SAMPLER_02_R1A_FREEFORM_CONFLICT_FAIL_CLOSED
ASH_DECODE_SAMPLER_02_R1A_POLICY_IDENTITY_PRESERVED_TO_RUNTIME
ASH_DECODE_SAMPLER_02_R1A_POLICY_IDENTITY_PRESERVED_TO_FINAL_SAMPLER
ASH_DECODE_SAMPLER_02_R1A_LOCKED_FIELDS_DECLARED
ASH_DECODE_SAMPLER_02_R1A_POST_ROUTING_DRIFT_MEASURED
ASH_DECODE_SAMPLER_02_R1A_FINAL_CANONICAL_REASSERTION_BOUND
ASH_DECODE_SAMPLER_02_R1A_FINAL_SAMPLING_SCALAR_PARITY
ASH_DECODE_SAMPLER_02_R1A_SALAD_TYPED_POLICY_MUTATION_ZERO
ASH_DECODE_SAMPLER_02_R1A_EOS_RERUN_OWNERSHIP_PRESERVED
ASH_DECODE_SAMPLER_02_R1A_FIXED_SEED_CONTRACT_PRESERVED
ASH_DECODE_SAMPLER_02_R1A_NO_DEFAULT_POLICY_MUTATION
ASH_DECODE_SAMPLER_02_R1A_NO_MODEL_QUALITY_OVERCLAIM
ASH_DECODE_SAMPLER_02_R1A_STATIC_CHECKS_PASS
ASH_DECODE_SAMPLER_02_R1A_RUNTIME_MATRIX_PASS
```

---

# 16. PASS semantics

PASS means:

```text
parent source inventory bound
one canonical typed-policy scalar definition
orchestrator duplicate scalar definition removed
policy and owner identity reach runtime
all locked fields reach runtime
runtime validates canonical override and digests
post-routing drift is measured honestly
canonical locked fields are reasserted before token selection
final sampler snapshot equals canonical request snapshot
free-form conflicts fail before inference
SALAD cannot mutate typed policy
EOS rerun preserves ownership and contract
route receipts use final runtime evidence
no default policy promotion
no model quality claim
```

PASS does not mean:

```text
structure-routing mutation source removed
greedy route proven contamination-free
sampled policy proven superior
default sampling policy changed
production decode promoted
checkpoint-model-tokenizer binding proven
persistent session enabled
single model load enabled
```

---

# 17. Safety and honesty

Required false:

```text
model_quality_claimed
translation_quality_claimed
korean_grammar_claimed
sft_alignment_claimed
production_decode_ready_claimed
default_sampler_policy_promoted
structure_routing_bias_source_removed_claimed
greedy_contamination_absent_claimed
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
persistent_session_activation_count
single_model_load_activation_count
```

---

# 18. Build and execution

```powershell
cargo fmt --manifest-path crates/model_core/Cargo.toml -- --check
cargo fmt --manifest-path crates/runtime/Cargo.toml -- --check
cargo fmt --manifest-path crates/orchestrator_local/Cargo.toml -- --check

cargo check --manifest-path crates/model_core/Cargo.toml
cargo check --manifest-path crates/runtime/Cargo.toml
cargo check --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_decode_sampler_02_r1a_typed_policy_ownership_gate

cargo run --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_decode_sampler_02_r1a_typed_policy_ownership_gate `
  -- `
  --repo-root . `
  --out-dir workspace/runtime/decode
```

The audit binary, not the source archive, owns creation of the manifest and runtime artifacts.

---

# 19. Verdict

PASS:

```text
status=PASS
ready_for_sampler_02_r1b=true
ready_for_sampler_02_r1b_scope=structure_routing_sampling_bias_source_suppression_only
ready_for_greedy_contamination_gate=false
ready_for_default_sampler_policy_promotion=false
ready_for_production_decode_promotion=false
```

HOLD reasons include:

```text
canonical_policy_definition_duplicated
runtime_policy_identity_missing
runtime_owner_identity_missing
finalizer_not_bound_to_all_active_paths
final_sampler_scalar_mismatch
freeform_conflict_executed_inference
retry_ownership_mismatch
runtime_evidence_missing
compile_truth_missing
```

R1A closes one question only:

```text
When decodeSamplerPolicy is present, which component owns the final values of
 temperature, top_p, top_k, min_p, and seed consumed by the sampler?
```

Required answer after PASS:

```text
The typed policy is the sole final owner.
Downstream routes may not leave persistent drift on locked fields.
Every attempted drift is measured.
The final sampler consumes the canonical typed-policy scalar snapshot.
```
