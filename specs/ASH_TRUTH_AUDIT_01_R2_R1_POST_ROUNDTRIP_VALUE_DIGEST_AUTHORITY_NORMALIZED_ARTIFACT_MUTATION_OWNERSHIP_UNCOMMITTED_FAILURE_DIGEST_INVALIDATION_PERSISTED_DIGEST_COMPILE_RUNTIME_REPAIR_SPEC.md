# ASH-TRUTH-AUDIT-01-R2-R1

## Post-Roundtrip Value Digest Authority / Normalized Artifact Mutation Ownership / Uncommitted Failure Digest Invalidation / Persisted Digest Compile-Runtime Repair

## 0. Metadata

- Parent: `ASH-TRUTH-AUDIT-01-R2-R1 Persisted Artifact Canonical Digest Closure / Producer Write-Roundtrip Self-Verification / Live Tensor Namespace SSOT Alignment / Final Two-Predicate Acceptance Repair`
- Upstream producer: `ASH-LORA-MIN1-R1`
- Patch class: persisted artifact writer ordering and digest authority repair
- Truth Audit revision increase: not authorized
- LoRA physical-proof semantics change: not authorized
- Acceptance predicate change: not authorized
- Predicate count: `88` retained
- Digest algorithm change: not authorized
- Canonicalization ID change: not authorized
- Automatic artifact migration: forbidden

## 1. Confirmed starting state

The native LoRA MIN1 execution reaches the complete physical update path:

```text
live_storage_bound=true
forward_count=1
loss_compute_count=1
backward_count=1
loss_is_finite=true
gradient_resolve_success_count=1
gradient_nonzero_count=8
parameter_same_device=true
gradient_same_device=true
moment_m_same_device=true
moment_v_same_device=true
optimizer_same_queue=true
gpu_optimizer_dispatch_count=1
gpu_optimizer_completion_count=1
gpu_parameter_apply_count=1
parameter_changed_count=8
moment_m_changed_count=8
moment_v_changed_count=8
parameter_reference_parity_verified=true
moment_m_reference_parity_verified=true
moment_v_reference_parity_verified=true
synthetic_parameter_buffer_count=0
synthetic_gradient_buffer_count=0
synthetic_optimizer_state_buffer_count=0
synthetic_target_identity_count=0
cpu_parameter_apply_count=0
host_upload_apply_count=0
legacy_optimizer_fallback_count=0
```

The producer then fails only in persisted artifact verification:

```text
producer_digest_roundtrip_match=false
producer_digest_readback_match=false
producer_persisted_self_verification_pass=false
update_terminal_state=Invalid
lora_min1_physical_proof_pass=false
```

## 2. Observed failure

```text
before_roundtrip=
sha256:68fbdef15cccebc01e47357543ca376c80f494ca3c652dfaa2a1d2c2ab916ae7

after_roundtrip=
sha256:1bb2f9d8972253242af18d775aa31b2cb9a23c88fae266f1c0d52de461a41b54
```

Truth Audit reports:

```text
lora_min1_predicate_count=88
lora_min1_predicate_pass_count=87
lora_min1_predicate_fail_count=1
lora_min1_predicate_unavailable_count=0
lora_min1_failed_predicates=["LORA_DIGEST_MATCH"]
```

The live tensor namespace predicate is already repaired and must remain passing.

## 3. Root cause

The producer currently computes a candidate digest from the construction-time `serde_json::Value`, inserts digest diagnostics, serializes and parses the artifact, and then compares the parsed representation against the construction representation.

```text
construction Value
-> digest
-> serialize
-> parse
-> digest
-> equality requirement
```

The parent contract defines the post-serialization, post-parse semantic value as authority. Therefore the construction value and persisted semantic value must not be compared as equal digest authorities.

A second hidden drift exists when the shared digest function performs another serializer/parser roundtrip internally. When the caller already supplies a parsed persisted value, this extra roundtrip moves digest authority one representation beyond the persisted artifact.

## 4. Repair objective

Establish one chain:

```text
construction Value
-> production serialization
-> parse
-> normalized semantic Value
-> neutralize digest fields
-> canonical key ordering
-> SHA-256
-> diagnostics on normalized Value
-> temporary write
-> readback parse
-> independent digest recomputation
-> verified promotion
```

