# ASH-BASETRAIN-TENSORCUBE-MUON-ATLAS-WAVE-HOST-SCRATCH-SLAB-REUSE-AND-PER-TILE-HEAP-CHURN-RETIREMENT-R1

## 0. Revision Identity

`ASH-BASETRAIN-TENSORCUBE-MUON-ATLAS-WAVE-HOST-SCRATCH-SLAB-REUSE-AND-PER-TILE-HEAP-CHURN-RETIREMENT-R1`

Admission environment:

`ASH_MUON_ATLAS_WAVE_HOST_SCRATCH_SLAB_REUSE_R1=1`

Parent requirements:

- `ASH_MUON_ATLAS_WAVE_STREAMING_HOST_RETIREMENT_R1=1`
- `ASH_MUON_ATLAS_WAVE_SOURCE_PACKING_RETIREMENT_R1=1`

## 1. Purpose

Retire repeated host heap allocation in the TensorCube Local Muon Atlas-wave path while preserving the already-closed full-host candidate and full-host source retirement authorities.

This revision closes these implementation axes:

- repeated Atlas-wave source scratch allocation/free churn;
- repeated Atlas-wave momentum scratch allocation/free churn;
- 256-F32 / 1024-byte per-tile source heap allocation;
- five independent per-tile `Vec<f32>` payload allocations in `PendingTile`;
- ambiguous conflation between memory-block reuse and source/candidate semantic aliasing.

This revision does not claim the historical allocator failure was proven to be heap fragmentation, VA fragmentation, system commit exhaustion, or one exact allocation instruction.

## 2. Physical Trigger

The preceding physical N8 run established:

- full source scratch requested bytes = 0;
- full source scratch allocation count = 0;
- full source materialization count = 0;
- full candidate weight allocation count = 0;
- full candidate momentum allocation count = 0;
- full orthogonal update allocation count = 0;
- Atlas page bytes = 16,777,216;
- a 16 MiB BoundedPack source wave was successfully bound immediately before a raw `memory allocation of 1024 bytes failed` abort.

A known source tile representation was exactly `256 * sizeof(f32) = 1024` bytes and was heap-owned per tile. This revision removes that allocation topology without claiming it was the unique historical root cause.

## 3. State Ownership SSOT

### Current source authority

`Current ResidentWeightPack` remains the sole current source-weight semantic authority.

Required:

- read-only source access;
- no current source mutation;
- no candidate alias;
- no source-to-candidate ownership transfer.

### Candidate target authority

`ResidentWeightPackBuilder` remains the target candidate authority under canonical parameter byte ranges and canonical tile mapping.

### Scratch authority

Reusable host slabs are transient runtime-owned memory only. They carry no semantic authority.

Memory-block reuse is allowed. Semantic source/candidate aliasing is forbidden.

## 4. Runtime-Owned Reusable Slabs

`ProductionMuonExecutionRuntime` owns persistent:

- `source_wave_slab: Vec<f32>`;
- `momentum_wave_slab: Vec<f32>`;
- source slab generation observation.

The slabs survive individual wave and parameter calls and are reused across the runtime lifetime.

Initial allocation is fallible and bounded by the resident-state Atlas page authority. Once stable capacity is established, the hot path must not grow the slab. A later request larger than the established capacity fails closed instead of silently reallocating.

Required invariants:

- source slab capacity bytes <= Atlas page bytes;
- momentum slab capacity bytes <= Atlas page bytes;
- source slab reallocation count = 0 after initial binding;
- source scratch reused as candidate = false.

## 5. Per-Tile Source Heap Retirement

The old heap-owned shape is retired:

```rust
fn read_resident_muon_tile_f32(...) -> Result<Vec<f32>>
```

The source tile reader becomes caller-owned:

```rust
fn read_resident_muon_tile_f32_into_slice(
    ...,
    destination: &mut [f32],
) -> Result<()>
```

The destination cardinality is exactly 256 F32 values. No `Vec::new`, `try_reserve_exact`, `to_vec`, or heap-owned tile temporary is permitted inside the tile reader.

