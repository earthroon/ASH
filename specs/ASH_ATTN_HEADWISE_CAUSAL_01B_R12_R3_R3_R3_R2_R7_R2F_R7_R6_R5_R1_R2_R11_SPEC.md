# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5-R1-R2-R11

## TensorCube Stage 6 Multi-K-Panel Accumulation / Ordered Panel Loop / Register Accumulator Persistence / Final-Write-Once Authority / Exact Stage5 Fallback / Generation 34→35→36 Seal

## 0. Authority

```text
PARENT=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5-R1-R2-R10
PARENT_VERDICT=PASS
PARENT_ROUTE=HeadwiseActive
PARENT_STAGE=Stage5Active
PARENT_STAGE_ID=tensorcube-stage-5-contiguous16x16-physical-allocation-v1
PARENT_FEATURE=tensorcube-contiguous-16x16-physical-allocation-v1
PARENT_FEATURE_MASK=0x000000000000001f
PARENT_GENERATION=34

STAGE=Stage6Active
STAGE_ID=tensorcube-stage-6-multi-k-panel-accumulation-v1
FEATURE=tensorcube-multi-k-panel-ordered-register-accumulation-v1
FEATURE_BIT=5
CHILD_FEATURE_MASK=0x000000000000003f
PREPARED_GENERATION=35
COMMITTED_GENERATION=36

IMPLEMENTATION_REVISION=R2-R11-R2-child-artifact-list-ssot-v1
CLI_EXTENSION_KEYS=122
CANONICAL_REGISTRY_KEYS=1744
CANONICAL_RESPONSE_FILE_LINES=3488
ATLAS_GROUPS=29
NEGATIVE_CONTROLS=720
CHILD_ARTIFACTS=33
DEFAULT_VERDICT=HOLD
```

R2-R11 activates exactly one feature beneath sealed Stage 5. It extends the K dimension from one 8-wide panel to eight ordered panels covering `head_dim=64`. It does not activate real Q/K/V adoption, KV writes, softmax, production output routing, tail panels, mixed precision, or cross-device execution.

## 1. Parent binding

The direct parent must prove:

```text
pass=true
stage=Stage5Active
feature_mask_after=0x1f
tile_count=128
tensorcube_output_scalars=32768
all Stage5 address/stride/alignment/parity counters=0
KV writes=0
generations=32/33/34
Atlas groups=24/24
negative controls=640/640
```

R2-R11 binds by SHA-256 the R2-R10 runtime artifact, manifest, Stage5 pointer, Stage5 relocation shader, device digest, Atlas digest, and parent scientific terminal. The parent is reused without rebuild, recommit, or mutation.

## 2. State and feature ownership

```text
AttentionRouteState owner=R2-R5 value=HeadwiseActive mutable_by_R2_R11=false
TensorCubeStageState owner=R2-R11 Stage5Active -> Stage6Prepared -> Stage6Active|Stage6Fallback|Quarantined
TensorCubeFeatureMaskState owner=R2-R11 0x1f -> 0x3f
PhysicalTileAddressState owner=R2-R10 mutable_by_R2_R11=false
PanelScheduleState owner=R2-R11
AccumulatorLifetimeState owner=R2-R11
FinalWriteOwnershipState owner=R2-R11
ChildArtifactListState owner=R2-R11 canonical ordered suffix list
StagePointerState owner=TensorCube registry Stage5 -> Stage6 CAS
KVOwnershipState owner=inherited registry, Stage6 write lease=none
ScientificEvidenceState owner=R1-R2 mutable_by_R2_R11=false
```

Only this transition is legal:

```text
0x000000000000001f -> 0x000000000000003f
popcount(parent XOR child)=1
bits 0..4 retained
bit 5 added
bits >=6 remain zero
```

## 3. K-panel geometry and ordered loop

```text
head_dim=64
panel_width=8
panel_count=8
covered_k=64
remainder_k=0
panel order=0,1,2,3,4,5,6,7
```

Tail panels are forbidden. Any head dimension, width, count, coverage, skip, duplicate, reverse order, tree reduction, or reassociation drift is terminal HOLD.

For each output scalar:

```text
acc = +0.0f
for panel in 0..7:
    panel_acc = +0.0f
    for panel_k in 0..7:
        k = panel * 8 + panel_k
        panel_acc = fma(A[row,k], B[k,column], panel_acc)
    acc = acc + panel_acc
```

The Stage5-layout-derived GPU oracle uses the same panel-local FMA grouping and ordered panel addition. No numerical tolerance is allowed.

## 4. Subgroup32 quadrant topology

```text
logical tiles=128
quadrants per tile=4
quadrant order=TL/TR/BL/BR
workgroups=512
workgroup size=32
subgroup size=32
subgroups per workgroup=1
panel iterations=4096
```

