# TENSORCUBE-TABLE-R4A-CF1

## SHARED PHYSICAL ARENA
## + PER-CHUNK TABLE / SCHEDULER RETIREMENT
## + CROSS-CHUNK TENSORCUBE CONSUME CLOSURE

## 0. Revision

```text
Patch ID:
TENSORCUBE-TABLE-R4A-CF1

Canonical name:
ASH-BASETRAIN-TENSORCUBE-TABLE-R4A-CF1-
SHARED-PHYSICAL-ARENA-PERSISTENT-SCHEDULER-
CROSS-CHUNK-INDIRECT-HIMUON-BACKEND-CLOSURE

Class:
GPU residency / resource-lifetime / scheduling cutover
No HiMuon math change
No AdamW math change
No routing change
No checkpoint format change
```

Direct parent:

```text
TENSORCUBE-TABLE-R4A
MULTI-CHUNK PARALLEL HIMUON CONSUMPTION
```

Physical-resource parents retained:

```text
MCU SESSION R7
MCU DEVICE RESOURCE R7A
A01 SubmissionEpoch lifetime
P4 exact Atlas lease
P5 ActiveAsync
R2A parallel compaction
R3 bounded persistent scheduler
```

## 1. Exact source closure in this bake

R4A established multi-chunk identity and fail-closed promotion gates but intentionally left two debts:

```text
HOLD_TENSORCUBE_TABLE_R4A_PER_CHUNK_TABLE_SCHEDULER_RETIREMENT_NOT_YET_CLOSED
HOLD_TENSORCUBE_TABLE_R4A_CROSS_BUFFER_INDIRECT_HIMUON_BACKEND_NOT_YET_CLOSED
```

CF1 materializes a real source path that coalesces completed HiMuon successor chunks into bounded resident windows.

For one resident window:

```text
multiple completed HiMuon successor chunks
    -> three R7A shared source arenas
       (candidate W / candidate M / update)
    -> GPU D2D copy into shared source ranges
    -> one TensorCube Table materialization
    -> one R2A/R3 scheduler instance
    -> one tracked SubmissionEpoch
    -> assembly target buffers
    -> per-chunk B06 tickets after physical completion
```

This first CF1 source cutover closes per-chunk TensorTable/scheduler/submission at the **HiMuon successor-consumption boundary**.

It does not yet claim that the upstream HiMuon mathematical producer itself has been fused across multiple P4 chunks into one compute dispatch. That is a later producer-side optimization and must not be inferred from this source bake.

## 2. Chunk law

```text
Chunk = residency / lease partition
TensorCube row = canonical execution identity
Resident window = physical shared-binding domain
Wave = transaction / publication fence
```

Canonical row identity remains:

```text
(parameter_index, tensorcube_ordinal)
```

Chunk identity never replaces R6 job identity.

## 3. Existing R7/R7A resource authority

CF1 introduces no new allocator authority.

It reuses:

```text
McuSessionRuntimeR7
McuDeviceResourceRuntimeR7A
McuArenaDomainIdR7A
McuArenaBudgetSealR7A
usage_segregated_buffer_arena
PhysicalAllocationId
SubmissionEpoch
```

CF1 ActiveVerified requires the R7A bounded arena to be present.

No hidden direct-create fallback is introduced by the new CF1 module.

## 4. Shared source arenas

Each resident window acquires usage-safe R7A storage arenas for:

```text
shared candidate weight source
shared candidate momentum source
shared orthogonal/update source
```

Required usage:

```text
STORAGE | COPY_DST
```

The original chunk candidate buffers remain COPY_SRC inputs.

Within one command encoder:

```text
chunk source buffers
    -> copy_buffer_to_buffer
    -> shared arena subranges
    -> R3 scheduler consumption
```

No CPU tensor staging is introduced.

## 5. Usage-segregation law

R4A-CF1 preserves the R2B-CF3 lesson that incompatible read/read-write roles must not be packed blindly into one conflicting WGPU buffer usage scope.

