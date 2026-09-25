# TENSORCUBE-TABLE-R4C-CF4

## HOST / DEVICE I/O + ROUNDTRIP CRITICAL-PATH ATTRIBUTION
## + RESIDENT WEIGHT HOST-COPY ATTRIBUTION
## + WEIGHT READ / SHA / F32 DECODE ATTRIBUTION
## + DECODER-BUNDLE BUILD ATTRIBUTION
## + DURABLE-PROJECTION D2H ROUNDTRIP ATTRIBUTION
## + ADAMW STATUS SUBMIT→COLLECT ATTRIBUTION
## + PACK WRITE / SYNC RECEIPT INTEGRATION
## + NO NEW WAIT / MAP / SUBMISSION
## + NO PHYSICAL GPU-TIMING PROMOTION

## 0. Revision

```text
Patch ID:
TENSORCUBE-TABLE-R4C-CF4

Canonical name:
ASH-BASETRAIN-TENSORCUBE-TABLE-R4C-CF4-
HOST-DEVICE-IO-ROUNDTRIP-CRITICAL-PATH-ATTRIBUTION
```

Direct implementation parent:

```text
ASH_PASS3_TENSORCUBE_TABLE_R1_CF1_IMMUTABLE_BYTE_ACCOUNTING_CORRECTION_CODE_ONLY.zip
SHA-256:
28aac2986d11721f33c9f7058cc1f8ce7e5ff88e7205d56794e9e437915fc0f0
files=8509
CRC=PASS
```

Class:

```text
PERFORMANCE ATTRIBUTION
I/O ATTRIBUTION
ROUNDTRIP ATTRIBUTION
CONTROL-PLANE TELEMETRY

NO TRAINING MATH CHANGE
NO OPTIMIZER MATH CHANGE
NO WEIGHT CONTENT CHANGE
NO CACHE POLICY CHANGE
NO H2D OPTIMIZATION
NO D2H OPTIMIZATION
NO DURABILITY POLICY CHANGE
NO GPU KERNEL CHANGE
NO GLOBAL WAIT INTRODUCTION
```

## 1. Purpose

CF4 establishes which current production cost dominates across:

```text
host memory copy
Weight source acquisition
Weight SHA validation
bytes→f32 decode + finite validation
Burn decoder bundle construction / host-side H2D preparation
D2H projection staging / submit / map / poll / yield / consume / cleanup
AdamW status submit→collect roundtrips
packed payload write / sync
```

CF4 does not remove or optimize any of those costs.

## 2. Three-axis evidence law

CF4 keeps separate:

```text
BYTES
TRANSACTIONS
HOST-OBSERVED WALL TIME
```

A small payload may still be expensive when transaction latency is high.
A large payload is not automatically the critical path.

No single axis promotes an optimization decision.

## 3. Mode

Environment:

```text
ASH_TENSORCUBE_TABLE_R4C_CF4_MODE=OFF
ASH_TENSORCUBE_TABLE_R4C_CF4_MODE=ACTIVE
```

Default when unset:

```text
OFF
```

OFF resets the attribution plane but records no CF4 counters/timers.
ACTIVE records the new attribution counters.

Execution semantics are unchanged by mode.

## 4. New attribution authority

New module:

```text
crates/base_train/src/
tensorcube_table_r4c_cf4_host_device_io_roundtrip_attribution.rs
```

It owns:

```text
HostDeviceIoAttributionModeR4CCF4
HostDeviceIoRoundtripCountersR4CCF4
HostDeviceIoRoundtripReceiptR4CCF4
```

and thread-local session aggregation only.

It owns no Device, Queue, Buffer, map ticket, submission, file writer or training state.

## 5. Resident Weight copy attribution

Current resident checkpoint read still performs:

```text
resident Arc<Vec<u8>>
→ borrowed resident slice
→ preallocated owned Vec<u8>
→ copy_from_slice
```

CF4 measures the existing copy with:

```text
resident_owned_copy_count
resident_owned_copy_bytes
resident_owned_copy_wall_ns
```

Instrumentation wraps the actual `copy_from_slice(projected)` call.

CF4 does not remove this copy.

## 6. Disk source read attribution

The nonresident physical checkpoint branch measures the existing:

```text
seek
read_exact
```

with:

```text
disk_source_read_count
disk_source_read_bytes
disk_source_read_wall_ns
```

