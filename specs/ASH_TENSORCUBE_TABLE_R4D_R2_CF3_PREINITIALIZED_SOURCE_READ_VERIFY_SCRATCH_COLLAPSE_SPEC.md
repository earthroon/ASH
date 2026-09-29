# TENSORCUBE-TABLE-R4D-R2-CF3

## PREINITIALIZED SOURCE READ + VERIFY SCRATCH COLLAPSE

```text
TENSORCUBE-TABLE-R4D-R2-CF3

PREINITIALIZED SOURCE READ
+ VERIFY SCRATCH COLLAPSE

+ R4D-R2 / R4D-R2-CF2 / A01 / CF11 PRESERVATION
+ TRANSIENT SAME-SOURCE PROVENANCE
+ BUILDER IDENTITY + STORAGE REVISION BINDING
+ RANGE-LOCAL OVERWRITE INVALIDATION
+ DIRECT-HOST SAME-SOURCE READ ELISION
+ SAME-SOURCE APPEND VERIFY REREAD ELISION
+ UNPROVEN INITIALIZED RANGE EXACT PHYSICAL VERIFY
+ 64 KiB CF3 VERIFY SCRATCH
+ NO ACTIVE PER-RANGE VERIFY Vec
+ NO ACTIVE PER-VERIFY spool.try_clone()
+ PREINITIALIZED BYTE MISMATCH FAIL-CLOSED PRESERVATION
+ APPEND CURSOR / HASH / INITIALIZED-RANGE PRESERVATION
+ FLUSH / SYNC_ALL / FINAL MERGE PRESERVATION
+ NO GPU TRANSFER / WAIT / NUMERICAL CHANGE
```

## 1. Parent

Direct bake parent:

```text
ASH_PASS3_TENSORCUBE_TABLE_R4D_R2_CF2_MONOTONIC_SEGMENT_CURSOR_CHUNK_LOOKUP_COLLAPSE_CODE_ONLY.zip
```

CF3 OBSERVE/ACTIVE requires:

```text
R4D-R2     = ACTIVE
R4D-R2-CF2 = ACTIVE
```

Default CF3 mode is `OFF`.

## 2. Provenance authority

CF3 introduces `PreinitializedSourceReadR4DR2CF3`, bound to:

```text
builder identity
builder storage revision
one R2 chunk byte interval
same-source subranges
```

The witness is transient. It is not a generation-wide cache or durable receipt.

`ResidentWeightPackBuilder` gains process-local builder identity, storage revision, and reusable CF3 verify scratch. Mutation authorities that change storage or initialized-range meaning advance the revision. Pure reads do not.

## 3. Same-source base and overlay

When an R2 64 KiB chunk is populated from the initialized successor builder, the copied interval becomes same-source provenance.

For direct-host AdamW overlap:

- `ACTIVE`: if builder identity, storage revision, and byte range are exact, the second builder read is elided.
- `OBSERVE`: the builder range is physically compared against the already-present scratch bytes before parity is admitted.
- External/mapped base bytes never become builder provenance merely from route identity. Direct-host bytes are still physically read and only that copied subrange becomes same-source.

Host-demoted scratch overwrite invalidates provenance only for the exact overwritten byte interval.

## 4. Append verification

Migrated R2 chunks use `append_or_verify_initialized_r4d_r2_cf3`.

```text
ACTIVE + exact same-source proof
    -> physical reread skipped

otherwise
    -> exact physical compare
```

Uninitialized-range inherited-source/write policy is unchanged. Builder hasher and append cursor remain parent-authoritative.

`ResidentWeightPackBuilderPreinitializedByteMismatch` remains the canonical fail-closed mismatch.

## 5. Storage-class compare

CF3 comparison behavior:

```text
Full storage
    -> direct compare against existing allocation

Paged-COW resident dirty page
    -> direct page-slice compare

Paged-COW inherited source
    -> direct source_bytes compare

Paged-COW spooled dirty page
    -> builder-owned spool seek/read into bounded reusable scratch
```

The migrated spooled compare path does not call `spool.try_clone()` per verify read.

## 6. Scratch boundary

```text
R4D_R2_CF3_VERIFY_SCRATCH_BYTES
=
R4D_R2_ENCODE_SCRATCH_BYTES
=
64 KiB
```

This is the migrated CF3 path ceiling only.

Legacy `CF11_INITIALIZED_VERIFY_SCRATCH_BYTES_R1 = 16 MiB` remains present for OFF/unmigrated parent paths.

## 7. Evidence truth

CF3 attribution is atomic and separately records base reads, direct-host reads/elisions, append requested/elided/physical verify bytes, storage-class compare bytes, spool reads, spool clone count, no-clone witness count, verify scratch allocation/peak, provenance ranges/invalidation/revision mismatch, OBSERVE parity, and ACTIVE append count.

A zero spool clone count is not accepted from a default counter alone. ACTIVE requires a physically observed spooled-verify no-clone witness before `paged_spool_file_clone_count == 0` can participate in promotion.

ACTIVE also requires physical exercise of direct-host same-source elision, same-source append verify elision, and physical verify fallback.

## 8. Durability / GPU boundary

CF3 changes no:

```text
spool.flush
spool.sync_all
final candidate merge
candidate writer flush/sync_all
source retirement
sealed candidate reload
queue.submit
map_async
get_mapped_range
device.poll
PollType::Wait
copy_buffer_to_buffer
queue.write_buffer
optimizer/tensor numerical math
```

Durability I/O compaction remains R4D-R3 scope.

## 9. Actual bake delta

```text
MOD 3
ADD 2
DEL 0
```

Modified:

```text
crates/base_train/src/lib.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/ram_weight_pack_persistent_residency.rs
```

Added:

```text
crates/base_train/src/tensorcube_table_r4d_r2_cf3_preinitialized_source_read_verify_scratch_collapse.rs
tools/validate_ash_tensorcube_table_r4d_r2_cf3_preinitialized_source_read_verify_scratch_collapse_static.py
```

## 10. Source seals

```text
lib.rs
de2dfba392856a2fbc9da2dc4916e87a4d4b0c59a71e10252ac3b4d3822fb005

production_multistep_loop_accumulation8_scheduler.rs
3778af130d123073d7e96ed4e25b0762bd1866a7e5fcca195bb279151275081d

ram_weight_pack_persistent_residency.rs
1eafa5574843179646d13544ebd97d7d8800c0bcce1b703515867dca78bb680c

tensorcube_table_r4d_r2_cf3_preinitialized_source_read_verify_scratch_collapse.rs
1067512f39f5089baad126eef38559ef6bec4ef0f511cbb123ae1077787dde34

CF3 static validator
736c72f789de6c44c43a27ec9ec8aa43975fadcbea99b0b10e86a41f355fbc24
```

## 11. Static acceptance

```text
CF3        120/120 PASS
CF2        105/105 PASS
R4D-R2     140/140 PASS
A01         53/53 PASS
R4D-R1     145/145 PASS
CF8        136/136 PASS
CF7        151/151 PASS
R0B        178/178 PASS
R0A        104/104 PASS
CF6        135/135 PASS
CF5        127/127 PASS
CF4         67/67 PASS
CF3-slot    77/77 PASS
R4B-CF3    127/127 PASS
R1                 PASS
B06         63/63 PASS
CF11        64/64 PASS
```

No parent validator source was modified.

## 12. Protected graph

```text
Cargo.toml byte-identical to parent
Cargo.lock byte-identical to parent
WGSL parent/work = 321 / 321
WGSL changed/added/deleted = 0 / 0 / 0
```

## 13. Artifact seals

Overlay code-only ZIP:

```text
ASH_TENSORCUBE_TABLE_R4D_R2_CF3_PREINITIALIZED_SOURCE_READ_VERIFY_SCRATCH_COLLAPSE_OVERLAY_CODE_ONLY.zip
SHA-256 3a9824696a69b8c80d2151d434325ead8ce9edb3dd712560b240c4ec9dad348e
files=5
CRC=PASS
```

Full code-only ZIP:

```text
ASH_PASS3_TENSORCUBE_TABLE_R4D_R2_CF3_PREINITIALIZED_SOURCE_READ_VERIFY_SCRATCH_COLLAPSE_CODE_ONLY.zip
SHA-256 8ef8d9b7c015d40440dd0613effe93a42371c1028ee1240adf138ff6e0d6d1bb
files=8534
CRC=PASS
```

Both ZIPs contain zero:

```text
specs/
artifacts/
*SPEC.md
generated manifest JSON
__pycache__/pyc
```

## 14. Evidence state

```text
SOURCE       BAKED
STATIC       PASS
COMPILE      UNVERIFIED
RUNTIME      UNVERIFIED
PHYSICAL     UNVERIFIED
PERFORMANCE  UNVERIFIED
```

The bake environment has no `cargo` or `rustc`. No higher evidence grade is inferred.

## 15. Compile acceptance

```powershell
cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo check -p base_train --lib --release --locked -j 1
cargo build -p base_train --bin base_train --release --locked -j 1
```

All must PASS before COMPILE promotion.

## 16. Physical / performance successor

First qualify CF3 in `OBSERVE`, then `ACTIVE`, with same-builder base, same-source direct-host overlay, external-base direct-host overlay, provenance invalidation, physical verify fallback, resident/inherited/spooled Paged-COW compare, and exact candidate bytes/digests.

After physical closure:

```text
TENSORCUBE-TABLE-R4D-R2-CLOSE-R1
PHYSICAL / PERFORMANCE CLOSURE
```

Then measured durability evidence may enter R4D-R3.

## 17. Final law

> CF3 does not remove verification as a semantic requirement. It removes a second storage read only where the exact bytes were already obtained from the exact same builder state and remained unmodified.

> Same-source proof is bound to builder identity, storage revision, and byte range. Scratch overwrite invalidates only the touched range.

> Unproven initialized bytes continue to undergo exact physical comparison and mismatch remains fail-closed.

> The migrated verify path is bounded to 64 KiB and does not allocate a verify Vec per initialized interval or clone the spool file per verify read.

> CF11 durability barriers, final merge, candidate bytes/SHA, and source retirement remain unchanged.

> SOURCE and STATIC evidence do not claim COMPILE, RUNTIME, PHYSICAL, or PERFORMANCE closure.
