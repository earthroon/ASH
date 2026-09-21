# TENSORCUBE-TABLE-R2A

## PARALLEL PREFIX COMPACTION + INDIRECT DISPATCH PERFORMANCE CLOSURE

```text
+ R2 GPU SCHEDULER AUTHORITY PRESERVATION
+ PARALLEL READY-PREDICATE EVALUATION
+ WORKGROUP-LOCAL PREFIX SCAN
+ RECURSIVE GROUP-OFFSET SCAN
+ STABLE READY-ROW COMPACTION

+ DEVICE-RESIDENT READY COUNT
+ GPU INDIRECT DISPATCH ARG GENERATION
+ NO READY-COUNT HOST ROUNDTRIP
+ NO BOUNDED-MAX OVERDISPATCH AS R2A TARGET

+ MUON PARALLEL COMPACTION
+ BP-DK PARAMETER-PLANE DEDUP + COMPACTION
+ SUCCESSOR PARALLEL COMPACTION

+ R2 SERIAL-GPU SCAN REFERENCE PRESERVATION
+ ZERO HOST ENUMERATION
+ ZERO HOST RANGE REBUILD
+ ZERO FULL TABLE READBACK
+ NO NUMERICAL CHANGE
```

## Parent

```text
TENSORCUBE-TABLE-R2
ASH_PASS3_TENSORCUBE_TABLE_R2_GPU_PARALLEL_CONSUMER_CODE_ONLY.zip
SHA-256 1a58e13d5872946f37959b57b6c304ee8c1477128a111bd86c3a52c99e40cdd4
```

R2 remains the semantic scheduler authority and exact reference oracle. R2A changes the ready-set implementation from a serial GPU scan to stable parallel GPU compaction and device-generated indirect dispatch.

## Core law

For one immutable TensorTable/lifecycle snapshot:

```text
R2 serial GPU ready identity
==
R2A parallel GPU ready identity
```

R2A may change scheduling cost. It may not change readiness semantics, row order, BP-DK parameter identity, numerical tensor values, successor publication authority, or generation identity.

## Parallel compaction pipeline

Each row/parameter plane follows:

```text
PASS A
predicate + 256-lane workgroup-local exclusive prefix
        ↓
level-0 group counts
        ↓
recursive group-count scans
        ↓
parent-offset propagation
        ↓
stable scatter
        ↓
compact ready identity
        ↓
device ready_count
        ↓
indirect dispatch args
```

The output ordering is stable ascending input identity. No unordered global atomic-append list is used as compaction authority.

## Recursive scan

The host knows only sealed capacities and therefore may encode a bounded scan hierarchy. It does not inspect ready rows or ready counts.

For each level:

```text
input counts
→ exclusive local offsets
→ next-level group counts
```

The top scalar count remains GPU resident. Parent offsets are propagated downward before stable scatter.

The scan hierarchy is derived recursively from:

```text
ceil(item_count / 256)
```

until one scalar count remains.

## Muon predicate

Inherited unchanged from R2:

```text
COMPUTE_DONE
AND MUON_CONSUME_READY
AND NOT MUON_CONSUMED
AND NOT FAILED
AND route_kind == MUON
```

Output:

```text
muon_ready_rows[]
muon_ready_count
```

ordered by TensorTable row index.

## Successor predicate

Inherited unchanged:

```text
MUON_CONSUMED
AND SUCCESSOR_READY
AND NOT SUCCESSOR_PUBLISHED
AND NOT FAILED
```

Output:

```text
successor_ready_rows[]
successor_ready_count
```

This remains readiness evidence only. B06 remains physical publication/ticket authority.

## BP-DK parameter plane

BP-DK state is parameter-scoped, so R2A does not compact TensorCube rows directly into checkpoint work.

GPU path:

```text
TensorCube lifecycle rows
→ bpdk_parameter_record_index
→ atomic parameter-ready bit plane
→ parallel stable parameter compaction
→ bpdk_ready_parameter_indices[]
```

