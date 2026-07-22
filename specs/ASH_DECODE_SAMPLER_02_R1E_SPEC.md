# ASH-DECODE-SAMPLER-02-R1E

## Checkpoint / Model / Tokenizer Binding Gate /
## EOS Identity Provenance /
## Runtime Vocabulary and Special-Token Contract /
## Decode Artifact Parent Binding /
## Cross-Model Receipt Rejection Seal

---

# 0. Patch identity

```text
patch_id=ASH-DECODE-SAMPLER-02-R1E
parent_patch_id=ASH-DECODE-SAMPLER-02-R1D
patch_class=decode_runtime_identity_binding_hardening
runtime_schema=ash.decode.sampler.02.r1e.checkpoint_model_tokenizer_binding.runtime_artifact.v1
primary_artifact=workspace/runtime/decode/ash_decode_sampler_02_r1e_checkpoint_model_tokenizer_binding_runtime_artifact.json
local_manifest=workspace/runtime/decode/ash_decode_sampler_02_r1e_local_manifest.json
r1a_spec_commit=6e5f461dd036e9a05a63977f3acb0a2d46cd6e4d
r1b_spec_commit=782aad4b002f4b7d2c7a5c4b8b4eb5329f826d21
r1c_spec_commit=348f39b410bea042781ba19aa79b65b3cc950bf7
r1d_spec_commit=3f77e0eae377d5d2e3f461850fe019ed99d57af5
parent_r1d_archive_sha256=f97f3ebd491d6bd738f5e3cdf96ef25fcfc1e35c3d8ab1b8ea551f8631fbde64
```

Required parent evidence:

```text
workspace/runtime/decode/ash_decode_sampler_02_r1a_typed_policy_final_sampling_ownership_runtime_artifact.json
workspace/runtime/decode/ash_decode_sampler_02_r1a_local_manifest.json
workspace/runtime/decode/ash_decode_sampler_02_r1b_structure_sampling_bias_suppression_runtime_artifact.json
workspace/runtime/decode/ash_decode_sampler_02_r1b_local_manifest.json
workspace/runtime/decode/ash_decode_sampler_02_r1c_greedy_control_contamination_runtime_artifact.json
workspace/runtime/decode/ash_decode_sampler_02_r1c_local_manifest.json
workspace/runtime/decode/ash_decode_sampler_02_r1d_minimum_new_token_eos_single_owner_runtime_artifact.json
workspace/runtime/decode/ash_decode_sampler_02_r1d_local_manifest.json
```

The gate must hash-validate every parent manifest and the exact referenced primary artifact. Copied PASS markers, matching names, and matching patch ids are not sufficient evidence.

---

# 1. Parent truth and remaining gap

R1A through R1D prove algorithmic ownership:

```text
R1A typed policy scalar ownership
R1B structure-routing locked-field mutation suppression
R1C greedy raw-argmax and selected-token purity
R1D minimum-new-token EOS single authority
```

They do not prove that a receipt belongs to one exact checkpoint, model specification, tokenizer manifest, vocabulary ordering, special-token mapping, or adapter overlay. R1E is the first runtime-model-bound artifact in this chain.

Current gaps:

```text
checkpoint probe occurs after generation
mismatch and missing provenance are warning-only
unknown checkpoint fingerprint fallback exists
only the first checkpoint file is runtime-hashed
multi-file checkpoint order and completeness are not sealed
model_spec_id and tokenizer_manifest_id are labels, not content identity
matching vocab size does not prove matching token-id ordering
checkpoint-declared special tokens are not separated from runtime tokenizer values
receipt joins do not require exact runtime binding digest
cross-model receipt reuse is not fail-closed
```

---

# 2. Purpose

Create one immutable contract before tokenizer construction, prompt encoding, model construction, upload, or generation:

```text
ordered checkpoint component set
+ model specification
+ tokenizer manifest
+ ordered id-to-token vocabulary
+ special-token identities
+ embedding/lm_head vocabulary tensor contract
+ ordered active adapter overlay
-> VerifiedDecodeRuntimeBinding
```

Required truth:

```text
verified_before_model_load=true
verified_before_prompt_encode=true
verified_before_generation=true
checkpoint/model/tokenizer mismatch fails closed
all live decode receipts carry one effective_runtime_binding_digest
cross-model and unbound live receipts are rejected
fallback_used=false
unknown checkpoint fallback count=0
```

