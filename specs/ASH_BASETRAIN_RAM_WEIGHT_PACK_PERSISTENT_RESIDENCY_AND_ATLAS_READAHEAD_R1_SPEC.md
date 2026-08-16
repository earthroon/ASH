# `ASH-BASETRAIN-RAM-WEIGHT-PACK-PERSISTENT-RESIDENCY-AND-ATLAS-READAHEAD-R1`

## Immutable Resident Weight Generations / One Initial Physical Source Read / RAM36-Bounded Atlas Feed

## 0. Status

```text
ASH-BASETRAIN-RAM-WEIGHT-PACK-PERSISTENT-RESIDENCY-AND-ATLAS-READAHEAD-R1

Immutable Weight Pack Host Residency /
One Physical Initial Weight-Pack Read Per Training Run /

36GiB Host Process Budget Admission /
Weight-Pack Exact Byte Reservation /
No Unbounded RAM Cache /

Packed Source RAM Authority /
No Per-Optimizer-Step Source Pack Reopen /
No Per-Step HDD Weight Re-Read /

Atlas Segment Indexed RAM View /
Exact Offset Slice Projection /
No Tensor Reconstruction /
No In-Generation Weight Mutation /

Micro-Atlas Sequential Read-Ahead /
Triple-Buffered Host-to-GPU Feed Preservation /
Current Page Compute /
Next Page H2D-Ready Resident Projection /
Next+1 Page Host Projection /

Existing 16MiB Micro-Atlas Preservation /
Existing 3-Slot Ring Preservation /

No Full GPU Weight Residency /
No VRAM Limit Violation /

No Adam M/V Eviction /
No Adam Quantization /
No Training Math Change /
No Optimizer Math Change /

36GiB RAM Hard-Cap Preservation /
PrivateUsage Pre/Post Verification /
Fail Closed If Weight Pack Cannot Be Admitted
```

Receipt schema:

```text
ash.basetrain.ram_weight_pack_persistent_residency_atlas_readahead.v1
```

## 1. Parent authority

This revision is parented by:

```text
ASH-BASETRAIN-RAM-RESIDENT-ADAM-MV-36GIB-PROCESS-BUDGET-AUTHORITY-R1
ASH-BASETRAIN-RAM-BUDGET-EXACT-INVENTORY-R1
R6A-R1 Packed Runtime Native Bootstrap / Accumulation Wave Residency
R6A-R2 Device-Limit-Aware Micro-Atlas / Vocab Row Paging
R6A-R2-R2 Subgroup32 Tiled Segment Gradient AdamW
N8 Long-Horizon Continuity
CF1 Release Profile Authority
```

The existing process hard limit remains exactly:

```text
38,654,705,664 bytes = 36 GiB
```

The process-memory authority remains Windows `PrivateUsage`. Working Set remains telemetry only.

## 2. Physical motivation

The existing production route has already retired microbatch-induced weight refetch:

```text
microbatch_induced_page_refetch_bytes = 0
```

The measured eight-step route nevertheless observed large packed weight traffic, including:

```text
actual_wave_resident_weight_read_bytes = 71,536,082,944
optimizer_source_pack_read_bytes       = 37,332,647,936
```

The optimization target is therefore not training math. It is repeated physical delivery of canonical packed weights from storage to host memory.

## 3. Critical generation semantics

The canonical `weights.r6pack` is not byte-identical for the whole training run. Optimizer commits create a new canonical candidate weight pack at every optimizer step.

Therefore R1 does **not** freeze one initial weight pack across all steps.

The correct SSOT is:

```text
GEN N resident weight pack
= immutable during generation N

optimizer computes candidate GEN N+1
= existing candidate serialization bytes
= durable weights.r6pack bytes
= successor resident bytes

successful durable commit
-> atomically promote GEN N+1 resident authority
-> drop GEN N resident authority
```

`No Weight Mutation` in this revision means:

```text
no mutation of an already-published resident generation
```

It does not mean optimizer updates are disabled.

## 4. Runtime host delivery topology

Initial generation:

