# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5-R1-R2-R8

## TensorCube Stage 3 Subgroup Fast-Path Activation / Stage2 Parent Binding / Single-Feature Mask Accumulation / Exact 32-Lane Mapping / Workgroup Reference Parity / Exact Stage2 Fallback / Generation 28→29→30 Seal

## 0. Authority

```text
PARENT=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5-R1-R2-R7
PARENT_VERDICT=PASS
PARENT_ROUTE=HeadwiseActive
PARENT_STAGE=Stage2Active
PARENT_MASK=0x0000000000000003
PARENT_GENERATION=28
STAGE=Stage3Active
FEATURE=tensorcube-physical-8x8-subgroup32-register-shuffle-output-v1
FEATURE_BIT=2
CHILD_MASK=0x0000000000000007
PREPARED_GENERATION=29
COMMITTED_GENERATION=30
IMPLEMENTATION_REVISION=R2-R8-R2-subgroup-pack-source-domain-closure-v1
WGSL_DIALECT=wgpu26_native_no_enable_v1
DEFAULT_VERDICT=HOLD
```

R2-R8 activates exactly one feature beneath sealed Stage 2. The top-level attention route remains `HeadwiseActive`. Stage 3 is a real 8×8 f32 subgroup32 numerical path, not the existing experimental shuffle seam.

Authoritative shaders:

```text
Stage2 reference=crates/burn_webgpu_backend/src/shaders/tensorcube_atlas_microtile_8x8_parity_workgroup.wgsl
Stage3 candidate=crates/burn_webgpu_backend/src/shaders/tensorcube_atlas_microtile_8x8_parity_subgroup32.wgsl
Topology probe=crates/burn_webgpu_backend/src/shaders/headwise_gqa4_subgroup_topology_probe.wgsl
Excluded experiment=crates/burn_webgpu_backend/src/shaders/tensorcube_atlas_microtile_8x8_subgroup_exp.wgsl
```

`enable subgroups;` is forbidden in wgpu 26 WGSL. SUBGROUP capability is requested through the device feature and proved through the runtime topology receipt.

## 1. Parent binding

Required R2-R7 terminal facts:

```text
pass=true
stage=Stage2Active
feature_mask_after=0x3
generation_after=28
dispatches=128/128
output_mismatch=0
non_finite=0
KV writes=0
Atlas groups=18/18
negative controls=520/520
```

R2-R8 binds the R2-R7 runtime artifact, local manifest, Stage2 pointer and Atlas digest by SHA-256. A complete exact parent set is reused without rebuild or recommit. A partial or mismatched parent set fails closed.

## 2. Feature transition and state ownership

Only this transition is legal:

```text
0x0000000000000003 -> 0x0000000000000007
popcount(parent XOR child)=1
bits 0 and 1 retained
bit 2 added
bits >=3 remain zero
```

```text
AttentionRouteState owner=R2-R5 value=HeadwiseActive mutable_by_R2_R8=false
TensorCubeStageState owner=R2-R8 Stage2Active -> Stage3Prepared -> Stage3Active|Stage3Fallback|Quarantined
TensorCubeFeatureMaskState owner=R2-R8 0x3 -> 0x7
StagePointerState owner=TensorCube registry Stage2 -> Stage3 CAS
KVOwnershipState owner=inherited runtime registry, Stage3 KV writes forbidden
ScientificEvidenceState owner=R1-R2 mutable_by_R2_R8=false
```

## 3. Exact subgroup topology

```text
workgroup_size=32
subgroup_size=32
subgroups_per_workgroup=1
subgroup_id=0
lane_range=0..31
lane_mask=0xffffffff
lane_coverage=32/32
```

Any size other than 32, multiple subgroups, partial coverage, a new adapter/device/queue, or an inferred rather than measured topology selects exact Stage 2 fallback before Stage 3 publication.

## 4. Lane ownership

For lane `L`:

```text
column=L & 7
row_low=L >> 3
row_high=row_low + 4
```

Each lane owns exactly:

```text
C[row_low][column]
C[row_high][column]
```

Therefore 32 lanes cover exactly 64 output scalars with no duplicate or missing coordinate.

## 5. Register exchange and arithmetic

For each `k=0..7`, lanes `0..7` seed A and B. Every lane executes the same three compute shuffles:

```text
a_low=subgroupShuffle(a_seed,row_low)
a_high=subgroupShuffle(a_seed,row_high)
b_value=subgroupShuffle(b_seed,column)
acc_low=fma(a_low,b_value,acc_low)
acc_high=fma(a_high,b_value,acc_high)
```

Compute contract:

```text
K steps=8
compute shuffles/lane=24
FMA/lane=16
shared memory bytes=0
workgroup barriers=0
atomics=0
```

## 6. Packing source-domain closure

There are 16 pack owners. Each owner writes one vec4. The low and high accumulator domains must remain separate until after subgroup exchange:

```text
packed_low = four subgroupShuffle(acc_low, source_lane) operations
packed_high = four subgroupShuffle(acc_high, source_lane) operations
packed = destination_pack_row < 4 ? packed_low : packed_high
```

Required packing contract:

