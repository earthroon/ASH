# R2B-CF2-R1
# FFN FUSED NATIVE BACKING IDENTITY AUTHORITY REPAIR

## Revision

Patch ID: ASH-BASETRAIN-R2B-CF2-R1-FFN-FUSED-NATIVE-BACKING-IDENTITY-AUTHORITY-REPAIR

Build revision: basetrain-r2b-cf2-r1-ffn-fused-native-backing-identity-authority-repair

Class: PHYSICAL GPU RESOURCE IDENTITY ATTRIBUTION / DIAGNOSTIC AUTHORITY REPAIR / NO PRODUCT FIX

Direct parent: R2B-CF2 FFN PERSISTENT FUSED EXACT BACKING / ACCESS PAIR ATTRIBUTION.

## Parent evidence

R2B-CF2 reached the real Atlas grouped-sequential layer-0 FFN path with input_hidden=READ and gate_pre_out, silu_gate_out, up_linear_out, ffn_product_out=READ_WRITE.

Parent CF2 reported shared_backing_pair_count=0, shared_binding_mask=0x0, mixed_access_shared_backing_present=false. The same execution then failed in WGPU 26 with STORAGE_READ_ONLY versus STORAGE_READ_WRITE on the same Buffer usage scope.

Therefore CF2 logical role/range capture remains valid, while its Arc::ptr_eq result is demoted from physical backing authority to wrapper identity only.

## Diagnosis

The raw bridge reconstructed CubeCL WgpuResource values with WgpuResource::new(...), which discarded CF1 storage identity metadata. The bridge then wrapped cloned wgpu::Buffer handles in fresh Arc allocations. Arc wrapper inequality therefore did not establish native backing inequality.

## Required repair

- CUBECL STORAGE-ID PROVENANCE PRESERVATION
- RAW-BORROW NATIVE BUFFER IDENTITY PROPAGATION
- ARC-WRAPPER IDENTITY DEMOTION
- INPUT-HIDDEN vs RW OUTPUT EXACT NATIVE PAIR ATTRIBUTION
- BUFFER OFFSET / SIZE RELATION PRESERVATION
- WGPU26 MIXED-ACCESS ERROR CORRELATION
- NO ACCESS MODE CHANGE
- NO COPY FIX
- NO EXECUTION SEMANTIC CHANGE

## Implemented identity authority

Three identity layers are kept separate:

1. wrapper_arc_same: diagnostic only, non-authoritative.
2. native_buffer_identity: process-local allocation token assigned when CubeCL creates the actual WGPU buffer and preserved across resource clone/raw borrow.
3. cubecl_storage_id: CubeCL storage allocation identity.

wrapper_arc_same=false never implies DISTINCT_BACKING. Incomplete identity fails closed as UNKNOWN_BACKING.

cubecl-wgpu-ash assigns a monotonic native-buffer token in WgpuStorage::alloc, stores it alongside StorageId, copies it into WgpuResource, and retires it on deallocation. This metadata does not change WGPU usage flags, allocation sizes, queue behavior, or storage reuse policy.

ExternalWgpuBufferAliasR2 carries the optional native token so external alias propagation does not erase the physical identity witness.

burn-wgpu-local/raw_access.rs now clones the complete WgpuResource instead of reconstructing it with WgpuResource::new(...). RawWgpuBorrow::clone does the same.

burn_webgpu_backend/raw_bridge.rs records StorageId/native-token provenance in a diagnostic-only process-local registry keyed by the raw lease seam id. Registration is OFF unless ASH_R2B_CF2_R1_NATIVE_IDENTITY_TRACE=1.

## Pair attribution

Mandatory READ/RW pairs:

- input_hidden <-> gate_pre_out
- input_hidden <-> silu_gate_out
- input_hidden <-> up_linear_out
- input_hidden <-> ffn_product_out

Secondary RW/RW pairs are also emitted for completeness.

Range classes:

- EXACT_RANGE
- A_CONTAINS_B
- B_CONTAINS_A
- PARTIAL_OVERLAP
- DISJOINT
- UNKNOWN_RANGE

DISJOINT does not imply different WGPU buffers.

Backing classes:

- SAME_BACKING
- DISTINCT_BACKING
- UNKNOWN_BACKING
- IDENTITY_AUTHORITY_DIVERGENCE

