# `ASH-BASETRAIN-TENSORCUBE-LOCAL-MUON-X-PAD17-WORKGROUP-BANK-CONFLICT-REDUCTION-R1`

## 1. Purpose

This revision changes only the workgroup-private physical layout of the Local Muon Newton-Schulz `x` matrix.

```text
logical Local Muon matrix     = 16 x 16
logical x elements            = 256
physical workgroup x layout   = 16 x 17
physical x elements           = 272
padding elements              = 16
padding bytes                 = 64
workgroup invocations         = 256
```

The optimization target is the column-stride access pattern in the first Newton-Schulz matrix product. The R1 implementation changes the workgroup leading dimension for `x` from 16 to 17 so column-selected reads no longer follow a 16-word physical stride.

This is an architecture-targeted workgroup-memory layout optimization. WGSL does not expose a universal physical bank topology contract, so this revision does not claim a universal conflict count or guaranteed speedup. Correctness authority remains logical candidate parity and padding isolation.

## 2. Parent authority

Parent SSOT is the Pass158 line through:

```text
ASH-BASETRAIN-TENSORCUBE-LOCAL-MUON-PRODUCTION-CALLSITE-ADOPTION-R1
ASH-BASETRAIN-TENSORCUBE-LOCAL-MUON-MULTI-TILE-BATCH-DISPATCH-R1
ASH-BASETRAIN-TENSORCUBE-LOCAL-MUON-OPTIMIZER-R1
TENSORCUBE-LOCAL-MUON-FIRST-CANDIDATE-ELIGIBILITY-REGISTRY-R1
CF1 Release Authority
```

Pass157 multi-tile dispatch and Pass158 production hybrid optimizer routing remain authoritative and are not replaced.

## 3. Exact scope

Only `x` changes physical workgroup representation.

```text
x          : 256 -> 272 f32, leading dimension 17
next_x     : 256 f32, unchanged
a_mat      : 256 f32, unchanged
aa_mat     : 256 f32, unchanged
b_mat      : 256 f32, unchanged
momentum   : 256 f32, unchanged
```

No global tensor, gradient, weight, momentum, candidate, checkpoint, registry, or optimizer-routing layout changes are admitted.

`PAD17` is a shader-private workgroup representation and must never escape into model or registry geometry.

## 4. Canonical index projection

The logical lane mapping remains:

```text
row = local_index / 16
col = local_index % 16
```

The physical `x` index becomes:

```text
x_index = row * 17 + col
```

The maximum logical physical index is `15 * 17 + 15 = 270`. The 16 padding slots are:

```text
row * 17 + 16, row in [0, 15]
```

Padding slots have no logical lane owner and must not participate in mathematical input, normalization, Newton-Schulz products, recurrence, candidate output, or momentum state.

## 5. Newton-Schulz rebinding

Initial `x` population is written through the PAD17 index.

The first matrix product remains mathematically:

```text
A = X X^T
```

but both `x` operands use physical leading dimension 17:

```text
x[row * 17 + k] * x[col * 17 + k]
```

`A`, `A^2`, and `B` remain packed 16x16 matrices.

The `B X` product keeps packed `B` addressing and uses PAD17 only for the `x` operand:

```text
b_mat[row * 16 + k] * x[k * 17 + col]
```

The Newton-Schulz recurrence remains mathematically unchanged:

```text
X_next = aX + BX
```

`next_x` remains packed 256 elements. After the existing barrier, its logical element is written back to `x[x_index]`.

The final orthogonal update is read from `x[x_index]` and emitted to the existing packed candidate/update buffers.

## 6. Norm semantics

R1 deliberately does not introduce subgroup or tree reduction. The existing lane-0 sequential norm remains the algorithmic authority so that the effect of PAD17 can be measured independently.

The loop still visits exactly 256 logical elements. Each logical ordinal is projected through:

```text
logical_row = logical / 16
logical_col = logical % 16
logical_x_index = logical_row * 17 + logical_col
```

No padding element may contribute to the norm.

Subgroup32 norm reduction and `momentum_local` retirement remain future revisions.

## 7. Mathematical non-change boundary

Pass159 must preserve:

```text
momentum recurrence
Nesterov recurrence
Newton-Schulz coefficients
Newton-Schulz iteration count
working dtype behavior
weight decay formula
candidate weight formula
candidate momentum formula
optimizer route partition
```

Required change counters are all zero:

```text
newtonSchulzFormulaChangeCount
newtonSchulzIterationChangeCount
muonMomentumFormulaChangeCount
optimizerRouteChangeCount
globalTensorLayoutChangeCount
registryGeometryChangeCount
candidateLayoutChangeCount
```

## 8. Workgroup storage accounting

The `x` workgroup allocation changes from 1,024 bytes to 1,088 bytes.

```text
xWorkgroupStorageBeforeBytes = 1024
xWorkgroupStorageAfterBytes  = 1088
xPaddingBytes                = 64
```

With the current remaining Local Muon workgroup arrays and scalar, total declared workgroup storage is 6,212 bytes.

The executor and physical harness must verify:

```text
6212 <= device.limits().max_compute_workgroup_storage_size
```

No workgroup-size reduction or alternate kernel fallback is allowed when the bound is not satisfied. Failure is fail-closed.

## 9. Production preservation

Pass159 uses the same `TensorCubeLocalMuonBatchExecutor` consumed by the Pass158 production callsite. No second production executor is introduced.

Required invariants remain:

```text
one workgroup = one logical 16x16 tile
legacyPerTileExecutorUsed = false
gradient payload readback = 0
candidate output = packed 256 elements per tile
```

Pass159 does not change the First Candidate registry, optimizer routing digest, Muon/AdamW partition, F32 Muon momentum authority, RAM36 ownership, Pass154 RAM weight residency, Pass155 VRAM cache, or Pass156 generation ordering.