---

# 3. Canonical ownership

Add:

```text
crates/model_core/src/decode_runtime_binding.rs
```

Canonical types:

```text
CheckpointComponentFingerprint
CheckpointSetBinding
SpecialTokenIdContract
ModelSpecBinding
VocabularyBinding
SpecialTokenIdentity
SpecialTokenContract
TokenizerBinding
CheckpointTensorVocabularyContract
EffectiveModelOverlayBinding
DecodeRuntimeBindingContract
VerifiedDecodeRuntimeBinding
DecodeArtifactBindingEnvelope
DecodeReceiptBindingRejection
CheckpointDeclaredMetadata
DecodeRuntimeBindingBuildReceipt
DecodeRuntimeBindingBuildInput
```

Canonical production functions:

```text
sha256_file_streaming
build_checkpoint_set_binding
model_spec_semantic_digest
build_model_spec_binding
tokenizer_vocab_digest
build_tokenizer_binding
build_checkpoint_tensor_vocab_contract
build_effective_model_overlay_binding
build_verified_decode_runtime_binding
verify_decode_receipt_binding
build_decode_artifact_binding_envelope
```

Model core owns binding identity. Runtime owns pre-load construction and propagation. Orchestrator owns parent validation and local receipts only.

---

# 4. Checkpoint component set

Every resolved checkpoint component is processed in loader order.

Per component:

```text
logical_index
stable file_name
byte_len
full streaming SHA-256
safetensors tensor_inventory_digest
tensor_count
```

Set digest requirements:

```text
path-independent
order-sensitive
content-sensitive
component-count-sensitive
```

The following must change identity or fail:

```text
missing shard
extra shard
shard order change
same file name with different content
duplicate resolved component
ambiguous tensor name across components
sidecar component count mismatch
sidecar ordered set digest mismatch
```

`checkpoint_sha256` from a legacy single-file sidecar is not silently treated as a multi-file ordered set digest.

Full checkpoint hashing is mandatory for R1E. An in-process verified hash cache is permitted only after one successful streaming hash and only while canonical path, size, high-resolution modification time, process epoch, and prior verified content digest still match.

---

# 5. Model specification binding

Bind both:

```text
raw model-spec file SHA-256
canonical semantic model-spec digest
```

Semantic contract includes model identity, architecture, dimensions, embedding contract, attention, rope, normalization, MLP, backend, vocab size, and special-token ids.

Matching `model_spec_id` without matching content is rejected.

---

# 6. Tokenizer and vocabulary binding

Bind both:

```text
raw tokenizer manifest SHA-256
canonical tokenizer semantic digest
```

Vocabulary contract must prove:

```text
token ids unique
token strings unique
id domain dense from 0 to vocab_size-1
max_token_id=vocab_size-1
ordered id-token sequence digest
reserved-token sequence digest
model-spec vocab size parity
```

Same vocab size with different ordering, token strings, reserved mapping, or token ids is rejected.

The manifest-declared hash is comparison evidence only. It never replaces hashing the actual loaded file or runtime vocabulary.

---

# 7. Special-token and EOS provenance

Keep checkpoint, model-spec, tokenizer-manifest, and vocabulary-entry sources distinct.

For PAD/BOS/EOS/UNK prove:

```text
token id in range
ids unique
token string non-empty
tokenizer manifest id/string matches vocabulary entry
model-spec id matches tokenizer id
checkpoint-declared id matches when checkpoint provenance is present
```

EOS required equality:

```text
checkpoint-declared EOS id, when present
== model spec eos_id
== tokenizer manifest EOS id
== vocabulary entry id for EOS token string
== runtime R1D authority EOS id
```

Missing checkpoint declaration is represented as absent provenance, not synthesized from the runtime tokenizer. Mismatch fails before generation.

---

# 8. Tensor vocabulary contract

Read safetensors headers without loading tensor payloads and locate embedding and lm_head tensors.

Required checks:

```text
embedding tensor exists
lm_head exists or is explicitly tied to embedding
embedding vocab axis matches tokenizer vocab
lm_head vocab axis matches tokenizer vocab
model-spec vocab matches tokenizer vocab
embedding hidden dimension matches model hidden size
lm_head hidden dimension matches model hidden size
ambiguous duplicate tensor names rejected
```

