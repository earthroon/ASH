# EVE-MCU-R3H-CF1

## MUON PACKED PHYSICAL SPAN DECOMPOSITION

**Revision:** EVE-MCU-R3H-CF1  
**Class:** Muon packed-geometry repair / physical copy decomposition authority  
**Parent:** EVE-MCU-R3H

```text
+ LOGICAL ROUTE / PHYSICAL CONTIGUITY SEPARATION
+ TILE-MAJOR PACKED SPAN DECOMPOSITION
+ CONTIGUOUS COPY-SUBSPAN AUTHORITY
+ EXACT LOGICAL COVERAGE
+ GAP / OVERLAP CLOSURE
+ EXISTING NONCONTIGUOUS FAIL-CLOSED PRESERVATION
+ NO PACKED LAYOUT CHANGE
+ NO MUON MATH CHANGE
+ NO BP-DK POLICY CHANGE
+ NO R3H LIFETIME POLICY CHANGE
```

## 1. Parent physical failure

Parent physical canary reached:

```text
EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_FIRST_FAILURE:
RamAdamTransactionalCandidateExecutionFailed:
E_MCU_FULL_DURABLE_R1_MUON_NONCONTIGUOUS_ROUTE
```

Before the failure, BP-DK-R3 was physically operating in `RUNTIME_IDENTITY` mode with `full_payload_sha_count=0`, `full_candidate_d2h_bytes=0`, and `host_candidate_materialization_count=0`.

CF1 therefore repairs only the Full-Durable/R3H Muon logical-to-packed copy projection and does not reopen BP-DK policy.

## 2. Root cause

The parent path used logical Muon route continuity as if it implied physical packed-buffer continuity.

The canonical packed mapping is 16×16 tile-major. For a logical row spanning multiple horizontal tiles, logically adjacent columns cross a tile boundary and therefore jump in packed address space.

Example:

```text
logical row: 0..15 | 16..31
packed row:  0..15 | 256..271
```

Therefore:

```text
logical contiguous != physically packed contiguous
```

The parent guard was correct for one physical copy, but the wrong object was being validated: the whole logical route instead of each real contiguous packed subspan.

## 3. Core law

```text
LogicalMuonRoute
    -> PackedPhysicalSpan[1..N]
    -> N copy_buffer_to_buffer commands
    -> one existing projection-window submission
```

Logical optimizer ownership remains unchanged.

Physical copy authority is decomposed only where canonical packed indices stop increasing by exactly one.

## 4. Logical route authority preservation

The existing `ProductionMuonRuntime::route_span()` implementation is byte-preserved.

The existing `ProductionMuonRuntime::packed_index_for_logical()` implementation is byte-preserved.

The TensorCube local Muon packed ABI and 16×16 tile constants remain canonical.

No fix of the form:

```text
route_span = min(route_span, tile_width)
```

is admitted.

## 5. New physical span authority

The scheduler now contains:

```text
MuonPackedPhysicalSpanR3HCF1
logical_muon_tile_row_spans_r3h_cf1(...)
decompose_muon_logical_route_to_packed_spans_r3h_cf1(...)
```

Each physical span binds:

```text
logical_start
logical_count
packed_start
```

For every span, the existing noncontiguous fail-closed condition is still enforced:

```text
packed_last == packed_start + logical_count - 1
```

## 6. Canonical tile-boundary decomposition

Logical routes are split at the canonical `TENSORCUBE_LOCAL_MUON_TILE_COLS` boundary.

The production helper then validates each produced span against the canonical `packed_index_for_logical()` authority.

This preserves an optimized O(number_of_physical_spans) production decomposition while retaining exact mapping validation.

The canonical tile constants are imported from:

```text
crate::tensorcube_local_muon_optimizer::
    TENSORCUBE_LOCAL_MUON_TILE_COLS
    TENSORCUBE_LOCAL_MUON_TILE_ROWS
```

No independent packed layout ABI is introduced.

## 7. Fail-closed coverage

The helper rejects:

```text
empty logical route
invalid tile geometry
logical route crossing a row
route outside Muon packed domain
missing packed start/last index
physical subspan noncontiguity
logical gap/overlap
redundant physical split
aggregate coverage drift
```

Aggregate completion requires:

```text
covered_elements == logical_count
expected_next_logical == route_end
gap_count == 0
overlap_count == 0
```

## 8. Guard preservation

Both parent callsite-specific guards remain present:

```text
E_MCU_FULL_DURABLE_R1_MUON_NONCONTIGUOUS_ROUTE
E_R3H_SUCCESSOR_MUON_NONCONTIGUOUS_ROUTE
```

