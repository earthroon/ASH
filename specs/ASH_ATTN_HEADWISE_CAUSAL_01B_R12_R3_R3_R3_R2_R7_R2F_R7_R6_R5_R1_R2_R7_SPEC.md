# ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5-R1-R2-R7

## TensorCube Stage 2 Workgroup Microtile Activation / Stage1 Parent Binding / Single-Feature Mask Accumulation / Shared-Memory Ownership / Same-Device Output·KV Parity / Exact Stage1 Fallback / Generation 26→27→28 Seal

## 0. State

```text
PARENT=ASH-ATTN-HEADWISE-CAUSAL-01B-R12-R3-R3-R3-R2-R7-R2F-R7-R6-R5-R1-R2-R6
PARENT_VERDICT=PASS
PARENT_ATTENTION_ROUTE_STATE=HeadwiseActive
PARENT_TENSORCUBE_STAGE_STATE=Stage1Active
PARENT_TENSORCUBE_FEATURE_MASK=0x0000000000000001
PARENT_TERMINAL_GENERATION=26
RUN_SCOPE=headwise-active-tensorcube-stage2-workgroup-microtile-single-feature-activation-v1
DEFAULT_VERDICT=HOLD
ATTENTION_ROUTE_ID=gqa4-cluster-production-canary-v1
ATTENTION_ROUTE_STATE=HeadwiseActive
TENSORCUBE_PARENT_STAGE_ID=tensorcube-stage-1-physical8x8-vec4-output-v1
TENSORCUBE_STAGE_ID=tensorcube-stage-2-physical8x8-workgroup-output-v1
TENSORCUBE_STAGE2_FEATURE_ID=tensorcube-physical-8x8-workgroup-microtile-output-v1
TENSORCUBE_PARENT_FEATURE_MASK=0x0000000000000001
TENSORCUBE_STAGE2_FEATURE_BIT=1
TENSORCUBE_STAGE2_FEATURE_MASK=0x0000000000000003
TENSORCUBE_STAGE2_KERNEL_KIND=WorkgroupTileReference
TENSORCUBE_SHADER_PATH=crates/burn_webgpu_backend/src/shaders/tensorcube_atlas_microtile_8x8_parity_workgroup.wgsl
TENSORCUBE_SHADER_ENTRYPOINT=main
FEATURE_TRANSITION_POLICY=inherit-stage1-plus-exactly-one-disabled-to-enabled-bit-v1
STAGE_ACTIVATION_POLICY=stage2-supported-scope-explicit-commit-v1
SHARED_MEMORY_POLICY=load-barrier-compute-barrier-pack-single-writer-v1
BARRIER_POLICY=uniform-two-phase-workgroup-barrier-v1
SAME_DEVICE_POLICY=stage1-stage2-buffer-queue-single-device-v1
OUTPUT_PARITY_POLICY=stage2-vs-stage1-f32-abs-rel-1e-4-zero-nonfinite-v1
KV_PARITY_POLICY=no-stage2-kv-write-bit-exact-unchanged-v1
FALLBACK_POLICY=stage2-to-stage1-exact-before-publication-v1
GENERATION_POLICY=parent26-stage-open27-stage-commit28-v1
PAYLOAD_POLICY=zero-host-materialization-zero-host-upload-zero-payload-readback-bounded-compact-decision-v1
ARTIFACT_LAYOUT=atlas-parallel-group-map-v1
RUNTIME_ROOT_POLICY=typed-streaming-deterministic-root-v1
```

R2-R7 activates exactly one additional TensorCube feature beneath the sealed `HeadwiseActive + Stage1Active` lineage. Stage 1 feature bit 0 remains enabled. Stage 2 adds only feature bit 1 for the physical 8×8 workgroup-memory microtile output path.

## 1. Parent authority

The direct parent must be a sealed R2-R6 artifact and manifest with:

