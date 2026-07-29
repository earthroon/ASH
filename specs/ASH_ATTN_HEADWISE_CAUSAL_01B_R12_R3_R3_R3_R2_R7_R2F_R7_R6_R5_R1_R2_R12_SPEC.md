# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5-R1-R2-R12

## TensorCube Stage 7 Multi-Tile Dispatch Grid / Head·KV-Block Coordinate Ownership / Dispatch-ID Bijection / Duplicate·Missing Tile Exclusion / Exact Stage6 Fallback / Generation 36→37→38 Seal

## 0. Authority

```text
PARENT=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5-R1-R2-R11
PARENT_VERDICT=PASS
PARENT_ROUTE=HeadwiseActive
PARENT_STAGE=Stage6Active
PARENT_STAGE_ID=tensorcube-stage-6-multi-k-panel-accumulation-v1
PARENT_FEATURE=tensorcube-multi-k-panel-ordered-register-accumulation-v1
PARENT_FEATURE_MASK=0x000000000000003f
PARENT_GENERATION=36

STAGE=Stage7Active
STAGE_ID=tensorcube-stage-7-multi-tile-dispatch-grid-v1
FEATURE=tensorcube-multi-tile-head-kv-block-dispatch-grid-v1
FEATURE_BIT=6
CHILD_FEATURE_MASK=0x000000000000007f
PREPARED_GENERATION=37
COMMITTED_GENERATION=38

IMPLEMENTATION_REVISION=R2-R12-stage7-multi-tile-dispatch-grid-v1
CLI_EXTENSION_KEYS=130
CANONICAL_REGISTRY_KEYS=1874
CANONICAL_RESPONSE_FILE_LINES=3748
ATLAS_GROUPS=31
NEGATIVE_CONTROLS=800
CHILD_ARTIFACTS=36
CHILD_ARTIFACT_LIST_SHA256=99d791578254d3ae82e78e2a6dabf79c3e4d01d4acc97e9a3cc9c24acd19494c
DEFAULT_VERDICT=HOLD
```

R2-R12 activates one feature beneath sealed Stage 6. It assigns every `(query_head, kv_block, quadrant)` coordinate to exactly one GPU workgroup and every `(query_head, kv_block)` pair to exactly one inherited Stage6 16×16 output tile. Stage6 arithmetic, ordered K-panel accumulation, subgroup packing, physical layout, and final-write-once semantics remain immutable.

## 1. Parent binding

The direct parent must prove:

```text
pass=true
stage=Stage6Active
feature_mask_after=0x3f
head_dim=64
panel_width=8
panel_count=8
logical_tiles=128
quadrant_workgroups=512
output_scalars=32768
all twelve Stage6 decision counters=0
bit_exact_parity=true
KV writes=0
host payload movement counters=0
compact decision=1 readback, 48 bytes
generations=34/35/36
Atlas groups=29/29
negative controls=720/720
child artifacts=33/33
```

R2-R12 binds the parent runtime artifact, local manifest, Stage6 pointer, three Stage6 shaders, parent device digest, Atlas digest, and scientific terminal by SHA-256. Parent regeneration, mutation, or recommit is forbidden.

## 2. Feature and state transition

```text
0x000000000000003f -> 0x000000000000007f
popcount(parent XOR child)=1
bits 0..5 retained
bit 6 added
bits >=7 remain zero

Stage6Active -> Stage7Prepared -> Stage7Active
Generation 36 -> 37 -> 38
```

Attention route remains `HeadwiseActive`. Stage7 receives no KV write lease and does not publish production attention output.

## 3. Dispatch-grid SSOT

```text
query heads=32
KV heads=4
GQA group size=8
KV block width=16
KV blocks/query head=4
KV span/query head=64
logical tiles=128
quadrants/tile=4

dispatch_workgroups(x=4, y=32, z=4)
dispatch calls=1
total workgroups=512
workgroup size=32
subgroup size=32
```

GPU workgroup execution order is not part of the contract. Each workgroup derives identity only from `workgroup_id`.