Shared arena means shared **within compatible semantic/usage roles**.

The implementation uses separate W/M/update source arena buffers and preserves the existing assembly target buffers.

## 6. Multi-epoch same-parameter TensorTable support

Historical TensorCube Table R1 admitted one epoch per parameter table materialization.

CF1 extends the table input ABI with:

```text
source_element_base_r4a_cf1
```

Historical callers use zero.

CF1 may provide multiple exact R6 epochs for the same parameter, provided the parameter authority is byte/geometry identical.

Repeated parameter epochs are rejected on drift of:

```text
canonical weight base
canonical momentum base
logical shape
tensorcube geometry
```

The parameter authority record is stored once.

R6 descriptors remain the semantic lineage authority; the shared-arena source base changes physical source addressing only.

## 7. Source address rebasing

For each row:

```text
shared source element
=
resident-window source base
+
original descriptor-local source element
```

This applies independently to:

```text
candidate weight
candidate momentum
orthogonal/update
```

Checked arithmetic is mandatory.

## 8. Resident-window admission

The production callsite retains multiple completed HiMuon successors in a CF1 ready map.

A resident window admits up to the current bounded Atlas/P5 concurrency target; the first source cut uses a maximum of three ready chunks per window.

A terminal single-chunk remainder uses the same CF1 shared-arena path rather than falling back to the old per-chunk R3 function.

Cross-chunk promotion evidence still requires at least one window containing more than one chunk.

## 9. One Table / Scheduler per resident window

For each resident window CF1 performs exactly:

```text
one TensorCubeTableHostAuthorityR1::materialize
one TensorCubeTableAuthorityR1::upload
one TensorCubeTablePersistentSchedulerR3::new
one scheduler.encode_generation_epoch
one tracked backend submission
```

There is no R3 constructor call per chunk inside the CF1 ActiveVerified branch.

This is the first physical cut from per-chunk object reconstruction to bounded shared-window reconstruction.

Full training-generation-long table/scheduler lifetime is not claimed yet.

## 10. GPU cross-chunk consume

After D2D packing, all row source offsets resolve into the same fixed shared W/M/update bindings.

The existing R2A/R3 device machinery therefore consumes a TensorCube Table containing rows from several chunk identities without WGSL needing bindless arbitrary-buffer lookup.

The backend model is classified as:

```text
R4A_CF1_SHARED_ARENA_CROSS_CHUNK_INDIRECT
```

`single_dispatch_cross_buffer_claimed` becomes true only when runtime telemetry observes at least one resident window containing multiple chunks.

## 11. Submission and lifetime authority

The CF1 backend batch submission tracks:

```text
all original chunk source allocations as READ
shared R7A W/M/update arenas as READ_WRITE within the submission lifetime
assembly W/M/update as WRITE
```

After physical completion:

```text
A01 submission leases release
original chunk A02 source leases reclaim
R7A shared source arena leases reclaim through exact R7A domain authority
assembly ranges mark complete
B06 tickets are claimed per original chunk
```

The shared source arena may not be reused before exact final-reader retirement.

## 12. P4 preservation

Every original chunk remains bound to its exact:

```text
Atlas slot
lease generation
lease digest
R6 epoch
P5 wave identity
```

CF1 does not merge P4 semantic identities merely because physical payloads are copied into a shared arena.

P4 retirement occurs only after the CF1 semantic consumer releases its token and the existing final-consumer conditions are satisfied.

## 13. P5 preservation

New P5 semantic consumer kind:

```text
TensorCubeTableCrossChunkHiMuonR4ACf1
```

CF1 consumer lifetime spans the shared resident-window consumption stage.

Historical R4A consumer identity remains materialized.

## 14. B06 preservation

B06 remains per original successor chunk.

Shared-window completion does not create one synthetic aggregate B06 ticket.

