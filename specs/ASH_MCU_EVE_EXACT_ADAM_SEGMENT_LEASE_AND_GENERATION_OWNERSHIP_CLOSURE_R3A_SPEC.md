# ASH-MCU-EVE-EXACT-ADAM-SEGMENT-LEASE-AND-GENERATION-OWNERSHIP-CLOSURE-R3A

## 0. Revision

```text
Patch ID:
ASH-MCU-EVE-EXACT-ADAM-SEGMENT-LEASE
-AND-GENERATION-OWNERSHIP-CLOSURE-R3A

Short name:
ADAM'S RIB EVE R3A
MCU ↔ EVE EXACT ADAM SEGMENT LEASE
GENERATION OWNERSHIP CLOSURE

Status:
SPEC RELEASE
```

Authority ceiling:

```text
Eve exact RAM Adam source lease authority        OPEN
MCU Eve-source production submit path            OPEN
MCU device target generation handoff             OPEN
GPU -> Eve RAM successor writeback                CLOSED
Eve CandidateComplete from device target          CLOSED
Eve G+1 commit                                    CLOSED
Durable-head migration                            CLOSED
Full-trainable generation semantics change        CLOSED
WGPU completion callback cutover                  CLOSED
Physical N8 PASS                                  NOT CLAIMED
```

---

# 1. Direct Parent

R3A directly inherits:

```text
ASH-ADAMS-RIB-EVE-MUTABLE-RAM-RESIDENT-ADAM-MV-AUTHORITY
-AND-TRANSACTIONAL-GENERATION-CUTOVER-R3
```

R3 established:

```text
Adam's Rib Eve
= canonical mutable Adam M/V semantic authority

RamResidentAdamMv
= Eve's concrete CPU-RAM body
```

R3A additionally consumes existing production authorities:

```text
AdamWActiveDeviceCandidateProducerR1
AdamWDeviceSourceSegmentR1
AdamWDeviceSourceLeaseR1
PendingAdamWActiveDeviceCandidateR1
AdamWActiveDevicePendingGenerationSchedulerR1
AdamWDeviceSegmentedGenerationR1
SubmissionEpoch / TrackedSubmission
HiMuon optimizer route registry
RAM36 packed/canonical bridge when route-sparse mode is active
```

R3A does not redefine those parents.

---

# 2. Current Source Truth

Before R3A, the production MCU AdamW scheduler accepts:

```rust
submit_from_host_source(
    ...,
    canonical_parameter_index,
    element_start,
    weight: &[f32],
    m: &[f32],
    v: &[f32],
    ...
)
```

The scheduler then creates `AdamRangeR1`, hashes the host source, creates `AdamWDeviceSourceSegmentR1`, issues a GPU source read lease, submits ActiveDevice AdamW, retains the pending owner and later collects device candidate segments.

This means that after Eve R3 the following architecture is still representable:

```text
Unknown host M/V
      |
      v
MCU AdamW scheduler
      |
      v
GPU AdamW
```

That is an authority hole because Eve already claims mutable Adam M/V truth.

R3A closes that hole.

---

# 3. Objective

After R3A admission:

> An MCU production AdamW source segment may obtain Adam M/V only through an exact Eve-issued RAM segment lease bound to the currently active Eve successor generation transaction.

Canonical path:

```text
Eve committed M/V generation G
            |
            | exact AdamRangeR1
            v
Eve RAM Segment Lease R3A
            |
            v
MCU source handoff
            |
            v
AdamWDeviceSourceSegmentR1
            |
            v
AdamWDeviceSourceLeaseR1
            |
            v
GPU AdamW ActiveDevice
            |
            v
Pending candidate G+1
            |
            v
AdamWDeviceSegmentedGeneration G+1
            |
            v
R3B handoff ready
```

Forbidden under R3A production admission:

```text
arbitrary &[f32] M/V
        |
        v
production MCU AdamW
```

---

# 4. Exact Authority Change

```text
BEFORE

MCU
= constructs Adam source range
+ accepts host M/V source

AFTER

Eve
= proves exact Adam M/V source range
+ binds source and target generation
+ binds M/V source digests

MCU
= consumes the Eve lease
+ manages GPU source lifetime
+ manages pending submissions
+ publishes the device target generation
```

