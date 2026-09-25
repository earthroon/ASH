# TENSORCUBE-TABLE-R4B-CF3

## FULL-ROUTE HOST LEDGER COMPACTION
## + EAGER TRAINING-ROW VEC RETIREMENT
## + ROW-INDEX FANOUT RETIREMENT
## + COMPACT PARAMETER ROUTE DESCRIPTORS
## + SINGLE PARAMETER COMPLETION PLANE
## + DERIVED LOGICAL ROW AUTHORITY
## + PHYSICAL ADAM SEGMENT EVIDENCE PRESERVATION

## 0. Revision

```text
Patch ID:
TENSORCUBE-TABLE-R4B-CF3

Canonical name:
ASH-BASETRAIN-TENSORCUBE-TABLE-R4B-CF3-
FULL-ROUTE-HOST-LEDGER-COMPACTION-
EAGER-TRAINING-ROW-VEC-RETIREMENT-
ROW-INDEX-FANOUT-RETIREMENT-
COMPACT-PARAMETER-ROUTE-DESCRIPTORS-
SINGLE-PARAMETER-COMPLETION-PLANE-
DERIVED-LOGICAL-ROW-AUTHORITY
```

Direct implementation parent:

```text
ASH_PASS3_TENSORCUBE_TABLE_R4C_CF3_SLOT_LIFECYCLE_BACKPRESSURE_CLOSURE_CODE_ONLY.zip
SHA-256:
d2812a344308b21f38ce17bb8dbe3cd918dc2ada0beb758a57ac0db471e53d76
files=8507
CRC=PASS
```

Class:

```text
HOST CONTROL-PLANE COMPACTION
HOST MUTABLE-STATE COMPACTION
LOGICAL ROUTE REPRESENTATION REPAIR

NO TRAINING MATH CHANGE
NO OPTIMIZER MATH CHANGE
NO GPU TENSORCUBE ROW CHANGE
NO GPU BUFFER LAYOUT CHANGE
NO WGPU KERNEL CHANGE
NO ADAMW PHYSICAL SEGMENT CHANGE
NO HIMUON TILE EXECUTION CHANGE
NO GENERATION COMMIT AUTHORITY CHANGE
```

## 1. Parent debt

Historical R4B-CF2 persisted:

```rust
rows: Vec<TrainingRowR4BCF2>,
row_indices_by_parameter: Vec<Vec<usize>>,
parameter_completion: Vec<ParameterCompletionR4BCF2>,
```

Every logical HiMuon tile and AdamW logical route span therefore received a persistent host row object even though current production completion is validated parameter-wide and then fanned back out to those rows.

Current production consumers used the eager rows for:

```text
generation reset
parameter completion fanout
pending-required-row scan
seal row counts
```

No external production consumer owned a `TrainingRowR4BCF2` reference.

## 2. CF3 compact authority

CF3 removes the production types/state:

```text
TrainingRowR4BCF2
TrainingRowKindR4BCF2
ResidencyStateR4BCF2
rows: Vec<TrainingRowR4BCF2>
row_indices_by_parameter: Vec<Vec<usize>>
```

and materializes:

```rust
ParameterRouteDescriptorR4BCF3 {
    parameter_index,
    logical_row_start,
    himuon_row_count,
    adamw_route_span_count,
    logical_row_count,
}
```

with one immutable descriptor per canonical parameter.

Mutable completion remains one:

```text
ParameterCompletionR4BCF2
```

per canonical parameter.

## 3. Logical full-route view preservation

The complete logical row domain remains represented without one host allocation per logical row.

Per parameter:

```text
logical_row_count
=
himuon_row_count
+
adamw_route_span_count
```

Global logical ordering remains:

```text
canonical parameter order

within parameter:
    HiMuon ROW_MAJOR_TILE_GRID logical rows
    then AdamW logical route spans
```

`logical_row_start` forms a checked prefix chain.

CF3 seals this projection with:

```text
logical_route_descriptor_digest
```

over canonical ordered descriptor fields.

## 4. No eager HiMuon tile expansion

Historical R4B-CF2 constructor performed nested:

```text
full_tile_rows × full_tile_cols
```

host iteration and `registry.resolve_tile(...)` for every HiMuon tile.

CF3 instead validates compact registry geometry:

```text
route rank == 2
tile geometry == 16 × 16
tile_count == full_tile_rows * full_tile_cols
muon_element_count == tile_count * 256
route.muon_element_count exact
```

and uses:

```text
expected_himuon_rows = grid.tile_count
```

