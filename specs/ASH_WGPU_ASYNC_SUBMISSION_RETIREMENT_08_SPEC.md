# ASH-WGPU-ASYNC-SUBMISSION-RETIREMENT-08

## Callback-Observed Completion / Nonblocking Poll / Deferred Retirement

### 0. Status

| Field | Authority |
|---|---|
| Patch ID | `ASH-WGPU-ASYNC-SUBMISSION-RETIREMENT-08` |
| Parent C07 | `ASH-GPU-EVIDENCE-COMPACTION-07` |
| Lifetime SSOT | A01 `SubmissionEpoch` + lease retirement disposition |
| Physical reuse SSOT | A02 arena, only after A01 `RetiredComplete` |
| Compact readback SSOT | A03 whole-buffer compact ring |
| Evidence parent | C07 compact evidence |
| Completion observation | `Queue::on_submitted_work_done` + nonblocking `Device::poll(Poll)` |
| Map observation | atomic `AsyncMapTicket` |
| Hot-path blocking wait target | zero in `ACTIVE_ASYNC` |
| Multi-generation speculation | forbidden |
| Submission coalescing | not introduced |
| Mixed precision | not introduced |
| Validation class in this bake | `STATIC_SOURCE_ONLY` |

### Current bake rollout status

This bake physically installs the C08 completion mailbox, nonblocking progress primitive, async map ticket, deferred retirement queue, and callback-only qualification fixture. All A01-tracked submissions arm a completion callback immediately after submit. Local Muon, fused HiMuon, AdamW R5, and C07 readback callbacks no longer require blocking `mpsc::Receiver::recv()` to observe map completion.

Production `MIRROR_VERIFIED` keeps the parent exact wait as a reference while the callback path is qualified. `ACTIVE_ASYNC` is intentionally not physically admitted in this bake because the upstream B06 active device successor path is still not physically admitted and because no device-loss fault qualification receipt has been produced in this environment. The built-in qualification receipt therefore records `activePhysicalAdmission=false`.

C08 must not turn an API presence claim into a physical promotion claim.

---

## 1. Authority split

```text
A01 = exact lifetime and retirement truth
A02 = reusable physical allocation truth
A03 = reusable upload / compact readback truth
B04-B06 = optimizer semantic state / generation truth
C07 = compact numerical evidence truth
C08 = completion observation and retirement scheduling
```

C08 may change *how* completion is observed. It may not weaken the meaning of completion.

---

## 2. Absolute lifetime invariant

```text
LogicalRelease != GpuCompletion != Reusable
```

Reusable requires:

```text
logical release
AND exact tracked completion
AND pending queue write count == 0
AND map state == Unmapped
AND no active overlapping lease
```

Timeout, cancellation, and device loss do not satisfy exact completion.

---

## 3. Tracked submit callback

Every A01 `submit_with_leases` submission performs:

```text
Queue::submit
→ exact SubmissionEpoch mint
→ Queue::on_submitted_work_done callback arm
```

The callback performs only an atomic completion-mailbox update. It does not mutate the allocator, map buffers, decode readback payloads, publish generations, or perform filesystem I/O.

The queue callback is a completion observation surface. A01 remains the owner of `completed_through`.

---

## 4. Completion mailbox

Each tracked queue domain owns:

```text
highestCompletedOrdinal : AtomicU64
callbackCount           : AtomicU64
```

A nonblocking progress call consumes these atomics into the A01 queue-domain completion prefix.

For a single ordered queue, observing completion of epoch `N` admits all earlier epochs in that queue prefix as complete.

---

## 5. Nonblocking progress pump

Hot-path progress uses:

```text
Device::poll(PollType::Poll)
→ consume completion mailboxes
→ update A01 completedThrough
→ progress map states
→ progress deferred retirement
```

Hot-path use of:

```text
PollType::Wait
PollType::WaitForSubmissionIndex
```

is forbidden in `ACTIVE_ASYNC`.

Blocking waits remain allowed only for:

```text
Mirror reference qualification
shutdown drain
recovery / diagnostic reference
```

---

## 6. No busy-spin progress

C08 must not implement:

```text
while !complete {
    device.poll(Poll)
}
```

as production progress.

The qualification fixture uses bounded nonblocking polls with a bounded thread park between polls. Poll cadence is a liveness policy, not a resource-reuse authority.

---

## 7. Async map ticket

Map completion is represented by:

```text
Requested
→ Ready | Failed
→ Consumed
→ Unmapped
```

The callback only changes the atomic state. Host decoding occurs outside the callback.

GPU submission completion and map readiness are distinct conditions. Host read requires both the relevant submission completion and map readiness.

---

## 8. Parent readback migration

C08 replaces blocking channel receives on the mandatory optimizer/evidence map surfaces with `AsyncMapTicket`:

```text
Local Muon readback
Fused HiMuon readback
AdamW R5 readback
C07 compact evidence readback
```

Mirror mode still performs its exact wait before consuming the map ticket. This preserves parent numerical behavior while removing the second blocking primitive (`recv`) from the path.

---

## 9. Deferred retirement

C08 introduces a scheduling queue for logical-release-first retirement:

```text
logical release intent
→ DeferredRetirementQueue
→ A01 completion becomes true
→ map lifecycle is closed
→ A02 reclaim / A03 compact slot release
```

Calling logical release does not return the underlying A02 page to the free pool.

---

## 10. A02 reuse remains strict

C08 never directly marks an arena page reusable. It calls the existing A02 reclaim function only after A01 reports `RetiredComplete`.

The C08 qualification fixture explicitly attempts an early A02 reclaim and requires that attempt to fail before it permits the deferred retirement to complete.

---

## 11. A03 compact ring

C08 does not create a second readback pool.

A03 still owns:

```text
one compact ring slot
=
one whole MAP_READ buffer lease
```

A compact slot is not free until GPU completion, host read, unmap, A01 retirement, and A02 reclaim are complete.

Ring exhaustion in Active must produce backpressure, not an unbounded dedicated readback allocation fallback.

---

## 12. In-flight budget

C08 defines an explicit budget ABI:

```text
max submission count
max reserved bytes
max pending maps
max compact readbacks
```

The values are promotion/benchmark policy and are not silently autotuned by the core lifetime layer.

Budget exhaustion returns `DeferredCapacity`; it does not block waiting for the GPU and does not silently expand the ring.

---

## 13. Generation barrier

C08 does not introduce speculative optimizer generations.

```text
uncommitted trainable generation count <= 1
```

Within one candidate generation, multiple ordered Local/Fused/AdamW/evidence submissions may be in flight. Generation `N+2` may not start before generation `N+1` reaches the semantic commit barrier.

---

## 14. Same-queue dependency rule

C08 may remove a CPU wait between candidate writers and C07 evidence only when both are ordered on the same queue and the evidence read is submitted after all required candidate writes.

C08 does not introduce a cross-queue synchronization protocol.

---

## 15. Cancellation

Cancellation means:

```text
semantic promotion forbidden
submitted GPU work remains in flight
logical state becomes cancelled/rejected
deferred retirement waits for actual completion
```

Cancellation never grants early buffer reuse.

---

## 16. Device loss

Device loss invalidates pending runtime work. It is not interpreted as successful completion.

All allocations owned by the lost device are non-reusable in a replacement device domain. B04/B06 state must explicitly rebootstrap through their existing generation rules.

A wall-clock watchdog may trigger recovery diagnostics but may not set A01 `completedThrough`.

---

## 17. Shutdown

Blocking drain is explicitly allowed at shutdown:

```text
stop admissions
→ exact drain outstanding tracked work
→ consume map callbacks
→ unmap
→ retire
→ shutdown
```

Shutdown waits are separately counted from hot-path waits.

---

## 18. Runtime modes

```text
OFF
MIRROR_VERIFIED
ACTIVE_ASYNC
```

`OFF` preserves parent behavior.

`MIRROR_VERIFIED` requires B06/C07 to be enabled, arms callbacks, runs the callback-only qualification fixture, and retains the parent exact wait as reference.

`ACTIVE_ASYNC` requires B06 Active, C07 Active, a real segmented device successor consumer, and an adopted physical C08 qualification receipt with `activePhysicalAdmission=true` and zero hot-path waits.

There is no silent Active-to-Mirror fallback.

---

## 19. Physical qualification receipt

The built-in executable fixture verifies:

```text
callback-only completion without WaitForSubmissionIndex
exact-wait parity
map callback readiness
early reclaim rejection
deferred compact retirement
```

Device-loss injection and the final zero-hot-path-wait production qualification require an external physical promotion run. The current source bake does not forge those results.

---

## 20. Submission semantics

C08 is not a submission-coalescing patch.