The Full-Durable guard is not deleted or weakened.

The R3H successor materialization path now uses the same physical-span SSOT, preventing the same packed-contiguity bug from reappearing after the first parent failure point.

## 9. Full-Durable projection adoption

The parent Full-Durable Muon path previously emitted one `FullTrainableProjectionCopyR1` per logical route.

CF1 emits one copy entry per physical packed span.

For each span:

```text
source_offset_bytes = packed_start * 4
target_offset_bytes = logical-window offset + span logical-relative offset
byte_count          = logical_count * 4
```

The logical target layout therefore remains linear even when packed source addresses jump between tile-major regions.

## 10. R3H successor materialization adoption

`materialize_resident_weight_successor_from_target_device_r3h()` uses the same decomposition helper.

The successor still materializes from the already-produced target device generation.

No persistent weight reload, optimizer replay, or alternate packed mapping is added.

## 11. Submission semantics

CF1 increases copy-command cardinality where one logical route crosses horizontal tile boundaries.

It does not create one GPU submission per span.

All subspans remain entries in the existing `copies` vector and are encoded into the existing projection-window command encoder before the existing tracked submission.

No new `wait_for_submission_exact` callsite is introduced.

The existing logical `successor_gpu_projection_entry_count` semantics are preserved: one Muon logical projection route still contributes exactly one logical projection entry even when it decomposes into multiple physical copy commands. Physical `copy_command_count` is reported separately by the CF1 witness and is not reinjected into logical topology counters.

## 12. Runtime witness

CF1 emits:

```text
[ASH-EVE-MCU-R3H-CF1][muon-packed-decompose]
```

with:

```text
site
parameter_index
logical_start
logical_count
physical_span_count
copy_command_count
covered_elements
gap_count=0
overlap_count=0
admitted=true
```

A previously failing multi-tile logical route should physically show:

```text
physical_span_count > 1
copy_command_count == physical_span_count
admitted=true
```

## 13. Unit fixtures baked into scheduler source

Added compile-time/runtime unit fixtures:

```text
r3h_cf1_two_horizontal_tiles_decompose
r3h_cf1_partial_start_decompose
r3h_cf1_non_multiple_width_decompose
r3h_cf1_route_crossing_row_rejected
```

The 50-column fixture seals:

```text
16 + 16 + 16 + 2 == 50
```

without copying tile padding.

## 14. Static physical-layout simulation

Bake qualification also replayed the canonical 16×16 tile-major mapping over multiple full-tile row/column geometries, partial starts, single-span routes, multi-span routes, and non-multiple logical widths.

For every generated span:

```text
packed_last == packed_start + span_count - 1
```

and for adjacent decomposed spans:

```text
next.logical_start == previous.logical_end
next.packed_start != previous.packed_end + 1
```

Result:

```text
SIMULATION_PASS
```

This is static bake evidence, not a substitute for Rust compile or GPU physical replay.

## 15. Source scope

Code delta:

```text
ADD 0
MOD 1
DEL 0

MOD
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
```

Byte-preserved key parent files:

```text
crates/base_train/src/tensorcube_local_muon_production_callsite_adoption.rs
crates/base_train/src/tensorcube_local_muon_optimizer.rs
crates/base_train/src/ram36_process_budget.rs
crates/base_train/src/resident_weight_replacement_authority_r3h.rs
```

## 16. Static seals

```text
decomposition helper definitions = 1
decomposition production callsites = 2
r3h_cf1 unit fixtures = 4
Full-Durable NONCONTIGUOUS guard refs = 1
R3H successor NONCONTIGUOUS guard refs = 1
new wait_for_submission_exact callsites = 0
new ResidentWeightPack::load_once callsites = 0
route_span callsite cardinality delta = 0
changed Rust delimiter balance = PASS
```

The production scheduler SHA-256 after bake is:

```text
0d6e2491d7fdb5de14795faedb0185de40f9f5173ae20beb60425c5e8a623b22
```

## 17. Parent byte-preservation hashes

```text
tensorcube_local_muon_production_callsite_adoption.rs
parent/work:
d50e48a515dee72e84ea4939c595610702bc2b322aeabf9412b92f1c2b6f54af

 tensorcube_local_muon_optimizer.rs
parent/work:
067f601397a8ff372b095f22b4f63330753702fbe998f0d0bccba71d4d8345b9

ram36_process_budget.rs
parent/work:
0394d326e5fddf14501db21412b98a9b4ac9d0377529daee9317baeac0fd4d3e

resident_weight_replacement_authority_r3h.rs
parent/work:
37079e72dc4c1a02ea53a410f51b35798a04d833ecb2aaac674241d7e3e4c497
```

