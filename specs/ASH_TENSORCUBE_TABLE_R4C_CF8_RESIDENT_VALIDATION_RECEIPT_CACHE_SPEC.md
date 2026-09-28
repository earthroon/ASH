# TENSORCUBE-TABLE-R4C-CF8

## RESIDENT VALIDATION RECEIPT CACHE

```text
TENSORCUBE-TABLE-R4C-CF8

RESIDENT VALIDATION RECEIPT CACHE

+ IMMUTABLE RESIDENT RANGE VALIDATION AUTHORITY
+ GENERATION / BACKING / RANGE / DIGEST EXACT CACHE IDENTITY
+ SHA-256 VALIDATION ONCE
+ FINITE F32 VALIDATION ONCE
+ POSITIVE RECEIPT REUSE
+ CF5 ZERO-COPY RANGE PRESERVATION
+ CF6 DIRECT BOUNDED UPLOAD PRESERVATION
+ CF7 IDENTITY COMPATIBILITY
+ OBSERVE FRESH-SCAN PARITY
+ ACTIVE SHA / FINITE RESCAN ELIMINATION
+ NEGATIVE / CORRUPT RECEIPT NON-REUSE
+ GENERATION / BACKING INVALIDATION
+ NO SOURCE-BYTE RETENTION
+ NO NEW H2D / D2H / GPU WAIT
```

## 1. Purpose

CF8 removes repeated CPU SHA-256 and F32 finite scans over an exact immutable resident checkpoint range. It does not remove validation. It converts a completed positive validation into a generation-local reusable receipt.

Parent chain:

```text
R4C-CF7 PARTIAL VRAM HOT-WEIGHT FORWARD / BACKWARD REUSE
R4D-R0B GRADIENT OBSERVABILITY DEVICE AGGREGATION
R4D-R0A HOT-PATH PIPELINE RESIDENCY
R4C-CF6 DIRECT / BOUNDED WEIGHT UPLOAD
R4C-CF5 HOST COPY COLLAPSE
```

## 2. Exact Identity

Canonical key:

```text
source_generation
resident_backing_digest
absolute_start
absolute_end
source_slice_digest
byte_length
element_count
dtype
validation_schema_revision
```

Schema: `R4C_CF8_VALIDATION_SCHEMA_V1`.

A hit requires exact equality for the complete key. Same parameter name, equal byte length, or equal logical role is insufficient.

## 3. Resident-Only Authority

CF8 is attached only to `ResidentCheckpointRangeView` / `CheckpointRangeBytes::Resident`.

The reader exposes metadata-only range identity:

```text
generation
backing_sha256
absolute_start
absolute_end
```

`OwnedFileRange` and `OwnedProjectionFallback` do not receive CF8 receipt reuse and continue through canonical parent validation.

The receipt cache stores no `Vec<u8>`, `Vec<f32>`, `Arc<Vec<u8>>`, or raw source pointer. It therefore does not extend host source lifetime.

## 4. Positive Receipt

`ResidentWeightValidationReceiptR4CCF8` seals the exact key with:

```text
sha256_verified=true
finite_verified=true
nonfinite_count=0
validation_digest
```

Only a positive receipt can satisfy ACTIVE reuse. Receipt digest and key are revalidated before reuse. Corrupt, partial, negative, mismatched, or stale receipts never satisfy admission.

## 5. First Use / Miss

```text
resident range
    -> SHA-256 over exact source bytes
    -> source_slice_digest equality
    -> bounded F32 finite scan
    -> positive receipt publish
    -> CF6 queue.write_buffer upload
```

A validation failure publishes no positive receipt.

## 6. ACTIVE Hit

On exact positive hit:

```text
resident metadata lookup
    -> positive receipt self-validation
    -> SHA rescan skipped
    -> finite rescan skipped
    -> CF6 upload bytes unchanged
```

CF8 removes CPU validation rescans only. Required H2D on a CF7 miss remains.

## 7. OBSERVE

`ASH_TENSORCUBE_TABLE_R4C_CF8_MODE=OBSERVE` preserves the parent fresh scan even when the cache has an exact would-hit. The fresh result must remain identical to the stored receipt authority; drift fails with `FAIL_R4C_CF8_OBSERVE_PARITY`.

## 8. Runtime Mode

```text
ASH_TENSORCUBE_TABLE_R4C_CF8_MODE

OFF / DISABLED / 0
OBSERVE / OBSERVE_ONLY
ACTIVE / ACTIVE_VERIFIED / 1
```

Default is `OFF`.

CF8 OBSERVE/ACTIVE requires CF6 ACTIVE.

## 9. Generation / Backing Invalidation

The cache is thread-local runtime state scoped to the active resident source generation.

Generation change clears receipts and increments generation invalidation evidence. Backing-digest change clears receipts and increments backing invalidation evidence.

Receipt metadata never retains the old source backing.

## 10. CF6 Integration

`DirectUploadSegment` carries:

```text
cf8_validation_key: Option<ResidentValidationCacheKeyR4CCF8>
cf8_validation_hit: bool
```

The source SHA block executes only when `cf8_validation_hit == false`. The bounded finite loop also executes only when `cf8_validation_hit == false`.

On miss, CF4/CF5 physical SHA/decode attribution remains active and CF8 records physical scan bytes/wall time. After the complete segment passes finite validation, the positive receipt is published.

On hit, scan attribution is not falsely incremented.

## 11. Preservation

Preserved:

```text
CF5 resident zero-copy range
CF6 16 MiB bounded direct upload
CF6 queue.write_buffer H2D
CF6 no full Vec<f32>
CF7 exact generation/digest/runtime cache identity
CF11 source retirement
```