It preserves the existing number and ordering of optimizer submissions unless a later patch explicitly changes that authority. Success is measured by removal of CPU blocking waits, not by fewer submits.

---

## 21. Telemetry

C08 tracks at minimum:

```text
submitted count
completion callbacks armed / observed
nonblocking poll count
hot-path blocking wait count
Mirror blocking wait count
shutdown blocking wait count
blocking channel receive count
busy-spin count
pending submission / map peaks
deferred retirement / retirement count
capacity defer count
compact ring backpressure count
cancellation count
early-reuse violation count
device-loss invalidation / false-completion count
watchdog alerts
```

These counters are scheduling observations, not VRAM measurements.

---

## 22. Failure classes

```text
FAIL_C08_RUNTIME_MODE_UNKNOWN
FAIL_C08_MODE_MATRIX
FAIL_C08_ACTIVE_UPSTREAM_NOT_ADMITTED
FAIL_C08_ACTIVE_PHYSICAL_ADMISSION_MISSING
FAIL_C08_ASYNC_QUALIFICATION_MISSING
FAIL_C08_CALLBACK_REGISTRATION_MISSING
FAIL_C08_QUEUE_SUBMISSION_AUTHORITY_BYPASS
FAIL_C08_COMPLETION_EPOCH_REGRESSION
FAIL_C08_FALSE_EARLY_COMPLETION
FAIL_C08_MAP_STATE_MISMATCH
FAIL_C08_HOST_READ_BEFORE_MAP_READY
FAIL_C08_EARLY_PHYSICAL_RETIREMENT
FAIL_C08_INFLIGHT_REUSE
FAIL_C08_CANCELLED_EARLY_REUSE
FAIL_C08_ACTIVE_LEASE_EVICTION
FAIL_C08_COMPACT_RING_UNBOUNDED_GROWTH
FAIL_C08_BACKPRESSURE_BYPASS
FAIL_C08_MULTI_GENERATION_SPECULATION
FAIL_C08_HOT_PATH_BLOCKING_WAIT
FAIL_C08_BLOCKING_CHANNEL_RECEIVE
FAIL_C08_BUSY_SPIN_PROGRESS
FAIL_C08_TIMEOUT_AS_COMPLETION_AUTHORITY
FAIL_C08_DEVICE_LOSS_FALSE_COMPLETION
FAIL_C08_SHUTDOWN_UNDRAINED_SUBMISSION
```

---

## 23. Static source gate

The bake carries:

```text
tools/ash_wgpu_async_submission_retirement_08_static_validate.py
```

The gate verifies:

```text
C08 module export
A01 callback mailbox and callback arming
nonblocking Poll path
A01 exact wait preserved for allowlisted reference paths
AsyncMapTicket adoption on Local/Fused/AdamW/C07
blocking mpsc receive removed from those mandatory readback helpers
deferred retirement uses existing A02/A03 release authority
A03 compact lease is schedulable without a second physical pool
production scheduler runs C08 qualification
Active mode is upstream-gated and physical-qualification-gated
current built-in receipt does not claim Active physical admission
no optimizer WGSL changes from C07
Cargo surface remains parent-identical
```

`STATIC_SOURCE_ONLY` is not Rust type-check, GPU execution, or C08 physical promotion.

---

## 24. Active promotion gate

A physical promotion run must prove:

```text
A01/A02/A03/C07/B06 parent gates valid
callback-only completion PASS
map callback PASS
deferred retirement parity PASS
ring backpressure PASS
cancellation retirement PASS
device-loss invalidation PASS
shutdown drain PASS
hot-path WaitForSubmissionIndex = 0
blocking completion recv = 0
busy-spin = 0
early reuse = 0
multi-generation speculation = 0
submission semantics parity = true
```

Only then may an external qualification receipt set:

```text
activePhysicalAdmission = true
```

---

## 25. Center declaration

> **C08 does not make completion less exact. It makes waiting less synchronous. Every tracked submit still belongs to an A01 SubmissionEpoch; the queue callback merely reports the highest completed prefix into an atomic mailbox. Logical release may happen early, but A02 reuse cannot. Map readiness remains an independent state, compact-ring exhaustion becomes backpressure rather than hidden allocation growth, and cancellation or timeout can never masquerade as GPU completion. The current bake proves the callback/map/deferred-retirement machinery and Mirror wiring while deliberately refusing to claim Active promotion before the upstream device-successor path and fault qualification exist.**