## 10. Kernel revision identity

The backend exposes:

```text
TENSORCUBE_LOCAL_MUON_KERNEL_LAYOUT_REVISION = X_PAD17_R1
```

The shader source changes and therefore the old pipeline object must not be treated as byte-identical. New process construction creates the canonical PAD17 pipeline while the bind-group layout itself remains unchanged.

## 11. Physical harness

New non-N8 binary:

```text
ash_basetrain_tensorcube_local_muon_x_pad17_workgroup_bank_conflict_reduction_r1
```

Default proof geometry remains 2048 x 2048, corresponding to 16,384 logical 16x16 tiles. The harness:

1. audits all 256 logical PAD17 indices for uniqueness;
2. verifies all 16 padding slots are outside the logical set;
3. verifies live workgroup-storage limits;
4. executes the existing multi-tile GPU batch executor;
5. samples GPU candidates against the existing CPU Local Muon reference;
6. verifies no tile omission, duplicate execution, or writable alias;
7. records host-observed executor wall time without mislabeling it as GPU timestamp time.

The harness does not run N8 and does not claim a production training speedup percentage.

## 12. Receipt

Receipt schema:

```text
ash.basetrain.tensorcube_local_muon_x_pad17_workgroup_bank_conflict_reduction.v1
```

Required identity fields include:

```text
kernelLayoutRevision = X_PAD17_R1
logicalTileSide = 16
logicalTileElements = 256
xPhysicalLeadingDimension = 17
xPhysicalStorageElements = 272
xPaddingElements = 16
xPaddingBytes = 64
workgroupInvocationCount = 256
xWorkgroupStorageBeforeBytes = 1024
xWorkgroupStorageAfterBytes = 1088
totalWorkgroupStorageBytes = 6212
```

Required correctness fields include:

```text
paddingLogicalParticipationCount = 0
paddingCandidateOutputCount = 0
candidateParityFailureCount = 0
tileOmissionCount = 0
tileDuplicateExecutionCount = 0
unexpectedWritableAliasCount = 0
legacyPerTileExecutorUsed = false
```

`gpuTimestampMeasurementSupported` is false unless an actual GPU timestamp path is introduced. `hostObservedExecutorWallNs` is explicitly host-observed elapsed time.

## 13. Static validation

New validator:

```text
tools/validate_tensorcube_local_muon_x_pad17_workgroup_bank_conflict_reduction_r1_static.py
```

It verifies the PAD17 constants, x-only padded storage, logical-to-physical mapping, PAD17-aware norm, Newton-Schulz `x` reads/writes, unchanged packed A/AA/B/next-x layouts, unchanged candidate/global addressing, workgroup-storage preflight, physical harness, production executor preservation, absence of subgroup/vec4 changes, and CF1 wiring.

Existing Local Muon and Pass157 validators are updated only to recognize the new exact PAD17 `x` addressing. They retain their original mathematical and structural gates.

## 14. PASS tokens

```text
PASS_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_X_PAD17_WORKGROUP_LAYOUT_R1
PASS_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_X_PAD17_CANDIDATE_PARITY_R1
PASS_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_X_PAD17_PADDING_ISOLATION_R1
PASS_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_X_PAD17_PRODUCTION_CALLSITE_PRESERVATION_R1
PASS_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_X_PAD17_WORKGROUP_BANK_CONFLICT_REDUCTION_R1
```

## 15. Representative failures

```text
FAIL_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_X_PAD17_LOGICAL_INDEX_ALIAS
FAIL_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_X_PAD17_PADDING_PARTICIPATION
FAIL_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_X_PAD17_NORM_PADDING_CONTAMINATION
FAIL_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_X_PAD17_CANDIDATE_PARITY
FAIL_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_X_PAD17_WORKGROUP_STORAGE_LIMIT
FAIL_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_X_PAD17_GLOBAL_LAYOUT_DRIFT
FAIL_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_X_PAD17_REGISTRY_GEOMETRY_DRIFT
FAIL_ASH_BASETRAIN_TENSORCUBE_LOCAL_MUON_X_PAD17_OPTIMIZER_ROUTE_DRIFT
```

## 16. Explicit non-goals

R1 does not implement:

```text
persistent BindGroup/resource slab reuse
dynamic offsets
push constants
subgroup32 norm reduction
tree norm reduction
momentum_local retirement
vec4 Newton-Schulz matmul
A symmetry rewrite
X transpose scratch
multiple Muon batches in flight
hardware-vendor runtime branching
```

Those remain independently measurable revisions.

## 17. Final SSOT

```text
LOGICAL MATRIX                = 16 x 16
LOGICAL X ELEMENTS            = 256
X WORKGROUP PHYSICAL LAYOUT   = 16 x 17
X PHYSICAL ELEMENTS           = 272
X PHYSICAL INDEX              = row * 17 + col
PADDING PARTICIPATION         = 0
NEXT_X / A / AA / B           = packed 16 x 16
NORM LOGICAL COUNT            = 256
GLOBAL TENSOR LAYOUT          = unchanged
REGISTRY GEOMETRY             = unchanged
OPTIMIZER ROUTING             = unchanged
NEWTON-SCHULZ FORMULA         = unchanged
NEWTON-SCHULZ ITERATIONS      = unchanged
MUON MOMENTUM FORMULA         = unchanged
PASS157 BATCH EXECUTOR        = preserved
PASS158 PRODUCTION CALLSITE   = preserved
BANK CONFLICT REDUCTION       = optimization target
UNIVERSAL BANK TOPOLOGY CLAIM = none
GUARANTEED SPEEDUP            = none
CORRECTNESS AUTHORITY         = candidate parity + padding isolation
```