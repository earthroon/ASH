# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5-R1-R2-R9

## TensorCube Stage 4 Logical 16×16 Composition / Stage3 Parent Binding / Four-Microtile Quadrant Ownership / Logical-to-Physical Coordinate Authority / Stage3 Reference Parity / Exact Stage3 Fallback / Generation 30→31→32 Seal

## 0. Authority

```text
PARENT=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5-R1-R2-R8
PARENT_VERDICT=PASS
PARENT_ROUTE=HeadwiseActive
PARENT_STAGE=Stage3Active
PARENT_STAGE_ID=tensorcube-stage-3-physical8x8-subgroup32-output-v1
PARENT_FEATURE_MASK=0x0000000000000007
PARENT_GENERATION=30
STAGE=Stage4Active
STAGE_ID=tensorcube-stage-4-logical16x16-composition-v1
FEATURE=tensorcube-logical-16x16-four-microtile-composition-v1
FEATURE_BIT=3
CHILD_FEATURE_MASK=0x000000000000000f
PREPARED_GENERATION=31
COMMITTED_GENERATION=32
IMPLEMENTATION_MODE=ExplicitComposeDispatch
IMPLEMENTATION_REVISION=R2-R9-stage4-logical16x16-explicit-compose-v1
WGSL_PATH=crates/burn_webgpu_backend/src/shaders/tensorcube_atlas_logical_16x16_compose.wgsl
DEFAULT_VERDICT=HOLD
```

R2-R9 adds one feature beneath sealed Stage 3. It performs no new arithmetic. Four immutable 8×8 subgroup32 microtile outputs are copied into one provisional logical 16×16 surface with explicit provenance. Physical contiguity is not claimed.

## 1. Parent binding

Required R2-R8 terminal facts:

```text
pass=true
verdict exact
headwise_route_state=HeadwiseActive
tensorcube_stage_state=Stage3Active
feature_mask_after=0x7
tensorcube_compute_dispatches=128
output_mismatch_count=0
non_finite_count=0
topology_mismatch_count=0
lane_packing_mismatch_count=0
tensorcube_kv_writes=0
generations=28/29/30
atlas_group_count=20
negative_control_passed=560
```

R2-R9 binds the parent runtime artifact, local manifest, Stage3 pointer, Stage3 shader identity, parent Atlas digest, device digest and scientific terminal by SHA-256. A complete parent set is reused without rebuild or recommit. Partial or mismatched parent state fails closed.

## 2. Feature and state ownership

Only this transition is legal:

```text
0x0000000000000007 -> 0x000000000000000f
popcount(parent XOR child)=1
bits 0..2 retained
bit 3 added
bits >=4 zero
```

```text
AttentionRouteState owner=R2-R5 value=HeadwiseActive mutable_by_R2_R9=false
TensorCubeStageState owner=R2-R9 Stage3Active -> Stage4Prepared -> Stage4Active|Stage4Fallback|Quarantined
TensorCubeFeatureMaskState owner=R2-R9 0x7 -> 0xf
LogicalTileCoordinateState owner=R2-R9
MicrotileQuadrantState owner=R2-R9
PhysicalMicrotileState owner=R2-R8 and immutable
StagePointerState owner=TensorCube registry Stage3 -> Stage4 CAS
KVOwnershipState owner=inherited registry, Stage4 KV write forbidden
ScientificEvidenceState owner=R1-R2 mutable_by_R2_R9=false
```

Logical coordinates, physical buffer offsets, quadrant identity and publication state are separate authorities.

## 3. Logical tile and quadrant model

```text
logical shape=16x16
logical scalars=256
microtile shape=8x8
scalars per microtile=64
microtiles per logical tile=4
quadrant order=TL/TR/BL/BR
TL id=0 origin=(0,0)
TR id=1 origin=(0,8)
BL id=2 origin=(8,0)
BR id=3 origin=(8,8)
```

For logical coordinate `(r,c)`:

```text
quadrant_row = r >> 3
quadrant_col = c >> 3
quadrant_id = quadrant_row * 2 + quadrant_col
micro_row = r & 7
micro_col = c & 7
micro_linear = micro_row * 8 + micro_col
```

