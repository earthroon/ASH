# ASH-TRUTH-AUDIT-01-R2-R1

## Persisted Artifact Canonical Digest Closure / Producer Write-Roundtrip Self-Verification / Live Tensor Namespace SSOT Alignment / Final Two-Predicate Acceptance Repair

## 0. Metadata

- Parent: `ASH-TRUTH-AUDIT-01-R2 LoRA MIN1 Predicate Failure Surface / Producer-Consumer Canonical Digest Parity / Field-by-Field Acceptance Receipt / Opaque Boolean Gate Elimination Repair`
- Upstream producer: `ASH-LORA-MIN1-R1`
- Patch class: persisted-representation and namespace-contract repair
- Truth Audit revision: `R2-R1`
- LoRA physical-proof semantics change: not authorized
- Predicate removal: forbidden
- Acceptance relaxation: forbidden
- Automatic artifact migration: forbidden
- New manifest authority: not authorized

## 1. Confirmed starting state

Truth Audit evaluates 88 named LoRA MIN1 predicates and reports exactly two failures:

```text
lora_min1_predicate_count=88
lora_min1_predicate_pass_count=86
lora_min1_predicate_fail_count=2
lora_min1_predicate_unavailable_count=0

lora_min1_failed_predicates=[
  "LORA_DIGEST_MATCH",
  "LORA_TARGET_TENSOR_ID_LIVE_NAMESPACE"
]
```

The remaining schema, authority, raw-borrow, graph, execution, mutation, comparator, synthetic-exclusion, fallback-exclusion, and lifecycle predicates pass. The GPU physical update path must not be changed by this repair.

## 2. Confirmed digest disagreement

The producer hashes a pre-persistence `serde_json::Value`, while Truth Audit hashes the parsed persisted representation. Even though both call a shared digest function, their semantic inputs are not guaranteed to be identical.

```text
producer reported: sha256:c2a746b34a511390e56d3a3f93812a3b6f07f0f8c3abc05ff07ba09da5e9cdd7
consumer computed: sha256:583b0e17c91d32cf86952412d243c99964cdb9f615b3dbd45829feb42363b380
```

The persisted semantic JSON representation becomes the digest SSOT.

## 3. Confirmed namespace disagreement

Runtime identity:

```text
ash.lora_min1.live.lm_head.lora_b.parameter:live:<runtime-id>:<offset>
```

Obsolete consumer expectation:

```text
ash.lora.min1.live.lm_head.lora_b.parameter:live:
```

The runtime-owned namespace uses `lora_min1`. The dotted `lora.min1` variant is not an accepted alias.

## 4. Scope

Authorized changes:

```text
LoRA MIN1 artifact canonicalization
LoRA MIN1 artifact persistence
producer digest roundtrip/readback verification
shared live parameter seam constant
shared live tensor namespace constant
namespace predicate validation
focused regression tests
```

Forbidden changes:

```text
forward graph
loss graph
backward execution
raw parameter or gradient borrow semantics
Adam state ownership
GPU optimizer shader
same-device or same-queue policy
in-place parameter mutation
compact evidence
independent comparator
88-predicate acceptance semantics
```

## 5. Shared module SSOT

`crates/lora_train/src/lora_min1_artifact.rs` owns:

```text
schema ID
patch ID
canonicalization ID
digest algorithm ID
acceptance contract ID
live parameter seam ID
live tensor identity prefix
digest-neutralized field lists
persistence normalization
canonical bytes
digest compute and verify
namespace validation
```

Canonical identifiers remain:

```text
schema=ash.lora.min1.r1.runtime_artifact.v1.1
patch_id=ASH-LORA-MIN1-R1
canonicalization_id=ash.json.canonical.v1
digest_algorithm=sha256
acceptance_contract_id=ash.lora.min1.acceptance.v1
```

The acceptance contract remains v1 and the predicate count remains 88.

## 6. Persisted semantic representation

Canonical digest flow:

```text
artifact Value
-> clone
-> neutralize declared digest-reporting fields
-> production JSON serialize
-> parse serialized bytes to Value
-> recursively sort object keys
-> preserve array order
-> reject non-finite numbers
-> compact serialize
-> SHA-256
```

Not authoritative:

```text
pre-write Rust Value
pretty-print whitespace
object insertion order
line endings
trailing newline
console output
native floating-point memory bytes
```

## 7. Digest-neutralized fields