Resident reads are not reclassified as disk reads.

## 7. Decoder Weight source attribution

The canonical single-slice `decode_f32_slice()` path now records:

```text
weight_source_read_count
weight_source_read_bytes
weight_source_read_wall_ns
```

around the existing `context.read_weight_range(...)` call.

## 8. SHA attribution

The existing exact slice SHA validation remains unchanged and is timed as:

```text
weight_sha_validation_count
weight_sha_validation_bytes
weight_sha_validation_wall_ns
```

No SHA check is removed or cached in CF4.

## 9. F32 decode / finite-validation attribution

The existing single-pass loop remains:

```text
4-byte chunk
→ f32::from_le_bytes
→ finite check
→ Vec<f32>::push
```

CF4 records:

```text
weight_f32_decode_validate_count
weight_f32_decode_input_bytes
weight_f32_decode_output_elements
weight_f32_materialized_bytes
weight_f32_decode_validate_wall_ns
```

No second validation pass is introduced for timing.

## 10. Decoder block bundle attribution

After all nine decoder Weight roles are materialized, CF4 measures only the existing:

```text
build_r6_r6_actual_decoder_block(device, values)
```

boundary.

Recorded:

```text
decoder_block_load_count
decoder_block_role_load_count
decoder_block_source_bytes
decoder_bundle_build_count
decoder_bundle_build_wall_ns
```

`decoder_bundle_build_wall_ns` is host-observed wall time around bundle construction.

It is not physical PCIe H2D duration.

## 11. No physical H2D-time promotion

CF4 does not introduce GPU timestamps.

Therefore:

```text
physical_gpu_overlap_supported = false
physical_gpu_overlap_ns = None
```

remain mandatory.

Existing R4C-CF1 structural H2D submit counters remain authoritative for submission facts.

## 12. Durable projection roundtrip attribution

The current production D2H window remains:

```text
create MAP_READ staging buffer
copy_buffer_to_buffer × N
submit_with_leases
map_async
poll_nonblocking_and_refresh loop
yield_now on empty callback
get_mapped_range
consume mapped bytes
unmap
release_submission_leases
```

CF4 wraps this existing path only.

No extra poll, map, submission or wait is added.

## 13. Projection counters

Per terminal aggregate:

```text
projection_window_count
projection_staging_create_count
projection_staging_created_bytes
projection_copy_command_count
projection_copy_command_bytes
projection_submission_count
projection_map_request_count
projection_map_ready_count
projection_poll_count
projection_yield_count
projection_submit_to_map_ready_wall_ns
projection_mapped_consume_count
projection_mapped_consume_bytes
projection_mapped_consume_wall_ns
projection_unmap_count
projection_lease_release_count
projection_cleanup_wall_ns
```

Actual copy bytes are summed from `copy.byte_count`.
Configured transfer-window capacity is not used as actual traffic.

## 14. Projection timer boundaries

Submission latency starts immediately after successful tracked submission.

It stops after:

```text
map callback success
AND
submission physical-complete observation
```

Consumer timing covers:

```text
layout.borrow(&mapped)
consumer callback
```

Cleanup timing covers:

```text
drop mapped view
unmap
mark_unmapped
release_submission_leases
```

These timers are host-observed wall times and do not claim GPU kernel duration.

## 15. Existing semantic D2H evidence reused

The scheduler continues using existing projection receipt fields:

```text
durable_projection_weight_d2h_bytes
durable_projection_adam_m_d2h_bytes
durable_projection_adam_v_d2h_bytes
```

CF4 aggregates those values into its terminal receipt.

The new generic copy-command byte counter does not replace semantic Weight/M/V D2H accounting.

## 16. AdamW status transaction attribution

The active-device pending-generation scheduler gains a private timestamp map:

```text
submitted_at_cf4: BTreeMap<AdamRangeR1, Instant>
```

Every admitted pending segment stores its submission timestamp.

Every existing `producer.try_collect(...)` call records one collection poll attempt.

When a segment becomes ready:

```text
pending owner removed
matching timestamp removed
submit→collect latency recorded
```

Terminal collection requires the timestamp map to be empty.

## 17. AdamW counters

CF4 records:

```text
optimizer_status_collect_poll_attempt_count
optimizer_status_yield_count
optimizer_status_submit_to_collect_total_ns
optimizer_status_submit_to_collect_max_ns
```

