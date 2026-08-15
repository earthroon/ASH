# ASH-BASETRAIN-RAM-ADAM-MV-PCIE-TRANSFER-OVERLAP-R1

## Status

Implementation-aligned BaseTrain optimizer transfer scheduling authority layered on top of `ASH-BASETRAIN-RAM-RESIDENT-ADAM-MV-FINAL-WRITEBACK-R1`.

## Patch identity

```text
ASH-BASETRAIN-RAM-ADAM-MV-PCIE-TRANSFER-OVERLAP-R1
```

## Core contract

```text
Triple-Buffered Optimizer Segment Transfer /
RAM M/V SSOT Preservation /

H2D(k+1) Preparation During Compute(k) /
D2H(k-1) Retirement During Compute(k) /

No Host Serial Segment Barrier /
No Full M/V Clone /
Bounded Transfer Window /

Explicit Segment Lease State /
No Slot Reuse Before D2H Commit /
RAM Commit Before Optimizer Commit /

Measured Transfer·Compute Overlap /
No Guaranteed Hardware Concurrency Claim /
No Optimizer Math Change
```

## 1. Parent authority

Required parent runtime mode:

```text
RAM_RESIDENT_MV
```

The parent contract remains authoritative:

- Adam M SSOT = host physical RAM;
- Adam V SSOT = host physical RAM;
- one-time resume hydration;
- whole-run M/V RAM residency;
- no per-step M/V disk read;
- no per-step M/V disk write;
- final run-completion M/V writeback only;
- `E:\ASH` durable publication through the existing Storage Root Authority;
- no zero-moment fallback, M/V reconstruction, receipt synthesis, or silent disk fallback.

This patch changes transfer scheduling only. It does not move optimizer-state authority out of RAM.

## 2. Explicit admission

New CLI admission:

```text
--admit-ram-adam-mv-pcie-transfer-overlap
```

It is legal only when:

```text
--admit-n8-long-horizon-continuity
--admit-ram-resident-adam-mv
--storage-publication-policy checkpoint
```

are already active.

Overlap admission without RAM-resident Adam M/V fails closed. Internal microbatch child configs explicitly disable this top-level admission.

## 3. Triple-buffer meaning

Triple buffering does **not** mean three complete copies of Adam M/V.

The authoritative state remains exactly one contiguous RAM M pack and one contiguous RAM V pack.

The transfer layer owns exactly three bounded segment leases:

```text
slot0
slot1
slot2
```

The transfer window is bounded to the existing 16 MiB optimizer segment geometry.

The capacity gate accounts for bounded host staging in addition to full resident M/V and the explicit RAM reserve.

R1 reserves a conservative host staging envelope for up to six segment-sized host vectors per slot, covering source weight/M/V staging and candidate weight/M/V retirement without permitting whole-state cloning.

## 4. Existing segment registry remains SSOT

No second optimizer offset registry is introduced.

Every transfer uses the existing packed parameter registry:

```text
parameter
→ packed byte offset
→ logical segment length
→ exact RAM M slice
→ exact RAM V slice
```

Mutable segment byte count must remain within the bounded transfer window.

## 5. Explicit lease state

Each slot has a monotonically increasing lease epoch and a segment identity.

States:

```text
FREE
H2D_RESERVED
H2D_IN_FLIGHT
READY_FOR_COMPUTE
COMPUTE_IN_FLIGHT
READY_FOR_D2H
D2H_IN_FLIGHT
READY_FOR_RAM_COMMIT
RAM_COMMITTED
FAILED
```

A reused slot receives a new lease epoch.

A stale completion, lease-epoch mismatch, segment-identity mismatch, byte-range mismatch, or illegal transition fails closed.

A failed batch quarantines its active slots as `FAILED`; they are not silently returned to `FREE`.

## 6. No slot reuse before RAM commit

A slot may return to `FREE` only after:

```text
GPU candidate result available
→ D2H/readback completion
→ exact M/V RAM range overwrite
→ RAM_COMMITTED
→ FREE
```

A slot still associated with an uncommitted RAM range may not be assigned to another segment.

The ring must be fully drained before the successful overlap receipt can be sealed.

## 7. Backend triple-batch ABI

The existing single-segment AdamW functions remain present as the serial parity/rollback path.

R1 adds a batch ABI accepting one to three segment inputs:

```text
r6_adamw_candidate_triple_batch(...)
```

For each input segment the batch path consumes:

- the existing raw GPU gradient lease when gradient data exists;
- bounded source weight staging;
- bounded source M staging;
- bounded source V staging;
- the existing AdamW optimizer step and LR bits.

The AdamW WGSL formula is unchanged.

## 8. Removal of the per-segment host wait chain

The pre-R1 helper executes each segment approximately as:

```text
prepare one segment
→ submit
→ device.poll(Wait)
→ map weight
→ map M
→ map V
→ map status
→ next segment
```

The R1 overlap path instead submits up to three independent segment command buffers without an intervening host `Poll(Wait)`.

After each slot submission, readback map requests are registered immediately. The host can then prepare and submit the next slot while earlier GPU work remains outstanding.

After the current one-to-three-slot batch has been submitted, one batch drain `device.poll(PollType::Wait)` services the outstanding mappings. Candidate payloads are then retired in deterministic segment order.

This removes the mandatory per-segment host wait barrier. It does not claim that the backend or hardware necessarily executes PCIe DMA and compute simultaneously.

## 9. H2D(k+1) preparation

After slot `k` is submitted, the host may prepare the bounded weight/M/V inputs for slot `k+1` without waiting for slot `k` map completion.

There is no whole-M/V clone and no unbounded pending-segment allocation.

The gradient remains on the existing raw GPU lease path and is not converted into a full host gradient payload.

## 10. D2H(k-1) retirement