The runtime may append into a pre-capacity-bound reusable wave slab, but the tile operation itself may not allocate.

Required witness:

`per_tile_source_heap_allocation_count=0`

## 6. BP-Delta-K Observer Adoption

The BP-Delta-K local observer must not reintroduce the same 1024-byte tile allocation through its `WaveTiles` callback.

The callback contract changes from heap-owned tile return to caller-owned destination:

```rust
FnMut(u32, &mut [f32]) -> Result<()>
```

The observer owns one persistent `wave_weight_slab: Mutex<Vec<f32>>`, allocates its maximum bounded wave capacity once, and reuses it across observer calls. Unexpected growth after initial capacity binding fails closed.

No per-tile observer `Vec<f32>` is permitted.

## 7. PendingTile Heap Churn Retirement

The old `PendingTile` shape containing five `Vec<f32>` members is retired.

The R1 representation uses fixed inline payloads:

```rust
source_weight: [f32; 256]
source_momentum: [f32; 256]
candidate_weight: [f32; 256]
candidate_momentum: [f32; 256]
orthogonal_update: [f32; 256]
```

This removes five independent payload heap allocations per pending tile. `BTreeMap` metadata/node allocation is not claimed to be retired by this revision.

Required witness:

`pending_tile_payload_heap_vec_count=0`

`pending_payload_arena_allocation_count=0` is valid for the fixed-inline representation.

## 8. Logical Retirement Versus Physical Deallocation

`source_wave_pack_retired=true` means the logical wave payload is retired. It does not require the backing slab allocation to be returned to the system allocator.

Therefore:

- logical payload may be cleared;
- slab capacity may remain resident;
- the same backing slab may serve the next wave/parameter;
- this memory reuse must not be described as source/candidate in-place semantic reuse.

The previous ambiguous field `source_scratch_reused_in_place` is not sufficient to describe this revision.

New authority distinction:

- `source_scratch_reused_as_candidate=false`;
- `source_wave_slab_reused=true` through reuse counters.

## 9. Required Runtime Witness

Each admitted Muon parameter terminal must emit:

`[ASH-MUON-ATLAS-WAVE-HOST-SCRATCH-SLAB-REUSE-AND-PER-TILE-HEAP-CHURN-RETIREMENT-R1]`

with at least:

- patch id;
- admission env;
- parameter index;
- generation;
- optimizer step;
- Atlas page bytes;
- source wave slab generation;
- source wave slab capacity bytes;
- source wave slab peak logical bytes;
- source wave slab initial allocation count;
- source wave slab reuse count;
- source wave slab reallocation count;
- momentum wave slab capacity bytes;
- momentum wave slab initial allocation count;
- per-tile source heap allocation count;
- pending tile payload heap Vec count;
- pending payload arena allocation count;
- pending payload peak live bytes;
- source scratch reused as candidate = false;
- full source scratch allocation count = 0;
- full source materialization count = 0;
- full candidate weight allocation count = 0;
- full candidate momentum allocation count = 0;
- orthogonal full update allocation count = 0;
- source coverage exact = true;
- source order exact = true;
- current source mutation count = 0;
- historical allocator failure root cause claimed = false;
- verdict = PASS.

Runtime PASS token:

`PASS_ASH_BASETRAIN_TENSORCUBE_MUON_ATLAS_WAVE_HOST_SCRATCH_SLAB_REUSE_AND_PER_TILE_HEAP_CHURN_RETIREMENT_R1`

Static PASS token:

`PASS_ASH_BASETRAIN_TENSORCUBE_MUON_ATLAS_WAVE_HOST_SCRATCH_SLAB_REUSE_AND_PER_TILE_HEAP_CHURN_RETIREMENT_R1_STATIC`

## 10. Parent Closure Preservation

The following must remain true:

- full source scratch allocation count = 0;
- full source materialization count = 0;
- cross-wave full source pack accumulation count = 0;
- source wave bound <= Atlas page;
- source coverage exact = true;
- source order exact = true;
- current source mutation count = 0;
- full candidate weight allocation count = 0;
- full candidate momentum allocation count = 0;
- full orthogonal update allocation count = 0;
- cross-wave full candidate payload accumulation count = 0;
- canonical candidate commit preserved;
- BP-Delta-K generation binding preserved;
- RAM36 hard budget remains unchanged.

## 11. No Semantic or Numerical Repair

This revision does not alter:

- Muon numerical formula;
- Muon tile geometry;
- Muon iteration count;
- momentum semantics;
- orthogonalization semantics;
- canonical parameter order;
- canonical tile order;
- BP-Delta-K semantics;
- optimizer generation binding;
- scheduler semantics.

Forbidden:

- tolerance widening;
- clamp/normalize repair;
- NaN repair;
- serialization repair;
- batch reordering repair;
- retry with a different semantic layout;
- RAM36 hard-limit increase;
- pagefile/OS policy mutation as a correctness mechanism.

## 12. Static Acceptance

The static validator must confirm:

- runtime-owned reusable source/momentum slabs exist;
- capacity initialization is fallible and one-time;
- unexpected slab growth fails closed;
- source and momentum slab capacities are Atlas bounded;
- old `read_resident_muon_tile_f32 -> Vec<f32>` source reader is absent;
- caller-owned exact-256 tile reader exists;
- observer `WaveTiles` callback uses caller-owned storage;
- observer old tile-returning `Vec<f32>` callback is absent;
- observer persistent wave slab exists;
- `PendingTile` owns fixed arrays and no payload Vecs;
- required runtime witness exists;
- required PASS token exists;
- Source-R1 and Candidate-R1 closure markers remain present.

## 13. Focused Unit Acceptance

At minimum:

- source slab initial capacity can be reused without reallocation;
- source slab backing pointer remains stable across clear/reuse in focused test scope;
- resident 16x16 tile can be read into caller-owned 256-F32 storage exactly;
- inline pending tile payload copy preserves all 256 F32 values.

## 14. Physical Acceptance

Static PASS alone does not close this revision.

A fresh Consumer CF1 and fresh cross-release authority are required because the binary changes.

Physical N8 acceptance must reach at least the previous failure neighborhood:

- generation >= 7;
- optimizer step >= 7;
- parameter 97 reached;
- large multi-wave parameters reached;
- no same 1024-byte allocation failure at the prior boundary;
- source slab reuse witness observed;
- per-tile source heap allocation count = 0;
- pending tile payload heap Vec count = 0;
- no full-source or full-candidate regression.

If another allocator failure occurs after this revision PASS, the new requested size and exact preceding runtime witness become the new first-failure SSOT. Do not back-attribute it to the retired full-source scratch axis.

## 15. Performance Boundary

This revision may reduce CPU allocator overhead and memory topology churn, but it does not close the known 7-minute-step wall-clock axis caused by qualification-mode candidate readback and exact GPU waits.

Separate follow-up revision:

`ASH-BASETRAIN-TENSORCUBE-MUON-ATLAS-WAVE-BULK-CANDIDATE-D2H-AND-HOTPATH-EXACT-WAIT-RETIREMENT-R1`

## 16. Non-Goals

- no zero-copy claim;
- no GPU source gather adoption;
- no B05 active promotion;
- no C07/C08 active promotion;
- no historical heap-fragmentation root-cause claim;
- no system commit root-cause claim;
- no allocator replacement.

## 17. Closure Condition

CLOSED requires all of:

- reusable Atlas-bounded source slab;
- reusable Atlas-bounded momentum slab;
- no hot-path slab reallocation;
- zero per-tile source heap allocation;
- zero pending-tile payload Vec allocation;
- exact source and candidate authorities preserved;
- full-source retirement preserved;
- full-candidate retirement preserved;
- prior generation-7 failure neighborhood crossed;
- no same 1024-byte allocation failure at the prior boundary;
- static PASS;
- focused test PASS;
- physical runtime PASS.
