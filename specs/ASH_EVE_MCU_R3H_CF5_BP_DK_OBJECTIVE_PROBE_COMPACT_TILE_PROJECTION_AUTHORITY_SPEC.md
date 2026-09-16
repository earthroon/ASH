# EVE-MCU-R3H-CF5

## BP-DK OBJECTIVE PROBE COMPACT TILE PROJECTION AUTHORITY

**Revision:** `EVE-MCU-R3H-CF5`  
**Parent:** `EVE-MCU-R3H-CF4 + BUFFER-AUTHORITY-INVENTORY-TEST-CF1`  
**Class:** BP-DK objective-probe representation closure / compact tile-native virtual source authority

```text
+ RETIRE ROW-SPAN EXPANSION
+ TILE-NATIVE SPARSE OVERLAY STORAGE
+ RANGE-LOCAL ON-DEMAND ROW PATCH
+ NO PER-ROW Vec<u8> ALLOCATION
+ NO O(TILE×ROW) SPAN METADATA
+ VIRTUAL SOURCE DIGEST PARITY
+ PARAMETER / SEGMENT DIGEST PARITY
+ OBJECTIVE PROBE SEMANTIC PRESERVATION
+ CF1 / CF2 / CF3 / CF4 PRESERVATION
+ NO PROBE DISABLE CHEAT
```

---

## 1. Parent physical blocker

The admitted parent physical campaign has already demonstrated CF1/CF2/CF3 execution and reaches the exact sparse Adam overlay coverage seal:

```text
[ASH-RAM36-HIMUON-SPARSE-ADAM-OVERLAY-COVERAGE-R1B]
coverage_entries=47
complete_entries=47
incomplete_entries=0
written_elements=197761024
expected_elements=197761024
parameter_local_gap_count=0
parameter_local_replay_count=0
parameter_local_overrun_count=0
verdict=EXACT
```

The next observed failure is:

```text
memory allocation of 536870912 bytes failed
```

`536870912 == 512 MiB`.

The parent objective-probe representation expands every 16x16 sparse tile overlay into sixteen persistent row spans. Each row span owns a `Vec<u8>` containing the 64-byte row payload. This creates O(tile × row) span metadata and per-row heap allocations before the objective-probe virtual source is consumed.

CF5 removes that representation expansion without disabling or weakening the objective probe.

---

## 2. Core authority law

```text
COPY OF THE VIRTUAL SOURCE IS NOT AUTHORITY.

THE AUTHORITY IS:
BASE PACKED WEIGHT SOURCE
+
ADMITTED SPARSE TILE OVERLAYS.
```

A sparse objective-probe tile remains a single tile-native object. Row bytes are derived only when a requested read range intersects that row.

Required production complexity:

```text
metadata = O(tile overlays)
```

Forbidden parent complexity:

```text
metadata = O(tile overlays × tile rows)
```

---

## 3. Tile payload sharing

`AshBpDkObjectiveProbeSparseTileOverlay::candidate_weight` is changed from:

```rust
Vec<f32>
```

to:

```rust
Arc<[f32; 256]>
```

The runtime overlay remains the owner of the admitted 16x16 candidate tile payload, while the compact projection clones only the `Arc` identity. The objective-probe projection does not duplicate 256 f32 candidate values for each tile.

Required:

```text
runtime tile payload
        ↓ shared Arc
compact projection tile
```

Forbidden:

```text
runtime tile payload
        ↓ deep clone
second 256-f32 tile payload
```

---

## 4. Compact projection authority

Production projection is represented by compact tile metadata equivalent to:

```rust
struct AshObjectiveProbeCompactTileCF5 {
    canonical_parameter_index: u32,
    tile_ordinal: u64,
    parameter_byte_offset: u64,
    parameter_byte_length: u64,
    row_start: u64,
    col_start: u64,
    rows: u32,
    cols: u32,
    row_stride_elements: u64,
    candidate_weight: Arc<[f32; 256]>,
    byte_start: u64,
    byte_end: u64,
}
```

`byte_start` and `byte_end` are coarse tile bounds used only to restrict range lookup. Exact patching remains row-local.

---

## 5. Row-span retirement