The normalized semantic value becomes the single owner of digest, mutation, console output and persisted bytes.

## 5. Scope

Authorized changes:

```text
shared canonical digest input contract
producer normalization order
producer artifact mutation ownership
temporary-file readback verification
failure digest invalidation
Windows promotion rollback
focused digest tests and diagnostics
```

Forbidden changes:

```text
LoRA forward graph
loss graph
backward execution
raw parameter borrow
raw gradient borrow
parameter-gradient alias handling
Adam state ownership
GPU optimizer shader
same-device policy
same-queue policy
in-place parameter update
compact evidence
independent comparator
Truth Audit predicate semantics
Truth Audit predicate count
live tensor namespace contract
```

## 6. Canonical identifiers

Unchanged:

```text
schema=ash.lora.min1.r1.runtime_artifact.v1.1
patch_id=ASH-LORA-MIN1-R1
canonicalization_id=ash.json.canonical.v1
digest_algorithm=sha256
acceptance_contract_id=ash.lora.min1.acceptance.v1
predicate_count=88
```

## 7. Construction value status

The pre-roundtrip Rust value is construction material only.

It is not:

```text
digest authority
persistence authority
console authority
final mutation authority
```

No final digest may be computed directly from this value.

## 8. Authority transfer

Authority transfers once:

```text
source Value
-> normalize_lora_min1_artifact_for_persistence
-> normalized Value
```

After this transfer, all subsequent mutations target only the normalized value or a later parsed roundtrip value replacing it.

## 9. Shared normalization API

The shared module owns:

```rust
pub fn normalize_lora_min1_artifact_for_persistence(
    value: &serde_json::Value,
) -> Result<serde_json::Value, String>;
```

It uses the same production JSON serializer used for artifact persistence and reparses the resulting bytes into `serde_json::Value`.

## 10. Shared canonical digest contract

`canonical_lora_min1_artifact_bytes` accepts an already parsed semantic JSON value.

Required flow:

```text
clone parsed value
-> neutralize declared digest fields
-> recursively sort object keys
-> preserve array order
-> reject non-finite numbers
-> compact JSON serialization
```

Forbidden inside the canonical byte function:

```text
another production serialize/parse roundtrip
```

Consumers already parse persisted files. An additional hidden roundtrip would move authority beyond the file representation.

## 11. Digest-neutralized fields

String fields neutralized to `""`:

```text
artifact_digest
producer_digest_before_persist
producer_digest_after_roundtrip
producer_digest_after_readback
```

Boolean fields neutralized to `false`:

```text
producer_digest_roundtrip_match
producer_digest_readback_match
producer_persisted_self_verification_pass
```

Producer and consumer use the same lists.

## 12. Producer preparation order

Required sequence:

```text
1. initialize digest and self-verification fields to neutral values
2. normalize source artifact through production serialize/parse
3. compute canonical digest from normalized value
4. insert artifact_digest into normalized value
5. insert producer_digest_before_persist into normalized value
6. normalize the normalized value one more time for stability verification
7. compute roundtrip digest from that parsed value
8. set producer_digest_after_roundtrip
9. set producer_digest_roundtrip_match
10. transfer sole artifact ownership to the roundtripped value
11. require normalized digest == roundtrip digest
12. serialize only the sole normalized artifact owner
```

The second normalization is a stability check between two parsed values, not a comparison against construction state.

## 13. Forbidden old order

```rust
let digest_before = digest_json(artifact)?;
```

is forbidden when `artifact` is still the construction-time value.

Also forbidden:

```text
hash source A
persist source B
print source C
```

## 14. Normalized mutation ownership

After roundtrip verification:

```rust
*artifact = roundtripped;
```

or equivalent ownership transfer is required.

All later fields mutate this same value:

```text
artifact_digest
producer_digest_after_roundtrip
producer_digest_after_readback
producer_digest_roundtrip_match
producer_digest_readback_match
producer_persisted_self_verification_pass
verdict
update_terminal_state
lora_min1_physical_proof_pass
first_validation_error_message
```

## 15. No split-brain output

The producer may not retain one artifact for console output and another for disk output.

Required:

```text
one normalized Value
-> digest
-> diagnostics
-> serialized bytes
-> console summary
```

## 16. Roundtrip comparison

