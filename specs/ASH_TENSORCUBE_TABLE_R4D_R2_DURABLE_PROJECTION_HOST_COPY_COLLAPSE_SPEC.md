# TENSORCUBE-TABLE-R4D-R2

## DURABLE PROJECTION HOST COPY COLLAPSE

```text
TENSORCUBE-TABLE-R4D-R2

DURABLE PROJECTION HOST COPY COLLAPSE

+ R4D-R1 / CF8 / CF7 / R0B / R0A PRESERVATION
+ RESIDENT SEQUENTIAL-PACK ZERO-COPY WINDOW VIEW
+ FILE FALLBACK BOUNDED-OWNED WINDOW PRESERVATION
+ MAPPED PROJECTION DIRECT CHUNK CONSUMPTION
+ FULL mapped.weight.to_vec() ELIMINATION IN ACTIVE
+ RESIDENT ADAM M/V BORROWED-SPAN AUTHORITY
+ R3B CANDIDATE M/V SPAN VISITOR
+ BOUNDED F32→LE ENCODE SCRATCH
+ FULL-WINDOW M/V SERIALIZATION Vec ELIMINATION
+ WEIGHT DELTA STATISTICS FUSION
+ WEIGHT BYTE RE-DECODE ELIMINATION
+ R3E BYTE-STREAM OBSERVATION
+ CF11 SUCCESSOR BUILDER STREAMING
+ PROJECTION D2H PRESERVATION / ATTRIBUTION
+ FLUSH / SYNC_ALL / RENAME PRESERVATION
+ NO WGSL CHANGE
```

## Purpose

R4D-R2 removes redundant host representations created after a resident source range or bounded mapped GPU projection already exists. It does **not** remove the required durable-projection D2H and does **not** change durability barriers.

Parent:

```text
TENSORCUBE-TABLE-R4D-R1
ADAMW STATUS DEVICE AGGREGATION
```

Primary physical targets are the full-trainable durable projection and resident-weight-successor materialization paths.

## Runtime Mode

```text
ASH_TENSORCUBE_TABLE_R4D_R2_MODE

OFF / DISABLED / 0
OBSERVE / OBSERVE_ONLY
ACTIVE / ACTIVE_VERIFIED / 1
```

Default is OFF. R2 OBSERVE/ACTIVE requires R4D-R1 ACTIVE.

Current bake behavior:

- OFF: parent materialized path.
- OBSERVE: parent materialized path remains authoritative; R2 attribution/baseline evidence is available. This bake does not claim an independent shadow durable-byte parity engine.
- ACTIVE: zero-copy/span/streaming durable projection is authoritative for migrated paths.

## Resident SequentialPack Window

`SequentialPackF32Reader` now supports an Arc-backed resident range view and a bounded owned-file window. Resident reads no longer require a full range `.to_vec()` on the migrated ACTIVE durable path. File fallback remains bounded-owned. Cursor/read accounting is preserved.

Legacy `read_f32()` remains a compatibility wrapper.

## Mapped Projection Copy Collapse

The existing R3H-CF2 GPU→host mapped projection remains parent-authoritative and visible in D2H accounting.

ACTIVE consumes the mapped `&[u8]` directly in bounded chunks instead of cloning the complete mapped window before overlay/hash/write/builder work.

R2 therefore claims:

```text
post-map full-window host clone removed
```

not:

```text
projection D2H removed
```

## Weight Streaming

The migrated ACTIVE path processes final projected weight with bounded chunking and fans the same canonical bytes into:

```text
SequentialPackWriter
ResidentWeightPackBuilder
weight pack hasher
parameter hasher
segment hasher
weight journal / R3E observer
fused update statistics
```

Existing direct-host and host-demoted Adam weight overlay semantics are preserved.

No complete 16 MiB mutable projected-weight Vec is required.

## Adam M/V Span Authority

`RamResidentAdamMv` adds R2 span-oriented APIs.

For presealed R3B candidates, `visit_candidate_logical_spans_r4d_r2(...)` emits borrowed M/V spans:

```text
Full A/B
    candidate M/V borrowed span

RouteSparse MuonInherited
    committed M/V borrowed span

RouteSparse ExplicitAdamW
    compact candidate-overlay borrowed span
```

