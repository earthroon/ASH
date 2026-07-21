# ASH-TRUTH-AUDIT-01-R2-R1-R1

## Single-Serialization Persisted Byte Authority / Fixed-Width Digest Placeholder Seal / Post-Hash Zero-Reserialization Patch / Readback Byte and Canonical Digest Parity Repair

## 0. Metadata

- Parent: `ASH-TRUTH-AUDIT-01-R2-R1 Post-Roundtrip Value Digest Authority / Normalized Artifact Mutation Ownership / Uncommitted Failure Digest Invalidation / Persisted Digest Compile-Runtime Repair`
- Upstream producer: `ASH-LORA-MIN1-R1`
- Patch class: single-serialization persisted artifact sealing repair
- Truth Audit revision: `R2-R1-R1`
- LoRA physical-proof semantics change: not authorized
- Acceptance predicate change: not authorized
- Predicate count: `88` retained
- Digest algorithm: `SHA-256` retained
- Canonicalization ID: `ash.json.canonical.v1` retained
- Acceptance contract: `ash.lora.min1.acceptance.v1` retained

## 1. Confirmed starting state

The LoRA MIN1 GPU path completes forward, loss, backward, live raw parameter and gradient borrow, same-device Adam state ownership, one native GPU optimizer dispatch/completion/apply, parameter/moment mutation, independent parity, and zero synthetic/CPU/host/legacy fallback.

Truth Audit currently reports:

```text
lora_min1_predicate_count=88
lora_min1_predicate_pass_count=87
lora_min1_predicate_fail_count=1
lora_min1_failed_predicates=["LORA_DIGEST_MATCH"]
```

The live tensor namespace predicate is already repaired and must remain passing.

## 2. Observed digest drift

```text
normalized digest:
sha256:464af60642b094b1d1c567794f44e02d2de8071557d383035e28a0b7f31a62b6

next production JSON roundtrip digest:
sha256:948f26f316fc65e68318de2dd6a2fa5035a9b6de11dd1089be9bfe24d6b8c068
```

Repeated production serialization continues moving the persisted representation after digest selection. Increasing the roundtrip count is forbidden.

## 3. Repair objective

Create persisted artifact bytes exactly once, calculate the digest from the parsed one-serialization candidate, patch only four fixed-width digest ranges, and prohibit production artifact serialization after hashing.

```text
final semantic fields
-> one production serialization
-> candidate bytes with four placeholders
-> parse candidate
-> shared canonical digest
-> equal-width byte patch
-> parse and independent digest verification
-> temporary raw-byte write/read parity
-> canonical digest readback parity
-> verified promotion
```

## 4. Scope

Authorized:

```text
shared digest placeholder constants
single-serialization producer writer
placeholder occurrence validation
fixed-width byte patching
post-patch JSON validation
non-digest byte preservation verification
temporary and promoted raw-byte parity
canonical digest readback verification
promotion rollback
focused tests and diagnostics
```

Forbidden:

```text
forward/loss/backward graph changes
raw parameter or gradient borrow changes
parameter-gradient alias changes
Adam state ownership changes
GPU optimizer shader changes
same-device or same-queue relaxation
parameter mutation changes
compact evidence changes
reference comparator changes
live tensor namespace changes
Truth Audit predicate additions/removals
```

## 5. Fixed-width digest contract

Canonical digest text:

```text
sha256:<64 lowercase hexadecimal characters>
```

Total width is exactly 71 ASCII bytes. Every placeholder and the real digest must have this width.

## 6. Shared placeholders

```text
artifact_digest
sha256:0000000000000000000000000000000000000000000000000000000000000000

producer_digest_before_persist
sha256:1111111111111111111111111111111111111111111111111111111111111111

producer_digest_after_roundtrip
sha256:2222222222222222222222222222222222222222222222222222222222222222

producer_digest_after_readback
sha256:3333333333333333333333333333333333333333333333333333333333333333
```

Each placeholder must occur exactly once in candidate bytes. Zero, duplicate, or overlapping occurrences are hard failures. A committed artifact digest equal to any placeholder is invalid.

## 7. Shared SSOT

`crates/lora_train/src/lora_min1_artifact.rs` owns:

```text
LORA_MIN1_DIGEST_WIDTH
four placeholder constants
placeholder slot registry
placeholder detection
committed digest validation
placeholder range discovery
fixed-width patching
non-digest byte preservation verification
canonical digest calculation
```

Producer and Truth Audit consume the same digest neutralization and validation contract.

## 8. Final semantic freeze

Before the one production serialization, candidate success fields are fixed:

```text
producer_digest_roundtrip_match=true
producer_digest_readback_match=true
producer_persisted_self_verification_pass=true
runtime_artifact_promoted=true
single_serialization_persisted_byte_authority=true
production_artifact_serialization_count=1
post_hash_production_reserialization_count=0
digest_placeholder_count=4
digest_placeholder_patch_count=4
digest_placeholder_patch_bytes=284
non_digest_bytes_preserved=true
temporary_byte_readback_parity_verified=true
promoted_byte_readback_parity_verified=true
```

These values become authoritative only when the immutable candidate passes readback and promotion. A rejected candidate is discarded, not rewritten as a canonical failure artifact.

## 9. One production serialization

Exactly one production artifact serialization is authorized:

```rust
let candidate_bytes = serde_json::to_vec_pretty(&artifact)?;
```

After canonical digest computation, no production artifact serializer may regenerate persisted bytes. Canonical compact serialization used only for hash input remains allowed.

## 10. Digest computation

```text
candidate bytes
-> parse serde_json::Value
-> neutralize four digest string fields to empty strings
-> neutralize three producer digest booleans to false
-> recursively sort object keys
-> preserve array order
-> compact canonical serialization
-> SHA-256
```

The parsed one-serialization candidate is digest authority.

## 11. Fixed-width byte patch

The producer locates four exact placeholder ranges and patches each 71-byte range with the 71-byte canonical digest.

Required:

```text
candidate length == patched length
patch range count=4
registered patch width=284 bytes
all changed indexes belong to registered ranges
all non-digest bytes remain identical
```

Unchecked global string replacement is forbidden.

## 12. Zero post-hash reserialization

After digest selection:

```text
production artifact serialization count=0
```

Allowed:

```text
fixed-width byte patch
JSON parse
canonical digest verification
raw file write/read
byte comparison
```

Forbidden:

```text
patched Value -> pretty JSON
readback Value -> pretty JSON
success diagnostic mutation -> artifact reserialization
```

## 13. Post-patch verification

Patched bytes must remain valid UTF-8 JSON, contain the canonical digest in all four registered fields, preserve success booleans, contain no committed placeholder, and independently recompute to the inserted digest.

The parsed patched bytes become the sole in-memory console authority.

## 14. Temporary readback

Canonical path:

```text
workspace/runtime/lora/min1/ash_lora_min1_r1_runtime_artifact.json
```

Temporary path:

```text
workspace/runtime/lora/min1/ash_lora_min1_r1_runtime_artifact.json.tmp
```

Required sequence:

```text
write patched bytes
flush
sync_all
close
read raw bytes
require raw byte equality
parse readback JSON
recompute canonical digest
require digest equality
```

Any mismatch preserves the previous canonical artifact.

## 15. Promotion rollback

When a canonical artifact exists:

```text
old canonical -> backup
verified tmp -> canonical
verify promoted raw-byte parity
verify promoted canonical digest parity
success -> remove backup best-effort
failure -> remove invalid new file and restore backup
```

Promotion is forbidden before placeholder, JSON, non-digest byte, temporary byte, and temporary digest checks pass.

## 16. Failure receipt separation

On any persistence failure, the failed candidate is not persisted. The in-memory console receipt must expose:

```text
verdict=fail
update_terminal_state=Invalid
lora_min1_physical_proof_pass=false
artifact_digest=""
producer_digest_before_persist=""
producer_digest_after_roundtrip=""
producer_digest_after_readback=""
producer_digest_roundtrip_match=false
producer_digest_readback_match=false
producer_persisted_self_verification_pass=false
runtime_artifact_promoted=false
temporary_byte_readback_parity_verified=false
promoted_byte_readback_parity_verified=false
non_digest_bytes_preserved=false
```

A candidate digest may appear only inside a stage-specific error message.

## 17. One-dispatch invariant

Artifact sealing must not trigger physical re-execution:

```text
gpu_optimizer_dispatch_count=1
gpu_optimizer_completion_count=1
gpu_parameter_apply_count=1
```

Persistence failure must not trigger an automatic second LoRA run.

## 18. Truth Audit consumer

Truth Audit remains read-only and file-level:

```text
read canonical bytes
parse JSON
shared digest neutralization
shared canonicalization
SHA-256
compare artifact_digest
evaluate 88 named predicates
```

Truth Audit does not patch files, inspect `.tmp` automatically, repair artifacts, or accept console-only candidate digests.

## 19. Implementation scope

```text
crates/lora_train/src/lora_min1_artifact.rs
crates/lora_train/src/bin/ash_lora_min1_r1.rs
```

Focused unit tests may be colocated in the shared artifact module.

## 20. Static and regression checks

```text
producer production to_vec_pretty count=1
producer post-hash production serializer count=0
placeholder constants=4
placeholder widths=71
placeholder values distinct
old roundtrip writer references=0
candidate and patched lengths equal
only registered ranges differ
patched bytes parse
patched digest matches
placeholder committed as digest is rejected
Truth Audit predicate count remains 88
GPU execution files unchanged
```

Failure injection must preserve the old canonical artifact for placeholder, patch, JSON, temporary-byte, temporary-digest, promotion, and post-promotion failures.

## 21. Expected producer output

```text
PASS_ASH_LORA_MIN1_R1
verdict=pass
single_serialization_persisted_byte_authority=true
production_artifact_serialization_count=1
post_hash_production_reserialization_count=0
digest_placeholder_count=4
digest_placeholder_patch_count=4
digest_placeholder_patch_bytes=284
non_digest_bytes_preserved=true
temporary_byte_readback_parity_verified=true
promoted_byte_readback_parity_verified=true
runtime_artifact_promoted=true
producer_digest_roundtrip_match=true
producer_digest_readback_match=true
producer_persisted_self_verification_pass=true
update_terminal_state=Finalized
lora_min1_physical_proof_pass=true
artifact_digest=sha256:<digest>
```

## 22. Expected Truth Audit output

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

Repository-wide HOLD may remain valid because independent verifier governance is outside this patch.

## 23. PASS conditions

```text
one production artifact serialization
four unique fixed-width placeholders
canonical digest from parsed candidate bytes
four equal-width patches
zero post-hash production reserializations
valid patched JSON
post-patch digest parity
temporary raw-byte and digest parity
promoted raw-byte and digest parity
rollback preservation of previous canonical artifact
empty committed digest on failure
one GPU optimizer dispatch
88/88 LoRA predicate acceptance
```

## 24. FAIL conditions

```text
more than one production serialization
production serialization after hash selection
placeholder count not exactly one
wrong placeholder width
unchecked global replacement
non-digest byte mutation
patched JSON failure
post-patch digest mismatch
temporary byte or digest mismatch
promotion before verification
failed candidate overwrites canonical artifact
candidate digest exposed as committed
second optimizer dispatch
predicate count change
physical-proof relaxation
```

## 25. Commands

```powershell
cargo run --release -p lora_train --bin ash_lora_min1_r1 -- --repo-root . --write-runtime-artifact
```

```powershell
cargo run --release -p lora_train --bin ash_truth_audit_01_r2 -- --repo-root . --lora-min1-artifact workspace/runtime/lora/min1/ash_lora_min1_r1_runtime_artifact.json --decode-min1-artifact workspace/runtime/tensorcube/min1/ash_tcu_decode_min1_r1_runtime_artifact.json --write-runtime-artifact --print-lora-min1-predicate-receipt
```

## 26. Canonical seal

```text
The final persisted bytes are created once.
The serializer may shape the artifact once.
It may not reshape the artifact after the digest is selected.

Four fields reserve four fixed-width digest slots.
The real digest replaces only those slots.
No byte length changes.
No evidence bytes change.
No number rendering changes.
No formatting changes.

After hashing:
No production reserialization.
No pretty-printer.
No semantic reconstruction.

One serialization.
Four fixed-width slots.
Zero post-hash reserializations.
One verified byte sequence.
One canonical digest.
Eighty-eight visible predicates.
Eighty-eight required passes.
```