```text
Canonical disk weights.r6pack
        |
        | one sequential physical read
        | simultaneous streaming SHA256
        v
ResidentWeightPack GEN N
        |
        +-> exact Atlas slices
        +-> optimizer source reader
```

Following optimizer generations:

```text
resident GEN N
    |
    +-> optimizer source read from RAM
             |
             v
candidate serialized weight bytes
       |                    |
       | durable write      | same bytes appended
       v                    v
weights.r6pack GEN N+1   ResidentWeightPackBuilder
                              |
                              v
                    immutable resident GEN N+1
                              |
                    durable commit succeeds
                              |
                              v
                    resident authority promotion
```

There is no source `weights.r6pack` reread between optimizer steps after initial residency.

## 5. Canonical weight authority

The canonical value authority remains the existing packed-state format and manifest.

Resident memory is a physical delivery authority, not a new model-format authority.

Required identity:

```text
resident byte count = packed manifest weightPackBytes
resident SHA256     = packed manifest weightPackSha256
resident generation = source/candidate training generation
resident step       = source/candidate optimizer step
resident path       = canonical candidate weights.r6pack path identity
```

The initial resident generation is populated from the canonical source file.

Successor resident generations are populated from the exact bytes already being serialized for the canonical candidate pack. They are not reconstructed from tensors and are not reread from disk.

## 6. Resident backing

Canonical implementation form:

```text
Arc<Vec<u8>>
```

The `Vec<u8>` backing is moved directly into the Arc owner.

R1 does not promote `Vec<u8>` through a path that requires a second multi-gigabyte resident backing allocation.

Resident bytes are exposed read-only through the `ResidentWeightPack` API.

No `Arc<Mutex<Vec<u8>>>` or equivalent mutable weight mirror is introduced.

## 7. Initial one-pass physical load

Initial source population performs:

```text
metadata length validation
-> one File::open
-> sequential bounded reads
-> append to resident Vec
-> SHA256 update on the same bytes
-> exact length verification
-> exact digest verification
-> publish resident authority
```

Forbidden:

```text
load file into RAM
-> close
-> reopen
-> second full-file digest scan
```

The read chunk is bounded at:

```text
16 MiB = 16,777,216 bytes
```

This transient chunk is explicitly preflighted against RAM36 and recorded as an exact inventory configured bound.

## 8. Successor one-pass construction

The successor builder reserves exact `weight_pack_bytes` before allocating its backing.

While existing optimizer candidate serialization produces each `weight_bytes` segment, R1 performs both:

```text
candidate disk writer.write(weight_bytes)
resident successor builder.append(weight_bytes)
```

The successor builder updates SHA256 while appending those same bytes.

At finalize, that already-computed digest becomes the resident generation digest. R1 does not perform a second full resident-buffer SHA scan.

## 9. Durable candidate writes remain authoritative

R1 retires **source disk reads**, not durable candidate writes.

Per-step canonical candidate `weights.r6pack` writes remain intact because they are part of the existing durable training-state transaction.

Therefore disk activity may still be visible during candidate publication.

This revision must not claim:

```text
all training disk I/O = 0
```

It claims:

```text
post-initial weight-source open/read/seek = 0
optimizer source weight disk read bytes   = 0
```

Candidate writes, checkpoint publication, receipts, final Adam writeback, and storage-root publication remain separate I/O authorities.

## 10. RAM36 reservation authority

New managed owner:

```text
HostRamOwner::ResidentWeightPack
```

Before initial population:

```text
current PrivateUsage
+ outstanding reservations
+ exact resident weight bytes
<= 38,654,705,664
```

The 16 MiB initial load scratch is also separately preflighted.

Post materialization:

```text
PrivateUsage <= 38,654,705,664
```

is verified again.

If the resident pack cannot be admitted, R1 fails closed. It does not fall back to repeated disk reads.

## 11. Old + successor overlap

During each optimizer candidate build, old and successor resident generations coexist temporarily.

This is intentional and must be accounted exactly.

RAM36 sequence:

```text
old resident already materialized
-> reserve exact successor bytes
-> materialize successor bytes
-> PrivateUsage post-check with both generations alive
-> durable candidate commit
-> publish successor resident authority
-> drop old resident
-> release old reservation
-> PrivateUsage post-promotion observation
```

No old resident is dropped early merely to create room for the successor.

If old + successor cannot fit under 36 GiB, the revision fails closed.

## 12. Exact inventory ownership

Existing exact inventory is extended with:

```text
ResidentWeightPack
ResidentWeightPackLoadScratch
ResidentWeightPackSuccessorTransient
```

`ResidentWeightPack` is run-resident while active.

`ResidentWeightPackLoadScratch` is a bounded initial-load transient.

`ResidentWeightPackSuccessorTransient` is active only while the old and next generations coexist before durable promotion.

There is no RAM36-only shadow owner invisible to the exact inventory.

## 13. Atlas resident slice authority

Checkpoint/Atlas range reads can bind a resident source session.

In resident mode:

```text
requested canonical path
-> resident generation identity validation
-> checked offset/end projection
-> exact &[u8] resident slice
```

No file handle exists in the resident session.

Resident range reads preserve existing logical read counters where required for older receipt semantics, while newly added physical source counters remain zero.

Out-of-bounds projections fail closed.

## 14. Optimizer source authority

The optimizer packed F32 reader can use either:

```text
legacy File source
or
resident Arc<Vec<u8>> source
```

Persistent-residency admission requires the resident source path.

The resident source identity must match current generation, optimizer step, path, exact byte count, and digest before optimizer evaluation.

In the admitted route:

```text
optimizer_source_weight_read_bytes on disk = 0
```

Logical optimizer resident read bytes are recorded separately.

## 15. No hidden disk fallback

Once resident authority is admitted and published, a missing resident slice, identity drift, or resident generation mismatch is an error.

R1 must not silently reopen the source pack from disk.

Terminal admitted-route invariants:

```text
post_residency_source_file_open_count = 0
post_residency_source_read_bytes      = 0
post_residency_source_seek_count      = 0
optimizer_disk_weight_read_bytes      = 0
```

## 16. Micro-Atlas geometry preservation

Existing geometry remains:

```text
micro atlas page = 16 MiB
GPU ring slots   = 3
```

No full model weight pack is uploaded to GPU memory.

Existing device buffer and storage binding limits remain authoritative.

## 17. Bounded read-ahead semantics

R1 permits only two future resident projections beyond the active request:

```text
current request
next resident projection
next+1 resident projection
```

The next and next+1 views are bounded to 16 MiB pages and are produced by checked slices of the existing resident backing.

No future-page `Vec<u8>` cache is created.

No unbounded prefetch depth is permitted.

## 18. H2D preparation boundary

The read-ahead receipt explicitly describes the preparation mode as:

```text
EXISTING_3_SLOT_RING_H2D_READY_RESIDENT_PROJECTION
```

Meaning:

```text
current page      = normal existing compute/upload authority
next page         = resident bytes projected and H2D-ready for the existing ring
next+1 page       = resident bytes projected as bounded future host view
```

R1 preserves the existing three-slot GPU upload ring. It does not introduce a second GPU device, full-weight VRAM residency, or an unbounded staging pool.

Critically, R1 does **not** claim measured transfer/compute overlap unless a later physical timing authority proves it:

```text
measuredTransferComputeOverlapClaimed = false
```

This prevents a host read-ahead receipt from being mislabeled as measured asynchronous GPU overlap.

## 19. No tensor reconstruction

Forbidden resident-cache forms include:

```text
full Vec<f32> model reconstruction
full decoded tensor cache
full layer tensor shadow authority
full vocab GPU materialization
```

Resident memory stores the canonical packed bytes.

Tensor/segment decoding remains bounded by the existing compute route.

## 20. Generation promotion authority

Resident generation promotion occurs only **after** existing `commit_active_state` succeeds.

Forbidden:

```text
candidate resident publication
-> later durable commit attempt
```

Required:

```text
candidate built and verified
-> durable active-state commit succeeds
-> resident successor identity verified
-> resident authority replaced
-> old resident dropped
```

