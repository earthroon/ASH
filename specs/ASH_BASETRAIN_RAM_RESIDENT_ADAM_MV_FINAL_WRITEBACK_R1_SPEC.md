# ASH-BASETRAIN-RAM-RESIDENT-ADAM-MV-FINAL-WRITEBACK-R1

## Status

Implementation-aligned BaseTrain optimizer-state storage authority for N8 long-horizon execution.

## Patch identity

```text
ASH-BASETRAIN-RAM-RESIDENT-ADAM-MV-FINAL-WRITEBACK-R1
```

## Core contract

```text
Adam M/V Host-RAM Authority /
One-Time Resume Hydration /
Whole-Run Optimizer State Residency /

No Per-Step M/V Disk Read /
No Per-Step M/V Disk Write /
No HDD Optimizer Hot Path /

Run-Completion Writeback Only /
Final M/V + Weight + Cursor + Scheduler Durable Seal /

E:\ASH Final Durable Authority /
No Zero-Moment Fallback /
No M/V Reconstruction /
No Silent Disk Fallback
```

## 1. Scope

This patch changes optimizer-state ownership, not optimizer math.

The existing subgroup32 segmented AdamW formula, gradient accumulation8 path, scheduler horizon extension, R14 authority, and N8 GEN5→GEN13 geometry remain unchanged.

Only explicit `--admit-ram-resident-adam-mv` execution enters the new path. The legacy packed-disk optimizer path remains available when this admission is absent.

## 2. Runtime ownership

During an admitted run:

```text
Adam M SSOT = system physical RAM
Adam V SSOT = system physical RAM
```

The last durable checkpoint remains the restart authority until final writeback succeeds.

The pagefile, virtual address space, receipts, intermediate weights, and run-local manifests are not optimizer-state authorities.

## 3. Explicit admission

New CLI:

```text
--admit-ram-resident-adam-mv
--adam-mv-ram-reserve-bytes <N>
```

R1 requires:

- N8 admission is active;
- durable storage publication policy is `checkpoint`;
- RAM reserve bytes are explicitly non-zero;
- source state is promoted GEN5 / OPT5 / CURSOR19;
- target budget is exactly eight optimizer commits.

There is no automatic RAM-or-disk best-effort mode.

## 4. Physical RAM capacity gate

The runtime reads available **physical RAM**, not pagefile-backed commit capacity.

Admission requires:

```text
availablePhysicalRamBytes
>= adamMBytes + adamVBytes + explicitReserveBytes
```

On Windows the implementation uses `GlobalMemoryStatusEx` and `ullAvailPhys` semantics.

Insufficient memory fails closed with the RAM-resident capacity HOLD. It does not silently fall back to disk-backed M/V.

## 5. One-time hydration

The promoted GEN5 manifest binds the initial Adam M/V sizes and SHA256 digests.

Before allocation, source M/V files must exist with exact declared lengths.

The generic resume verifier intentionally avoids a redundant full M/V digest scan in RAM mode. Hydration itself performs the single authoritative full M/V physical read and SHA verification.

Hydration uses bounded aligned reads and materializes two contiguous host allocations:

```text
AdamMResidentPack : Vec<f32>
AdamVResidentPack : Vec<f32>
```

No per-parameter allocation forest and no full-buffer clone are admitted.

## 6. Segment authority reuse

The existing packed parameter offset registry remains the sole segment address authority.

For each AdamW segment:

```text
parameter offset registry
→ RAM M slice
→ RAM V slice
→ existing subgroup32 AdamW GPU segment
→ updated M/V copied back into the same RAM ranges
```

No shadow optimizer offset table is introduced.

## 7. Hot-path disk retirement

In RAM-resident mode, optimizer steps 6 through 13 read M/V from RAM.

Intermediate optimizer steps do not create `adam_m.r6pack` or `adam_v.r6pack`.

The required hot-path accounting is:

```text
perStepMVDiskReadBytes  = 0
perStepMVDiskWriteBytes = 0
optimizerHotPathDiskReadCount  = 0
optimizerHotPathDiskWriteCount = 0
```

Weights remain on the existing hot runtime path and are not moved to HDD as part of each optimizer transaction.

## 8. Run-local state semantics

Intermediate GEN6..GEN12 packed manifests use:

```text
publicationState = RUN_LOCAL_RAM_MV
optimizerStateRuntimeMode = RAM_RESIDENT_MV
optimizerStateDurable = false
runtimePayloadFilesPerGeneration = 1
```

Only the weight payload is physically present in those run-local slots.

These states are logical optimizer commits for the currently running process, but are not fresh-process resume checkpoints.

A fresh process pointed at `RUN_LOCAL_RAM_MV` fails closed and must return to the last durable checkpoint.

## 9. Crash semantics

If the process or machine stops before final writeback, RAM M/V is lost.

Example:

```text
RAM reached GEN10 / OPT10
process terminated before final writeback
```

