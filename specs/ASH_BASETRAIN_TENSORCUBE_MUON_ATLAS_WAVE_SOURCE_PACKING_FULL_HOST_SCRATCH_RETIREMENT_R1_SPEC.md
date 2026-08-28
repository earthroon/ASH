# ASH-BASETRAIN-TENSORCUBE-MUON-ATLAS-WAVE-SOURCE-PACKING-FULL-HOST-SCRATCH-RETIREMENT-R1

## 0. Revision identity

```text
ASH-BASETRAIN-TENSORCUBE-MUON-
ATLAS-WAVE-SOURCE-PACKING-
FULL-HOST-SCRATCH-RETIREMENT-R1
```

This revision retires the remaining full-cardinality Muon host source-packing scratch while preserving the previously closed candidate-retirement, BP-Delta-K generation, RAM36 projection, and successor-allocation ownership axes.

## 1. Physical trigger SSOT

The parent physical run already proved:

```text
full_candidate_weight_allocation_count=0
full_candidate_momentum_allocation_count=0
full_orthogonal_update_allocation_count=0
cross_wave_full_payload_accumulation_count=0
payload_retired=true
coverage_exact=true
```

and repeatedly emitted:

```text
source_scratch_reused_in_place=true
source_scratch_retired=false
```

The run later reproduced:

```text
memory allocation of 1044033536 bytes failed
```

This revision does not claim that the historical 1,044,033,536-byte request has already been directly proven to be `packed_muon_weight`. The owner claim remains false until direct evidence exists.

## 2. Target ownership shape

Before:

```text
Current Resident Weight
  -> full host packed_muon_weight
  -> Atlas execution waves
  -> candidate written back into same source scratch
```

After:

```text
Current Resident Weight Authority
  -> exact Atlas-bounded source pack
  -> Muon wave execution
  -> compact BP-Delta-K evidence
  -> exact candidate tile commit
  -> physically allocated Successor ResidentWeightPack Authority
```

The source authority and target authority are separate.

## 3. SSOT ownership

### 3.1 Source

`ResidentWeightPack` for the current generation owns source generation, source optimizer step, parameter identity, canonical packed byte offset, current weight bytes, and current weight digest.

Source wave packs are projections only. They never become durable/current training-state authority.

### 3.2 Geometry

`MuonResidentStateGraph::atlas_page_bytes()` and the existing execution plan own the source-wave bound and canonical tile identity. The scheduler does not introduce an independent source-wave byte constant.

### 3.3 Target

The already physically allocated successor `ResidentWeightPackBuilder` owns target-generation candidate bytes. The Muon source scratch is not reused as the candidate target.

## 4. Production admission

The new revision is explicitly admitted by:

```text
ASH_MUON_ATLAS_WAVE_SOURCE_PACKING_RETIREMENT_R1=1
```

It requires the parent candidate-retirement revision:

```text
ASH_MUON_ATLAS_WAVE_STREAMING_HOST_RETIREMENT_R1=1
```

The published D10 qualification profile remains:

```text
ASH_MUON_RESIDENT_STATE_MODE=ACTIVE_VERIFIED
ASH_HIMUON_DEVICE_CANDIDATE_MODE=MIRROR_VERIFIED
ASH_HYBRID_DEVICE_COMMIT_MODE=MIRROR_VERIFIED
ASH_GPU_EVIDENCE_MODE=MIRROR_VERIFIED
ASH_C08_ASYNC_SUBMISSION_RETIREMENT_MODE=MIRROR_VERIFIED
```

BP-Delta-K full replay/counterfactual routes remain disabled:

```text
ASH_BP_DK_ACTIVE_FUSION_REPLAY_MODE=DISABLED
ASH_BP_DK_ACTIVE_FUSION_COUNTERFACTUAL_MODE=DISABLED
```

No runtime mode is silently mutated by the revision.

## 5. Full source scratch retirement

When the new admission is active, the scheduler must not create a full-cardinality host source Vec for Muon.

Forbidden admitted-path semantics include:

