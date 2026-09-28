# TENSORCUBE-TABLE-R4C-CF5

## HOST COPY COLLAPSE

```text
TENSORCUBE-TABLE-R4C-CF5

HOST COPY COLLAPSE

+ RESIDENT WEIGHT RANGE ZERO-COPY VIEW AUTHORITY
+ ARC-BACKING RANGE LEASE
+ SECOND FULL-SIZE BYTE BUFFER ELIMINATION
+ DIRECT RANGE SHA-256
+ DIRECT RANGE FINITE-DECODE
+ OWNED FALLBACK PRESERVATION
+ RESIDENT GENERATION / DIGEST AUTHORITY PRESERVATION
+ LOGICAL READ ACCOUNTING PRESERVATION
+ CF4 ATTRIBUTION EXTENSION
+ NO NEW D2H / H2D
+ NO NEW GPU SYNCHRONIZATION
+ NO UNSAFE LIFETIME ESCAPE
+ SAME-SOURCE BYTE / FLOAT PARITY
```

## 1. Purpose

CF5 removes the redundant full-range host byte copy on the resident checkpoint path.

Parent behavior:

```text
resident checkpoint Arc<Vec<u8>>
    -> resident slice
    -> second full-size Vec<u8>
    -> SHA-256
    -> finite F32 decode
    -> downstream Vec<f32> / upload consumer
```

CF5 behavior:

```text
resident checkpoint Arc<Vec<u8>>
    -> immutable Arc-backed range view
    -> direct SHA-256
    -> direct finite F32 decode / upload consumption
```

CF5 does not yet eliminate the downstream `Vec<f32>` materialization required by existing decoder consumers. That remains a successor optimization.

## 2. Canonical Range Authority

The reader materializes:

```text
CheckpointRangeSourceClass
    ResidentZeroCopyView
    OwnedFileRange
    OwnedProjectionFallback

ResidentCheckpointRangeView
    Arc<Vec<u8>> backing
    absolute_start
    absolute_end
    generation
    backing_sha256

CheckpointRangeBytes
    Resident(ResidentCheckpointRangeView)
    Owned { Vec<u8>, source_class }
```

`ResidentCheckpointRangeView` exposes immutable `&[u8]` only. It does not expose mutable backing or fabricate lifetimes.

## 3. Resident Zero-Copy Law

`read_bounded_checkpoint_range_view()` MUST:

```text
validate requested path identity
validate range bounds
require resident generation
require resident backing digest
preserve logical read accounting
preserve resident projection accounting
preserve resident readahead accounting
clone only the Arc handle
return an immutable range view
```

The resident view body MUST NOT perform:

```text
slice.to_vec()
full-range Vec allocation
copy_from_slice(projected)
unsafe lifetime extension
transmute
```

## 4. Legacy Owned API Preservation

The legacy:

```text
read_bounded_checkpoint_range() -> Vec<u8>
```

remains available for callers that explicitly require ownership.

If a resident view is converted to owned bytes, that copy remains visible to both CF4 and CF5 attribution. CF5 active physical admission therefore fails if a resident owned copy survives in the production route.

This preserves parent observability instead of hiding fallback behavior.

## 5. Production Consumer Cutover

The following production surfaces consume the range-view authority:

```text
AW01 residency coordinator
Atlas runtime route admission
Atlas runtime forward decoder weight load
R6A-R2 segmented vocab / lm-head paging
Atlas final-output full-plan tensor decode
```

After CF5 bake, direct production callsites of the legacy owned read APIs are retired. Their definitions remain as compatibility fallbacks only.

## 6. Projection / Disk Fallback

The following remain explicit owned paths:

```text
physical file range read
AshObjectiveProbeSparseWeightProjection transformed range
```

These are classified and metered as owned fallbacks. CF5 does not mislabel transformed data as zero-copy resident data.

## 7. Direct Digest Authority

Resident source digest verification runs directly over the range view:

```text
sha256(view.as_bytes())
```

The digest input byte sequence, order, and existing `source_slice_digest` authority are preserved.

No new digest domain or replacement digest is introduced.

## 8. Direct F32 Decode Authority

Resident F32 decoding consumes the view directly:

```text
for chunk in view.chunks_exact(4)
    f32::from_le_bytes(...)
    finite check
```

The following remain unchanged:

```text
little-endian interpretation
4-byte F32 cardinality
element ordering
finite validation
logical element coverage
```

## 9. Segmented Tensor Preservation

Segmented tensors remain segment-ordered and digest-bound.

CF5 MUST NOT concatenate all resident source segments into a new full byte tensor before decoding or upload.

