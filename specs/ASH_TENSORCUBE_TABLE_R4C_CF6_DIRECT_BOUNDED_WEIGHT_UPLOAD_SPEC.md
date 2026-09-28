# TENSORCUBE-TABLE-R4C-CF6

## DIRECT / BOUNDED WEIGHT UPLOAD

```text
TENSORCUBE-TABLE-R4C-CF6

DIRECT / BOUNDED WEIGHT UPLOAD

+ RESIDENT BYTE-RANGE DIRECT UPLOAD AUTHORITY
+ FULL Vec<f32> HOST MATERIALIZATION ELIMINATION
+ BOUNDED 16 MiB DECODE / UPLOAD WINDOW
+ F32 FINITE VALIDATION PRESERVATION
+ SOURCE-SLICE DIGEST PRESERVATION
+ TENSOR ELEMENT ORDER PRESERVATION
+ WGPU QUEUE STAGING AUTHORITY
+ SAME-DEVICE FINAL BURN TENSOR DESTINATION
+ RESIDENT RANGE LIFETIME CLOSURE
+ SEGMENTED WEIGHT STREAMING
+ NO SECOND FULL-SIZE HOST BUFFER
+ NO DUPLICATE H2D
+ NO NEW D2H
+ NO PER-WINDOW GPU WAIT
+ CF4 / CF5 ATTRIBUTION PRESERVATION
```

## 1. Purpose

CF5 removed the redundant resident `Arc<Vec<u8>> -> Vec<u8>` copy. CF6 removes the next full-size host materialization in the production model-weight path:

```text
resident &[u8]
    -> full Vec<f32>
    -> Tensor::from_data
    -> GPU
```

CF6 replaces it with:

```text
resident &[u8]
    -> bounded finite-validation window
    -> queue.write_buffer
    -> canonical final Burn tensor buffer
```

The production decoder and final RMSNorm paths no longer require a full host `Vec<f32>`.

## 2. Parent

Parent source:

```text
TENSORCUBE-TABLE-R4C-CF5
HOST COPY COLLAPSE
```

CF6 preserves CF5 resident range-view authority, source digest authority, logical read accounting, and CF11 source-retirement closure.

## 3. Canonical Direct Upload Authority

New module:

```text
crates/base_train/src/tensorcube_table_r4c_cf6_direct_bounded_weight_upload.rs
```

The canonical path materializes the final Burn tensor first with `Tensor::<InferenceBackend, 1>::empty(...)` or `Tensor::<InferenceBackend, 2>::empty(...)`, then obtains its same-device raw WGPU destination through `BurnToRawWgpuBridge::bridge_native_tensor_f32_live_strict`. The bridge must report `host_uploads = 0`.

## 4. Bounded Window Law

Upload window ceiling is 16 MiB. Every window is F32 aligned (`window_bytes % 4 == 0`). Tail windows preserve exact logical bytes and element count. No full tensor staging `Vec<f32>` is created.

## 5. Finite Validation

Every source window is decoded with `f32::from_le_bytes(...)` and must satisfy `is_finite() == true` before enqueue. CF6 does not sanitize NaN/Inf or change endian interpretation.

## 6. Source Digest and Segmented Ordering

Every slice still requires exact `sha256(source bytes) == source_slice_digest`. Segments are ordered by `logical_element_start` and `slot_segment_index`, must be gap-free/non-overlapping, and write to `destination.buffer_offset + logical_element_start * 4`.

## 7. Production Cutover

CF6 replaces full decoded materialization in:

```text
atlas_runtime_forward_wave_execution.rs
    input norm
    q/k/v/o projections
    post-attention norm
    gate/up/down projections

atlas_runtime_final_output_real_loss.rs
    model.norm.weight
```

The decoder block is finalized through the existing `R6R9C5CompleteDecoderWeightMaterials` and `build_r6_r9_c5_actual_decoder_block_from_materials`, preserving the model-layer ABI.

## 8. WGPU Queue Staging Resolution

The planning language allowed a custom bounded staging-slot ring. The baked implementation intentionally does not add a second explicit staging ring. It uses bounded `Queue::write_buffer` windows and WGPU's existing queue-owned staging authority.

Reason: a custom host staging ring plus staging GPU buffers would add D2D copies, explicit copy commands, and another submission/reuse lifecycle. CF6 is scoped to removing full host F32 materialization, not adding another transport layer.

