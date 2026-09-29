# TENSORCUBE-TABLE-R4D-R2-CF2

## MONOTONIC SEGMENT CURSOR + CHUNK LOOKUP COLLAPSE

```text
TENSORCUBE-TABLE-R4D-R2-CF2

MONOTONIC SEGMENT CURSOR
+ CHUNK LOOKUP COLLAPSE

+ R4D-R2 DURABLE STREAMING PRESERVATION
+ A01-SUBMISSION-LEASE-R1 PRESERVATION

+ PARAMETER-LOCAL ORDERED BTreeMap RANGE
+ BORROWED SEGMENT CURSOR
+ ONE WEIGHT CURSOR PER LOGICAL R2 WINDOW
+ MONOTONIC 64 KiB CHUNK WALK
+ CROSS-CHUNK SEGMENT RETENTION
+ NO ACTIVE PER-CHUNK FULL PARAMETER FILTER

+ M/V BORROWED CURSOR
+ NO ACTIVE M/V Vec<&Segment>
+ NO ACTIVE M/V SECONDARY SORT

+ FULL-DURABLE ADAMW ROUTE CURSOR
+ R3H SUCCESSOR ADAMW ROUTE CURSOR
+ NO ACTIVE PER-ROUTE FULL PARAMETER FILTER

+ OFF LEGACY PATH PRESERVATION
+ OBSERVE LEGACY / CURSOR EXACT PARITY
+ ACTIVE CURSOR AUTHORITY

+ LOCK-FREE CF2 TELEMETRY COUNTERS
+ MEASURED-ZERO REQUIRES EXERCISED ACTIVE PATH

+ EXACT AdamRangeR1 ORDER PRESERVATION
+ EXACT WEIGHT / M / V OVERLAY PRESERVATION
+ EXACT ADAMW HOST COVERAGE PRESERVATION
+ EXACT CF11 BUILDER SEMANTICS PRESERVATION

+ R4D_R2_ENCODE_SCRATCH_BYTES PRESERVATION
+ NO GPU TRANSFER CHANGE
+ NO GPU WAIT CHANGE
+ NO DURABILITY CHANGE
+ NO OPTIMIZER NUMERICAL CHANGE
```

---

## 0. Revision

```text
Patch ID:
TENSORCUBE-TABLE-R4D-R2-CF2

Short name:
R4D-R2-CF2-SEGMENT-CURSOR

Class:
CPU HOT-PATH LOOKUP COMPACTION
ORDERED SEGMENT TRAVERSAL
R2 STREAMING FOLLOW-UP
```

Direct bake parent:

```text
ASH_PASS3_A01_SUBMISSION_LEASE_R1_INCREMENTAL_COMPLETION_FRONTIER_LIVE_SET_COMPACTION_CODE_ONLY.zip
```

Parent semantic chain:

```text
TENSORCUBE-TABLE-R4D-R2
DURABLE PROJECTION HOST COPY COLLAPSE

+

A01-SUBMISSION-LEASE-R1
INCREMENTAL COMPLETION FRONTIER
+ LIVE-SET COMPACTION
```

---

## 1. Purpose

R4D-R2 removed full-window host representations from the durable projection path, but its 64 KiB weight streaming path could still perform repeated parameter-segment lookup work.

The parent AdamW host-demoted generation owns:

```rust
segments: BTreeMap<AdamRangeR1, AdamWHostDemotedCandidateSegmentCf3>
```

while compatibility lookup is:

```rust
segments_for_parameter(parameter_index)
    -> whole-map filter
    -> Vec<&AdamWHostDemotedCandidateSegmentCf3>
```

The R2 weight path called that lookup inside the 64 KiB chunk loop. R2 M/V paths additionally materialized the Vec and sorted it again by `element_start`. Full-durable and R3H successor route validation also repeated parameter lookup per AdamW route.

CF2 changes only the lookup/traversal representation.

---

## 2. Canonical Ordering Authority

`AdamRangeR1` remains the canonical map key and derives `PartialOrd, Ord` with field order:

```text
canonical_parameter_index
element_start
element_count
```

The existing `BTreeMap<AdamRangeR1, ...>` therefore remains the source authority.

CF2 does not add a duplicate:

```text
HashMap<parameter, Vec<segment>>
```

or equivalent second segment ledger.

---

## 3. New Borrowed Cursor Authority

CF2 materializes:

```rust
AdamWParameterSegmentCursorR4DR2CF2<'a>
```

whose state is conceptually:

```text
parameter_index
BTreeMap::Range<'a, AdamRangeR1, Segment>
current: Option<&'a Segment>
last_logical_start
```

The cursor owns no candidate payload and creates no full parameter pointer Vec.

The source generation exposes:

```rust
parameter_segment_cursor_r4d_r2_cf2(parameter_index)
```

while legacy:

