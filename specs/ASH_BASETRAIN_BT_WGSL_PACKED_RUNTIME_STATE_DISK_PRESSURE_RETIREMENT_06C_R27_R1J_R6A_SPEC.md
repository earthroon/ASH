# ASH-BASETRAIN-BT-WGSL-PACKED-RUNTIME-STATE-DISK-PRESSURE-RETIREMENT-06C-R27-R1J-R6A

## Revision / parent authority

- Patch: `ASH-BASETRAIN-BT-WGSL-PACKED-RUNTIME-STATE-DISK-PRESSURE-RETIREMENT-06C-R27-R1J-R6A`
- Build: `bt-wgsl-packed-runtime-state-disk-pressure-retirement-06c-r27-r1j-r6a`
- Code parent: Pass103 / R6 Production Multi-Step Loop + Accumulation8 + Warmup/Scheduler.
- Physical parent: physically passed R5 generation3 / optimizer-step3 / cursor-next3.
- R6 physical promotion before R6A: not established.
- Role: replace R6 runtime persistence and transport before physical R6 promotion. Training math remains R6 authority.

## 1. Disk-pressure authority

R6A retires the storage amplification created by 201 weight + 201 Adam-M + 201 Adam-V runtime payload files, per-parameter syncs, post-write full-state digest rereads, and derived `runtime_weights.r6arena` reconstruction. It does not claim zero disk traffic: crash-safe weight+m+v persistence and actual Atlas/optimizer work reads remain.

## 2. Packed runtime state

Each packed generation owns exactly three runtime payloads:

```text
weights.r6pack
adam_m.r6pack
adam_v.r6pack
```

`.r6pack` is internal runtime state, not safetensors, not a public checkpoint ABI, and not an R1J checkpoint-export event.

Encoding is exact `F32`, little-endian, compression `NONE`, padding `0`, parameter count `201`.

## 3. Exact parameter-offset registry

`packed_state_manifest.json` uses schema `ash.basetrain.packed_runtime_state.r6a.v1` and carries 201 ordered entries with parameter ID/index, shape, element count, byte offset/length, and weight/M/V logical SHA256 values.

For every parameter:

`byte_length = logical_element_count * 4`.

The first offset is zero, every next offset equals the previous end, and the final end equals all three physical pack sizes. Gap, overlap, shape/span drift, out-of-bounds ranges, weight/M/V geometry divergence, registry digest drift, or physical-size drift fail closed.

Registry digest domain: `ash.basetrain.packed_runtime_state.registry.v1`.

Candidate manifest state is `VALIDATED_READY_FOR_CANONICAL_POINTER`, never pre-pointer `COMMITTED`.

## 4. Generation ping-pong slots

Runtime storage uses:

```text
training_state/slot_a/
training_state/slot_b/
```

The active source slot is immutable while the opposite slot is staged. An inactive stale slot is explicitly removed before reuse; it is never appended to or silently resumed.

First physical N=2 topology:

```text
R5 generation3 -> one-time streaming adoption -> slot_a
step4: slot_a generation3 -> slot_b generation4
step5: slot_b generation4 -> slot_a generation5
```

The higher generation number or newer timestamp never selects canonical state. Only `active_training_state.json` does.

## 5. One-time R5 generation3 adoption

The first R6A run receives R5's legacy per-parameter generation3 state. Exactly one explicit migration source is allowed: `R5_PRIMARY_COMMITTED_GENERATION3`.

Each legacy weight/M/V payload is read once and streamed into its packed destination while its existing logical digest is verified. Resulting packed logical parameter-set parity must equal the R5 committed candidate authority. No dtype conversion, repair, normalization, mutation, or full-state host materialization is allowed.

Migration read/write and its three payload syncs are reported separately from production optimizer-step I/O.

## 6. Sequential candidate egress and write-time SHA256

R6A owns one `SequentialPackWriter` for each of weight, M and V. Each writer creates `<name>.partial`, writes forward only, updates whole-file SHA256 over the same bytes being written, flushes, executes exactly one `sync_all`, and renames to the final pack filename.

Per optimizer commit:

- weight pack sync = 1
- Adam-M pack sync = 1
- Adam-V pack sync = 1
- total packed payload sync = 3
- per-parameter payload sync = 0

The current logical parameter SHA256 is updated from the same candidate bytes, preserving 201 weight + 201 M + 201 V logical digest authority without physical per-parameter files.

Same-process candidate publication requires `post_write_digest_reread_bytes=0`. Completed packs are not reopened and scanned merely to obtain SHA256.

## 7. Fresh-process integrity is distinct

A fresh-process resume performs exactly one sequential integrity scan per pack, validating whole-pack SHA256 and every registered logical digest. This is recorded as `fresh_resume_integrity_scan_bytes` and is distinct from prohibited post-write rehash.