Inverse mapping:

```text
logical_row = quadrant_row * 8 + micro_row
logical_col = quadrant_col * 8 + micro_col
```

Required closure:

```text
logical coordinates=256/256
quadrants=4/4
64 coordinates per quadrant
forward/inverse identity=true
duplicate coordinate=0
missing coordinate=0
row/column swap=0
TR/BL swap=0
mirror or transpose=0
```

## 4. Explicit composition execution

The selected mode is immutable:

```text
mode=ExplicitComposeDispatch
logical tiles=128
Stage3 parent microtile dispatches=512
compose workgroups=128
logical output vec4 writes=8192
logical output scalars=32768
```

Each Stage3 source is bound read-only. The composition shader writes:

```text
provisional logical output surface
per-scalar provenance source_linear = quadrant_id * 64 + micro_linear
```

Forbidden:

```text
payload arithmetic
reduction, interpolation or filtering
source overwrite
partial quadrant publication
host-side assembly
physical-contiguity claim
cross-microtile arithmetic
K-panel activation
```

## 5. GPU bit-exact parity and ownership

The GPU compares every Stage4 scalar against the selected Stage3 source using f32 bit patterns. A per-logical-tile 256-bit atomic source bitmap proves exactly-once source use.

Compact decision fields:

```text
logical scalar mismatch
quadrant identity mismatch
coordinate mapping mismatch
microtile identity mismatch
duplicate source
missing source
```

Required terminal values:

```text
logical scalar mismatch=0
quadrant identity mismatch=0
coordinate mapping mismatch=0
microtile identity mismatch=0
duplicate source=0
missing source=0
bit-exact parity=true
```

No numerical tolerance is allowed because composition performs no arithmetic.

## 6. Device, KV and payload boundary

```text
same physical device=true
same queue lineage=true
new adapter/device/queue=0
cross-device copies=0
KV writes=0
KV bytes changed=0
page-table mutations=0
residency mutations=0
KV bit-exact=true
host materializations=0
host uploads=0
host assemblies=0
payload readbacks=0
payload buffer maps=0
compact decision readbacks=1
compact decision bytes=24
```

Only the six decision counters may be host-visible.

## 7. Exact fallback

Direct fallback:

```text
Stage4 -> Stage3
```

Inherited chain:

```text
Stage4 -> Stage3 -> Stage2 -> Stage1 -> HeadwiseActive -> ReferenceActive
```

Required drill:

```text
Stage3 fallback logical tiles=128/128
Stage3 fallback microtiles=512/512
direct Stage2 fallbacks=0
direct Stage1 fallbacks=0
direct Headwise fallbacks=0
direct Reference fallbacks=0
```

Fallback occurs before Stage4 publication and preserves the same source identities, device, queue, KV state and generation 30 parent.

## 8. Pointer and generation seal

Stage3 compare value:

```text
schema=ash.attn.tensorcube.stage-pointer.v3
lineage_patch_id=R2-R8
active_stage_id=tensorcube-stage-3-physical8x8-subgroup32-output-v1
feature_mask_after=0x7
generation_after=30
pointer SHA == R2-R8 manifest stage_pointer_sha256
```

Stage4 publication:

```text
schema=ash.attn.tensorcube.stage-pointer.v4
lineage_patch_id=R2-R9
parent_stage_id=tensorcube-stage-3-physical8x8-subgroup32-output-v1
active_stage_id=tensorcube-stage-4-logical16x16-composition-v1
feature_mask_before=0x7
feature_mask_after=0xf
generation_before=30
prepared_generation=31
generation_after=32
write_count=1
parent runtime SHA exact
parent pointer SHA exact
quadrant map digest exact
receipt digest exact
```

Any post-CAS failure restores the exact Stage3 pointer bytes. Blind overwrite, stale compare state, multiple writes or publication at generation 31 are HOLD.

## 9. Evidence closure

```text
R2-R9 CLI extension keys=90
child artifacts before manifest=24
Atlas authority groups=22
negative controls=600
runtime root=typed streaming
full-root serde_json::Value authority tree=forbidden
```