Shared string fields neutralized to `""`:

```text
artifact_digest
producer_digest_before_persist
producer_digest_after_roundtrip
producer_digest_after_readback
```

Shared boolean fields neutralized to `false`:

```text
producer_digest_roundtrip_match
producer_digest_readback_match
producer_persisted_self_verification_pass
```

Producer and consumer must use the same lists. No additional field may be excluded independently.

## 8. Producer roundtrip sequence

Before persistence:

```text
1. initialize digest diagnostic fields
2. compute digest from persistence-normalized representation
3. insert artifact_digest
4. serialize with the production serializer
5. parse serialized bytes
6. recompute digest
7. compare before and after roundtrip
8. refuse persistence when unequal
```

Expected:

```text
producer_digest_roundtrip_match=true
```

## 9. Temporary-file readback sequence

Canonical path:

```text
workspace/runtime/lora/min1/ash_lora_min1_r1_runtime_artifact.json
```

Required flow:

```text
prepare verified bytes
-> write .json.tmp
-> flush
-> sync_all
-> read .json.tmp
-> parse
-> recompute digest
-> compare with artifact_digest
-> record readback diagnostics
-> rewrite final diagnostic values
-> read and verify temporary file again
-> promote temporary file only after equality
```

The previous canonical artifact must not be replaced when verification fails.

## 10. Producer diagnostic fields

```text
producer_digest_before_persist
producer_digest_after_roundtrip
producer_digest_after_readback
producer_digest_roundtrip_match
producer_digest_readback_match
producer_persisted_self_verification_pass
```

Expected for a written PASS artifact:

```text
producer_digest_before_persist=<digest>
producer_digest_after_roundtrip=<same digest>
producer_digest_after_readback=<same digest>
producer_digest_roundtrip_match=true
producer_digest_readback_match=true
producer_persisted_self_verification_pass=true
```

These diagnostics do not replace independent consumer recomputation.

## 11. Persistence failure semantics

If roundtrip, readback, parse, final digest, or promotion verification fails:

```text
verdict=fail
update_terminal_state=Invalid
lora_min1_physical_proof_pass=false
```

The producer must not print `PASS_ASH_LORA_MIN1_R1` for an artifact that failed persistence verification.

## 12. Live namespace SSOT

Shared parameter seam ID:

```text
ash.lora_min1.live.lm_head.lora_b.parameter
```

Shared tensor identity prefix:

```text
ash.lora_min1.live.lm_head.lora_b.parameter:live:
```

Conceptual constants:

```rust
pub const LORA_MIN1_LIVE_PARAMETER_SEAM_ID: &str =
    "ash.lora_min1.live.lm_head.lora_b.parameter";

pub const LORA_MIN1_LIVE_TENSOR_ID_PREFIX: &str =
    "ash.lora_min1.live.lm_head.lora_b.parameter:live:";
```

The raw bridge and Truth Audit evaluator consume the shared constants.

## 13. Namespace grammar

Accepted form:

```text
ash.lora_min1.live.lm_head.lora_b.parameter:live:<runtime-id>:<offset>
```

Required:

```text
exact prefix
non-empty runtime-id
non-empty offset
offset parseable as u64
```

Truth Audit validates structure only. It must not hardcode an observed numeric runtime ID.

Rejected forms include:

```text
authoritative_lm_head_lora_b_window
ash.lora.min1.live.lm_head.lora_b.parameter:live:1:0
ash.lora_min1.live.lm_head.lora_b.parameter:fixture:1:0
ash.lora_min1.live.lm_head.lora_b.parameter:live::0
ash.lora_min1.live.lm_head.lora_b.parameter:live:1:not-a-number
```

## 14. Consumer digest sequence

Truth Audit performs:

```text
read persisted bytes
-> parse Value
-> validate canonicalization metadata
-> invoke shared digest computation
-> compare computed digest with artifact_digest
```

Truth Audit must not reconstruct an imagined pre-write producer object.

For a valid artifact:

```text
producer_digest_before_persist
== producer_digest_after_roundtrip
== producer_digest_after_readback
== artifact_digest
== truth_audit_computed_digest
```

Required predicate:

```text
LORA_DIGEST_MATCH=true
```

## 15. Predicate preservation

This repair does not add or remove required predicates.

```text
acceptance_contract_id=ash.lora.min1.acceptance.v1
predicate_count=88
```

