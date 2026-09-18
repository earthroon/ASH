# EVE-MCU-R3H-CF11-R1-CF1-CF1-CF1-CF1

## BP-DK LOCAL OBSERVER
## TRANSACTIONAL PENDING CANDIDATE SNAPSHOT CLOSURE

```text
+ PENDING BUFFER READ-ONLY DURABILITY VIEW
+ TARGET GENERATION EXACT BINDING
+ COMMITTED STATE INHERITANCE FOR NO-PENDING PARAMETERS
+ POST-COMMIT STATE EQUIVALENCE CONTRACT
+ NO EARLY PENDING COMMIT
+ NO TRANSACTION ATOMICITY BREAK
+ RESTORE-AS-COMMITTED PARITY PRESERVATION
+ R8A STREAM VERIFY CLOSURE PRESERVATION
+ CF1-CF1 PACKED M/V DIGEST CLOSURE PRESERVATION
+ CF11-R1 MEMORY PRESERVATION
```

## 0. Revision

```text
Patch ID:
EVE-MCU-R3H-CF11-R1-CF1-CF1-CF1-CF1

Class:
BP-DK TRANSACTIONAL SNAPSHOT AUTHORITY CLOSURE
PENDING-CANDIDATE DURABILITY PROJECTION
NO-EARLY-COMMIT REPAIR
```

Direct parent:

```text
EVE-MCU-R3H-CF11-R1-CF1-CF1-CF1
```

Parent full code-only SHA-256:

```text
22f750fb183983e17addbc9786001781880324a2237c835ba810114acf9e40cb
```

## 1. Parent Physical Blocker

The parent physical canary advanced through:

```text
CF11-R1 bounded workspace
CF1-CF1 packed M/V digest/address parity
R8A Dirty -> CleanSealed pre-durability seal
R8A streamed leaf/root verification
```

and then failed at:

```text
BpDkLocalSnapshotPendingGeneration
```

The existing committed-only snapshot API correctly rejects any unresolved pending generation. The candidate filesystem persistence boundary, however, executes before the existing generation finalize authority commits BP-DK pending state.

## 2. Root Cause

Current transaction law:

```text
candidate BP-DK update
-> pending = Some(target candidate)
-> candidate filesystem persistence
-> filesystem commit
-> existing commit_pending_generation_r1(target)
```

The old snapshot path required:

```text
state.pending == None
```

before candidate filesystem persistence, which conflicts with transactional atomicity.

CF1-CF1-CF1-CF1 does not move the commit earlier. It introduces a distinct read-only candidate snapshot view.

## 3. Existing Committed Snapshot Authority Preserved

The existing API remains:

```text
for_each_state_snapshot_mapped_r3h_cf4(...)
```

and keeps:

```text
BpDkLocalSnapshotPendingGeneration
```

as its committed-only invariant.

No global `allow_pending` switch is introduced.

## 4. New Candidate Snapshot Authority

New backend API:

```text
for_each_candidate_state_snapshot_mapped_r3h_cf4(...)
```

Arguments include exact:

```text
expected_optimizer_generation
expected_bp_generation
```

Selection law:

```text
match state.pending:
    Some(target pending)
        -> pending buffer
        -> pending metadata

    None
        -> committed buffer
        -> committed metadata
```

## 5. Exact Target Binding

Pending state is admitted only when:

```text
pending.optimizer_generation == expected_optimizer_generation
pending.bp_generation        == expected_bp_generation
```

Fail-closed errors:

```text
E_CF11_R1_CF1_CF1_CF1_CF1_BPDK_PENDING_OPTIMIZER_GENERATION_DRIFT
E_CF11_R1_CF1_CF1_CF1_CF1_BPDK_PENDING_GENERATION_DRIFT
```

A mismatched pending generation never silently falls back to committed state.

## 6. Pending View Metadata

When pending is selected, the durability view uses:

```text
buffer                    = pending.buffer
last_parameter_revision   = pending.parameter_revision
last_optimizer_generation = pending.optimizer_generation
last_bp_generation        = pending.bp_generation
initialized               = true
source_revision           = pending.source_revision
observer_revision         = pending.observer_revision
policy_revision/digest    = pending policy authority
registry_digest           = pending.registry_digest
optimizer_routing_digest  = pending.optimizer_routing_digest
last_source_weight_digest = pending.source_weight_digest
```

Buffer and metadata therefore come from the same logical candidate version.