Existing production receipt remains authority for:

```text
optimizer_status_readback_count
optimizer_status_readback_bytes
```

Terminal CF4 seal requires:

```text
optimizer_status_readback_bytes
=
optimizer_status_readback_count * 4
```

## 18. AdamW latency meaning

Submit→collect latency includes any combination of:

```text
queue scheduling
GPU work
status copy
map readiness
host collection cadence
```

It is not named or promoted as GPU kernel time.

## 19. Existing candidate payload readback law preserved

CF4 does not add Weight/M/V candidate payload readbacks.

Existing zero-payload-readback contracts remain unchanged.

## 20. Pack write/sync integration

CF4 does not add duplicate pack timers.

It reuses existing N8 step timing fields:

```text
final_weight_pack_write_wall_ns
final_weight_pack_sync_wall_ns
final_adam_m_pack_write_wall_ns
final_adam_m_pack_sync_wall_ns
final_adam_v_pack_write_wall_ns
final_adam_v_pack_sync_wall_ns
```

and existing disk receipts:

```text
packed_weight_payload_write_bytes
packed_m_payload_write_bytes
packed_v_payload_write_bytes
packed_payload_sync_count
```

CF4 computes checked terminal sums only.

Durability behavior remains unchanged.

## 21. No hot-path telemetry I/O

The CF4 attribution module performs no:

```text
File::create
OpenOptions
fs::write
map_async
queue submit
device poll
```

Hot paths update memory-resident counters only.

One terminal JSON receipt is emitted at the N8 qualification boundary.

## 22. Terminal receipt

Output:

```text
tensorcube_table_r4c_cf4_host_device_io_roundtrip_attribution_receipt.json
```

Terminal log:

```text
[ASH-TENSORCUBE-TABLE-R4C-CF4][io-roundtrip]
```

The log is emitted once at terminal attribution, not once per role/window/poll.

## 23. Receipt scope

Receipt binds:

```text
source generation
target generation
source optimizer step
target optimizer step
```

plus:

```text
all CF4 counters
existing optimizer status readback count/bytes
existing semantic projection D2H Weight/M/V bytes
existing pack write bytes
existing pack sync count
existing pack write/sync wall time
```

## 24. Receipt integrity

Required:

```text
optimizer_status_readback_bytes
=
optimizer_status_readback_count * 4

projection_map_ready_count
<=
projection_map_request_count

projection_map_request_count
=
projection_submission_count
```

Checked arithmetic is used for aggregate byte/time/counter sums in the new attribution paths.

## 25. Instrumentation-overhead truth

CF4 receipt contains:

```text
instrumentation_overhead_ns = None
instrumentation_overhead_judgment = JUDGMENT_DEFERRED_BASELINE_REQUIRED
```

until a valid ACTIVE/OFF same-source physical A/B is available.

No arbitrary overhead threshold is encoded.

## 26. No optimization promotion

CF4 does not emit an authoritative choice among:

```text
resident host-copy collapse
direct Weight upload
async D2H readback ring
AdamW status aggregation
durability sync compaction
```

Those are follow-up branches selected only after physical CF4 evidence.

## 27. Exact implementation delta

Compared with the direct parent:

```text
MOD 5
ADD 2
DEL 0
```

Modified:

```text
crates/base_train/src/lib.rs
crates/base_train/src/base_train_atlas_wave_01_checkpoint_reader.rs
crates/base_train/src/atlas_runtime_forward_wave_execution.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/unified_atlas_mcu_adamw_active_device_pending_generation_scheduler_r1.rs
```

Added:

```text
crates/base_train/src/tensorcube_table_r4c_cf4_host_device_io_roundtrip_attribution.rs
tools/validate_ash_tensorcube_table_r4c_cf4_host_device_io_roundtrip_attribution_static.py
```

No `burn_webgpu_backend` source changed.
No WGSL source changed.
No R1/R4B/R4C parent implementation source was rewritten for semantics.

## 28. Source SHA-256