The contract is content-bound through tensor names, shapes, hidden size, vocab size, and its own digest.

---

# 9. Effective model overlay

Active LoRA/adapter context contributes to the effective identity:

```text
ordered adapter ids
ordered adapter source file hashes or deterministic inline identity
exact f32 effective scales via to_bits()
ordered adapter revisions when present
overlay digest
```

Base identity:

```text
checkpoint set
+ model spec
+ tokenizer/vocabulary/special tokens
+ checkpoint tensor vocabulary contract
-> base_runtime_binding_digest
```

Effective identity:

```text
base_runtime_binding_digest
+ ordered overlay digest
-> effective_runtime_binding_digest
```

Different adapter order or scale is a different effective runtime identity.

---

# 10. Fail-closed pre-load gate

Required runtime order:

```text
resolve request paths
load model spec and tokenizer manifest as identity inputs
load adapter metadata required for overlay identity
build and verify runtime binding
construct tokenizer
encode prompt
construct/load model instance
upload tensors
run generation
```

Forbidden order:

```text
generation -> post-generation checkpoint probe -> warning
```

Failures must return an error. They may not downgrade to `provenance_missing`, `unknown_checkpoint_fingerprint`, path-only identity, id-only identity, size-only identity, or best-effort continuation.

---

# 11. Runtime propagation

`CheckpointFingerprintProbe` remains a compatibility surface but is derived from the verified binding.

It must distinguish:

```text
checkpoint_special_token_ids
runtime_tokenizer_special_token_ids
verified_runtime_binding_digest
checkpoint_set_digest
```

`StandardInferResult` and `StandardInferCandidateOutput` propagate:

```text
verified_decode_runtime_binding
base_runtime_binding_digest
effective_runtime_binding_digest
checkpoint_set_digest
model_spec_semantic_digest
tokenizer_vocab_digest
special_token_contract_digest
overlay_digest
```

The active route receipt consumes these runtime values directly and verifies exact equality against the embedded verified binding.

Request-side reconstruction is forbidden.

---

# 12. Artifact binding and parent lineage

R1A through R1D are classified as:

```text
binding_scope=algorithmic_unbound
evidence_class=synthetic_algorithmic_gate
```

R1E is classified as:

```text
binding_scope=runtime_model_bound
evidence_class=verified_runtime_bundle
```

The artifact envelope includes:

```text
patch_id
artifact_sha256
ordered parent artifact hashes
binding scope
base runtime binding digest
effective runtime binding digest
evidence class
```

Algorithmic parent evidence may prove algorithms, but may not be reused as live model-bound generation evidence.

---

# 13. Cross-model receipt rejection

All live receipts produced after the pre-load gate must satisfy:

```text
receipt.effective_runtime_binding_digest
== active_verified_binding.effective_runtime_binding_digest
```

Missing digest:

```text
RuntimeBindingDigestMissing
rejected=true
fallback_used=false
```

Different digest:

```text
CrossModelDecodeReceiptRejected
rejected=true
fallback_used=false
```

Matching file names, model ids, tokenizer ids, vocab sizes, or special-token ids are not substitutes for the full digest.

Receipts covered include sampling ownership, structure bias, greedy purity, EOS authority, generation telemetry, candidate output, and active route receipt.

---

# 14. Model-instance and cache identity

The effective runtime binding digest is the identity component for:

```text
NativeWgpuModel instance
vocab atlas
embedding row-gather cache
lm_head atlas
KV cache
tokenizer lookup
special-token lookup
token-id banlist projection
token-dependent sampler slot
```

Rules:

```text
same digest -> reuse permitted
different digest -> cache miss or hard purge
missing digest -> reuse forbidden
```

R1E seals identity ownership only. Persistent session and single-model-load promotion remain later scope.

---

# 15. Audit gate

Add:

```text
crates/orchestrator_local/src/bin/ash_decode_sampler_02_r1e_checkpoint_model_tokenizer_binding_gate.rs
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
--runtime-profile
--model-spec
--tokenizer-manifest
--checkpoint, repeatable
--checkpoint-fingerprint-sidecar
--full-checkpoint-hash
--out-dir
```

The gate performs:

```text
parent artifact and manifest hash validation
real local checkpoint/model/tokenizer bundle verification
full ordered checkpoint hashing
safetensors tensor inventory and shape verification
EOS multi-source provenance verification
16 same-binding positive cases
32 cross-model, mismatch, and missing-binding negative controls
minimum synthetic case count=48
static source checks
no-mutation and no-quality-overclaim guards
```