The production source must contain zero instances of the former materialization pattern:

```rust
spans.push(AshObjectiveProbeOverlaySpan { ... })
```

and zero objective-probe row allocations of:

```rust
Vec::with_capacity(64)
```

Required physical receipt fields:

```text
row_span_materialized_count=0
per_row_vec_allocation_count=0
```

---

## 6. Range-local patch authority

`read_range()` first reads the canonical base packed-weight bytes for the requested range.

It then:

1. binary-searches to the first tile whose coarse `byte_end` can intersect the range,
2. walks only subsequent candidate tiles until `tile.byte_start >= requested_end`,
3. derives at most one 64-byte stack row at a time,
4. patches only the exact byte intersection into the bounded caller result.

The temporary row representation is:

```rust
[0u8; 64]
```

on the stack, not a heap `Vec<u8>`.

Arbitrary unaligned byte ranges remain valid. A request intersecting only 1-3 bytes of one f32 must preserve the exact parent byte stream.

---

## 7. Read lookup complexity

Compact tiles are ordered by canonical physical byte start. Their coarse byte ends are required to remain monotonic.

Range lookup uses:

```rust
partition_point(|tile| tile.byte_end <= start)
```

therefore range lookup does not scan all prior model tiles for each requested segment.

Expected complexity is approximately:

```text
O(log(tile_count) + intersecting_tiles)
```

plus bounded row patch work.

---

## 8. Virtual source semantic preservation

For the same:

```text
base packed weight file
manifest
sparse tile overlays
```

CF5 must expose the same virtual bytes as the parent row-span projection.

Required parity domains:

```text
full virtual source digest
parameter digest
weight-segment digest
arbitrary requested byte range
```

No optimizer arithmetic, candidate values, objective evaluation policy, batch selection, stochastic policy, receipt logic or commit decision is changed.

---

## 9. Objective-probe policy preservation

CF5 MUST NOT close the allocation blocker by changing:

```text
ASH_BP_DK_FUSION_LOCAL_ONE_STEP_OBJECTIVE_PROBE_MODE
```

from the reproducing mode to `DISABLED`.

Likewise forbidden:

```text
QUALIFICATION -> OBSERVE
smaller model fixture
reduced overlay set
skipped candidate branch
```

The same physical objective-probe policy must remain enabled during CF5 qualification.

---

## 10. Runtime witness

CF5 emits:

```text
[ASH-EVE-MCU-R3H-CF5][objective-probe-compact-projection]
```

with fields including:

```text
tile_overlay_count=...
compact_tile_entry_count=...
legacy_logical_row_span_count=...
row_span_materialized_count=0
per_row_vec_allocation_count=0
parameter_digest_count=...
segment_digest_count=...
virtual_source_read_count=...
virtual_source_read_bytes=...
max_tiles_touched_per_read=...
virtual_source_digest_computed=true
parameter_segment_digest_complete=true
admitted=true
```

`legacy_logical_row_span_count` is a cardinality witness only. It is computed arithmetically and does not materialize row-span objects.

Required:

```text
compact_tile_entry_count == tile_overlay_count
row_span_materialized_count == 0
per_row_vec_allocation_count == 0
```

---

## 11. Differential tests

CF5 bakes eight focused test fixtures:

```text
r3h_cf5_compact_projection_matches_parent_bytes
r3h_cf5_no_row_span_materialization_and_shared_tile_payload
r3h_cf5_partial_unaligned_range_matches_parent
r3h_cf5_cross_tile_range_patch_matches_parent
r3h_cf5_sparse_gap_returns_base_bytes
r3h_cf5_virtual_source_digest_matches_parent_projection
r3h_cf5_duplicate_tile_identity_rejected
r3h_cf5_tile_out_of_parameter_bounds_rejected
```

The parent row behavior is represented only inside bounded test helpers. The production source contains no persistent row-span projection.

---

## 12. Existing static validator realignment

`tools/validate_ash_bp_dk_fusion_local_one_step_objective_probe_10_static.py` previously required the retired row-span representation as a static invariant.

CF5 changes those representation-specific checks to require:

```text
AshObjectiveProbeCompactTileCF5
range-local row derivation
no spans.push(AshObjectiveProbeOverlaySpan)
no Vec::with_capacity(64)
CF5 compact projection receipt
O(tile) compact tile allocation
```

No objective-probe semantic checks are removed.

With the historical compile-chain file temporarily supplied for validator execution, the CF5 tree introduced zero new static-validator failures relative to the CF4 + test-CF1 parent. The same nine pre-existing historical/hash checks remained failing in both trees.

This is static evidence only, not compile/runtime evidence.

---

## 13. CF1 preservation

CF1 Muon packed decomposition source remains byte-identical through the unchanged scheduler.

Required physical witness remains:

```text
[ASH-EVE-MCU-R3H-CF1][muon-packed-decompose]
gap_count=0
overlap_count=0
admitted=true
```

---

## 14. CF2 preservation

CF2 borrowed mapped readback remains unchanged.

Required:

```text
mapped_full_window_clone_count=0
mapped_full_window_clone_bytes=0
consumer_completed=true
unmap_after_consume=true
```

---

## 15. CF3 preservation

CF3 submission lease coalescing remains unchanged.

Required:

```text
copy_command_count >> coalesced source lease count
```

No return to one lease per copy command.

---

## 16. CF4 preservation

CF4 observer checkpoint streaming files remain byte-identical except for the pre-existing runtime overlay file that CF5 necessarily changes to share candidate tile payloads.

The canonical CF4 persistence machinery remains present:

```text
parameter-scoped mapped observer state readback
direct payload file streaming
incremental payload SHA-256
manifest metadata-only accumulation
```

CF5's purpose is to allow the physical campaign to reach that later authority.

---

## 17. BUFFER-AUTHORITY-INVENTORY-TEST-CF1 preservation

`buffer_authority_inventory.rs` remains byte-identical to the admitted test-isolation bake.

CF5 introduces no runtime dependency on the test-only observer lock.

---

## 18. Non-goals

CF5 does not claim to optimize or change:

```text
Muon math
AdamW math
HiMuon math
BP-DK policy thresholds
objective function
forward loss
GPU copy command count
R7A cache retention
CF4 checkpoint disk throughput
R3C commit semantics
RAM36 hard limit
```

---

## 19. Static bake seal

Parent layers:

```text
CF4 Full SHA-256:
63711ea3622ac61cc321cbb804542b82d55c01f0b7e65fb81583bd00af6614ea

BUFFER-AUTHORITY-INVENTORY-TEST-CF1 Overlay SHA-256:
6a73e3513f72e6ba464dffa3779edf936b3f710c92cb47d7c97b0beea20d2411
```

CF5 full:

```text
ASH_PASS3_EVE_MCU_R3H_CF5_BP_DK_OBJECTIVE_PROBE_COMPACT_TILE_PROJECTION_AUTHORITY_CODE_ONLY.zip
SHA-256:
22297d0866c61391e12a8cab8717aa9dcd504af60b30f831911745bf06fcc03a
Files: 8426
CRC: PASS
```

CF5 overlay:

```text
ASH_EVE_MCU_R3H_CF5_BP_DK_OBJECTIVE_PROBE_COMPACT_TILE_PROJECTION_AUTHORITY_OVERLAY_CODE_ONLY.zip
SHA-256:
d6c42ba8be580ca61b27a608fcb3de68c52d4bd373e8a715246e330f739560ab
Files: 3
CRC: PASS
```

Delta:

```text
ADD 0
MOD 3
DEL 0
```

Changed files:

```text
crates/base_train/src/bp_delta_k_fusion_local_one_step_objective_probe.rs
parent c9e093c1d6f9ef402e8e45f1c3eb47922016ef964d5242fdf9994bf5a0aa00a8
CF5    7d066935f4f44807b29ad08c3837600d85a6a63582725a3b1ef0eb280e2ca3f0

crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
parent 7ddbb86b638a3060fc3cd6ab610ff12f2c5185b08b7980905024f192000626f9
CF5    48099ce049f37ce0ac32433273e1f8701cd65d636206d8ee01dbf09146615948

tools/validate_ash_bp_dk_fusion_local_one_step_objective_probe_10_static.py
parent 34e7b52beaee95832d6e112656feec8f15c2f0a67609475f50d7fc72a418e20e
CF5    0cd2ebe8f5304a3c68f0a6ebd10378b061617be493faea21233d4a96a949581c
```