A new 128-thread multi-subgroup assumption is forbidden. Each logical 16×16 tile is produced by four disjoint exact-subgroup32 quadrant workgroups.

## 5. Private accumulator persistence

Every subgroup lane owns two WGSL function-private accumulators:

```text
acc_low
acc_high
```

They are initialized exactly once before the panel loop, persist across all eight panels, and are consumed only by terminal packing after the loop. Storage-buffer and workgroup-memory accumulator paths are forbidden. Physical ISA register residency is not claimed without backend disassembly evidence.

R2-R8-R2 packing semantics remain mandatory:

```text
packed_low  = subgroupShuffle(acc_low, source_lane)
packed_high = subgroupShuffle(acc_high, source_lane)
packed      = select(packed_low, packed_high, destination_condition)
```

Selecting low/high in the source lane before shuffle is forbidden. The historical `4096/8192` mismatch signature remains a required negative control.

## 6. Final-write-once authority

No Stage6 output store may occur inside the panel loop. After terminal packing, exactly 16 pack-owner lanes per quadrant write disjoint vec4 slots.

```text
vec4 writes per quadrant=16
vec4 writes per tile=64
final vec4 writes=8192
final scalar writes=32768
intermediate output writes=0
zero-write slots=0
multi-write slots=0
out-of-range writes=0
cross-quadrant alias=0
```

A per-slot atomic write-count surface and complete-coverage audit prove exactly-once final publication.

## 7. GPU execution and oracle

Authoritative shaders:

```text
crates/burn_webgpu_backend/src/shaders/tensorcube_atlas_multi_k_panel_16x16_subgroup32.wgsl
crates/burn_webgpu_backend/src/shaders/tensorcube_atlas_multi_k_panel_16x16_oracle.wgsl
crates/burn_webgpu_backend/src/shaders/tensorcube_atlas_multi_k_panel_16x16_verify.wgsl
```

Execution receipt:

```text
scalar FMAs per lane per panel=16
scalar FMAs per lane=128
scalar FMAs per tile=16384
scalar FMAs total=2097152
compute shuffles per lane=192
final pack shuffles per lane=8
total shuffles per lane=200
oracle workgroups=512
oracle output scalars=32768
oracle intermediate partial tiles=0
```

These are execution counts, not a performance-superiority claim.

## 8. Compact verification

Only one 48-byte decision token containing twelve u32 counters may be host-visible:

```text
output mismatch
non-finite
panel order mismatch
panel skip
panel duplicate
K coverage mismatch
accumulator initialization mismatch
accumulator persistence mismatch
intermediate output write
final write-count mismatch
quadrant topology mismatch
lane packing mismatch
```

PASS requires all twelve counters to be zero and every Stage6 output bit pattern to equal the oracle output bit pattern.

```text
host materializations=0
host uploads=0
payload readbacks=0
payload buffer maps=0
compact decision readbacks=1
compact decision bytes=48
cross-device copies=0
KV writes=0
KV bit-exact=true
```

## 9. Exact fallback

```text
Stage6 -> Stage5 -> Stage4 -> Stage3 -> Stage2 -> Stage1 -> HeadwiseActive -> ReferenceActive
```

Required direct drill:

```text
Stage5 fallback tiles=128/128
Stage5 fallback scalars=32768/32768
direct Stage4/Stage3/Stage2/Stage1/Headwise/Reference fallbacks=0
```

Fallback occurs before Stage6 publication and preserves the Stage5 pointer, mask `0x1f`, generation 34, device, queue, physical layout, and KV state.

## 10. Pointer and generation seal

The exact Stage5 pointer is the CAS compare value. Stage6 publication writes one v6 pointer record containing:

```text
parent and child stage IDs
feature mask 0x1f -> 0x3f
generation 34 -> 35 -> 36
parent runtime SHA
parent pointer SHA
panel schedule digest
accumulator contract digest
final-write digest
fast shader SHA
receipt digest
write_count=1
```

Any post-CAS failure restores the exact Stage5 pointer bytes. Blind overwrite, stale compare state, multiple writes, generation reuse, or publication at generation 35 is HOLD.

## 11. Evidence closure

The runtime root is a typed Atlas parallel streaming group map. A giant authoritative root `serde_json::json!` expression or complete root `serde_json::Value` tree is forbidden.

```text
R2-R11 extension keys=122
canonical registry keys=1744
canonical response-file keys=1744
canonical response-file lines=3488
empty or whitespace-only lines=0
Atlas groups=29/29
negative controls=720/720
child artifacts=33
```

