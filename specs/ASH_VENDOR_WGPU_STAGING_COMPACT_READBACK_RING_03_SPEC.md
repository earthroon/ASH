# ASH-VENDOR-WGPU-STAGING-AND-COMPACT-READBACK-RING-03

## Persistent Upload Staging / Compact Status Readback Ring / A02 Destination Reuse

### 0. Status

| Field | Authority |
|---|---|
| Patch ID | `ASH-VENDOR-WGPU-STAGING-AND-COMPACT-READBACK-RING-03` |
| Parent A01 | `ASH-VENDOR-WGPU-SUBMISSION-EPOCH-LEASE-01` |
| Parent A02 | `ASH-VENDOR-WGPU-USAGE-SEGREGATED-ARENA-02` |
| Pinned wgpu API | `wgpu 26.0.1` through `wgpu26` |
| Primary role | host↔device transfer reuse and bounded compact-status readback scheduling |
| Upload allocation authority | `wgpu::util::StagingBelt` transport chunks |
| GPU destination authority | A02 `ArenaLease` |
| Submission/completion authority | A01 exact tracked submission |
| Bulk optimizer readback | preserved |
| Blocking wait | preserved |
| Muon momentum residency | not introduced |
| GPU evidence reduction | not introduced |
| Validation class in this bake | `STATIC_SOURCE_ONLY` |
| Next patch | `ASH-TENSORCUBE-MUON-RESIDENT-STATE-GRAPH-04` |

A03 answers:

> How can host-originated optimizer payloads reach reusable A02 destinations without allocating a fresh initialized GPU buffer for every batch, while small existing status readbacks use a bounded scheduling ring without changing their semantics?

A03 does **not** claim that host↔device bytes disappear. It changes the transfer vessel, not the semantic payload.

---

## 1. Authority chain

```text
A00
semantic role / owner / movement inventory
        ↓
A01
submission completion / lease retirement
        ↓
A02
usage-segregated reusable GPU destinations
        ↓
A03
reusable upload transport + compact status scheduling
```

The SSOT split is strict:

```text
A01 = lifetime authority
A02 = destination allocation authority
A03 = transfer scheduling authority
```

A03 must never become a competing primary GPU allocator.

---

## 2. wgpu 26.0.1 StagingBelt lifecycle

The pinned source exposes the canonical lifecycle:

```text
StagingBelt::write_buffer(...)
        ↓
StagingBelt::finish()
        ↓
Queue::submit(...)
        ↓
StagingBelt::recall()
```

`recall()` schedules remapping of closed staging chunks after their GPU copy use is complete. Device polling performed by the existing A01/readback path progresses these map callbacks.

A03 must **not** use or claim `finish_and_recall_on_submit()`: that API is not present in the pinned `wgpu 26.0.1` implementation used by this codebase.

Required ordering in every migrated optimizer submission:

```text
stage uploads into command encoder
→ finish staging belts
→ A01 exact submit
→ recall staging belts
→ existing exact completion / readback path
```

No validation that may intentionally return before submission is placed between `finish()` and the A01 submit call.

---

## 3. Upload lanes

A03 owns two reusable transfer lanes:

```text
Control
BulkState
```

### Control

Typical payloads:

```text
kernel params
structural descriptors
row maps
status initialization
small metadata
```

Policy baseline:

```text
chunk size = 256 KiB
```

### BulkState

Typical payloads:

```text
source weight
source Muon momentum
AdamW source weight / M / V
```

Policy baseline:

```text
chunk size = 8 MiB
```

These are transfer classes, not semantic owners. There is no separate Local-Muon, HiMuon, or AdamW staging allocator.

---

## 4. Destination contract

Every normal migrated upload targets an A02-owned lease with exact `COPY_DST` usage.

```text
uniform payload
→ UNIFORM | COPY_DST

storage payload
→ STORAGE | COPY_DST [| exact extra usage]
```

Status buffers that are later copied to readback use:

```text
STORAGE | COPY_DST | COPY_SRC
```

A03 may not upload directly into:

```text
external borrowed buffers
ConservativeUnknown completion buffers
unregistered raw backing buffers
```

The A01/A02 physical allocation identity remains authoritative.

---

## 5. Initialization contract transition

Before A03, migrated host-originated buffers were created as initialized buffers.

A03 changes the transport contract to:

```text
A02 destination
ArenaInitializationContract::CopyDestinationBeforeRead
        +
A03 full staging copy
        ↓
compute read
```

