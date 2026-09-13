# ASH-EVE-MCU-R3G-R2

## SUBMISSION-BOUND MUTATION LEASE
## + GPU COMPLETION AUTHORITY

```text
+ PENDING / SUBMITTED / COMPLETED / PREPARED TYPESTATE
+ WRITE RANGE / ALLOCATION / GENERATION BINDING
+ EXISTING A01 SUBMISSION EPOCH REUSE
+ EXACT-TRACKED COMPLETION ADMISSION
+ COMPLETION-BEFORE-COMMIT BINDING
+ EXISTING RETIREMENT / REUSE AUTHORITY PRESERVATION
+ NO EXTRA PER-PARAMETER WAIT
+ R3C-R2 PREPARED-PERMIT BINDING
+ NO SHA POLICY CHANGE
+ NO BP-DK POLICY CHANGE
```

## 0. Revision

```text
Patch ID:
ASH-EVE-MCU-R3G-R2

Direct parent:
EVE-MCU-R3C-R2
CONSUMING FULL-TRAINABLE GENERATION COMMIT AUTHORITY

Class:
GPU MUTATION COMPLETION AUTHORITY
SUBMISSION-BOUND COMMIT PREPARATION
```

Parent operator evidence:

```text
R3C-R2 debug/release regression PASS
R3C-R2 canonical release build PASS
```

This R3G-R2 bake itself is not compiled or physically executed in the bake environment.

---

# 1. Existing Authority Reused

R3G-R2 reuses the existing WGPU lease/runtime authority:

```text
SubmissionEpoch
TrackedSubmission
PhysicalAllocationId
SubmissionLeaseSpec
CompletionCoverage::ExactTracked
queue completion mailbox
submission_completed_nonblocking
LeaseRetirementDisposition
assert_reuse_eligible
```

R3G-R2 does not create a second submission counter, queue-completion registry, or retirement engine.

---

# 2. Existing R3G RAM Lease Preservation

Existing:

```text
EveRamAdamSegmentLeaseR3G<'a>
```

remains the RAM Adam exact source-read lease.

It is not reinterpreted as GPU mutation authority.

New mutation authority is materialized separately in:

```text
crates/base_train/src/
adams_rib_eve_submission_bound_mutation_lease_r3g_r2.rs
```

---

# 3. Typestate

The new capability has private typestate markers:

```text
MutationPendingR3G2
MutationSubmittedR3G2
MutationCompletedR3G2
MutationPreparedR3G2
```

and private move-only capability:

```text
EveGpuMutationLeaseR3G2<State>
```

No `Clone` or `Copy` implementation exists for the mutation capability.

Cloneable snapshots and receipts are evidence only and do not grant commit authority.

---

# 4. Initial Integration Form

R3G-R2 does not modify every GPU submit callsite.

At full-generation commit preparation it reconstructs the Pending authority from the canonical target-generation owner, then binds it to the actual A01 writer leases already recorded for that target.

The transition is:

```text
canonical target allocation/generation
        ↓
Pending
        ↓ exact A01 writer lease identity
Submitted
        ↓ existing completion mailbox
Completed
        ↓ range / generation / ExactTracked validation
Prepared
        ↓
R3C-R2 consuming generation permit
```

No synthetic submission is generated.

---

# 5. Backend Read-Only Bridge

Added read-only backend witness:

```text
PhysicalAllocationWriteLeaseSnapshotR3G2
physical_allocation_write_lease_snapshots_r3g2(...)
```

It exposes from the existing A01 registry:

```text
logical lease id
site id
physical allocation id
semantic role
exact offset / size
last writer SubmissionEpoch
completion coverage
submission completed state
logical/map state
retirement disposition
```

This API does not create completion or alter retirement state.

---

# 6. Completion Law

A mutation reaches `Completed` only when all bound writer leases report:

```text
submission_completed = true
completion_coverage = ExactTracked
```

The completion value is derived from the existing queue-domain `completed_through` authority after refreshing existing completion mailboxes.

Forbidden inference remains:

```text
SubmissionEpoch exists  != completed
queue.submit returned    != completed
Rust borrow ended        != completed
```

---

# 7. Allocation Binding

Each mutation target binds the exact:

```text
PhysicalAllocationId
```

and filters A01 writer leases by that allocation.

A lease from another allocation cannot satisfy the mutation authority.

---

# 8. Semantic Role Binding

Persistent target roles admitted by the first R3G-R2 integration are:

