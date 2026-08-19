# ASH-BASETRAIN-N8-DEFERRED-DURABLE-WRITEBACK-R1

## 1. Patch identity

```text
ASH-BASETRAIN-N8-DEFERRED-DURABLE-WRITEBACK-R1

Eight-Step Resident Transaction /
Intermediate Packed Payload Write Zero /
Resident Weight Successor Authority /
RAM Adam M·V Continuity /
Final-Step Triple-Pack Materialization /
Resident Checkpoint Source Authority /
Final Packed Sync Cardinality /
Single Durable Checkpoint Publication /
Single Archive Publication Seal
```

Parent build revision:

```text
n8-deferred-durable-writeback-r1
```

Resident-checkpoint closure:

```text
ASH-BASETRAIN-N8-DEFERRED-DURABLE-WRITEBACK-R1-
RESIDENT-CHECKPOINT-SOURCE-AUTHORITY-CLOSURE

revision=n8-deferred-resident-checkpoint-source-authority-r1
```

Final packed-sync closure:

```text
ASH-BASETRAIN-N8-DEFERRED-DURABLE-WRITEBACK-R1-
FINAL-PACKED-SYNC-CARDINALITY-CLOSURE

revision=n8-deferred-final-packed-sync-cardinality-r1
```

## 2. Purpose

N8 long-horizon training executes eight optimizer steps. R1 moves packed-state
durability out of the intermediate optimizer-step critical path.

Steps 1-7 advance through verified resident weights and RAM-resident Adam M/V state
without writing large packed training payloads. Step 8 materializes the final
`weights.r6pack`, `adam_m.r6pack`, and `adam_v.r6pack`, then the existing durable
checkpoint and archive publication run once.

Two physical closures complete the route:

1. Resident Checkpoint Source Authority allows an intermediate logical checkpoint to be
   backed by verified resident bytes without requiring an intermediate physical
   `weights.r6pack`.
2. Final Packed Sync Cardinality makes the final durability ledger count actual packed
   writer finalizations rather than assuming one weight sync per optimizer step.

Neither closure changes forward, backward, gradient, optimizer, scheduler, TensorCube,
subgroup, Atlas geometry, checkpoint serialization, or archive format semantics.

## 3. Explicit admission

The route is explicit:

```text
--admit-n8-deferred-durable-writeback
```

It requires:

```text
--admit-production-multistep-loop
--admit-n8-long-horizon-continuity
--production-loop-optimizer-steps 8
--admit-ram-resident-adam-mv
--admit-ram-weight-pack-persistent-residency
--storage-publication-policy checkpoint
```

The persistent weight route retains the pre-existing RAM36 and exact-inventory parent
requirements. No parent gate is weakened.

Admission remains fail-closed:

```text
N8DeferredWritebackN8AdmissionMissing
N8DeferredWritebackStepWindowMismatch
N8DeferredWritebackRamAdamMvAuthorityMissing
N8DeferredWritebackResidentWeightAuthorityMissing
N8DeferredWritebackCheckpointPublicationRequired
```

When deferred admission is absent, legacy persistence behavior remains authoritative.

## 4. Eight-step resident transaction

For source generation `G`:

```text
G
 -> step 1 resident successor G+1
 -> step 2 resident successor G+2
 -> ...
 -> step 7 resident successor G+7
 -> step 8 resident successor G+8
 -> final triple-pack materialization
 -> packed durability sync seal
 -> durable checkpoint publication
 -> archive publication
```

For the current generation-5 reproducer:

```text
5 -> 6 -> 7 -> 8 -> 9 -> 10 -> 11 -> 12 -> 13
```

Intermediate generations are resident commits and are intentionally non-durable.
Restart authority remains the last durable checkpoint.

## 5. Intermediate packed payload write zero

In deferred mode, steps 1-7 must not create or write large packed training payloads:

```text
weights.r6pack = 0 bytes written
adam_m.r6pack  = 0 bytes written
adam_v.r6pack  = 0 bytes written
runtime payload file count = 0
```

Weight materialization is gated by:

```text
write_weight_payload = !deferred_durable_writeback || final_writeback
```

Adam M/V writers remain final-writeback-only.

The candidate stream still computes complete SHA-256 and byte-length identity even when
the disk writer is absent.

Hard failure:

```text
N8DeferredWritebackIntermediatePackedPayloadWriteDetected
```

Small control and diagnostic writes are outside the packed training payload count.