Each submitted segment encodes candidate weight/M/V/status copy-to-readback operations and registers mapping callbacks before the batch drain.

These operations may be in flight while later independent slot work is prepared/submitted.

Actual backend copy-engine/compute concurrency is not assumed. RAM authority is updated only after the batch completion evidence is available.

## 11. RAM commit barrier

For each completed slot:

```text
candidate M/V readback
→ resident.update_slices(exact_offset)
→ lease identity verification
→ RAM_COMMITTED
```

Only after every expected optimizer segment has reached the RAM authority may the enclosing optimizer transaction advance its generation/optimizer/cursor/scheduler state.

Partial parameter completion is not an optimizer commit.

## 12. No disk regression

R1 derives physical hot-path M/V disk counters from the existing R6A step receipts.

The overlap receipt is sealable only when:

```text
perStepMVDiskReadBytes  = 0
perStepMVDiskWriteBytes = 0
```

Final N8 M/V writeback is excluded from the per-step write count because it remains the parent run-completion durable seal.

No PCIe scheduling failure may trigger a disk-backed optimizer fallback.

## 13. No optimizer math change

Frozen:

```text
subgroup32 AdamW kernel
beta1
beta2
epsilon
weight decay
bias correction
scheduler LR bits
gradient accumulation8
R14 backward authority
```

The new path changes only segment preparation, in-flight submission, readback retirement, and RAM commit scheduling.

The legacy serial RAM-M/V path remains compiled and available when overlap admission is absent.

## 14. Measurement authority

R1 records:

```text
transferSlotCount
transferWindowBytes
boundedHostStagingBytes
segmentCount
maximumInflightSegments
h2dBytes
d2hBytes
hostPrepareWallNs
hostSerialWaitNs
hostRamCommitWallNs
optimizerStepWallNs
```

and all lease/fallback violation counters.

The runtime receipt is:

```text
optimizer_pcie_overlap_ledger.json
```

The ledger is written before Storage Root publication, so successful N8 durable receipt publication carries the overlap evidence with the run.

## 15. Hardware-overlap claim boundary

R1 explicitly distinguishes pipeline overlap from proven physical copy-engine concurrency.

Current R1 backend records:

```text
overlapMeasurementSupported = 0
measuredTransferComputeOverlapNs = null
```

unless a future backend-specific same-clock-domain measurement path is explicitly admitted.

It is forbidden to synthesize a non-zero physical overlap value from unrelated host and GPU clocks.

Therefore R1 may prove:

- removal of the per-segment host `Poll(Wait)` chain;
- up to three submitted/in-flight segment leases;
- bounded staging;
- exact RAM retirement;
- no disk regression;
- optimizer math preservation.

R1 does **not** by itself prove a specific RTX GPU copy-engine overlap ratio or speedup factor.

## 16. Failure semantics

Any of the following fails closed:

- transfer slot count drift;
- transfer window overflow;
- lease epoch mismatch;
- stale completion identity;
- slot reuse before RAM commit;
- batch output cardinality drift;
- candidate nonfinite status;
- M/V RAM bounds mismatch;
- per-step M/V disk I/O;
- ring not fully drained;
- silent disk fallback;
- optimizer math drift.

A failed in-memory optimizer transaction does not synthesize durable state. The last durable checkpoint remains the restart authority under the parent RAM-resident contract.

## 17. N8 / Storage ordering

Successful N8 execution preserves the ordering:

```text
GEN5 durable parent
→ one-time M/V hydration
→ triple-buffered RAM↔GPU segment execution
→ GEN13 / OPT13 / CURSOR83
→ final M/V writeback once
→ N8 receipt closure
→ E:\ASH Storage Root verified checkpoint publication
→ RAM-resident M/V PASS
→ PCIe overlap structural PASS
→ N8 PASS
→ Resume-Cut exact-determinism frontier
```

The overlap ledger must exist before Storage Root receipt copying.

The overlap PASS must not precede durable Storage Root publication or the parent RAM-resident final-writeback PASS.

## 18. PASS

Structural/runtime PASS:

```text
PASS_ASH_BASETRAIN_RAM_ADAM_MV_PCIE_TRANSFER_OVERLAP_R1
```

Meaning:

- exactly three transfer slots exist;
- segment leases are epoch-bound;
- no illegal reuse occurred;
- M/V authority remained in RAM;
- readback retirement completed before RAM commit;
- optimizer transactions did not commit before RAM M/V closure;
- per-step M/V disk I/O remained zero;
- optimizer math was not changed.

## 19. Measurement HOLD

Until an explicitly admitted same-clock-domain physical overlap measurement path exists:

```text
HOLD_ASH_BASETRAIN_RAM_ADAM_MV_PCIE_TRANSFER_OVERLAP_PHYSICAL_MEASUREMENT_NOT_YET_ADMITTED
```

This HOLD does not invalidate the structural overlap pipeline. It prevents a structural scheduling result from being silently promoted into a claim of guaranteed hardware PCIe/compute concurrency.

## 20. Non-goals

R1 does not add:

- pinned host allocation;
- persistent mapped staging;
- adaptive 2/3/4-slot depth;
- explicit CUDA streams;
- backend-specific D3D12/Vulkan copy-queue authority;
- full M/V VRAM residency;
- transfer compression;
- M/V quantization;
- canonical GEN13 parent promotion;
- Resume-Cut determinism proof.

Those remain separate follow-on authorities after the physical N8 result is observed.

## SSOT seal

```text
FULL M/V AUTHORITY = RAM
TRANSFER RING       = 3 bounded temporary segment leases
DISK M/V HOT PATH   = 0
RAM COMMIT          = required before optimizer commit
PHYSICAL OVERLAP    = measured only when supported; never assumed
OPTIMIZER MATH      = unchanged
```
