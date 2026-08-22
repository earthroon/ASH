# ASH-VENDOR-WGPU-SUBMISSION-EPOCH-LEASE-01

## Submission-Epoch Lease / Exact Completion / Deferred Retirement Authority

### 0. Status

| Field | Authority |
|---|---|
| Patch ID | `ASH-VENDOR-WGPU-SUBMISSION-EPOCH-LEASE-01` |
| Parent | `ASH-VENDOR-BUFFER-AUTHORITY-INVENTORY-00` |
| Runtime WGPU | `wgpu 26.0.1` |
| Core role | GPU submission lifetime authority |
| Physical reuse | forbidden in A01 |
| Arena / size classes | forbidden in A01 |
| Bulk readback removal | forbidden in A01 |
| Async wait removal | forbidden in A01 |
| Next | `ASH-VENDOR-WGPU-USAGE-SEGREGATED-ARENA-02` |

A00 answered what a buffer means and where bytes move. A01 answers when the GPU is actually finished with a tracked byte range.

---

## 1. Core invariant

```text
LogicalRelease
!=
GpuCompletion
!=
Reusable
```

A logical owner dropping or releasing a lease is not completion evidence. A01 introduces explicit submission lifetime authority before A02 is allowed to reuse physical capacity.

---

## 2. Epoch separation

Three epoch-like concepts exist and must remain separate.

```text
Alias Registry Epoch
= alias metadata mutation order

Legacy GPU verification submission_epoch
= verification subsystem sequence

A01 SubmissionEpoch
= tracked queue submission lifetime authority
```

Forbidden:

```text
A01 epoch = alias last_access_epoch
A01 epoch = verification receipt submission_epoch
```

A01 epoch is:

```rust
pub struct SubmissionEpoch {
    pub device_id: DeviceAuthorityId,
    pub queue_id: QueueAuthorityId,
    pub ordinal: u64,
}
```

---

## 3. Native completion token

`wgpu 26.0.1` returns a `SubmissionIndex` from `Queue::submit`. A01 binds that native token to an ASH submission epoch at submit time.

```text
ASH SubmissionEpoch
= serializable authority identity

wgpu::SubmissionIndex
= runtime-only native completion token
```

`SubmissionIndex` must not be serialized as a durable receipt identity.

Tracked completion uses:

```rust
wgpu::PollType::WaitForSubmissionIndex(ticket.native_index.clone())
```

not the ambiguous most-recent-submission `PollType::Wait` on mandatory optimizer candidate paths.

---

## 4. Queue authority

A01 v1 uses a single tracked queue domain per optimizer lease graph.

```text
QueueAuthorityId
DeviceAuthorityId
Submission ordinal
```

are process-local authorities. They are not pointer values and are not durable cross-run identities.

Cross-queue lease adoption is not admitted in A01 v1.

---

## 5. Logical lease

```rust
pub struct AshBufferLease {
    pub lease_id: LogicalLeaseId,
    pub allocation: AllocationAuthority,
    pub device_id: DeviceAuthorityId,
    pub queue_id: QueueAuthorityId,
    pub site_id: String,
    pub semantic_role: BufferSemanticRole,
    pub class: BufferLeaseClass,
    pub offset: u64,
    pub size: u64,
    pub logical_state: LeaseLogicalState,
    pub map_state: LeaseMapState,
    pub pending_queue_write_count: u32,
    pub last_writer_submission: Option<SubmissionEpoch>,
    pub last_reader_submission: Option<SubmissionEpoch>,
    pub retire_after_submission: Option<SubmissionEpoch>,
    pub completion_coverage: CompletionCoverage,
}
```

A01 separates allocation identity from logical byte-range lease identity.

---

## 6. Allocation authority

```text
Owned PhysicalAllocationId
ExternalBorrowed observation identity
```

must remain distinct.

A `RawWgpuBufferLease` borrowed from an external runtime is not silently promoted into an ASH-owned physical allocation.

---

## 7. Lease classes

A01 lease class expresses usage compatibility only.

```text
StorageReadOnly
StorageReadWrite
Uniform
CopyStaging
MapReadback
ExternalBorrowed
VendorOpaque
```

It is not the future A02 capacity/size class.

---

## 8. Submission access authority

Every tracked optimizer submission declares access intent before submit.

```text
Read
Write
ReadWrite
```

For a tracked epoch `E`:

```text
read  -> lastReaderSubmission = E
write -> lastWriterSubmission = E

retireAfterSubmission
= latest tracked read/write epoch in the same queue domain
```

---

## 9. Queue-write pending authority

`Queue::write_buffer()` is not considered GPU-complete at call return.

A01 records:

```text
queue.write_buffer
-> PendingQueueWrite
-> next tracked Queue::submit
-> bind to SubmissionEpoch E
```

