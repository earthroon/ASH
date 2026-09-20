# TENSORCUBE-TABLE-R2

## GPU TABLE-PARALLEL CONSUMER
## READY-ROW COMPACTION + DEVICE-SIDE MULTI-CONSUMER SCHEDULING

```text
+ R1 GPU-RESIDENT TENSOR TABLE PRESERVATION
+ GPU STATUS SCAN
+ READY-ROW COMPACTION
+ CONSUMER-SPECIFIC ROW-INDEX VIEWS

+ MUON TABLE-PARALLEL CONSUME
+ BP-DK TABLE-DERIVED CAPTURE PLAN
+ SUCCESSOR TABLE-DERIVED READY VIEW

+ DEVICE-SIDE READY COUNT
+ BOUNDED COMPACTION WORKSPACE
+ WAVE / GENERATION / TABLE-DIGEST BINDING
+ SUBMISSION-LINEAGE HANDOFF PRESERVATION

+ NO FULL TABLE READBACK
+ NO PER-PARAMETER HOST RANGE REBUILD
+ NO DUPLICATE CONSUMER JOB TABLE
+ NO HIDDEN CPU SCHEDULER FALLBACK

+ EXISTING NUMERICAL KERNEL PRESERVATION
+ B06 / BP-DK / R8A / RAM36 AUTHORITY PRESERVATION
```

## Parent

```text
TENSORCUBE-TABLE-R1
ASH_PASS3_TENSORCUBE_TABLE_R1_GPU_RESIDENT_TENSOR_TABLE_AUTHORITY_CODE_ONLY.zip
SHA-256 fbd975bae2966f7d3ef83920654a056af13731ab54338847ef920fdd5fc07950
```

R1 remains the canonical TensorCube row/geometry/source/destination authority. R2 does not create a second TensorTable.

## Core law

> Consumer readiness is derived from TensorTable lifecycle state on the device.

> The host may encode a bounded scan/consume wave, but ActiveVerified execution must not reconstruct the ready set parameter-by-parameter or read back the full table.

## R1 dependency closure

R2 adds one missing immutable SoA column to R1:

```text
route_kind[]
```

It is materialized directly from `TensorCubeConsumeParameterAuthorityR1::route_kind` and uploaded alongside the existing GPU-resident columns. No optimizer-route inference is performed in the shader.

## GPU ready views

R2 materializes bounded device-resident buffers:

```text
muon_row_indices[]
muon_count_overflow[2]

bpdk_parameter_record_indices[]
bpdk_count_overflow[2]
bpdk_seen[]

successor_row_indices[]
successor_count_overflow[2]
```

Each output contains identity only. Geometry, offsets, generations, and parameter metadata remain in TensorTable R1.

## Binding-budget decomposition

Muon, BP-DK, and successor scans are separate compute pipelines instead of one oversized bind group. The split avoids reintroducing historical storage-buffer binding pressure while preserving one TensorTable authority.

## Stable GPU compaction

R2 intentionally starts with a deterministic device-side stable scan:

```text
ascending table_row_index
→ predicate
→ compact ready identity
```

The scan uses one GPU invocation for deterministic compaction order. This is a correctness/authority closure, not a performance claim. Parallel prefix-scan is deferred to a later performance revision.

No host row enumeration participates in ActiveVerified scheduling.

## Consumer predicates

Muon:

```text
COMPUTE_DONE
AND MUON_CONSUME_READY
AND NOT MUON_CONSUMED
AND NOT FAILED
AND route_kind == MUON
```

BP-DK:

```text
BPDK_READY
AND NOT BPDK_CAPTURED
AND NOT FAILED
```

Successor:

```text
MUON_CONSUMED
AND SUCCESSOR_READY
AND NOT SUCCESSOR_PUBLISHED
AND NOT FAILED
```

BP-DK output is parameter-state scoped. Multiple TensorCube rows referencing the same `bpdk_parameter_record_index` emit exactly one compact parameter record via device-side deduplication. Successor-ready rows remain eligibility only; B06 is still the publication/ticket authority.

## Muon table-parallel consumer

R2 adds a GPU consumer driven by compact Muon row identities plus TensorTable source/destination offset columns. Candidate W, candidate M, and orthogonal update are copied bitwise as `u32` words. Each ready TensorCube row is consumed by a 256-thread workgroup. No floating-point arithmetic or numerical transformation is introduced.

The W/M/update copy passes are separated to remain within the storage-binding budget.

## Address contract

R1 stores offsets as 64-bit lo/hi pairs. R2 currently admits the exact u32-addressable physical domain only:

```text
offset + R6_TILE_ELEMENTS <= u32::MAX
```

The host checks this before scheduling, while the copy shader also rejects non-zero high words through the device overflow flag. No shader-int64 dependency is introduced.

## Bounded max dispatch

R2 does not blockingly read `ready_count` back before consumer dispatch. It uses bounded maximum dispatch plus a device-side ready-count gate. Copy workgroups are distributed over bounded 2D dispatch dimensions and slots beyond the device count return immediately.

## Lifecycle transition

