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
DEFAULT_VERDICT=HOLD
```

R2-R8 activates exactly one new TensorCube feature beneath sealed Stage 2. Bits 0 and 1 remain inherited. Bit 2 enables a real 8×8 f32 subgroup32 register-shuffle numerical path. The top-level attention route remains `HeadwiseActive`.

The existing experimental seam:

```text
crates/burn_webgpu_backend/src/shaders/tensorcube_atlas_microtile_8x8_subgroup_exp.wgsl
```

is probe-only and may never be counted as Stage 3 numerical execution. The authoritative Stage 3 shader is:

```text
crates/burn_webgpu_backend/src/shaders/tensorcube_atlas_microtile_8x8_parity_subgroup32.wgsl
entrypoint=main
```

## 1. PASS claim boundary

R2-R8 PASS proves only:

```text
sealed R2-R7 parent reused without rebuild or recommit
feature mask 0x3 -> 0x7 with one added bit
exact subgroup size 32
one subgroup per workgroup
32/32 lane coverage
same physical device and queue lineage as Stage 2
Stage3 output parity against sealed Stage2 workgroup output
KV unchanged and unwritten
exact Stage3 -> Stage2 fallback
zero tensor payload movement
atomic Stage2 -> Stage3 pointer transition
generation 28 -> 29 -> 30
```

R2-R8 PASS does not claim subgroup portability, performance superiority, logical 16×16 support, K-panel streaming, macro-tiles, TensorCube KV mutation, or production rollout.

## 2. Parent binding and reuse

Required R2-R7 facts:

```text
pass=true
verdict exact
headwise_route_state=HeadwiseActive
tensorcube_stage_state=Stage2Active
feature_mask_after=0x0000000000000003
tensorcube_compute_dispatches=128
output_mismatch_count=0
non_finite_count=0
tensorcube_kv_writes=0
generations=26/27/28
atlas_group_count=18
negative_control_passed=520
```

R2-R8 binds by SHA-256:

```text
R2-R7 runtime artifact
R2-R7 local manifest
R2-R7 Stage2 pointer
R2-R7 Atlas digest
Stage2 workgroup reference shader
Stage3 subgroup32 shader
subgroup topology probe shader
experimental seam shader as excluded identity
```

Reuse policy:

```text
all parent files absent -> explicit R2-R7 bootstrap may run once
complete exact parent set -> reuse without rebuild or pointer rewrite
partial parent set -> fail closed
complete but digest, verdict, stage, mask, or generation mismatch -> fail closed
```

Parent runtime and manifest bytes must remain unchanged before and after R2-R8.

## 3. State ownership

```text
AttentionRouteState owner=R2-R5 value=HeadwiseActive mutable_by_R2_R8=false
TensorCubeStageState owner=R2-R8 Stage2Active -> Stage3Prepared -> Stage3Active|Stage3Fallback|Quarantined
TensorCubeFeatureMaskState owner=R2-R8 0x3 -> 0x7
StagePointerState owner=TensorCube stage registry Stage2 -> Stage3 CAS
KVOwnershipState owner=inherited runtime registry, Stage3 KV write forbidden
ScientificEvidenceState owner=R1-R2 mutable_by_R2_R8=false
```

No state domain may substitute for another. Stage 3 activation never rewrites the parent scientific PASS or HOLD terminal.

## 4. Single-feature accumulation

Only this transition is legal:

```text
0x0000000000000003
-> 0x0000000000000007
```

Required:

```text
new bit index=2
popcount(parent XOR child)=1
bits 0 and 1 retained
all bits >=3 remain zero
no fourth feature Prepared or Enabled
```

Any clearing, aliasing, replacement, multi-bit addition, or environment-driven enablement is terminal HOLD.

## 5. Subgroup topology

```text
workgroup_size=32
required_subgroup_size=32
subgroups_per_workgroup=1
subgroup_id=0
lane_range=0..31
lane_mask=0xffffffff
lane_coverage=32/32
```

The numerical shader may run only after the topology probe on the same device and queue reports exact size 32 and one subgroup. Sizes 4, 8, 16, 64, multiple subgroups, partial subgroups, or inferred topology select exact Stage 2 fallback before Stage 3 dispatch.

Forbidden:

```text
new instance, adapter, device, queue, or runtime registry
64-lane workgroup with two subgroups
subgroup_id > 0
silent lane remapping
workgroup-memory emulation counted as Stage3
experimental seam counted as numerical dispatch
```

## 6. Lane and output ownership

For lane `L` in `0..31`:

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

Therefore:

```text
32 lanes × 2 scalars = 64 scalars
rows 0..7 covered
columns 0..7 covered
no duplicate coordinate
no missing coordinate
```

Packing ownership:

```text
pack owners=16
one vec4 slot per pack owner
four source scalars per vec4
16 vec4 writes × 4 components = 64 scalars
single writer per vec4 slot
```

Duplicate, missing, overlapping, or out-of-range ownership is terminal HOLD.

## 7. Register exchange and arithmetic order

For each `k=0..7`, lanes `0..7` seed the input values:

```text
a_seed=A[lane][k] when lane<8, otherwise 0
b_seed=B[k][lane] when lane<8, otherwise 0
```

Every lane executes the same ordered direct-index shuffle schedule:

```text
a_low=subgroupShuffle(a_seed,row_low)
a_high=subgroupShuffle(a_seed,row_high)
b_value=subgroupShuffle(b_seed,column)
```

Then:

```text
acc_low=fma(a_low,b_value,acc_low)
acc_high=fma(a_high,b_value,acc_high)
```

Contract:

```text
K steps=8
compute shuffles/lane=24
packing shuffles/lane=4
total shuffles/lane=28
FMA/lane=16
workgroup shared bytes=0
workgroup barriers=0
atomic operations=0
```

Shuffle operations under divergent control flow, arithmetic reassociation outside the declared policy, hidden shared memory, barriers, or atomics are terminal HOLD.

## 8. Same-device execution

Stage 3 reuses the R2-R7 runtime handles. Required equalities:

```text
physical device digest
adapter and backend identity
required feature bitwords
runtime registry identity
queue lineage identity
buffer allocation generation
Q/K/V/KV/output device ownership
```

Required counters:

```text
new adapters=0
new devices=0
new queues=0
cross-device copies=0
```

## 9. Numerical parity

Each supported attempt executes on one command lineage:

```text
sealed Stage2 workgroup reference dispatch
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

