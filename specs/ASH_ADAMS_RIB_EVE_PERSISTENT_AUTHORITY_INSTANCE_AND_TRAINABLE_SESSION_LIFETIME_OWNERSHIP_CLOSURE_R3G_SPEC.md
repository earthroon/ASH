# ASH-ADAMS-RIB-EVE-PERSISTENT-AUTHORITY-INSTANCE-AND-TRAINABLE-SESSION-LIFETIME-OWNERSHIP-CLOSURE-R3G

## 0. Revision

```text
Patch ID:
ASH-ADAMS-RIB-EVE
-PERSISTENT-AUTHORITY-INSTANCE
-AND-TRAINABLE-SESSION-LIFETIME-OWNERSHIP-CLOSURE-R3G

Short name:
ADAM'S RIB EVE R3G
PERSISTENT AUTHORITY INSTANCE
+ TRAINABLE SESSION LIFETIME OWNERSHIP

Status:
STATIC MATERIALIZATION RELEASE

Rust compile PASS:          NOT CLAIMED
GPU physical PASS:          NOT CLAIMED
Crash/reopen physical PASS: NOT CLAIMED
N8 PASS:                    NOT CLAIMED
```

Static token:

```text
PASS_ASH_ADAMS_RIB_EVE_PERSISTENT_AUTHORITY_INSTANCE_AND_TRAINABLE_SESSION_LIFETIME_OWNERSHIP_CLOSURE_R3G_STATIC
```

Physical state:

```text
HOLD_ASH_ADAMS_RIB_EVE_R3G_PHYSICAL_PENDING
```

## 1. Integration Parent

R3G is materialized on the R3F source line and preserves the semantics of:

```text
R1   Adam geometry / generation / projection ABI
R2   canonical Adam mathematical update and parity
R3   mutable RAM-resident Adam M/V semantic authority
R3A  MCU <- Eve exact Adam source lease
R3B  ActiveDevice target -> bounded Eve candidate writeback
R3C  atomic Adam + Muon + Weight generation commit join
R3C1 production atomic callsite cutover
R3D  Adam recovery durable reference
R3E  Weight keyframe / exact successor journal
R3F  HiMuon momentum durable cadence
```

R3G does not reinterpret historical R3 or R3A digests.

## 2. Current Source Problem

Current `RamResidentAdamMv` initializes:

```text
eve_mutable_authority_epoch_r3 = 0
```

and first R3 adoption advances it to one. A fresh rehydrate can therefore reproduce the same R3 epoch.

Current R3A lease sequencing historically begins from one inside `ProductionMuonRuntime`. If generation, range, M/V bits and R3 epoch are identical after a fresh rehydrate, a historical R3A lease identity can be numerically reproduced.

R3G closes that authority-incarnation ambiguity.

## 3. Current Lifetime Truth

R3G MUST NOT falsely claim that BaseTrain hydrates Adam for every optimizer generation. Existing R6 already hydrates one `RamResidentAdamMv` and reuses it across the generation loop of one R6 execution invocation.

The remaining lifetime boundary is the R6 invocation itself.

R3G introduces an explicit session runtime ABI capable of owning one hydrated Eve body above generation transactions. Production multi-invocation physical qualification remains pending until an execution campaign proves one hydrated body survives more than one execution invocation.

## 4. Core Law

After admitted R3G authority materialization:

> A fresh live Eve RAM authority incarnation receives one persistent authority-instance identity that is never silently reused for the same training-state root.

And for the session ABI:

> A `TrainableSessionRuntimeR3G` owns exactly one `RamResidentAdamMv` body. Generation transitions mutate that body's committed generation but do not redefine its authority-instance identity.

## 5. Authority Ceiling

R3G materializes:

```text
persistent Eve authority-instance semantic ABI
append-only authority journal
root-level exclusive session guard
Eve-owned lease sequencer ABI
R3G successor exact Adam segment lease
MCU validation of R3G lease uniqueness
TrainableSessionRuntimeR3G ownership envelope
```

R3G does not claim:

```text
MCU execution-fabric migration
HiMuon persistent-session migration
AdamW WGPU pipeline persistence
AdamW buffer-arena persistence
multi-device Adam
multi-device HiMuon
device-hot canonical Eve
new Adam mathematical rules
new Adam M/V durable payload format
```

## 6. Dependency Direction

```text
adam_rib_eve
      ^
      |
 base_train
      ^
      |
 production runtime
```

`adam_rib_eve` owns semantic identity. BaseTrain owns RAM bytes, filesystem journal, session guard and production integration.

## 7. Persistent Authority Identity

Semantic type:

```rust
pub struct EveAuthorityInstanceIdentityR3G {
    pub authority_instance_ordinal: u64,
    pub opened_from_generation: AdamGenerationOrdinalR1,
    pub source_m_sha256: String,
    pub source_v_sha256: String,
    pub previous_record_digest: String,
    pub record_digest: String,
}
```