## 6. Resident weight successor authority

Candidate weight bytes flow to the resident successor on every step and to the physical
weight writer only at the final boundary:

```text
GPU/optimizer candidate bytes
        -> ResidentWeightPackBuilder     steps 1-8
        -> weights.r6pack writer         step 8 only
```

Resident successor identity preserves:

```text
generation
optimizer step
logical source path
byte length
SHA-256
```

No intermediate disk weight file may become a hidden continuation authority.

## 7. Resident Atlas plan source

Deferred continuation uses:

```text
materialize_production_atlas_plan_for_resident_packed_runtime
```

The legacy materializer retains the physical-file requirement.

Before resident plan materialization:

```text
resident generation == SourceState generation
resident optimizer step == SourceState optimizer step
resident source path == logical packed-weight source path
resident byte length == manifest weight byte length
resident SHA-256 == manifest weight SHA-256
```

Failure:

```text
N8DeferredWritebackResidentPlanSourceIdentityDrift
```

Only backing authority changes. Atlas geometry and parameter layout remain unchanged.

## 8. Source-generation SSOT compatibility

R1 composes with:

```text
ASH-BASETRAIN-N8-SOURCE-WEIGHT-GENERATION-SSOT-R1
```

`SourceState.generation` remains semantic authority. Resident RAM/VRAM objects are
carriers and parity witnesses, not generation creators.

No synthetic generation-zero fallback is permitted.

## 9. RAM Adam M/V continuity

Steps 1-7:

```text
Adam M physical pack write = 0
Adam V physical pack write = 0
```

Step 8:

```text
Adam M final pack write = 1
Adam V final pack write = 1
```

Existing RAM exact-inventory, RAM36 process budget, generation, final writeback, and
resume-cut contracts remain authoritative.

## 10. Final-step triple-pack materialization

Only step 8 is a packed-payload durability boundary.

Required files:

```text
weights.r6pack
adam_m.r6pack
adam_v.r6pack
```

Required physical state:

```text
weight payload bytes > 0
Adam M payload bytes > 0
Adam V payload bytes > 0
runtime payload file count = 3
```

Failures:

```text
N8DeferredWritebackFinalTriplePackIncomplete
N8DeferredWritebackFinalWeightDigestDrift
```

## 11. Durable checkpoint and archive publication

Publication remains after the eight-step loop and after packed sync validation.

Required counts:

```text
durable checkpoint publication count = 1
archive/durable receipt publication count = 1
```

Failures:

```text
N8DeferredWritebackMultipleDurablePublication
N8DeferredWritebackMultipleArchivePublication
```

Canonical order:

```text
final resident successor
 -> final triple-pack materialization
 -> packed writer sync cardinality validation
 -> final training-state commit
 -> N8 finalization
 -> durable checkpoint publication
 -> archive publication
```

Publication must not bypass a packed-sync mismatch.

## 12. Resident Checkpoint Source Authority Closure

### 12.1 Physical failure that motivated the closure

The earlier physical reproducer reached:

```text
[N8-DEFERRED][STEP]
step=1/8
source_generation=5
target_generation=6
weight_source=resident
adam_source=ram_resident
weight_payload_write_bytes=0
adam_m_payload_write_bytes=0
adam_v_payload_write_bytes=0
final_materialization=0
```

then failed with:

```text
BTR27R1JR6APackedSourceMissing:<slot_b/weights.r6pack>
```

The failure was a legacy physical-file assumption in the next-step checkpoint consumer.

### 12.2 Logical identity versus physical backing

Within deferred intermediate generations:

```text
checkpoint logical identity
    = path + generation + byte length + SHA-256

checkpoint physical backing
    = verified ResidentWeightPack / active resident range-read session
```

A valid intermediate state is:

```text
logical checkpoint path present
physical weights.r6pack absent
resident source present
path match = 1
digest match = 1
byte length match = 1
generation match = 1
disk fallback = 0
```

### 12.3 Active resident range-read authority

The active resident range-read session binds:

```text
logical path
generation
byte length
SHA-256
resident bytes
```

Checkpoint preflight validates this authority before considering the legacy disk gate.

### 12.4 Fail-closed parity

Hard failures:

```text
N8DeferredResidentCheckpointAuthorityMissing
N8DeferredResidentCheckpointPathDrift
N8DeferredResidentCheckpointDigestDrift
N8DeferredResidentCheckpointSizeDrift
N8DeferredResidentCheckpointGenerationDrift
N8DeferredResidentCheckpointUnexpectedDiskFallback
```