The backend claims one existing `LocalMuonDeviceSuccessorTicketR1` for each original chunk after the shared submission physically completes.

## 15. BP-DK preservation

BP-DK durability and filesystem authority remain outside CF1.

CF1 changes only the device consumption topology.

No BP-DK state is synthesized in the TensorTable.

## 16. R4A HOLD retirement conditions

R4A final promotion gates can be satisfied by CF1 only when runtime evidence reports:

```text
per_chunk_table_rebuild_count = 0
per_chunk_scheduler_recreate_count = 0
cross_chunk_window_count > 0
max_distinct_chunks_in_window > 1
```

Then:

```text
single_dispatch_cross_buffer_claimed = true
```

The historical R4A HOLD tokens remain fail-closed guards rather than being deleted.

## 17. No per-chunk map/poll scheduling loop in new module

The new CF1 high-level module contains no:

```text
map_async
blocking device poll
private queue.submit
```

Completion uses the existing tracked backend collection path.

One nonblocking completion observation applies to one resident-window submission rather than one table submission per chunk.

## 18. Telemetry

CF1 records at minimum:

```text
resident_window_count
cross_chunk_window_count
admitted_chunk_count
max_distinct_chunks_in_window
table_materialization_count
r2a_scheduler_create_count
r3_scheduler_create_count
submission_count
chunk_count_submitted
completed_chunk_count
shared_arena_binding_count
per_chunk_table_materialization_count
per_chunk_scheduler_create_count
ready_count_host_map_count
host_row_enumeration_count
host_range_rebuild_count
cross_chunk_indirect_backend_materialized
shared_arena_binding
```

Runtime logs:

```text
[ASH-TENSORCUBE-TABLE-R4A-CF1][indirect-himuon]
[ASH-TENSORCUBE-TABLE-R4A-CF1][wave-fence]
[ASH-TENSORCUBE-TABLE-R4A-CF1][performance]
```

## 19. Activation

```text
ASH_TENSORCUBE_TABLE_R4A_CF1_MODE=OFF
ASH_TENSORCUBE_TABLE_R4A_CF1_MODE=OBSERVE_ONLY
ASH_TENSORCUBE_TABLE_R4A_CF1_MODE=ACTIVE_VERIFIED
```

CF1 enabled requires:

```text
R4A enabled
R3 ActiveVerified
```

CF1 ActiveVerified additionally requires:

```text
R4A ActiveVerified
R7A bounded arena present
```

## 20. Numerical preservation

CF1 does not modify:

```text
HiMuon mathematical producer
Muon orthogonalization
subgroup reduction order
momentum math
AdamW math
optimizer routing
checkpoint serialization
```

The shared stage moves already-computed successor bytes and reuses existing TensorCube table-copy kernels.

## 21. Physical qualification

A real ActiveVerified campaign must prove at least:

```text
admitted_chunk_count > 1
cross_chunk_window_count > 0
max_distinct_chunks_in_window > 1
per_chunk_table_rebuild_count = 0
per_chunk_scheduler_recreate_count = 0
ready_count_host_map_count = 0
host_row_enumeration_count = 0
host_range_rebuild_count = 0
assembly coverage complete
B06 ticket count exact
P4/P5 retirement exact
stale lease execution = 0
numerical successor parity exact
```

## 22. Performance qualification

Measure against the R4A/R3 per-chunk consumer baseline:

```text
chunk count
resident-window count
submission count
chunks per submission
Table materialization count
R2A/R3 scheduler construction count
host encode time
host wait time
GPU active time
GPU idle-gap time
parameter wall time
```

Performance PASS is not claimed statically.

## 23. Changed files

