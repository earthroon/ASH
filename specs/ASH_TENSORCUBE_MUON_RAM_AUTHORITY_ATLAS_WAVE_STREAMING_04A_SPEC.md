# ASH-TENSORCUBE-MUON-RAM-AUTHORITY-ATLAS-WAVE-STREAMING-04A

## 0. Status and parent

- Patch ID: `ASH-TENSORCUBE-MUON-RAM-AUTHORITY-ATLAS-WAVE-STREAMING-04A`
- Parent semantic authority: `ASH-TENSORCUBE-MUON-RESIDENT-STATE-GRAPH-04`
- Physical transport authority: the existing N8 RAM-resident weight / RAM-resident Adam M/V / device-limit-aware Atlas projection route.
- Transport revision: `RAM_AUTHORITY_ATLAS_WAVE_V1`.
- 04A supersedes B04 whole-model GPU physical residency. It preserves B04 generation identity, candidate isolation, ownership, rollback, B05/B06/C07/C08 boundaries, and D10A authority classification.

## 1. Required state ownership

Long-lived live training authority is physical RAM:

```text
Canonical Weight Generation
Adam M
Adam V
Muon Momentum
Successor Weight Generation
Successor Adam State
Successor Muon Momentum
Ownership / Routing / Generation Metadata
```

GPU authority is transient only:

```text
Current Atlas Weight Wave
Current Optimizer-State Companion Wave
Wave Candidate Weight
Wave Candidate Optimizer State
Orthogonal / Update Scratch
Compact Evidence Scratch
```

Disk authority remains durable checkpoint/publication. Therefore:

```text
RAM = live canonical authority
GPU = transient wave working set
Disk = durable publication authority
```

## 2. Whole-model GPU residency retirement

The parent physical design that admitted or allocated all Muon elements as five simultaneous F32 surfaces is retired.

The following is forbidden as an Active 04A admission rule:

```text
total_muon_elements * sizeof(F32) * 5 <= GPU budget
```

The following physical objects must not exist as whole-model Active authorities:

```text
whole committed weight GPU buffer
whole candidate weight GPU buffer
whole committed Muon momentum GPU buffer
whole candidate Muon momentum GPU buffer
whole update scratch GPU buffer
whole-model Adam M/V GPU cache
```

`wholeGraphCapacityPreflightCount`, `wholeGraphAllocationAttemptCount`, `wholeModelGpuWeightResidentBytes`, and `wholeModelGpuOptimizerResidentBytes` must all remain zero in 04A physical qualification.

## 3. Existing Atlas projection SSOT

04A does not create a second paging subsystem. It adopts the existing BaseTrain Atlas geometry and route as SSOT:

```text
R6A_R2_MICRO_ATLAS_PAGE_BYTES = 16 MiB
R6A_R2_RING_SLOT_COUNT = 3
```

These values are consumed from `device_limit_aware_micro_atlas_vocab_row_paging`; B04A must not duplicate them as independent constants.

Canonical address flow is:

```text
Canonical Parameter Address
 -> Ownership Registry
 -> Model Projection
 -> Atlas Segment / Wave
 -> Physical transient GPU lease
```

A physical slot address is never a canonical semantic address.

## 4. Physical-RAM canonical weight authority

For optimizer step `G -> G+1`, `CanonicalWeight[G]` is immutable source authority in RAM. The GPU receives only the current Atlas wave projection. Accepted candidate results are written to the existing RAM successor generation authority. The source generation cannot be mutated in place.

```text
RAM CanonicalWeight[G]
 -> Atlas wave projection
 -> GPU transient compute
 -> accepted candidate range
 -> RAM SuccessorWeight[G+1]
```

A wave acceptance is not a generation promotion.

## 5. Physical-RAM Adam M/V authority

Existing N8 RAM-resident Adam M/V is retained. 04A must not create persistent GPU Adam M/V authority. An Adam-owned wave may transiently project exact W/M/V ranges, compute candidate W/M/V, and return accepted candidate state to RAM successor authority.

The same canonical Weight/M/V range identity is mandatory.

## 6. Physical-RAM Muon momentum authority

The existing BaseTrain Muon momentum vector and its existing RAM36 exact-inventory registration remain the single live momentum lineage. 04A must not create a second canonical momentum store.

```text
RAM Canonical Muon Momentum
 -> exact wave projection
 -> GPU candidate momentum
 -> accepted candidate range
 -> RAM successor Muon Momentum
```

`LOCAL`, `FUSED_RIGHT`, and `FUSED_DOWN` consume the same canonical momentum lineage.

## 7. Transient GPU wave working set

For a Muon wave the transient set is bounded to the currently admitted Atlas physical batch:

```text
Weight source chunk
Muon momentum source chunk
Candidate weight chunk
Candidate momentum chunk
Orthogonal/update scratch
optional compact evidence/control
```

