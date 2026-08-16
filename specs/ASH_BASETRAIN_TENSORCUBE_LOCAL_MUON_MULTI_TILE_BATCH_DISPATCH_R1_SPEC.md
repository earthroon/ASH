# `ASH-BASETRAIN-TENSORCUBE-LOCAL-MUON-MULTI-TILE-BATCH-DISPATCH-R1`

## TensorCube Local Muon Multi-Tile Physical Executor / Batched Workgroup Dispatch

```text
ASH-BASETRAIN-TENSORCUBE-LOCAL-MUON-MULTI-TILE-BATCH-DISPATCH-R1

One Workgroup Per 16x16 Tile /
Multi-Tile Workgroup Dispatch /
Per-Tile GPU Transaction Retirement /
Canonical Tile Descriptor Projection /
Device-Limit-Bounded Physical Batching /
Bulk Candidate Readback /
Deterministic Tile Scatter /
No Muon Math Change /
No Newton-Schulz Math Change /
No Momentum Math Change
```

Receipt schema:

```text
ash.basetrain.tensorcube_local_muon_multi_tile_batch_dispatch.v1
```

## 1. Parent authority

Parent implementation authority is the Pass156 line through:

```text
ASH-BASETRAIN-GPU-SUCCESSOR-WEIGHT-COMMIT-CONTINUITY-R1
ASH-BASETRAIN-VRAM-HOT-WEIGHT-PAGE-RESIDENCY-R1
ASH-BASETRAIN-RAM-WEIGHT-PACK-PERSISTENT-RESIDENCY-AND-ATLAS-READAHEAD-R1
ASH-BASETRAIN-TENSORCUBE-LOCAL-MUON-OPTIMIZER-R1
ASH-BASETRAIN-TENSORCUBE-LOCAL-MUON-FIRST-CANDIDATE-REGISTRY-R1
CF1 Release Profile Authority
```

This revision changes host/GPU execution granularity only. It does not change the Local Muon formula, Newton-Schulz iteration count, momentum recurrence, working dtype, candidate weight formula, registry geometry, or optimizer commit semantics.

## 2. Parent physical truth

The parent Local Muon backend exposed a single-tile ABI whose physical kernel execution was:

```text
one 16x16 tile
-> pipeline/bind resources
-> dispatch_workgroups(1, 1, 1)
-> submit
-> poll wait
-> candidate/momentum/update/status readback
```

A 2048 x 2048 parameter contains:

```text
128 x 128 = 16,384 tiles
```

Executing that geometry as 16,384 independent host GPU transactions is the overhead targeted by R1.

## 3. Critical scope correction

The Pass156 production training path does not yet contain a live Local Muon optimizer callsite. The Local Muon backend exists as a candidate ABI plus registry/reference authority.

Therefore R1 does **not** claim that the current production BaseTrain wall time is already improved.

R1 physically closes the batch-capable executor and harness first and emits:

```text
HOLD_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_MULTI_TILE_PRODUCTION_CALLSITE_NOT_PRESENT_R1
```

until a later revision binds the executor to an admitted production Local Muon route.

No hidden callsite or fabricated production speedup is permitted.

## 4. Canonical tile geometry

Tile geometry remains exactly:

```text
16 rows x 16 columns
256 invocations
one workgroup = one tile
```

The canonical registry remains authoritative for logical geometry, including:

```text
element_offset
row_start
col_start
row_stride_elements
tensor_cube_id
plane_identity
```

The existing registry statement remains authoritative:

```text
Logical row-major top-left element offset.
This is not a contiguous 256-element claim.
```

## 5. GPU descriptor projection

R1 introduces a GPU-safe descriptor projection. It is not a new geometry SSOT.

Each physical tile descriptor carries at least:

```text
tile ordinal
gradient base offset
gradient row stride
packed batch input/output base
per-tile status base
```

Gradient indexing is:

```text
desc.gradient_base_offset_elements
+ row * desc.gradient_row_stride_elements
+ col
```

Source weight/momentum and candidate outputs may use packed contiguous 256-element batch staging because those buffers are temporary execution projections, not canonical model layout authorities.

