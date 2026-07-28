# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5-R1-R2-R10

## TensorCube Stage 5 Contiguous 16×16 Physical Allocation / Stage4 Parent Binding / Single-Feature Mask Accumulation / Row·Tile Stride Authority / Adapter Alignment Closure / Physical Address Bijection / Padding Guard / Same-Device Bit-Exact Relocation Parity / Exact Stage4 Fallback / Generation 32→33→34 Seal

## 0. Authority

```text
PARENT=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5-R1-R2-R9
PARENT_VERDICT=PASS
PARENT_ROUTE=HeadwiseActive
PARENT_STAGE=Stage4Active
PARENT_STAGE_ID=tensorcube-stage-4-logical16x16-composition-v1
PARENT_FEATURE=tensorcube-logical-16x16-four-microtile-composition-v1
PARENT_FEATURE_MASK=0x000000000000000f
PARENT_GENERATION=32

STAGE=Stage5Active
STAGE_ID=tensorcube-stage-5-contiguous16x16-physical-allocation-v1
FEATURE=tensorcube-contiguous-16x16-physical-allocation-v1
FEATURE_BIT=4
CHILD_FEATURE_MASK=0x000000000000001f
PREPARED_GENERATION=33
COMMITTED_GENERATION=34

ALLOCATION_MODE=DedicatedAlignedTileBuffer
SOURCE_ACCESS_MODE=Stage4LogicalCoordinateAccessor
PHYSICAL_LAYOUT=RowMajorF32Vec4
IMPLEMENTATION_REVISION=R2-R10-stage5-contiguous16x16-physical-allocation-v1
CLI_EXTENSION_KEYS=105
CANONICAL_REGISTRY_KEYS=1622
CHILD_ARTIFACTS=27
DEFAULT_VERDICT=HOLD
```

R2-R10 activates exactly one feature beneath sealed Stage 4. It adds no matrix arithmetic, K-panel accumulation, Q/K/V adoption, KV mutation, or production-route publication. Its only functional claim is relocation of each sealed logical 16×16 tile into one dedicated, adapter-aligned physical tile slot.

## 1. Parent binding and reuse

The direct parent must prove:

```text
pass=true
stage=Stage4Active
feature_mask_after=0x0f
logical_tiles=128
parent_microtiles=512
logical_scalars=32768
all Stage4 composition mismatch counters=0
bit_exact_parity=true
KV writes=0
generations=30/31/32
Atlas groups=22/22
negative controls=600/600
```

R2-R10 binds by SHA-256 the R2-R9 runtime artifact, manifest, Stage4 pointer, Atlas digest, logical-coordinate-map digest, Stage4 composition shader and parent scientific terminal. A complete exact parent set is reused without rebuild, recommit or pointer rewrite. Partial or mismatched parent state fails closed.

## 2. State ownership and feature transition

```text
AttentionRouteState owner=R2-R5 value=HeadwiseActive mutable_by_R2_R10=false
TensorCubeStageState owner=R2-R10 Stage4Active -> Stage5Prepared -> Stage5Active|Stage5Fallback|Quarantined
TensorCubeFeatureMaskState owner=R2-R10 0x0f -> 0x1f
LogicalTileCoordinateState owner=R2-R9 mutable_by_R2_R10=false
PhysicalTileAddressState owner=R2-R10
PhysicalTileStrideState owner=R2-R10
PhysicalTileAlignmentState owner=R2-R10
PhysicalTileAllocationState owner=R2-R10
PaddingOwnershipState owner=R2-R10
StagePointerState owner=TensorCube registry Stage4 -> Stage5 CAS
KVOwnershipState owner=inherited registry, Stage5 write lease=none
ScientificEvidenceState owner=R1-R2 mutable_by_R2_R10=false
```

Only this mask transition is legal:

```text
0x000000000000000f -> 0x000000000000001f
popcount(parent XOR child)=1
bits 0..3 retained
bit 4 added
bits >=5 remain zero
```

## 3. Physical geometry and contiguity

```text
logical shape=16x16
scalar=f32
scalar bytes=4
row scalars=16
row vec4 slots=4
row stride=64 bytes
tile scalars=256
tile vec4 slots=64
tile payload=1024 bytes
tile count=128
```

Contiguous means no padding inside the 1024-byte payload. Adjacent columns differ by 4 bytes, vec4 slots by 16 bytes, and rows by exactly 64 bytes. Only tail padding after byte 1023 is permitted when required by adapter alignment. Stage 5 does not claim that the four Stage 3 source microtiles were physically adjacent.

## 4. Alignment and stride authority

The sole alignment authority is:

```text
adapter.limits.min_storage_buffer_offset_alignment
```

Derived values:

```text
alignment > 0 and power-of-two
tile_stride = align_up(1024, alignment)
tile_padding = tile_stride - 1024
payload_bytes = 128 * 1024 = 131072
reserved_bytes = 128 * tile_stride
```

Required:

