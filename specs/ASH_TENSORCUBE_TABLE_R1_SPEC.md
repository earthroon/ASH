# TENSORCUBE-TABLE-R1

## GPU-RESIDENT TENSOR TABLE AUTHORITY

```text
+ R6 DESCRIPTOR → TENSOR TABLE ROW MATERIALIZATION
+ TENSORCUBE ROW IDENTITY SSOT
+ PARAMETER / CUBE / GENERATION COLUMN AUTHORITY

+ PACKED W / M / UPDATE SOURCE COLUMNS
+ SUCCESSOR W / M DESTINATION COLUMNS
+ BP-DK STATE COLUMN
+ STATUS / FLAGS COLUMN

+ GPU-RESIDENT SOA TABLE
+ IMMUTABLE GEOMETRY COLUMNS
+ MUTABLE LIFECYCLE STATUS COLUMN

+ EXACT RANGE / ALIAS PROOF
+ GENERATION-BOUND TABLE SEAL
+ TABLE DIGEST

+ MUON CONSUME VIEW
+ BP-DK SNAPSHOT VIEW
+ SUCCESSOR VIEW

+ NO DUPLICATE CONSUMER JOB TABLE
+ NO PER-PARAMETER HOST TABLE REBUILD
+ NO NUMERICAL CHANGE
```

## 1. Authority

`McuTensorCubeJobDescriptorR6` remains the sole TensorCube decomposition authority. TENSORCUBE-TABLE-R1 materializes rows from existing R6 descriptors and must not recompute tile geometry from tensor shapes.

Canonical row identity is:

```text
(parameter_index, tensorcube_ordinal)
```

`table_row_index` is only a compact bijective index over that identity.

## 2. Logical table and physical layout

The table is logically row-oriented and physically GPU-resident as Structure-of-Arrays. Immutable identity, geometry, source, destination, generation, and flags columns are separated from the mutable lifecycle status column.

64-bit logical offsets are uploaded as `lo/hi u32` words so R1 does not introduce a new shader-int64 requirement.

## 3. Immutable row columns

Each row binds at least:

```text
parameter_index
canonical_job_ordinal
tensorcube_ordinal
tensorcube_row
tensorcube_col
valid_rows
valid_cols
queue_generation_id
queue_epoch_id
source_generation
target_generation
wave_ordinal
packed_weight_source_element
packed_momentum_source_element
orthogonal_update_source_element
logical_momentum_destination_element
physical_successor_destination_element
weight_span_start
weight_span_count
bpdk_parameter_record_index
flags
```

Packed W/M/update coordinates come directly from R6 lineage. Logical weight row spans and canonical momentum destinations reuse TENSORCUBE-CONSUME-R1 projection authority. Physical successor destination uses the same padded TensorCube target coordinate used by TENSORCUBE-CONSUME-R2.

## 4. Parameter authority

Parameter-wide geometry and canonical base coordinates remain normalized in a parameter table. Tensor rows reference parameter state by `parameter_index`; BP-DK parameter state is referenced through `bpdk_parameter_record_index` rather than duplicating large state metadata per TensorCube row.

A BP-DK binding must explicitly provide its physical state offset/length and source/target generations. Missing state must not be synthesized.

## 5. Lifecycle authority

Lifecycle state is a mutable GPU-resident bitset. R1 defines the ABI for:

```text
COMPUTE_READY
COMPUTE_SUBMITTED
COMPUTE_DONE
MUON_CONSUME_READY
MUON_CONSUMED
BPDK_READY
BPDK_CAPTURED
SUCCESSOR_READY
SUCCESSOR_PUBLISHED
FAILED
```

Unknown bits are rejected. Lifecycle status is excluded from the immutable TensorTable digest and may have its own runtime digest.

## 6. Generation seal

A table may contain only one exact source generation and one exact target generation. Generation drift across R6 descriptors is fail-closed. BP-DK target generation must exactly match the descriptor candidate generation.

## 7. Digest

`tensor_table_digest` binds:

```text
schema revision
source generation
target generation
R6 lineage digest
parameter authority digest
immutable row records
parameter records
logical weight row spans
```

Mutable lifecycle status is not part of this digest.

## 8. Range / alias proof