No mismatch is silently repaired and no placeholder/spill pack is created.

### 12.5 Physical closure evidence

The follow-up physical run proved resident-only continuation through all intermediate
generations:

```text
generation 6  authority=resident physical_file_present=0 disk_fallback=0
generation 7  authority=resident physical_file_present=0 disk_fallback=0
generation 8  authority=resident physical_file_present=0 disk_fallback=0
generation 9  authority=resident physical_file_present=0 disk_fallback=0
generation 10 authority=resident physical_file_present=0 disk_fallback=0
generation 11 authority=resident physical_file_present=0 disk_fallback=0
generation 12 authority=resident physical_file_present=0 disk_fallback=0
```

Each observation also reported path, digest, byte-length, and generation parity equal to
1. Steps 1-7 each reported zero weight/M/V payload write bytes.

Therefore the Resident Checkpoint Source Authority Closure is physically established for
step-2 through step-8 continuation.

## 13. Final Packed Sync Cardinality Closure

### 13.1 Physical failure that motivated the closure

After resident continuation was repaired, the same physical N8 run reached step 8:

```text
[N8-DEFERRED][STEP]
step=8/8
source_generation=12
target_generation=13
weight_source=resident
adam_source=ram_resident
weight_payload_write_bytes=4666580992
adam_m_payload_write_bytes=4666580992
adam_v_payload_write_bytes=4666580992
final_materialization=1
```

The triple pack physically materialized, then the route failed with:

```text
R6APackedPayloadSyncCountMismatch
```

This proves the remaining failure is the aggregate durability ledger rather than
resident continuation or final payload materialization.

### 13.2 Sync ownership SSOT

```text
packed_payload_sync_count
=
actual durable packed writer finalization/sync count
```

It is not optimizer-step count and is not generation count.

Expected count and observed count are separate:

```text
expected = route-specific durability contract
observed = physical SequentialPackWriter finalize receipts
```

The aggregate `R6ADiskStepReceipt.packed_payload_sync_count` must also equal the sum of
the writer observations. Any drift is a hard failure:

```text
R6APackedPayloadSyncObservationDrift
```

### 13.3 Route-specific cardinality matrix

Canonical route matrix:

| Route | Weight sync | Adam M sync | Adam V sync | Total |
|---|---:|---:|---:|---:|
| Legacy disk | N | N | N | 3N |
| RAM Adam, non-deferred | N | 1 | 1 | N+2 |
| N8 Deferred | 1 | 1 | 1 | 3 |

For eight optimizer steps:

```text
legacy disk = 24
legacy RAM Adam = 10
N8 deferred = 3
```

The Deferred branch uses the canonical final runtime payload cardinality rather than a
naked magic number:

```text
R6A_RUNTIME_PAYLOAD_FILES_PER_GENERATION = 3
```

### 13.4 Expected cardinality resolver

Canonical resolution:

```text
(deferred=true,  ram_adam=true)  -> 3
(deferred=false, ram_adam=true)  -> N+2
(deferred=false, ram_adam=false) -> 3N
(deferred=true,  ram_adam=false) -> hard fail
```

Invalid deferred-without-RAM remains:

```text
N8DeferredWritebackRamAdamMvAuthorityMissing
```

### 13.5 Intermediate sync zero

Steps 1-7 must produce:

```text
weight sync = 0
Adam M sync = 0
Adam V sync = 0
packed sync delta = 0
```

Hard failure:

```text
N8DeferredWritebackIntermediatePackedPayloadSyncDetected
```

Control JSON/fsync operations do not belong to the packed payload sync counter.

### 13.6 Final writer ownership

Step 8 must produce exactly:

```text
weight sync = 1
Adam M sync = 1
Adam V sync = 1
```

Hard failure:

```text
N8DeferredWritebackFinalPackedSyncOwnershipMismatch
```

The final observed total must therefore be exactly 3.

### 13.7 Existing mismatch guard preserved

The existing failure token remains authoritative:

```text
R6APackedPayloadSyncCountMismatch
```

Its corrected meaning is:

```text
observed physical packed writer sync count
!=
route-specific expected packed writer sync count
```

The closure does not disable or wildcard the guard.

### 13.8 No synthetic count repair

Forbidden:

```text
hard-code observed count to 3
increment aggregate count without writer receipt
count optimizer commits as payload syncs
count directory/control syncs as packed payload syncs
silently accept 2 or 4 final writer syncs
```