The 33 child artifacts are governed by one ordered canonical suffix array. `CHILD_ARTIFACT_EXPECTED` is derived from that array length. Runtime sealing compares both the emitted artifact count and the exact emitted suffix sequence against the canonical list. Count-only acceptance is forbidden.

The final three entries are:

```text
runtime_artifact.json
canonical_args.txt
canonical_run.cmd
```

The manifest binds parent runtime and manifest, parent and child pointers, Stage5 shader, three Stage6 shaders, binary identity, canonical CLI, all 33 child artifacts, all group digests, Atlas digest, panel schedule, accumulator contract, and final-write contract.

## 12. PASS

```text
parent R2-R10 PASS exact
HeadwiseActive unchanged
Stage5Active exact
mask 0x1f -> 0x3f
added bits=1/1
head_dim=64
panel width=8
panel count=8
K coverage=64/64
remainder=0
logical tiles=128/128
quadrant workgroups=512/512
workgroup/subgroup=32/32
panel iterations=4096/4096
scalar FMAs total=2097152
final vec4 writes=8192/8192
final scalar writes=32768/32768
all twelve decision counters=0
bit-exact parity=true
same device and queue=true
KV writes=0
host payload movement counters=0
compact decision=1 readback, 48 bytes
Stage5 fallback=128 tiles and 32768 scalars
direct lower fallbacks=0
generations=34/35/36
Atlas groups=29/29
negative controls=720/720
child artifacts=33/33
child artifact ordered suffix list exact
manifest closure exact
parent scientific terminal preserved
```

Expected summary:

```text
[r2f-r7-r6-r5-r1-r2-r11][summary] parent_r2_r10=PASS headwise_parent=HeadwiseActive parent_stage=Stage5Active stage=Stage6Active parent_feature=tensorcube-contiguous-16x16-physical-allocation-v1 feature=tensorcube-multi-k-panel-ordered-register-accumulation-v1 mask=0x000000000000001f->0x000000000000003f added_bits=1/1 head_dim=64 panel_width=8 panel_count=8 k_coverage=64/64 remainder_k=0 logical_tiles=128/128 quadrant_workgroups=512/512 workgroup_size=32 subgroup_size=32 subgroups_per_workgroup=1 panel_iterations=4096/4096 scalar_fmas_per_lane_per_panel=16 scalar_fmas_per_lane=128 scalar_fmas_per_tile=16384 scalar_fmas_total=2097152 compute_shuffles_per_lane=192 final_pack_shuffles_per_lane=8 total_shuffles_per_lane=200 final_vec4_writes=8192/8192 final_scalar_writes=32768/32768 output_mismatch=0 non_finite=0 panel_order_mismatch=0 panel_skip=0 panel_duplicate=0 k_coverage_mismatch=0 accumulator_initialization_mismatch=0 accumulator_persistence_mismatch=0 intermediate_output_write=0 final_write_count_mismatch=0 quadrant_topology_mismatch=0 lane_packing_mismatch=0 bit_exact_parity=true same_device=true same_queue_lineage=true kv_writes=0 kv_bit_exact=true stage5_fallback_tiles=128/128 stage5_fallback_scalars=32768/32768 direct_stage4_fallbacks=0 direct_stage3_fallbacks=0 direct_stage2_fallbacks=0 direct_stage1_fallbacks=0 direct_headwise_fallbacks=0 host_materializations=0 host_uploads=0 payload_readbacks=0 payload_buffer_maps=0 compact_decision_readbacks=1 compact_decision_bytes=48 cross_device_copies=0 generations=34/35/36 atlas_groups=29/29 new_negative=720/720 child_artifacts=33/33 pass=true
```

Success token:

```text
PROMOTE_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_R1_R2_R11_TENSORCUBE_STAGE6_MULTI_K_PANEL_ORDERED_REGISTER_ACCUMULATION_STAGE5_PARENT_SUBGROUP32_QUADRANT_WORKER_PANEL_LOCAL_FMA_GROUPING_FINAL_WRITE_ONCE_STAGE5_DERIVED_GPU_ORACLE_PARITY_EXACT_STAGE5_FALLBACK_AND_GENERATION_34_35_36_SEALED
```

## 13. HOLD

Any parent, feature, K geometry, panel order, arithmetic grouping, accumulator lifetime, subgroup topology, quadrant ownership, lane packing, final-write count, oracle parity, non-finite, device, queue, KV, payload movement, fallback, pointer, generation, Atlas, CLI, child-artifact count, child-artifact ordered suffix list, manifest, binary, shader, or negative-control mismatch is terminal HOLD.

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_R1_R2_R11_STAGE6_PARENT_PANEL_ORDER_ACCUMULATOR_WRITE_ONCE_PARITY_FALLBACK_OR_GENERATION_NOT_PROVEN
```