```text
MOD crates/base_train/src/lib.rs
MOD crates/base_train/src/tensorcube_table_r1.rs
MOD crates/base_train/src/tensorcube_table_parallel_consumer_r2.rs
MOD crates/base_train/src/tensorcube_table_r3_cf1_production_adoption.rs
MOD crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
MOD crates/base_train/src/unified_atlas_mcu_submission_epoch_dependency_active_async_r1.rs
MOD crates/burn_webgpu_backend/src/base_train_tensorcube_local_muon_active_device_pending_r1.rs
ADD crates/base_train/src/tensorcube_table_r4a_cf1_shared_arena_himuon.rs
ADD tools/validate_ash_tensorcube_table_r4a_cf1_shared_arena_himuon_static.py
```

Delta:

```text
MOD 7
ADD 2
DEL 0
```

## 24. Static evidence

```text
PASS_TENSORCUBE_TABLE_R4A_CF1_SHARED_PHYSICAL_ARENA_PERSISTENT_SCHEDULER_CROSS_CHUNK_INDIRECT_HIMUON_STATIC checks=90
PASS_TENSORCUBE_TABLE_R4A_MULTI_CHUNK_PARALLEL_HIMUON_STATIC checks=66
PASS_TENSORCUBE_TABLE_R3_CF1_PRODUCTION_CALLSITE_STATIC checks=51
PASS_TENSORCUBE_TABLE_R3_PERSISTENT_SCHEDULER_STATIC checks=52
PASS_TENSORCUBE_TABLE_R2A_PARALLEL_COMPACTION_STATIC checks=39
PASS_TENSORCUBE_TABLE_R2_GPU_PARALLEL_CONSUMER_STATIC checks=28
PASS_TENSORCUBE_TABLE_R1_STATIC checks=20
PASS_ASH_MCU_SESSION_PERSISTENT_EXECUTION_FABRIC_AND_OPTIMIZER_INDEPENDENT_JOB_AUTHORITY_R7_STATIC checks=55
```

Known unrelated parent drift:

```text
MCU R7A validator = 79 / 83
```

The same four failures are present in the unmodified R4A parent archive:

```text
budget fail closed
max buffer size guarded
storage binding size guarded
uniform binding size guarded
```

They are therefore not attributed to CF1.

## 25. Artifact seal

```text
Overlay ZIP
SHA-256 7fb4d5107ddd76317bb22de54f2c9c14bfc27a04433470a28027cd07c74f3ca2
files 9
CRC PASS

Full code-only ZIP
SHA-256 68e3b2a34fb60f615589cfdb46560eace3cad7b40c329b10b0441a9d3cf13cff
files 8,493
CRC PASS
```

## 26. Evidence boundary

At bake time:

```text
SOURCE       PASS
STATIC       PASS
ARCHIVE      PASS
COMPILE      NOT RUN
RUNTIME      NOT RUN
PHYSICAL     NOT RUN
PERFORMANCE  UNMEASURED
PROMOTED     NO
```

No Rust compile or physical speedup is claimed by this bake environment.

## 27. Compile acceptance

```powershell
cargo test -p base_train --lib tensorcube_table_r4a_cf1_ --release --locked
cargo test -p base_train --lib tensorcube_table_r4a_ --release --locked
cargo test -p base_train --lib tensorcube_table_r3_ --release --locked
cargo test -p base_train --lib tensorcube_table_r2a_ --release --locked
cargo build -p base_train --bin base_train --release --locked
```

## 28. Final law

> R4A declared that chunk is residency metadata rather than execution identity.
>
> CF1 removes the per-chunk TensorTable/R3 consume object graph from the ActiveVerified successor-consumption path by packing several completed HiMuon successor chunks into usage-safe R7A shared source arenas.
>
> Original R6/P4/P5 identities remain exact. TensorCube rows retain their canonical job identities. Physical source addressing gains a bounded shared-arena base only.
>
> One resident window is consumed through one TensorCube Table, one R2A/R3 scheduler stack and one tracked SubmissionEpoch. B06 tickets remain per original chunk after physical completion.
>
> This is a real orchestration/I/O cut at the successor-consumption boundary. It is not yet a claim that upstream HiMuon mathematical compute itself has been fused across several P4 chunks.
