# TENSORCUBE-TABLE-R4A-CF2-CF1

## DIRECT PRODUCER OUTPUT → CF1 SHARED ARENA
## + CANDIDATE REPACK D2D RETIREMENT
## + EXACT PRODUCER / CONSUMER RANGE-LEASE HANDOFF

## 0. Revision

Patch ID: `TENSORCUBE-TABLE-R4A-CF2-CF1`

Canonical name:

`ASH-BASETRAIN-TENSORCUBE-TABLE-R4A-CF2-CF1-DIRECT-PRODUCER-OUTPUT-CF1-SHARED-ARENA-CANDIDATE-REPACK-D2D-RETIREMENT`

Direct parent: `TENSORCUBE-TABLE-R4A-CF2`

Semantic parents:

- `TENSORCUBE-TABLE-R4A-CF1`
- MCU SESSION R7
- MCU DEVICE RESOURCE R7A
- MCU HiMuon packed-gradient R7A1
- A01 SubmissionEpoch
- P4 Exact Lease
- P5 ActiveAsync

This revision changes physical output ownership and source addressing only. HiMuon mathematics, reduction order, optimizer routing, B06, BP-DK and generation commit semantics remain unchanged.

## 1. Parent debt

CF2 materialized the producer multi-batch authority while preserving historical truth:

```text
TENSORCUBE_TABLE_R4A_CF2_MULTI_BATCH_ASYNC_AUTHORITY_MATERIALIZED = true
TENSORCUBE_TABLE_R4A_CF2_DIRECT_SHARED_ARENA_OUTPUT_MATERIALIZED = false
```

CF2-CF1 materializes the direct-output child without rewriting the historical CF2 constant.

## 2. Core physical law

Historical:

```text
HiMuon producer
→ private candidate W/M/update
→ CF1 GPU D2D repack
→ shared CF1 source arenas
→ TensorCube Table consumer
```

CF2-CF1:

```text
P4 slot
→ exact R7A W/M/update shared subranges
→ HiMuon writes directly into those ranges
→ producer SubmissionEpoch completes
→ CF1 exact READ range leases bind the same bytes
→ TensorCube Table consumes them
→ final reader retirement
→ arena reclaim
```

No producer-to-CF1 payload relocation is required on the direct path.

## 3. P4-slot shared output geometry

One parameter-scoped direct arena owns three R7A leases:

```text
candidate weight
candidate momentum
orthogonal/update
```

Subrange geometry:

```text
slot_stride_bytes
  = align_up(max_wave_payload_bytes,
             min_storage_buffer_offset_alignment)

total_arena_bytes
  = slot_stride_bytes * R6 Atlas slot count
```

The exact P4 `slot_index` selects the output subrange. P4 still owns slot reuse safety and is not redefined.

## 4. Direct output ABI

Backend materializes `ActiveDeviceDirectOutputBindingR4ACf2Cf1` with:

```text
candidate weight Arc<wgpu::Buffer>
candidate momentum Arc<wgpu::Buffer>
update Arc<wgpu::Buffer>
exact PhysicalAllocationId for each role
physical_element_start
element_capacity
```

The producer binds each output as shared buffer + exact byte offset + exact byte size.

A01 tracks the output as exact `OwnedExisting` physical ranges rather than private candidate allocations.

## 5. Candidate backing physical subrange ABI

`MuonDeviceCandidatePartitionBacking` gains defaulted physical starts:

```text
candidate_weight_physical_element_start
candidate_momentum_physical_element_start
update_scratch_physical_element_start
```

Historical/private producer paths explicitly use zero. The direct child stores the nonzero P4-slot-derived base.

Checked arithmetic and capacity validation are fail-closed.

## 6. Output ownership split

ActiveDevice candidate resources distinguish:

```text
Private
DirectSharedR4ACf2Cf1
```

Private preserves historical A02 ownership/reclaim.

DirectShared means the successor does not own the shared arena page; the parameter-scoped CF2-CF1 arena owns physical lifetime.

Legacy private consumers fail closed when given DirectShared state.

## 7. Direct producer submission

Normal and expert-routed ActiveDevice producer paths gain direct-output variants.

No second mathematical HiMuon shader is introduced.

R7A1 packed-gradient physical identity and exact multi-consumer lifetime remain unchanged.

## 8. Direct CF1 consumer

The backend direct CF1 path:

1. requires DirectShared successors;
2. validates shared allocation identity and physical offsets;
3. acquires A01 `OwnedExisting` READ range leases over W/M/update;
4. submits through tracked SubmissionEpoch authority;
5. writes existing real assembly targets;
6. marks coverage after exact physical completion;
7. produces one existing B06 ticket per original successor chunk.

The direct consumer never owns or prematurely reclaims the shared source arena.

## 9. Repack retirement

For the direct route:

```text
payload_copy_count = 0
payload_copy_bytes = 0
cf1_repack_d2d_copy_count = 0
cf1_repack_d2d_bytes = 0
candidate W/M/update D2H = 0
```

The historical CF1 repack route remains compatibility-only for non-direct producers.

## 10. TensorCube source addressing

CF1 already supports `source_element_base_r4a_cf1`.

CF2-CF1 sets it to the producer's exact physical element start:

```text
shared arena base
+ physical_element_start
+ R6 descriptor-local source offset
```

No chunk-private source buffer is reconstructed.

## 11. Producer/consumer lease handoff

Physical lifetime is:

```text
producer WRITE range lease
→ producer physical completion
→ CF1 READ range lease
→ CF1 physical completion
→ downstream final-reader proof
→ R7A reclaim
```