No production `resolve_tile()` call remains in the R4B-CF3 host ledger path.

## 5. Adam logical route spans preserved

Existing `route_span(...)` remains the logical Adam-span authority.

CF3 continues walking compact route boundaries to derive:

```text
expected_adamw_route_spans
```

This is intentionally distinct from actual Adam physical segment count.

## 6. Physical Adam evidence preserved

CF3 retains production consumption of:

```rust
full.adamw.segment_ranges_r4b_cf2()
```

and exact validation through:

```rust
adam_range_is_exact_route(...)
```

It continues recording:

```text
actual_adamw_physical_segments
```

from actual physical segment ranges.

CF3 does not replace physical segment evidence with logical span arithmetic.

## 7. Physical HiMuon evidence preserved

CF3 retains:

```rust
full.muon.publication_receipt()?
full.muon.descriptors()
```

and validates per-parameter Muon completed elements against the route registry.

Expected geometry comes from compact descriptors.
Completed coverage still comes from the actual full trainable device generation.

## 8. Completion plane

For each parameter, physical evidence is validated first.

Then the single completion record is updated:

```text
completed_himuon_elements
completed_adamw_elements
completed_himuon_rows
completed_adamw_route_spans
actual_adamw_physical_segments
route_coverage_complete
candidate_weight_complete
optimizer_state_complete
parameter_terminal
```

No row-index fanout follows.

## 9. Pending-required-row derivation

Historical:

```rust
self.rows
    .iter()
    .filter(|row| !row.completed && !row.failed)
```

is retired.

CF3 derives:

```text
expected_rows
= expected_himuon_rows + expected_adamw_route_spans

completed_rows
= completed_himuon_rows + completed_adamw_route_spans

pending_rows
= expected_rows - completed_rows - failed_row_count
```

with checked arithmetic and fail-closed guards for over-completion or over-accounting.

Global `pending_required_rows` is the checked sum over parameter completion records.

## 10. Generation reset

Historical reset traversed all persistent logical host rows and all parameter completion records.

CF3 reset touches only mutable parameter completion records and generation-level pending receipts.

Immutable route descriptors survive generation reset unchanged.

## 11. Seal compaction

Historical seal re-scanned `rows` to derive:

```text
himuon_row_count
adamw_route_span_count
total_training_row_count
```

CF3 derives those values from compact descriptors and validates the full descriptor/completion parameter plane:

```text
route count == descriptor count == completion count
parameter identity exact
prefix chain exact
descriptor logical count exact
descriptor/completion expected geometry exact
```

## 12. Ready / commit authority parity

CF3 preserves the existing `GenerationCommitReadyR4BCF2` criteria:

```text
all parameters terminal
failed parameter count == 0
pending required rows == 0
full trainable coverage complete
EVE candidate complete
HiMuon target complete
Weight successor ready
B06 active-device commit
submission epoch union complete
```

The existing `ready_digest` schema and inputs remain unchanged.

Existing R4B-CF2 receipt digest inputs also remain unchanged. The new compact descriptor digest is reported separately and is not injected into the historical receipt digest.

R3C/R3C1 remain the sole generation commit authority.

## 13. Receipt extension

`TensorCubeTableR4BCF2Receipt` now additionally carries:

```text
hostLedgerPatchId = TENSORCUBE-TABLE-R4B-CF3
hostLedgerPassToken
hostLedgerHoldToken

compactParameterRouteDescriptorMaterialized

eagerHostTrainingRowLedgerMaterialized = false
rowIndexFanoutMaterialized = false
logicalFullRouteViewPreserved = true

logicalRouteDescriptorDigest

mutableParameterCompletionRecordCount
compactRouteDescriptorCount

eagerHostTrainingRowRecordCount = 0
rowIndexEntryCount = 0
```

Historical logical count fields remain:

```text
totalTrainingRowCount
himuonRowCount
adamwRouteSpanCount
```

Their numerical meaning is preserved; they are now logical counts rather than heap-object counts.

## 14. Unit-test source

Source materializes bounded tests for:

```text
parameter-derived pending rows
compact descriptor prefix identity
over-completion fail-closed behavior
```

These tests are source-materialized only in this bake environment; Rust execution is not claimed.

## 15. Exact implementation delta

Compared with the direct parent:

```text
MOD 2
ADD 1
DEL 0
```

Modified production source:

```text
crates/base_train/src/tensorcube_table_r4b_cf2_full_route_training_table.rs
```

Modified parent validator:

```text
tools/validate_ash_tensorcube_table_r4b_cf2_full_route_training_table_static.py
```

Added CF3 validator:

```text
tools/validate_ash_tensorcube_table_r4b_cf3_full_route_host_ledger_compaction_static.py
```

No scheduler, R4C, WGPU kernel, TensorCube R1 GPU-table or optimizer implementation file changed.

## 16. Source SHA-256

```text
179e2a263270b1a580ccb3e68393bdbced6fff37b9d9c30222e068ac088c6ed1  crates/base_train/src/tensorcube_table_r4b_cf2_full_route_training_table.rs
e9a562b7af4b3ed4d581a5b89208527282e2fd03b22ec8fda6a95e3b6e6dd19d  tools/validate_ash_tensorcube_table_r4b_cf2_full_route_training_table_static.py
b881117846a6028fba07da1086c20f6d0a50328ac23f62ad1a756f6c28da7482  tools/validate_ash_tensorcube_table_r4b_cf3_full_route_host_ledger_compaction_static.py
```

## 17. Static acceptance

CF3:

```text
PASS_TENSORCUBE_TABLE_R4B_CF3_FULL_ROUTE_HOST_LEDGER_COMPACTION_STATIC checks=127
```

Maintained parent R4B-CF2:

```text
PASS_TENSORCUBE_TABLE_R4B_CF2_FULL_ROUTE_TRAINING_ROW_TABLE_UNIFIED_GENERATION_VIEW_STATIC checks=118
```

Retained neighboring regressions:

```text
R4B-CF1     77/77 PASS
R4B         58/58 PASS

R4A-CF2-CF1 90/90 PASS
R4A-CF2     40/40 PASS
R4A-CF1     90/90 PASS
R4A         66/66 PASS

R4C-CF3     77/77 PASS
R4C-CF2     75/75 PASS
R4C-CF1    131/131 PASS
R4C         82/82 PASS
```

Python validators also pass `py_compile`.

## 18. Compile / runtime / physical status

The bake environment has no Rust toolchain.

Therefore:

```text
SOURCE       APPLIED
STATIC       PASS
ARCHIVE      CRC PASS
COMPILE      UNVERIFIED
RUNTIME      UNVERIFIED
PHYSICAL     UNVERIFIED
PERFORMANCE  UNVERIFIED
```

No compile, runtime, physical or performance promotion is claimed.

Required local continuation:

```powershell
cargo check `
  -p base_train `
  --lib `
  --release `
  --locked
```

```powershell
cargo test `
  -p base_train `
  --lib `
  --release `
  --locked `
  tensorcube_table_r4b_cf3_ `
  -- `
  --nocapture
```

```powershell
cargo build `
  -p base_train `
  --bin base_train `
  --release `
  --locked
```

## 19. Baked archive

```text
ASH_PASS3_TENSORCUBE_TABLE_R4B_CF3_FULL_ROUTE_HOST_LEDGER_COMPACTION_CODE_ONLY.zip
SHA-256:
7d564ab3acbec3829ea30226f359a8d1ec3dbd3d3c5541417cb7db6a0bd3e736
files=8508
CRC=PASS
```

Archive exclusion policy:

```text
specs/       0 entries
artifacts/   0 entries
manifest/    0 entries
manifests/   0 entries
```

Build-authority files such as `Cargo.toml` and `Cargo.lock` remain present. Source filenames containing the word `manifest` remain when they are implementation source rather than generated manifest payloads.

## 20. Evidence boundary

CF3 statically establishes:

```text
persistent eager row ledger removed
row-index fanout removed
one compact descriptor per parameter
one mutable completion record per parameter
logical row counts preserved by compact derivation
physical Muon evidence preserved
physical Adam segment evidence preserved
ready/commit authority preserved
```

CF3 does NOT yet establish measured:

```text
RSS reduction
heap allocation reduction
step-time reduction
generation-time reduction
```

Those require later runtime/performance measurement.

## 21. Final law

> R4B-CF3 removes duplicated host representation, not route semantics. A logical TensorCube row is now derived from compact parameter geometry instead of receiving a persistent mutable Rust object.

> Expected logical rows come from registry geometry. Completed rows come from validated physical generation evidence. Actual Adam physical segment evidence remains independently observed.

> Generation readiness, B06, R3B, submission-union and R3C authority are preserved. The historical ready digest and receipt digest inputs remain stable across the host representation change.

> The source structure changes host bookkeeping from logical-row scale toward parameter scale. Actual memory and wall-time improvements remain UNVERIFIED until measured.