Before admission, R1 reuses Consume-R1's exact logical weight projection and validates destination non-overlap for logical weight spans and canonical momentum spans. Checked arithmetic is required for all span and offset construction.

No atomics may be used to conceal illegal write aliasing.

## 9. GPU residency

After host metadata seal, each column is uploaded once to a GPU storage buffer. Immutable buffers are `STORAGE | COPY_DST`. Mutable lifecycle status is `STORAGE | COPY_DST | COPY_SRC`.

The hot path must not read back the full TensorTable merely to select work.

## 10. Views

### Muon Consume View

Select rows satisfying:

```text
COMPUTE_DONE
AND MUON_CONSUME_READY
AND NOT MUON_CONSUMED
AND NOT FAILED
```

and route-authorized for Muon.

TENSORCUBE-CONSUME-R2 gains a `from_tensor_table_muon_view()` adapter and derives its physical copy ranges directly from TensorTable rows instead of rebuilding TensorCube geometry.

### BP-DK Snapshot View

Select parameter-state references satisfying:

```text
BPDK_READY
AND NOT BPDK_CAPTURED
AND NOT FAILED
```

and deduplicate many TensorCube rows to one BP-DK parameter record.

### Successor View

Select rows satisfying:

```text
MUON_CONSUMED
AND SUCCESSOR_READY
AND NOT SUCCESSOR_PUBLISHED
AND NOT FAILED
```

B06 remains a separate fail-closed successor evidence authority; table status does not spoof a B06 ticket.

## 11. Migration law

```text
Phase A
existing Consume-R1/R2 remains runtime authority
TensorTable is materialized and parity-validated

Phase B
TensorTable metadata becomes consumer metadata authority
existing consumers derive views from the table

Phase C
GPU table status scan / compaction directly schedules consumers
```

R1 closes Phase A and introduces the Phase-B Consume-R2 adapter. It does not claim GPU compaction or final production promotion.

## 12. Preservation laws

R1 must preserve:

```text
Muon numerical math
AdamW numerical math
BP-DK update math
R8A hashing semantics
R6 descriptor authority
B06 successor authority
existing candidate W/M/update allocations
```

No second full W/M/update tensor allocation is allowed. The table is metadata only.

## 13. Required tests / static gates

Required source tests include:

```text
tensorcube_table_r1_r6_row_identity_exact_and_weight_coverage
tensorcube_table_r1_status_not_in_immutable_digest_and_muon_view_exact
tensorcube_table_r1_bpdk_view_deduplicated
```

The 30×34 / 16×16 fixture must materialize 6 TensorCube rows and exactly cover 1020 logical weight elements.

Static validator:

```text
tools/validate_ash_tensorcube_table_r1_static.py
```

must verify module export, GPU SoA columns, R6 source authority, Consume-R1 reuse, Muon/BP-DK/successor views, Consume-R2 table adapter, lifecycle authority, and GPU upload path.

## 14. Evidence boundary

A source/static bake may claim only:

```text
SOURCE
STATIC
```

until Rust compilation is run. It must not claim COMPILE, RUNTIME, PHYSICAL, PERFORMANCE, or PROMOTED without corresponding evidence.

## 15. Completion law

TENSORCUBE-TABLE-R1 is complete when:

1. every table row originates from an R6 descriptor;
2. `(parameter_index, tensorcube_ordinal)` is unique;
3. generation identity is exact and sealed;
4. packed W/M/update coordinates remain R6-authored;
5. logical weight spans remain Consume-R1-authored;
6. physical successor coordinates remain Consume-R2-compatible;
7. BP-DK state is referenced once per parameter and never synthesized;
8. immutable and mutable table columns are physically separated;
9. the immutable digest excludes lifecycle state;
10. Muon, BP-DK, and successor views derive from the same TensorTable identity;
11. Consume-R2 can derive a physical plan directly from the Muon view;
12. no consumer-specific TensorCube geometry table is introduced;
13. no numerical tensor operation changes;
14. no second full tensor allocation is introduced.

## Final law

> TensorCube is the canonical row identity of a GPU-resident TensorTable. R6 defines the rows once; Muon, BP-DK, checkpoint and successor systems consume views over those same rows instead of constructing independent job tables.