```text
pass=true
verdict exact
headwise_route_state=HeadwiseActive
tensorcube_stage_state=Stage1Active
feature_id=tensorcube-physical-8x8-vec4-microtile-output-v1
feature_mask_after=0x0000000000000001
tensorcube_compute_dispatches=128
output_mismatch_count=0
non_finite_count=0
tensorcube_kv_writes=0
compact_decision_readbacks=1
generations=24/25/26
atlas_group_count=18
negative_control_passed=480
```

R2-R7 binds the parent runtime artifact, local manifest, Stage 1 pointer and Atlas digest by SHA-256. Parent runtime and manifest bytes must remain unchanged before and after R2-R7.

Parent reuse policy:

```text
all R2-R6 files absent -> explicit R2-R6 bootstrap may run once
complete and exact parent set -> reuse without rebuild or recommit
partial parent set -> fail closed
complete but digest or terminal mismatch -> fail closed
```

## 2. State ownership

```text
AttentionRouteState owner=R2-R5 value=HeadwiseActive mutable_by_R2_R7=false
TensorCubeStageState owner=R2-R7 Stage1Active -> Stage2Prepared -> Stage2Active|Stage2Fallback|Quarantined
TensorCubeFeatureMaskState owner=R2-R7 0x1 -> 0x3
SharedMemoryOwnershipState owner=R2-R7 workgroup-local only
KVOwnershipState owner=inherited runtime registry, Stage2 KV writes forbidden
StagePointerState owner=TensorCube stage registry, Stage1 -> Stage2 CAS
ScientificEvidenceState owner=R1-R2, mutable_by_R2_R7=false
```

No state domain may substitute for another. Stage 2 activation does not rewrite the parent scientific PASS or HOLD result and does not replace the top-level HeadwiseActive route.

## 3. Single-feature transition

The only legal mask transition is:

```text
0x0000000000000001
-> 0x0000000000000003
```

Required:

```text
new feature bit index=1
popcount(parent XOR child)=1
parent bit 0 retained
all bits >=2 remain zero
no second feature Prepared or Enabled
```

## 4. Workgroup microtile contract

```text
physical tile=8x8 f32
packing=vec4-f32
workgroup size=64
load owners=16
compute owners=64
pack owners=16
barrier count=2
shared A=64 f32=256 bytes
shared B=64 f32=256 bytes
shared C=64 f32=256 bytes
shared total=768 bytes
output vec4 slots=16
output scalars=64
```

Execution phases:

```text
1. local_id 0..15 load A/B vec4 slots into disjoint shared cells
2. every invocation crosses barrier 1
3. local_id 0..63 owns one C scalar and performs the 8-term f32 FMA accumulation
4. every invocation crosses barrier 2
5. local_id 0..15 owns one output vec4 and writes the provisional Stage 2 output
```

Forbidden:

```text
early return before either barrier
non-uniform barrier branch
shared-cell multiple writer
output vec4 multiple writer
atomic accumulation
subgroup operation
logical 16x16 path
K-panel streaming
macro-tile path
TensorCube KV write
Stage 1 committed output overwrite before parity
```

## 5. Same-device execution

Stage 2 must reuse the already selected runtime device and queue handles. Creating a new instance, adapter, device, queue or runtime registry is forbidden.

Required identity closure:

```text
parent physical device digest == Stage 2 physical device digest
adapter identity exact
backend identity exact
required feature bitwords exact
subgroup observation exact
same queue lineage=true
cross-device copies=0
```

## 6. Stage 2 versus Stage 1 parity

For each attempt, the same command stream executes:

```text
sealed Stage 1 Vec4 reference dispatch
Stage 2 workgroup dispatch
GPU-side Stage2-vs-Stage1 compare dispatch
```

Runtime matrix:

```text
attempts=128
Stage 1 reference dispatches=128
Stage 2 dispatches=128
workgroups=128
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
payload readbacks=0
payload buffer maps=0
host materializations=0
host uploads=0
cross-device copies=0
compact decision readbacks=1
compact decision bytes=8
```