Atlas groups:

```text
identity
parent_binding
parent_stage3
parent_feature_mask
sealed_parent_reuse
stage4_feature
feature_transition
logical_tile_shape
quadrant_table
forward_coordinate_map
inverse_coordinate_map
microtile_identity
microtile_ownership
composition_mode
same_device_queue
bit_exact_parity
kv_parity
compact_decision
stage3_fallback
generation_pointer
negative_controls
verdict
```

Negative controls cover parent mutation, pointer mismatch, feature corruption, quadrant permutation, mirrors/transposes, off-by-one boundaries, duplicate/missing identities, mixed generation/device/layout, mode drift, partial publication, source overwrite, payload movement, fallback skip, generation drift, Atlas mutation, manifest omission and binary drift.

## 10. PASS

```text
parent R2-R8 PASS exact
sealed parent reused without recommit
HeadwiseActive unchanged
Stage3Active exact
mask 0x7 -> 0xf
added bits=1/1
logical tile=16x16
microtile=8x8
quadrants=TL/TR/BL/BR
logical tiles=128/128
parent microtiles=512/512
logical scalars=32768/32768
all six decision counters=0
bit-exact parity=true
same device and queue=true
KV writes=0
payload movement counters=0
compact decision=1 readback, 24 bytes
Stage3 fallback=128 logical tiles and 512 microtiles
direct lower fallbacks=0
generations=30/31/32
Atlas groups=22/22
negative controls=600/600
manifest closure exact
parent scientific terminal preserved
```

Expected summary:

```text
[r2f-r7-r6-r5-r1-r2-r9][summary] parent_r2_r8=PASS headwise_parent=HeadwiseActive parent_stage=Stage3Active stage=Stage4Active parent_feature=tensorcube-physical-8x8-subgroup32-register-shuffle-output-v1 feature=tensorcube-logical-16x16-four-microtile-composition-v1 mask=0x0000000000000007->0x000000000000000f added_bits=1/1 logical_tile=16x16 microtile=8x8 microtiles_per_logical_tile=4 quadrants=4/4 quadrant_order=TL/TR/BL/BR logical_tiles=128/128 parent_microtiles=512/512 logical_scalars=32768/32768 logical_scalar_mismatch=0 quadrant_identity_mismatch=0 coordinate_mapping_mismatch=0 microtile_identity_mismatch=0 duplicate_source=0 missing_source=0 bit_exact_parity=true same_device=true same_queue_lineage=true kv_writes=0 kv_bit_exact=true stage3_fallback_logical_tiles=128/128 stage3_fallback_microtiles=512/512 direct_stage2_fallbacks=0 direct_stage1_fallbacks=0 direct_headwise_fallbacks=0 host_materializations=0 host_uploads=0 payload_readbacks=0 payload_buffer_maps=0 compact_decision_readbacks=1 compact_decision_bytes=24 cross_device_copies=0 generations=30/31/32 atlas_groups=22/22 new_negative=600/600 pass=true
```

Success token:

```text
PROMOTE_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_R1_R2_R9_TENSORCUBE_STAGE4_LOGICAL16X16_COMPOSITION_STAGE3_PARENT_FOUR_MICROTILE_QUADRANT_OWNERSHIP_LOGICAL_PHYSICAL_COORDINATE_AUTHORITY_STAGE3_REFERENCE_PARITY_EXACT_FALLBACK_AND_GENERATION_30_31_32_SEALED
```

## 11. HOLD

Any parent, feature, logical shape, quadrant, coordinate, ownership, composition mode, same-device, parity, KV, payload, fallback, pointer, generation, Atlas, CLI, artifact, manifest, binary or negative-control mismatch is terminal HOLD. No automatic quadrant repair, coordinate transpose, host assembly, tolerance broadening, parent regeneration or hidden lower-stage fallback counted as Stage4 success is allowed.

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_R1_R2_R9_STAGE4_PARENT_FEATURE_QUADRANT_COORDINATE_OWNERSHIP_PARITY_FALLBACK_OR_GENERATION_NOT_PROVEN
```
