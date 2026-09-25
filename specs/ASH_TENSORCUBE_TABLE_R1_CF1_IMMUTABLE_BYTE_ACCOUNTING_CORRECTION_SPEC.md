# TENSORCUBE-TABLE-R1-CF1

## IMMUTABLE COLUMN BYTE ACCOUNTING CORRECTION
## + 11×U32 / 11×U64 EXACT COLUMN ACCOUNTING
## + ACTUAL UPLOAD-BYTE PARITY ORACLE
## + MUTABLE STATUS EXCLUSION PRESERVATION
## + GPU BUFFER SIZE AUTHORITY PRESERVATION
## + RECEIPT BYTE TRUTH REPAIR
## + NO GPU LAYOUT CHANGE
## + NO TABLE IDENTITY CHANGE

## 0. Revision

```text
Patch ID:
TENSORCUBE-TABLE-R1-CF1

Canonical name:
ASH-BASETRAIN-TENSORCUBE-TABLE-R1-CF1-
IMMUTABLE-COLUMN-BYTE-ACCOUNTING-CORRECTION-
11-U32-11-U64-EXACT-COLUMN-ACCOUNTING-
ACTUAL-UPLOAD-BYTE-PARITY-ORACLE
```

Direct implementation parent:

```text
ASH_PASS3_TENSORCUBE_TABLE_R4B_CF3_FULL_ROUTE_HOST_LEDGER_COMPACTION_CODE_ONLY.zip
SHA-256:
7d564ab3acbec3829ea30226f359a8d1ec3dbd3d3c5541417cb7db6a0bd3e736
files=8508
CRC=PASS
```

Class:

```text
ACCOUNTING CORRECTION
RECEIPT TRUTH REPAIR
STATIC PARITY GUARD

NO GPU BUFFER LAYOUT CHANGE
NO GPU ALLOCATION ALGORITHM CHANGE
NO ROW SCHEMA CHANGE
NO COLUMN ORDER CHANGE
NO TABLE DIGEST CHANGE
NO TRAINING MATH CHANGE
NO OPTIMIZER MATH CHANGE
```

## 1. Confirmed parent debt

Historical source reported immutable bytes using:

```text
11 * 4 + 10 * 8
= 124 bytes / row
```

Actual immutable upload inventory is:

```text
11 immutable u32 columns
11 immutable logical-u64 columns
```

The exact immutable payload is therefore:

```text
11 * 4 + 11 * 8
= 132 bytes / row
```

Historical accounting undercounted by:

```text
8 bytes / row
```

## 2. Exact immutable u32 inventory

```text
parameter_index
tensorcube_ordinal
tensorcube_row
tensorcube_col
valid_rows
valid_cols
wave_ordinal
weight_span_count
bpdk_parameter_record_index
route_kind
flags
```

Count:

```text
11
```

## 3. Exact immutable logical-u64 inventory

```text
canonical_job_ordinal
queue_generation
queue_epoch
source_generation
target_generation
packed_weight_source
packed_momentum_source
orthogonal_update_source
logical_momentum_destination
physical_successor_destination
weight_span_start
```

Count:

```text
11
```

Each logical-u64 value is still uploaded as two u32 words:

```text
lo u32
hi u32
```

therefore it accounts for 8 bytes per row.

## 4. Mutable status remains separate

```text
lifecycle_status
```

remains the one mutable u32 column.

Canonical per-row accounting:

```text
immutable = 132 bytes
mutable lifecycle status = 4 bytes
```

No double accounting is introduced.

## 5. Materialized source constants

CF1 adds:

```text
TENSORCUBE_TABLE_R1_CF1_PATCH_ID
TENSORCUBE_TABLE_R1_CF1_IMMUTABLE_BYTE_ACCOUNTING_CORRECTED

TENSORCUBE_TABLE_R1_IMMUTABLE_U32_COLUMN_COUNT = 11
TENSORCUBE_TABLE_R1_IMMUTABLE_U64_COLUMN_COUNT = 11
TENSORCUBE_TABLE_R1_MUTABLE_U32_COLUMN_COUNT = 1

TENSORCUBE_TABLE_R1_IMMUTABLE_ROW_BYTES = 132
TENSORCUBE_TABLE_R1_MUTABLE_STATUS_ROW_BYTES = 4
```