## 7. Committed Inheritance

When no pending state exists, the candidate durability view inherits the currently committed buffer and metadata.

This supports mixed candidate snapshots containing:

```text
pending target parameters
+
unchanged committed parameters
```

No fake pending state is materialized for inherited parameters.

## 8. Read-Only Pending Preservation

The candidate API clones only the buffer `Arc` for readback. It does not:

```text
take pending
clear pending
replace committed buffer
call resolve_generation_r1
call commit_pending_generation_r1
```

After streaming, the backend reacquires the state lock and verifies each pending witness still has:

```text
the same target generations
and
Arc::ptr_eq(original pending buffer, current pending buffer)
```

Fail-closed errors include:

```text
E_CF11_R1_CF1_CF1_CF1_CF1_BPDK_PENDING_COMMITTED_DURING_SNAPSHOT
E_CF11_R1_CF1_CF1_CF1_CF1_BPDK_PENDING_GENERATION_CHANGED_DURING_SNAPSHOT
E_CF11_R1_CF1_CF1_CF1_CF1_BPDK_PENDING_BUFFER_CHANGED_DURING_SNAPSHOT
```

## 9. Candidate Snapshot Receipt

New backend receipt:

```text
TensorCubeBpDkLocalCandidateSnapshotReceiptR1
```

Fields:

```text
expected_optimizer_generation
expected_bp_generation
parameter_count
pending_parameter_count
inherited_parameter_count
pending_generation_exact
pending_preserved_after_snapshot
```

Required:

```text
pending_parameter_count + inherited_parameter_count == parameter_count
pending_generation_exact == true
pending_preserved_after_snapshot == true
```

## 10. Production Integration

`ProductionMuonRuntime::persist_bp_dk_observer_state(...)` now uses the candidate-aware API with:

```text
expected_optimizer_generation = optimizer_step
expected_bp_generation        = optimizer_step
```

The existing payload serialization, digest construction, manifest schema and file names remain unchanged.

New compact runtime token:

```text
[ASH-BP-DK-CF11-R1-CF1-CF1-CF1-CF1][transactional-candidate-snapshot]
```

It reports:

```text
target_generation
target_optimizer_generation
target_bp_generation
parameter_count
pending_parameter_count
inherited_parameter_count
state_bytes
candidate_snapshot_digest
pending_generation_exact
pending_preserved=true
filesystem_candidate_only=true
admitted=true
```

## 11. Restore-As-Committed Preservation

The existing snapshot restore path remains unchanged and reconstructs:

```text
ResidentObserverState {
    buffer: durable snapshot bytes,
    committed metadata: durable snapshot metadata,
    pending: None,
}
```

Therefore a filesystem generation that later becomes authoritative still restores directly as committed state. CF1-CF1-CF1-CF1 introduces no durable pending representation.

## 12. Commit / Abort Authority Preservation

The existing generation finalization path remains the only authority that calls:

```text
commit_pending_generation_r1(context.optimizer_step)
```

Abort retains the existing abort authority.

Candidate snapshot success alone never implies runtime transaction commit.

## 13. Tests Added

Backend tests under prefix:

```text
bpdk_cf11_r1_cf1_cf1_cf1_cf1_
```

include:

```text
pending_target_selection_exact
no_pending_inherits_committed_state
pending_optimizer_generation_mismatch_rejected
pending_bp_generation_mismatch_rejected
```

The production candidate API additionally enforces pending buffer/generation preservation after mapped readback.

## 14. Modified Files

```text
MOD crates/burn_webgpu_backend/src/bp_delta_k_local_observer.rs
MOD crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
ADD tools/validate_ash_eve_mcu_r3h_cf11_r1_cf1_cf1_cf1_cf1_bpdk_pending_snapshot_static.py
```

No scheduler source is modified.

## 15. Source SHA-256

```text
7e2669c831337c0e1ce8e4fa342cfa7e763debcee626b113fec5aeb262b1f5f4  crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
c655c94e6e067cf516a80e97210bcbacf15f4f89a529b1eb6573d08525efbf11  crates/burn_webgpu_backend/src/bp_delta_k_local_observer.rs
4eb8bc0d834d525dbeffce05210204f0860c962d49eb771669b061fe795457ee  tools/validate_ash_eve_mcu_r3h_cf11_r1_cf1_cf1_cf1_cf1_bpdk_pending_snapshot_static.py
```

## 16. Static Qualification

