# ASH-TRUTH-AUDIT-01-R2

## LoRA MIN1 Predicate Failure Surface / Producer-Consumer Canonical Digest Parity / Field-by-Field Acceptance Receipt / Opaque Boolean Gate Elimination Repair

### 0. Metadata
- Parent: `ASH-TRUTH-AUDIT-01-R2 Semantic Evidence Classifier Refinement`
- Upstream proof: `ASH-LORA-MIN1-R1`
- Patch class: Truth Audit consumer diagnostics and canonical acceptance repair
- Truth Audit revision increase: not authorized
- LoRA acceptance relaxation: forbidden
- Automatic artifact repair: forbidden
- New manifest hierarchy: not authorized

### 1. Confirmed starting state
The LoRA producer emitted a physical PASS with live storage, one forward/loss/backward, one native GPU optimizer dispatch/completion/apply, parameter/m/v mutation, independent parity, zero synthetic buffers, and zero CPU/host/legacy fallback. Truth Audit retained Decode-only counters:

```text
runtime_observation_count=1
independent_comparator_count=1
independent_physical_verification_count=1
lora_min1_physical_proof_pass=false
decode_min1_physical_proof_pass=true
```

This is a producer-consumer acceptance disagreement. It does not prove that the GPU update failed.

### 2. Problem
The existing consumer reduces all LoRA acceptance conditions into one short-circuiting `&&` expression. A final `false` does not reveal which field failed, whether it was missing, had the wrong JSON type, differed from the expected value, failed digest validation, or contradicted primitive runtime evidence.

### 3. Repair objectives
The repair must provide:

```text
one shared producer-consumer canonical digest implementation
one shared acceptance contract ID
one stable predicate ID per acceptance condition
one non-short-circuiting evaluator
one complete JSON acceptance receipt
one concise console failed-predicate surface
```

No existing acceptance condition may be silently removed.

### 4. Shared module SSOT
Recommended module:

```text
crates/lora_train/src/lora_min1_artifact.rs
```

It owns schema ID, patch ID, canonicalization ID, digest algorithm ID, acceptance contract ID, canonical bytes, digest compute/verify, predicate result schema, acceptance receipt schema, and evaluator.

### 5. Canonical identifiers

```text
schema=ash.lora.min1.r1.runtime_artifact.v1.1
patch_id=ASH-LORA-MIN1-R1
canonicalization_id=ash.json.canonical.v1
digest_algorithm=sha256
acceptance_contract_id=ash.lora.min1.acceptance.v1
```

The producer records all identifiers. Truth Audit evaluates each through a named predicate.

### 6. Canonical digest
Before hashing, clone the artifact and replace `artifact_digest` with an empty string while keeping the field present. Canonical JSON uses recursively sorted object keys, preserved array order, canonical JSON escaping, finite numbers only, stable shortest round-trip number serialization, and no insignificant whitespace.

Required digest predicates:

```text
LORA_DIGEST_FIELD_PRESENT
LORA_DIGEST_FORMAT_VALID
LORA_CANONICALIZATION_SUCCEEDED
LORA_DIGEST_MATCH
```

Truth Audit records reported digest, computed digest, and match status. Digest validity proves integrity only.

### 7. Predicate result schema

```json
{
  "predicate_id": "LORA_GPU_OPTIMIZER_COMPLETION_COUNT",
  "category": "execution",
  "expected": 1,
  "actual": 0,
  "pass": false,
  "available": true,
  "failure_kind": "unexpected_value",
  "evidence_class": "RuntimeObservation"
}
```

Required failure kinds include `artifact_unavailable`, `field_missing`, `wrong_json_type`, `unexpected_value`, `out_of_range`, `empty_identity`, `forbidden_identity`, `digest_mismatch`, `contradictory_authority`, and `dependent_predicate_unavailable`.

### 8. No short circuit
All safely evaluable predicates run even after earlier failures. Missing, wrong-type, and wrong-value outcomes remain distinct. Only an unparseable artifact may prevent field evaluation, and even that produces a load receipt.

