# ASH-BASETRAIN-BT-WGSL-CANONICAL-PACKED-GENESIS-REUSE-AND-PATH-IDENTITY-06C-R27-R1J-R6A-R2-R1

## Revision / authority

- Patch: `ASH-BASETRAIN-BT-WGSL-CANONICAL-PACKED-GENESIS-REUSE-AND-PATH-IDENTITY-06C-R27-R1J-R6A-R2-R1`
- Build: `bt-wgsl-canonical-packed-genesis-reuse-and-path-identity-06c-r27-r1j-r6a-r2-r1`
- Code parent: Pass107 / R6A-R2 Device-Limit-Aware Micro-Atlas Vocab Row Paging.
- Physical parent: physically passed R5 generation3 / optimizer-step3 / cursor-next3.
- R6, R6A, R6A-R1 and R6A-R2 physical promotion before this patch: not established.
- Observed R6A-R2 failure: `AW01CheckpointRangeReadSessionPathDrift` between an absolute Windows path and a repo-relative path referring to the same packed weight file.
- Role: replace textual path equality with physical file identity, move generation3 packed adoption out of disposable run directories into an immutable content-addressed cache, and reclaim only transaction-owned failed staging.

## 1. Physical path identity

Path text is not file identity. `AW01CheckpointRangeReadSession` binds `ash.basetrain.physical_path_identity.v1` instead of a raw `PathBuf` equality contract.

A path is resolved against the explicit range-session resolution root, canonicalized, and bound to physical metadata. On Windows the preferred identity is volume serial + file index obtained from the opened file handle. On Unix it is device + inode. When platform physical IDs are unavailable, canonical physical path is the fallback identity.

Windows display normalization removes extended-path spelling differences such as `\\?\` and normalizes separators for receipt display only. Lowercasing path text is not a physical identity authority.

The same physical file reached through absolute, relative, junction/symlink-resolved, or equivalent path aliases is admitted. A replaced/different physical file is rejected even when textual spelling happens to match.

The old `AW01CheckpointRangeReadSessionPathDrift` raw-path contract is retired. True source replacement fails as `AW01CheckpointRangePhysicalFileDrift`; identity resolution failure is reported separately.

Runtime range receipt records physical identity checks, alias-equivalence count, raw-path comparison count, physical drift count, and the session physical identity digest. `raw_path_identity_comparison_count` must remain zero.

## 2. Immutable generation3 packed genesis cache

R5 generation3 is no longer migrated into every new run-local `slot_a`. The canonical cache root is derived from the R5 workspace and lives outside `base_train_runs`:

```text
workspace/base_train_cache/packed_genesis/
  objects/<cache-key>/
    weights.r6pack
    adam_m.r6pack
    adam_v.r6pack
    packed_state_manifest.json
  index/<cache-key>.json
  staging/
  locks/
```

The cache key is content-addressed and binds model identity, R5 training-state digest, R5 parameter-set digest, R5 optimizer-state digest, packed-runtime schema, parameter-registry schema, segment-registry schema, dtype and endianness. Run-directory path is not part of the cache key.

A different R5 state or incompatible packed schema therefore produces a different key rather than overwriting an existing object.

## 3. Cache publication authority

Only an index with publication state `IMMUTABLE_READY` can make a cache object reusable. An object directory alone, a partial pack set, a manifest without index, or staging contents are not canonical cache authority.

Cache miss build order:

1. acquire same-key single-writer OS lifetime lock;
2. remove only same-key orphan cache staging after exclusive ownership is established;
3. stream R5 generation3 legacy weight/M/V into three packed files;
4. derive whole-pack, logical-parameter and weight-segment digests from the write stream;
5. sync packed payloads and manifest;
6. atomically publish the completed object directory;
7. sync/write and atomically publish the cache index.

The final object is immutable. It is never an AdamW destination and is not copied or hardlinked into a mutable run slot.

On Windows the build lock uses an open file handle with share mode zero so process lifetime, rather than stale lockfile text, owns exclusion.

## 4. Cache-hit admission

A cache hit validates only small index/manifest authority, parent/content bindings, registry digests, and physical file sizes before training starts. It does not full-scan weight/M/V packs merely to calculate their SHA256 again.

Cache-hit migration authority is exactly:

```text
genesis_cache_hit=1
genesis_cache_build_count=0
migration_source_read_bytes=0
migration_pack_write_bytes=0
migration_pack_sync_count=0
r5_legacy_payload_open_count=0
cache_hit_full_pack_rehash_bytes=0
```

Actual training work reads are not classified as migration reads. Atlas verifies packed weight segment digests from the bytes it already consumes. AdamW source streaming verifies weight/M/V logical digests from the bytes it already consumes. Integrity verification therefore does not introduce a shadow full-state read pass.

## 5. First-run cache miss boundary

The first R6A-R2-R1 run for an R5 parent may legitimately be a cache miss. That run performs the one required R5 generation3 migration and may saturate an HDD while the immutable cache is constructed.

Once cache publication succeeds, later fresh runs using the same R5 parent must hit the cache and must not repeat migration I/O. Physical proof of retry reuse is therefore established by a subsequent same-parent cache-hit receipt, not inferred from the first miss alone.

R6A-R2-R1 currently admits the R5 physical-parent path only. Fresh resume from a later R6 training-state directory is not promoted by this patch and is rejected at CLI/runtime admission rather than silently treated as equivalent.

## 6. Direct genesis source and ping-pong transition

The packed genesis cache is the direct generation3 training source:

```text
GENESIS_CACHE generation3
    -> step4 candidate slot_b generation4
    -> step5 candidate slot_a generation5