No full reconstructed M/V window is required.

For non-presealed resident candidate fill, `write_committed_candidate_span_r4d_r2(...)` uses bounded committed-source chunks rather than a full 16 MiB M/V clone.

## Bounded Encoding

```text
R4D_R2_ENCODE_SCRATCH_BYTES = 64 KiB
```

M/V f32 values are encoded to little-endian bytes in bounded reusable chunks. Full-window `m_bytes` / `v_bytes` vectors are removed from the migrated ACTIVE path.

The 64 KiB limit describes LE-byte encoding scratch. The bounded non-presealed committed-source M/V bridge uses bounded f32 chunks separately and is not misreported as the same allocation.

## Statistics Fusion

The parent durable path could reconstruct final weight bytes and later decode them again for:

```text
update_nonzero_element_count
update_sum_squares
update_max_abs
```

R2 accumulates those values while selecting/emitting the final projected weight.

Parent precision is preserved:

```text
delta = f32
sum_squares accumulation = f64
max_abs = f32
```

ACTIVE requires projected-weight statistics rescan bytes = 0.

## R3E / Journal Byte APIs

Weight journal and durable-stream authorities gain byte-oriented R2 entrypoints so source/target bytes can be consumed directly without reconstructing a complete f32 window.

Journal offset, codec, digest and source/target cardinality semantics remain unchanged.

## CF11 Successor Preservation

`ResidentWeightPackBuilder` remains the successor byte authority. R2 may append/verify multiple ordered chunks for one logical window, but aggregate bytes must equal the parent projected window exactly.

CF11 initialized-range verification, paged-COW behavior, successor digest and source-retirement semantics remain preserved.

## Durability Boundary

`SequentialPackWriter::finalize()` remains:

```rust
self.file.flush()?;
self.file.sync_all()?;
fs::rename(&self.partial_path, &self.final_path)?;
```

R2 does not optimize, coalesce, reorder or remove these barriers. That scope belongs to R4D-R3.

## No New GPU Transfer / Wait

The R2 module adds no new:

```text
map_async
get_mapped_range
PollType::Wait
device.poll
queue.write_buffer
queue.submit
copy_buffer_to_buffer
```

Existing projection D2H remains separately attributed.

## ACTIVE Fail-Closed

The migrated ACTIVE path fails closed if it observes:

```text
resident sequential owned full copy
resident full-window f32 materialization
mapped full-weight clone
resident Adam full-window clone
R3B candidate full-window clone
full-window M/V serialization Vec
projected-weight statistics rescan
encode scratch > 64 KiB
source alias leak
```

Terminal receipt:

```text
tensorcube_table_r4d_r2_durable_projection_host_copy_collapse_receipt.json
```

Compact log:

```text
[ASH-TENSORCUBE-TABLE-R4D-R2][durable-projection-host-copy-collapse]
```

Pass token:

```text
PASS_TENSORCUBE_TABLE_R4D_R2_DURABLE_PROJECTION_HOST_COPY_COLLAPSE
```

## Actual Code Delta

```text
MOD 5
ADD 2
DEL 0
```

Modified:

```text
crates/base_train/src/lib.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/ram_resident_adam_mv.rs
crates/base_train/src/trainable_generation_weight_payload_retirement_r3e.rs
crates/base_train/src/weight_successor_durable_journal_r3e.rs
```

Added:

```text
crates/base_train/src/tensorcube_table_r4d_r2_durable_projection_host_copy_collapse.rs
tools/validate_ash_tensorcube_table_r4d_r2_durable_projection_host_copy_collapse_static.py
```

No parent validator required successor modification.

## Build Graph / WGSL Seal

```text
Cargo.toml byte-identical
Cargo.lock byte-identical
parent WGSL files = 321
work WGSL files = 321
WGSL changed = 0
WGSL added = 0
```

## Static Acceptance