A failed durable commit cannot advance resident authority.

## 21. Final resident lifetime

The final resident generation remains available through final writeback and receipt construction.

Before RAM36 finalization:

```text
resident receipt written
-> final resident dropped
-> exact inventory resident owner released
-> RAM36 resident reservation released
-> PrivateUsage observed
-> RAM36 final receipt finalized
```

This prevents reservation leaks at process-budget closure.

## 22. CLI admission

New explicit flag:

```text
--admit-ram-weight-pack-persistent-residency
```

It requires existing production authorities, including:

```text
--admit-ram36-process-budget-authority
--admit-ram-budget-exact-inventory
--admit-ram-resident-adam-mv
--admit-r6a-r1-native-bootstrap-wave-residency
--admit-r6a-r2-device-limit-micro-atlas-vocab-paging
```

The process-level flag is forcibly disabled inside nested per-step configs. A nested step cannot create a second resident/cache authority.

## 23. Release CF1 authority

The route remains bound to the exact Release binary sealed by CF1.

Production execution authority remains:

```text
CF1 Release compile chain
-> exact target/release/base_train.exe SHA seal
-> launch exact sealed release executable
```

A Debug binary is not production performance or RAM authority.

## 24. New receipt

Output:

```text
basetrain_ram_weight_pack_residency_receipt.json
```

Required fields include:

```text
initialGeneration
finalGeneration
initialOptimizerStep
finalOptimizerStep
residentWeightPackBytes
initialSourceFileOpenCount
initialSourceReadBytes
initialSourceSeekCount
initialDigestVerified
postResidencySourceFileOpenCount
postResidencySourceReadBytes
postResidencySourceSeekCount
optimizerResidentWeightReadBytes
optimizerDiskWeightReadBytes
residentGenerationPromotionCount
successorMaterializationCount
logicalAtlasReadSessionCount
residentAtlasProjectionCount
residentAtlasProjectionBytes
residentAtlasReadaheadProjectionCount
residentAtlasReadaheadProjectionBytes
microAtlasPageBytes
microAtlasRingSlotCount
h2dPreparationMode
measuredTransferComputeOverlapClaimed
fullGpuWeightResidency
trainingMathChangeCount
optimizerMathChangeCount
```

## 25. Required physical truth

For an eight-step N8 run admitted by this revision:

```text
initial source file open count = 1
initial source seek count      = 0
initial source read bytes      = exact initial weight pack bytes
initial digest verified        = true

post-residency source opens    = 0
post-residency source reads    = 0
post-residency source seeks    = 0
optimizer disk weight reads    = 0

resident promotion count       = 8
successor materialization      = 8

micro atlas page               = 16 MiB
ring slots                     = 3
full GPU weight residency      = 0

RAM36 violations               = 0
training math changes          = 0
optimizer math changes         = 0
```

The exact wall-time is measured evidence, not a correctness gate.

## 26. Pass tokens

```text
PASS_ASH_BASETRAIN_RAM_WEIGHT_PACK_PERSISTENT_RESIDENCY_AND_ATLAS_READAHEAD_R1_STATIC
PASS_ASH_BASETRAIN_RAM_WEIGHT_PACK_PERSISTENT_RESIDENCY_R1
PASS_ASH_BASETRAIN_ATLAS_TRIPLE_BUFFERED_READAHEAD_R1
PASS_ASH_BASETRAIN_RAM_WEIGHT_PACK_PERSISTENT_RESIDENCY_AND_ATLAS_READAHEAD_R1
```

## 27. Representative failures

```text
FAIL_ASH_BASETRAIN_WEIGHT_PACK_RAM36_ADMISSION_REJECTED
FAIL_ASH_BASETRAIN_WEIGHT_PACK_SOURCE_IDENTITY_MISMATCH
FAIL_ASH_BASETRAIN_WEIGHT_PACK_SOURCE_SHORT_READ
FAIL_ASH_BASETRAIN_WEIGHT_PACK_RESIDENT_DIGEST_MISMATCH
FAIL_ASH_BASETRAIN_WEIGHT_PACK_RESIDENT_PRIVATE_USAGE_OVER_LIMIT
FAIL_ASH_BASETRAIN_WEIGHT_PACK_RESIDENT_SLICE_OUT_OF_BOUNDS
FAIL_ASH_BASETRAIN_WEIGHT_PACK_POST_RESIDENCY_DISK_READ
FAIL_ASH_BASETRAIN_WEIGHT_PACK_POST_RESIDENCY_SOURCE_REOPEN
```