Every negative case must be rejected without fallback. Same-token or same-size coincidences do not pass.

---

# 16. Required artifacts

Rust locally creates under `workspace/runtime/decode`:

```text
ash_decode_sampler_02_r1e_checkpoint_model_tokenizer_binding_runtime_artifact.json
ash_decode_sampler_02_r1e_local_manifest.json
ash_decode_sampler_02_r1e_parent_binding_receipt.json
ash_decode_sampler_02_r1e_source_inventory_receipt.json
ash_decode_sampler_02_r1e_checkpoint_component_inventory.json
ash_decode_sampler_02_r1e_checkpoint_set_binding_receipt.json
ash_decode_sampler_02_r1e_model_spec_binding_receipt.json
ash_decode_sampler_02_r1e_tokenizer_binding_receipt.json
ash_decode_sampler_02_r1e_vocabulary_contract_receipt.json
ash_decode_sampler_02_r1e_special_token_contract_receipt.json
ash_decode_sampler_02_r1e_eos_identity_provenance_receipt.json
ash_decode_sampler_02_r1e_checkpoint_tensor_vocab_contract.json
ash_decode_sampler_02_r1e_effective_model_overlay_binding.json
ash_decode_sampler_02_r1e_runtime_binding_contract.json
ash_decode_sampler_02_r1e_decode_artifact_binding_envelope.json
ash_decode_sampler_02_r1e_cross_model_rejection_matrix.json
ash_decode_sampler_02_r1e_real_bundle_verification_receipt.json
ash_decode_sampler_02_r1e_cache_identity_guard.json
ash_decode_sampler_02_r1e_static_checks.json
ash_decode_sampler_02_r1e_no_mutation_guard.json
ash_decode_sampler_02_r1e_model_quality_claim_guard.json
ash_decode_sampler_02_r1e_verdict.json
```

Per case:

```text
workspace/runtime/decode/r1e/cases/<case_id>/
  active_binding.json
  candidate_receipt_binding.json
  verification_result.json
  rejection_receipt.json
  case_result.json
  stdout.jsonl
  stderr.log
```

Generated runtime artifacts, manifests, receipts, and case directories are excluded from the source bake archive.

---

# 17. Static gates

```text
canonical_decode_runtime_binding_module_count=1
verified_binding_type_count=1
checkpoint_set_digest_function_count=1
model_spec_semantic_digest_function_count=1
tokenizer_vocab_digest_function_count=1
cross_model_receipt_rejection_function_count=1
preload_binding_verification_call_count>=1
post_generation_authority_probe_call_count=0
unknown_checkpoint_fingerprint_fallback_count=0
first_checkpoint_only_identity_use_count=0
runtime_tokenizer_value_mislabeled_as_checkpoint_special_token_count=0
runtime_result_binding_surface_bound=true
active_route_receipt_binding_surface_bound=true
live_receipt_without_binding_digest_count=0
binding_digest_overwrite_count=0
cross_model_fallback_count=0
```

Primary artifact remains externally flat and exposes top-level `schema`, `patch_id`, `pass`, `status`, and `verdict`. Atlas parallel groups are an internal assembly mechanism only. Duplicate primary keys fail closed.

---

# 18. Canonical failures