Many TensorCube rows referencing one BP-DK parameter record produce one parameter identity. No BP-DK state or receipt is synthesized.

## Device-resident ready count

The final scan scalar becomes the ready-count authority for that compact view.

Production R2A source contract:

```text
ready_count_map_count=0
full_table_readback_count=0
host_row_enumeration_count=0
host_range_rebuild_count=0
legacy_host_scheduler_used=false
```

These are source-contract fields until runtime/physical evidence is collected.

## GPU indirect dispatch

R2A emits one 24-byte indirect-args buffer per compact plane:

```text
copy_dispatch_x
copy_dispatch_y
copy_dispatch_z
status_dispatch_x
status_dispatch_y
status_dispatch_z
```

Muon copies execute with:

```text
dispatch_workgroups_indirect(..., 0)
```

and the ordered lifecycle transition executes with:

```text
dispatch_workgroups_indirect(..., 12)
```

No ready-count CPU map is required between compaction and consumption. Large ready sets use deterministic 2D dispatch geometry with X bounded to 65,535.

## Muon physical consumer

The R2A Muon consumer reads compact TensorTable row identities and resolves source/destination offsets from existing R1 SoA columns.

Weight, momentum and update payload movement remains exact bitwise `u32` copying:

```text
destination_words[destination + lane]
=
source_words[source + lane]
```

No floating-point arithmetic or optimizer numerical change is introduced.

## Lifecycle transition

After all Muon W/M/update copy passes, a separate indirect status pass executes:

```text
atomicOr(MUON_CONSUMED)
```

only when the shared overflow flag remains clear. R2A does not mark rows consumed at scheduling time.

## Address domain

R2A preserves the current R2 u32-addressable physical constraint:

```text
offset + R6_TILE_ELEMENTS <= u32::MAX
```

64-bit offsets remain represented as lo/hi columns. R2A introduces no shader-int64 requirement.

## Bounded scratch

R2A allocates metadata scratch only:

```text
predicate bits
local prefixes
group counts
group offsets
compact identity buffers
BP-DK parameter-ready plane
count / overflow words
indirect args
```

No second W/M/update tensor allocation is introduced. All capacities are derived from sealed TensorTable row/parameter counts.

## Overflow law

Any compact output overflow, BP-DK parameter-index overflow, unsupported address domain, or indirect-dispatch geometry overflow is fail-closed. No truncation is admissible.

## R2 reference preservation

The parent R2 single-invocation stable GPU scanner remains source-visible as a qualification/reference oracle:

```text
pass.dispatch_workgroups(1, 1, 1)
```

R2A ActiveVerified must not silently fall back to it or to host enumeration.

## Activation modes

```text
Off
ObserveOnly
ActiveVerified
```

`ActiveVerified` is required for R2A Muon indirect consumption.

## Generation/table identity

Every scheduler instance binds exact:

```text
TensorTable digest
source generation
target generation
row capacity
parameter capacity
```

Drift is rejected before encoding consumer work.

## Binding-budget preservation

R2A uses separate WGSL modules/pipelines for Muon predicate, successor predicate, BP-DK mark, BP-DK parameter predicate, group scan, parent propagation, scatter, indirect args, copy and lifecycle transition.

New R2A shader maximum binding count is 7, below the historical 8-storage-buffer pressure point.

## WGSL modules

```text
crates/base_train/src/shaders/
  tensorcube_table_muon_predicate_scan_r2a.wgsl
  tensorcube_table_successor_predicate_scan_r2a.wgsl
  tensorcube_table_bpdk_parameter_mark_r2a.wgsl
  tensorcube_table_bpdk_parameter_predicate_scan_r2a.wgsl
  tensorcube_table_group_scan_r2a.wgsl
  tensorcube_table_add_parent_offsets_r2a.wgsl
  tensorcube_table_stable_scatter_r2a.wgsl
  tensorcube_table_indirect_args_r2a.wgsl
  tensorcube_table_muon_copy_indirect_r2a.wgsl
  tensorcube_table_status_transition_indirect_r2a.wgsl
```

