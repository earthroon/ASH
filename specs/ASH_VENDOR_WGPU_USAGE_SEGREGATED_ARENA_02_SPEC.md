# ASH-VENDOR-WGPU-USAGE-SEGREGATED-ARENA-02

## Usage-Segregated Physical Buffer Reuse / A01 Retirement Admission / Exact-Usage Arena

### 0. Status

| Field | Authority |
|---|---|
| Patch ID | `ASH-VENDOR-WGPU-USAGE-SEGREGATED-ARENA-02` |
| Parent | `ASH-VENDOR-WGPU-SUBMISSION-EPOCH-LEASE-01` |
| First physical reuse | yes |
| External borrowed reuse | forbidden |
| `ConservativeUnknown` reuse | forbidden |
| `create_buffer_init` migration | forbidden in A02 |
| Upload transport change | forbidden in A02 |
| Bulk readback removal | forbidden in A02 |
| Submission coalescing | forbidden in A02 |
| Static closure | `STATIC_SOURCE_ONLY` until Rust/GPU execution |
| Next | `ASH-VENDOR-WGPU-STAGING-AND-COMPACT-READBACK-RING-03` |

A02 is the first patch allowed to reuse a physical `wgpu::Buffer`. Reuse is admitted only after A01 proves the previous logical lease is `RetiredComplete`.

---

## 1. Core SSOT

```text
Arena reuse admission
=
A01 RetiredComplete
AND AllocationAuthority::Owned
AND CompletionCoverage::ExactTracked
AND map state Unmapped
AND no pending queue write
AND no active arena incarnation
```

`drop`, Rust scope exit, alias tombstone, equal byte length, or equal semantic role are not reuse authority.

---

## 2. Segregation authority

Each reusable pool is keyed by:

```text
DeviceAuthorityId
QueueAuthorityId
exact wgpu BufferUsages bits
ArenaBindingClass
resolved alignment
aligned capacity class
```

A02 v1 requires exact usage-bit equality. Usage-superset reuse is not admitted.

Primary classes:

```text
Storage
Uniform
Readback
CopyOnly
```

`MAP_READ` readback storage is never merged with primary `STORAGE` allocations.

---

## 3. MAP_READ policy

A02 preserves a dedicated readback pool:

```text
COPY_DST | MAP_READ
```

The readback pool uses whole-buffer reuse only. One physical readback buffer has at most one live logical arena lease at a time.

This avoids mapping one page range while unrelated ranges on the same physical buffer are still live.

---

## 4. A02 v1 page/range model

A02 seals page/range identity now but intentionally uses one reusable range per physical page on migrated production paths until a target-GPU page-size benchmark exists.

```text
ArenaPage
= one owned physical wgpu::Buffer

ArenaRange v1
= offset 0 / aligned capacity

ArenaLease
= logical size + page identity + incarnation
```

This provides real warm-path physical reuse without inventing an unbenchmarked multi-slot page size. Multi-slot storage suballocation may be promoted in a later A02 revision without changing the page/range ABI.

---

## 5. Logical size versus reserved capacity

```text
logical_size
!=
reserved_size
```

The logical payload size remains the copy/semantic authority. Reserved capacity may be alignment-rounded.

A migrated callsite must never use `buffer.size()` as tensor payload cardinality authority.

---

## 6. Alignment

A02 resolves alignment from runtime/device authority and public wgpu constants:

```text
Storage class
→ device.limits().min_storage_buffer_offset_alignment

Uniform class
→ device.limits().min_uniform_buffer_offset_alignment

COPY_SRC/COPY_DST
→ wgpu::COPY_BUFFER_ALIGNMENT

MAP_READ/MAP_WRITE
→ wgpu::MAP_ALIGNMENT
```

No hardcoded `256` binding alignment is permitted.

---

## 7. Initialization contract

Arena admission classifies initialization semantics:

```text
FullOverwriteBeforeRead
CopyDestinationBeforeRead
ExplicitClearBeforeRead
HostInitializationRequired
Unknown
```

A02 v1 reusable production paths admit only `FullOverwriteBeforeRead` and `CopyDestinationBeforeRead`.

`HostInitializationRequired` and `Unknown` remain dedicated.

Therefore existing `create_buffer_init` source/params/state buffers are not migrated by A02.

---

## 8. Migrated Local Muon surfaces

Reusable storage:

```text
local_muon.candidate_weight
local_muon.candidate_momentum
local_muon.update
```

Reusable whole readback:

```text
local_muon.readback.weight
local_muon.readback.momentum
local_muon.readback.update
local_muon.readback.status
```

Dedicated in A02:

```text
params
descriptors/source uploads
source weight/source momentum
status primary buffer
packed gradient producer
```

The packed-gradient producer remains outside A02 because A01 still classifies its cross-submission completion authority conservatively.

---

## 9. Migrated Fused HiMuon surfaces

Reusable storage:

```text
fused_muon.candidate_weight
fused_muon.candidate_momentum
fused_muon.update
```

Reusable readback:

```text
fused_muon.readback.weight
fused_muon.readback.momentum
fused_muon.readback.update
fused_muon.readback.status
```

Params, descriptors, source weight, source momentum, and primary status remain on their current allocation/initialization path.

---

## 10. Migrated AdamW surfaces

Reusable storage:

```text
adamw.candidate_weight
adamw.candidate_m
adamw.candidate_v
```

Reusable readback:

```text
adamw.readback.weight
adamw.readback.m
adamw.readback.v
adamw.readback.status
```

AdamW params, source W/M/V, row map, and primary status keep current `create_buffer_init` semantics.

---

## 11. Physical identity handoff to A01