A scalar passes when:

```text
abs_error <= 1.0e-4
or
rel_error <= 1.0e-4
```

Required terminal counters:

```text
output mismatch=0
non-finite=0
topology mismatch=0
lane/packing ownership mismatch=0
```

Stage 2 is the direct numerical authority. Headwise and Stage 1 are inherited lower fallback authorities, not the direct Stage 3 comparison target.

## 10. KV and payload boundary

Stage 3 receives no KV write lease:

```text
KV writes=0
KV bytes changed=0
page-table mutations=0
residency mutations=0
allocation generation unchanged
KV bit-exact=true
```

Payload contract:

```text
host materializations=0
host uploads=0
payload readbacks=0
payload buffer maps=0
cross-device copies=0
compact decision readbacks=1
compact decision bytes=16
```

The 16-byte decision token may contain only:

```text
output mismatch count
non-finite count
topology mismatch count
lane/packing ownership mismatch count
```

Tensor values, sampled payloads, hashes derived from payload bytes, or debug tensor slices are forbidden in host-visible receipts.

## 11. Exact fallback

Direct R2-R8 fallback:

```text
Stage3 -> Stage2
```

Inherited chain:

```text
Stage3 -> Stage2 -> Stage1 -> HeadwiseActive -> ReferenceActive
```

While Stage 2 is healthy, Stage 3 may not skip directly to Stage 1, HeadwiseActive, or ReferenceActive. Fallback must occur before Stage 3 output publication and with the same input, decode step, device, queue lineage, KV state, layout, and generation.

Required fallback drill:

```text
Stage2 fallback dispatches=128/128
direct Stage1 fallbacks=0
direct Headwise fallbacks=0
direct Reference fallbacks=0
```

## 12. Stage pointer CAS and rollback

Required Stage 2 compare value:

```text
schema=ash.attn.tensorcube.stage-pointer.v2
lineage_patch_id=R2-R7
active_stage_id=tensorcube-stage-2-physical8x8-workgroup-output-v1
feature_mask_after=0x3
generation_after=28
pointer SHA == R2-R7 manifest stage_pointer_sha256
```

Stage 3 publication:

```text
schema=ash.attn.tensorcube.stage-pointer.v3
lineage_patch_id=R2-R8
parent_stage_id=Stage2 ID
active_stage_id=Stage3 ID
feature_mask_before=0x3
feature_mask_after=0x7
generation_before=28
prepared_generation=29
generation_after=30
write_count=1
parent runtime SHA exact
parent pointer SHA exact
receipt digest exact
```

If the shared pointer already contains a valid R2-R8 Stage 3 record, idempotent validation must recover the R2-R7 pointer identity through `parent_pointer_sha256`. Any failure after replacement restores the original Stage 2 pointer bytes. Blind overwrite, multiple successful writes, stale compare state, or ambiguous rollback is terminal HOLD.

## 13. Generation seal

```text
parent terminal=28
Stage3Prepared=29
Stage3Active=30
```

Generation reuse, decrement, skip, publication at 29, or silent buffer-generation mutation is forbidden.

## 14. Atlas and serialization

The typed streaming runtime root contains exactly 20 authority groups:

```text
identity
parent_binding
parent_stage2
parent_feature_mask
sealed_parent_reuse
stage3_feature
feature_transition
subgroup_capability
subgroup_topology
lane_mapping
register_exchange
packing_ownership
same_device_queue
output_parity
kv_parity
compact_decision
stage2_fallback
generation_pointer
negative_controls
verdict
```

Each group contains canonical payload JSON, SHA-256, group digest, and a non-authoritative fields projection. Constructing a complete root `serde_json::Value` tree is forbidden.

## 15. Required artifacts

```text
*_parent_binding.json
*_sealed_parent_reuse.json
*_stage2_parent_identity.json
*_subgroup_capability.json
*_subgroup_topology.json
*_lane_mapping.json
*_register_exchange.json
*_packing_ownership.json
*_feature_transition.json
*_stage_transition.json
*_tensorcube_stage3_dispatch.json
*_output_parity.json
*_kv_parity.json
*_stage2_fallback.json
*_zero_copy_receipt.json
*_compact_decision.json
*_generation_receipt.json
*_stage_pointer_receipt.json
*_negative_control_outcomes.json
*_static_checks.json
*_runtime_artifact.json
*_canonical_args.txt
*_canonical_run.cmd
*_local_manifest.json
```

The local manifest closes all 23 child artifacts before the manifest itself, both parent artifacts, parent and child pointer digests, shader identities, CLI identity, binary identity, all Atlas group digests, and the R2-R8 Atlas digest.

## 16. CLI contract

The strict R2-R8 response-file registry adds exactly 77 keys. They cover parent paths, shared pointer, Stage 2 reference shader, Stage 3 shader, topology probe, excluded experimental seam, IDs, masks, subgroup topology, lane mapping, shuffle/FMA counts, dispatch count, tolerances, policies, budgets, negative-control count, and all required/forbidden boolean gates.

Required static closure:

```text
registry extension keys=77
response-file extension keys=77
missing keys=0
extra keys=0
duplicate keys=0
unknown or wrong-polarity keys fail closed
```

## 17. Negative controls

R2-R8 adds exactly 56 groups × 10 controls:

```text
new negative controls=560
```

Families include parent mutation, partial parent state, mask corruption, fourth-feature activation, experimental-shader promotion, shader identity drift, wrong topology, missing/duplicate lanes, lane-map corruption, shuffle-source corruption, divergent shuffle, K-loop/order mutation, FMA policy drift, ownership collisions, hidden shared memory/barriers/atomics, new-device or queue injection, payload movement, oversized decision token, parity corruption, KV mutation, fallback skip, pointer overwrite, generation drift, Atlas mutation, manifest omission, and binary identity drift.

Every control must reject for the intended reason and preserve deterministic Stage 2 state.