```text
Vec<f32>(full Muon parameter cardinality)
Vec::with_capacity(full Muon parameter cardinality)
vec![0.0f32; full Muon parameter cardinality]
full parameter source clone
a renamed semantic equivalent of packed_muon_weight
```

The legacy full-pack route may remain reachable only when the new admission is not requested.

Required scheduler witness:

```text
[ASH-MUON-ATLAS-SOURCE-SCRATCH-RETIREMENT-R1]
full_source_scratch_requested_bytes=0
full_source_scratch_allocation_count=0
atlas_source_bound_authority=runtime_resident_state_graph
historical_1044033536_owner_claimed=false
```

## 6. R1 source route: BoundedPack

R1 implements BoundedPack source streaming. It does not claim a zero-copy route.

Required terminal value:

```text
source_zero_copy_wave_count=0
```

For each local or fused source execution partition:

1. Bind exact parameter/generation/wave identity.
2. Read only the canonical 16x16 source tiles required by that partition from current `ResidentWeightPack` bytes.
3. Allocate the host source pack with a fallible bounded allocation.
4. Enforce source-pack capacity not greater than the Atlas page bound.
5. Execute the Muon partition.
6. Retire the source wave pack when its execution scope ends.

## 7. Exact source tile projection

Each source tile is read using parameter byte offset, parameter logical column count, full tile-column count, tile ordinal, and canonical 16x16 row-major tile geometry.

Required invariants:

```text
source generation exact
source optimizer step exact
parameter identity exact
canonical tile ordinal exact
canonical packed byte offset exact
source values finite
```

No parameter reordering or source-value normalization is permitted.

## 8. Source pack capacity

For an allocated BoundedPack:

```text
source_requested_bytes = source_wave_elements * sizeof(f32)
source_capacity_bytes <= atlas_page_bytes
```

Failure tokens include:

```text
FAIL_ASH_BASETRAIN_MUON_ATLAS_WAVE_SOURCE_PACK_ALLOCATION
FAIL_ASH_BASETRAIN_MUON_SOURCE_WAVE_CAPACITY_EXCEEDS_ATLAS_BOUND
```

No emergency full gather and no silent adaptive wave resize are allowed.

## 9. BP-Delta-K local observer source

The BP-Delta-K local observer must not force reconstruction of a full host source tensor. It accepts either the legacy `Packed(source)` route or the admitted `WaveTiles(read_tile)` route.

`WaveTiles` fills the observer GPU weight buffer through Atlas-bounded host waves. The GPU buffer may remain full-parameter sized because this revision targets host source duplication, not GPU observer-buffer retirement.

No full host observer source reconstruction is permitted in the admitted source-streaming route.

## 10. Successor direct candidate commit

Muon candidate tiles are not written back into the source pack.

```text
candidate tile
  -> exact target logical byte ranges
  -> ResidentWeightPackBuilder::write_f32_at
```

Required output authority:

```text
candidate_weight_streamed_to_successor=true
candidate_weight_in_place=false
```

The current source resident pack remains read-only.

## 11. Sparse successor initialization contract

The successor builder is physically allocated at its exact full target capacity by the already closed RAM36 successor-allocation authority.

This revision permits exact sparse initialization of Muon candidate ranges before sequential serialization. Builder state tracks initialized ranges, initialized byte count, append cursor, and allocated full successor capacity.

Random target writes must be non-overlapping and in-bounds. When later sequential serialization reaches an already initialized Muon range, it must verify the bytes exactly rather than overwrite them silently.

A mismatch fails with:

```text
ResidentWeightPackBuilderPreinitializedByteMismatch
```

Finalization requires exact full coverage and exact final digest.

## 12. No successor duplicate full buffer

The sparse-write mechanism uses the already allocated successor `ResidentWeightPackBuilder` capacity. It must not create another full target Vec to support random access.

## 13. Candidate retirement preservation

The parent closure remains mandatory:

```text
full_candidate_weight_allocation_count=0
full_candidate_momentum_allocation_count=0
full_orthogonal_update_allocation_count=0
```

and:

```text
PASS_ASH_BASETRAIN_TENSORCUBE_MUON_ATLAS_WAVE_STREAMING_HOST_FULL_CANDIDATE_MATERIALIZATION_RETIREMENT_R1
```

Source-scratch retirement must not reintroduce any full candidate aggregate.

## 14. Bounded pending source evidence

The existing candidate streaming path can delay canonical commit when physical fused-down completion order differs from canonical tile order. Therefore bounded `PendingTile` evidence may retain per-tile source values across a wave boundary.

This is not a full source pack and must not be falsely reported as zero.

The revision separately measures:

```text
maximum_source_wave_pack_live_bytes
maximum_pending_source_evidence_bytes
maximum_combined_source_transient_bytes
```

The forbidden condition is cross-wave full source-pack accumulation, not bounded pending evidence required by canonical-commit correctness.

## 15. Pending bound preservation

The existing bounded pending-tile invariant remains:

```text
pending_tiles <= full_tile_cols + atlas_wave_tile_capacity
```

A violation remains fail-closed under the parent candidate-streaming gate. No full-parameter pending source reconstruction is allowed.

## 16. Runtime witnesses

Per source binding:

```text
[ASH-MUON-ATLAS-WAVE-SOURCE-BINDING-R1]
parameter_index=...
generation=...
optimizer_step=...
wave_id=...
partition=local|fused
source_route=BoundedPack
atlas_page_bytes=...
atlas_source_bound_bytes=...
source_requested_bytes=...
source_capacity_bytes=...
full_source_scratch_allocation_count=0
source_is_full_parameter=false
```

After source wave-pack scope retirement:

```text
[ASH-MUON-ATLAS-WAVE-SOURCE-RETIREMENT-R1]
source_wave_pack_retired=true
active_source_wave_pack_count_after=0
bounded_pending_source_evidence_tiles_after=...
cross_wave_full_source_pack_accumulation_count=0
```

## 17. Parameter terminal witness

Required terminal witness:

```text
[ASH-MUON-ATLAS-WAVE-SOURCE-PACKING-RETIREMENT-R1]
```

Required fields include:

```text
source_zero_copy_wave_count=0
source_bounded_pack_binding_count>0
full_source_scratch_allocation_count=0
full_source_materialization_count=0
cross_wave_full_source_pack_accumulation_count=0
source_scratch_reused_in_place=false
source_scratch_retired=true
source_coverage_exact=true
source_order_exact=true
current_source_mutation_count=0
candidate_full_weight_allocation_count=0
candidate_full_momentum_allocation_count=0
orthogonal_full_update_allocation_count=0
source_allocation_owner_attribution_exact=true
historical_1044033536_owner_claimed=false
verdict=PASS
```

Required PASS token:

```text
PASS_ASH_BASETRAIN_TENSORCUBE_MUON_ATLAS_WAVE_SOURCE_PACKING_FULL_HOST_SCRATCH_RETIREMENT_R1
```

## 18. Historical 1,044,033,536-byte failure

The revision preserves the historical exact request size as evidence but does not manufacture an owner identity.

Required field:

```text
historical_1044033536_owner_claimed=false
```

If source-retirement PASS is observed and the same raw allocation failure later recurs, this revision has closed the source full-scratch axis and the remaining allocation belongs to a different/next owner until directly attributed.

If the admitted source path itself attempts a full source scratch, the revision fails before claiming PASS.

## 19. RAM36 preservation

Hard process limit remains exactly:

```text
38,654,705,664 bytes
```

No `PrivateUsage` discount, synthetic subtraction, hard-limit increase, or reservation rewrite is allowed.

The prior successor transition remains authoritative:

```text
Admitted
-> PhysicalAllocated
-> Materializing
-> Materialized
-> Promoted
-> Released
```

## 20. Logical retirement versus OS reclamation

This revision distinguishes Rust source-wave lifetime end, allocator free/reuse behavior, and Windows process `PrivateUsage` reclamation. They are not the same event.

The revision claims bounded live host source structures, not immediate OS page return.

