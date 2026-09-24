# TENSORCUBE-TABLE-R4A
# MULTI-CHUNK PARALLEL HIMUON CONSUMPTION

## 0. Revision

```text
Patch ID:
TENSORCUBE-TABLE-R4A

Canonical name:
ASH-BASETRAIN-TENSORCUBE-TABLE-R4A-MULTI-CHUNK-PARALLEL-HIMUON-CONSUMPTION

Class:
GPU RESIDENCY / SCHEDULING ARCHITECTURE
NO NUMERICAL CHANGE
NO OPTIMIZER MATH CHANGE
NO DURABILITY SEMANTIC CHANGE
```

Direct parent:

```text
TENSORCUBE-TABLE-R3-CF1
PRODUCTION CALLSITE ADOPTION
```

Semantic parents:

```text
TENSORCUBE-TABLE-R1
TENSORCUBE-TABLE-R2A
TENSORCUBE-TABLE-R3
UNIFIED-ATLAS-MCU R6
P4 EXACT LEASE
P5 ACTIVEASYNC
```

## 1. Target law

```text
CHUNK = RESIDENCY PARTITION ONLY
TENSORCUBE ROW = EXECUTION SSOT
WAVE = TRANSACTION / RESIDENCY FENCE
HIMUON = MULTI-CHUNK DEVICE CONSUMER
```

Chunk identity must never replace canonical `(parameter_index, tensorcube_ordinal)` execution identity.

## 2. Multi-chunk admission

One admitted parameter/wave domain may hold more than one chunk concurrently. Every admitted chunk binds:

```text
chunk_id
wave_ordinal
queue_generation_id
queue_epoch_id
source_generation
target_generation
first/last canonical job ordinal
row_count
atlas_slot_index
P4 lease generation
P4 lease digest
resident/submitted/complete/failed lifecycle
```

All row identities must remain unique across admitted chunks.

## 3. P4 exact lease

R4A requires exact nonzero Atlas lease generation and exact lease digest. Stale/recycled lease identity fails closed before execution admission.

## 4. P5 ActiveAsync

R4A adds the semantic consumer class:

```text
TensorCubeTableMultiChunkHiMuonR4A
```

P5 consumer lifetime remains bound to the exact wave identity and physical submission completion. R4A does not weaken lease retirement.

## 5. Parameter completion authority

A parameter may span multiple chunks. Parameter completion therefore derives from total canonical TensorCube rows, not chunk completion order.

```text
parameter_expected_himuon_rows
parameter_completed_himuon_rows
```

Completion is valid only when all expected rows are complete and no chunk is failed.

Out-of-order chunk completion is explicitly legal.

## 6. Wave fence

Wave/parameter terminal authority requires:

```text
all required chunks terminal
all required rows terminal
no failed chunk
no duplicate row identity
no stale lease
parameter completed rows == expected rows
```

Chunk completion alone never means B06 publication, BP-DK durability, or generation commit.

## 7. Authority preservation

R4A preserves:

```text
R6 descriptor authority
P4 exact lease
P5 ActiveAsync
R3 scheduler parent
R2A compaction/indirect-dispatch parent
B06 publication authority
BP-DK durability authority
generation commit authority
HiMuon numerical math
AdamW numerical math
checkpoint format
```

## 8. Current backend physical constraint

Current HiMuon chunks may bind distinct physical source/candidate WGPU buffers. WebGPU WGSL cannot dereference arbitrary `physical_allocation_id` values as bindless storage-buffer pointers.

Therefore the final target:

```text
ONE CROSS-CHUNK READY TABLE
-> ONE BINDLESS-LIKE CROSS-BUFFER INDIRECT HIMUON DISPATCH
```

is not claimed by this first source bake.

The current backend execution model remains:

```text
MULTI_IN_FLIGHT_CHUNK_DISPATCH_WITH_EXACT_LEASES
```

with a wider bounded resident window. R4A explicitly records:

```text
single_dispatch_cross_buffer_claimed=false
```

until a shared physical arena / equivalent binding closure exists.

## 9. First source-bake adoption

The first R4A bake materializes the canonical multi-chunk control authority in the real production path:

```text
R6 seal
-> R6 descriptor snapshot
-> R4A admit_chunk
-> HiMuon submission
-> R4A mark_submitted
-> independent ActiveAsync progress
-> R4A mark_completed
-> parameter/wave fence receipt
```

It also extends P5 default concurrency from historical `2` to exact R6 Atlas slot count `3` only when R4A mode is enabled and no explicit max-in-flight value is supplied.

Historical default remains `2` with R4A disabled.

## 10. Activation modes

```text
ASH_TENSORCUBE_TABLE_R4A_MODE=OFF
ASH_TENSORCUBE_TABLE_R4A_MODE=OBSERVE_ONLY
ASH_TENSORCUBE_TABLE_R4A_MODE=ACTIVE_VERIFIED
```

`OBSERVE_ONLY` binds real production chunks and produces R4A authority evidence without changing HiMuon mathematics.

`ACTIVE_VERIFIED` is fail-closed until both debts are removed:

```text
per-chunk R3 TensorTable/scheduler recreation == 0
single-dispatch / shared-arena cross-buffer HiMuon backend closure == true
```