For each source/candidate/scratch surface, the physical batch is capped by the existing Atlas page geometry. Total model size is not a VRAM admission variable.

An optional `ASH_MUON_RESIDENT_STATE_BUDGET_BYTES` is interpreted only as a transient wave working-set bound. It cannot revive whole-graph admission.

## 8. Triple-buffer geometry and actual concurrency

04A binds every physical batch to the existing three-slot Atlas ring identity. Physical identity includes at least:

```text
semantic partition
wave ordinal
slot ordinal
slot incarnation / lease
source generation
candidate generation
canonical range
```

Mirror qualification may retain exact waits for parity. Therefore 04A claims adoption of three-slot geometry and legal temporal slot reuse, not three simultaneously in-flight Muon waves. True overlap is a C08 Active physical-qualification claim.

## 9. A01 / A02 / A03 lifetime authority

A01 exact submission epochs remain the lifetime authority. Logical wave completion alone cannot make a slot reusable.

A02 remains the reusable transient buffer allocator. Candidate W/M/update and related wave scratch must satisfy A02 reclaim conditions including `RetiredComplete`, ownership, exact tracking, unmapped state, no pending queue writes, and no overlap.

A03 remains staging/compact-readback authority. 04A must not introduce an uncontrolled second upload/readback pool.

## 10. Wave-scoped B04 semantic ledger

Active B04A holds semantic candidate ledgers, not whole-model GPU buffers. `prepare_atlas_wave_partition` records generation/ownership/partition identity. Each physical batch is recorded against that semantic partition. The semantic partition is complete only after at least one admitted physical batch finishes.

The legacy whole-resident allocation route is forbidden from the 04A Active path.

## 11. Wave-scoped B05 candidate backing

A B05 candidate backing represents one transient Atlas wave window, not an entire semantic Local/Fused partition.

It binds:

```text
partition kind
semantic partition identity
partitionElementStart
elementCount
source generation
candidate generation
physical allocation identities
wave/slot identity
```

Multiple backing windows may cover one semantic Local/Fused partition. They must be contiguous and exact with no gap or duplicate.

B05 keeps three distinct authorities:

```text
canonical Muon packed address
canonical model projection address
physical transient Atlas-wave address
```

Address collapse is forbidden.

## 12. Temporal physical reuse

A02 may legally recycle the same `PhysicalAllocationId` for a later wave only after A01 retirement/reclaim. B05 physical-overlap validation must therefore include wave/partition lease identity, rather than treating allocation-ID reuse across different retired waves as simultaneous overlap.

Within one live wave, candidate weight, candidate momentum, and update scratch remain physically disjoint.

## 13. LOCAL / FUSED ownership

```text
LOCAL -> Local Muon
FUSED_RIGHT -> HiMuon
FUSED_DOWN -> HiMuon
```

Atlas segmentation is downstream of canonical ownership. It cannot change optimizer ownership or create a second routing authority.

Fused pair semantics remain canonical even when physical batches split the full semantic fused set into multiple transient windows.

## 14. RAM successor and full-coverage generation transaction

Each accepted wave writes only its canonical range into the existing RAM successor generation. Full promotion requires exact whole-generation coverage:

```text
planned elements == RAM-successor committed elements
missing = 0
duplicate = 0
Muon/AdamW overlap = 0
unclassified = 0
physical writes == planned ownership
```

All wave candidates are children of one full-generation attempt. No wave can autonomously promote the generation.

## 15. B06 boundary

B06 remains the full-trainable-generation commit authority. 04A/B05 produce wave-scoped physical candidates and RAM successor coverage. Only after all mandatory coverage/evidence is complete may B06 PREPARE run. After all fallible checks pass, B06 COMMIT is the single generation promotion point.

One optimizer step performs exactly one canonical generation promotion.

B06 Active `DeviceSegmentedGenerationV1` adoption is not claimed by 04A and remains a later full-Active blocker.

## 16. C07 evidence boundary

C07 must ultimately reduce deterministic compact evidence across canonical wave order rather than requiring whole-model GPU candidate residency. Completion order and evidence reduction order are distinct.

04A closes transport compatibility for wave-scoped candidate backings. It does not by itself claim that every final C07 incremental full-generation evidence path is physically qualified. D10A Mirror still requires actual candidate evidence and host witness parity before Mirror PASS.

## 17. C08 boundary

C08 owns callback completion, mailbox progress, async map lifetime and deferred retirement. Mirror may retain exact waits as parity authority. The 04A source path must remain compatible with later ActiveAsync overlap without making callback code mutate canonical RAM authority directly.

## 18. RAM36 exact inventory

Existing RAM resident weight, Adam M/V, and Muon momentum authorities must remain in the RAM36 inventory. New duplicate full-model Vec shadows are forbidden. A new long-lived payload, if ever introduced, requires exact byte count, owner, lifetime and release accounting before admission.

RAM pressure must not silently fall back to per-wave disk streaming.

## 19. Deferred durability