## 6. WGSL workgroup mapping

The canonical batch-capable shader uses `@builtin(workgroup_id)` and computes:

```text
local_tile = workgroup_id.y * dispatch_x + workgroup_id.x
```

Padded workgroups satisfy:

```text
local_tile >= tile_count
-> uniform workgroup early return
```

The return occurs before every `workgroupBarrier()`.

Because `local_tile` depends only on `workgroup_id`, every invocation in the workgroup takes the same branch.

## 7. 1D and 2D dispatch

If a physical batch fits the device X workgroup limit:

```text
dispatch_x = tile_count
dispatch_y = 1
```

Otherwise R1 uses deterministic 2D flattening:

```text
dispatch_x = min(tile_count, max_compute_workgroups_per_dimension)
dispatch_y = ceil(tile_count / dispatch_x)
```

and requires:

```text
dispatch_y <= max_compute_workgroups_per_dimension
```

No universal hardcoded 65,535 value is the runtime authority. The live WGPU device limit is authoritative.

## 8. Device-limit-bounded physical batch sizing

The executor derives its maximum physical batch from the minimum of:

```text
workgroup dispatch capacity
weight storage binding capacity
momentum storage binding capacity
candidate storage binding capacity
descriptor storage binding capacity
status storage binding capacity
max_buffer_size
```

All byte/element multiplication and range arithmetic is checked.

If the logical tile set does not fit one physical batch, R1 uses bounded chunks. It never falls back to one GPU transaction per tile merely because one giant batch is impossible.

## 9. Pipeline authority

R1 introduces `TensorCubeLocalMuonBatchExecutor`.

The shader module, bind group layout, pipeline layout, and compute pipeline are constructed once per executor instance.

The executor can execute one or more physical batches without rebuilding the compute pipeline for every tile.

The existing single-tile ABI is preserved for compatibility but now routes through the batch-capable implementation using one tile.

There is no second copy of the Local Muon mathematical kernel.

## 10. Physical batch transaction

One physical batch performs:

```text
build descriptor array
build packed source weight buffer
build packed source momentum buffer
bind existing gradient source buffer
allocate bounded candidate outputs
build one bind group
build one command encoder
one compute pass
dispatch_workgroups(dispatch_x, dispatch_y, 1)
bulk copies to four readback buffers
one queue submit
four map_async requests
one device poll wait
bulk host decode
```

Expected counts per physical batch:

```text
dispatch count = 1
queue submit count = 1
poll wait count = 1
readback buffer count = 4
```

## 11. Per-tile status and atomic failure

Status remains tile-local:

```text
status[tile * 2 + 0] = nonfinite/error count
status[tile * 2 + 1] = completion count
```

Each valid tile must finish with:

```text
nonfinite = 0
completion = 1
```

A failed tile prevents the physical harness from declaring parity/coverage PASS.

No partial model commit semantics are introduced by batching.

## 12. Workgroup memory isolation

Existing workgroup arrays remain workgroup-local:

```text
x
next_x
a_mat
aa_mat
b_mat
momentum_local
norm_inv
```

No cross-tile workgroup state, cross-tile barrier, or cross-tile reduction is introduced.

## 13. Mathematical non-change boundary

R1 preserves the exact existing operations for:

```text
momentum recurrence
Nesterov branch
sequential 256-element norm reduction
Newton-Schulz A = X X^T
A^2
B = bA + cA^2
X recurrence
weight decay and candidate update
BF16-emulated working projection
```

R1 does not yet introduce subgroup norm reduction, workgroup tree reduction, vec4 matmul storage, matrix transpose scratch, or subgroupShuffle matmul.

## 14. Gradient payload authority

The gradient remains an existing raw WGPU buffer lease.

R1 does not read the gradient payload back to CPU merely to batch the tiles.

Required counters:

```text
gradientPayloadReadbackCount = 0
gradientPayloadReadbackBytes = 0
```

## 15. Deterministic output ordering

Batch output is packed by canonical logical tile ordinal.

The physical GPU completion timing never determines logical output identity.

Required invariants:

```text
workgroupCount = logicalTileCount
tileOmissionCount = 0
tileDuplicateExecutionCount = 0
unexpectedWritableAliasCount = 0
```

## 16. Physical harness

R1 adds:

```text
ash_basetrain_tensorcube_local_muon_multi_tile_batch_dispatch_r1
```

Default proof geometry:

```text
matrix side = 2048
tile side = 16
tiles per row = 128
logical tile count = 16,384
```

The harness creates deterministic synthetic gradient/weight/momentum payloads on the existing WGPU device, executes the batch executor, verifies all tile completion statuses, and compares sampled GPU candidates against the existing CPU Local Muon reference.

The default parity sample count is 8, spread deterministically over the logical tile range.

## 17. Harness receipt

Required output includes logical tile count, physical batch count, tiles-per-batch bounds, dispatch/workgroup counts, pipeline/bind/encoder/submit/wait counts, upload/readback byte counts, tile omission/duplication/alias counts, parity sample/failure counts, wall time, reduction ratios, and the production callsite adoption state.

## 18. 2048 x 2048 ideal target

If live device binding/workgroup limits admit the entire payload in one physical batch, expected evidence is:

```text
logicalTileCount = 16,384
physicalBatchCount = 1
dispatchCount = 1
workgroupCount = 16,384
pipelineBuildCount = 1
queueSubmitCount = 1
pollWaitCount = 1
```

If the live device requires multiple bounded batches, a larger dispatch count is valid as long as it remains device-limit-derived and every logical tile executes exactly once.

Correctness does not require `dispatchCount == 1` on every adapter.

## 19. Physical PASS tokens

```text
PASS_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_MULTI_TILE_BATCH_DISPATCH_R1
PASS_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_BATCH_TILE_COVERAGE_R1
PASS_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_DEVICE_LIMIT_BOUNDED_BATCH_R1
PASS_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_BATCH_CANDIDATE_PARITY_R1
```

Production adoption remains:

```text
HOLD_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_MULTI_TILE_PRODUCTION_CALLSITE_NOT_PRESENT_R1
```

until an explicit later production route adoption revision.

## 20. Static validator

New validator:

```text
tools/validate_tensorcube_local_muon_multi_tile_batch_dispatch_r1_static.py
```

It is appended to the CF1 validator chain and verifies the batch executor, descriptor addressing, device-limit bounds, 2D dispatch, bulk readback, physical harness, mathematical non-change boundary, and honest production HOLD.

Parent Local Muon validators are updated only where their old textual checks referred directly to single-tile shader addressing. Their original semantic gates remain unchanged.

## 21. Non-goals

R1 does not implement production Local Muon route adoption, subgroup norm reduction, NS matmul vectorization, subgroup shuffle matmul, cross-parameter batching, multiple physical batches in flight, asynchronous queue overlap, new optimizer math, new momentum math, or checkpoint semantic changes.

## 22. Final SSOT

```text
CANONICAL TILE GEOMETRY
= existing Local Muon registry

TILE SIZE
= 16 x 16

INVOCATIONS
= 256 per workgroup

ONE WORKGROUP
= one canonical tile

OLD PHYSICAL GRANULARITY
= one GPU transaction per tile

NEW PHYSICAL GRANULARITY
= many tiles per device-limit-bounded batch

WORKGROUP TILE IDENTITY
= workgroup_id -> descriptor

GRADIENT ADDRESS
= descriptor base + row * canonical stride + col

PIPELINE
= executor-level, not per tile

BIND GROUP
= physical-batch level

QUEUE SUBMIT
= physical-batch level

POLL WAIT
= physical-batch level

READBACK
= bulk physical-batch level

TILE OMISSION
= 0

TILE DUPLICATION
= 0

WRITABLE ALIAS
= 0

GRADIENT PAYLOAD READBACK
= 0

LOCAL MUON MATH CHANGE
= 0

NEWTON-SCHULZ MATH CHANGE
= 0

MOMENTUM MATH CHANGE
= 0

PRODUCTION TRAINING CALLSITE ADOPTED
= false in R1 parent topology
```