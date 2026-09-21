# R2B-CF2-R1
# FFN FUSED NATIVE BACKING IDENTITY AUTHORITY REPAIR

## Revision

```text
Patch ID:
ASH-BASETRAIN-R2B-CF2-R1-FFN-FUSED-NATIVE-BACKING-IDENTITY-AUTHORITY-REPAIR

Build revision:
basetrain-r2b-cf2-r1-ffn-fused-native-backing-identity-authority-repair

Class:
PHYSICAL GPU RESOURCE IDENTITY ATTRIBUTION
DIAGNOSTIC AUTHORITY REPAIR
NO PRODUCT FIX
```

Direct parent:

```text
R2B-CF2
FFN PERSISTENT FUSED EXACT BACKING / ACCESS PAIR ATTRIBUTION
```

## Compilefix-1

The first bake exposed Rust `E0282` in the FFN binding trace because the `None` match arm left the local tuple element types underconstrained at the `serde_json::json!` boundary. Compilefix-1 adds only this explicit local type:

```rust
let (storage_id, native_id, external_alias_state, identity_source): (
    Option<String>,
    Option<u64>,
    Option<String>,
    &'static str,
) = match identity { ... };
```

No identity value, access mode, trace schema, storage ownership, dispatch behavior, or training semantic changes. The static validator now seals this explicit-type requirement.

## Parent physical evidence

R2B-CF2 reached the real Atlas grouped-sequential layer-0 FFN path and observed:

```text
input_hidden     READ

gate_pre_out     READ_WRITE
silu_gate_out     READ_WRITE
up_linear_out     READ_WRITE
ffn_product_out  READ_WRITE
```

Parent CF2 reported:

```text
shared_backing_pair_count=0
shared_binding_mask=0x0
mixed_access_shared_backing_present=false
```

The same execution then failed in WGPU 26 with:

```text
STORAGE_READ_ONLY
vs
STORAGE_READ_WRITE

BufferUses(STORAGE_READ_WRITE) is exclusive inside one compute-dispatch usage scope.
```

Therefore CF2 logical role/range capture remains valid, but its `Arc::ptr_eq` result is demoted from physical backing authority to wrapper identity only.

## Root diagnosis

The raw bridge reconstructed CubeCL `WgpuResource` values with `WgpuResource::new(...)`, dropping the CF1 storage identity metadata. It then wrapped cloned `wgpu::Buffer` handles in fresh `Arc` allocations. As a result:

```text
Arc::ptr_eq(A, B) == false
```

only established different Rust `Arc` wrappers. It did not establish different native WGPU buffer allocations.

## Required repair

R2B-CF2-R1 performs diagnostic authority repair only:

```text
+ CUBECL STORAGE-ID PROVENANCE PRESERVATION
+ RAW-BORROW NATIVE BUFFER IDENTITY PROPAGATION
+ ARC-WRAPPER IDENTITY DEMOTION
+ INPUT-HIDDEN vs RW OUTPUT EXACT NATIVE PAIR ATTRIBUTION
+ BUFFER OFFSET / SIZE RELATION PRESERVATION
+ WGPU26 MIXED-ACCESS ERROR CORRELATION
+ NO ACCESS MODE CHANGE
+ NO COPY FIX
+ NO EXECUTION SEMANTIC CHANGE
```

## Implemented identity layers

Three layers are kept distinct:

```text
wrapper_arc_same
    diagnostic only
    non-authoritative

native_buffer_identity
    process-local allocation token assigned when CubeCL creates the WGPU buffer
    stable across WgpuResource clone / raw borrow propagation

cubecl_storage_id
    CubeCL storage allocation identity
```

`wrapper_arc_same=false` must never imply `DISTINCT_BACKING`.

If native/storage identity is unavailable or incomplete, the classification fails closed as `UNKNOWN_BACKING`.

## Vendor allocation identity authority

`cubecl-wgpu-ash` now assigns a monotonically increasing process-local native-buffer token when `WgpuStorage::alloc` creates the actual WGPU buffer.

The token is stored next to the `StorageId` in the canonical storage owner and copied into `WgpuResource`.