Producer completion alone is never reclaim authority.

## 12. Current overlap boundary

This first source implementation begins direct CF1 consumption after the existing producer successor collection observes producer physical completion.

Therefore CF2-CF1 closes candidate relocation D2D but does **not** claim producer-N+1 GPU compute / CF1-consumer-N overlap.

That remains a later performance child.

## 13. P4 / P5 / B06 / BP-DK preservation

- P4 exact slot, lease generation, digest and R6 epoch remain per original wave.
- P5 gains `TensorCubeTableDirectSharedArenaR4ACf2Cf1` as an explicit semantic consumer.
- B06 remains per original successor and is issued only after direct CF1 physical completion.
- BP-DK durability/filesystem authority stays outside the TensorTable.
- Generation commit authority is unchanged.

## 14. Production cutover

When CF2-CF1 ActiveVerified is selected:

```text
CF2 / CF1 / R4A parents active
→ open one parameter-scoped direct arena
→ bind every producer wave to P4-slot output subrange
→ use direct producer entrypoint
→ collect physically completed direct successor
→ group direct successors into CF1 ready windows
→ submit direct CF1 window with zero repack
→ collect window
→ stage B06 per original wave
→ release P5 / retire P4
→ after all exact readers retire, reclaim direct arena
```

R4A runtime classification becomes:

`R4A_CF2_CF1_DIRECT_SHARED_ARENA_CROSS_CHUNK_INDIRECT`.

## 15. Telemetry

At minimum:

```text
direct_output_chunk_count
private_candidate_buffer_create_count
cf1_repack_d2d_bytes
cf1_repack_d2d_copy_count
producer_consumer_dependency_count
producer_consumer_overlap_count
direct_window_count
direct_cross_chunk_window_count
orphan_direct_output_count
consumer_without_producer_count
stale_incarnation_count
early_reclaim_count
```

The overlap counter is observational and is not a PASS predicate in this revision.

## 16. Runtime receipts

Required logs include:

```text
[ASH-TENSORCUBE-TABLE-R4A-CF2-CF1][handoff]
[ASH-TENSORCUBE-TABLE-R4A-CF2-CF1][consumer-bind]
[ASH-TENSORCUBE-TABLE-R4A-CF2-CF1][performance]
```

The handoff receipt binds zero payload-copy count and bytes.

## 17. Source/static qualification

Current bake:

```text
R4A-CF2-CF1  90/90 PASS
CF2           40/40 PASS
CF1           90/90 PASS
R4A           66/66 PASS
R3-CF1        51/51 PASS
R3            52/52 PASS
R2A           39/39 PASS
R2            28/28 PASS
R1            20/20 PASS
MCU R7        55/55 PASS
```

Known R7A1 validator baseline remains `77/82` on both the unmodified CF2 parent and this child. The same five textual cutover checks fail in both trees, so this is not attributed to CF2-CF1.

## 18. Exact implementation delta

Compared with the CF2 code-only parent:

```text
MOD 10
ADD 2
DEL 0
```

New files:

```text
crates/base_train/src/tensorcube_table_r4a_cf2_cf1_direct_shared_arena.rs
tools/validate_ash_tensorcube_table_r4a_cf2_cf1_direct_shared_arena_static.py
```

## 19. Artifact seal

```text
Overlay ZIP
SHA-256 46b9a98616d923ac00b6656e1b1beea09625aa6c80cb1fc97f7e59a75d502b26
files 12
CRC PASS

Full code-only ZIP
SHA-256 7272db8ca6310aae55ab5fe9213a436954c92c7ed89a099489d1f96ed0785fbe
files 8,497
CRC PASS

Specification artifact
SHA-256 05cc1382c746a65bbbf5dfc979b22f68e1ff3ce8e156fe132bc220fd19fb6975
```

## 20. Evidence boundary

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

No zero-D2D runtime or speedup claim is made without physical evidence.

## 21. Compile acceptance

```powershell
cargo test -p base_train --lib tensorcube_table_r4a_cf2_cf1_ --release --locked
cargo test -p base_train --lib tensorcube_table_r4a_cf2_ --release --locked
cargo test -p base_train --lib tensorcube_table_r4a_cf1_ --release --locked
cargo test -p burn_webgpu_backend --lib tensorcube_local_muon --release --locked
cargo build -p base_train --bin base_train --release --locked
```

## 22. Physical acceptance

First qualify ObserveOnly, then ActiveVerified.

ActiveVerified physical PASS requires at minimum:

```text
direct_output_chunk_count > 0
private_candidate_buffer_create_count = 0
candidate W/M/update D2H = 0
cf1_repack_d2d_bytes = 0
cf1_repack_d2d_copy_count = 0
payload_copy_count = 0
payload_copy_bytes = 0
producer exact range lease = true
consumer exact range lease = true
output overlap count = 0
orphan direct output count = 0
consumer without producer count = 0
stale incarnation count = 0
early reclaim count = 0
B06 / P4 / P5 exact
bit-exact successor parity
```

Producer/consumer overlap is not required by this revision.

## 23. Final law

> P4 slot identity selects an exact aligned subrange inside bounded R7A candidate W/M/update arenas. HiMuon writes directly into those bytes. After producer physical completion, CF1 obtains exact read-range leases over the same allocation/subrange and consumes them without candidate D2D repacking or D2H materialization.
>
> Shared memory never weakens lifetime authority. Producer completion is not reclaim authority; the shared arena returns only after exact downstream reader retirement.
>
> CF2-CF1 removes candidate relocation. It does not yet claim producer/consumer GPU overlap.