Observed cardinality originates from the weight/M/V writer finalize results.

### 13.9 Runtime diagnostic

Deferred mode emits:

```text
[N8-DEFERRED][PACKED-SYNC]
mode=final_only
optimizer_steps=8
intermediate_sync_count=0
weight_sync_count=1
adam_m_sync_count=1
adam_v_sync_count=1
expected_sync_count=3
observed_sync_count=3
match=1
```

On a mismatch `match=0` is diagnostic only; the existing hard gate still aborts.

## 14. Deferred receipt sync evidence

`n8_deferred_durable_writeback_receipt.json` additionally seals:

```text
packedPayloadSyncMode = n8_deferred_final_only
intermediatePackedPayloadSyncCount = 0
finalWeightSyncCount = 1
finalAdamMSyncCount = 1
finalAdamVSyncCount = 1
expectedPackedPayloadSyncCount = 3
observedPackedPayloadSyncCount = 3
packedPayloadSyncCardinalityMatch = true
```

The receipt still seals:

```text
intermediate packed payload writes = 0
final weight write count = 1
final Adam M write count = 1
final Adam V write count = 1
durable checkpoint publication count = 1
archive publication count = 1
synthetic disk fallback count = 0
training math change count = 0
optimizer math change count = 0
gradient math change count = 0
```

## 15. Static validator and CF1 integration

Canonical validator remains:

```text
tools/validate_ash_basetrain_n8_deferred_durable_writeback_r1_static.py
```

It remains registered in:

```text
tools/run_r27r1j_r6a_r2_r2_cf1_compile_chain.ps1
```

The validator now seals both closures and additionally verifies:

```text
writer sync observation ledger exists
observed aggregate cross-check exists
legacy disk 3N formula preserved
legacy RAM N+2 formula preserved
deferred final-only 3 formula exists
invalid deferred/RAM combination fails closed
intermediate sync zero gate exists
final weight/M/V sync ownership exactly one each
existing R6APackedPayloadSyncCountMismatch preserved
negative 2-sync and 4-sync fixtures rejected
```

The RAM-resident Adam validator separately preserves both non-deferred RAM and deferred
sync contracts.

## 16. Implementation surface

Parent and previous closure implementation surface remains authoritative.

Final Packed Sync Cardinality Closure modifies only:

```text
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
tools/validate_ash_basetrain_n8_deferred_durable_writeback_r1_static.py
tools/validate_ram_resident_adam_mv_final_writeback_static.py
```

No checkpoint schema, model tensor, optimizer kernel, shader, or archive implementation
file is changed by this closure.

Baked overlays exclude generated artifacts, manifests, `.sha256` sidecars, and Python
cache output.

## 17. Bake-time structural evidence

Observed in the reconstructed cumulative source tree:

```text
Deferred durable writeback + resident + sync closures:       118/118 PASS
RAM resident Adam M/V final writeback:                         73/73 PASS
N8 source-weight generation SSOT:                              28/28 PASS
Persistent TensorCube resource validator:                      68/68 PASS
N8 long-horizon continuity:                                    70/70 PASS
RAM weight-pack persistent residency / Atlas readahead:        67/67 PASS
VRAM hot-weight-page residency:                                70/70 PASS
GPU successor weight commit continuity:                        52/52 PASS
Storage-root authority:                                        39/39 PASS
RAM36 process-budget authority:                                63/63 PASS
N8 RAM-resident resume-cut determinism:                        118/118 PASS
RAM Adam M/V PCIe transfer overlap:                             76/76 PASS
```

The RAM exact-inventory validator also exits successfully.

The reduced bake tree lacks some `specs/cli/...` fixtures required by older full R6A
validators, and the bake container has no Rust toolchain. Therefore Release CF1 on the
authoritative local checkout remains the compilation and complete static-chain promotion
gate.

## 18. Promotion tokens

Parent static tokens remain:

```text
PASS_ASH_BASETRAIN_N8_DEFERRED_DURABLE_WRITEBACK_STRUCTURAL_R1
PASS_ASH_BASETRAIN_N8_EIGHT_STEP_RESIDENT_TRANSACTION_R1
PASS_ASH_BASETRAIN_N8_INTERMEDIATE_PACKED_PAYLOAD_WRITE_ZERO_R1
PASS_ASH_BASETRAIN_N8_FINAL_TRIPLE_PACK_MATERIALIZATION_R1
PASS_ASH_BASETRAIN_N8_SINGLE_DURABLE_CHECKPOINT_PUBLICATION_R1
PASS_ASH_BASETRAIN_N8_SINGLE_ARCHIVE_PUBLICATION_R1
```