On deallocation, the token entry is retired with the storage allocation.

This token is diagnostic metadata only. It does not modify buffer creation flags, buffer usage, allocation size, storage reuse policy, or queue behavior.

## External alias propagation

`ExternalWgpuBufferAliasR2` now carries the optional native-buffer token so an external alias does not silently erase the physical identity witness.

The existing external alias lifecycle and ownership semantics remain unchanged.

## Raw borrow preservation

`burn-wgpu-local/raw_access.rs` no longer reconstructs raw resources with:

```text
WgpuResource::new(buffer.clone(), offset, size)
```

for the Cube tensor raw-borrow path.

Instead it clones the full `WgpuResource`, preserving:

```text
CubeCL StorageId provenance
native buffer token
external alias state
offset
size
```

`RawWgpuBorrow::clone` likewise clones the full resource.

## Backend diagnostic propagation

`burn_webgpu_backend/raw_bridge.rs` records the preserved identity metadata in a diagnostic-only process-local registry keyed by the raw lease seam id.

Registration is enabled only when:

```text
ASH_R2B_CF2_R1_NATIVE_IDENTITY_TRACE=1
```

Normal production execution with the diagnostic gate OFF does not populate the registry.

## Exact binding matrix

Mandatory primary comparisons:

```text
input_hidden READ
    ↔ gate_pre_out READ_WRITE

input_hidden READ
    ↔ silu_gate_out READ_WRITE

input_hidden READ
    ↔ up_linear_out READ_WRITE

input_hidden READ
    ↔ ffn_product_out READ_WRITE
```

Secondary completeness comparisons are emitted for all RW/RW pairs among the four outputs.

## Range relation

Byte ranges remain independent of backing identity and are classified as:

```text
EXACT_RANGE
A_CONTAINS_B
B_CONTAINS_A
PARTIAL_OVERLAP
DISJOINT
UNKNOWN_RANGE
```

A `DISJOINT` relation does not mean distinct WGPU buffers.

## Backing relation

Allowed relations:

```text
SAME_BACKING
DISTINCT_BACKING
UNKNOWN_BACKING
IDENTITY_AUTHORITY_DIVERGENCE
```

Rules:

```text
native same == true OR StorageId same == true
    → SAME_BACKING

native same == false AND StorageId same == false
    → DISTINCT_BACKING

native/storage comparison disagree
    → IDENTITY_AUTHORITY_DIVERGENCE

insufficient authority
    → UNKNOWN_BACKING
```

Identity divergence fails closed and blocks promotion.

## Mixed-access classes

```text
DistinctBacking
SameBackingSameAccess
SameBackingReadVsReadWrite
SameBackingReadWriteVsReadWrite
UnknownBackingMixedAccess
IdentityAuthorityDivergence
```

High-value promotion witness:

```text
SameBackingReadVsReadWrite
```

with the parent WGPU 26 validation failure reproduced.

## Diagnostic output

Trace file:

```text
r2b_cf2_r1_native_backing_identity_trace.jsonl
```

Environment:

```text
ASH_R2B_CF2_R1_NATIVE_IDENTITY_TRACE=1
ASH_R2B_CF2_TRACE_ROOT=<trace-root>
ASH_R2B_CF2_PROCESS_RUN_ID=<run-id>
```

Events:

```text
FFN_FUSED_NATIVE_BINDING_IDENTITY
FFN_FUSED_NATIVE_PAIR
FFN_FUSED_NATIVE_IDENTITY_SUMMARY
ENCODER_FINISH_BEGIN
```

The parent CF2 trace remains intact and can run simultaneously.

## Promotion branches

### Exact pair

```text
exact_native_mixed_access_pair_count == 1
```

Promotion:

```text
ExactNativeMixedAccessPair
```

Next revision may repair only that exact binding/storage ownership relation.

### Multi-binding alias set

```text
exact_native_mixed_access_pair_count > 1
```

Promotion:

```text
MultiBindingNativeAliasSet
```

Next revision must repair the isolated alias set without arbitrarily selecting one pair.

### Top-level FFN alias excluded

Only when every primary pair is authoritatively distinct with no unknown or divergence:

```text
TopLevelFfnAliasExcluded
```

Then the search may move below the top-level FFN logical buffers into fused dynamic bind-group/internal materialization.

### Hold

Any missing backing authority or storage/native disagreement remains:

```text
HoldIdentityUnresolved
or
HOLD_IDENTITY_AUTHORITY_DIVERGED
```

## No product repair

This revision does not:

```text
change READ / READ_WRITE declarations
change WGPU BufferUsages
insert copy buffers
force unique output allocations
disable in-place reuse
disable Burn/CubeCL fusion
split bind groups
split dispatches
split encoders
change CUBECL_WGPU_MAX_TASKS
change FFN math
change optimizer/gradient math
change Atlas scheduling or residency semantics
```

The parent invalid dispatch is intentionally preserved for attribution.

## Source delta

```text
MOD crates/ash_wgpu26_storage_interop/src/storage_alias_registry.rs
MOD crates/burn_webgpu_backend/src/base_train_ffn_tensorcube_persistent_executor.rs
MOD crates/burn_webgpu_backend/src/raw_bridge.rs
MOD vendor_fork_scaffold/burn-wgpu-local/src/raw_access.rs
MOD vendor_fork_scaffold/burn-wgpu-local/src/storage_alias_registry.rs
MOD vendor_fork_scaffold/cubecl-wgpu-ash/src/compute/storage.rs
ADD tools/validate_ash_r2b_cf2_r1_ffn_fused_native_backing_identity_static.py
```

Delta:

```text
MOD 6
ADD 1
DEL 0
```

Source-delta digest:

```text
b8d46d6b633a703be5265cb7bf9f89d424c4b697eb10a025185735e9dedd377e
```

## Static acceptance

Current bake:

```text
PASS_R2B_CF2_R1_FFN_FUSED_NATIVE_BACKING_IDENTITY_STATIC checks=63
PASS_R2B_CF2_FFN_FUSED_EXACT_BACKING_PAIR_STATIC checks=48
PASS_R2B_CF1_STORAGE_ALIAS_ATTRIBUTION_STATIC checks=48
```

Parent/full-tree comparison confirms only the six intended modified sources and one new validator differ.

## Compile status

The bake environment does not provide `cargo`, `rustc`, or `rustfmt`, so Rust compilation is not claimed by this artifact.

Required downstream gates:

```text
cargo check -p burn_webgpu_backend --lib --release --locked -j 1
cargo check -p base_train --lib --release --locked -j 1
cargo build -p base_train --bin base_train --release --locked -j 1
```

## Archive seal

Review overlay:

```text
ASH_R2B_CF2_R1_FFN_FUSED_NATIVE_BACKING_IDENTITY_AUTHORITY_REPAIR_OVERLAY_CODE_ONLY.zip
SHA-256 1219673fcae82d3ddc323aa5f029ee7cde18afe7306b3d9b132172aeed81635d
Files 7
CRC PASS
```

Full applied code-only tree:

```text
ASH_PASS3_R2B_CF2_R1_FFN_FUSED_NATIVE_BACKING_IDENTITY_AUTHORITY_REPAIR_CODE_ONLY.zip
SHA-256 7197c3cef085acdc0a733f56d233c92a9b6877df443ebe7336db7137474099d8
Files 8484
CRC PASS
```

## Completion law

R2B-CF2-R1 may be physically promoted only after a production run proves one of:

```text
ExactNativeMixedAccessPair
MultiBindingNativeAliasSet
TopLevelFfnAliasExcluded
```

while retaining the same parent WGPU validation class or otherwise providing equivalent dispatch evidence.

No fix is authorized in this revision.

## Final law

> R2B-CF2 established FFN logical roles and ranges but its Arc equality witness was only wrapper identity. R2B-CF2-R1 preserves CubeCL StorageId and an allocation-time native WGPU backing token through resource clone, external alias propagation, raw borrow, and FFN pair attribution. Arc wrapper equality is now explicitly non-authoritative. The invalid WGPU mixed-access dispatch remains unchanged so the exact physical alias pair can be identified before any ownership or binding repair is attempted.