No failure may trigger silent disk fallback, Adam eviction, batch shrink, precision downgrade, or cap relaxation.

## 28. Static validation

New validator:

```text
tools/validate_ram_weight_pack_persistent_residency_atlas_readahead_r1_static.py
```

It is included in the existing CF1 validator chain.

It verifies at minimum:

```text
module/export/CLI binding
RAM36 dependency
exact inventory owners
exact 36GiB reuse
16MiB / 3-slot geometry reuse
Arc<Vec<u8>> resident backing
one-pass initial load + streaming digest
16MiB load scratch preflight
candidate same-byte successor construction
no second successor full digest scan
no persistent source full scan before load
resident range session with physical disk counters zero
bounded current/next/next+1 resident projection
explicit H2D-ready preparation semantics
no fake measured overlap claim
optimizer resident source reader
exact successor RAM36 reservation
old+successor inventory overlap
post-materialization PrivateUsage verification
promotion after durable commit
old resident drop before reservation release
zero optimizer disk weight reads
zero post-residency physical source I/O
final resident release before RAM36 finalization
no full GPU residency
no Adam quantization
no training math change
no optimizer math change
```

## 29. Non-goals

R1 does not implement:

```text
full GPU weight residency
new GPU device
weight quantization
Adam quantization
Adam eviction
checkpoint semantic rewrite
optimizer semantic rewrite
training math rewrite
batch geometry change
dataset streaming rewrite
persistent cross-run RAM cache
mmap-as-residency substitution
unbounded read-ahead
unbounded staging pool
measured transfer/compute overlap claim
candidate durable-weight-write retirement
```

Candidate durable-write optimization, if required by later physical evidence, is a separate revision.

## 30. Final SSOT

```text
CANONICAL WEIGHT VALUES
= EXISTING PACKED STATE

INITIAL PHYSICAL SOURCE READ
= ONE SEQUENTIAL PASS

INITIAL DIGEST
= SAME PHYSICAL READ PASS

CURRENT HOST WEIGHT DELIVERY
= IMMUTABLE RESIDENT GENERATION

OPTIMIZER SOURCE AFTER INITIAL RESIDENCY
= RESIDENT MEMORY

SUCCESSOR RESIDENT SOURCE
= SAME BYTES ALREADY SERIALIZED FOR CANDIDATE PACK

SUCCESSOR SECOND FULL SHA SCAN
= FORBIDDEN

GENERATION PROMOTION
= ONLY AFTER DURABLE COMMIT

POST-RESIDENCY WEIGHT-SOURCE DISK READ
= ZERO

DURABLE CANDIDATE WEIGHT WRITE
= PRESERVED

ATLAS ACCESS
= CHECKED RESIDENT OFFSET SLICE

READ-AHEAD
= CURRENT + NEXT + NEXT+1, BOUNDED

H2D PREPARATION
= EXISTING 3-SLOT RING H2D-READY RESIDENT PROJECTION

MEASURED GPU OVERLAP CLAIM
= FALSE UNTIL PHYSICALLY PROVEN

MICRO ATLAS
= 16 MiB

GPU RING
= 3 SLOTS

FULL GPU WEIGHT RESIDENCY
= FORBIDDEN

RAM HARD LIMIT
= 38,654,705,664 BYTES

OLD + SUCCESSOR PEAK
= EXACTLY ACCOUNTED AND FAIL-CLOSED

ADAM EVICTION
= FORBIDDEN

ADAM QUANTIZATION
= FORBIDDEN

TRAINING MATH CHANGE
= 0

OPTIMIZER MATH CHANGE
= 0
```