R3A does not make Eve the GPU execution owner.

```text
Eve mutable authority      YES
Eve source lease authority YES
Eve execution authority    NO
```

---

# 5. Non-Goals

R3A MUST NOT:

```text
change canonical Adam mathematics
change AdamW WGSL
change Adam hyperparameters
change HiMuon mathematics
change Muon momentum authority
change optimizer routing
change parameter eligibility
change weight-generation authority
make Eve own model weights
perform GPU candidate M/V -> Eve RAM writeback
mark Eve candidate Complete from device output
commit Eve G+1
change durable checkpoint format
retire ordinary-step Adam durable payload format
change full-model HybridOptimizerCommitCoordinator semantics
introduce Device-Hot Eve
replace SubmissionEpoch
replace current nonblocking pending collection
claim full N8 physical qualification
```

---

# 6. Dependency Direction

Dependency direction remains:

```text
adam_rib_eve
      ^
      |
 base_train
      ^
      |
burn_webgpu_backend
```

`adam_rib_eve` owns semantic lease identity only.

It must not import:

```text
RamResidentAdamMv
BackendDevice
BackendQueue
WGPU Buffer
BaseTrain runtime types
```

BaseTrain owns physical RAM lease materialization and MCU integration.

---

# 7. R3A Eve Constants

R3A adds:

```rust
ADAMS_RIB_EVE_EXACT_RAM_SEGMENT_LEASE_AUTHORITY_MATERIALIZED_R3A = true
ADAMS_RIB_EVE_MCU_EXACT_SEGMENT_LEASE_BOUND_R3A = true
ADAMS_RIB_EVE_EXECUTION_AUTHORITY_MIGRATED_R3A = false
ADAMS_RIB_EVE_DURABLE_AUTHORITY_MIGRATED_R3A = false
ADAMS_RIB_EVE_RAM_WRITEBACK_AUTHORITY_MIGRATED_R3A = false
ADAMS_RIB_EVE_PHYSICAL_QUALIFIED_R3A = false
```

Historical R3 authority flags remain immutable.

---

# 8. Semantic Eve Lease Identity

`adam_rib_eve` adds:

```rust
pub struct EveAdamSegmentLeaseIdentityR3A {
    pub generation: AdamGenerationIdentityR1,
    pub range: AdamRangeR1,
    pub layout_digest: String,
    pub range_set_digest: String,
    pub mutable_authority_epoch: u64,
    pub lease_ordinal: u64,
    pub source_m_sha256: String,
    pub source_v_sha256: String,
    pub lease_digest: String,
}
```

The semantic identity contains no pointer, Vec, slice or WGPU handle.

---

# 9. Lease Generation Binding

The lease binds one exact transition:

```text
source:
    model generation     = G
    optimizer generation = O

target:
    model generation     = G+1
    optimizer generation = O+1
```

A lease from `G -> G+1` cannot be reused for `G+1 -> G+2`.

The target optimizer generation must also match the optimizer step consumed by GPU AdamW.

---

# 10. Exact Adam Range

Every lease uses existing:

```rust
AdamRangeR1 {
    canonical_parameter_index,
    element_start,
    element_count,
}
```

No R3A-local Adam coordinate type replaces it.

Required:

```text
element_count > 0
range arithmetic does not overflow
range is inside the exact canonical parameter
range resolves to one exact packed RAM region
range belongs to AdamW execution ownership
```

---

# 11. Parameter Range Binding

BaseTrain adds `EveAdamRangeBindingR3A`, binding:

```text
canonical parameter index
parameter id
canonical element count
parameter byte offset
parameter byte length
parameter-offset-registry digest
route kind
binding digest
```

The parameter-offset-registry digest must equal the Eve R3 range-set digest.

No caller-supplied independent Adam byte offset becomes a new authority.

---

# 12. HiMuon Route-Sparse Cross-Check

When the existing RAM Adam body owns a packed/canonical bridge, Eve lease issue additionally checks that the exact `AdamRangeR1` resolves through that bridge.