```text
R1AParentEvidenceIncomplete
R1BParentEvidenceIncomplete
R1CParentEvidenceIncomplete
R1DParentEvidenceIncomplete
DecodeRuntimeBindingMissing
DecodeRuntimeBindingNotVerifiedBeforeModelLoad
CheckpointSetEmpty
CheckpointComponentMissing
CheckpointComponentUnreadable
CheckpointComponentDuplicate
CheckpointComponentCountMismatch
CheckpointComponentOrderMismatch
CheckpointComponentHashMismatch
CheckpointSidecarIncomplete
CheckpointSidecarMismatch
ModelSpecMissing
ModelSpecHashMismatch
ModelSpecSemanticDigestMismatch
ModelSpecIdentityEmpty
TokenizerManifestMissing
TokenizerManifestHashMismatch
TokenizerSemanticDigestMismatch
TokenizerVocabSizeMismatch
TokenizerVocabDigestMismatch
TokenizerTokenIdDuplicate
TokenizerTokenStringDuplicate
TokenizerTokenIdDomainSparse
SpecialTokenIdOutOfRange
SpecialTokenIdDuplicate
SpecialTokenStringMismatch
CheckpointModelTokenizerSpecialTokenMismatch
EosIdentityProvenanceMissing
EosIdentityMismatch
CheckpointEmbeddingTensorMissing
CheckpointLmHeadTensorMissing
CheckpointTensorAmbiguous
CheckpointEmbeddingVocabMismatch
CheckpointLmHeadVocabMismatch
CheckpointHiddenSizeMismatch
RuntimeBindingDigestMissing
RuntimeBindingDigestMismatch
CrossModelDecodeReceiptRejected
AlgorithmicArtifactMisusedAsRuntimeEvidence
ModelInstanceBindingMismatch
DecodeCacheBindingMismatch
UnknownCheckpointFingerprintFallbackObserved
CompileTruthMissing
```

---

# 19. PASS formula

```text
PASS =
  r1a_parent_binding_pass
  && r1b_parent_binding_pass
  && r1c_parent_binding_pass
  && r1d_parent_binding_pass
  && compile_truth_pass
  && real_checkpoint_component_count>=1
  && checkpoint_set_full_runtime_hash_verified
  && checkpoint_component_hash_mismatch_count==0
  && checkpoint_component_order_mismatch_count==0
  && checkpoint_component_completeness_mismatch_count==0
  && model_spec_raw_hash_verified
  && model_spec_semantic_contract_verified
  && tokenizer_manifest_raw_hash_verified
  && tokenizer_semantic_contract_verified
  && vocab_id_domain_dense
  && vocab_token_id_unique
  && vocabulary_digest_verified
  && special_token_contract_verified
  && eos_identity_all_sources_match
  && checkpoint_tensor_vocab_contract_verified
  && preload_binding_verification_pass
  && live_receipt_without_binding_digest_count==0
  && cross_model_negative_control_unexpected_pass_count==0
  && cross_model_runtime_receipt_accept_count==0
  && unknown_checkpoint_fingerprint_fallback_count==0
  && binding_digest_overwrite_count==0
  && checkpoint_mutation_count==0
  && model_spec_mutation_count==0
  && tokenizer_mutation_count==0
  && model_quality_claim_count==0
```

PASS proves exact runtime identity binding and fail-closed receipt rejection. It does not prove checkpoint quality, tokenizer quality, translation quality, checkpoint promotion, or production readiness.

---

# 20. Build and run

```powershell
cargo fmt --all -- --check
cargo check --manifest-path crates/model_core/Cargo.toml
cargo check --manifest-path crates/runtime/Cargo.toml
cargo check --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_decode_sampler_02_r1e_checkpoint_model_tokenizer_binding_gate
```

Runtime-profile invocation:

```powershell
cargo run --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_decode_sampler_02_r1e_checkpoint_model_tokenizer_binding_gate `
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
  --runtime-profile specs/runtime_profile_v5_48259.toml `
  --full-checkpoint-hash true `
  --out-dir workspace/runtime/decode
```

`--checkpoint` is repeatable for explicit multi-file checkpoint invocation.

Expected PASS token:

```text
PASS_ASH_DECODE_SAMPLER_02_R1E_CHECKPOINT_MODEL_TOKENIZER_BINDING_EOS_IDENTITY_PROVENANCE_RUNTIME_VOCABULARY_SPECIAL_TOKEN_CONTRACT_DECODE_ARTIFACT_PARENT_BINDING_CROSS_MODEL_RECEIPT_REJECTION_NO_MUTATION_NO_MODEL_QUALITY_OVERCLAIM
```

Expected outputs:

```text
primary_artifact=workspace/runtime/decode/ash_decode_sampler_02_r1e_checkpoint_model_tokenizer_binding_runtime_artifact.json
manifest=workspace/runtime/decode/ash_decode_sampler_02_r1e_local_manifest.json
```

---

# 21. Promotion boundary

On PASS:

```text
status=PASS
ready_for_sampler_02_r1f=true
ready_for_sampler_02_r1f_scope=live_inference_binding_propagation_and_single_model_instance_receipt
ready_for_default_sampler_policy_promotion=false
ready_for_checkpoint_promotion=false
ready_for_production_decode_promotion=false
```