```text
tile_stride >= 1024
tile_stride % alignment == 0
tile_stride % 16 == 0
reserved_bytes has no overflow
reserved_bytes <= max_buffer_size
```

The payload allocation is one dedicated GPU buffer. Each tile is exposed through one 1024-byte dynamic storage binding with dynamic offset `tile_index * tile_stride`. Creating 128 payload buffers is forbidden.

## 5. Canonical physical address bijection

For tile `t`, row `r`, column `c`:

```text
tile_base(t) = allocation_base + t * tile_stride
scalar_address(t,r,c) = tile_base(t) + r * 64 + c * 4
```

For vec4 slot `v`:

```text
row = v >> 2
vec4_column = v & 3
vec4_address(t,v) = tile_base(t) + row * 64 + vec4_column * 16
```

Inverse mapping must recover exactly the original tile, row and column. Required closure:

```text
forward mappings=32768/32768
inverse mappings=32768/32768
duplicate payload address=0
missing payload address=0
cross-tile overlap=0
payload-padding alias=0
```

Logical coordinate authority and physical byte-address authority remain separate SSOT domains.

## 6. Allocation and padding ownership

```text
payload allocation count=1
allocation owner=Stage5
allocation mode=DedicatedAlignedTileBuffer
prepared allocation generation=33
published allocation generation=34
allocation identity immutable after prepare
```

The destination may not alias Stage4 source, Q/K/V, KV cache, logits or attention output. Allocation replacement after prepare, host-visible payload mapping, per-tile payload buffers and cross-device allocation are forbidden.

When `tile_padding > 0`, every padding word is initialized to poison `0x7fc00001`. Relocation must preserve all poison words and never read padding as tensor payload. When no padding is required, the guard reports `NoneRequired` with zero corruption.

## 7. Same-device relocation execution

The authoritative Stage5 shader is:

```text
crates/burn_webgpu_backend/src/shaders/tensorcube_atlas_physical_16x16_contiguous_copy.wgsl
entrypoint=main
workgroup_size=64
```

Each invocation copies exactly one vec4 from the Stage4 logical source into the bound 1024-byte Stage5 destination slot. No arithmetic, reduction, transpose, mirror, filtering, subgroup operation, barrier or atomic payload write is allowed.

Runtime matrix:

```text
Stage4 logical source tiles=128
Stage5 dynamic offsets=128
Stage5 dispatches=128
workgroups=128
vec4 relocations=8192
scalar relocations=32768
same-device relocation bytes=131072
```

This is an intentional device-local relocation, not zero-copy. Required movement counters:

```text
same-device relocation bytes=131072
host materializations=0
host uploads=0
host assemblies=0
payload readbacks=0
payload buffer maps=0
cross-device copies=0
```

## 8. Bit-exact parity and compact decision

Because Stage5 performs no arithmetic:

```text
Stage5Physical[t,r,c].to_bits() == Stage4Logical[t,r,c].to_bits()
```

The only host-visible GPU result is one 32-byte decision token containing eight u32 counters:

```text
payload mismatch
address mapping mismatch
row stride mismatch
tile stride mismatch
overlap or alias mismatch
alignment mismatch
padding corruption
allocation generation mismatch
```

PASS requires all eight counters to be zero. Tensor payload, sampled values and tensor-derived debug slices may not be read back.

## 9. KV boundary and fallback

Stage5 receives no KV write lease:

```text
KV writes=0
KV bytes changed=0
page-table mutations=0
residency mutations=0
KV bit-exact=true
```

Direct fallback:

```text
Stage5 -> Stage4
```

Inherited chain:

```text
Stage5 -> Stage4 -> Stage3 -> Stage2 -> Stage1 -> HeadwiseActive -> ReferenceActive
```

Required drill:

```text
Stage4 fallback tiles=128/128
Stage4 fallback scalars=32768/32768
direct Stage3/Stage2/Stage1/Headwise/Reference fallbacks=0
```

Fallback occurs before Stage5 publication and preserves Stage4 source identity, device, queue, KV state and generation 32.

## 10. Pointer and generation seal

The exact Stage4 pointer is the CAS compare value. Stage5 publication writes one v5 pointer record containing:

```text
parent and child stage IDs
feature mask 0x0f -> 0x1f
generation 32 -> 33 -> 34
parent runtime SHA
parent pointer SHA
allocation receipt SHA
physical layout digest
address map digest
stride/alignment digest
receipt digest
write_count=1
```

Any post-CAS failure restores the exact Stage4 pointer bytes. Blind overwrite, stale compare state, multiple writes, generation reuse or publication at generation 33 are terminal HOLD.

## 11. Evidence closure

Exactly 24 Atlas authority groups are required:

```text
identity
parent_binding
parent_stage4
parent_feature_mask
sealed_parent_reuse
stage5_feature
feature_transition
adapter_limits
allocation_plan
allocation_identity
row_stride
tile_stride
alignment
physical_address_map
address_bijection
padding_guard
source_binding
same_device_queue
relocation_parity
kv_parity
compact_decision
stage4_fallback
generation_pointer
verdict
```

