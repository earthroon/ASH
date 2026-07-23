# ASH-DECODE-SAMPLER-02-R1F

## Live Inference Binding Propagation /
## Single Verified Model Instance Ownership /
## Tokenizer-Model-Decode Session Binding /
## Cache and KV Identity Carry-Through /
## Bound Runtime Receipt End-to-End Seal

---

# 0. Patch identity

```text
patch_id=ASH-DECODE-SAMPLER-02-R1F
parent_patch_id=ASH-DECODE-SAMPLER-02-R1E
patch_class=live_decode_runtime_binding_propagation_hardening
runtime_schema=ash.decode.sampler.02.r1f.live_inference_binding.runtime_artifact.v1
primary_artifact=workspace/runtime/decode/ash_decode_sampler_02_r1f_live_inference_binding_runtime_artifact.json
local_manifest=workspace/runtime/decode/ash_decode_sampler_02_r1f_local_manifest.json
r1e_spec_commit=d64c020a70ddbdbd9f1294d800673f843a8e81a6
parent_r1e_archive_sha256=ec110f6121f06c4fc6e243e47c8c5411df2f9894c3df79ef0dd520d453a5d538
```

Required parent evidence is the complete R1A through R1E artifact and manifest chain. Every manifest must hash-bind its referenced primary artifact. A copied PASS marker is not evidence.

---

# 1. Parent truth and remaining gap

R1E proves the exact checkpoint, model specification, tokenizer manifest, ordered vocabulary, special-token contract, tensor vocabulary shape, and adapter overlay identity before inference. It rejects cross-model receipts by `effective_runtime_binding_digest`.

R1E does not yet prove that the same verified identity is physically carried by every live object participating in generation. Current pre-R1F gaps include:

```text
VerifiedDecodeRuntimeBinding held as an infer-local value
NativeWgpuModel and ReferenceModel without direct verified binding ownership
NativeTokenizer without a bound runtime instance identity
GenerationSamplingConfig without a decode-session contract
GenerationTelemetry without model/tokenizer/session identity
DecodeState and KvCache without binding ownership
cache reuse decisions without exact model/session digest checks
candidate and result bindings reconstructed after generation
reference/CPU paths allowed to return without bound telemetry
```

R1F changes binding from result decoration into live execution ownership.

---

# 2. Purpose

Establish one unbroken authority chain:

```text
VerifiedDecodeRuntimeBinding
-> BoundTokenizerRuntimeIdentity
-> VerifiedModelInstanceBinding
-> BoundDecodeSessionContract
-> GenerationSamplingConfig
-> DecodeState / KvCache / cache objects
-> GenerationTelemetry and per-step receipts
-> StandardInferCandidateOutput
-> StandardInferResult
-> orchestrator route receipt
```

Every live object and receipt must agree on:

```text
effective_runtime_binding_digest
model_instance_id
tokenizer_instance_id
decode_session_id
```

Missing or mismatched identity fails closed. Request-side or result-side reconstruction is forbidden.

---

# 3. Canonical types and helpers

Extend:

```text
crates/model_core/src/decode_runtime_binding.rs
```

Required types:

```text
BoundModelBackendKind
VerifiedModelInstanceBinding
BoundTokenizerRuntimeIdentity
BoundDecodeSessionContract
BoundRuntimeObjectKind
BoundRuntimeObjectIdentity
BoundRuntimeBindingEndToEndReceipt
```

Required helpers:

```text
ordered_token_ids_digest
build_verified_model_instance_binding
build_bound_tokenizer_runtime_identity
build_bound_decode_session_contract
verify_runtime_object_binding
verify_bound_runtime_object_identity
verify_end_to_end_decode_binding
```

All identity builders are deterministic and content-derived. Pointer addresses, wall-clock timestamps, and process-random values are forbidden as the sole identity source.

---

# 4. Verified model instance ownership

Each model instance receives one immutable `VerifiedModelInstanceBinding` before its first authoritative forward.

The binding includes:

```text
model_instance_id
backend kind
base runtime binding digest
effective runtime binding digest
checkpoint set digest
model spec semantic digest
overlay digest
instance epoch
binding receipt digest
```

Per request or decode session:

```text
active_authoritative_model_instance_count=1
simultaneously_authoritative_model_instance_count=1
model_instance_binding_switch_count=0
```

Native-to-reference fallback is allowed only when the original instance is retired before any authoritative result commit and the replacement has the same verified runtime binding. Cross-binding fallback and dual authority are rejected.

---

# 5. Bound tokenizer runtime identity

Tokenizer construction produces `BoundTokenizerRuntimeIdentity` containing:

```text
tokenizer_instance_id
tokenizer semantic digest
ordered vocabulary digest
special-token contract digest
effective runtime binding digest
binding receipt digest
```

Prompt encoding produces an ordered prompt-token digest bound to the tokenizer instance. Equal input text under different vocabularies or token mappings is a different prompt identity.

Required prompt receipt:

```text
input text SHA-256
ordered prompt token digest
prompt token count
tokenizer instance id
effective runtime binding digest
```

---

# 6. Decode session contract

Create one immutable `BoundDecodeSessionContract` after model and tokenizer binding and before generation.

The session identity binds:

```text
request identity
session epoch
model instance id
tokenizer instance id
effective runtime binding digest
ordered prompt token digest
sampling policy definition digest
sampling request contract digest
EOS authority contract digest
session contract digest
```

Lifecycle:

```text
Created
-> ModelBound
-> TokenizerBound
-> PromptBound
-> SamplingBound
-> GenerationActive
-> GenerationFinalized
```

A finalized session may not mutate KV or generation telemetry. `request_id` alone is never accepted as a session identity.

---

# 7. Sampling and telemetry carry-through

`GenerationSamplingConfig` carries optional bound values during migration:

```text
decode_session_contract
model_instance_binding
tokenizer_runtime_identity
```

A bound generation route requires all three and exact digest parity.

`GenerationTelemetry` carries:

```text
decode_session_contract
model_instance_binding
tokenizer_runtime_identity
effective_runtime_binding_digest
runtime_object_identity
bound_generation_steps
unbound_generation_steps
binding_mismatch_steps
model_instance_switch_steps
decode_session_switch_steps
```

Every generation step records:

```text
decode_session_id
model_instance_id
effective_runtime_binding_digest
```

Bound routes require:

```text
unbound_generation_steps=0
binding_mismatch_steps=0
model_instance_switch_steps=0
decode_session_switch_steps=0
```

---

# 8. DecodeState and KV identity

`DecodeState` and `KvCache` own a `BoundRuntimeObjectIdentity`.

Required identity fields:

```text
object kind
object instance id
model instance id
decode session id
effective runtime binding digest
object epoch
binding receipt digest
```

Every KV read, append, truncate, reset, and reuse validates exact identity parity.

Forbidden:

```text
cross-model KV reuse
cross-tokenizer KV reuse
cross-prompt KV reuse
cross-session KV reuse
KV mutation after session finalization
unbound KV reuse on a bound route
```

The current request-local path expects:

```text
cross_session_kv_reuse_count=0
```

---

# 9. Cache identity carry-through

The following caches and runtime objects must carry or verify `BoundRuntimeObjectIdentity`:

```text
model instance core
vocabulary atlas
embedding row-gather cache
lm_head atlas
GPU sampling runtime
GPU penalty runtime
KV cache
domain adapter weight cache
domain adapter delta buffer
readback staging and token-dependent sampler slots
```

Rules:

```text
same effective binding + same model instance + compatible session -> reuse may be permitted
different effective binding -> reject or hard purge
different model instance where instance-local -> reject or purge
different decode session where session-local -> reject
missing identity -> no reuse on bound route
```

No silent cache-key downgrade to path, model id, vocab size, token count, or device id is allowed.

---

# 10. End-to-end result origin

`StandardInferCandidateOutput` and `StandardInferResult` propagate binding only from live generation telemetry.

Required fields:

```text
model_instance_binding
tokenizer_runtime_identity
decode_session_contract
runtime_object_identity
binding_origin
binding_origin_receipt_digest
model_instance_id
tokenizer_instance_id
decode_session_id
effective_runtime_binding_digest
```

Required origin:

```text
binding_origin=live_generation_carry_through
```

Forbidden:

```text
result binding reconstructed from request-local VerifiedDecodeRuntimeBinding
candidate binding reconstructed after generation
binding digest inserted only during route receipt assembly
reference path returning telemetry=None on a claimed bound route
```

Required zeros:

```text
result_binding_reconstruction_count=0
candidate_binding_reconstruction_count=0
route_receipt_binding_reconstruction_count=0
```

---

# 11. Fallback ownership

A fallback may become authoritative only if:

```text
prior model instance made no authoritative commit
prior model instance is explicitly retired
replacement uses identical effective runtime binding
replacement receives a new verified model instance id
one model remains authoritative
session ownership transition is explicitly receipted
```

Forbidden:

```text
native and CPU both authoritative
native result silently replaced after commit
fallback with different checkpoint/tokenizer/overlay digest
binding-free CPU reference result
```