```text
kv_block_id    = workgroup_id.x
query_head_id  = workgroup_id.y
quadrant_id    = workgroup_id.z
kv_head_id     = query_head_id / 8
```

## 4. Tile and workgroup bijection

```text
tile_dispatch_id = query_head_id * 4 + kv_block_id
query_head_id     = tile_dispatch_id / 4
kv_block_id       = tile_dispatch_id % 4

workgroup_linear_id = tile_dispatch_id * 4 + quadrant_id
tile_dispatch_id    = workgroup_linear_id / 4
quadrant_id          = workgroup_linear_id % 4
```

Required closure:

```text
tile forward mappings=128/128
tile inverse mappings=128/128
unique tile IDs=128/128
workgroup forward mappings=512/512
workgroup inverse mappings=512/512
unique workgroup IDs=512/512
duplicate tile IDs=0
missing tile IDs=0
duplicate workgroup IDs=0
missing workgroup IDs=0
out-of-range coordinates=0
```

## 5. Duplicate and missing exclusion

GPU-only evidence surfaces:

```text
tile bitmap=128 bits, 4 u32 words
workgroup bitmap=512 bits, 16 u32 words
output ownership audit=8192 vec4 slots
```

Candidate workgroups use atomic bit claims. A finalize pass verifies complete expected masks and exact write count one for every output vec4 slot. Coverage bitmaps are never mapped or read back as payload.

## 6. Output ownership

```text
output_tile_slot = tile_dispatch_id

quadrant 0 owns tile-local vec4 slots  0..15
quadrant 1 owns tile-local vec4 slots 16..31
quadrant 2 owns tile-local vec4 slots 32..47
quadrant 3 owns tile-local vec4 slots 48..63

output tiles=128/128
output vec4 slots=8192/8192
output scalars=32768/32768
cross-head alias=0
cross-block alias=0
cross-quadrant alias=0
```

The physical tile stride is inherited from Stage5/Stage6 and is never hard-coded as a semantic authority.

## 7. Candidate and Stage6 reference

Authoritative shaders:

```text
crates/burn_webgpu_backend/src/shaders/tensorcube_atlas_multi_tile_dispatch_grid_16x16_subgroup32.wgsl
crates/burn_webgpu_backend/src/shaders/tensorcube_atlas_multi_tile_dispatch_grid_verify.wgsl
```

Candidate:

```text
single dispatch 4×32×4
workgroup_id-derived head/block/quadrant identity
inherited Stage6 ordered multi-K arithmetic
inherited low/high source-domain packing
inherited final-write-once output
```

Reference:

```text
sealed Stage6 linear schedule 4×1×128
same GPU-generated head/block-distinguishing operands
same f32 panel-local FMA grouping
same physical output layout
```

Parity is bit-exact. Numerical tolerance is forbidden.

## 8. Compact decision

One 56-byte token contains fourteen measured u32 counters:

```text
output mismatch
non-finite
tile dispatch-ID mismatch
head ownership mismatch
KV-head ownership mismatch
KV-block ownership mismatch
quadrant ownership mismatch
duplicate tile
missing tile
duplicate workgroup
missing workgroup
out-of-range coordinate
output-slot alias
grid-dimension mismatch
```

PASS requires all counters to be zero.

```text
compact decision readbacks=1
compact decision bytes=56
payload readbacks=0
payload buffer maps=0
host materializations=0
host uploads=0
cross-device copies=0
KV writes=0
```

Atlas groups, individual artifacts, runtime artifact, and manifest must serialize these measured runtime counters. Literal zero, literal `all_zero=true`, or literal PASS evidence is forbidden.

## 9. Exact fallback

```text
Stage7 -> Stage6 -> Stage5 -> Stage4 -> Stage3 -> Stage2 -> Stage1 -> HeadwiseActive -> ReferenceActive
```

Required direct drill:

```text
Stage6 fallback tiles=128/128
Stage6 fallback scalars=32768/32768
direct Stage5/Stage4/Stage3/Stage2/Stage1/Headwise/Reference fallbacks=0
```

Failure preserves the exact Stage6 pointer, feature mask `0x3f`, and generation 36. Partial Stage7 output publication is forbidden.