The valid comparison is:

```text
digest(normalized parsed Value)
==
digest(normalized Value serialized and parsed again)
```

The invalid comparison is:

```text
digest(construction Value)
==
digest(persisted parsed Value)
```

## 17. Temporary artifact write

Canonical path:

```text
workspace/runtime/lora/min1/ash_lora_min1_r1_runtime_artifact.json
```

Temporary path:

```text
workspace/runtime/lora/min1/ash_lora_min1_r1_runtime_artifact.json.tmp
```

Required flow:

```text
write temporary bytes
-> flush
-> sync_all
-> close
-> read bytes
-> parse
-> recompute digest
-> compare with artifact_digest
```

## 18. Readback diagnostics

On equality:

```text
producer_digest_after_readback=<canonical digest>
producer_digest_readback_match=true
producer_persisted_self_verification_pass=true
```

On inequality:

```text
producer_digest_after_readback=<actual digest>
producer_digest_readback_match=false
producer_persisted_self_verification_pass=false
```

## 19. Final rewrite verification

After success diagnostics are inserted:

```text
serialize normalized artifact
-> rewrite temporary file
-> read and parse
-> recompute digest
```

Because diagnostics are neutralized, the digest must remain equal to `artifact_digest`.

## 20. Promotion ownership

The canonical file is replaced only after final readback equality.

On platforms where rename replaces an existing file, rename the verified temporary file directly.

On Windows:

```text
existing canonical file
-> backup
verified temporary file
-> canonical path
promotion failure
-> restore backup
promotion success
-> remove backup best-effort
```

The previous canonical artifact must survive a failed promotion.

## 21. Uncommitted digest invalidation

If any persistence stage fails, the in-memory failure receipt must expose no committed digest.

Required failure mutations:

```text
artifact_digest=""
producer_digest_before_persist=""
producer_digest_after_roundtrip=""
producer_digest_after_readback=""
producer_digest_roundtrip_match=false
producer_digest_readback_match=false
producer_persisted_self_verification_pass=false
verdict=fail
update_terminal_state=Invalid
lora_min1_physical_proof_pass=false
```

A candidate digest may remain only inside the stage-specific error message.

## 22. Existing artifact preservation

A failed new write must not modify the old canonical runtime artifact.

Truth Audit may therefore continue reading the previous artifact until a new verified artifact is promoted.

This is fail-closed behavior, not stale fallback authority.

## 23. One-dispatch invariant

Persistence repair must not cause physical re-execution.

Required:

```text
gpu_optimizer_dispatch_count=1
gpu_optimizer_completion_count=1
gpu_parameter_apply_count=1
```

Forbidden:

```text
persistence failure
-> automatic full LoRA retry
-> second optimizer dispatch
```

## 24. Truth Audit consumer

Truth Audit continues to:

```text
read canonical artifact
-> parse persisted JSON
-> compute canonical digest directly from parsed value
-> evaluate 88 named predicates
```

Truth Audit must not:

```text
read .tmp automatically
repair artifacts
accept console digests
accept uncommitted producer state
perform another hidden normalization roundtrip
```

## 25. Expected producer output

```text
PASS_ASH_LORA_MIN1_R1
verdict=pass
producer_digest_roundtrip_match=true
producer_digest_readback_match=true
producer_persisted_self_verification_pass=true
update_terminal_state=Finalized
lora_min1_physical_proof_pass=true
artifact_digest=sha256:<digest>
```

## 26. Expected Truth Audit output

```text
HOLD_ASH_TRUTH_AUDIT_01_R2
verdict=hold
lora_min1_artifact_state=accepted
lora_min1_gate_pass=true
lora_min1_artifact_digest_reported=sha256:<digest>
lora_min1_artifact_digest_computed=sha256:<same digest>
lora_min1_artifact_digest_match=true
lora_min1_predicate_count=88
lora_min1_predicate_pass_count=88
lora_min1_predicate_fail_count=0
lora_min1_predicate_unavailable_count=0
lora_min1_failed_predicates=[]
runtime_observation_count=2
independent_comparator_count=2
independent_physical_verification_count=2
lora_min1_physical_proof_pass=true
decode_min1_physical_proof_pass=true
```

Repository-wide HOLD may remain correct for independent verifier work outside this patch.

## 27. Static checks