---

# 12. Runtime and orchestrator propagation

Runtime creates model/tokenizer/session identity and binds generation before the first decode step. Orchestrator consumes runtime evidence and may not synthesize or repair missing identity.

The active route receipt verifies exact equality between:

```text
R1E verified runtime binding
model instance binding
tokenizer runtime identity
decode session contract
KV/cache identity
generation telemetry
candidate output
final result
```

Mismatch yields a canonical rejection and no fallback.

---

# 13. Audit gate

Add:

```text
crates/orchestrator_local/src/bin/ash_decode_sampler_02_r1f_live_inference_binding_propagation_gate.rs
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
--r1d-parent-artifact
--r1d-parent-manifest
--r1e-parent-artifact
--r1e-parent-manifest
--runtime-profile
--full-checkpoint-hash
--run-live-smoke
--out-dir
```

Default gate mode:

```text
run_live_smoke=false
```

It performs:

```text
R1A-R1E parent hash validation
real R1E bundle reconstruction and verification
production model/tokenizer/session/object identity construction
64 deterministic positive and negative cases
static live-route surface inspection
no-mutation and no-quality-overclaim checks
```

Case matrix:

```text
12 model-instance ownership cases
12 tokenizer/session binding cases
8 KV identity cases
8 cache identity cases
12 telemetry/result propagation cases
12 fallback and negative-control cases
case_count=64
```

`--run-live-smoke true` must fail closed until the gate invokes the canonical live runtime path and captures real bound telemetry. It may not claim a live smoke from synthetic helper execution.

---

# 14. Negative controls

Required rejected controls include:

```text
model instance binding digest mismatch
tokenizer vocabulary digest mismatch
prompt token digest mismatch
decode session id mismatch
KV cross-session reuse
KV cross-model reuse
vocab atlas cross-model reuse
GPU sampler cross-model reuse
domain adapter overlay mismatch
CPU fallback binding mismatch
native/reference dual authority
result binding post-hoc reconstruction
missing binding digest
unbound generation step
model instance switch during generation
session switch during generation
```

Every rejection must report:

```text
rejected=true
fallback_used=false
```

---

# 15. Required local artifacts

```text
workspace/runtime/decode/
  ash_decode_sampler_02_r1f_live_inference_binding_runtime_artifact.json
  ash_decode_sampler_02_r1f_local_manifest.json
  ash_decode_sampler_02_r1f_parent_binding_receipt.json
  ash_decode_sampler_02_r1f_source_inventory_receipt.json
  ash_decode_sampler_02_r1f_real_bundle_verification_receipt.json
  ash_decode_sampler_02_r1f_model_instance_ownership_receipt.json
  ash_decode_sampler_02_r1f_tokenizer_runtime_identity_receipt.json
  ash_decode_sampler_02_r1f_decode_session_contract_receipt.json
  ash_decode_sampler_02_r1f_kv_identity_receipt.json
  ash_decode_sampler_02_r1f_cache_identity_receipt.json
  ash_decode_sampler_02_r1f_generation_telemetry_binding_receipt.json
  ash_decode_sampler_02_r1f_candidate_result_binding_receipt.json
  ash_decode_sampler_02_r1f_fallback_ownership_receipt.json
  ash_decode_sampler_02_r1f_end_to_end_binding_receipt.json
  ash_decode_sampler_02_r1f_static_checks.json
  ash_decode_sampler_02_r1f_no_mutation_guard.json
  ash_decode_sampler_02_r1f_model_quality_claim_guard.json
  ash_decode_sampler_02_r1f_verdict.json
```

Per-case artifacts are placed under `workspace/runtime/decode/r1f/cases/<case_id>/`.

Generated artifacts, manifests, receipts, and case directories are excluded from the source bake archive.

---

# 16. Canonical failures

```text
R1EParentEvidenceIncomplete
VerifiedModelInstanceBindingMissing
VerifiedModelInstanceBindingMismatch
MultipleAuthoritativeModelInstances
ModelInstanceSwitchedDuringGeneration
TokenizerRuntimeIdentityMissing
TokenizerRuntimeIdentityMismatch
PromptTokenDigestMismatch
DecodeSessionContractMissing
DecodeSessionContractMismatch
DecodeSessionSwitchedDuringGeneration
GenerationStepUnbound
GenerationStepBindingMismatch
KvBindingMissing
KvCrossModelReuseRejected
KvCrossSessionReuseRejected
CacheBindingMissing
CacheCrossModelReuseRejected
CacheCrossSessionReuseRejected
FallbackBindingMismatch
DualModelAuthorityObserved
ResultBindingReconstructed
CandidateBindingReconstructed
RouteReceiptBindingReconstructed
BoundRuntimeEndToEndMismatch
LiveSmokeRequiresCanonicalRuntimeInvocation
CompileTruthMissing
```