Mandatory current bindings include:

```text
local_muon.status
fused_muon.status
generation_cache.weight_write
```

---

## 10. Exact tracked candidate submissions

A01 ActiveVerified bake covers the current candidate/readback submissions for:

```text
Local Muon physical batch
Fused HiMuon physical batch
R5 AdamW candidate
```

They use `submit_with_leases(...)` and retain the returned `wgpu::SubmissionIndex` in a runtime-only `SubmissionTicket`.

---

## 11. Local Muon tracked lease set

Per physical candidate batch:

```text
READ
params
descriptors
gradient
weight
momentum

READWRITE
candidate weight
candidate momentum
orthogonal update
status

WRITE
candidate weight readback
candidate momentum readback
update readback
status readback
```

The packed-gradient producer submission is currently marked:

```text
A01_CONSERVATIVE_UNKNOWN_SUBMISSION
```

because the returned `RawWgpuBufferLease` does not yet carry a cross-submission A01 physical lease identity. This buffer must not be admitted to A02 reuse until that bridge is added.

---

## 12. Fused HiMuon tracked lease set

Per fused physical batch:

```text
READ
params
descriptors
gradient
source weight
source momentum

READWRITE
candidate weight
candidate momentum
update
status

WRITE
four readback buffers
```

Planner domain authority remains unchanged.

```text
FUSED_RIGHT / FUSED_DOWN planning
!=
A01 lifetime authority
```

A01 only seals resource lifetime around the already-selected physical execution.

---

## 13. AdamW tracked lease set

Per candidate call:

```text
READ
params
gradient
weight
M prev
V prev
row map

READWRITE
candidate weight
candidate M
candidate V
status

WRITE
weight readback
M readback
V readback
status readback
```

The existing four readback waits remain four waits for A01 behavior parity, but each wait targets the same exact `SubmissionIndex` instead of using a generic most-recent wait.

Wait coalescing is not A01 scope.

---

## 14. Mapping state

```text
Unmapped
MapRequested
MappedRead
MapFailed
```

A readback range is not reusable while mapped or while map completion is unresolved.

Current mandatory flow:

```text
submit E
-> map_async requests
-> WaitForSubmissionIndex(E)
-> host read
-> buffer.unmap()
-> mark Unmapped
```

---

## 15. Logical release

`release_submission_leases()` changes logical ownership state only.

```text
Live -> Released
```

It does not free or return capacity to a pool.

---

## 16. Retirement disposition

Derived states:

```text
Live
PendingQueueWrite
InFlight
HostMapped
ReleasedAwaitingCompletion
RetiredComplete
ConservativeHold
```

A01 may prove `RetiredComplete`. A01 still does not reuse that allocation.

---

## 17. Completion prefix

For one queue domain, exact completion of epoch `E` proves completion of earlier submitted epochs in that same queue ordering.

```text
completedThrough = max(completedThrough, E.ordinal)
```

This must never be applied across queue domains.

Repeated exact waits on the same submission do not count as multiple completed submissions.

---

## 18. External alias in-flight seal

Vendor alias registry keeps its metadata epoch authority, but now also records:

```text
in_flight_materialization_count
```

Materialization flow:

```text
external alias
-> encode copy
-> queue.submit
-> mark materialization in-flight
-> register on_submitted_work_done callback
-> completion callback decrements in-flight count
-> DetachedOwned when safe and not tombstoned
```

A tombstoned alias with an in-flight materialization is retained by sweep.

```text
Tombstoned
AND in_flight_materialization_count > 0
-> do not erase entry
```

This closes the previous `finalize_after_submit == completion` ambiguity.

---

## 19. Vendor alias behavior preservation

A01 does not add a blocking wait to standalone alias materialization. Destination ownership remains available after queue submission under queue-order semantics, while source alias metadata retirement is deferred until completion evidence arrives.

---

## 20. Generation-sealed Muon cache

A01 does not replace the cache.

The existing resident-weight cache remains semantic identity authority.

On slot reuse:

```text
queue.write_buffer(slot.buffer, ...)
```

is recorded as a pending queue write and is bound to the next tracked optimizer submission on that queue.

---

## 21. Conservative surfaces

A01 does not falsely promote surfaces whose cross-submission physical identity is not yet connected.

Current conservative examples:

```text
Local Muon packed-gradient producer
opaque vendor submissions outside A01 tracked optimizer routes
external allocations not owned by ASH
```

A02 must reject these as physical reuse sources until an exact lifetime bridge exists.

---

## 22. Forbidden changes

A01 must not introduce:

```text
buffer pool
arena allocator
size classes
suballocation reuse
capacity reuse
readback removal
poll removal
submission coalescing
Muon momentum residency migration
AdamW/Muon device commit
```