## 18. PASS

PASS requires:

```text
parent R2-R7 PASS exact
sealed parent reused without recommit
HeadwiseActive unchanged
Stage2Active exact
mask 0x3 -> 0x7
added bits=1/1
real subgroup32 shader exact
experimental seam excluded
workgroup/subgroup=32/32
subgroups per workgroup=1
lane coverage=32/32
lane mask=0xffffffff
outputs per lane=2
pack owners=16
compute/pack/total shuffles=24/4/28
FMA/lane=16
shared bytes=0
barriers=0
same device and queue=true
Stage2/Stage3 dispatches=128/128
subgroups=128/128
output tiles=128/128
output scalars=8192/8192
all mismatch and non-finite counters=0
KV writes=0
KV bit-exact=true
Stage2 fallback dispatches=128/128
direct lower fallbacks=0
all payload movement counters=0
compact decision=1 readback, 16 bytes
stage pointer writes=1/1
generations=28/29/30
Atlas groups=20/20
negative controls=560/560
manifest closure exact
parent scientific terminal preserved
```

## 19. HOLD

Any parent, identity, mask, shader, topology, lane mapping, shuffle schedule, packing ownership, same-device, parity, KV, payload, fallback, pointer, generation, Atlas, manifest, CLI, binary, or negative-control mismatch is terminal HOLD. No automatic topology repair, subgroup remapping, hidden workgroup fallback counted as success, parent regeneration, feature-mask repair, or silent route downgrade is allowed.

## 20. Verdicts

Success:

```text
PROMOTE_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_R1_R2_R8_TENSORCUBE_STAGE3_SUBGROUP32_FASTPATH_ACTIVATION_STAGE2_PARENT_SINGLE_FEATURE_ACCUMULATION_EXACT_LANE_MAPPING_WORKGROUP_REFERENCE_PARITY_EXACT_STAGE2_FALLBACK_AND_GENERATION_28_29_30_SEALED
```

Default HOLD:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_R1_R2_R8_STAGE3_PARENT_FEATURE_SUBGROUP_TOPOLOGY_LANE_MAPPING_PARITY_FALLBACK_OR_GENERATION_NOT_PROVEN
```

Expected summary:

```text
[r2f-r7-r6-r5-r1-r2-r8][summary]
parent_r2_r7=PASS
headwise_parent=HeadwiseActive
parent_stage=Stage2Active
stage=Stage3Active
parent_feature=tensorcube-physical-8x8-workgroup-microtile-output-v1
feature=tensorcube-physical-8x8-subgroup32-register-shuffle-output-v1
mask=0x0000000000000003->0x0000000000000007
added_bits=1/1
same_device=true
same_queue_lineage=true
workgroup_size=32
subgroup_size=32
subgroups_per_workgroup=1
lane_coverage=32/32
lane_mask=0xffffffff
outputs_per_lane=2
pack_owners=16
compute_shuffles_per_lane=24
pack_shuffles_per_lane=4
total_shuffles_per_lane=28
fma_per_lane=16
tensorcube_dispatches=128/128
subgroups=128/128
output_tiles=128/128
output_scalars=8192/8192
output_mismatch=0
non_finite=0
topology_mismatch=0
lane_packing_mismatch=0
kv_writes=0
kv_bit_exact=true
stage2_fallback_dispatches=128/128
direct_stage1_fallbacks=0
direct_headwise_fallbacks=0
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

## 21. Final seal

```text
sealed R2-R7 Stage2Active parent
+ inherited feature bits 0 and 1
+ one new feature bit 2
+ real exact32 subgroup numerical shader
+ deterministic two-output-per-lane mapping
+ uniform register shuffle schedule
+ fixed eight-step f32 accumulation
+ sixteen-owner vec4 packing
+ Stage3-vs-Stage2 GPU parity
+ unchanged KV
+ zero tensor payload movement
+ bounded compact decision
+ exact Stage3-to-Stage2 fallback
+ atomic pointer CAS and rollback
+ generation 28->29->30
= TensorCube Stage 3 subgroup32 fast path sealed without weakening Stage 2 authority, state ownership, fallback order, or evidence integrity
```
