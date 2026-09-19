# TENSORCUBE-CONSUME-R1

## TensorCube Consume Relation Authority

```text
+ R6 DESCRIPTOR REUSE
+ PARAMETER AUTHORITY TABLE
+ PACKED → CANONICAL PROJECTION
+ EXACT DESTINATION RANGE PROOF
+ NO GPU WRITE YET
```

## 0. Parent

Direct parent:

```text
ASH_PASS3_EVE_MCU_R3H_CF11_R1_CF1_CF1_CF1_CF1_CF1_CF1_RAM36_CURRENT_SOURCE_PROMOTION_CODE_ONLY.zip
SHA-256 918fb8724ce05e7b76c7415055e9e8a2ac0f639dddc011a4bc7f3ad231223b00
```

R1 class:

```text
TENSORCUBE RELATION AUTHORITY
POST-COMPUTE CONSUME PROJECTION
DESTINATION GEOMETRY ADMISSION
NO-EXECUTION STRUCTURAL FOUNDATION
```

## 1. Core law

`McuTensorCubeJobDescriptorR6` remains the single TensorCube job identity authority.

R1 does not introduce an independent Muon consume scheduler. It derives the consume relation from:

```text
R6 descriptor row
+
parameter-wide canonical geometry
```

No new GPU write, WGSL kernel, dispatch, D2H or H2D path is introduced.

## 2. R6 geometry SSOT

R6 now exposes:

```text
R6_TILE_SIDE = 16
R6_TILE_ELEMENTS = R6_TILE_SIDE * R6_TILE_SIDE
R6_TILE_BYTES_F32 = R6_TILE_ELEMENTS * 4
```

The existing R6 descriptor builder uses these constants for gradient base, TensorCube row/col origins, valid edge rows/cols and packed W/M/U offsets.

This is a source SSOT refactor only. Numerical tile geometry remains 16x16 / 256 f32 elements.

## 3. Parameter authority table

New:

```text
TensorCubeConsumeParameterAuthorityR1
```

It binds only parameter-wide metadata:

```text
parameter_index
canonical_weight_base_element
canonical_momentum_base_element
logical_rows
logical_cols
tensorcube_rows
tensorcube_cols
momentum_element_count
route_kind
consume_enabled
```

The builder stores parameter authority keyed by canonical parameter index and rejects authority drift.

It is not a second scheduler and contains no ready queue, priority or submission order.

## 4. R6 descriptor reuse

The relation directly consumes `McuTensorCubeJobDescriptorR6` fields:

```text
canonical_job_ordinal
parameter_index
tensorcube_ordinal
tensorcube_row
tensorcube_col
valid_rows
valid_cols
candidate_weight_offset_elements
candidate_momentum_offset_elements
queue_generation_id
queue_epoch_id
```

No independent consume-job ordinal exists.

R1 requires exact TensorCube identity reconstruction from canonical job ordinal.

## 5. Packed source proof

Candidate W/M packed source offsets remain R6 authority.

Per R6 epoch R1 proves:

```text
[start,end) within descriptor_count * R6_TILE_ELEMENTS
pairwise source-range disjointness
```

for both candidate weight and candidate momentum.

R1 never recomputes packed source offsets from parameter geometry.

## 6. Canonical weight projection

Weight projection uses exact row spans.

For every valid local row:

```text
logical_row = tensorcube_row * R6_TILE_SIDE + local_row
logical_col_start = tensorcube_col * R6_TILE_SIDE

destination_start =
    canonical_weight_base_element
    + logical_row * logical_cols
    + logical_col_start

count = valid_cols
```

A TensorCube is not incorrectly modeled as one contiguous 256-element canonical weight span.

Partial edge cubes are preserved exactly.

## 7. Canonical momentum projection

Current HiMuon momentum storage remains padded TensorCube order:

```text
canonical_momentum_dst_start =
    canonical_momentum_base_element
    + canonical_job_ordinal * R6_TILE_ELEMENTS

count = R6_TILE_ELEMENTS
```

Weight and momentum destination geometry are deliberately separate.

## 8. Exact destination proof

R1 proves full `[start,end)` bounds and pairwise disjointness for:

```text
canonical weight row spans
canonical momentum spans
```

Adjacent spans pass. Any overlap fails closed.

The same proof rejects cross-parameter destination overlap.

Coverage must be exact:

```text
weight_gap_count = 0
weight_overlap_count = 0
momentum_gap_count = 0
momentum_overlap_count = 0
```

## 9. Relation table

New:

```text
TensorCubeConsumeRelationRowR1
TensorCubeConsumeWeightRowSpanR1
TensorCubeConsumeRelationBuilderR1
TensorCubeConsumeRelationReceiptR1
```

A relation row binds R6 epoch identity, TensorCube identity, packed W/M source coordinates, canonical momentum destination and the corresponding weight-row-span table range.

The weight span table retains insertion order because relation rows index it. Sorted shadow copies are used for range proof only.

## 10. Relation identity

R1 seals:

```text
r6_descriptor_digest
parameter_authority_digest
consume_relation_digest
```

R6 lineage aggregates the exact existing `descriptor_manifest_digest_r6()` results for admitted epochs.

The relation digest binds R6 lineage, parameter geometry, relation rows, weight row spans and schema revision.

## 11. Production integration

R1 is connected to both current R6 production paths.

### Active async / ActiveVerified

```text
R6 seal
→ descriptor_snapshot_for_r8()
→ R1 admit_r6_epoch()
→ existing async execution unchanged
```

After all waves drain and assembly coverage is exact:

```text
R1 seal
→ compact relation receipt
→ existing segmented successor handoff
```

`source_parameter_byte_offset` and `momentum_start` are passed into the active-async function as read-only canonical geometry inputs only.

### Streaming R6 path

```text
R6 seal / routing
→ final descriptor snapshot
→ R1 admit_r6_epoch()
→ existing CPU successor consumption
```

After parameter waves complete:

```text
R1 seal
→ compact relation receipt
→ existing pending-tile terminal checks
```

## 12. No consume cutover

The current CPU streaming path remains production authority:

```text
pending_tiles.remove(next_tile)
write_successor_muon_tile_f32(...)
HiMuonMomentumRuntimeR8::commit_candidate_range_r8(...)
```

R1 performs no second write and no shadow mutation.

The active-async device segmented successor path is likewise unchanged except for relation observation.

## 13. Compact receipt

```text
[ASH-TENSORCUBE-CONSUME-R1][relation]
```

Reports:

```text
descriptors
parameters
relations
weight_spans
momentum_spans
weight_elements
momentum_elements
weight_gaps
weight_overlaps
momentum_gaps
momentum_overlaps
r6_digest
parameter_digest
relation_digest
exact_destination_range_proof
admitted
```

No per-TensorCube success log is emitted.

## 14. Fixtures

R1 source includes fixtures for:

```text
full 16x16 exact projection
30x34 nontrivial 2x3 grid
14x2 partial edge
packed source overlap rejection
packed source out-of-bounds rejection
parameter authority drift rejection
duplicate R6 epoch rejection
cross-parameter weight overlap rejection
cross-parameter momentum overlap rejection
cross-parameter adjacency admission
deterministic relation digest
```

The 30x34 fixture requires exact 1020 logical weight elements with zero gap/overlap.

## 15. Changed files

```text
MOD crates/base_train/src/lib.rs
MOD crates/base_train/src/unified_atlas_mcu_global_tensorcube_job_queue_r6.rs
MOD crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
ADD crates/base_train/src/tensorcube_consume_relation_r1.rs
ADD tools/validate_ash_tensorcube_consume_r1_relation_authority_static.py
```

No other file changed.

## 16. Source SHA-256

```text
41a86fe55c6c7946614a0511f967a765e2d3b08628edc029a84d019c3bc4d493  crates/base_train/src/lib.rs
62af2bbe220a7c5fc1e5cfdacd73b40069d1b6026e098fcca68d298ff92c273e  crates/base_train/src/unified_atlas_mcu_global_tensorcube_job_queue_r6.rs
daab42416fa29ae4c09b91546ab192908b116f5e522e0f9a64a409e6aed1cfe3  crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
9b0651bcc778685f969b4dcdb2759ce3842727c57c0be98f4f92a4e96ea765b4  crates/base_train/src/tensorcube_consume_relation_r1.rs
50611ef25afa6ee50400c9031414f20bf473c38b13ee3d7f58be8cfe2247fee6  tools/validate_ash_tensorcube_consume_r1_relation_authority_static.py
```