## 12. Attribution

Counters include requests, hits, misses, inserts, invalidations, positive/negative receipt counts, SHA scan/avoided bytes, finite scan/avoided bytes, validation wall time, receipt failures, generation/backing/schema invalidation, duplicate validation, OBSERVE parity failure, and source-alias leak evidence.

Terminal receipt:

```text
tensorcube_table_r4c_cf8_resident_validation_receipt_cache_receipt.json
```

Compact log:

```text
[ASH-TENSORCUBE-TABLE-R4C-CF8][resident-validation-receipt-cache]
```

## 13. ACTIVE Fail-Closed

ACTIVE requires:

```text
validation_request_count > 0
validation_cache_hit_count > 0
sha_bytes_avoided > 0
finite_bytes_avoided > 0
receipt_validation_failure_count = 0
observe_parity_failure_count = 0
source_alias_leak_count = 0
```

## 14. Transfer / Synchronization Contract

The CF8 module adds no `queue.write_buffer`, `queue.submit`, `map_async`, `get_mapped_range`, `PollType::Wait`, or `device.poll`, and no H2D/D2H of its own.

## 15. Actual Delta

```text
MOD 4
ADD 2
DEL 0
```

Modified:

```text
crates/base_train/src/tensorcube_table_r4c_cf6_direct_bounded_weight_upload.rs
crates/base_train/src/lib.rs
crates/base_train/src/base_train_atlas_wave_01_checkpoint_reader.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
```

Added:

```text
crates/base_train/src/tensorcube_table_r4c_cf8_resident_validation_receipt_cache.rs
tools/validate_ash_tensorcube_table_r4c_cf8_resident_validation_receipt_cache_static.py
```

## 16. Build Graph Preservation

```text
Cargo.toml byte-identical
Cargo.lock byte-identical
WGSL checked = 320
WGSL changed = 0
```

## 17. Static Acceptance

```text
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

## 18. Source Seals

```text
44ca3f7306b1abce5cfb5dd7c580e4e2e674690d889197ad73457631d3e1696d  crates/base_train/src/tensorcube_table_r4c_cf6_direct_bounded_weight_upload.rs
0e350976b90c950e4f12f65531ea72b8ddd2454538de1cd05a3a7e01c81c76a8  crates/base_train/src/lib.rs
3d9f77b56ad8e429d653595dd7497bac710421789b5eea7f2b5137592bd19000  crates/base_train/src/base_train_atlas_wave_01_checkpoint_reader.rs
0e657ec4d04892eab941c723e0c43d35d29637f75fe712ce485ca4db10ee9567  crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
4f76b11d7b353b743b52f8ce291487d8fdd3fc2bef4b5f509030b1aa914415fe  crates/base_train/src/tensorcube_table_r4c_cf8_resident_validation_receipt_cache.rs
1ff48f5474e7e8a4b39aa24051f6f3fa036f23a4b1e2abf3e9d70af68a05e922  tools/validate_ash_tensorcube_table_r4c_cf8_resident_validation_receipt_cache_static.py
```

## 19. Artifact Seals

```text
Overlay code-only ZIP
SHA-256 286067b631573d378684925fc18e5683b8792d8b00a4b90fd83b78742c98222e
files=6
CRC=PASS

Full code-only ZIP
SHA-256 0d48ce86221db13f854d514bdb129aed2cc9de38809a296141a8b7d70304680c
files=8524
CRC=PASS
```

## 20. Evidence State

```text
SOURCE       BAKED
STATIC       PASS
COMPILE      UNVERIFIED IN BAKE ENVIRONMENT
RUNTIME      UNVERIFIED AFTER CF8
PHYSICAL     UNVERIFIED AFTER CF8
PERFORMANCE  UNVERIFIED
```

The bake environment has no Rust toolchain. No compile/runtime/speedup claim is inferred from static evidence.

## 21. Local Compile Acceptance

```powershell
cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo check -p base_train --lib --release --locked -j 1
cargo build -p base_train --bin base_train --release --locked -j 1
```

## 22. Runtime Qualification

First:

```text
CF6 = ACTIVE
CF8 = OBSERVE
```

Require exact would-hit identity, fresh SHA/finite parity, and zero OBSERVE parity failures.

Then:

```text
CF6 = ACTIVE
CF8 = ACTIVE
```

Require cache hit > 0, SHA/finite avoided bytes > 0, no fresh rescan on hits, no CF8 H2D/D2H/wait, and CF11 source-retirement PASS.

## 23. Performance Boundary

Same-source A/B compares CF7 parent versus CF7 + CF8 ACTIVE. Measure SHA/finite bytes scanned, CPU process time, weight-load wall time, forward/backward wall time, optimizer-step wall time, and generation wall time.

No exact speedup is claimed before physical A/B.

## 24. Successor

```text
TENSORCUBE-TABLE-R4D-R1
ADAMW STATUS DEVICE AGGREGATION

+ per-segment tiny status readback removal
+ device step-status ledger
+ optimizer-step bounded readback
+ commit failure atomicity preservation
```

## 25. Final Law

> Validation remains mandatory. Repeating identical SHA and finite validation over the same immutable resident range does not.

> CF8 binds successful validation to generation, resident backing digest, absolute byte range, source slice digest, byte/element cardinality, dtype, and schema revision. Exact identity reuses evidence; anything else executes canonical validation.

> The receipt cache contains metadata only, introduces no GPU transfer or wait, and never becomes model-commit or durability authority.