Same-process next-step use relies on write-time digest authority plus physical range verification and does not perform a fresh-resume full scan.

## 8. Single-open sequential optimizer source

For each optimizer transaction, `weights.r6pack`, `adam_m.r6pack`, and `adam_v.r6pack` are each opened once. `SequentialPackF32Reader` consumes them in registry order and checks the expected byte cursor before each bounded read. End-of-pass reader coverage must equal each full pack size.

This retires per-chunk reopen/seek churn while preserving bounded host chunks.

## 9. 16 MiB bounded streaming

Packed migration and candidate persistence retain the 16 MiB state-stream budget. Full weight, M or V host materialization is forbidden. Full model or full optimizer-state GPU residency is not required.

## 10. Atlas direct packed-weight source

The derived `runtime_weights.r6arena` path is retired.

Atlas production plans are built directly from `weights.r6pack`, exact registered byte ranges, the write-time whole-pack identity, and per-parameter write-time digests. Packed source range geometry begins at byte zero and never inherits genesis/R3/R5 safetensors offsets.

Packed source binding records source SHA256, source byte count, parameter-offset-registry digest, and `postWriteDigestRereadBytes=0`. Atlas forward/loss/backward continues to validate the physical tensor range digest when the range is consumed.

Physical storage seal:

```text
runtime_arena_create_count=0
runtime_arena_rewrite_count=0
runtime_arena_write_bytes=0
runtime_arena_read_bytes=0
```

## 11. Direct packed AdamW state source

AdamW reads the exact registered weight/M/V ranges directly from the active packs and writes generation-N weight/M/V candidates sequentially into the inactive packs. Training formula, decoupled weight decay, and target-step bias correction remain R6 authority.

## 12. R6 training semantics preserved

R6A does not alter:

- gradient accumulation exactly 8
- eight real forward/loss/backward microbatches per optimizer transaction
- active-loss-slot weighted FP32 device accumulation
- no per-microbatch weight/optimizer/cursor/scheduler mutation
- one AdamW update after all eight microbatches
- cursor +8 per optimizer commit
- scheduler +1 per optimizer commit
- generation +1 and optimizer step +1 per commit

Loss, gradient, attention, RMSNorm, AdamW and scheduler formulas are outside R6A storage scope.

## 13. Candidate and canonical commit boundary

Candidate order is:

```text
STAGING
-> three packed payload writes/syncs
-> packed manifest geometry/digest validation
-> cursor candidate
-> scheduler candidate
-> VALIDATED
-> VALIDATED_READY_FOR_CANONICAL_POINTER
-> atomic active training-state replacement
```

There is no `transaction.committed.json` before the canonical pointer.

Windows retains `MoveFileExW(MOVEFILE_REPLACE_EXISTING | MOVEFILE_WRITE_THROUGH)` after the active-state partial is fully written/synced.

Generation, optimizer step, cursor, scheduler, active pack slot, packed-manifest digest, pack SHA256 values, and registry digest are one canonical transaction.

## 14. Crash safety

Before active-pointer replacement, incomplete/finished inactive packs and even a ready manifest are noncanonical. Partial packs are not resumed and orphan packs are not auto-adopted. If a candidate fails, the active source pack set remains untouched.

After pointer replacement, the new slot is canonical and the old slot becomes reusable inactive storage.

## 15. Training-state V3 packed binding

`ash.basetrain.training_state.v3` additionally binds:

- `packedStateSchema`
- `packedStateSlot`
- `packedStateManifestDigest`
- weight/M/V pack SHA256 values
- `parameterOffsetRegistryDigest`
- runtime payload files per generation = 3
- per-parameter runtime payload files = 0
- runtime arena counters = 0
- post-write digest reread bytes = 0

Immutable committed training-state history and parent training-state digest chaining remain R6 authority.

## 16. Disk accounting

R6A separately records migration reads, fresh-resume integrity reads, optimizer work reads, packed payload writes, control writes, digest-only rereads, and derived-arena I/O. A physical operation is not silently double-counted across accounting classes.

Each production step records exact logical state bytes, weight/M/V packed write bytes, optimizer-source pack read bytes, control bytes, sync counts, file counts, arena counters, digest-reread bytes, source-mutation count, partial-adoption count, registry coverage, and direct-packed-Atlas authority.

## 17. Physical N=2 promotion harness

R6A is applied before first physical R6 promotion, so the physical run starts from R5:

```text
source generation=3
source optimizer step=3
source cursor next=3
gradient accumulation=8
production optimizer steps=2
```

Expected:

```text
migration: generation3 -> slot_a
step4: ordinals 3..10, slot_a -> slot_b
step5: ordinals 11..18, slot_b -> slot_a
```

Final N=2 authority:

- generation 5
- optimizer step 5
- cursor last 18 / next 19 / consumed 19
- production microbatches 16

Production commits, excluding the explicit migration, must report packed payload sync count 6, per-parameter payload file/sync count 0, runtime-arena I/O 0, and post-write digest reread bytes 0. The initial migration separately reports three pack syncs.

## 18. Receipt / structural contract

Runtime R6A receipt Atlas: exactly 64 waves, <=8 fields per wave, duplicate-key fail closed.

Structural gates: exactly 80 ordered flags from `--require-bt-wgsl-r27r1j-r6a-contract-001=true` through `080=true`.

Structural receipt Atlas: exactly 64 semantic waves.

Current implementation contains 223 unique meaningful R6A negative canaries; numeric padding canaries are prohibited.

Static validator: `tools/validate_r27r1j_r6a_packed_runtime_state_disk_pressure_retirement_static.py`.

Parent R1J through R6 validators change only stale terminal-child/storage expectations necessary for the R6A handoff. Parent training semantics remain intact.

## 19. PASS / HOLD

R6 core PASS remains required:

`PASS_ASH_BASETRAIN_BT_WGSL_PRODUCTION_MULTI_STEP_LOOP_ACCUMULATION8_WARMUP_SCHEDULER_06C_R27_R1J_R6`

R6A PASS:

`PASS_ASH_BASETRAIN_BT_WGSL_PACKED_RUNTIME_STATE_DISK_PRESSURE_RETIREMENT_06C_R27_R1J_R6A`

Intended terminal HOLD:

`HOLD_ASH_BASETRAIN_R1J_R6A_PACKED_RUNTIME_STATE_PRODUCTION_MULTISTEP_COMMITTED_LONG_HORIZON_TRAINING_PROMOTION_NOT_YET_ADMITTED`

An exit code 1 caused only after both PASS tokens by that exact HOLD is intended.

## 20. Minimum first-run R6A receipt

```text
r27r1jr5_physical_parent=1
r6_code_parent=1
packed_runtime_state_adopted=1
packed_runtime_genesis_adoption=1
packed_runtime_genesis_source=R5_PRIMARY_COMMITTED_GENERATION3
source_training_generation=3
source_optimizer_step=3
source_cursor_next_batch_ordinal=3
parameter_count=201
production_loop_target_optimizer_steps=2
production_loop_committed_optimizer_steps=2
production_microbatch_count=16
gradient_accumulation=8
production_accumulation_adoption=1
training_generation_after=5
optimizer_step_after=5
cursor_next_batch_ordinal_after=19
runtime_payload_files_per_generation=3
per_parameter_runtime_payload_file_count=0
packed_payload_sync_count=6
migration_packed_payload_sync_count=3
per_parameter_payload_sync_count=0
runtime_arena_create_count=0
runtime_arena_rewrite_count=0
runtime_arena_write_bytes=0
runtime_arena_read_bytes=0
post_write_digest_reread_bytes=0
source_pack_mutation_count=0
partial_pack_adoption=0
generation_checkpoint_export=0
receipt_atlas_waves=64
proof_ledger=HOLD
```

Actual migration/read/write byte counts are physical observations and are not hardcoded.

## 21. PASS meaning / boundary

R6A PASS proves that the R5 generation3 authority was streamed once into an exact three-pack runtime representation and that the R6 accumulation8 production loop then persisted each optimizer candidate as three sequential packs rather than 603 per-parameter payloads. Physical/logical SHA256 is derived from bytes at write time, the completed packs are not reread for publication hashing, Atlas consumes direct registered weight-pack ranges, AdamW consumes direct registered weight/M/V ranges, and source packs remain immutable while the opposite slot is staged. Canonical generation/optimizer/cursor/scheduler/pack authority changes only through the atomic active-state pointer.

R6A does **not** prove that Windows disk active time can never reach 100%. Large sequential crash-safe writes and actual model/optimizer work reads can still saturate a slow disk. It retires disk amplification, not the disk itself.

## SSOT seal

```text
603 SMALL PAYLOAD FILES
+ HUNDREDS OF SYNCS
+ WRITE -> FULL REHASH READ
+ PER-PARAM WEIGHT FILES -> DERIVED ARENA WRITE -> ARENA READ

becomes

3 SEQUENTIAL PACKS
+ 3 PAYLOAD SYNCS / OPTIMIZER COMMIT
+ WRITE-TIME WHOLE + LOGICAL SHA256
+ 3 SINGLE-OPEN SEQUENTIAL SOURCE READERS FOR ADAMW
+ DIRECT ATLAS WEIGHT-PACK RANGES
+ ZERO DERIVED ARENA
+ ZERO POST-WRITE PACK REHASH
```

R6A retires disk amplification without weakening crash-safe canonical state ownership.