## 17. Static qualification

```text
PASS_TENSORCUBE_CONSUME_R1_RELATION_AUTHORITY_STATIC checks=56
PASS_ASH_BASETRAIN_UNIFIED_ATLAS_MCU_GLOBAL_TENSORCUBE_JOB_QUEUE_AND_INDEPENDENT_WORK_ADMISSION_R6_STATIC
PASS_EVE_MCU_R3H_CF11_R1_BOUNDED_COW_WORKSPACE_STATIC checks=22
PASS_EVE_MCU_R3H_CF11_R1_CF1_CF1_CF1_CF1_CF1_BPDK_GENERATION_BINDING_STATIC checks=27
PASS_EVE_MCU_R3H_CF11_R1_CF1_CF1_CF1_R8A_PREDURABILITY_SEAL_STATIC checks=30
PASS_EVE_MCU_R3H_CF11_R1_CF1_CF1_MUON_PACKED_ADDRESS_STATIC checks=26
PASS_EVE_MCU_R3H_CF11_R1_CF1_PACKED_MV_DIGEST_STATIC checks=27
PASS_EVE_MCU_R3H_CF11_R1_CF1_CF1_CF1_CF1_CF1_CF1_RAM36_CURRENT_SOURCE_PROMOTION_STATIC checks=32
```

The older atlas-wave-streaming validator retains the same two direct-parent failures:

```text
atlas page authority used
streaming path mutates persistent momentum per tile
```

R1 adds no new failure there.

Rust toolchain is unavailable in the bake environment, so COMPILE/RUNTIME/PHYSICAL are not claimed.

## 18. Artifacts

Overlay:

```text
ASH_TENSORCUBE_CONSUME_R1_RELATION_AUTHORITY_OVERLAY_CODE_ONLY.zip
SHA-256 c4a03ae9262daa7f4fa49fbb3c4c0556eb873f7fdd0ee90eb4132efb3cd9958e
FILES 5
CRC PASS
```

Full:

```text
ASH_PASS3_TENSORCUBE_CONSUME_R1_RELATION_AUTHORITY_CODE_ONLY.zip
SHA-256 9649b6147ef89e0156532a0fed6ef786ea8b7862d5cd91abe9713090202b7986
FILES 8442
CRC PASS
```

Both exclude specs/, artifacts/, manifests/, Markdown, __pycache__ and *.pyc.

## 19. Physical acceptance

With R6 enabled, both ActiveVerified active-async and streaming R6 execution must seal:

```text
weight_gaps=0
weight_overlaps=0
momentum_gaps=0
momentum_overlaps=0
exact_destination_range_proof=true
admitted=true
```

Existing numerical successor output must remain unchanged.

## 20. Evidence

```text
SOURCE       APPLIED
STATIC       PASS
ARCHIVE CRC  PASS
COMPILE      NOT RUN
RUNTIME      UNVERIFIED
PHYSICAL     UNVERIFIED
PERFORMANCE  UNMEASURED
```

## 21. R2 boundary

Only after R1 compiles and physically seals may `TENSORCUBE-CONSUME-R2 GPU Parallel Consume Plane` add device scatter.

R2 must consume the R1 relation/parameter authority instead of independently reconstructing TensorCube → canonical geometry.

## 22. Final law

> TensorCube R6 remains the single job identity authority for compute and future successor consumption.

> The parameter authority table contains parameter-wide canonical geometry only and is not another scheduler.

> Packed W/M coordinates remain R6 source-domain authority.

> Canonical weight projection uses exact row spans including partial edges; momentum preserves the current padded 256-element TensorCube commit layout.

> Exact full destination ranges, including cross-parameter ranges, must be proven non-overlapping before any future parallel scatter is admitted.

> R1 adds no WGSL, no GPU write, no dispatch, no transfer and no optimizer numerical change.