Reserved HOLD tokens:

```text
HOLD_TENSORCUBE_TABLE_R4A_PER_CHUNK_TABLE_SCHEDULER_RETIREMENT_NOT_YET_CLOSED
HOLD_TENSORCUBE_TABLE_R4A_CROSS_BUFFER_INDIRECT_HIMUON_BACKEND_NOT_YET_CLOSED
```

This prevents a false performance promotion.

## 11. No hot-path readback introduced

The new R4A control module contains no `map_async`, device polling, shader, numerical kernel, tensor readback, or host range reconstruction.

It does not add a per-chunk CPU checksum chain.

## 12. Runtime receipt

R4A emits:

```text
[ASH-TENSORCUBE-TABLE-R4A][wave-fence]
```

including:

```text
mode
parameter
source/target generation
admitted chunk count
resident chunk peak
expected/completed HiMuon row count
completed/failed chunk count
out-of-order completion count
parameter complete
wave fence ready
P4/P5/B06/BP-DK preservation
per-chunk table rebuild count
per-chunk scheduler recreate count
ready-count host-map count
host enumeration/range rebuild count
backend dispatch model
single-dispatch-cross-buffer claim
receipt digest
```

## 13. Static acceptance

Required:

```text
R4A module exported
chunk descriptor authority present
canonical TensorCube row identity preserved
exact generation/queue/lease validation
multi-chunk row uniqueness
out-of-order completion tracking
parameter completion authority
wave fence authority
P5 semantic consumer adoption
R4A-enabled Atlas-slot-count default concurrency
historical P5 default preserved
R3/R2A parents preserved
no new map/poll/numerical kernel
ActiveVerified debts fail closed
```

Current bake static results:

```text
PASS_TENSORCUBE_TABLE_R4A_MULTI_CHUNK_PARALLEL_HIMUON_STATIC checks=66
PASS_TENSORCUBE_TABLE_R3_CF1_PRODUCTION_CALLSITE_STATIC checks=51
PASS_TENSORCUBE_TABLE_R3_PERSISTENT_SCHEDULER_STATIC checks=52
PASS_TENSORCUBE_TABLE_R2A_PARALLEL_COMPACTION_STATIC checks=39
PASS_TENSORCUBE_TABLE_R2_GPU_PARALLEL_CONSUMER_STATIC
PASS_TENSORCUBE_TABLE_R1_STATIC
```

## 14. Compile acceptance

```powershell
cargo test -p base_train --lib tensorcube_table_r4a_ --release --locked
cargo test -p base_train --lib tensorcube_table_r3_ --release --locked
cargo test -p base_train --lib tensorcube_table_r2a_ --release --locked
cargo build -p base_train --bin base_train --release --locked
```

Compile is not claimed by the bake environment.

## 15. ObserveOnly physical qualification

Run with:

```text
ASH_TENSORCUBE_TABLE_R4A_MODE=OBSERVE_ONLY
```

Required evidence:

```text
admitted_chunk_count > 1
resident_chunk_peak > 1
duplicate_row_identity_count = 0
stale_lease_count = 0
parameter_expected_himuon_rows == parameter_completed_himuon_rows
failed_chunk_count = 0
parameter_complete = true
wave_transaction_fence_ready = true
P4/P5/B06/BP-DK preserved
```

Out-of-order completion count may be zero or nonzero; correctness must not depend on completion order.

## 16. ActiveVerified promotion boundary

R4A ActiveVerified may be promoted only after a successor closes both:

```text
per-chunk TensorTable/scheduler construction retirement
shared-arena / equivalent cross-buffer indirect HiMuon execution
```

The target hot path then becomes:

```text
MULTIPLE RESIDENT CHUNKS
-> ONE CANONICAL TENSORCUBE TABLE
-> CROSS-CHUNK READY COMPACTION
-> GPU INDIRECT HIMUON
-> OUT-OF-ORDER ROW COMPLETION
-> GPU PARAMETER COMPLETION
-> WAVE TRANSACTION FENCE
```

## 17. Evidence boundary

At bake time:

```text
SOURCE      PASS
STATIC      PASS
ARCHIVE     requires artifact seal
COMPILE     NOT RUN
RUNTIME     NOT RUN
PHYSICAL    NOT RUN
PERFORMANCE UNMEASURED
PROMOTED    NO
```

## 18. Final law

> R4A begins the authority cutover from chunk-serialized orchestration to TensorCube-row execution under a multi-chunk residency domain.
>
> Chunk is residency metadata. TensorCube row is execution identity. P4/P5 keep physical lifetime exact, parameter completion is independent of chunk order, and Wave remains the transaction fence.
>
> This first bake does not falsely claim WebGPU bindless cross-buffer execution. ActiveVerified remains fail-closed until per-chunk R3 object recreation and physical multi-buffer dispatch are retired.

## 19. Bake artifact seal

```text
Overlay ZIP
SHA-256 e212b7500095616216e153e363394c4ac43ddb7b4880237d1538387f7fb93c5d
regular files 5
CRC PASS

Full code-only ZIP
SHA-256 1ea39c9e02b69f462ad96eac322dd5b0e76633fb5dbf94ec1bd571bda7a306dd
regular files 8,491
CRC PASS
```