---

## 23. Behavior parity

A01 may change synchronization specificity:

```text
PollType::Wait
-> PollType::WaitForSubmissionIndex(exact_ticket)
```

It must not change:

```text
WGSL
buffer usage bits
buffer byte sizes
bind groups
pipeline layouts
dispatch geometry
copy ordering
optimizer math
candidate values
Muon planning
AdamW/Muon ownership
```

---

## 24. Static implementation surfaces

Backend:

```text
crates/burn_webgpu_backend/src/buffer_submission_lease.rs
crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon.rs
crates/burn_webgpu_backend/src/tensorcube_fused_pair_muon.rs
crates/burn_webgpu_backend/src/base_train_r5_optimizer_continue.rs
crates/burn_webgpu_backend/src/tensorcube_generation_sealed_muon_cache.rs
crates/burn_webgpu_backend/src/lib.rs
```

Vendor fork:

```text
vendor_fork_scaffold/burn-wgpu-local/src/storage_alias_registry.rs
vendor_fork_scaffold/burn-wgpu-local/src/compute/storage.rs
```

Static validator:

```text
tools/ash_vendor_buffer_a01_static_validate.py
```

---

## 25. Static gate

Required source truths:

```text
A01 module exported
Queue::submit return captured on tracked candidate paths
WaitForSubmissionIndex used on Local/Fused/AdamW candidate paths
plain PollType::Wait absent from those candidate/readback paths
queue-write pending hook present for Local/Fused/cache writes
external alias in-flight counter present
alias tombstone sweep preserves in-flight entries
WGSL unchanged from A00 parent
Cargo.toml unchanged from A00 parent
no arena/pool implementation introduced
```

The static gate must identify itself as `STATIC_SOURCE_ONLY` and cannot claim Rust typecheck or physical GPU execution.

---

## 26. Runtime promotion gate

Physical promotion requires a target-machine run proving:

```text
TrackedSubmissionCount > 0
CompletedSubmissionCount > 0
ExactWaitCount > 0

PendingQueueWriteCount returns to 0
EarlyReuseReject path works
Mapped ranges are never declared reusable

LocalMuonParity = true
FusedHiMuonParity = true
AdamWParity = true

GradientPayloadD2H = 0

AllocatorPolicyUnchanged = true
PhysicalReuseIntroduced = false
ArenaIntroduced = false
```

---

## 27. Failure classes

```text
FAIL_A01_EARLY_REUSE
FAIL_A01_PENDING_QUEUE_WRITE_REUSE
FAIL_A01_MAP_ACTIVE_REUSE
FAIL_A01_CROSS_DEVICE_LEASE_ADOPTION
FAIL_A01_CROSS_QUEUE_LEASE_ADOPTION
FAIL_A01_CROSS_CLASS_LEASE_ADOPTION
FAIL_A01_WRITABLE_RANGE_OVERLAP
FAIL_A01_RANGE_OUT_OF_BOUNDS
FAIL_A01_STALE_LEASE
FAIL_A01_NATIVE_SUBMISSION_TICKET_MISSING
FAIL_A01_NATIVE_SUBMISSION_TICKET_MISMATCH
FAIL_A01_COMPLETION_OVERCLAIM
FAIL_A01_REGISTRY_EPOCH_CONFUSION
FAIL_A01_VERIFICATION_EPOCH_CONFUSION
FAIL_A01_ALIAS_SWEEP_WHILE_INFLIGHT
```

Not every failure class is yet exercised by a physical runtime test in this code bake. The specification defines the authority boundary; promotion evidence remains separate.

---

## 28. A02 admission rule

A02 may consider reuse only when A01 can prove the owned allocation/range is no longer active.

At minimum:

```text
logical state = Released
tracked GPU accesses completed
pending queue writes = 0
map state = Unmapped
owned allocation authority valid
no writable overlap
```

Anything conservative or externally owned remains outside the arena.

---

## 29. Final authority declaration

Before A01:

> ASH could identify buffer roles and movement, but logical scope, alias tombstones, queue writes, and generic blocking waits did not form an exact GPU completion authority.

After A01:

> Mandatory Local Muon, fused HiMuon, and AdamW candidate submissions bind an ASH submission epoch to the exact `wgpu::SubmissionIndex` returned by `Queue::submit`. Readback mapping is sealed against that exact completion token. Queue writes are represented as pending until a submit binds them. External alias tombstones no longer erase in-flight materialization evidence. Surfaces without cross-submission physical identity remain conservative and are explicitly barred from future arena reuse.

### Center sentence

> **A01 turns `release()` from a guess about GPU lifetime into a separate logical event, then makes exact submission completion the only bridge toward physical retirement.**