```rust
segments_for_parameter(...)
```

remains available for OFF, OBSERVE, diagnostics, tests, and unmigrated callsites.

---

## 4. Monotonic Cursor Law

A cursor admits logical starts only monotonically:

```text
next_logical_start >= previous_logical_start
```

Regression fails closed:

```text
FAIL_R4D_R2_CF2_SEGMENT_CURSOR_REGRESSION
```

A segment is permanently advanced only when:

```text
segment_end <= current_logical_start
```

or after its terminal overlap has been consumed.

When a segment crosses the current chunk/window boundary:

```text
segment_end > logical_end
```

it remains `current` for the next monotonic visit.

---

## 5. Weight Chunk Lookup Collapse

R4D-R2 retains:

```text
R4D_R2_ENCODE_SCRATCH_BYTES = 64 KiB
```

CF2 does not enlarge that scratch and does not change the logical R6 window.

For each logical R2 weight window:

```text
open parameter-local cursor once
    ↓
64 KiB chunk 0
64 KiB chunk 1
64 KiB chunk 2
...
```

ACTIVE uses cursor-specific overlay helpers:

```text
overlay_direct_host_adam_weight_r4d_r2_cf2
overlay_host_demoted_adam_weight_r4d_r2_cf2
```

Those helpers do not call `segments_for_parameter()`.

Existing target/source offset arithmetic and f32 little-endian encoding semantics remain unchanged.

---

## 6. OFF / OBSERVE / ACTIVE

Environment:

```text
ASH_TENSORCUBE_TABLE_R4D_R2_CF2_MODE
```

Accepted:

```text
OFF / DISABLED / 0
OBSERVE / OBSERVE_ONLY
ACTIVE / ACTIVE_VERIFIED / 1
```

Default:

```text
OFF
```

CF2 OBSERVE/ACTIVE requires:

```text
R4D-R2 = ACTIVE
```

### OFF

Parent `segments_for_parameter()` behavior remains authoritative.

### OBSERVE

Weight chunks retain the legacy result as authority and apply the cursor to a bounded shadow scratch. Required parity:

```text
legacy overlaid element count == cursor overlaid element count
legacy final chunk bytes       == cursor final chunk bytes
```

Failure:

```text
FAIL_R4D_R2_CF2_WEIGHT_OVERLAP_PARITY
```

M/V and route traversal compare exact overlap/segment geometry before the legacy authority performs publishing side effects.

### ACTIVE

Cursor traversal becomes authoritative for migrated R2 production paths.

---

## 7. M/V Cursor Adoption

ACTIVE `visit_projected_adam_mv_spans_r4d_r2` uses one borrowed cursor for the logical window.

It preserves the existing sequence:

```text
committed/base gap span
AdamW overlay span
committed/base gap span
...
tail base span
```

ACTIVE does not perform:

```text
segments_for_parameter()
Vec<&Segment>
sort_by_key(element_start)
```

for migrated M/V span projection.

`write_projected_adam_mv_candidate_r4d_r2` uses the same principle and preserves:

```text
write_committed_candidate_span_r4d_r2(...)
write_candidate_slices(...)
```

with exact M/V source ranges and byte offsets.

---

## 8. Route Lookup Collapse

CF2 migrates both:

```text
full-durable-r1 AdamW route validation
r3h-successor AdamW route validation
```

to a parameter-local cursor.

For each AdamW route:

```text
route_start >= segment.element_start
route_end   <= segment_end
```

must still hold.

Parent missing-fragment failures remain:

```text
E_CF9_CF3_FULL_DURABLE_ADAMW_HOST_FRAGMENT_MISSING
E_R3H_SUCCESSOR_ADAMW_HOST_FRAGMENT_MISSING
```

OBSERVE compares legacy and cursor segment identity by:

```text
canonical_parameter_index
element_start
element_count
```

ACTIVE does not perform a full parameter filter for each route.

---

## 9. Coverage and Byte Semantics

CF2 changes no:

```text
AdamW/Muon route decision
segment candidate value
weight source offset
weight target offset
M/V source range
M/V target range
AdamW host element coverage
CF11 initialized-byte verification
weight/M/V hash domain
parameter ordering
durable output byte order
```

Existing coverage gates remain authoritative.

---

## 10. Telemetry Boundary

Because CF2 is itself a CPU hot-path optimization, CF2-owned counters use atomic telemetry rather than a global mutex on each chunk/segment event.

Counters include:

```text
parameter_range_open_count
weight_cursor_open_count
weight_chunk_visit_count
mv_cursor_open_count
route_cursor_open_count
route_cursor_visit_count
cursor_segment_advance_count
cursor_cross_window_retention_count
legacy_segments_for_parameter_call_count
parameter_segment_vec_materialization_count
parameter_segment_secondary_sort_count
per_chunk_full_parameter_scan_count
per_route_full_parameter_scan_count
observe_weight_parity_count
observe_mv_parity_count
observe_route_parity_count
```