All previously passing 86 predicates must remain passing. Producer diagnostic fields are integrity diagnostics covered by the digest, not hidden acceptance predicates.

## 16. Static tests

```text
S01 raw bridge imports the shared live parameter seam ID
S02 namespace predicate imports the shared live tensor prefix
S03 dotted namespace appears only in a negative test
S04 producer and consumer share digest neutralization fields
S05 predicate count remains 88
S06 forward/backward/shader/comparator paths remain unchanged
```

## 17. Digest regression tests

```text
D01 pretty serialization and parse preserve digest
D02 object key order does not change digest
D03 whitespace and line endings do not change digest
D04 raw semantic mutation without digest recomputation fails LORA_DIGEST_MATCH
D05 neutralized diagnostic values do not change digest
D06 temporary-file readback digest equals reported digest before promotion
```

## 18. Namespace regression tests

Accepted:

```text
ash.lora_min1.live.lm_head.lora_b.parameter:live:6185506036438099345:0
```

Rejected:

```text
ash.lora.min1.live.lm_head.lora_b.parameter:live:1:0
ash.lora_min1.live.lm_head.lora_b.parameter:live::0
ash.lora_min1.live.lm_head.lora_b.parameter:live:1:not-a-number
```

## 19. Implementation scope

```text
crates/lora_train/src/lora_min1_artifact.rs
crates/lora_train/src/lora_min1.rs
crates/lora_train/src/bin/ash_lora_min1_r1.rs
```

Truth Audit binary modification is unnecessary when it already consumes the shared evaluator and digest verifier.

## 20. Required run sequence

```text
1. generate a fresh LoRA MIN1 artifact
2. confirm producer roundtrip and readback verification
3. run Truth Audit with the predicate receipt
4. confirm digest and namespace predicates pass
5. confirm 88/88 acceptance
```

LoRA producer:

```powershell
cargo run --release -p lora_train --bin ash_lora_min1_r1 -- --repo-root . --write-runtime-artifact
```

Truth Audit:

```powershell
cargo run --release -p lora_train --bin ash_truth_audit_01_r2 -- --repo-root . --lora-min1-artifact workspace/runtime/lora/min1/ash_lora_min1_r1_runtime_artifact.json --decode-min1-artifact workspace/runtime/tensorcube/min1/ash_tcu_decode_min1_r1_runtime_artifact.json --write-runtime-artifact --print-lora-min1-predicate-receipt
```

## 21. Expected producer output

```text
PASS_ASH_LORA_MIN1_R1
verdict=pass
producer_digest_roundtrip_match=true
producer_digest_readback_match=true
producer_persisted_self_verification_pass=true
lora_min1_physical_proof_pass=true
artifact_digest=sha256:<digest>
```

## 22. Expected Truth Audit output

```text
HOLD_ASH_TRUTH_AUDIT_01_R2
verdict=hold
lora_min1_artifact_state=accepted
lora_min1_gate_pass=true
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

The repository-wide verdict may remain HOLD because independent verifier review is outside this patch.

## 23. PASS conditions

```text
producer uses persistence-normalized digest input
producer roundtrip digest matches
producer temporary-file readback digest matches
consumer independently computes the same digest
LORA_DIGEST_MATCH=true
underscore namespace passes
obsolete dotted namespace fails
all previous 86 predicates remain passing
predicate_count=88
predicate_pass_count=88
predicate_fail_count=0
LoRA evidence counters increment exactly once
```

## 24. FAIL conditions

```text
pre-write Value remains digest authority
producer promotes before readback verification
producer and consumer neutralize different fields
digest depends on pretty formatting
dotted namespace remains accepted
runtime numeric identity is hardcoded
predicate count decreases
physical requirements are removed
LoRA counters increment without 88/88 acceptance
```

## 25. Canonical seal

```text
The artifact on disk is the digest authority.

Not the pre-write Rust Value.
Not pretty-print whitespace.
Not console output.
Not a producer self-check boolean.

The producer serializes, parses, hashes, writes, reads, parses and verifies.
The consumer reads, parses, hashes and compares independently.

The live namespace belongs to the raw-storage bridge:

ash.lora_min1.live.lm_head.lora_b.parameter:live:

No digest drift.
No namespace alias.
No predicate removal.
No acceptance relaxation.

One persisted representation.
One shared digest contract.
One live namespace SSOT.
Eighty-eight visible predicates.
Eighty-eight required passes.
```