After W/M/update copy passes, a dedicated status pass executes `atomicOr(MUON_CONSUMED)` only when the shared overflow flag remains zero. Lifecycle storage is treated atomically by R2.

## Overflow law

Each compact view carries `[count, overflow]`. Capacity overflow or unsupported address width sets overflow. Overflow is fail-closed: Muon lifecycle publication is suppressed and no truncation is admitted.

## Host/reference path

`TensorCubeTableReadyReferenceR2::diagnostic_from_host()` exists only for diagnostic A/B parity. Active source contract seals:

```text
scheduler_authority=GPU_TENSOR_TABLE
host_row_enumeration_count=0
host_range_rebuild_count=0
full_table_readback_count=0
ready_count_readback_count=0
legacy_host_scheduler_used=false
```

These remain source-contract fields until physical runtime evidence exists.

## Table/generation binding

The scheduler binds exact `table_digest`, `source_generation`, `target_generation`, and `row_capacity`, and rejects drift before consumer encoding. No ready view may be rebound to another TensorTable generation.

## BP-DK / B06 boundary

R2 creates the GPU-derived compact BP-DK parameter-record buffer required for checkpoint planning but does not alter filesystem durability, checkpoint manifest/SHA authority, pending-generation transactionality, or commit/abort semantics.

R2 does not synthesize or claim B06 tickets. Existing B06 completeness, physical-completion, and submission-lineage gates remain unchanged.

## Numerical preservation

R2 changes work discovery and byte movement only. It does not change Muon orthogonalization/scaling, momentum/weight update math, BP-DK delta math, or R8A digest math. No second full W/M/update allocation is introduced.

## Changed files

```text
MOD crates/base_train/src/lib.rs
MOD crates/base_train/src/tensorcube_table_r1.rs
ADD crates/base_train/src/tensorcube_table_parallel_consumer_r2.rs
ADD crates/base_train/src/shaders/tensorcube_table_muon_scan_r2.wgsl
ADD crates/base_train/src/shaders/tensorcube_table_bpdk_scan_r2.wgsl
ADD crates/base_train/src/shaders/tensorcube_table_successor_scan_r2.wgsl
ADD crates/base_train/src/shaders/tensorcube_table_muon_copy_r2.wgsl
ADD crates/base_train/src/shaders/tensorcube_table_status_transition_r2.wgsl
ADD tools/validate_ash_tensorcube_table_r2_gpu_parallel_consumer_static.py
```

Delta: MOD 2 / ADD 7 / DEL 0.

## Static qualification

```text
PASS_TENSORCUBE_TABLE_R2_GPU_PARALLEL_CONSUMER_STATIC checks=28
PASS_TENSORCUBE_TABLE_R1_STATIC checks=20
PASS_TENSORCUBE_CONSUME_R2_GPU_PARALLEL_PLANE_STATIC checks=61
PASS_TENSORCUBE_CONSUME_R1_RELATION_AUTHORITY_STATIC checks=56
PYTHON_VALIDATOR_COMPILE_PASS
```

Bake environment:

```text
RUST_TOOLCHAIN=UNAVAILABLE
COMPILE=NOT_RUN
RUNTIME=NOT_RUN
PHYSICAL=NOT_RUN
PERFORMANCE=UNMEASURED
PROMOTED=NO
```

No compile/runtime/physical/performance claim is made by this bake.

## Artifacts

```text
ASH_TENSORCUBE_TABLE_R2_GPU_PARALLEL_CONSUMER_OVERLAY_CODE_ONLY.zip
SHA-256 a821473e00afcb220e7dd9de971205947c0e16bc24ef4c477506d8199eb44e73
FILES 9
CRC PASS

ASH_PASS3_TENSORCUBE_TABLE_R2_GPU_PARALLEL_CONSUMER_CODE_ONLY.zip
SHA-256 1a58e13d5872946f37959b57b6c304ee8c1477128a111bd86c3a52c99e40cdd4
FILES 8459
CRC PASS
```

## Compile acceptance

First local gate:

```text
cargo test -p base_train --lib tensorcube_table_r2_
```

Full relevant library compile/test plus current WGSL/Naga validation must pass before any runtime claim.

## Physical acceptance target

Physical promotion requires exact GPU ready-set parity, BP-DK parameter-set parity, Muon destination byte parity, zero compaction/address overflow, zero full-table readback, zero host row enumeration/range rebuild, no hidden legacy scheduler fallback, and preserved B06 gates.

Performance promotion additionally requires measured scan/compact/copy timing. The current stable serial GPU scan is not claimed as the final performance implementation.

## Final law

> R1 made TensorCube a row in a GPU-resident TensorTable. R2 makes device lifecycle state the scheduling source for that table.

> The GPU deterministically compacts Muon rows, BP-DK parameter records, and successor rows without a full-table host readback. Muon W/M/update movement is then performed from compact row identity by parallel GPU workgroups with bitwise-preserving copies.

> R2 does not weaken BP-DK durability, B06 successor publication, RAM36 residency, R8A identity, or generation authorities. Ready identity is scheduling evidence, not transaction publication authority.