```text
PASS_TENSORCUBE_TABLE_R4D_R2_DURABLE_PROJECTION_HOST_COPY_COLLAPSE_STATIC checks=140
PASS_TENSORCUBE_TABLE_R4D_R1_ADAMW_STATUS_DEVICE_AGGREGATION_STATIC checks=145
PASS_TENSORCUBE_TABLE_R4C_CF8_RESIDENT_VALIDATION_RECEIPT_CACHE_STATIC checks=136
PASS_TENSORCUBE_TABLE_R4C_CF7_PARTIAL_VRAM_HOT_WEIGHT_REUSE_STATIC checks=151
PASS_TENSORCUBE_TABLE_R4D_R0B_GRADIENT_OBSERVABILITY_DEVICE_AGGREGATION_STATIC checks=178
PASS_TENSORCUBE_TABLE_R4D_R0A_HOT_PATH_PIPELINE_RESIDENCY_STATIC checks=104
PASS_TENSORCUBE_TABLE_R4C_CF6_DIRECT_BOUNDED_WEIGHT_UPLOAD_STATIC checks=135
PASS_TENSORCUBE_TABLE_R4C_CF5_HOST_COPY_COLLAPSE_STATIC checks=127
PASS_TENSORCUBE_TABLE_R4C_CF4_HOST_DEVICE_IO_ROUNDTRIP_ATTRIBUTION_STATIC checks=67
PASS_TENSORCUBE_TABLE_R4C_CF3_SLOT_LIFECYCLE_STATIC checks=77
PASS_TENSORCUBE_TABLE_R4B_CF3_FULL_ROUTE_HOST_LEDGER_COMPACTION_STATIC checks=127
PASS_TENSORCUBE_TABLE_R1_CF1_IMMUTABLE_BYTE_ACCOUNTING_STATIC
PASS_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF1_STATIC checks=63
PASS_EVE_MCU_R3H_CF11_PAGED_COW_CANDIDATE_WEIGHT_SUCCESSOR_STATIC checks=64
```

## Artifact Seals

```text
Overlay code-only ZIP
SHA-256 8ba59835cdd11aa94d850b1d197c59986593275060196444e2b011e2461d4a63
files=7
CRC=PASS

Full code-only ZIP
SHA-256 9d3323de5efdb2ebbe85faa270e4dff1ca16dfda5c5a41e6495c832f2dbd30cf
files=8529
CRC=PASS
```

## Evidence State

The bake environment has no Rust toolchain.

```text
SOURCE       BAKED
STATIC       PASS
COMPILE      UNVERIFIED IN BAKE ENVIRONMENT
RUNTIME      UNVERIFIED AFTER R2
PHYSICAL     UNVERIFIED AFTER R2
PERFORMANCE  UNVERIFIED
```

No compile/runtime/speedup claim is inferred from static evidence.

## Local Compile Acceptance

```powershell
cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo check -p base_train --lib --release --locked -j 1
cargo build -p base_train --bin base_train --release --locked -j 1
```

## Physical Acceptance

ACTIVE physical qualification must establish:

```text
R2 path exercised
resident full source copy = 0
resident full f32 materialization = 0
mapped full-weight clone = 0
resident M/V full-window clone = 0
R3B candidate full-window clone = 0
full-window serialization Vec = 0
statistics rescan = 0
encode scratch <= 64 KiB
projection D2H remains correctly attributed
weight/M/V durable byte and digest authorities exact
CF11/B06 generation closure PASS
```

## Performance Boundary

Same-source A/B compares R4D-R1 parent + R2 OFF against the same runtime + R2 ACTIVE.

Measure host allocation count/bytes, peak private bytes, copy bytes, CPU time, projection-consume wall time, serialization wall time, durable-write wall time, optimizer-step wall time and generation wall time.

`sync_all` wall time remains a separate category. If it dominates after R2, that is evidence for R4D-R3.

No exact speedup claim before physical A/B.

## Successor

```text
TENSORCUBE-TABLE-R4D-R3
GENERATION DURABILITY I/O COMPACTION
```

## Final Law

> R4D-R2 does not remove durable projection or its required D2H. It removes redundant host ownership after the source or mapped projection already exists.

> Resident source bytes remain borrowed, Adam M/V is emitted as ordered spans, final bytes use bounded encoding scratch, and writer/hash/journal/statistics consumers share the same canonical stream.

> Durable bytes, digest domains, parameter order, coverage, flush, sync_all, rename and crash-consistency semantics remain parent-authoritative.