Each resident segment may independently carry a zero-copy view until its immediate consumer completes.

## 10. Source Retirement / Lifetime Law

A range view owns an Arc reference to the resident checkpoint backing, so its lifetime is explicitly bounded to the immediate decode / upload scope.

Forbidden:

```text
global ResidentCheckpointRangeView cache
cross-generation range retention
successor state retaining source Arc
checkpoint receipt retaining source Arc
unsafe lifetime escape
```

Existing CF11 closure remains authoritative:

```text
reader_closed=true
live_alias_count=0
source reservation released
source retired before successor reservation
```

A CF5 physical run that leaves source aliases alive at retirement is FAIL.

## 11. CF5 Attribution

CF5 adds compact attribution counters:

```text
resident_zero_copy_view_count
resident_zero_copy_view_bytes
resident_owned_copy_count
resident_owned_copy_bytes
owned_fallback_read_count
owned_fallback_read_bytes
direct_view_sha_count
direct_view_sha_bytes
direct_view_decode_count
direct_view_decode_bytes
direct_view_decode_output_elements
direct_view_decode_materialized_bytes
```

Runtime attribution mode:

```text
ASH_TENSORCUBE_TABLE_R4C_CF5_MODE=ACTIVE
```

Default when absent is `OFF`.

The optimization itself is structural and does not depend on attribution mode. The mode controls CF5 counters / physical fail-closed observation only.

## 12. Physical Fail-Closed Rule

When CF5 attribution is ACTIVE:

```text
resident_owned_copy_count MUST equal 0
resident_owned_copy_bytes MUST equal 0
```

Otherwise:

```text
FAIL_TENSORCUBE_TABLE_R4C_CF5_RESIDENT_OWNED_COPY_OBSERVED
```

is emitted.

## 13. Receipt

Terminal receipt:

```text
tensorcube_table_r4c_cf5_host_copy_collapse_receipt.json
```

Terminal compact log:

```text
[ASH-TENSORCUBE-TABLE-R4C-CF5][host-copy-collapse]
```

It reports zero-copy bytes/count, any surviving resident owned copy, owned fallback bytes, direct SHA/decode bytes, and duplicate-copy closure.

## 14. No New GPU Traffic / Synchronization

CF5 adds no new:

```text
map_async
get_mapped_range
device poll
queue submit
onSubmittedWorkDone wait
D2H staging readback
H2D validation upload
GPU timestamp query
```

`no_new_gpu_transfer_or_sync_contract=true` is a source-structure statement. It is not a measured GPU-overlap claim.

## 15. Numerical Preservation

CF5 changes byte ownership only.

Unchanged:

```text
optimizer math
Muon math
AdamW math
WGSL
TensorCube kernels
checkpoint format
safetensors layout
source-slice digests
parameter order
generation identity
B06 evidence mode
CF11 successor ownership
RAM36 reservation semantics
durability ordering
```

## 16. Physical Acceptance

A same-source physical canary may promote CF5 only when:

```text
resident_zero_copy_view_count > 0
resident_zero_copy_view_bytes > 0
resident_owned_copy_count = 0
resident_owned_copy_bytes = 0
source digest exact
F32 finite decode exact
source retirement closure PASS
new GPU transfer/synchronization introduced by CF5 = 0
```

Performance improvement remains separately measured by CF4/CF5 wall-time evidence.

## 17. Performance Claim Boundary

SOURCE/STATIC evidence can establish that the redundant resident byte copy has been removed from the production call graph.

It cannot establish the amount of wall-time improvement.

No `% faster`, throughput, generation-latency, or end-to-end training-time claim is permitted until same-source physical A/B evidence exists.

## 18. Actual Implementation Delta

Parent:

```text
EVE-MCU-CLOSE-R2-PHYS-CANARY-R1-CF1
B06 NON-P5 MUON DEVICE TARGET COMMIT EVIDENCE MODE CLOSURE
```

Actual CF5 delta:

```text
MOD 8
ADD 2
DEL 0
```

Modified:

```text
crates/base_train/src/atlas_runtime_final_output_real_loss.rs
crates/base_train/src/atlas_runtime_forward_wave_execution.rs
crates/base_train/src/atlas_runtime_route_admission.rs
crates/base_train/src/base_train_atlas_wave_01_checkpoint_reader.rs
crates/base_train/src/base_train_atlas_wave_01_residency_coordinator.rs
crates/base_train/src/device_limit_aware_micro_atlas_vocab_row_paging.rs
crates/base_train/src/lib.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
```

Added:

```text
crates/base_train/src/tensorcube_table_r4c_cf5_host_copy_collapse.rs
tools/validate_ash_tensorcube_table_r4c_cf5_host_copy_collapse_static.py
```

No `Cargo.toml`, `Cargo.lock`, or WGSL delta.

## 19. Static Acceptance

Executed in bake environment:

```text
PASS_TENSORCUBE_TABLE_R4C_CF5_HOST_COPY_COLLAPSE_STATIC checks=127
PASS_TENSORCUBE_TABLE_R4C_CF4_HOST_DEVICE_IO_ROUNDTRIP_ATTRIBUTION_STATIC checks=67
PASS_TENSORCUBE_TABLE_R4C_CF3_SLOT_LIFECYCLE_STATIC checks=77
PASS_TENSORCUBE_TABLE_R4B_CF3_FULL_ROUTE_HOST_LEDGER_COMPACTION_STATIC checks=127
PASS_TENSORCUBE_TABLE_R1_CF1_IMMUTABLE_BYTE_ACCOUNTING_STATIC
PASS_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF1_STATIC checks=63
PASS_EVE_MCU_R3H_CF11_PAGED_COW_CANDIDATE_WEIGHT_SUCCESSOR_STATIC checks=64
```

Legacy Atlas static scripts that require excluded `specs/cli` or PowerShell support files are not claimed as executed from the code-only bake environment.

## 20. Compile / Runtime Evidence State

Bake environment contains no Rust toolchain.

Therefore:

```text
SOURCE      BAKED
STATIC      PASS
COMPILE     UNVERIFIED IN BAKE ENVIRONMENT
RUNTIME     UNVERIFIED AFTER CF5
PHYSICAL    UNVERIFIED AFTER CF5
PERFORMANCE UNVERIFIED
```

Local authoritative compile/build remains required before physical promotion.

## 21. Source Seals

```text
236ff6a046da510ddf74da44d862ac7d34c8141a96c3898163002400106e5c2b  crates/base_train/src/atlas_runtime_final_output_real_loss.rs
5c3347cfcf5d70efbee9eeb2a3dd2f4154c4d5fe5671f728babff8aab88d2ee8  crates/base_train/src/atlas_runtime_forward_wave_execution.rs
7a5d21042d375aad6bf6049adf411ad1f86fa5e4e80552eecbbad01b8a163509  crates/base_train/src/atlas_runtime_route_admission.rs
88c550179dc7e8b943635da9ac9799a700c34078146b5bd640bcf395289eaad7  crates/base_train/src/base_train_atlas_wave_01_checkpoint_reader.rs
585b41245ff9d9b7142762d5db71f2de25886ac8a376b420dd6666e4dacfe02e  crates/base_train/src/base_train_atlas_wave_01_residency_coordinator.rs
ec0efba31c9f0c544582ecc19da41e7c342beb6e37b155597968895c2322c662  crates/base_train/src/device_limit_aware_micro_atlas_vocab_row_paging.rs
0d8f44d4f96f8ec748e50eef6676971f2fa0cc19f31c13afd9ec5a3bf5025e46  crates/base_train/src/lib.rs
5ce3b8fbd5acbfaa8b8e0f8974833948147beefafac0d2cbf9e8a3f7152234f1  crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
f382fe2daeed1a40b8adc07f19ee5c5d068c2c3bf75c4da305c0af1965131d9c  crates/base_train/src/tensorcube_table_r4c_cf5_host_copy_collapse.rs
6eb1f3139ca2adb2d3a187d87aec7ea6f38a74879bd785b11d6505fd85396da9  tools/validate_ash_tensorcube_table_r4c_cf5_host_copy_collapse_static.py
```

## 22. Artifact Seals

```text
Overlay code-only ZIP
SHA-256 46bf1a65f08884e9ba822e1cf2d99a1f5cec5f1e3db0b5805ca64aa25713bd6e
files=10
CRC=PASS

Full code-only ZIP
SHA-256 3a195a5d3d138fdf119499c6d489bf7a0bdda241271c0890097470d9595ed739
files=8514
CRC=PASS
```

## 23. Completion Law

CF5 may issue:

```text
PASS_TENSORCUBE_TABLE_R4C_CF5_HOST_COPY_COLLAPSE
```

only after local compile and same-source physical replay establish:

```text
zero-copy resident range actually exercised
resident duplicate owned copy = 0
source digest / decode parity preserved
source retirement closure preserved
no new GPU transfer or synchronization introduced
```

> Resident means resident. An immutable source range already owned by the resident checkpoint backing must not be copied into a second full-size byte buffer merely to hash, decode, or upload it.