### 9. Load and schema predicates

```text
LORA_ARTIFACT_ARGUMENT_PRESENT
LORA_ARTIFACT_READ_AND_PARSE_SUCCEEDED
LORA_SCHEMA_SUPPORTED
LORA_PATCH_ID_MATCH
LORA_CANONICALIZATION_ID_MATCH
LORA_DIGEST_ALGORITHM_MATCH
LORA_ACCEPTANCE_CONTRACT_ID_MATCH
```

An unreadable LoRA artifact must not abort the whole Truth Audit process.

### 10. Identity predicates

```text
LORA_TARGET_MODULE_MATCH                  expected lm_head.lora_b
LORA_TARGET_PARAMETER_KIND_MATCH          expected lora_b
LORA_TARGET_TENSOR_ID_NONEMPTY
LORA_TARGET_TENSOR_ID_NOT_FORBIDDEN_STATIC_ID
LORA_TARGET_TENSOR_ID_LIVE_NAMESPACE
LORA_LIVE_STORAGE_BOUND                   expected true
```

Forbidden former identity: `authoritative_lm_head_lora_b_window`.
Accepted runtime namespace prefix: `ash.lora.min1.live.lm_head.lora_b.parameter:live:`.

### 11. Raw borrow predicates
Each attempt and success count must equal one:

```text
LORA_PARAMETER_RAW_BORROW_ATTEMPT_COUNT
LORA_PARAMETER_RAW_BORROW_SUCCESS_COUNT
LORA_GRADIENT_RAW_BORROW_ATTEMPT_COUNT
LORA_GRADIENT_RAW_BORROW_SUCCESS_COUNT
LORA_MOMENT_M_RAW_BORROW_ATTEMPT_COUNT
LORA_MOMENT_M_RAW_BORROW_SUCCESS_COUNT
LORA_MOMENT_V_RAW_BORROW_ATTEMPT_COUNT
LORA_MOMENT_V_RAW_BORROW_SUCCESS_COUNT
```

### 12. Authority predicates
Exact case-sensitive values:

```text
LORA_PARAMETER_AUTHORITY = live_burn_model_param
LORA_GRADIENT_AUTHORITY = live_burn_backward
LORA_MOMENT_M_AUTHORITY = lora_min1_native_optimizer_registry
LORA_MOMENT_V_AUTHORITY = lora_min1_native_optimizer_registry
LORA_STEP_AUTHORITY = lora_min1_native_optimizer_registry
LORA_UPDATE_AUTHORITY = lora_min1_native_optimizer
```

### 13. Alias topology predicates
When `parameter_gradient_backing_alias=true`, require disjoint ranges and `shared_backing_buffer_single_rw_binding`. When false, require `separate_parameter_gradient_bindings`. The consumer may not hardcode one allocator topology as the only valid topology.

```text
LORA_ALIAS_SHARED_RANGE_DISJOINT
LORA_ALIAS_SHARED_BINDING_MODE
LORA_ALIAS_SEPARATE_BINDING_MODE
```

### 14. Graph and execution predicates

```text
LORA_FIXTURE_PASS=true
LORA_LIVE_PASS=true
LORA_TARGET_REQUIRES_GRAD=true
LORA_TARGET_IN_LOSS_GRAPH=true
LORA_FORWARD_COUNT=1
LORA_LOSS_COMPUTE_COUNT=1
LORA_BACKWARD_COUNT=1
LORA_LOSS_FINITE=true
```

### 15. Gradient predicates

```text
LORA_GRADIENT_RESOLVE_ATTEMPT_COUNT=1
LORA_GRADIENT_RESOLVE_SUCCESS_COUNT=1
LORA_GRADIENT_NONZERO>0
LORA_GRADIENT_NAN_ZERO=0
LORA_GRADIENT_INF_ZERO=0
```

### 16. Device and queue predicates
All must be true:

```text
LORA_PARAMETER_SAME_DEVICE
LORA_GRADIENT_SAME_DEVICE
LORA_MOMENT_M_SAME_DEVICE
LORA_MOMENT_V_SAME_DEVICE
LORA_OPTIMIZER_SAME_QUEUE
```

### 17. Update and mutation predicates

```text
LORA_AUTHORITATIVE_PARAMETER_IN_PLACE=true
LORA_GPU_OPTIMIZER_DISPATCH_COUNT=1
LORA_GPU_OPTIMIZER_COMPLETION_COUNT=1
LORA_GPU_PARAMETER_APPLY_COUNT=1
LORA_PARAMETER_CHANGED>0
LORA_MOMENT_M_CHANGED>0
LORA_MOMENT_V_CHANGED>0
```

### 18. Comparator predicates
All must be true:

```text
LORA_PARAMETER_REFERENCE_PARITY
LORA_MOMENT_M_REFERENCE_PARITY
LORA_MOMENT_V_REFERENCE_PARITY
LORA_GRADIENT_REFERENCE_PARITY
LORA_LOSS_REFERENCE_PARITY
```

Count predicates:

```text
LORA_CPU_REFERENCE_COMPARATOR_COUNT=2
LORA_OBSERVED_EXECUTION_COUNT=1
LORA_VERIFIED_RESULT_COUNT=1
```

No hidden consumer-only count is allowed.

### 19. Synthetic and fallback exclusions
All expected zero:

```text
LORA_SYNTHETIC_PARAMETER_BUFFER_ZERO
LORA_SYNTHETIC_GRADIENT_BUFFER_ZERO
LORA_SYNTHETIC_OPTIMIZER_STATE_BUFFER_ZERO
LORA_SYNTHETIC_TARGET_IDENTITY_ZERO
LORA_CPU_PARAMETER_APPLY_ZERO
LORA_CPU_OPTIMIZER_STEP_ZERO
LORA_CPU_GRADIENT_MATERIALIZE_FOR_APPLY_ZERO
LORA_HOST_PARAMETER_RECONSTRUCTION_ZERO
LORA_HOST_UPLOAD_APPLY_ZERO
LORA_LEGACY_OPTIMIZER_FALLBACK_ZERO
LORA_CPU_SHADOW_STATE_COMMIT_ZERO
LORA_DETACHED_GPU_PARAMETER_APPLY_ZERO
LORA_TEMPORARY_RESULT_COMMIT_ZERO
```

Missing forbidden counters are failures, not implicit zeros.

### 20. Lifecycle and aggregate consistency

```text
LORA_UPDATE_TERMINAL_STATE_FINALIZED
LORA_ARTIFACT_VERDICT_PASS
LORA_ARTIFACT_PHYSICAL_PROOF_PASS
LORA_PHYSICAL_PROOF_REPORTED_MATCH
```

Truth Audit recomputes physical proof from primitive predicates. A reported PASS cannot override a failed primitive predicate.

### 21. Acceptance receipt
Truth Audit artifact adds:

```json
{
  "lora_min1_artifact_state": "rejected_semantic",
  "lora_min1_acceptance_contract_id": "ash.lora.min1.acceptance.v1",
  "lora_min1_gate_pass": false,
  "lora_min1_artifact_digest_reported": "sha256:...",
  "lora_min1_artifact_digest_computed": "sha256:...",
  "lora_min1_artifact_digest_match": true,
  "lora_min1_predicate_count": 0,
  "lora_min1_predicate_pass_count": 0,
  "lora_min1_predicate_fail_count": 0,
  "lora_min1_predicate_unavailable_count": 0,
  "lora_min1_failed_predicate_ids": [],
  "lora_min1_acceptance_receipt": {}
}
```

Artifact states:

```text
not_provided
unavailable
rejected_integrity
rejected_schema
rejected_semantic
rejected_contradiction
accepted
```

### 22. Console surface
Default output includes artifact state, gate status, reported/computed digest, digest match, predicate counts, and failed predicate IDs.

Detailed flag:

```text
--print-lora-min1-predicate-receipt
```

Detailed line:

```text
lora_min1_predicate_failure id=<ID> category=<category> expected=<json> actual=<json> failure_kind=<kind>
```

### 23. No silent coercion
Forbidden conversions include string to integer, integer to boolean, string to boolean, null to missing, and missing counter to zero. Wrong types produce `wrong_json_type`.

### 24. Counter eligibility
Only a fully accepted receipt may set:

```text
lora_runtime_observation_eligible=true
lora_independent_comparator_eligible=true
lora_independent_physical_verification_eligible=true
```

Only these eligibility fields increment Truth Audit counters. The artifact-reported final boolean does not directly increment counters.

### 25. Evidence classes

```text
GPU dispatch/completion/apply and mutation -> RuntimeObservation
independent numerical parity -> IndependentComparator
complete accepted contract -> IndependentPhysicalVerification
schema/identity/digest/range checks -> ComputedInvariant
```

### 26. Required tests
1. Object key order and pretty/compact whitespace do not change the digest.
2. Raw mutation without digest recomputation fails `LORA_DIGEST_MATCH`.
3. Semantic mutation with recomputed valid digest fails the named semantic predicate while digest remains valid.
4. Missing, wrong-type, and wrong-value cases remain distinct.
5. Alias shared and separate modes are both testable.
6. Producer and consumer use identical constants and canonical digest implementation.
7. Stable predicate IDs and predicate count are snapshot-tested.
8. Current LoRA artifact produces a non-empty exact failed-predicate list before any semantic relaxation.

### 27. Diagnostic sequence

```text
1. Run new Truth Audit against the existing LoRA artifact with detailed receipt.
2. Capture exact failed predicate IDs.
3. Regenerate LoRA artifact with canonicalization and contract metadata.
4. Run Truth Audit again.
5. Repair only the producer, consumer, or shared contract proven wrong by the receipt.
```

No cause may be patched by guess.

### 28. Repository verdict preservation
This repair does not force repository-wide PASS. Existing independent verifier review remains separate. An accepted LoRA artifact changes only its physical evidence contribution:

```text
runtime_observation_count += 1
independent_comparator_count += 1
independent_physical_verification_count += 1
lora_min1_physical_proof_pass=true
```

### 29. Implementation scope

```text
crates/lora_train/src/lora_min1_artifact.rs
crates/lora_train/src/lib.rs
crates/lora_train/src/bin/ash_lora_min1_r1.rs
crates/lora_train/src/bin/ash_truth_audit_01_r2.rs
```

No generic repository-wide canonicalization framework, new audit revision, new manifest service, or automatic artifact migration is authorized.

### 30. PASS conditions

```text
shared producer-consumer digest SSOT
stable acceptance contract and predicate IDs
non-short-circuiting complete receipt
missing/type/value failures separated
reported and computed digest exposed
full receipt stored in Truth Audit artifact
exact failed predicate IDs printed
no acceptance requirement silently removed
accepted receipt increments each physical counter exactly once
```

### 31. FAIL conditions

```text
opaque boolean remains
producer and consumer hash different canonical forms
digest depends on key insertion order or whitespace
missing counters default to zero
wrong types are coerced
evaluation stops at first ordinary failure
expected/actual values are omitted
hidden consumer-only predicates remain
artifact-reported PASS directly increments counters
diagnostics relax failed predicates
```

### 32. Canonical seal

```text
A false aggregate gate is not a diagnostic.

Producer PASS and consumer rejection must not collapse into an unexplained
lora_min1_physical_proof_pass=false.

Producer and consumer hash the same canonical bytes with the same function.
Every required field has a stable predicate ID.
Every rejection records expected and actual values.
Every missing field remains missing.
Every wrong type remains wrong.
Every semantic contradiction remains visible.

The receipt explains the verdict.
It does not manufacture the verdict.

No opaque boolean gate.
No hidden consumer-only predicate.
No silent default.
No type coercion.
No digest drift.
No automatic relaxation.
No counter increment without an accepted physical-evidence receipt.
```