The runtime root is a typed streaming Atlas group map. A giant authoritative root `serde_json::json!` expression or complete root `serde_json::Value` tree is forbidden.

The local manifest closes 27 child artifacts plus both parent artifacts, parent and child pointers, Stage4 and Stage5 shader SHA-256 values, adapter/alignment evidence, allocation identity, address and stride digests, CLI identity, binary identity, all group digests and the Atlas digest.

Strict CLI closure:

```text
R2-R10 extension keys=105
canonical registry keys=1622
canonical response-file keys=1622
missing=0
extra=0
duplicate=0
```

Negative controls:

```text
64 groups * 10 controls = 640
```

They cover parent, mask, geometry, stride, alignment, allocation, address bijection, padding, source binding, same-device identity, payload movement, parity, KV, fallback, pointer, generation, Atlas, manifest, binary and shader mutations.

## 12. PASS

PASS requires:

```text
parent R2-R9 PASS exact
HeadwiseActive unchanged
Stage4Active exact
mask 0x0f -> 0x1f
added bits=1/1
row stride=64
tile payload=1024
alignment observed from adapter
tile stride=align_up(1024,alignment)
one payload allocation
allocation identity stable
allocation generations=33/34
128 dynamic offsets
128/128 dispatches
8192/8192 vec4 relocations
32768/32768 scalar relocations
32768/32768 forward and inverse mappings
all eight decision counters=0
bit-exact relocation parity=true
padding preserved=true
same device and queue=true
KV writes=0
all host payload movement counters=0
compact decision=1 readback, 32 bytes
Stage4 fallback=128 tiles and 32768 scalars
direct lower fallbacks=0
generations=32/33/34
Atlas groups=24/24
negative controls=640/640
manifest closure exact
parent scientific terminal preserved
```

Expected summary:

```text
[r2f-r7-r6-r5-r1-r2-r10][summary] parent_r2_r9=PASS headwise_parent=HeadwiseActive parent_stage=Stage4Active stage=Stage5Active parent_feature=tensorcube-logical-16x16-four-microtile-composition-v1 feature=tensorcube-contiguous-16x16-physical-allocation-v1 mask=0x000000000000000f->0x000000000000001f added_bits=1/1 allocation_mode=DedicatedAlignedTileBuffer physical_layout=RowMajorF32Vec4 tile_count=128 logical_tile=16x16 row_stride_bytes=64 tile_payload_bytes=1024 adapter_alignment=<observed> tile_stride_bytes=<derived> tile_padding_bytes=<derived> allocation_reserved_bytes=<derived> allocation_identity_stable=true allocation_generations=33/34 dynamic_offsets=128/128 dynamic_offset_alignment_failures=0 stage5_dispatches=128/128 workgroups=128/128 vec4_relocations=8192/8192 scalar_relocations=32768/32768 same_device_relocation_bytes=131072 forward_address_mappings=32768/32768 inverse_address_mappings=32768/32768 payload_mismatch=0 address_mapping_mismatch=0 row_stride_mismatch=0 tile_stride_mismatch=0 overlap_or_alias_mismatch=0 alignment_mismatch=0 padding_corruption=0 allocation_generation_mismatch=0 bit_exact_relocation_parity=true same_device=true same_queue_lineage=true kv_writes=0 kv_bit_exact=true stage4_fallback_tiles=128/128 stage4_fallback_scalars=32768/32768 direct_stage3_fallbacks=0 direct_stage2_fallbacks=0 direct_stage1_fallbacks=0 direct_headwise_fallbacks=0 host_materializations=0 host_uploads=0 payload_readbacks=0 payload_buffer_maps=0 compact_decision_readbacks=1 compact_decision_bytes=32 cross_device_copies=0 generations=32/33/34 atlas_groups=24/24 new_negative=640/640 pass=true
```

Success token:

```text
PROMOTE_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_R1_R2_R10_TENSORCUBE_STAGE5_CONTIGUOUS16X16_PHYSICAL_ALLOCATION_STAGE4_PARENT_ROW_TILE_STRIDE_ALIGNMENT_AUTHORITY_PHYSICAL_ADDRESS_BIJECTION_PADDING_GUARD_SAME_DEVICE_BIT_EXACT_RELOCATION_EXACT_STAGE4_FALLBACK_AND_GENERATION_32_33_34_SEALED
```

## 13. HOLD

Any parent, feature, geometry, adapter-limit, allocation, alignment, row-stride, tile-stride, address, inverse-address, alias, padding, source-binding, same-device, parity, KV, payload, fallback, pointer, generation, Atlas, CLI, artifact, manifest, binary, shader or negative-control mismatch is terminal HOLD.

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_R1_R2_R10_STAGE5_PARENT_FEATURE_ALLOCATION_STRIDE_ALIGNMENT_ADDRESS_PADDING_PARITY_FALLBACK_OR_GENERATION_NOT_PROVEN
```