The compact decision token may contain only mismatch and non-finite counters. Tensor payload is never host-visible.

## 7. KV parity

Stage 2 receives no KV write lease.

```text
KV writes=0
KV bytes changed=0
page-table mutations=0
residency mutations=0
allocation generation before=26
allocation generation after=26
KV bit-exact unchanged=true
```

## 8. Exact fallback

The direct R2-R7 fallback is:

```text
Stage2 -> Stage1
```

The inherited chain remains:

```text
Stage2 -> Stage1 -> HeadwiseActive -> ReferenceActive
```

While Stage 1 is healthy, direct Stage2-to-Headwise or Stage2-to-Reference fallback is forbidden. Stage 2 provisional output must remain invisible until parity and pointer commit succeed.

R2-R7 proves 128 Stage 1 fallback/reference dispatches on the same device. Any failure after pointer replacement restores the original Stage 1 pointer bytes through the rollback guard.

## 9. Stage pointer CAS

The existing Stage 1 pointer is the compare value. Required precondition:

```text
schema=ash.attn.tensorcube.stage-pointer.v1
lineage_patch_id=R2-R6
active_stage_id=Stage1 ID
feature_mask_after=0x1
generation_after=26
write_count=1
pointer SHA == R2-R6 manifest stage_pointer_sha256
```

Successful replacement publishes:

```text
schema=ash.attn.tensorcube.stage-pointer.v2
lineage_patch_id=R2-R7
parent_stage_id=Stage1 ID
active_stage_id=Stage2 ID
feature_mask_before=0x1
feature_mask_after=0x3
generation_before=26
prepared_generation=27
generation_after=28
write_count=1
parent runtime SHA exact
parent pointer SHA exact
receipt digest exact
```

Blind overwrite, multiple writes and mismatched compare state are terminal HOLD.

## 10. Generation seal

```text
parent terminal=26
Stage2Prepared=27
Stage2Active=28
```

Generation reuse, decrement, skip or provisional-generation publication is forbidden.

## 11. Atlas authority groups

Exactly 18 groups are required:

```text
identity
parent_binding
parent_stage1
parent_feature_mask
sealed_parent_reuse
stage2_feature
feature_transition
workgroup_topology
shared_memory
barrier_discipline
same_device_queue
output_ownership
output_parity
kv_parity
compact_decision
stage1_fallback
generation_pointer
verdict
```

Each group carries a canonical payload, payload SHA-256 and group digest. Runtime root serialization is typed and streaming; a full root `serde_json::Value` tree is forbidden.

## 12. Required artifacts

```text
*_parent_binding.json
*_sealed_parent_reuse.json
*_workgroup_topology.json
*_device_receipt.json
*_feature_transition.json
*_stage_transition.json
*_tensorcube_stage2_dispatch.json
*_output_parity.json
*_kv_parity.json
*_stage1_fallback.json
*_zero_copy_receipt.json
*_generation_receipt.json
*_stage_pointer_receipt.json
*_negative_control_outcomes.json
*_static_checks.json
*_runtime_artifact.json
*_canonical_args.txt
*_canonical_run.cmd
*_local_manifest.json
```

The manifest closes every child artifact, both parent artifacts, the parent pointer digest, new Stage 2 pointer digest, Atlas digest, CLI identity and binary identity.

## 13. CLI contract

R2-R7 extends the strict response-file registry with exactly 53 keys covering:

```text
R2-R6 parent artifact and manifest
shared stage-pointer path
workgroup shader path and entrypoint
Stage 1 and Stage 2 IDs
feature IDs, bit and masks
workgroup size, shared bytes and barrier count
feature, shared-memory, barrier, same-device, parity, fallback, generation and payload policies
128 dispatch count
1e-4 absolute and relative tolerances
520 negative controls
zero mismatch and non-finite budgets
all required and forbidden boolean gates
```