Schema:

```text
ash.adams_rib_eve.authority_instance.r3g
```

Ordinal zero is forbidden.

## 8. Authority Record Digest

The record digest binds exactly:

```text
R3G schema
instance ordinal
opened model generation
opened optimizer generation
verified source M SHA-256
verified source V SHA-256
previous authority-record digest
```

It does not bind wall-clock time, PID, thread identity, pointer address, hostname or allocator identity.

## 9. Journal

Production journal path:

```text
training_state/eve/r3g/eve_authority_instance.r3g.journal
```

The journal is append-only JSON-lines control metadata. It is not Adam M/V payload.

Bootstrap:

```text
ordinal = 1
previous_record_digest = 64 zero hex characters
```

Successor:

```text
ordinal = previous ordinal + 1
previous_record_digest = previous record_digest
```

## 10. Journal Validation

Every existing journal record is revalidated before allocation.

Fail-closed conditions include:

```text
invalid JSON
patch/schema drift
record digest drift
ordinal gap
hash-chain drift
trailing partial record
ordinal overflow
```

R3G does not silently truncate or roll back to an earlier valid record.

## 11. Durable Publication

New authority allocation follows:

```text
validate journal
-> compute next identity
-> append complete record
-> flush
-> sync_all
-> reload and verify last record
-> only then bind live Eve authority
```

A journal-sync failure does not admit R3G live authority.

## 12. Root Exclusivity

BaseTrain materializes `TrainableSessionRootGuardR3G` before authority allocation.

A second concurrent owner of the same root fails closed. The current static implementation uses an exclusive create-new session-lock file and retains the handle for the admitted runtime lifetime. Crash/stale-lock behavior remains part of physical qualification and operator-repair policy.

## 13. Historical R3A ABI Preservation

`EveAdamSegmentLeaseIdentityR3A` remains unchanged.

R3G introduces a successor wrapper rather than modifying the R3A digest:

```rust
pub struct EveAdamSegmentLeaseIdentityR3G {
    pub parent_r3a: EveAdamSegmentLeaseIdentityR3A,
    pub authority_instance_ordinal: u64,
    pub authority_instance_record_digest: String,
    pub lease_digest: String,
}
```

## 14. R3G Lease Digest

```text
R3G lease digest = SHA256(
    R3G lease schema
    || parent R3A lease digest
    || authority instance ordinal
    || authority instance record digest
)
```

Therefore a reproduced historical R3A parent identity under a fresh rehydrate is not a reproduced R3G identity when the persistent authority instance changes.

## 15. Eve Lease Sequencer

`EveLeaseSequencerR3G` begins at one for one authority instance and uses checked monotonic increment.

Issued ordinals are burned even when a later submit fails. Wrapping to zero is forbidden.

The identity namespace is therefore:

```text
(authority_instance_ordinal, lease_ordinal)
```

## 16. RAM Binding

`RamResidentAdamMv` gains:

```text
optional R3G authority-instance binding
verified hydrated source M digest
verified hydrated source V digest
```

The hydrated source digests are copied from the already-verified packed-state manifest during hydration. R3G authority allocation does not perform an additional full M/V scan.

The resident body rejects a second R3G authority binding and rejects source-generation or source-digest drift.

## 17. R3G RAM Lease

BaseTrain materializes:

```rust
EveRamAdamSegmentLeaseR3G<'a>
```

which wraps the exact R3A RAM lease and does not clone full M/V storage.

## 18. MCU Production Submit

`AdamWActiveDevicePendingGenerationSchedulerR1` gains `submit_from_eve_source_r3g`.

It validates:

```text
R3G lease digest
R3A parent generation
optimizer generation
range cardinality
a single authority instance for the target generation
R3G lease uniqueness
range uniqueness / non-overlap
```

The scheduler maintains a distinct R3G lease-digest set. R3G lease reuse fails closed.

## 19. ProductionMuonRuntime

`ProductionMuonRuntime` gains `submit_adamw_active_device_pending_eve_segment_r3g`.

Under the R3G submit path it is an Eve-lease consumer. It does not choose the R3G lease ordinal.

The historical `next_eve_r3a_lease_ordinal` remains for R3A compatibility only and is not the R3G production identity source.

## 20. R6 Production Integration

When `admit_adams_rib_eve_persistent_authority_instance_r3g` is enabled, R6:

```text
requires Eve R3 + MCU Eve R3A parents
acquires R3G root guard
allocates and durably publishes a fresh R3G authority instance
binds it to the resident Eve body
creates an EveLeaseSequencerR3G
issues R3G successor leases for AdamW ActiveDevice source submission
retains physical PASS as HOLD
```

The R3A compatibility path remains reachable only when R3G authority admission is disabled.