Resident closure static tokens:

```text
PASS_ASH_BASETRAIN_N8_DEFERRED_RESIDENT_CHECKPOINT_SOURCE_AUTHORITY_STRUCTURAL_R1
PASS_ASH_BASETRAIN_N8_DEFERRED_RESIDENT_CHECKPOINT_IDENTITY_PARITY_R1
PASS_ASH_BASETRAIN_N8_DEFERRED_STEP2_RESIDENT_CONTINUATION_R1
```

Final sync closure static token:

```text
PASS_ASH_BASETRAIN_N8_DEFERRED_FINAL_PACKED_SYNC_CARDINALITY_STRUCTURAL_R1
```

Final sync closure physical token:

```text
PASS_ASH_BASETRAIN_N8_DEFERRED_FINAL_PACKED_SYNC_CARDINALITY_PHYSICAL_R1
```

Resident closure physical token:

```text
PASS_ASH_BASETRAIN_N8_DEFERRED_RESIDENT_CHECKPOINT_SOURCE_PHYSICAL_R1
```

Parent final tokens remain:

```text
PASS_ASH_BASETRAIN_N8_DEFERRED_DURABLE_WRITEBACK_PHYSICAL_R1
PROMOTE_ASH_BASETRAIN_N8_DEFERRED_DURABLE_WRITEBACK_R1
```

Static evidence alone does not satisfy physical/final promotion.

## 19. Physical acceptance

The next physical N8 run must preserve the already-observed resident behavior:

```text
steps 1-7 packed payload write bytes = 0
steps 1-7 packed payload sync count = 0
checkpoint authority = resident
physical intermediate weights.r6pack may be absent
disk fallback = 0
```

Step 8 must show:

```text
weight payload bytes > 0
Adam M payload bytes > 0
Adam V payload bytes > 0
final materialization = 1

[N8-DEFERRED][PACKED-SYNC]
intermediate_sync_count=0
weight_sync_count=1
adam_m_sync_count=1
adam_v_sync_count=1
expected_sync_count=3
observed_sync_count=3
match=1
```

The former:

```text
R6APackedPayloadSyncCountMismatch
```

must not recur for the valid 1+1+1 writer result.

After the sync seal, execution must progress to:

```text
final training-state commit
durable checkpoint publication count = 1
archive publication count = 1
```

Only then may the parent physical and promotion tokens be emitted.

## 20. No semantic-change boundary

R1 and both closures do not change:

- forward or backward equations,
- loss or gradient values,
- gradient accumulation count,
- AdamW or Muon equations,
- scheduler profile or learning-rate policy,
- dataset/token ordering,
- generation increment policy,
- TensorCube topology,
- exact subgroup32 execution,
- R14 owner-pin semantics,
- Stage11 merge semantics,
- Atlas geometry or parameter ordering,
- packed checkpoint serialization format,
- archive format.

The Final Packed Sync Cardinality Closure changes only:

```text
route-specific expected packed durability sync cardinality
physical writer-sync observation accounting
aggregate receipt validation and diagnostics
```

## 21. Final SSOT statement

```text
During an admitted N8 eight-step resident transaction, SourceState generations advance
through verified resident weights and RAM Adam M/V state.

Optimizer steps 1-7 write zero packed training payload bytes and perform zero packed
payload durability syncs.

An intermediate checkpoint path is a logical identity, not an unconditional filesystem
authority. A verified ResidentWeightPack and active resident range-read session may back
that identity when path, generation, byte length, and SHA-256 match exactly. Resident
mismatch fails closed and never silently falls back to disk.

Packed payload sync cardinality follows actual durable writer ownership, not optimizer
step count. Legacy disk mode remains 3N; non-deferred RAM Adam remains N+2; N8 deferred
mode performs exactly three final packed syncs: weights, Adam M, and Adam V.

Expected sync cardinality is route-specific. Observed sync cardinality comes from physical
writer-finalization receipts. A mismatch remains a hard failure.

Only step 8 materializes and syncs weights.r6pack, adam_m.r6pack, and adam_v.r6pack.
After the sync seal passes, the final durable checkpoint is published once and the
archive is published once.
```