Bake results:

```text
PASS_EVE_MCU_R3H_CF11_R1_CF1_CF1_CF1_CF1_BPDK_PENDING_SNAPSHOT_STATIC checks=37
PASS_EVE_MCU_R3H_CF11_R1_CF1_CF1_CF1_R8A_PREDURABILITY_SEAL_STATIC checks=30
PASS_EVE_MCU_R3H_CF11_R1_CF1_CF1_MUON_PACKED_ADDRESS_STATIC checks=26
PASS_EVE_MCU_R3H_CF11_R1_CF1_PACKED_MV_DIGEST_STATIC checks=27
PASS_EVE_MCU_R3H_CF11_R1_BOUNDED_COW_WORKSPACE_STATIC checks=22
PASS_EVE_MCU_R3H_CF11_PAGED_COW_CANDIDATE_WEIGHT_SUCCESSOR_STATIC checks=64
PYTHON_VALIDATOR_COMPILE_PASS
RUST_DELIMITER_SCAN_PASS
```

## 17. Code-Only Artifacts

Overlay:

```text
ASH_EVE_MCU_R3H_CF11_R1_CF1_CF1_CF1_CF1_BPDK_PENDING_SNAPSHOT_OVERLAY_CODE_ONLY.zip
SHA-256 ed46eac9431a48ca60de6e9cc2158157a7d917c97a35a8bfc6f003d6f379c38a
FILES 3
CRC PASS
```

Full:

```text
ASH_PASS3_EVE_MCU_R3H_CF11_R1_CF1_CF1_CF1_CF1_BPDK_PENDING_SNAPSHOT_CODE_ONLY.zip
SHA-256 c509456026a55992c1b6d5ad1d057115e827862a9174fa7e2fda44ed57fea375
FILES 8438
CRC PASS
```

Both archives exclude:

```text
specs/      0
artifacts/  0
manifests/  0
Markdown    0
__pycache__ 0
*.pyc       0
```

## 18. Evidence Boundary At Bake

```text
SOURCE        APPLIED
STATIC        PASS
ARCHIVE CRC   PASS
RUST COMPILE  NOT RUN - Rust toolchain unavailable in bake environment
RUST TEST     NOT RUN
RUNTIME       NOT RUN
PHYSICAL      NOT RUN
PERFORMANCE   UNMEASURED
```

No compile/runtime/physical claim is made by this bake.

## 19. Physical Acceptance

Re-enter the same canary fixture that previously failed at:

```text
BpDkLocalSnapshotPendingGeneration
```

Required first evidence:

```text
[transactional-candidate-snapshot]
pending_generation_exact=true
pending_preserved=true
admitted=true
```

Required disappearance:

```text
BpDkLocalSnapshotPendingGeneration
```

Parent physical closures must remain:

```text
R8A stream_verify_exact=true
packed M/V digest/address exact
CF11-R1 bounded workspace exact
```

Full post-commit equivalence remains a downstream physical gate if execution reaches normal generation finalization.

## 20. Completion Law

CF1-CF1-CF1-CF1 closes only when:

1. committed-only snapshot authority remains strict;
2. candidate snapshot authority is distinct;
3. target pending buffer and pending metadata are selected together;
4. no-pending parameters inherit committed state;
5. pending target generation is exact;
6. mismatched pending state fails closed;
7. candidate readback does not resolve, move or replace pending state;
8. production candidate persistence uses the new authority;
9. restore remains committed-state restoration with `pending=None`;
10. existing commit/abort authority remains unchanged;
11. R8A, packed M/V and CF11-R1 parent closures remain intact;
12. the same physical canary advances beyond `BpDkLocalSnapshotPendingGeneration`.

## 21. Final Law

> CF11-R1-CF1-CF1-CF1-CF1 introduces a read-only BP-DK transactional candidate durability view; it does not commit BP-DK state early.

> Target-generation pending buffers are snapshot sources where present, and no-pending parameters inherit the committed state.

> Pending buffer and metadata version are selected together and exact target generation is fail-closed.

> The live pending transaction remains unresolved through candidate persistence and is committed only by the existing generation-finalization authority.

> Durable restore remains committed-state restore with no pending transaction.

> No optimizer numerical semantics, BP-DK update arithmetic, R8A identity semantics, packed M/V digest semantics, CF11 paged-COW semantics, CF11-R1 workspace semantics or generation commit/abort semantics change in this revision.