For route-sparse mode:

```text
ExplicitAdamw
→ lease permitted

MuonInherited
→ AdamW Eve lease forbidden
```

Failure:

```text
E_ADAMS_RIB_EVE_R3A_MUON_RANGE_ADAMW_LEASE_FORBIDDEN
```

R3A does not alter HiMuon eligibility.

---

# 13. Mutable Authority Epoch

Each Eve R3 adoption owns a non-zero `mutable_authority_epoch`.

The lease binds that epoch. If RAM Adam authority is rehydrated or re-adopted after recovery, old lease identities are invalid even if numerical generation fields happen to match.

---

# 14. Lease Ordinal

Every production Eve lease receives a unique non-zero `lease_ordinal`.

The production runtime owns monotonically increasing ordinal allocation.

```text
Eve lease ordinal
!=
SubmissionEpoch
```

The first is RAM-source identity. The second is GPU physical lifetime identity.

---

# 15. Physical Eve RAM Lease

BaseTrain adds conceptually:

```rust
#[must_use]
pub struct EveRamAdamSegmentLeaseR3A<'a> {
    identity: EveAdamSegmentLeaseIdentityR3A,
    m: &'a [f32],
    v: &'a [f32],
    packed_byte_offset: u64,
}
```

Required:

```text
not Clone
not Copy
read-only M/V
private physical fields
exact semantic lease identity
exact packed byte range
```

No mutable committed M/V slice escapes through this lease.

---

# 16. Lease Issuance State

Canonical issuer:

```rust
issue_eve_adam_segment_lease_r3a(...)
```

requires:

```text
Eve R3 admitted
Eve phase = CandidateFilling
active source generation exact
active target generation exact
layout digest exact
range-set digest exact
route exact
range valid
committed RAM generation = source generation
```

A free-floating lease without an active successor transaction is forbidden.

---

# 17. Exact Source Moment Digest

Lease issue hashes only the requested M/V segment:

```text
source_m_sha256
source_v_sha256
```

R3A forbids a small lease from causing a whole-Adam M/V hash scan.

Required target:

```text
full Adam-state hash scan count = 0
```

A future segment digest-tree revision remains separate.

---

# 18. RAM Lease Lifetime

The RAM lease only needs to survive Eve RAM validation through device source H2D creation.

After `AdamWDeviceSourceSegmentR1` owns exact GPU copies, the RAM borrow may end.

GPU physical lifetime is then owned by existing:

```text
AdamWDeviceSourceLeaseR1
+
SubmissionEpoch
```

---

# 19. MCU R3A Submit API

The scheduler adds:

```rust
submit_from_eve_source_r3a(...)
```

This API receives the weight source, one `EveRamAdamSegmentLeaseR3A`, optional gradient lease, optimizer step and Adam hyperparameters. It does not receive arbitrary `m: &[f32]` and `v: &[f32]` arguments.

---

# 20. Legacy Host API

Existing `submit_from_host_source(...)` remains for historical compatibility.

When R3A production admission is active:

```text
legacy host source submit count = 0
```

No failed Eve lease may silently fall back to the legacy API.

---

# 21. Weight Authority Boundary

Eve does not own model weights.

R3A still permits the existing weight source path, but requires:

```text
weight source generation
==
Eve lease source model generation
```

Weight segment cardinality must equal the leased Adam range cardinality. No truncation or clamp repair is allowed.

---

# 22. Device Source Provenance

The R3A MCU source digest binds:

```text
source generation
target generation
Eve lease digest
weight payload digest
```

`AdamWDeviceSourceSegmentR1::seed_from_host` remains the physical H2D materializer, but Eve is now the semantic authority for M/V source bytes.

This is provenance cutover, not a transfer-mechanics rewrite.

---

# 23. H2D Policy

Valid:

```text
Eve canonical RAM M/V
→ bounded H2D
→ GPU source
```

Invalid:

```text
unowned host M/V
→ GPU source
```

R3A does not require Adam M/V H2D bytes to be zero.

---

# 24. Existing GPU Source Lease Reuse