```text
5bf8b5ecfbafb3d492a5e824621665306265796ddbe3db8deabe31d65ac3b8b2  crates/base_train/src/lib.rs
d88478189eca99207c9377912eb57113f2e0c591abc6364356459ce6a84f9f86  crates/base_train/src/base_train_atlas_wave_01_checkpoint_reader.rs
a5e8f81494133dfaafc262962ca3836aa9930fde7953557499a6655b9db6413a  crates/base_train/src/atlas_runtime_forward_wave_execution.rs
ec124619ee7120134c191d9f1de9db9d495f7e0c9ada694d101948e093d695b4  crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
a1c71ff7957d1781b7f27bc74b76f966c3ef4a649c9226419f952f5afb92ee8a  crates/base_train/src/unified_atlas_mcu_adamw_active_device_pending_generation_scheduler_r1.rs
39fd6d39ae4c217eff0a4b9b2049c87d03c97d846b2a639906624bc7d7fd7ab5  crates/base_train/src/tensorcube_table_r4c_cf4_host_device_io_roundtrip_attribution.rs
fa4f8bda5dab9f21d59c8dfe16697342230b19ca93d5cb1ab9a0b8d20416dd81  tools/validate_ash_tensorcube_table_r4c_cf4_host_device_io_roundtrip_attribution_static.py
```

## 29. Static acceptance

CF4:

```text
PASS_TENSORCUBE_TABLE_R4C_CF4_HOST_DEVICE_IO_ROUNDTRIP_ATTRIBUTION_STATIC checks=67
```

Maintained regressions:

```text
R1           PASS
R1-CF1       PASS
R4B-CF3      127/127 PASS
R4C           82/82 PASS
R4C-CF1      131/131 PASS
R4C-CF2       75/75 PASS
R4C-CF3       77/77 PASS
```

The CF4 validator passes Python `py_compile`.

## 30. Compile / runtime / physical status

The bake environment contains no `cargo` or `rustc` executable.

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
  tensorcube_table_r4c_cf4_ `
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

## 31. Physical qualification

Run the same source/config twice:

```text
CF4 ACTIVE
CF4 OFF
```

with the same:

```text
model
dataset
generation source
optimizer source
cache budget
R4C slot mode
optimizer mode
step budget
```

Only after this pair may instrumentation perturbation and critical-path ranking be promoted.

## 32. Follow-up branch law

After physical CF4 evidence:

```text
resident copy / decode dominant
→ R4C-CF5 resident Weight host-copy collapse / validation witness work

bundle construction / host H2D preparation dominant
→ R4C-CF6 direct Weight upload / H2D preparation work

durable projection D2H map/poll dominant
→ R4D-R2 persistent async readback ring

AdamW status transaction latency dominant
→ R4D-R1 device status aggregation

pack sync dominant
→ R4D-R3 generation durability I/O compaction
```

No branch is selected by CF4 itself.

## 33. Baked archive

```text
ASH_PASS3_TENSORCUBE_TABLE_R4C_CF4_HOST_DEVICE_IO_ROUNDTRIP_ATTRIBUTION_CODE_ONLY.zip
SHA-256:
8e5fd995c0ce18261a0c1437e6fd7da50008595eb91d97d2736df4d82194d141
files=8511
CRC=PASS
```

Archive exclusion policy:

```text
specs/       0 entries
artifacts/   0 entries
manifest/    0 entries
manifests/   0 entries
```

Build-authority source such as `Cargo.toml` and `Cargo.lock` remains present.
Implementation source filenames containing `manifest` remain when they are source code rather than generated artifact payloads.

## 34. Evidence boundary

CF4 SOURCE/STATIC establishes that instrumentation is attached to the existing source operations and that no separate timing submission/readback path is introduced.

It does not establish:

```text
which domain is actually dominant
actual instrumentation overhead
physical PCIe transfer duration
copy-engine / compute overlap
actual speedup opportunity
```

Those are PHYSICAL/PERFORMANCE claims and remain UNVERIFIED.

## 35. Final law

> CF4 measures bytes, transactions and host-observed wall time as separate evidence dimensions.

> Resident Weight copies are classified as host memory traffic, not disk traffic. Decoder read, SHA, decode and bundle construction are separately timed without changing their algorithms.

> Durable projection instrumentation observes the existing staging/copy/submit/map/poll/yield/consume/unmap lifecycle and adds no new synchronization operation.

> AdamW's four-byte status path is treated as a latency-sensitive roundtrip. CF4 records collection attempts and submit-to-collect latency instead of judging the path from payload bytes alone.

> Existing pack write/sync timing is reused. CF4 does not alter durability policy.

> CF4 is attribution only. It must produce physical evidence before any I/O or CPU-roundtrip optimization branch is promoted.