```text
MuonCandidateWeight
MuonCandidateMomentum
AdamWCandidateWeight
AdamWCandidateM
AdamWCandidateV
```

A writer lease with another semantic role cannot satisfy the target.

---

# 9. Write Range Binding

Actual writer offsets and sizes come from A01 lease records.

The union of the actual writer ranges must cover at least the complete logical target byte prefix:

```text
[0, logical_byte_length)
```

No short writer range may be promoted as full target mutation completion.

Muon arena writer leases may cover a physically rounded allocation span larger than the logical tensor; logical coverage remains the admission boundary.

---

# 10. Submission Set Binding

The canonical target generation already records the writer submission epochs that produced the target.

R3G-R2 requires:

```text
observed writer epoch set
==
expected target writer epoch set
```

A subset of expected submissions cannot be silently promoted merely because its byte range covers the tensor.

---

# 11. Generation Binding

Every mutation target binds:

```text
source TrainableGenerationId
target TrainableGenerationId
```

and requires successor relation for both:

```text
target.model_generation
    = source.model_generation + 1

target.optimizer_generation
    = source.optimizer_generation + 1
```

The same allocation cannot be reused as authority for another generation transition by identity coincidence alone.

---

# 12. Persistent Muon Target Binding

`MuonDeviceSegmentedGenerationR1` now exposes only a typed target description for R3G-R2.

For every persistent Muon segment it creates mutation targets for:

```text
Weight
Momentum
```

using the segment's:

```text
canonical parameter index
physical allocation IDs
logical element count
exact assembly submission epochs
source/target model generation
```

---

# 13. Muon Update Scratch Boundary

Muon orthogonal Update is not a persistent member of the final trainable generation.

It is consumed through the existing BP-DK evidence path and retired before the R3C generation commit boundary.

Therefore this first R3G-R2 commit-permit integration binds persistent Muon W/M targets, not already-retired Update scratch.

This is an explicit scope boundary, not a claim that Update completion is irrelevant.

Its existing parent completion/evidence path remains unchanged.

---

# 14. Persistent AdamW Target Binding

`AdamWDeviceSegmentedGenerationR1` creates R3G-R2 mutation targets for every candidate segment:

```text
Weight
M
V
```

Each target binds the exact candidate allocation and the actual candidate submission epoch.

---

# 15. No Additional Exact Wait

`prepare_generation_mutation_set_r3g_r2(...)` snapshots A01 telemetry before and after mutation preparation.

Required:

```text
exact_wait_count_after
-
exact_wait_count_before
= 0
```

Failure token:

```text
E_R3G2_UNEXPECTED_EXACT_WAIT
```

The new R3G-R2 module contains no `wait_for_submission_exact` call.

---

# 16. Existing Completion Paths

This integration relies on completion already established by parent execution paths.

Examples include:

```text
Muon assembly copy completion
AdamW try_collect nonblocking completion admission
```

R3G-R2 does not weaken or remove those parent gates.

---

# 17. Prepared Generation Mutation Set

Materialized:

```text
PreparedGenerationMutationSetR3G2
```

It owns:

```text
source generation
target generation
prepared mutation receipts
exact-wait delta
prepared digest
```

It does not implement `Clone`.

---

# 18. R3C-R2 Permit Binding

`FullTrainableGenerationPreparedR3C` now privately owns:

```text
gpu_mutations: PreparedGenerationMutationSetR3G2
```

`prepare_full_trainable_generation_commit_r3c(...)` rejects the permit unless:

```text
all mutation receipts target the R3C target generation
all required mutations are completed
all completion coverage is ExactTracked
exact-wait delta = 0
```

The mutation-set digest participates in the R3C prepared digest.

---

# 19. Precommit Preservation

R3C-R2 precommit validation re-validates the prepared generation mutation set before any irreversible generation commit-tail mutation.

Pending or incomplete GPU mutation authority cannot be admitted into the R3C commit tail.

---

# 20. Single Commit Authority Preservation

The R3C-R2 single consuming generation commit remains unchanged as the only generation commit authority.

R3G-R2 is subordinate:

```text
R3G-R2 GPU mutation completion authority
        ↓
R3C-R2 full-generation consuming authority
```

No parallel transaction authority is created.

---

# 21. Commit Result Witness

`CommittedFullTrainableGenerationR3C2` additionally carries:

```text
gpu_mutation_prepared_digest
gpu_mutation_count
gpu_mutation_exact_wait_count_delta
```

Scheduler checks these against the precommit R3G-R2 authority.

---

# 22. Production Witness

Added runtime witness:

```text
[ASH-EVE-MCU-R3G-R2]
```

Required fields include:

```text
source generation
target generation
mutation set digest
mutation count
completionCoverage=EXACT_TRACKED
submissionCompleted=true
exactWaitDelta=0
preparedForR3C=true
```

A printed source token is not itself physical proof until observed in an actual production run.

---

# 23. Completion-Before-Reuse Preservation

R3G-R2 does not create a new reuse registry.

Physical reuse remains governed by existing A01 lifecycle states:

```text
ReleasedAwaitingCompletion
RetiredComplete
```

and:

```text
assert_reuse_eligible(...)
```

Therefore logical release remains distinct from physical reuse eligibility.

---

# 24. Abort / Retirement Boundary

The R3G-R2 typestate capability itself is not the physical allocation owner.

On transaction abort, physical target ownership and submission retirement continue through the existing generation owner / A01 lease retirement paths.

Dropping the R3G-R2 capability does not mean:

```text
GPU complete
allocation reusable
generation committed
```

No destructor-based commit or retirement authority is added.

---

# 25. Raw TrackedSubmission Non-Exposure

The new base_train R3G-R2 capability does not store or expose raw `TrackedSubmission`.

It consumes read-only writer snapshots from the existing backend authority.

Thus cloneability of backend `TrackedSubmission` is not promoted into cloneable generation-commit capability.

---

# 26. Numerical Non-Claim

R3G-R2 proves only the relevant lifecycle properties:

```text
intended persistent allocation was written
expected writer submission identity is exact
writer submission is complete
logical write range is covered
target belongs to the intended generation
```

It does not prove:

```text
shader mathematics correct
all tensor values bit-exact
model quality correct
silent hardware corruption impossible
```

Existing numerical/content evidence remains separate.

---

# 27. SHA Policy Preservation

No changes are made to:

```text
ExactSha256
RuntimeIdentity
R3A source M/V hash
BP-DK exact digest
canary state digest
checkpoint digest
```

R3G-R2 is not the SHA-retirement revision.

---

# 28. BP-DK Preservation

No changes are made to:

```text
BP-DK mode
Disabled semantics
post-update exact digest policy
compact numerical reduction
proposal/resolve policy
```

---

# 29. Existing R3G RAM Lease Preservation

No semantic changes are made to:

```text
EveRamAdamSegmentLeaseR3G<'a>
```

or its underlying R3A content hashing.

---

# 30. Source Delta

```text
ADD 1
MOD 7
DEL 0
```

Added:

```text
crates/base_train/src/adams_rib_eve_submission_bound_mutation_lease_r3g_r2.rs
```

Modified:

```text
crates/burn_webgpu_backend/src/buffer_submission_lease.rs
crates/base_train/src/lib.rs
crates/base_train/src/eve_himuon_full_trainable_generation_commit_r3c.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
crates/base_train/src/unified_atlas_mcu_bp_dk_device_resident_post_update_segmented_successor_r1.rs
crates/base_train/src/unified_atlas_mcu_full_model_device_segmented_successor_r1.rs
```

---

# 31. Source SHA-256 Seal

```text
541f38bcf601dde52e983323fb7606e3ea99f8eaa419075aa0735c7fafcdac28  crates/burn_webgpu_backend/src/buffer_submission_lease.rs
808dbd09a9ff62addecb7b1f9d3d9cc49a0c62704070afdb972a396a957651d4  crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
13776b23a613748a4db59d0ae08315bf09cb24cce24fa31419010f10219ed906  crates/base_train/src/adams_rib_eve_submission_bound_mutation_lease_r3g_r2.rs
e2a51fb169e1ca47a89999a4862f3560d852d451774aa11347b69f96c78ff851  crates/base_train/src/eve_himuon_full_trainable_generation_commit_r3c.rs
ce1874db540b0884ac73194f95f38488ee0554ef20824b52e4ae1c9879f7ee37  crates/base_train/src/unified_atlas_mcu_bp_dk_device_resident_post_update_segmented_successor_r1.rs
a73636df61d8e84854f71c05f2d0bdb9cfbd15d95814db8d13a0fb4f26cdc2f1  crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
bfa9ef23531037801b038812b41dcb0211710583f6ff5d2e0611b89b10e0947b  crates/base_train/src/lib.rs
9d5314cd93a791936357f935683cff72c071527e55274c89e544a014bbfea271  crates/base_train/src/unified_atlas_mcu_full_model_device_segmented_successor_r1.rs
```