R3A preserves existing `AdamWDeviceSourceLeaseR1`, including exact source-reader lifetime, SubmissionEpoch binding, release after completion, pre-submit safe drop and post-submit owner retention.

No second GPU source-lifetime system is added.

---

# 25. Production Runtime Lease Ordinal Owner

`ProductionMuonRuntime` adds one monotonic R3A lease ordinal source.

This avoids generation-local duplicate semantic lease identities while keeping `SubmissionEpoch` independent. Overflow fails closed.

---

# 26. Production Runtime Eve Submit

`ProductionMuonRuntime` adds:

```rust
submit_adamw_active_device_pending_eve_segment_r3a(...)
```

It validates:

```text
HybridDeviceCommitRuntimeMode = ActiveVerified
source generation == current committed generation
Adam route owns the entire submitted range
Muon-owned range count = 0
optimizer step == Eve target optimizer generation
```

It then delegates to the MCU scheduler Eve-source API.

---

# 27. RAM Production Cutover

Under:

```text
--admit-mcu-eve-exact-adam-segment-lease-r3a
```

the RAM-resident ActiveDevice path does not obtain M/V by directly forwarding `RamResidentAdamMv::slices()` into the MCU scheduler.

Instead:

```text
ParameterStage / canonical registry binding
→ Eve exact lease issue
→ ProductionMuonRuntime Eve submit
→ MCU Eve submit
```

Legacy direct RAM slices remain only in the `false` compatibility branch.

---

# 28. Duplicate and Overlap Firewall

R3A preserves current `AdamRangeR1` duplicate and overlap rejection.

Additionally:

```text
duplicate Eve lease digest
→ FAIL CLOSED
```

A submitted semantic lease cannot be used twice.

---

# 29. Candidate Collection

Current nonblocking collection remains authoritative:

```text
PendingAdamWActiveDeviceCandidateR1
→ try_collect
→ device segment publication
```

Collection failure retains the pending owner. R3A does not replace the current polling/progress loop.

---

# 30. No Post-Submit Orphan

After GPU submission, an Eve RAM borrow ending does not retire GPU source ownership.

The exact device source lease remains until SubmissionEpoch completion.

Required:

```text
post-submit orphan count = 0
```

---

# 31. Device Target Completion

R3A device completion requires:

```text
pending segments = 0
range coverage exact
device generation complete
published parameter count exact
published element count exact
active device source readers = 0
```

Only then may R3A publish an R3B handoff.

---

# 32. Generation Ownership Handoff

BaseTrain adds `McuEveAdamDeviceGenerationHandoffR3A`, binding:

```text
Adam generation identity
Eve layout digest
Eve range-set digest
Eve mutable authority epoch
MCU scheduler receipt digest
device generation digest
submitted segment count
SubmissionEpoch count
published parameter/element counts
legacy host source count
candidate M/V D2H counts
R3B handoff state
```

---

# 33. Handoff Meaning

Successful R3A handoff proves only:

```text
exact Eve source generation consumed
all AdamW target device segments produced
all source GPU readers retired
device target generation complete
legacy arbitrary host M/V source count = 0
```

It does not prove:

```text
GPU target M/V written into Eve RAM
Eve candidate coverage complete in RAM
Eve candidate seal complete
Eve target generation committed
```

---

# 34. Eve State at R3A Terminal Boundary

At R3A handoff-ready boundary:

```text
Eve committed generation = source G
Eve candidate generation = target G+1
Eve phase = CandidateFilling
MCU AdamW device target G+1 = complete
```

This asymmetry is intentional. R3B closes it.

---

# 35. GPU -> RAM Ceiling

R3A requires:

```text
candidate M D2H bytes = 0
candidate V D2H bytes = 0
Eve RAM target writeback by R3A = 0
```

R3A itself introduces no device-target-to-Eve writeback path. Existing broader durable projection code is not promoted as Eve R3A writeback authority.

---

# 36. Full Production Continuation Ceiling

R3A is source-ownership closure only.

The existing full training loop still requires Eve candidate materialization/seal/commit semantics after the device target stage.

Therefore R3A alone does not claim that a complete multi-step production N8 run can advance through Eve G+1 without R3B.