Therefore the destination is reusable only because the logical payload is fully overwritten before compute reads it.

No stale bytes from a previous arena incarnation may become semantic input.

---

## 6. Copy alignment and zero padding

A03 separates:

```text
logical payload size
aligned copy size
```

The aligned size follows `wgpu::COPY_BUFFER_ALIGNMENT`.

If padding is required:

```text
padding bytes = 0
```

is mandatory.

The A02 destination reserved capacity must cover the aligned copy size, while shader binding semantics continue to use the actual logical structure contract.

Failure classes:

```text
FAIL_A03_COPY_ALIGNMENT
FAIL_A03_COPY_RANGE_OUT_OF_BOUNDS
FAIL_A03_NONZERO_PADDING
```

---

## 7. Oversize compatibility path

A03 v1 bounds normal belt writes with:

```text
A03_MAX_RING_WRITE_BYTES = 32 MiB
```

A larger single payload may use the compatibility path:

```text
queue.write_buffer(A02 destination)
→ A01 pending queue-write ledger
→ same existing optimizer submit
```

This fallback:

- does not create an extra submit;
- does not bypass A01 lifetime authority;
- does not make the payload resident;
- is explicitly counted as `OversizeCompat`.

The threshold is a v1 transfer policy, not a claim of optimal physical performance.

---

## 8. Same-submission ordering

Normal staging uploads are encoded into the **same command encoder** as the consuming compute pass.

Canonical order:

```text
upload copies
→ compute pass
→ result copies to readback
→ finish encoder
→ one A01 submit
```

Forbidden:

```text
submit(upload)
wait
submit(compute)
```

A03 must not increase optimizer submission count merely to perform uploads.

---

## 9. Migrated Local Muon inputs

The A03 batch path migrates:

```text
params              → Control
non-resident descriptors → Control
non-resident source weight → BulkState
source momentum     → BulkState
status initialization → Control
```

Preserved outside this migration:

```text
gradient-pack producer
resident structural descriptor cache
resident generation-sealed weight cache
candidate output buffers
bulk candidate readbacks
```

The gradient-pack producer remains outside the mandatory A03 batch-upload migration because its cross-submission producer lifetime is a separate authority boundary.

---

## 10. Migrated fused HiMuon inputs

The fused executor migrates:

```text
params          → Control
descriptors     → Control
source weight   → BulkState
source momentum → BulkState
status init     → Control
```

`FUSED_RIGHT` / `FUSED_DOWN` planning, shader math, dispatch geometry, candidate result authority, and bulk readback semantics remain unchanged.

---

## 11. Migrated AdamW inputs

The R5 AdamW candidate path migrates:

```text
params      → Control
weight      → BulkState
M prev      → BulkState
V prev      → BulkState
row map     → Control
status init → Control
```

A03 does not alter the AdamW update formula or AdamW/Muon ownership partition.

---

## 12. Compact status readback ring

A03 introduces a scheduling ring only for **already compact status payloads**.

```text
A03_COMPACT_READBACK_SLOT_COUNT = 4
```

Each slot is backed by one whole A02 `MAP_READ | COPY_DST` buffer lease.

```text
one slot
=
one whole MAP_READ buffer lease
```

There is no byte-range suballocation of mapped readback buffers.

Slot state machine:

```text
Free
→ Encoding
→ InFlight
→ MapRequested
→ HostReadComplete
→ Draining
→ Free
```

A slot may return to `Free` only after the existing A01 map/completion lifecycle has finished and its A02 arena lease is reclaim-eligible.

---

## 13. What “compact” means in A03

A03 compact readback means:

> bounded transport of payloads that were already small.

It does **not** mean:

```text
GPU-generated weight digest
GPU update norm
coverage reduction
momentum digest
candidate checksum
```

Those belong to C07 GPU evidence compaction.

Therefore current bulk readbacks remain:

```text
Local Muon candidate weight
Local Muon candidate momentum
Local Muon orthogonal update

Fused HiMuon candidate weight
Fused HiMuon candidate momentum
Fused HiMuon update

AdamW candidate W
AdamW candidate M
AdamW candidate V
```

---

## 14. Blocking behavior is preserved

A03 does not remove A01 exact completion waits.

```text
WaitForSubmissionIndex
```

remains the completion authority on mandatory optimizer paths.

A03 must not claim asynchronous optimizer retirement. That belongs to C08.

---

## 15. Generation-sealed cache preservation