This is a scope-preserving resolution, not a claim that a custom staging-slot reuse layer was implemented.

## 9. No New Synchronization / Readback

The CF6 upload module adds no:

```text
map_async
get_mapped_range
device.poll
onSubmittedWorkDone
explicit queue.submit
copy_buffer_to_buffer
```

`queue.write_buffer` is the required H2D path. No validation-only upload or new D2H is introduced.

## 10. Attribution

Environment:

```text
ASH_TENSORCUBE_TABLE_R4C_CF6_MODE
```

Accepted values: `OFF`, `OBSERVE`, `ACTIVE`. Default is `OFF`.

CF6 counters:

```text
direct_upload_tensor_count
direct_upload_source_bytes
direct_upload_element_count
upload_window_count
upload_window_peak_bytes
queue_write_count
required_h2d_bytes
duplicate_h2d_bytes
finite_validation_bytes
finite_validation_wall_ns
upload_enqueue_wall_ns
full_host_f32_materialization_count
full_host_f32_materialization_bytes
```

Terminal receipt:

```text
tensorcube_table_r4c_cf6_direct_bounded_weight_upload_receipt.json
```

Terminal log:

```text
[ASH-TENSORCUBE-TABLE-R4C-CF6][direct-bounded-weight-upload]
```

`ACTIVE` fails closed if the direct path is not exercised, full-host F32 materialization is observed, or duplicate H2D is recorded.

## 11. CF4 / CF5 Attribution Preservation

CF6 preserves CF4 source-read, SHA, decode-validation, and decoder-bundle attribution. Finite-validation wall time is kept separate from queue-write enqueue wall time.

CF5 gains `record_direct_view_decode_without_materialization(...)` so direct validation remains visible without falsely incrementing `direct_view_decode_materialized_bytes`.

The CF4 and CF5 static validators are successor-aware and accept either their original inline callsite or the canonical CF6 delegate.

## 12. Numerical / Ownership Preservation

Unchanged:

```text
optimizer math
Muon math
AdamW math
WGSL
TensorCube kernels
checkpoint format
safetensors layout
source slice digest
parameter ordering
generation identity
B06 evidence mode
CF11 successor ownership
RAM36 semantics
durability ordering
```

Each `CheckpointRangeBytes` view remains Arc-backed only for immediate upload scope. CF6 adds no global range cache or cross-generation source alias.

## 13. Actual Delta

```text
MOD 7
ADD 2
DEL 0
```

Modified:

```text
crates/base_train/src/atlas_runtime_final_output_real_loss.rs
crates/base_train/src/atlas_runtime_forward_wave_execution.rs
crates/base_train/src/lib.rs
crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
crates/base_train/src/tensorcube_table_r4c_cf5_host_copy_collapse.rs
tools/validate_ash_tensorcube_table_r4c_cf4_host_device_io_roundtrip_attribution_static.py
tools/validate_ash_tensorcube_table_r4c_cf5_host_copy_collapse_static.py
```

Added:

```text
crates/base_train/src/tensorcube_table_r4c_cf6_direct_bounded_weight_upload.rs
tools/validate_ash_tensorcube_table_r4c_cf6_direct_bounded_weight_upload_static.py
```

No `Cargo.toml`, `Cargo.lock`, or WGSL delta.

## 14. Static Acceptance

Executed in bake environment:

```text
PASS_TENSORCUBE_TABLE_R4C_CF6_DIRECT_BOUNDED_WEIGHT_UPLOAD_STATIC checks=135
PASS_TENSORCUBE_TABLE_R4C_CF5_HOST_COPY_COLLAPSE_STATIC checks=127
PASS_TENSORCUBE_TABLE_R4C_CF4_HOST_DEVICE_IO_ROUNDTRIP_ATTRIBUTION_STATIC checks=67
PASS_TENSORCUBE_TABLE_R4C_CF3_SLOT_LIFECYCLE_STATIC checks=77
PASS_TENSORCUBE_TABLE_R4B_CF3_FULL_ROUTE_HOST_LEDGER_COMPACTION_STATIC checks=127
PASS_TENSORCUBE_TABLE_R1_CF1_IMMUTABLE_BYTE_ACCOUNTING_STATIC
PASS_EVE_MCU_CLOSE_R2_PHYS_CANARY_R1_CF1_STATIC checks=63
PASS_EVE_MCU_R3H_CF11_PAGED_COW_CANDIDATE_WEIGHT_SUCCESSOR_STATIC checks=64
```