```

No generation3 cache payload is copied into `slot_a` before step4. After step4 commit, the ordinary mutable run-slot ping-pong authority resumes.

Training state records packed source kind and genesis cache key as provenance. The cache itself remains immutable after its first publication.

## 7. Failed-run staging reclamation

R6A-R2-R1 reclamation is storage-transaction reclamation, not a memory garbage collector.

Each new run owns an explicit staging ledger. Candidate directories are tracked when created and removed from the reclamation set immediately after canonical active-state commit succeeds. On an error, the guard may reclaim only directories still proven to belong to the uncommitted current transaction and emits `r6a_r2_r1_failed_run_reclamation.json`.

Automatically reclaimable classes include transaction-owned partial/candidate staging and same-key cache build staging whose live writer lock is exclusively owned by the current builder.

Automatic reclamation must never delete:

- an `IMMUTABLE_READY` canonical genesis cache object;
- the current active run slot;
- committed training-state history;
- active training-state authority;
- legacy failed run directories whose ownership predates R6A-R2-R1 and cannot be proven.

Legacy `_01/_02/_03` style failed outputs remain operator-required cleanup. Name, age, modification time, or “looks failed” is not sufficient deletion authority.

## 8. No silent canonical cleanup

Deletion authority is fail-closed. Canonical cache deletion count and active-slot reclamation count must remain zero. A corrupt canonical cache is not silently deleted/rebuilt under the same key. Content drift fails closed and requires explicit operator action or a new content identity.

## 9. Parent storage and compute contracts preserved

R6A-R2-R1 does not change the parent training mathematics or micro-atlas geometry. Preserved authority includes:

- accumulation exactly 8 independent `batch_size=1` lanes;
- internal native WGPU bootstrap and same device/queue lineage;
- bootstrap/device-limit preflight before training storage mutation;
- 16 MiB micro-atlas physical page and triple ring;
- sparse embedding vocab-page admission;
- 24-page LM-head forward and 24-page LM-head backward for vocab 48,259 / hidden 2,048;
- no full embedding/LM-head GPU residency;
- no runtime arena;
- three packed mutable runtime payloads per committed run generation;
- write-time SHA authority and no post-write full-state rehash;
- one AdamW update, cursor +8, scheduler +1, generation +1 and optimizer step +1 per accumulation transaction.

## 10. Physical path receipt

Per range-read session the implementation records at least:

```text
physical_identity_check_count
absolute_relative_alias_equivalence_count
raw_path_identity_comparison_count
physical_file_drift_count
session_physical_identity_digest
```

The previously observed absolute/relative alias pair must resolve as the same physical file rather than `PathDrift`.

## 11. Cache receipt

R6A-R2-R1 terminal receipt records:

```text
canonical_path_identity_adopted
genesis_cache_lookup
genesis_cache_key_valid
genesis_cache_hit
genesis_cache_miss
genesis_cache_build_count
duplicate_generation3_pack_write_count
migration_source_read_bytes
migration_pack_write_bytes
migration_pack_sync_count
r5_legacy_payload_open_count
cache_hit_full_pack_rehash_bytes
failed_run_reclaimed_bytes
orphan_partial_reclaimed_count
canonical_genesis_cache_deleted_count
active_slot_reclaimed_count
```

A single run has exactly one of cache hit or cache miss. Cache build count equals the miss flag. Duplicate generation3 pack writes remain zero.

## 12. Structural authority

- Runtime R6A-R2-R1 receipt Atlas: exactly 80 waves.
- Structural receipt Atlas: exactly 80 semantic waves.
- Structural gates: exactly 96 ordered gates from `--require-bt-wgsl-r27r1j-r6a-r2-r1-contract-001=true` through `096=true`.
- Semantic negative canaries: 34 unique meaningful canaries with no numeric filler.
- Static validator: `tools/validate_r27r1j_r6a_r2_r1_canonical_packed_genesis_reuse_path_identity_static.py`.
- R6A-R2-R1 is the terminal structural child; R1J through R6A-R2 validators retain their parent semantics and only advance stale terminal-child/storage expectations required by this patch.

## 13. Physical N=2 harness

The physical promotion command starts from the R5 parent:

```text
generation3 / optimizer3 / cursor-next3
```

Expected training progression remains:

```text
step4: ordinals 3..10 -> generation4 / optimizer4 / cursor-next11
step5: ordinals 11..18 -> generation5 / optimizer5 / cursor-next19
```

The first run for this R5 state may report a cache miss and one migration. If that run fails after cache publication, the next run with a fresh output directory must report a cache hit and zero migration read/write/sync/legacy-open counters.

## 14. Required PASS chain

A completed physical production run must retain the parent PASS chain and then emit:

1. `PASS_ASH_BASETRAIN_BT_WGSL_PRODUCTION_MULTI_STEP_LOOP_ACCUMULATION8_WARMUP_SCHEDULER_06C_R27_R1J_R6`
2. `PASS_ASH_BASETRAIN_BT_WGSL_PACKED_RUNTIME_STATE_DISK_PRESSURE_RETIREMENT_06C_R27_R1J_R6A`
3. `PASS_ASH_BASETRAIN_BT_WGSL_PACKED_RUNTIME_NATIVE_BOOTSTRAP_AND_ACCUMULATION_WAVE_RESIDENCY_06C_R27_R1J_R6A_R1`
4. `PASS_ASH_BASETRAIN_BT_WGSL_DEVICE_LIMIT_AWARE_MICRO_ATLAS_VOCAB_ROW_PAGING_06C_R27_R1J_R6A_R2`
5. `PASS_ASH_BASETRAIN_BT_WGSL_CANONICAL_PACKED_GENESIS_REUSE_AND_PATH_IDENTITY_06C_R27_R1J_R6A_R2_R1`

Intended terminal HOLD:

`HOLD_ASH_BASETRAIN_R1J_R6A_R2_R1_CANONICAL_PACKED_GENESIS_CACHE_ADOPTED_PRODUCTION_MULTISTEP_LONG_HORIZON_PROMOTION_NOT_YET_ADMITTED`

Exit code 1 caused only after the complete PASS chain by this exact HOLD is intended.

## 15. PASS meaning

R6A-R2-R1 PASS establishes the canonical path-identity and cache transaction machinery for the production run: range sessions compare physical file identity rather than raw path text; generation3 packed state is sourced from an immutable content-addressed cache rather than copied into each run; cache miss performs at most the one canonical build; cache hit performs zero legacy migration I/O; mutable generation4+ state remains run-local ping-pong; and automatic reclamation is restricted to explicitly owned uncommitted staging.

A first-run cache miss does **not by itself physically prove retry reuse**. Retry zero-migration becomes physically established when a later same-parent run reports `genesis_cache_hit=1` with all migration counters zero.

## 16. Not proven

R6A-R2-R1 does not establish:

- HDD utilization always below 100%;
- zero training work I/O;
- automatic deletion of historical failed outputs created before ownership ledgers existed;
- R6 resume-state promotion;
- full model RAM/GPU residency;
- permanent optimizer-state GPU residency;
- distributed training or cross-device determinism;
- long-horizon production promotion or checkpoint-retention policy.

## SSOT seal

```text
PATH TEXT != FILE IDENTITY

absolute alias
relative alias
junction alias
extended Windows prefix

may all name the same physical file.
The range session binds the physical file, not its spelling.

R5 generation3 is also one state, not one state per retry.

FIRST MISS:
R5 legacy -> packed genesis cache -> IMMUTABLE_READY

NEXT SAME-PARENT RUN:
cache hit
migration read  = 0
migration write = 0
migration sync  = 0
legacy opens    = 0

GENESIS_CACHE generation3
    -> slot_b generation4
    -> slot_a generation5

Reclamation is not guesswork.
Owned uncommitted staging may be removed.
Canonical cache, active state and unproven legacy outputs may not.

BUILD ONCE.
REUSE BY CONTENT IDENTITY.
COMPARE PHYSICAL FILES, NOT PATH STRINGS.
RECLAIM ONLY OWNED STAGING.
```