Preserved files include:

```text
production_multistep_loop_accumulation8_scheduler.rs
cd14a404060953818f490110490817af2e1f447f2f9f40ac1c51aa1da5cf9821

bp_delta_k_stale_observation_seal.rs
81d85c2209aaeda9131cf4e851e4ed742d7dd786111173cd1e6cec5a853b3e78

burn_webgpu_backend/src/bp_delta_k_local_observer.rs
acec57949dd61e3e974386b3e9f0e4201e1f70286bcdcd30d08925bfaae43559

burn_webgpu_backend/src/buffer_authority_inventory.rs
d038ce26a24af25d6ef68b3a6572a14f2512af27fc32e1747054334bcd9a1ac9
```

Code-only archive seal:

```text
Markdown files: 0
specs/ files:    0
artifacts/ files:0
```

Rust delimiters for both modified Rust files were statically balanced.

---

## 20. Evidence status at bake time

```text
SOURCE / STATIC             PASS
ARCHIVE                     PASS
STATIC VALIDATOR DELTA      PASS relative to parent baseline
RUST COMPILE                UNVERIFIED
RUNTIME TEST                UNVERIFIED
DIGEST PARITY TEST          UNVERIFIED
PHYSICAL CF5                UNVERIFIED
CF4 PHYSICAL REACHABILITY   UNVERIFIED
FULL CANARY                 UNVERIFIED
PERFORMANCE                 UNMEASURED
```

No compile, runtime or physical PASS is claimed by the bake environment because the bake container does not provide the Rust toolchain or target physical GPU runtime.

---

## 21. Physical completion law

CF5 is physically complete only when the same canary fixture that reproduced the parent 512 MiB failure demonstrates:

```text
1. objective probe remains enabled under the same policy.
2. CF5 compact projection receipt appears.
3. tile_overlay_count > 0.
4. compact_tile_entry_count == tile_overlay_count.
5. row_span_materialized_count == 0.
6. per_row_vec_allocation_count == 0.
7. admitted == true.
8. parent 536870912-byte objective-projection allocation does not recur at the same authority.
9. execution advances beyond the old blocker region.
10. preferably CF4 observer-checkpoint-stream is subsequently reached.
```

A later independent failure does not revoke CF5 physical admission if these conditions have already been positively witnessed.

---

## 22. Promotion tokens

Static / compile / regression:

```text
PASS_EVE_MCU_R3H_CF5_BP_DK_OBJECTIVE_PROBE_COMPACT_TILE_PROJECTION_AUTHORITY
```

Differential digest parity:

```text
PASS_EVE_MCU_R3H_CF5_OBJECTIVE_PROBE_VIRTUAL_SOURCE_DIGEST_PARITY
```

Physical:

```text
PASS_EVE_MCU_R3H_CF5_PHYSICAL_OBJECTIVE_PROBE_COMPACT_TILE_PROJECTION
```

Hold:

```text
HOLD_EVE_MCU_R3H_CF5_OBJECTIVE_PROBE_COMPACT_PROJECTION_PHYSICAL_CLOSURE_UNPROVEN
```

---

## 23. Final authority law

> EVE-MCU-R3H-CF5 preserves the BP-DK objective probe and the exact virtual candidate source it observes while retiring the row-span representation that expanded every sparse tile into persistent heap-backed row objects.
>
> A candidate tile remains one admitted tile payload shared by `Arc<[f32;256]>`. The projection stores only O(tile) compact geometry and shared payload identities. Requested virtual-source ranges derive intersecting row bytes on demand into a bounded 64-byte stack buffer and patch only the requested output range.
>
> No per-row `Vec<u8>` and no O(tile × row) span metadata is materialized. Full-source, parameter, segment and arbitrary-range byte semantics remain subject to exact differential parity qualification. Objective-probe policy, optimizer mathematics, CF1/CF2/CF3/CF4 authority, RAM36 policy, R3G completion and R3C commit semantics remain unchanged.