## 21. BP-Delta-K generation preservation

Existing ownership remains:

```text
SOURCE:
  graph generation
  plan generation
  pre-update source generation

TARGET:
  post-update optimizer generation
  post-update BP generation
```

For GEN6 -> GEN7, the expected relationship remains:

```text
source_optimizer_generation=6
target_optimizer_generation=7
graph_optimizer_generation=6
plan_optimizer_generation=6
post_update_optimizer_generation=7
post_update_bp_generation=7
```

No generation repair or rewrite is introduced.

## 22. Failure and durability boundary

The revision remains fail-stop. If failure occurs before durable promotion:

```text
no partial durable promotion
immutable durable source remains restart authority
```

No transactional rollback of all in-memory mutations is claimed.

## 23. Static gate

Static validation must prove at least:

```text
new source retirement env exists
candidate-retirement parent is required
admitted scheduler source scratch is Vec::new
legacy full pack is isolated to non-admitted route
resident current weight is source authority
Atlas page owns source-pack bound
BoundedPack uses fallible source allocation
source pack capacity gate exists
BP-Delta-K observer has WaveTiles source mode
candidate tiles commit to successor builder
successor prewrites are verified during sequential append
candidate full-host closure remains intact
RAM36 36 GiB hard limit is unchanged
historical 1,044,033,536-byte owner is not falsely claimed
no disk spill/mmap/manual-GC/mode-mutation workaround exists
```

Required static PASS:

```text
PASS_ASH_BASETRAIN_TENSORCUBE_MUON_ATLAS_WAVE_SOURCE_PACKING_FULL_HOST_SCRATCH_RETIREMENT_R1_STATIC
```

## 24. Focused tests

Required focused behavior includes sparse successor prewrite followed by exact sequential append verification and exact final coverage/digest, overlap rejection for random prewrites, and preservation of the parent streaming digest parity fixture.

## 25. Physical acceptance

A fresh physical N8 run using a fresh release binary, fresh Consumer CF1 authority, and fresh cross-release authority must show:

```text
full_source_scratch_allocation_count=0
source_scratch_reused_in_place=false
source_scratch_retired=true
source_bounded_pack_binding_count>0
maximum_source_wave_pack_live_bytes <= atlas_page_bytes
cross_wave_full_source_pack_accumulation_count=0
source_coverage_exact=true
```

and preserve candidate full-host retirement, BP-Delta-K target generation binding, and RAM36 successor physical-allocation ownership PASS receipts.

`N8_EXIT=0` is not required to close this local revision if a later, independently attributed first failure appears.

## 26. Forbidden repairs

```text
No RAM36 hard-limit increase
No PrivateUsage discount
No source full-scratch rename
No full source clone
No full source mmap
No disk spill
No emergency full gather
No emergency wave resize
No source/candidate alias reintroduction
No full candidate aggregate reintroduction
No BP-Delta-K replay reintroduction
No generation rewrite
No parameter reordering
No Physical N2 mutation
No RAM36 parent replacement
No silent runtime mode mutation
No manual GC correctness dependency
```

## 27. Non-claims

This revision does not claim that the historical 1,044,033,536-byte allocation owner is already proven, that zero-copy source streaming is implemented in R1, that all host memory pressure is solved, that Windows `PrivateUsage` immediately decreases after every wave, that persistent current/successor weights are themselves wave-streamed, that all allocator fragmentation is eliminated, or that N8/GEN13 necessarily completes.

## 28. Exact claim boundary

This revision claims only:

```text
Muon production source preparation no longer requires a
full-cardinality host packed source scratch when the R1 admission is active.

Current ResidentWeightPack remains source truth.

Source host packs are Atlas-bounded BoundedPack projections.

Muon candidate tiles commit directly into the already physically allocated
successor ResidentWeightPack authority rather than reusing the source scratch.

Bounded pending source evidence remains explicitly measured and does not
constitute a full source-pack fallback.

The previously closed candidate, BP-Delta-K, RAM36 projection, and successor
physical-allocation axes remain closed.
```