Durable authority remains the previous GEN5 checkpoint.

Forbidden recovery:

- zero moments;
- receipt-to-M/V synthesis;
- optimizer-state reconstruction from weights;
- partial run-local state adoption;
- silent disk fallback.

## 10. Final writeback boundary

Only the final N8 optimizer commit performs M/V disk writeback.

For N8:

```text
GEN13 / OPT13 / CURSOR83
```

must be fully computed before final writeback is admitted.

At that final boundary:

```text
weights.r6pack
adam_m.r6pack
adam_v.r6pack
cursor
scheduler
active training state
```

become a complete resumable tuple again.

The final packed manifest returns to the durable packed publication state and records `optimizerStateOrigin = RAM_RESIDENT_ADAM_MV_FINAL_WRITEBACK`.

## 11. Existing Storage Root Authority

This patch does not introduce another storage root.

It reuses:

```text
--basetrain-storage-root <PATH>
--storage-publication-policy checkpoint
```

The recommended deployment remains:

```text
D: hot runtime / source / build
RAM: active Adam M/V
E:\ASH: durable checkpoint and receipts
```

No `E:\ASH` literal is hard-coded in core Rust.

## 12. Durable publication order

The N8 sequence becomes:

```text
GEN13 compute closure
→ final M/V writeback to final hot packed state
→ N8 structural receipt closure
→ Storage Root copy/hash verification
→ durable checkpoint publication
→ RAM-M/V durable receipt
→ RAM-M/V PASS
→ N8 PASS
→ Resume-Cut HOLD
```

N8 PASS must not be printed before durable checkpoint publication completes.

## 13. Existing R6A packed-disk contract

The original R6A disk-backed optimizer mode remains unchanged when RAM admission is absent.

In RAM mode, the old R6A disk optimizer-state PASS is not emitted as if its three-files-per-generation contract still applied.

RAM mode explicitly supersedes the disk optimizer-state authority while preserving packed weights and the downstream native/micro-atlas/subgroup32 execution chain.

The RAM-mode packed sync geometry for N8 is:

```text
8 weight pack syncs
+ final Adam-M sync
+ final Adam-V sync
= 10 packed payload syncs
```

rather than the legacy `8 × 3` optimizer-state persistence pattern.

## 14. Performance accounting

The patch records:

```text
optimizerHydrationCount
adamMResidentBytes
adamVResidentBytes
physicalRamAvailableAtAdmission
ramReserveBytes
optimizerStepsExecuted
optimizerMUploadBytes
optimizerVUploadBytes
optimizerMDownloadBytes
optimizerVDownloadBytes
finalMWritebackBytes
finalVWritebackBytes
```

No speedup factor is claimed without physical measurements.

The hard optimization claim is narrower:

```text
optimizer M/V disk hot-path bytes = 0
```

## 15. Final receipt

Runtime and durable receipt name:

```text
ram_resident_adam_mv_final_writeback_receipt.json
```

Required successful N8 identity:

```text
sourceTrainingGeneration = 5
sourceOptimizerStep = 5
runtimeMode = RAM_RESIDENT_MV
optimizerHydrationCount = 1
optimizerStepsExecuted = 8
perStepMVDiskReadBytes = 0
perStepMVDiskWriteBytes = 0
finalTrainingGeneration = 13
finalOptimizerStep = 13
finalCursorNext = 83
finalMWritebackCount = 1
finalVWritebackCount = 1
durableWeightVerified = 1
durableMVerified = 1
durableVVerified = 1
durableCursorVerified = 1
durableSchedulerVerified = 1
zeroMomentFallbackCount = 0
optimizerStateReconstructionCount = 0
silentDiskFallbackCount = 0
trainingReplayCount = 0
optimizerReplayCount = 0
```

## 16. PASS / HOLD

PASS:

```text
PASS_ASH_BASETRAIN_RAM_RESIDENT_ADAM_MV_FINAL_WRITEBACK_R1
```

Capacity HOLD:

```text
HOLD_ASH_BASETRAIN_RAM_RESIDENT_ADAM_MV_CAPACITY_INSUFFICIENT
```

Standalone readiness HOLD:

```text
HOLD_ASH_BASETRAIN_RAM_RESIDENT_ADAM_MV_READY_N8_NOT_YET_EXECUTED
```

After successful N8 durable publication, the existing next-stage HOLD remains:

```text
HOLD_ASH_BASETRAIN_N8_CONTINUOUS_GEN13_CANDIDATE_READY_RESUME_CUT_EXACT_DETERMINISM_NOT_YET_ADMITTED
```

## 17. Explicit non-goals

R1 does not add pinned host memory, asynchronous double buffering, full optimizer VRAM residency, dirty-page checkpointing, mid-run durable M/V checkpoints, crash recovery beyond last durable checkpoint, resume-cut determinism proof, or canonical GEN13 parent promotion.

Those remain later optimization/admission axes after the physical RAM-resident N8 result is measured.