A02 physical pages receive a real A01 `PhysicalAllocationId` once, at page creation.

Reused pages bind into later tracked submissions through:

```text
LeaseAllocationKind::OwnedExisting(PhysicalAllocationId)
SubmissionLeaseSpec::owned_existing(...)
SubmissionLeaseSpec::readback_existing(...)
```

A reused page must never be reported by A01 as a newly-created physical allocation for every submission.

---

## 12. Incarnation / ABA guard

Every reacquisition increments page incarnation.

```text
same physical page
+ same offset
+ new incarnation
=
new logical arena lease
```

A stale incarnation cannot reclaim or mutate the current page state.

---

## 13. Reclaim transaction

```text
optimizer submission
↓
A01 exact completion
↓
readback unmap
↓
A01 logical release
↓
A01 assert_reuse_eligible
↓
physical-allocation identity parity
↓
A02 reclaim
↓
page free for next acquire
```

Reclaim before `RetiredComplete` is `FAIL_A02_EARLY_REUSE`.

---

## 14. Allocation selection

A02 v1 selection is deterministic:

```text
exact ArenaKey
→ exact aligned-capacity class
→ first lowest-ordinal free page
```

No hash-iteration-dependent random selection.

---

## 15. Semantic role and physical reuse

Semantic role is not the pool key. A retired `MuonCandidateWeight` page may later back `AdamWCandidateM` only when all physical compatibility dimensions match.

The new logical lease receives a new semantic role and incarnation. Old semantic identity never survives through physical reuse.

---

## 16. Generation-sealed cache

The existing generation-sealed Muon cache remains a semantic residency authority and is not absorbed into A02.

```text
Generation-Sealed Muon Cache
= persistent semantic state authority

A02 Arena
= ephemeral physical capacity reuse authority
```

---

## 17. Telemetry

A02 records at least:

```text
acquire_count
reuse_hit_count
reuse_miss_count
new_page_count
page_destroy_count
requested_bytes
reserved_bytes
retained_page_bytes
peak_retained_page_bytes
internal_fragmentation_bytes
early_reuse_reject_count
mapped_reuse_reject_count
pending_write_reject_count
usage_mismatch_reject_count
alignment_reject_count
stale_range_reject_count
page_size_as_logical_size_count
reclaimed_range_count
```

`retained_page_bytes` is not claimed to be physical VRAM residency.

---

## 18. Behavior-preserving boundaries

A02 changes physical allocation reuse only. It must preserve:

```text
WGSL source
optimizer formulas
planner domains
workgroup counts
copy payload sizes
bulk D2H semantics
exact A01 waits
queue submission cardinality
candidate output authority
AdamW/Muon disjoint ownership
```

A02 does not claim optimizer wall-time promotion until target GPU benchmarking.

---

## 19. Mandatory failure classes

```text
FAIL_A02_EARLY_REUSE
FAIL_A02_NON_OWNED_ADMISSION
FAIL_A02_UNKNOWN_COMPLETION_ADMISSION
FAIL_A02_DEVICE_MISMATCH
FAIL_A02_QUEUE_MISMATCH
FAIL_A02_USAGE_MISMATCH
FAIL_A02_MAP_ACTIVE_REUSE
FAIL_A02_PENDING_QUEUE_WRITE_REUSE
FAIL_A02_WRITABLE_RANGE_OVERLAP
FAIL_A02_STALE_RANGE_HANDLE
FAIL_A02_RANGE_ALIGNMENT
FAIL_A02_RANGE_OUT_OF_BOUNDS
FAIL_A02_PAGE_SIZE_AS_LOGICAL_SIZE
FAIL_A02_HOST_INIT_MIGRATION
FAIL_A02_ACTIVE_PAGE_EVICTION
```

---

## 20. Static validation

Code bake includes:

```text
tools/ash_vendor_buffer_a02_static_validate.py
```

It validates:

```text
A01 parent still passes
arena module/export exists
OwnedExisting physical identity path exists
external borrowed and ConservativeUnknown are rejected
exact usage bits are in ArenaKey
MAP_READ and STORAGE are segregated
MAP/COPY/device binding alignment authority exists
create_buffer_init callsites remain outside arena migration
Local/Fused/AdamW candidate/readback paths use A02
all arena leases are reclaimed through A01 lease IDs
WGSL and Cargo configuration remain unchanged
```

This is `STATIC_SOURCE_ONLY`. Rust typecheck and physical GPU execution are separate evidence.

---

## 21. Promotion target

Physical promotion requires at minimum:

```text
A01ParentValid = true
EarlyReuseCount = 0
NonOwnedAdmissionCount = 0
UnknownCompletionAdmissionCount = 0
DeviceMismatchCount = 0
QueueMismatchCount = 0
UsageMismatchCount = 0
StaleRangeCount = 0
LocalMuonParity = true
FusedHiMuonParity = true
AdamWParity = true
BulkReadbackSemanticsUnchanged = true
SubmissionCountSemanticsUnchanged = true
WarmArenaReuseObserved = true
WarmEligibleCreateBufferDelta = 0
```

The present bake must not claim these runtime values until executed on the target Rust/wgpu/GPU environment.

---

## 22. Next handoff

A02 leaves `create_buffer_init` and repeated upload transport visible by design.

A03 therefore owns:

```text
persistent upload/staging reuse
small parameter/descriptor transport
compact readback ring
```

### Center sentence

> **A01 proves when bytes are dead. A02 is allowed to reuse only those dead bytes, and only inside the same device, queue, exact usage, alignment, and capacity contract. Equal size is not permission. `RetiredComplete` is permission.**