Unknown, duplicate, missing, wrong-value and wrong-polarity keys are terminal HOLD.

## 14. Negative controls

R2-R7 adds exactly 52 groups × 10 controls = 520 controls. Required families include parent mutation, partial parent state, feature-bit errors, shader identity drift, workgroup-size errors, shared-memory extent errors, missing or non-uniform barriers, writer collisions, uninitialized reads, output publication errors, new device or queue injection, payload movement, compact-decision violations, numerical mismatch, KV mutation, fallback skip, pointer overwrite, generation drift and third-feature preparation.

Every control must reject the intended mutation and preserve deterministic Stage 1 state.

## 15. PASS

PASS requires:

```text
parent R2-R6 PASS exact
sealed parent reused without recommit
HeadwiseActive unchanged
Stage1Active parent exact
feature mask 0x1 -> 0x3
added bits=1/1
workgroup shader identity exact
workgroup size=64
shared memory=768 bytes
barriers=2
load/compute/pack owners=16/64/16
shared and output ownership single-writer exact
Stage 2 dispatches/workgroups/tiles=128/128
output scalars=8192/8192
output mismatch=0
non-finite=0
KV writes=0
KV bit-exact=true
same device=true
same queue lineage=true
payload movement counters=0
compact decision=1 readback, 8 bytes
Stage 1 fallback dispatches=128/128
direct Headwise and Reference fallbacks=0
stage pointer writes=1/1
generations=26/27/28
Atlas groups=18/18
negative controls=520/520
manifest closure exact
```

## 16. HOLD

HOLD occurs on any parent, identity, feature-mask, shader, workgroup topology, shared-memory ownership, barrier, same-device, parity, KV, fallback, pointer, generation, Atlas, manifest or negative-control mismatch. No automatic repair, silent downgrade, hidden retry, feature-mask rewrite or parent regeneration is allowed.

## 17. Verdicts

Success:

```text
PROMOTE_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_R1_R2_R7_TENSORCUBE_STAGE2_WORKGROUP_MICROTILE_ACTIVATION_STAGE1_PARENT_SINGLE_FEATURE_ACCUMULATION_SHARED_MEMORY_OWNERSHIP_SAME_DEVICE_OUTPUT_KV_PARITY_EXACT_STAGE1_FALLBACK_AND_GENERATION_26_27_28_SEALED
```

Default HOLD:

```text
HOLD_ASH_ATTN_HEADWISE_CAUSAL_01B_R12_R3_R3_R3_R2_R7_R2F_R7_R6_R5_R1_R2_R7_STAGE2_PARENT_FEATURE_SHARED_MEMORY_BARRIER_PARITY_FALLBACK_OR_GENERATION_NOT_PROVEN
```

Expected summary:

```text
[r2f-r7-r6-r5-r1-r2-r7][summary]
parent_r2_r6=PASS
headwise_parent=HeadwiseActive
parent_stage=Stage1Active
stage=Stage2Active
parent_feature=tensorcube-physical-8x8-vec4-microtile-output-v1
feature=tensorcube-physical-8x8-workgroup-microtile-output-v1
mask=0x0000000000000001->0x0000000000000003
added_bits=1/1
same_device=true
same_queue_lineage=true
workgroup_size=64
shared_memory_bytes=768
barriers=2
load_owners=16
compute_owners=64
pack_owners=16
tensorcube_dispatches=128/128
workgroups=128/128
output_tiles=128/128
output_scalars=8192/8192
output_mismatch=0
non_finite=0
kv_writes=0
kv_bit_exact=true
stage1_fallback_dispatches=128/128
direct_headwise_fallbacks=0
host_materializations=0
host_uploads=0
payload_readbacks=0
payload_buffer_maps=0
compact_decision_readbacks=1
compact_decision_bytes=8
cross_device_copies=0
generations=26/27/28
atlas_groups=18/18
new_negative=520/520
pass=true
```