The historical anonymous `11 * 4 + 10 * 8` expression is retired.

## 6. Checked accounting

`estimated_immutable_row_bytes_r1(row_count)` now uses:

```text
row_count
.checked_mul(TENSORCUBE_TABLE_R1_IMMUTABLE_ROW_BYTES)
```

with the existing fail-closed overflow authority:

```text
E_TENSORCUBE_TABLE_R1_IMMUTABLE_BYTES_OVERFLOW
```

Zero-row arithmetic still returns zero; actual GPU table admission continues to reject an empty upload through its separate production guard.

## 7. Upload-byte parity oracle

CF1 materializes:

```text
expected_immutable_gpu_upload_bytes_r1(row_count)
```

which derives the expected immutable byte count from:

```text
row_count × 11 × size_of::<u32>()
+
row_count × 11 × size_of::<u64>()
```

This binds the accounting truth to the exact column type composition rather than only to a literal `132` assertion.

## 8. Physical buffer authority preserved

Actual WGPU buffers continue to be created with:

```rust
let bytes = bytemuck::cast_slice(values);

size: bytes.len() as u64
```

and populated by:

```rust
queue.write_buffer(&buffer, 0, bytes)
```

Therefore CF1 repairs receipt/accounting truth only.

It does NOT repair an undersized physical buffer and does not change actual buffer allocation size.

## 9. GPU representation preserved

Logical-u64 upload remains:

```rust
words.push(value as u32);
words.push((value >> 32) as u32);
```

CF1 does not change:

```text
SoA column count
column ordering
u64 lo/hi encoding
BufferUsage
binding layout
GPU ABI
WGSL
```

## 10. Table identity preserved

`immutable_table_digest_r1(...)` remains unchanged.

The digest still binds logical table content and existing lineage/authority inputs, not byte-accounting metadata.

CF1 does not bump the TensorCube Table R1 schema or alter row identity.

## 11. Receipt effect

For row count `R`:

```text
immutable_table_bytes = R * 132
mutable_status_bytes = R * 4
```

Existing total law remains:

```text
total_table_bytes
=
immutable_table_bytes
+ mutable_status_bytes
+ parameter_authority_bytes
+ weight_span_table_bytes
```

`parameter_authority_bytes` and `weight_span_table_bytes` are unchanged and out of CF1 scope.

## 12. Unit-test source materialized

Source includes:

```text
tensorcube_table_r1_cf1_immutable_column_accounting_exact
tensorcube_table_r1_cf1_immutable_column_accounting_overflow_fails_closed
```

The tests bind:

```text
immutable u32 count = 11
immutable u64 count = 11
mutable u32 count = 1
immutable row bytes = 132
mutable status row bytes = 4
1 row immutable = 132
3 rows immutable = 396
upload-byte oracle for 3 rows = 396
0 rows accounting = 0
overflow = fail closed
```

These Rust tests are source-materialized but not executed in the bake environment.

## 13. Static validator

New validator:

```text
tools/validate_ash_tensorcube_table_r1_cf1_immutable_byte_accounting_static.py
```

It verifies:

```text
CF1 patch marker
11 immutable u32 count
11 immutable u64 count
1 mutable u32 count
checked 132-byte accounting
actual upload-byte oracle
old 124-byte formula absent
old 10-u64 comment absent
bytes.len() physical buffer authority preserved
queue.write_buffer authority preserved
u64 lo/hi representation preserved
lifecycle status separate
actual upload call inventory = 12 u32 columns total
    (11 immutable + 1 mutable)
actual upload call inventory = 11 u64 columns
unit-test source present
```

Parent R1 validator is maintained to require the corrected accounting constants.