## 18. Baked artifacts

Full code-only archive:

```text
ASH_PASS3_EVE_MCU_R3H_CF1_MUON_PACKED_PHYSICAL_SPAN_DECOMPOSITION_CODE_ONLY.zip
SHA-256 f7acb57ad1fd8f682b52738e851cfd8a13503f0e22205296d732051b12e135be
Files 8426
CRC PASS
```

Overlay:

```text
ASH_EVE_MCU_R3H_CF1_MUON_PACKED_PHYSICAL_SPAN_DECOMPOSITION_OVERLAY_CODE_ONLY.zip
SHA-256 d948e26f3a518485abb1700ef1b163720d281f872e861912a30a534903bd0637
Files 1
CRC PASS
```

Both code archives contain:

```text
specs/    0
artifacts/ 0
*.md       0
```

## 19. Evidence state at bake time

The bake environment has no Rust toolchain.

Therefore:

```text
SOURCE / STATIC   PASS
PACKED-LAYOUT SIM PASS
ARCHIVE           PASS
COMPILE           UNVERIFIED
RUNTIME-TEST      UNVERIFIED
PHYSICAL          UNVERIFIED
PERFORMANCE       UNMEASURED
```

No compile, runtime, or GPU physical claim is made by the bake environment.

## 20. Compile qualification

Required:

```text
cargo test -p base_train --lib --locked r3h_cf1_
cargo test -p base_train --lib --release --locked r3h_cf1_
cargo test -p base_train --lib --release --locked r3h_
cargo test -p base_train --lib --release --locked r3g_r2_
cargo test -p base_train --lib --release --locked bp_dk_r3_
cargo build -p base_train --bin base_train --release --locked -j 1
```

Compile/regression promotion token:

```text
PASS_EVE_MCU_R3H_CF1_MUON_PACKED_PHYSICAL_SPAN_DECOMPOSITION
```

## 21. Physical qualification

Re-seal native CF1 for the rebuilt release binary, then run the existing physical canary:

```text
--eve-mcu-close-r2-phys-canary-r1
```

Required positive evidence:

```text
[ASH-EVE-MCU-R3H-CF1][muon-packed-decompose]
physical_span_count > 1        # at least one prior multi-tile route
copy_command_count == physical_span_count
covered_elements == logical_count
gap_count=0
overlap_count=0
admitted=true
```

Required negative evidence:

```text
E_MCU_FULL_DURABLE_R1_MUON_NONCONTIGUOUS_ROUTE    absent on valid decomposition
E_R3H_SUCCESSOR_MUON_NONCONTIGUOUS_ROUTE          absent on valid decomposition
E_MCU_FULL_DURABLE_R1_MUON_PACKED_SPAN_DECOMPOSITION_DRIFT absent
```

The canary must progress beyond the old failure point and either reach R3H/R3G/R3C closure or expose the next independent blocker.

Physical promotion token:

```text
PASS_EVE_MCU_R3H_CF1_PHYSICAL_MUON_PACKED_SPAN_DECOMPOSITION
```

Hold token:

```text
HOLD_EVE_MCU_R3H_CF1_MUON_PACKED_ROUTE_PHYSICAL_CLOSURE_UNPROVEN
```

## 22. Explicit non-claims

CF1 does not claim to fix:

```text
HiMuon target backing lifetime
R7A retained VRAM page caching
GPU allocator trimming
long-horizon VRAM stability
R3H RAM36 replacement closure
```

Those remain separate residency authorities.

## 23. Completion law

R3H-CF1 is complete only when logical Muon ownership is unchanged, every logical Muon route is decomposed into the exact physically contiguous packed subspans required by canonical 16×16 tile-major layout, aggregate logical coverage is exact with zero gap/overlap, each emitted copy range is physically contiguous, both Full-Durable and R3H successor paths use one shared decomposition authority, no per-span submission/wait is introduced, no packed ABI/Muon math/BP-DK/R3H lifetime policy changes occur, and the physical canary progresses beyond the parent NONCONTIGUOUS_ROUTE failure.

## 24. Final authority law

> EVE-MCU-R3H-CF1 does not redefine a logical Muon route to make it look physically contiguous. It preserves the logical route and materializes the exact set of physical packed subspans that actually exist.
>
> The existing noncontiguous guard remains fail-closed and is applied to each physical span. The union of admitted spans must exactly equal the original logical route, with no gap, overlap, tile padding, packed-address fiction, extra GPU wait, or optimizer semantic drift.