---

# 17. PASS formula

```text
PASS =
  r1a_parent_binding_pass
  && r1b_parent_binding_pass
  && r1c_parent_binding_pass
  && r1d_parent_binding_pass
  && r1e_parent_binding_pass
  && compile_truth_pass
  && real_r1e_bundle_verification_pass
  && deterministic_case_count==64
  && deterministic_case_fail_count==0
  && active_authoritative_model_instance_count==1
  && simultaneously_authoritative_model_instance_count==1
  && model_instance_switch_count==0
  && tokenizer_binding_mismatch_count==0
  && decode_session_binding_mismatch_count==0
  && cross_model_kv_accept_count==0
  && cross_session_kv_accept_count==0
  && cross_model_cache_accept_count==0
  && cross_session_cache_accept_count==0
  && unbound_generation_steps==0
  && binding_mismatch_steps==0
  && result_binding_reconstruction_count==0
  && candidate_binding_reconstruction_count==0
  && cross_binding_fallback_accept_count==0
  && default_policy_mutation_count==0
  && model_quality_claim_count==0
```

PASS proves deterministic production binding APIs, runtime surface propagation, parent binding, and negative-control rejection. With `run_live_smoke=false`, PASS does not prove a real model forward was executed under the new session contract. It does not prove model quality, persistent session promotion, throughput, or production readiness.

---

# 18. Build and run

```powershell
cargo check --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_decode_sampler_02_r1f_live_inference_binding_propagation_gate
```

```powershell
cargo run --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_decode_sampler_02_r1f_live_inference_binding_propagation_gate `
  -- `
  --repo-root . `
  --r1a-parent-artifact workspace/runtime/decode/ash_decode_sampler_02_r1a_typed_policy_final_sampling_ownership_runtime_artifact.json `
  --r1a-parent-manifest workspace/runtime/decode/ash_decode_sampler_02_r1a_local_manifest.json `
  --r1b-parent-artifact workspace/runtime/decode/ash_decode_sampler_02_r1b_structure_sampling_bias_suppression_runtime_artifact.json `
  --r1b-parent-manifest workspace/runtime/decode/ash_decode_sampler_02_r1b_local_manifest.json `
  --r1c-parent-artifact workspace/runtime/decode/ash_decode_sampler_02_r1c_greedy_control_contamination_runtime_artifact.json `
  --r1c-parent-manifest workspace/runtime/decode/ash_decode_sampler_02_r1c_local_manifest.json `
  --r1d-parent-artifact workspace/runtime/decode/ash_decode_sampler_02_r1d_minimum_new_token_eos_single_owner_runtime_artifact.json `
  --r1d-parent-manifest workspace/runtime/decode/ash_decode_sampler_02_r1d_local_manifest.json `
  --r1e-parent-artifact workspace/runtime/decode/ash_decode_sampler_02_r1e_checkpoint_model_tokenizer_binding_runtime_artifact.json `
  --r1e-parent-manifest workspace/runtime/decode/ash_decode_sampler_02_r1e_local_manifest.json `
  --runtime-profile specs/runtime_profile_v5_48259.toml `
  --full-checkpoint-hash true `
  --run-live-smoke false `
  --out-dir workspace/runtime/decode
```

Expected PASS token:

```text
PASS_ASH_DECODE_SAMPLER_02_R1F_LIVE_INFERENCE_BINDING_PROPAGATION_SINGLE_VERIFIED_MODEL_INSTANCE_TOKENIZER_MODEL_DECODE_SESSION_BINDING_CACHE_KV_IDENTITY_CARRY_THROUGH_BOUND_RUNTIME_RECEIPT_END_TO_END_NO_MUTATION_NO_MODEL_QUALITY_OVERCLAIM
```

Expected outputs:

```text
primary_artifact=workspace/runtime/decode/ash_decode_sampler_02_r1f_live_inference_binding_runtime_artifact.json
manifest=workspace/runtime/decode/ash_decode_sampler_02_r1f_local_manifest.json
```

---

# 19. Promotion boundary

On PASS with `run_live_smoke=false`:

```text
status=PASS
production_binding_api_sealed=true
live_forward_receipt_proven=false
ready_for_r1f_live_smoke_closure=true
ready_for_default_sampler_policy_promotion=false
ready_for_production_decode_promotion=false
```