## 10. Pointer seal

The exact Stage6 pointer is the CAS compare value. Stage7 writes one v7 pointer record containing:

```text
parent and child stage IDs
feature mask 0x3f -> 0x7f
generation 36 -> 37 -> 38
parent runtime SHA
parent pointer SHA
grid-shape digest
coordinate-ownership digest
dispatch-bijection digest
candidate shader SHA
receipt digest
write_count=1
```

Any post-CAS failure restores the exact Stage6 pointer bytes.

## 11. Atlas and artifact closure

Exactly 31 Atlas authority groups are required:

```text
identity, parent_binding, parent_stage6, parent_feature_mask,
sealed_parent_reuse, stage7_feature, feature_transition,
profile_head_geometry, gqa_head_map, kv_block_geometry, grid_shape,
grid_coordinate_ownership, tile_dispatch_forward_map,
tile_dispatch_inverse_map, workgroup_forward_map,
workgroup_inverse_map, quadrant_ownership, output_tile_ownership,
output_slot_ownership, tile_coverage, workgroup_coverage,
operand_identity, stage6_reference, bit_exact_parity,
final_write_once, same_device_queue, kv_parity, compact_decision,
stage6_fallback, generation_pointer, verdict
```

The child artifact count is derived only from one canonical ordered suffix array:

```text
CHILD_ARTIFACT_EXPECTED = CHILD_ARTIFACT_SUFFIXES.len() = 36
actual suffix list == canonical suffix list
actual suffix-list SHA-256 == 99d791578254d3ae82e78e2a6dabf79c3e4d01d4acc97e9a3cc9c24acd19494c
count-only acceptance forbidden
```

CLI closure:

```text
R2-R12 extension keys=130
canonical registry keys=1874
response-file key/value pairs=1874
response-file lines=3748
missing keys=0
extra keys=0
duplicate keys=0
empty lines=0
```

Negative controls:

```text
80 families × 10 cases = 800/800
```

## 12. PASS

```text
parent R2-R11 PASS exact
HeadwiseActive unchanged
Stage6Active exact
mask 0x3f -> 0x7f
added bits=1/1
query heads=32
KV heads=4
GQA group size=8
KV block width=16
KV blocks/head=4
logical tiles=128/128
grid=4×32×4
dispatch calls=1/1
workgroups=512/512
all tile/workgroup mappings exact
all duplicate/missing counters=0
output tiles=128/128
output vec4 slots=8192/8192
output scalars=32768/32768
all fourteen decision counters=0
bit-exact parity=true
same device and queue=true
KV writes=0
host payload movement counters=0
compact decision=1 readback, 56 bytes
Stage6 fallback=128 tiles and 32768 scalars
direct lower fallbacks=0
generations=36/37/38
Atlas groups=31/31
negative controls=800/800
child artifacts=36/36
artifact ordered suffix list exact
manifest closure exact
```

Success token:

```text
PROMOTE_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_R1_R2_R12_TENSORCUBE_STAGE7_MULTI_TILE_DISPATCH_GRID_STAGE6_PARENT_HEAD_KV_BLOCK_COORDINATE_OWNERSHIP_GQA_MAP_DISPATCH_ID_BIJECTION_DUPLICATE_MISSING_EXCLUSION_STAGE6_REFERENCE_PARITY_EXACT_FALLBACK_AND_GENERATION_36_37_38_SEALED
```

## 13. HOLD

Any parent identity, feature mask, profile geometry, GQA mapping, KV-block geometry, grid shape, coordinate ownership, tile/workgroup bijection, coverage, output ownership, operand identity, Stage6 parity, final-write-once, device, queue, KV boundary, host movement, compact decision, fallback, pointer, generation, Atlas, CLI, artifact-list, manifest, binary, shader, or negative-control mismatch is terminal HOLD.

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_R1_R2_R12_STAGE7_PARENT_GRID_COORDINATE_BIJECTION_COVERAGE_PARITY_FALLBACK_OR_GENERATION_NOT_PROVEN
```