Build graph preservation:

```text
Cargo.toml byte-identical
Cargo.lock byte-identical
WGSL files checked=320
WGSL changed=0
```

## 15. Evidence State

The bake environment has no Rust toolchain.

```text
SOURCE       BAKED
STATIC       PASS
COMPILE      UNVERIFIED IN BAKE ENVIRONMENT
RUNTIME      UNVERIFIED AFTER CF6
PHYSICAL     UNVERIFIED AFTER CF6
PERFORMANCE  UNVERIFIED
```

No speedup claim is made from static evidence.

## 16. Source Seals

```text
30e01b5d70307cfaefa03fdc50f3801e7edc8138b2ebec93ffe8b8c7b9221803  crates/base_train/src/atlas_runtime_final_output_real_loss.rs
15174c11bda5462a6995858db0fcc14111160c806de195adfa612697514f4f4b  crates/base_train/src/atlas_runtime_forward_wave_execution.rs
9833c8ac811ef87cc84b6106ff146b3f5cbd847d955623c10296e4dd0bf4a38a  crates/base_train/src/lib.rs
819eb7213997ce5a0390d94990ea3466d9432d86d1e6fca2f4925c3e73db1103  crates/base_train/src/production_multistep_loop_accumulation8_scheduler.rs
41ced255bdb83b05fb7ea6c6a17f0965bfd1f98a489b197008c9a2ff90f33ae0  crates/base_train/src/tensorcube_table_r4c_cf5_host_copy_collapse.rs
3764c39dc099b67874fdbd167d12000b91e81177d933494ba58cf7055e7e4003  tools/validate_ash_tensorcube_table_r4c_cf4_host_device_io_roundtrip_attribution_static.py
93ebf166c29294644ea90ac0f2ff235ce85245567dc2e659172fb46321565305  tools/validate_ash_tensorcube_table_r4c_cf5_host_copy_collapse_static.py
ad84c30502108786291da2e12fde19ed70ff77256a86e6a3908c2f23407a9510  crates/base_train/src/tensorcube_table_r4c_cf6_direct_bounded_weight_upload.rs
f7791062cb59805532916cbcd6a6914d91c86b98914dba3b3d92eff4577f3a5f  tools/validate_ash_tensorcube_table_r4c_cf6_direct_bounded_weight_upload_static.py
```

## 17. Artifact Seals

```text
Overlay code-only ZIP
SHA-256 c663b4e930ef175f4b2d8948b91487d0df63006b74ccf71deb12509086b5633a
files=9
CRC=PASS

Full code-only ZIP
SHA-256 c79ce337576c6000b63b6c75952e3ea0692028b646f919a4df3fc9c9649c6255
files=8516
CRC=PASS
```

## 18. Local Compile Acceptance

Required:

```powershell
cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo check -p base_train --lib --release --locked -j 1
cargo build -p base_train --bin base_train --release --locked -j 1
```

## 19. Physical Acceptance

Same-source replay must establish:

```text
CF5 resident zero-copy exercised
CF6 direct bounded upload exercised
direct_upload_tensor_count > 0
direct_upload_source_bytes > 0
upload_window_peak_bytes <= 16777216
full_host_f32_materialization_count = 0
full_host_f32_materialization_bytes = 0
duplicate_h2d_bytes = 0
new D2H introduced by CF6 = 0
no per-window GPU wait introduced
source digest exact
finite validation exact
CF11 source-retirement closure PASS
```

## 20. Performance Claim Boundary

Source/static evidence proves removal of the full decoded host tensor from the production call graph. It does not prove end-to-end speedup. Same-source physical A/B remains required for peak private bytes, weight-load wall time, generation wall time, and training wall time.

## 21. Successor

After CF6 physical closure:

```text
R4D-R1
ADAMW STATUS DEVICE AGGREGATION

+ GPU-side segment status reduction
+ step-level bounded status readback
+ no per-segment map/poll latency chain
```

## 22. Final Law

> CF5 removes the redundant full-size byte copy. CF6 removes the redundant full-size decoded float tensor.

> Resident F32 source bytes are finite-validated in bounded windows and written directly into the canonical final Burn tensor backing on the same runtime device.

> Required H2D remains. Duplicate H2D, new D2H, full host `Vec<f32>`, and per-window GPU waits are forbidden.

> CF6 is a host-materialization collapse, not a GPU-kernel rewrite or a performance claim.