---

# 32. Full Code-Only ZIP Seal

```text
ASH_PASS3_EVE_MCU_R3G_R2_SUBMISSION_BOUND_MUTATION_LEASE_GPU_COMPLETION_AUTHORITY_CODE_ONLY.zip

SHA-256:
f0f09c2041395ca344f437aaa5510a5e1bf39908704bff927ae9b80338b5efe4

Files: 8425
CRC: PASS
```

Excluded from ZIP:

```text
specs/      0
artifacts/  0
spec markdown 0
```

---

# 33. Static Bake Verification

Bake-time static checks:

```text
changed source files                   8
new exact-wait calls in R3G-R2 module 0
Pending typestate                      present
Submitted typestate                    present
Completed typestate                    present
Prepared typestate                     present
raw TrackedSubmission in R3G-R2 module 0
A01 completion snapshot bridge         present
R3C prepared mutation binding          present
scheduler R3G-R2 preparation call      1
R3G-R2 production witness              1
source lexical balance                 PASS
ZIP CRC                                PASS
```

These are SOURCE / STATIC / ARCHIVE evidence only.

---

# 34. Compile / Runtime Status

Bake environment:

```text
cargo unavailable
rustc unavailable
```

Therefore:

```text
COMPILE      UNVERIFIED
RUNTIME      UNVERIFIED
PHYSICAL     UNVERIFIED
PERFORMANCE  UNMEASURED
```

No higher-tier PASS is claimed by this commit.

---

# 35. Required Regression Commands

Debug base_train R3G-R2 tests:

```text
cargo test -p base_train --lib --locked r3g_r2_
```

Release base_train R3G-R2 tests:

```text
cargo test -p base_train --lib --release --locked r3g_r2_
```

Backend release regression because `buffer_submission_lease.rs` changed:

```text
cargo test -p burn_webgpu_backend --lib --release --locked
```

Canonical release chain:

```text
cargo build -p burn_webgpu_backend --lib --release --locked
cargo build -p base_train --bin base_train --release --locked -j 1
```

---

# 36. Physical Acceptance

An actual production G→G+1 commit must emit:

```text
[ASH-EVE-MCU-R3G-R2]
completionCoverage=EXACT_TRACKED
submissionCompleted=true
exactWaitDelta=0
preparedForR3C=true
```

and subsequently complete the existing R3C-R2 consuming commit.

Only then may physical mutation-completion authority be promoted.

---

# 37. Forbidden Repairs

```text
NO new exact wait per parameter
NO device.poll(Wait) added to R3G-R2 preparation
NO epoch>0 completion inference
NO raw TrackedSubmission as commit capability
NO Clone on mutation capability
NO allocation substitution
NO short-range promotion
NO subset-of-writer-epochs promotion
NO separate submission epoch registry
NO separate retirement engine
NO R3G RAM lease semantic rewrite
NO SHA policy change
NO BP-DK policy change
NO optimizer math change
NO residency policy change
```

---

# 38. PASS Tokens

Compile/runtime promotion token after operator verification:

```text
PASS_EVE_MCU_R3G_R2_SUBMISSION_BOUND_MUTATION_LEASE_GPU_COMPLETION_AUTHORITY
```

Physical promotion token:

```text
PASS_EVE_MCU_R3G_R2_PHYSICAL_MUTATION_COMPLETION_AUTHORITY
```

Current bake state:

```text
HOLD_EVE_MCU_R3G_R2_GPU_COMPLETION_AUTHORITY_UNPROVEN
```

---

# 39. Final Law

> R3G-R2 does not create GPU completion. It binds the full-generation commit authority to completion evidence already owned by the WGPU submission lease runtime.

> The canonical target generation defines which physical allocations and submission epochs are expected. The A01 lease registry defines which exact ranges were written and whether those writer submissions completed. Both identities must agree before Prepared mutation authority exists.

> No new per-parameter exact wait is introduced. If completion is not already visible at the R3C preparation boundary, R3G-R2 rejects with completion pending rather than silently promoting the mutation.

> Only Prepared GPU mutation authority enters the R3C-R2 full-generation permit. SHA/content verification remains unchanged and separate.