04A preserves N8 deferred durable writeback:

```text
intermediate steps: no durable full-pack publication
final configured boundary: durable publication
```

Wave completion and RAM canonical generation promotion are not disk-publication events.

## 20. Telemetry and qualification

Mandatory 04A telemetry includes:

```text
atlasWavePartitionCount
atlasWavePhysicalBatchCount
atlasWaveTransientRequestedBytes
atlasWavePeakTransientBytes
wholeGraphCapacityPreflightCount
wholeGraphAllocationAttemptCount
wholeModelGpuWeightResidentBytes
wholeModelGpuOptimizerResidentBytes
```

Physical 04A PASS requires real Muon wave execution and:

```text
atlasWavePartitionCount > 0
atlasWavePhysicalBatchCount > 0
wholeGraphCapacityPreflightCount = 0
wholeGraphAllocationAttemptCount = 0
wholeModelGpuWeightResidentBytes = 0
wholeModelGpuOptimizerResidentBytes = 0
```

It must additionally preserve A01/A02/A03 invariants and RAM36 exact inventory.

## 21. D10A compatibility

D10A exact Mirror authority remains:

```text
B04 ACTIVE_VERIFIED
B05 MIRROR_VERIFIED
B06 MIRROR_VERIFIED
C07 MIRROR_VERIFIED
C08 MIRROR_VERIFIED
```

The semantic mode name is retained to avoid authority-class churn, while the physical transport revision is explicitly bound as `RAM_AUTHORITY_ATLAS_WAVE_V1` in the D10A execution receipt.

A D10A Mirror PASS additionally requires the 04A zero-whole-residency conditions.

## 22. Failure policy

Mandatory failures include, as applicable:

```text
FAIL_B04A_ATLAS_GEOMETRY_MISSING
FAIL_B04A_ATLAS_GEOMETRY_DRIFT
FAIL_B04A_ATLAS_WAVE_RANGE_MISMATCH
HOLD_B04A_ATLAS_WAVE_CAPACITY_UNSATISFIABLE
FAIL_B04A_WHOLE_MODEL_GPU_WEIGHT_RESIDENCY
FAIL_B04A_WHOLE_MODEL_GPU_OPTIMIZER_RESIDENCY
FAIL_B04A_SECOND_MOMENTUM_LINEAGE
FAIL_B04A_SOURCE_GENERATION_MUTATION
FAIL_B04A_SUCCESSOR_DUPLICATE_WRITE
FAIL_B04A_SUCCESSOR_MISSING_COVERAGE
FAIL_B04A_PARTIAL_GENERATION_PROMOTION
```

No silent fallback to the old whole-resident graph is permitted in Active 04A.

## 23. Static/source closure

Static validation must inspect exact struct/function/callsite scopes and prove at minimum:

```text
04A patch/schema/transport revision
whole-graph required bytes fixed at zero
old whole-graph size formula not used by Active construction
existing Atlas page/ring constants are consumed from BaseTrain SSOT
Local and Fused physical batches are page-capped
source W/M are supplied from RAM on every Active wave
A01 tracked submit/wait/release remains
A02 transient candidate allocation/reclaim remains
A03 upload/compact-readback remains
wave backing carries semantic offset and wave/slot identity
B05 accepts exact multiple contiguous wave windows
RAM Muon momentum authority/inventory remains singular
D10A receipt binds 04A transport and zero whole-residency counters
WGSL tree is unchanged from D10A parent
```

## 24. Required gates

Source closure requires:

```text
PASS_ASH_TENSORCUBE_MUON_RAM_AUTHORITY_ATLAS_WAVE_STREAMING_04A_STATIC
cargo check -p burn_webgpu_backend
cargo check -p base_train
cargo build -p base_train --release
```

Physical transport qualification later requires:

```text
PASS_ASH_TENSORCUBE_MUON_RAM_AUTHORITY_ATLAS_WAVE_STREAMING_04A_PHYSICAL
```

04A source/static success must not be described as physical GPU qualification.

## 25. Non-goals

04A does not:

```text
introduce mixed precision
change optimizer math
create new Adam ownership
create a second Muon momentum lineage
mint a D09 permit
publish D10
claim B06 Active device AdamW adoption
claim C08 Active overlap
claim physical performance improvement before measurement
```

## 26. Final state flow

```text
Physical RAM Canonical G
        |
        | existing Atlas projection
        v
Transient GPU Wave / Slot
        |
        | Local or HiMuon compute
        v
Wave Candidate + Evidence
        |
        | accepted exact range
        v
Physical RAM Successor G+1
        |
        | repeat all canonical ownership ranges
        v
Full Coverage Exact
        |
        v
B06 PREPARE -> B06 COMMIT
        |
        v
Physical RAM Canonical G+1
```

04A's central invariant is: **the whole training state lives in physical RAM; the GPU borrows only the current Atlas wave and returns the accepted result.**