Physical R3A qualification may be performed as an isolated source-to-device-generation canary. Full training continuation remains HOLD until R3B closes RAM writeback and Eve candidate completion.

---

# 37. Admission

New CLI:

```text
--admit-mcu-eve-exact-adam-segment-lease-r3a
```

Default:

```text
false
```

Required parents:

```text
Eve R3 admitted
RAM-resident Adam M/V admitted
transactional RAM Adam active
ProductionMuonRuntime callsite admitted
MCU AdamW pending scheduler available
exact packed parameter registry available
SubmissionEpoch tracking available
```

In HiMuon route-sparse mode the existing route bridge remains authoritative.

---

# 38. No Silent Parent Adoption

R3A admission without Eve R3:

```text
FAIL CLOSED
```

R3A does not silently enable R3 or silently convert legacy in-place RAM Adam into transactional authority.

---

# 39. Scheduler Receipt Extension

The existing AdamW pending scheduler receipt extends with:

```text
eve_r3a_source_submit_count
eve_r3a_unique_lease_count
eve_r3a_source_m_hash_bytes
eve_r3a_source_v_hash_bytes
legacy_host_source_submit_count
```

Successful admitted R3A device target requires:

```text
legacy_host_source_submit_count = 0

eve_r3a_source_submit_count
== submitted_segment_count

eve_r3a_unique_lease_count
== submitted_segment_count
```

---

# 40. Failure Atomicity

Before device submission:

```text
failure
→ Eve RAM remains source committed authority
→ lease retires
```

After device submission:

```text
failure
→ retain pending GPU owner
→ retire submitted work
→ release source readers
→ discard incomplete device target
→ only then allow Eve candidate abort
```

A returned error must not orphan submitted memory ownership.

---

# 41. No New Adam Mathematics

R3A does not implement or duplicate:

```text
M update
V update
bias correction
weight decay
```

Existing Eve R2 Adam math and backend parity remain canonical.

---

# 42. HiMuon Boundary

HiMuon momentum does not enter Eve Adam leases.

```text
AdamW-owned range
→ Eve M/V source lease

Muon-owned range
→ HiMuon momentum authority
```

The full optimizer partition remains disjoint.

---

# 43. Source Files

New Eve semantic file:

```text
crates/아담의_갈비뼈_이브/src/segment_lease_r3a.rs
```

New BaseTrain files:

```text
crates/base_train/src/adams_rib_eve_exact_segment_lease_r3a.rs

crates/base_train/src/unified_atlas_mcu_eve_adam_generation_ownership_r3a.rs
```

Modified integration surfaces include:

```text
crates/아담의_갈비뼈_이브/src/lib.rs

crates/base_train/src/ram_resident_adam_mv.rs
crates/base_train/src/unified_atlas_mcu_adamw_active_device_pending_generation_scheduler_r1.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/config.rs
crates/base_train/src/bin/base_train.rs
crates/base_train/src/pipeline.rs
crates/base_train/src/lib.rs
```

---

# 44. Static Gate

New validator:

```text
tools/validate_ash_mcu_eve_exact_adam_segment_lease_generation_ownership_closure_r3a_static.py
```

Static PASS requires at minimum:

```text
Eve R3 parent present
semantic lease identity dependency-neutral
exact AdamRangeR1 binding
non-Clone RAM lease
read-only M/V lease
CandidateFilling gate
mutable authority epoch binding
unique lease ordinal
exact M/V segment digest
no full Adam-state scan
HiMuon route firewall
MCU Eve submit API
legacy API retained only for compatibility
SubmissionEpoch preserved
generation handoff present
Eve committed generation unchanged at R3A handoff
candidate M/V D2H = 0 at R3A ownership handoff
R3B handoff ready
execution/durable/writeback authority ceilings retained
```

Static PASS token:

```text
PASS_ASH_MCU_EVE_EXACT_ADAM_SEGMENT_LEASE
_AND_GENERATION_OWNERSHIP_CLOSURE_R3A_STATIC
```

---

# 45. Required Regression Gates

R3A bake must preserve static PASS for:

```text
Eve R1 geometry / generation ABI
Eve R2 canonical Adam math
Eve R3 mutable RAM authority
RAM Adam transactional A/B
HiMuon route-sparse R1
packed/canonical bridge R1A
order-independent sparse overlay R1B
MCU AdamW pending generation scheduler R1
full-model device segmented AdamW successor R1
```

R3A does not waive any parent gate.

---

# 46. Physical Qualification

R3A physical qualification requires an actual local WGPU canary containing:

```text
at least 2 distinct AdamW ranges
at least 2 pending/in-flight candidates during the run
one complete AdamW device target generation
Eve R3 RAM source authority active
```

Required physical evidence:

```text
all production Adam M/V source bytes came from Eve leases
arbitrary host M/V source count = 0
range mismatch count = 0
generation mismatch count = 0
lease reuse count = 0
post-submit orphan count = 0
final pending count = 0
final active source reader count = 0
device target generation complete = true
Eve committed generation unchanged = true
Eve phase remains CandidateFilling = true
R3B handoff ready = true
```

Physical PASS is not granted by static source inspection.

---

# 47. Physical Token

Reserved:

```text
PASS_ASH_MCU_EVE_EXACT_ADAM_SEGMENT_LEASE
_AND_GENERATION_OWNERSHIP_CLOSURE_R3A_PHYSICAL
```

Until physical canary completion:

```text
HOLD_ASH_MCU_EVE_R3A_PHYSICAL_PENDING
```

---

# 48. Negative Fixtures

Mandatory later physical/unit negative fixtures include:

```text
R3A without Eve R3
lease outside CandidateFilling
stale authority epoch
wrong source generation
wrong target generation
wrong target optimizer generation
wrong layout digest
wrong registry digest
zero range
out-of-bounds range
Muon-owned AdamW lease
lease reuse
segment overlap
segment duplicate
weight cardinality mismatch
M/V cardinality mismatch
legacy host M/V submit under R3A admission
post-submit owner loss
partial generation publication
Eve CandidateComplete before R3B
Eve committed generation advance before R3B
GPU target -> Eve RAM writeback through R3A
```

---

# 49. Bake Truth

The R3A source bake may claim only static materialization when the new gate and inherited regression gates pass.

If the bake environment lacks Cargo/Rustc or compatible physical WGPU execution, it MUST NOT claim:

```text
Rust compile PASS
GPU physical PASS
N8 physical PASS
R3B RAM writeback PASS
```

---

# 50. Final Invariant

```text
Eve owns Adam M/V truth.

MCU may not invent Adam M/V truth.

Every admitted production AdamW M/V source begins as one exact Eve lease.

Each lease binds:
- one source generation
- one target generation
- one AdamRangeR1
- one Eve layout
- one mutable authority epoch
- one unique lease ordinal
- one exact source M payload
- one exact source V payload

The Eve RAM borrow lives only until exact GPU source materialization.

SubmissionEpoch then owns GPU source lifetime.

A complete GPU Adam target generation is still not Eve G+1.

Eve remains committed at source G and CandidateFilling for target G+1
until R3B returns the exact device target M/V into Eve RAM and closes candidate completion.
```

Final sentence:

> **R3A is the cutover where MCU loses the right to accept arbitrary Adam M/V and becomes a consumer of Eve-issued exact generation-bound segment leases. Eve owns where Adam came from; MCU owns where that leased state goes on the GPU; neither may silently claim the other's generation authority.**

---

# 51. Direct Successor

```text
ASH-MCU-EVE-ADAMW-ACTIVEDEVICE-TARGET
-TO-RAM-WRITEBACK-CIRCULATION
-AND-EVE-CANDIDATE-SEAL-CLOSURE-R3B
```

R3B objective:

```text
AdamWDeviceSegmentedGeneration G+1
→ bounded exact M/V D2H
→ Eve candidate RAM backing
→ exact candidate coverage
→ Eve candidate M/V digest
→ Eve CandidateComplete
→ commit-permit-ready boundary
```

R3B MUST consume the exact R3A device-generation handoff. It must not rediscover generation or Adam range identity independently.