## Changed files

```text
MOD crates/base_train/src/lib.rs
ADD crates/base_train/src/tensorcube_table_parallel_compaction_r2a.rs
ADD 10 R2A WGSL modules
ADD tools/validate_ash_tensorcube_table_r2a_parallel_compaction_static.py
```

Delta:

```text
MOD 1
ADD 12
DEL 0
```

## Static qualification

```text
PASS_TENSORCUBE_TABLE_R2A_PARALLEL_COMPACTION_STATIC checks=39
PASS_TENSORCUBE_TABLE_R2_GPU_PARALLEL_CONSUMER_STATIC checks=28
PASS_TENSORCUBE_TABLE_R1_STATIC checks=20
PASS_TENSORCUBE_CONSUME_R2_GPU_PARALLEL_PLANE_STATIC checks=61
PASS_TENSORCUBE_CONSUME_R1_RELATION_AUTHORITY_STATIC checks=56
PASS_ASH_WGSL_WGPU26_GLOBAL_COMPATIBILITY_STRUCTURAL_R1
NEW_R2A_WGSL_MODULE_COUNT=10
NEW_R2A_MAX_BINDING_COUNT=7
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

No COMPILE/RUNTIME/PHYSICAL/PERFORMANCE claim is made.

## Artifacts

Overlay:

```text
ASH_TENSORCUBE_TABLE_R2A_PARALLEL_COMPACTION_OVERLAY_CODE_ONLY.zip
SHA-256 3cd4d3f306b64374128bb0ffc3eecf59270127f06e28734fbe6b8e0c54f98166
FILES 13
CRC PASS
```

Full:

```text
ASH_PASS3_TENSORCUBE_TABLE_R2A_PARALLEL_COMPACTION_INDIRECT_DISPATCH_CODE_ONLY.zip
SHA-256 366622d278d7a51e06755efe0832f5566c7f70d1fcf3d49b778eeb12d72a115f
FILES 8471
CRC PASS
```

## Compile acceptance

First local gate:

```text
cargo test -p base_train --lib tensorcube_table_r2a_
```

Then existing R2/R1 tests and exact current WGPU26/Naga shader validation must pass before RUNTIME evidence is admitted.

## Physical acceptance

Same-source physical qualification must prove exact R2 serial GPU vs R2A parallel identity parity for Muon rows, BP-DK parameter records, and successor rows, with stable order where applicable.

Integrated Muon execution additionally requires exact destination-byte parity and zero overflow. BP-DK integration requires exact checkpoint parameter set and existing payload SHA preservation. B06 successor coverage and submission-lineage gates remain strict.

## Performance acceptance

R2A is not promoted merely because it is parallel. Measure at least:

```text
predicate_us
local_scan_us
group_scan_us
parent_propagation_us
scatter_us
indirect_args_us
consumer_us
host_encode_us
```

against R2 serial GPU under representative production TensorTable sizes and readiness densities.

Promotion requires measured non-regression or improvement and zero CPU ready-count roundtrip.

## R3 boundary

Only after R2A physical/performance closure should R3 assume parallel ready selection, device-resident ready count, and GPU-generated consumer dispatch are production-safe.

Next target:

```text
TENSORCUBE-TABLE-R3

PERSISTENT DEVICE SCHEDULER
+ CROSS-WAVE AUTONOMOUS REFILL
+ INDIRECT DISPATCH CHAIN
+ ZERO HOST WAVE ENUMERATION
```

## Final law

> R2 moved TensorCube scheduling authority from the host to the GPU. R2A removes the serial GPU ready-selection bottleneck without changing readiness semantics.

> Ready identities are produced by stable parallel prefix compaction, BP-DK state is deduplicated at parameter granularity, counts remain device-resident, and Muon consumer/status dispatch dimensions are generated on the GPU.

> The R2 serial scanner remains a qualification oracle rather than a production fallback.

> R2A is not PERFORMANCE or PROMOTED until exact physical parity and measured timing evidence exist on the target device.