Native/storage equality disagreement fails closed and blocks promotion.

Mixed-access classes include SameBackingReadVsReadWrite, which is the high-value correlation for the parent WGPU validation failure.

## Trace

Trace file: r2b_cf2_r1_native_backing_identity_trace.jsonl

Environment:

- ASH_R2B_CF2_R1_NATIVE_IDENTITY_TRACE=1
- ASH_R2B_CF2_TRACE_ROOT=<trace-root>
- ASH_R2B_CF2_PROCESS_RUN_ID=<run-id>

Events:

- FFN_FUSED_NATIVE_BINDING_IDENTITY
- FFN_FUSED_NATIVE_PAIR
- FFN_FUSED_NATIVE_IDENTITY_SUMMARY
- ENCODER_FINISH_BEGIN

Parent CF2 tracing remains intact and may run simultaneously.

## Promotion branches

ExactNativeMixedAccessPair:
exact_native_mixed_access_pair_count == 1.

MultiBindingNativeAliasSet:
exact_native_mixed_access_pair_count > 1.

TopLevelFfnAliasExcluded:
all four primary READ/RW pairs are authoritatively distinct, with zero unknown and zero identity divergence.

Otherwise HOLD remains.

No product fix is authorized in this revision.

## No product repair

This revision does not change READ/READ_WRITE declarations, WGPU BufferUsages, copies, unique-allocation policy, fusion, bind-group topology, dispatch topology, encoder topology, task throttling, FFN math, optimizer/gradient math, or Atlas scheduling/residency semantics.

## Source delta

MOD crates/ash_wgpu26_storage_interop/src/storage_alias_registry.rs
MOD crates/burn_webgpu_backend/src/base_train_ffn_tensorcube_persistent_executor.rs
MOD crates/burn_webgpu_backend/src/raw_bridge.rs
MOD vendor_fork_scaffold/burn-wgpu-local/src/raw_access.rs
MOD vendor_fork_scaffold/burn-wgpu-local/src/storage_alias_registry.rs
MOD vendor_fork_scaffold/cubecl-wgpu-ash/src/compute/storage.rs
ADD tools/validate_ash_r2b_cf2_r1_ffn_fused_native_backing_identity_static.py

Delta: MOD 6 / ADD 1 / DEL 0

Source-delta digest:
84f0406162306475ffd0e89cc8780ec8ccde16c775473dc0670567f378192378

## Static acceptance

PASS_R2B_CF2_R1_FFN_FUSED_NATIVE_BACKING_IDENTITY_STATIC checks=62
PASS_R2B_CF2_FFN_FUSED_EXACT_BACKING_PAIR_STATIC checks=48
PASS_R2B_CF1_STORAGE_ALIAS_ATTRIBUTION_STATIC checks=48

Parent/full-tree comparison confirms no other source delta.

## Compile status

The bake container did not expose cargo/rustc/rustfmt, so compilation is not claimed by this artifact.

Required downstream gates:

cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo check -p base_train --lib --release --locked -j 1
cargo build -p base_train --bin base_train --release --locked -j 1

## Archive seal

Overlay:
ASH_R2B_CF2_R1_FFN_FUSED_NATIVE_BACKING_IDENTITY_AUTHORITY_REPAIR_OVERLAY_CODE_ONLY.zip
SHA-256 1084f973c5b6dc85351deee0e7c0e0fe3cb88a3836b5111e496512207fa0ffc0
Files 7
CRC PASS

Full:
ASH_PASS3_R2B_CF2_R1_FFN_FUSED_NATIVE_BACKING_IDENTITY_AUTHORITY_REPAIR_CODE_ONLY.zip
SHA-256 c8e21ae6e18f319c9c2a3e92675788f9d8b691b12f5086c4cb1e542aa74955c7
Files 8484
CRC PASS

## Final law

R2B-CF2 established FFN logical roles and ranges but its Arc equality witness was wrapper identity only. R2B-CF2-R1 preserves CubeCL StorageId and an allocation-time native WGPU backing token through resource clone, external alias propagation, raw borrow, and FFN pair attribution. Arc wrapper equality is explicitly non-authoritative. The invalid WGPU mixed-access dispatch remains unchanged so the exact physical alias pair can be identified before any ownership or binding repair is attempted.