## 14. Exact implementation delta

Compared with the direct parent:

```text
MOD 2
ADD 1
DEL 0
```

Modified production source:

```text
crates/base_train/src/tensorcube_table_r1.rs
```

Modified parent validator:

```text
tools/validate_ash_tensorcube_table_r1_static.py
```

Added validator:

```text
tools/validate_ash_tensorcube_table_r1_cf1_immutable_byte_accounting_static.py
```

No scheduler, R4A, R4B, R4C, optimizer, WGPU kernel or vendor source changed.

## 15. Source SHA-256

```text
637f1b3671efad50e70f13747abfd3b325c7f5c864f67e067973a963ab4016e2  crates/base_train/src/tensorcube_table_r1.rs
7361ec5a7d62c38c2b4bef7ccd16c5ea4f1e09ce243c5a615b245c00f2d7b8c2  tools/validate_ash_tensorcube_table_r1_static.py
ce2dd35f100e3805fc2c1b486f3b58821787153f52bcfc48dccf78db87dc6ce2  tools/validate_ash_tensorcube_table_r1_cf1_immutable_byte_accounting_static.py
```

## 16. Static acceptance

CF1:

```text
PASS 24/24
PASS_TENSORCUBE_TABLE_R1_CF1_IMMUTABLE_BYTE_ACCOUNTING_STATIC
```

Maintained parent R1:

```text
PASS 23/23
PASS_TENSORCUBE_TABLE_R1_STATIC
```

Retained neighboring regressions:

```text
R4A          66/66 PASS
R4A-CF1      90/90 PASS
R4A-CF2      40/40 PASS
R4A-CF2-CF1  90/90 PASS

R4B          58/58 PASS
R4B-CF1      77/77 PASS
R4B-CF2     118/118 PASS
R4B-CF3     127/127 PASS

R4C          82/82 PASS
R4C-CF1     131/131 PASS
R4C-CF2      75/75 PASS
R4C-CF3      77/77 PASS
```

Python validators pass `py_compile`.

## 17. Compile / runtime / physical status

The bake environment has no `rustc` or `cargo` executable.

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

No compile/runtime/physical/performance promotion is claimed.

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
  tensorcube_table_r1_cf1_ `
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

## 18. Baked archive

```text
ASH_PASS3_TENSORCUBE_TABLE_R1_CF1_IMMUTABLE_BYTE_ACCOUNTING_CORRECTION_CODE_ONLY.zip
SHA-256:
28aac2986d11721f33c9f7058cc1f8ce7e5ff88e7205d56794e9e437915fc0f0
files=8509
CRC=PASS
```

Archive exclusion policy:

```text
specs/       0 entries
artifacts/   0 entries
manifest/    0 entries
manifests/   0 entries
```

Build-authority files such as `Cargo.toml` and `Cargo.lock` remain present. Source filenames containing `manifest` remain when they are implementation source rather than generated manifest payloads.

## 19. Evidence boundary

CF1 establishes at SOURCE/STATIC level:

```text
actual immutable upload inventory = 11 u32 + 11 logical-u64
correct immutable accounting = 132 bytes / row
mutable lifecycle accounting remains separate = 4 bytes / row
old 124-byte accounting retired
physical GPU allocation remains actual-byte-slice authoritative
```

CF1 does not establish measured performance improvement because no physical data movement or allocation behavior is changed by this correction.

## 20. Final law

> TensorCube Table R1 physically uploads eleven immutable u32 columns and eleven immutable logical-u64 columns. The canonical immutable payload is therefore 132 bytes per row, not 124.

> This revision repairs accounting truth only. Actual WGPU buffers were already sized from their real upload byte slices, so CF1 does not repair an undersized GPU allocation and does not change the physical table layout.

> Mutable lifecycle status remains a separate four-byte-per-row column and must not be folded into immutable accounting.

> The corrected estimator is guarded by the real column inventory so a future schema change cannot silently recreate the same accounting drift.