The existing generation-sealed Muon cache remains semantic residency authority.

A03 does not replace its current queue-write behavior merely for uniformity. Its state ownership changes are deferred to B04, where committed Muon momentum and candidate momentum become an explicit device-resident generation graph.

---

## 16. Telemetry

A03 records at minimum:

```text
upload request count
Control upload count / bytes
BulkState upload count / bytes
staging belt write count / bytes
oversize compatibility count / bytes
migrated initialized-buffer count

compact readback acquire / reuse count
compact ring exhaust count
compact map-request / release count

padding bytes
padding failures
extra upload submission count
armed-but-not-submitted failures
```

Transfer counters are not physical VRAM measurements.

---

## 17. Warm-path target

After warmup under a stable shape, the target is:

```text
eligible migrated create_buffer_init delta = 0
normal staging transport reuses belt chunks
compact status readback reuses A02 backing buffers
extra upload submission count = 0
```

Large oversize compatibility payloads are reported separately and do not falsify this claim.

---

## 18. Behavior preservation

A03 must preserve:

```text
WGSL
optimizer formulas
Muon / HiMuon dispatch domains
AdamW/Muon ownership
candidate cardinality
bulk result readback semantics
gradient D2H = 0
submission-count semantics
exact completion authority
```

A03 changes transfer construction, not numerical authority.

---

## 19. Mandatory failures

```text
FAIL_A03_UPLOAD_TARGET_NOT_OWNED
FAIL_A03_UPLOAD_TARGET_USAGE_MISMATCH
FAIL_A03_UPLOAD_TARGET_COMPLETION_UNKNOWN
FAIL_A03_COPY_ALIGNMENT
FAIL_A03_COPY_RANGE_OUT_OF_BOUNDS
FAIL_A03_NONZERO_PADDING
FAIL_A03_ARMED_ENCODER_NOT_SUBMITTED
FAIL_A03_EXTRA_UPLOAD_SUBMISSION
FAIL_A03_STAGING_UNBOUNDED_GROWTH
FAIL_A03_COMPACT_RING_OVERWRITE
FAIL_A03_COMPACT_SLOT_INFLIGHT_REUSE
FAIL_A03_COMPACT_SLOT_MAPPED_REUSE
FAIL_A03_BULK_READBACK_SEMANTIC_CHANGE
FAIL_A03_EVIDENCE_AUTHORITY_INTRUSION
```

---

## 20. Static source gate

The code bake carries:

```text
tools/ash_vendor_buffer_a03_static_validate.py
```

The static gate verifies, among other things:

```text
A03 module exported
pinned StagingBelt API uses finish → submit → recall
no unavailable finish_and_recall_on_submit API
COPY_DST destinations are A02-owned
zero padding is explicit
Local/Fused/AdamW input migration exists
status readback uses the compact scheduling ring
bulk readbacks remain present
no new GPU evidence reduction authority
no extra direct queue.submit in migrated executors
A01 owned-existing prevalidation remains before submit
Cargo / WGSL parent surfaces remain unchanged
```

`STATIC_SOURCE_ONLY` is not Rust type-check and not physical GPU promotion.

---

## 21. Promotion gate

Physical A03 promotion requires a real target run proving:

```text
A01 parent valid
A02 parent valid

upload target ownership valid
exact COPY_DST usage valid

armed encoder not submitted = 0
extra upload submissions = 0
nonzero padding failures = 0

compact ring overwrite = 0
compact in-flight reuse = 0
compact mapped reuse = 0

bulk readback semantics unchanged
gradient D2H = 0

Local Muon parity = true
Fused HiMuon parity = true
AdamW parity = true

generation cache authority preserved
```

Static source validation alone does not satisfy this runtime promotion gate.

---

## 22. B04 handoff

A03 leaves intentional traffic:

```text
source weight H2D
source momentum H2D
AdamW source state H2D
candidate payload D2H
blocking exact waits
```

The next patch changes the first major semantic state flow:

```text
B04 RESIDENT MUON STATE GRAPH

host source momentum upload
        ↓ retire
GPU committed momentum N
        ↓
GPU candidate momentum N+1
```

### Center declaration

> **A02 made GPU destinations reusable. A03 makes the transport into those destinations reusable. It removes repeated initialized-buffer construction without pretending the payload itself disappeared. Small status readbacks enter a bounded whole-buffer ring, while bulk optimizer outputs, completion waits, and Muon state authority remain untouched for their own later patches.**