```text
S01 no digest is computed from the pre-normalized artifact
S02 canonical byte computation performs no hidden JSON roundtrip
S03 producer imports the shared normalization function
S04 one normalized artifact owns all final mutation
S05 failed persistence clears committed digest fields
S06 Truth Audit predicate count remains 88
S07 GPU execution files are unchanged
```

## 28. Digest regression tests

```text
D01 normalized Value digest survives production serialize/parse
D02 diagnostic field mutation does not change digest
D03 object insertion order does not change digest
D04 pretty versus compact formatting does not change digest after parse
D05 raw semantic mutation without digest update fails LORA_DIGEST_MATCH
D06 final temporary-file readback equals reported digest
D07 parsed consumer value hashes without another normalization generation
```

## 29. Failure tests

### F01 Normalized roundtrip mismatch

Expected:

```text
producer_digest_roundtrip_match=false
artifact_digest=""
canonical artifact not replaced
```

### F02 Temporary-file mutation

Expected:

```text
producer_digest_readback_match=false
artifact_digest=""
canonical artifact not replaced
```

### F03 Invalid temporary JSON

Expected:

```text
verdict=fail
update_terminal_state=Invalid
lora_min1_physical_proof_pass=false
```

### F04 Promotion failure

Expected:

```text
previous canonical artifact restored
producer PASS forbidden
```

## 30. Implementation scope

```text
crates/lora_train/src/lora_min1_artifact.rs
crates/lora_train/src/bin/ash_lora_min1_r1.rs
```

No Truth Audit evaluator modification is required.

## 31. Required commands

Producer:

```powershell
cargo run --release -p lora_train --bin ash_lora_min1_r1 -- --repo-root . --write-runtime-artifact
```

Truth Audit:

```powershell
cargo run --release -p lora_train --bin ash_truth_audit_01_r2 -- --repo-root . --lora-min1-artifact workspace/runtime/lora/min1/ash_lora_min1_r1_runtime_artifact.json --decode-min1-artifact workspace/runtime/tensorcube/min1/ash_tcu_decode_min1_r1_runtime_artifact.json --write-runtime-artifact --print-lora-min1-predicate-receipt
```

## 32. PASS conditions

```text
post-roundtrip parsed Value is digest authority
canonical byte function does not re-roundtrip parsed values
normalized digest equals normalized stability-roundtrip digest
normalized digest equals temporary-file readback digest
normalized digest equals final persisted-file digest
one normalized Value owns console and persisted output
failed persistence exposes no committed digest
previous canonical file survives failed promotion
GPU optimizer dispatch remains exactly one
Truth Audit passes all 88 LoRA predicates
```

## 33. FAIL conditions

```text
construction Value remains digest authority
canonical digest function performs a hidden additional roundtrip
producer hashes one object and writes another
console and disk use different artifact owners
candidate digest is printed as committed after failure
canonical file is removed before verified replacement can be restored
persistence retry causes another optimizer update
predicate count changes
physical-proof predicates are weakened
Truth Audit accepts an uncommitted artifact
```

## 34. Completion definition

The repair is complete when:

```text
producer no longer compares construction state with persisted state
normalized parsed Value owns digest and all later mutation
producer roundtrip and readback verification pass
Truth Audit independently computes the same digest
LORA_DIGEST_MATCH=true
all 88 LoRA MIN1 predicates pass
```

## 35. Canonical seal

```text
The pre-roundtrip Rust Value is construction material.
It is not digest authority.

Authority begins after production serialization and parse.

That normalized Value owns the digest.
That normalized Value owns diagnostics.
That normalized Value owns console output.
That normalized Value owns persisted bytes.

The canonical digest function hashes the parsed semantic Value directly.
It does not move authority through another hidden roundtrip.

A candidate digest is not a committed digest.
A failed temporary write is not a runtime artifact.
A completed GPU step is not enough to authorize a corrupt receipt.

No pre-roundtrip digest authority.
No hidden re-roundtrip authority.
No split-brain artifact mutation.
No uncommitted digest exposure.
No premature promotion.
No second optimizer dispatch.
No predicate relaxation.

One normalized artifact.
One canonical digest.
One verified temporary file.
One recoverable promotion.
Eighty-eight visible predicates.
Eighty-eight required passes.
```