## 21. Trainable Session Runtime ABI

R3G materializes:

```rust
pub struct TrainableSessionRuntimeR3G
pub struct EveTrainableSessionRuntimeR3G
```

The Eve runtime owns exactly one `RamResidentAdamMv`, one persistent authority-instance identity and one Eve lease sequencer.

Session phases are typed:

```text
Open
GenerationActive
Closing
Closed
Poisoned
```

## 22. Generation Semantics

The session ABI separates persistent live authority from generation transaction state.

Successful generation commit:

```text
Adam committed generation G -> G+1
authority instance I -> I
lease sequencer remains monotonic
```

Recoverable generation abort:

```text
candidate discarded
committed Adam preserved
authority instance preserved
already-issued lease ordinals remain consumed
```

## 23. Fresh Reopen

A fresh rehydrate from the same exact numerical Adam state allocates a successor authority record.

Required identity relation:

```text
same generation
same M bits
same V bits
possibly same historical R3A parent lease identity

but

new R3G authority instance
=> new R3G lease identity
```

## 24. RAM36

R3G creates no second canonical full M/V pair.

The resident body remains the existing `RamResidentAdamMv`; the session envelope owns that body rather than copying it.

No full M/V scan is introduced solely for R3G authority allocation.

## 25. Configuration

BaseTrain adds:

```text
admit_adams_rib_eve_persistent_authority_instance_r3g
admit_trainable_session_lifetime_ownership_r3g
```

Session-lifetime admission without persistent authority admission fails closed.

## 26. No Silent Fallback

R3G failure does not silently downgrade the same submitted segment to R3A-only authority.

Fail-closed examples:

```text
missing authority journal parent
invalid journal
sync failure
root already owned
missing resident Eve body
R3 parent missing
R3A parent missing
missing R3G authority binding
R3G authority drift
R3G lease reuse
ordinal overflow
```

## 27. Static Validation

Validator:

```text
tools/validate_ash_adams_rib_eve_persistent_authority_instance_trainable_session_lifetime_ownership_r3g_static.py
```

Current bake result:

```text
35 / 35 PASS
```

Static token:

```text
PASS_ASH_ADAMS_RIB_EVE_PERSISTENT_AUTHORITY_INSTANCE_AND_TRAINABLE_SESSION_LIFETIME_OWNERSHIP_CLOSURE_R3G_STATIC
```

## 28. Parent Regression

The current R3G bake retains PASS for the existing static validators covering:

```text
Eve R3
MCU Eve R3A
MCU Eve R3B
Eve/HiMuon R3C
Eve/HiMuon R3C1
Adam durability R3D
Weight durability R3E
HiMuon momentum durability R3F
```

Observed descendant totals remain:

```text
R3C  18 / 18 PASS
R3C1 30 / 30 PASS
R3D  41 / 41 PASS
R3E  52 / 52 PASS
R3F  66 / 66 PASS
```

## 29. Compile Boundary

The bake environment used for this revision exposes no `cargo`, `rustc` or `rustfmt` binary.

Therefore this revision MUST NOT claim Rust compile PASS from this bake environment.

New and modified Rust files pass UTF-8 and structural delimiter checks; Python R3G validator passes `py_compile`.

## 30. Physical Qualification

Physical promotion requires at minimum:

```text
real R6 production execution
R3G authority journal durable append/sync
multiple R3G Adam segment leases
R3G unique lease count == issued lease count
R3G lease reuse count == 0
fresh close/reopen increments authority instance
same-state reopen produces a distinct R3G lease digest
concurrent same-root writer rejected
crash windows around journal publication exercised
no additional full M/V scan
R3C1 atomic commit preserved
RAM36 bound preserved
Adam numerical parity preserved
```

Trainable-session lifetime physical qualification additionally requires:

```text
one explicit TrainableSessionRuntimeR3G
more than one execution invocation
Adam hydration count == 1
Adam body replacement count == 0
one authority instance across those invocations
```

Until that campaign exists:

```text
HOLD_ASH_ADAMS_RIB_EVE_R3G_PHYSICAL_PENDING
```

## 31. Explicit Non-Claims

R3G does not claim completion of:

```text
session-persistent MCU
session-persistent HiMuon
AdamW pipeline cache
WGPU fixed buffer arena
incremental HiMuon momentum identity
multi-GPU parameter sharding
cross-device TensorCube HiMuon
```

## 32. Direct Successor

After R3G compile and physical qualification, the intended architecture successor is:

```text
ASH-MCU
-SESSION-PERSISTENT-EXECUTION-FABRIC
-AND-OPTIMIZER-INDEPENDENT-JOB-AUTHORITY-R7
```

R3G establishes the authority/lifetime foundation required before that execution migration:

> Generation changes state. Rehydration changes live authority incarnation. These identities are never conflated.