```text
pack owners=16
vec4 writes=16
components/write=4
packing shuffles/lane=8
total shuffles/lane=32
low/high source domains separate=true
single writer per vec4 slot=true
```

Forbidden pattern:

```text
selected=select(acc_low,acc_high,destination_condition)
subgroupShuffle(selected,source_lane)
```

That pattern applies the low/high choice in the source lane's domain and aliases rows 4..7 onto rows 0..3. It produces exactly 32 mismatches per tile, or 4096 mismatches across 128 tiles, and is terminal HOLD.

## 7. Same-device numerical parity

Each supported attempt executes on one device and queue lineage:

```text
Stage2 workgroup reference dispatch
Stage3 subgroup32 candidate dispatch
GPU-side Stage3-vs-Stage2 compare dispatch
```

Runtime matrix:

```text
attempts=128
Stage2 reference dispatches=128
Stage3 dispatches=128
Stage3 subgroups=128
output tiles=128
output scalars=8192
```

A scalar passes when `abs_error <= 1e-4` or `rel_error <= 1e-4`.

Required terminal counters:

```text
output mismatch=0
non-finite=0
topology mismatch=0
lane/packing mismatch=0
```

## 8. KV and payload boundary

```text
KV writes=0
KV bytes changed=0
page-table mutations=0
residency mutations=0
KV bit-exact=true
host materializations=0
host uploads=0
payload readbacks=0
payload buffer maps=0
cross-device copies=0
compact decision readbacks=1
compact decision bytes=16
```

The compact token may contain only output mismatch, non-finite, topology mismatch and lane/packing mismatch counts.

## 9. Exact fallback

Direct fallback:

```text
Stage3 -> Stage2
```

Inherited chain:

```text
Stage3 -> Stage2 -> Stage1 -> HeadwiseActive -> ReferenceActive
```

While Stage 2 is healthy, direct Stage 1, Headwise or Reference fallback is forbidden. Required drill:

```text
Stage2 fallback dispatches=128/128
direct Stage1 fallbacks=0
direct Headwise fallbacks=0
direct Reference fallbacks=0
```

## 10. Pointer and generation seal

The Stage2 pointer is the CAS compare value. Stage3 publication writes one pointer record containing parent pointer SHA, parent runtime SHA, mask `0x3 -> 0x7`, and generations `28 -> 29 -> 30`. Any post-CAS failure restores the exact Stage2 pointer bytes. Blind overwrite, stale compare state or multiple writes are terminal HOLD.

## 11. Atlas, CLI and controls

```text
Atlas groups=20
CLI extension keys=77
child artifacts before manifest=23
negative controls=560
runtime root=typed streaming
full-root serde_json::Value tree=forbidden
```

Static shader closure requires:

```text
subgroupShuffle call sites=11
compute shuffle schedule=3 calls inside 8-step loop
packing shuffle sites=8
packed_low present
packed_high present
destination-domain vec4 select present
subgroupShuffle(selected,...) absent
enable subgroups directive absent
shared memory absent
barriers absent
atomics absent
```

## 12. PASS

PASS requires every parent, feature, topology, lane, packing source-domain, same-device, parity, KV, payload, fallback, pointer, generation, Atlas, CLI, artifact, manifest and negative-control check to pass exactly.

Expected summary:

```text
[r2f-r7-r6-r5-r1-r2-r8][summary]
parent_r2_r7=PASS
headwise_parent=HeadwiseActive
parent_stage=Stage2Active
stage=Stage3Active
mask=0x0000000000000003->0x0000000000000007
added_bits=1/1
same_device=true
same_queue_lineage=true
workgroup_size=32
subgroup_size=32
subgroups_per_workgroup=1
lane_coverage=32/32
outputs_per_lane=2
pack_owners=16
compute_shuffles_per_lane=24
pack_shuffles_per_lane=8
total_shuffles_per_lane=32
fma_per_lane=16
tensorcube_dispatches=128/128
subgroups=128/128
output_scalars=8192/8192
output_mismatch=0
non_finite=0
topology_mismatch=0
lane_packing_mismatch=0
kv_writes=0
kv_bit_exact=true
stage2_fallback_dispatches=128/128
host_materializations=0
host_uploads=0
payload_readbacks=0
payload_buffer_maps=0
compact_decision_readbacks=1
compact_decision_bytes=16
cross_device_copies=0
generations=28/29/30
atlas_groups=20/20
new_negative=560/560
pass=true
```

Success token:

```text
PROMOTE_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_R1_R2_R8_TENSORCUBE_STAGE3_SUBGROUP32_FASTPATH_ACTIVATION_STAGE2_PARENT_SINGLE_FEATURE_ACCUMULATION_EXACT_LANE_MAPPING_WORKGROUP_REFERENCE_PARITY_EXACT_STAGE2_FALLBACK_AND_GENERATION_28_29_30_SEALED
```

## 13. HOLD

Any mismatch is terminal HOLD. No automatic source-domain repair, tolerance broadening, hidden workgroup fallback counted as Stage3 success, parent regeneration, feature-mask repair, topology remapping or payload readback is allowed.