ACTIVE measured-zero admission is permitted only after corresponding cursor paths are physically exercised.

---

## 11. ACTIVE Fail-Closed Gates

ACTIVE receipt requires:

```text
weight_cursor_open_count > 0
weight_chunk_visit_count > 0
mv_cursor_open_count > 0
route_cursor_open_count > 0
route_cursor_visit_count > 0

per_chunk_full_parameter_scan_count = 0
per_route_full_parameter_scan_count = 0
parameter_segment_vec_materialization_count = 0
parameter_segment_secondary_sort_count = 0
legacy_segments_for_parameter_call_count = 0
```

This prevents an unexercised literal/default zero from being promoted as physical evidence.

---

## 12. OBSERVE Gates

OBSERVE receipt requires the physical path to produce:

```text
observe_weight_parity_count > 0
observe_mv_parity_count > 0
observe_route_parity_count > 0
```

No parity mismatch is tolerated.

---

## 13. No GPU / Durability Change

The CF2 attribution module adds no:

```text
queue.submit
map_async
get_mapped_range
device.poll
PollType::Wait
copy_buffer_to_buffer
queue.write_buffer
```

CF2 also changes no:

```text
flush
sync_all
rename
spool publication
crash-consistency ordering
```

R4D-R3 remains the durability I/O optimization boundary.

---

## 14. Actual Bake Delta

```text
MOD 3
ADD 2
DEL 0
```

Modified:

```text
crates/base_train/src/lib.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/unified_atlas_mcu_full_model_device_segmented_successor_r1.rs
```

Added:

```text
crates/base_train/src/tensorcube_table_r4d_r2_cf2_monotonic_segment_cursor.rs
tools/validate_ash_tensorcube_table_r4d_r2_cf2_monotonic_segment_cursor_static.py
```

---

## 15. Source Seals

```text
crates/base_train/src/lib.rs
3d475fd4101a032f94387e6113a0da5411a11309117cd00f8cadfb2e66993c6a

crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
11b55a4f935ec29ae238a253fc6857a291f5a252d59cf87d4d66749f49c80d59

crates/base_train/src/unified_atlas_mcu_full_model_device_segmented_successor_r1.rs
9803d24b358e0f89e80aaf964972ef881f53f520b8b38372dfa0156f1ba415bb

crates/base_train/src/tensorcube_table_r4d_r2_cf2_monotonic_segment_cursor.rs
81558ce384ade7607622ec48afdda207794ff60fd6c91773f1cb6dcb62095d97

tools/validate_ash_tensorcube_table_r4d_r2_cf2_monotonic_segment_cursor_static.py
a53d252b88f3f08ddc2bccc50cd4129896a457c714248a3be89d4f6fb55d8d19
```

---

## 16. Protected Graph Seal

```text
Cargo.toml byte-identical to parent
Cargo.lock byte-identical to parent

WGSL parent = 321
WGSL work   = 321
WGSL changed = 0
WGSL added   = 0
WGSL deleted = 0
```

No shader or package graph change is part of CF2.

---

## 17. Static Acceptance

CF2 validator:

```text
PASS_TENSORCUBE_TABLE_R4D_R2_CF2_MONOTONIC_SEGMENT_CURSOR_STATIC checks=105
```

Selected parent regressions:

```text
R4D-R2   140/140 PASS
A01-R1     53/53 PASS
R4D-R1    145/145 PASS
CF8        136/136 PASS
CF7        151/151 PASS
R0B        178/178 PASS
R0A        104/104 PASS
CF6        135/135 PASS
CF5        127/127 PASS
CF4         67/67 PASS
CF3         77/77 PASS
R4B-CF3    127/127 PASS
R1                 PASS
B06-CF1     63/63 PASS
CF11        64/64 PASS
```

No parent validator source required modification.

---

## 18. Artifact Packaging Law

Distributed code ZIPs intentionally exclude:

```text
specs/
artifacts/
*SPEC.md
generated manifest JSON
__pycache__ / *.pyc
```

Source-code files whose Rust/Python names contain the word `manifest` remain code and are not treated as generated manifest artifacts.

Overlay code-only ZIP:

```text
ASH_TENSORCUBE_TABLE_R4D_R2_CF2_MONOTONIC_SEGMENT_CURSOR_CHUNK_LOOKUP_COLLAPSE_OVERLAY_CODE_ONLY.zip
SHA-256 1aabc82164b6d1d72aff75fcdf58c9b83b96d616a9545dde533763ce5755ec55
files=5
CRC=PASS
```

Full code-only ZIP:

```text
ASH_PASS3_TENSORCUBE_TABLE_R4D_R2_CF2_MONOTONIC_SEGMENT_CURSOR_CHUNK_LOOKUP_COLLAPSE_CODE_ONLY.zip
SHA-256 b2292c6bd02610a891aff5f490784cb4ac5aa3f9416e43f4fef125c6b9adfc66
files=8532
CRC=PASS
```

Archive audit for both:

```text
specs/          0
artifacts/      0
*SPEC.md        0
manifest JSON   0
__pycache__/pyc 0
```

---

## 19. Evidence State

The bake environment does not provide `cargo` or `rustc`.

```text
SOURCE       BAKED
STATIC       PASS
COMPILE      UNVERIFIED
RUNTIME      UNVERIFIED
PHYSICAL     UNVERIFIED
PERFORMANCE  UNVERIFIED
```

No higher evidence grade is inferred from static gates.

---

## 20. Compile Acceptance

Authoritative local Rust environment must run:

```powershell
cargo check `
  -p burn_webgpu_backend `
  --lib `
  --release `
  --locked `
  -j 1

cargo check `
  -p base_train `
  --lib `
  --release `
  --locked `
  -j 1

cargo build `
  -p base_train `
  --bin base_train `
  --release `
  --locked `
  -j 1
```

All must PASS before COMPILE promotion.

---

## 21. OBSERVE Qualification

Use:

```text
R4D-R2     = ACTIVE
R4D-R2-CF2 = OBSERVE
```

Exercise:

```text
full durable projection
R3H resident weight successor materialization
AdamW host-demoted segments
M/V projection/writeback
multiple 64 KiB weight chunks
```

Required exact parity:

```text
weight final bytes
weight overlaid element count
M/V overlap geometry
route covering segment identity
AdamW host coverage
final pack/digest authorities
```

---

## 22. ACTIVE Qualification

Then:

```text
R4D-R2     = ACTIVE
R4D-R2-CF2 = ACTIVE
```

Required physical evidence:

```text
weight cursor exercised
multiple weight chunks exercised
M/V cursor exercised
route cursor exercised

per-chunk full parameter scan = Measured(0)
per-route full parameter scan = Measured(0)
parameter segment Vec materialization = Measured(0)
secondary sort = Measured(0)
legacy parameter lookup = Measured(0)

weight/M/V output exact
coverage exact
CF11 closure PASS
```

---

## 23. Performance Boundary

Same-source A/B:

```text
R4D-R2 ACTIVE + CF2 OFF
vs
R4D-R2 ACTIVE + CF2 ACTIVE
```

Measure:

```text
parameter lookup count
full parameter scan count
segment lookup allocation count/bytes
cursor advance count
weight chunk count
AdamW segment count
segment lookup CPU wall time
R2 projection-consume CPU wall time
CPU process time
optimizer-step wall time
generation wall time
```

No exact speedup claim is allowed before physical A/B.

---

## 24. Successor

After CF2 physical closure:

```text
TENSORCUBE-TABLE-R4D-R2-CF3

PREINITIALIZED SOURCE READ
+ VERIFY SCRATCH COLLAPSE
```

CF2 does not absorb CF11 initialized-source reread, verify scratch reuse, spool I/O, or `sync_all` work.

---

## 25. Completion Law

CF2 may emit:

```text
PASS_TENSORCUBE_TABLE_R4D_R2_CF2_MONOTONIC_SEGMENT_CURSOR
```

only when:

```text
SOURCE
    borrowed ordered cursor implemented
    weight / M/V / route paths migrated

STATIC
    CF2 gate PASS
    selected parent regressions PASS

COMPILE
    backend release PASS
    base_train lib release PASS
    base_train binary PASS

RUNTIME OBSERVE
    weight byte parity exact
    M/V geometry parity exact
    route segment identity parity exact

PHYSICAL ACTIVE
    all migrated cursor paths exercised
    prohibited legacy lookup/materialization counters measured zero
    output and coverage exact
    CF11 closure PASS

PERFORMANCE
    measured independently
```

---

## 26. Final Law

> **R4D-R2-CF2 does not change AdamW segment ownership or overlay semantics. It changes how already ordered segments are reached.**

> **The existing `BTreeMap<AdamRangeR1, ...>` remains the source authority. A borrowed parameter-local range and one-current-segment cursor replace repeated full-map filtering on migrated R2 production paths.**

> **The R2 64 KiB scratch remains unchanged. A segment crossing a chunk boundary stays current for the next monotonic chunk instead of being rediscovered from the complete segment registry.**

> **M/V projection/writeback and AdamW route validation use the same ordered-source principle without ACTIVE parameter-wide Vec materialization or secondary sorting.**

> **No output byte, digest, optimizer value, GPU transfer, durability barrier, A01 lease lifecycle rule, or CF11 successor authority is changed by CF2.**

> **SOURCE and STATIC evidence do not claim compile success, physical closure, or performance improvement.**
