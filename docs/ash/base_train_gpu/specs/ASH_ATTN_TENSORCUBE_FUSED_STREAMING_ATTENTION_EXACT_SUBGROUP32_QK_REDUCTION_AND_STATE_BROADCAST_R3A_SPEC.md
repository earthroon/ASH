# ASH-ATTN-TENSORCUBE-FUSED-STREAMING-ATTENTION-EXACT-SUBGROUP32-QK-REDUCTION-AND-STATE-BROADCAST-R3A

## Status

```text
Patch ID:
ASH-ATTN-TENSORCUBE-FUSED-STREAMING-ATTENTION-EXACT-SUBGROUP32-QK-REDUCTION-AND-STATE-BROADCAST-R3A

Parent precision authority:
ASH-ATTN-TENSORCUBE-FUSED-STREAMING-ATTENTION-FP16-BF16-QKV-STORAGE-FP32-STATE-ACCUMULATION-R3

Optimization scope:
WG32 exact-subgroup32 candidate path

QK reduction:
FP32 subgroupAdd

State owner:
subgroupElect

State broadcast:
subgroupBroadcastFirst

WG32 exact subgroup QK-tree partial-dot scratch:
0 B

WG32 exact subgroup token-loop QK workgroup barriers:
0

F32 / FP16 / BF16 precision profiles:
preserved
```

## Parent SSOT

```text
ASH-ATTN-TENSORCUBE-FUSED-STREAMING-ATTENTION-FP16-BF16-QKV-STORAGE-FP32-STATE-ACCUMULATION-R3
ASH-ATTN-TENSORCUBE-FUSED-STREAMING-ATTENTION-SUBGROUP-MATRIX-TILE-AND-ADAPTIVE-WORKGROUP-R2
ASH-ATTN-TENSORCUBE-STAGE10-11-12-FUSED-STREAMING-ATTENTION-NO-PROBABILITY-MATERIALIZATION-R1
```

R3A changes the WG32 subgroup physical reduction and state-broadcast mechanism. It does not change the fused-attention equations, precision profile semantics, final context tolerance, independent oracle, or WG64/WG128 shader bodies.

## Correctness prerequisite discovered during R3A

The R3 parent WG32 shaders had a concrete Q-cache initialization defect.

The physical workgroup size was 32 and each lane wrote only:

```text
q_cache[lane]
```

while QK used both:

```text
q_cache[lane]
q_cache[lane + 32]
```

Therefore Q-cache elements 32..63 were not initialized by the WG32 workgroup before the dot product.

R3A repairs both WG32 baselines and both WG32 exact-subgroup candidates so every lane loads two Q values:

```text
q_cache[lane]
q_cache[lane + 32]
```

This is an explicit prerequisite correctness repair. It is not hidden as part of the performance claim.

Affected WG32 source families:

```text
R2 F32 WorkgroupOnly
R2 F32 SubgroupAssisted
R3 packed-half WorkgroupOnly
R3 packed-half SubgroupAssisted
```

## No workgroup32 = subgroup32 assumption

R3A does not infer subgroup size from `@workgroup_size(32,1,1)`.

ASH already performs a physical subgroup probe during existing-device bootstrap. R3A threads the already-observed result through:

```text
existing_device_bootstrap
    -> burn-wgpu-local runtime handle registry
    -> NativeWgpuRuntimeHandles
    -> W7
    -> Stage12
    -> R2/R3 candidate pipeline construction
```

New runtime-handle field:

```text
subgroup_probe_observed_size: u32
```

Exact subgroup admission revision:

```text
FUSED_ATTN_EXACT_SUBGROUP32_ADMISSION_R1
```

Subgroup candidate pipelines are built/admitted only when:

```text
SUBGROUP feature available
AND
subgroup_probe_observed_size == 32
```

WG32 exact-subgroup receipt additionally requires:

```text
selected workgroup == WG32
selected reduction path == SubgroupAssisted
exact subgroup32 admitted
single-subgroup workgroup == true
```

If exact subgroup32 is not established, the selector chooses the WorkgroupOnly path before replay dispatch. A failed subgroup dispatch does not retry with another reduction path inside the active replay.

## WG32 baseline preservation

The WorkgroupOnly WG32 path remains the physical A/B baseline.

Its legacy QK reduction retains:

```text
partial_dot[32] = 128 B
stride 16 -> 8 -> 4 -> 2 -> 1 tree reduction
6 logical QK workgroup-barrier invocation points per KV token
```

The baseline receives only the Q-cache correctness repair described above.

## ExactSubgroup32 QK reduction

R3A QK reduction revision:

```text
EXACT_SUBGROUP32_QK_SUBGROUP_ADD_R1
```

For head dimension 64 and WG32, each subgroup invocation owns two Q/K components:

```text
partial = q[d] * k[d] + q[d + 32] * k[d + 32]
total   = subgroupAdd(partial)
```

The exact subgroup shader contains no `partial_dot` workgroup array and no stride reduction loop.

Structural retirement receipt:

```text
legacy partial-dot scratch = 128 B
active partial-dot scratch = 0 B
partial-dot scratch retired = 128 B

legacy QK barriers/token = 6
exact subgroup QK barriers/token = 0
```

These are logical/source-structure receipts. They are not claims about measured GPU stall cycles or occupancy.

## Barrier boundary

R3A does **not** claim that the complete WG32 subgroup shader contains zero barriers.

The exact subgroup shader retains:

```text
1 workgroupBarrier after cooperative Q-cache population
1 storageBarrier before final state/write-count commit
```

The optimized contract is specifically:

```text
token-loop QK-tree workgroup barriers = 0
```

There is no `workgroupBarrier()` after the token loop begins.

## State transition ownership

State broadcast revision:

```text
SUBGROUP_ELECT_BROADCAST_FIRST_STATE_R1
```

R3A does not treat local invocation lane 0 as subgroup lane 0.

Canonical transition ownership uses:

```text
subgroupElect()
```

The elected invocation computes the online transition and broadcasts:

```text
alpha
beta
next running max
next running denominator
next running count
```

through:

```text
subgroupBroadcastFirst(...)
```

There is no indexed `subgroupBroadcast(value, 0)` dependency and no local-lane/subgroup-lane identity assumption.

## Shared alpha/beta authority

The R1/R2/R3 recurrence remains:

```text
m_new = max(m_old, m_tile)
alpha = exp(m_old  - m_new)
beta  = exp(m_tile - m_new)

l_new = l_old * alpha + l_tile * beta
A_new = A_old * alpha + A_tile * beta
```

The same elected FP32 `alpha` and `beta` values are broadcast and consumed by both denominator evolution and weighted-V numerator evolution.

No separate Stage11/Stage12 scale authority is introduced.

## Collective participation

The QK `subgroupAdd(local_dot)` is outside the token-admission branch.

Causally inadmissible tokens contribute:

```text
local_dot = 0
```

while all subgroup invocations still participate in the collective.

The subgroup contract, descriptor geometry, and chunk bounds are workgroup-uniform preconditions and are checked before state mutation.

## Subgroup contract failure lane

Stage12 candidate status word 7 is promoted from reserved to:

```text
candidate_subgroup_contract_failure_count
```

The exact subgroup WG32 shader reports a contract failure when the runtime shader-visible subgroup contract is not exact 32.

The existing `words[0..24] == 0` final failure gate includes word 7, so subgroup contract failure is fail-closed.

No partial successful receipt is promoted when this lane is non-zero.

## R2/R3 precision preservation

R3A preserves:

```text
F32Safe
Fp16QkvStorageF32State
Bf16QkvStorageF32State
```

Packed half candidates still decode to FP32 before QK reduction:

```text
FP16/BF16 storage
    -> explicit FP32 decode
    -> FP32 local QK partial
    -> FP32 subgroupAdd
    -> FP32 score
    -> FP32 online softmax state
    -> FP32 weighted-V numerator
    -> FP32 final context
```

No half softmax state, half numerator, or half context is introduced.

## WG64/WG128 preservation

The following R3 parent shaders are byte-identical in R3A:

```text
R2 WG64 WorkgroupOnly
R2 WG64 SubgroupAssisted
R2 WG128 WorkgroupOnly
R2 WG128 SubgroupAssisted
R3 WG64 packed-half WorkgroupOnly
R3 WG64 packed-half SubgroupAssisted
R3 WG128 packed-half WorkgroupOnly
R3 WG128 packed-half SubgroupAssisted
```

WG64/WG128 multi-subgroup restructuring is outside R3A scope.

## Independent oracle and tolerance

The F32 raw-Q/K/V Stage12 oracle is byte-identical to the R3 parent.

The final normalize/verify shader is also byte-identical.

Tolerance remains exactly:

```text
absolute tolerance = 2.0e-4
relative tolerance = 2.0e-3
relative floor = 1.0e-4
```

R3A does not widen numerical tolerance to accommodate subgroup reduction ordering.

## Replay selection seal

The first Stage12 replay descriptor selects the R2 physical variant. The resulting selection is stored in `candidate_variant_selection` and reused for later descriptors.

R3A therefore preserves:

```text
no mid-replay workgroup swap
no mid-replay reduction-path swap
no mid-replay precision swap
```

Exact subgroup32 is a pre-dispatch capability admission, not a runtime failure fallback.

## R3A receipts

Stage12/W7 surfaces include:

```text
exact_subgroup32_dispatch_count
subgroup_probe_observed_size
exact_subgroup32_admitted
logical_qk_barrier_invocation_points_avoided
partial_dot_scratch_bytes_retired
qk_subgroup_add_count
subgroup_elect_transition_count
subgroup_broadcast_first_count
candidate_subgroup_contract_failure_count
```

For an actual WG32 ExactSubgroup32 dispatch, W7 requires:

```text
subgroup_probe_observed_size = 32
exact_subgroup32_admitted = true
logical_qk_barrier_invocation_points_avoided > 0
partial_dot_scratch_bytes_retired = 128
qk_subgroup_add_count > 0
subgroup_elect_transition_count > 0
subgroup_broadcast_first_count > 0
candidate_subgroup_contract_failure_count = 0
```

## Parent zero-materialization contracts

Still required:

```text
candidate retained-score read = 0
candidate Stage11-transition read = 0
secondary candidate QK recompute = 0
full score matrix allocation = 0
full probability matrix allocation = 0
```

## Static validation

New validator:

```text
tools/validate_ash_attn_tensorcube_fused_streaming_attention_exact_subgroup32_qk_reduction_state_broadcast_r3a_static.py

215/215 PASS
```

Coverage includes:

```text
existing physical subgroup probe propagation
exact subgroup32 pipeline admission
WG32 Q-cache 64-element initialization repair
WG32 WorkgroupOnly tree baseline preservation
WG32 exact subgroup partial-dot retirement
WG32 exact subgroup token-loop QK barrier retirement
subgroupAdd FP32 QK reduction
subgroupElect state ownership
subgroupBroadcastFirst state propagation
no local-lane/subgroup-lane identity assumption
packed FP16/BF16 -> FP32 decode preservation
Stage12 replay-chain selection seal
candidate subgroup-contract failure lane
W7 exact-subgroup receipt gate
parent tolerance preservation
independent oracle preservation
WG64/WG128 parent SHA preservation
zero retained-score/transition/probability contracts
```

Parent regressions in the bake environment:

```text
Stage11 active vendor adoption                  83/83 PASS
Vendor variable-row softmax                   100/100 PASS
Vendor mixed precision                         70/70 PASS
Vendor compact readback                        64/64 PASS
Generation-sealed Muon immutable cache         66/66 PASS
Muon backend surface rebind                    35/35 PASS
FFN multi-slot                                  35/35 PASS
FFN persistent resource slab                   35/35 PASS
FFN timestamp/resource-churn guard             35/35 PASS
FFN physical-perf harness static               35/35 PASS
FFN fused production                           35/35 PASS
GPU70K G45                                     35/35 PASS
GPU70K G27                                     35/35 PASS
Atlas/HOTPATH                                  56/56 PASS
HOTPATH allocation                             56/56 PASS
```

The prior R3 validator reports:

```text
283/293 PASS
```

Its ten failures are intentionally superseded checks:

```text
9 checks expect the old WG32 packed-half subgroup source structure
1 check expects the old W7 R3 revision literal
```

R3A's 215-check validator directly revalidates the R3 precision profiles, FP32 numerical state authority, exact half decode surfaces, parent tolerance, R2 geometry/state-chain contracts, and oracle independence under the new WG32 subgroup implementation.

## Changed files

The R3A overlay contains fourteen changed files:

```text
crates/burn_webgpu_backend/src/device_handles.rs
crates/burn_webgpu_backend/src/existing_device_bootstrap.rs
crates/burn_webgpu_backend/src/lib.rs
crates/burn_webgpu_backend/src/shaders/tensorcube_fused_attention_r2_wg32_subgroup.wgsl
crates/burn_webgpu_backend/src/shaders/tensorcube_fused_attention_r2_wg32_workgroup.wgsl
crates/burn_webgpu_backend/src/shaders/tensorcube_fused_attention_r3_wg32_subgroup_packed_half.wgsl
crates/burn_webgpu_backend/src/shaders/tensorcube_fused_attention_r3_wg32_workgroup_packed_half.wgsl
crates/burn_webgpu_backend/src/tensorcube_fused_attention_r2_variants.rs
crates/burn_webgpu_backend/src/tensorcube_fused_attention_r3_precision.rs
crates/burn_webgpu_backend/src/tensorcube_fused_attention_r3a_exact_subgroup32.rs
crates/burn_webgpu_backend/src/tensorcube_stage12_weighted_value_accumulation.rs
crates/model_core/src/attention_interconnect_w7.rs
tools/validate_ash_attn_tensorcube_fused_streaming_attention_exact_subgroup32_qk_reduction_state_broadcast_r3a_static.py
vendor_fork_scaffold/burn-wgpu-local/src/runtime_handles.rs
```

Code ZIPs contain no Markdown, no `*.sha256`, and no Python cache artifacts.

## Evidence status

The bake environment contains no Cargo, rustc, rustfmt, WGSL physical compiler, or GPU execution authority.

Therefore:

```text
STATIC_BAKED_READY
NO_LOCAL_RUST_COMPILE_CLAIM
NO_LOCAL_WGSL_COMPILE_CLAIM
NO_PHYSICAL_SUBGROUP32_EXECUTION_CLAIM
NO_GPU_TIMESTAMP_CLAIM
NO_OCCUPANCY_IMPROVEMENT_CLAIM
NO_SPEEDUP_CLAIM
PHYSICAL_W7_GATE_REQUIRED
```

User-local Cargo/WGPU execution is the final physical SSOT.

## Physical promotion targets

At minimum:

```text
physical bootstrap subgroup probe observes 32
WG32 exact-subgroup F32 shader compiles/runs
WG32 exact-subgroup FP16 shader compiles/runs
WG32 exact-subgroup BF16 shader compiles/runs
candidate_subgroup_contract_failure_count = 0
candidate/oracle context gate PASS
nonfinite state/context = 0
write-order violation = 0
retained score = 0
transition tape = 0
probability matrix = 0
secondary QK recompute = 0
```

A/B performance evidence must compare the same geometry, precision, input, and attention state between:

```text
WG32 WorkgroupOnly tree reduction
vs
WG32 ExactSubgroup32 reduction
```

The receipt should include GPU timestamps plus the structural barrier/scratch counters. R3A does not set a synthetic speedup threshold.

## Non-goals

```text
No WG64 multi-subgroup rewrite
No WG128 multi-subgroup rewrite
No new workgroup geometry
No new precision profile
No half softmax state
No half weighted-V numerator
No half context
No retained score
No transition tape
No probability matrix
No runtime benchmark autotuner
No R4 promotion-table mutation
No automatic subgroup promotion
```

## Next line

After physical correctness/timestamp evidence, R3A becomes an explicit candidate for:

```text
ASH-ATTN-TENSORCUBE-FUSED-STREAMING-ATTENTION-PRECISION-AWARE-VARIANT-SELECTION-AND-PER-GEOMETRY-PROMOTION-R4
```

WG64/WG128 multi-subgroup optimization, if justified by the R3A evidence, remains a separate later line.

## Promotion seal

```text
PROMOTE_ASH_ATTN_TENSORCUBE_FUSED_STREAMING_ATTENTION_EXACT_SUBGROUP32_QK_REDUCTION_AND_STATE_BROADCAST_R3A

R3_PRECISION_AUTHORITY_PRESERVED
R2_VARIANT_AUTHORITY_PRESERVED
R1_FUSED_SEMANTIC_AUTHORITY_PRESERVED

WG32_Q_CACHE_FULL_64_ELEMENT_INITIALIZATION_REPAIRED

NO_WORKGROUP32_EQUALS_SUBGROUP32_ASSUMPTION
EXISTING_PHYSICAL_SUBGROUP_PROBE_PROPAGATED
EXACT_SUBGROUP32_PRE_DISPATCH_ADMISSION
SINGLE_SUBGROUP_WG32_IDENTITY

FP32_SUBGROUP_ADD_QK_REDUCTION
ZERO_QK_PARTIAL_DOT_SCRATCH
128_BYTE_PARTIAL_DOT_SCRATCH_RETIREMENT
ZERO_TOKEN_LOOP_QK_WORKGROUP_BARRIERS

Q_CACHE_READINESS_WORKGROUP_BARRIER_PRESERVED
FINAL_STORAGE_COMMIT_BARRIER_PRESERVED
NO_ZERO_TOTAL_BARRIER_CLAIM

SUBGROUP_ELECT_STATE_OWNER
SUBGROUP_BROADCAST_FIRST_ALPHA
SUBGROUP_BROADCAST_FIRST_BETA
SUBGROUP_BROADCAST_FIRST_RUNNING_STATE
NO_LOCAL_LANE_SUBGROUP_LANE_IDENTITY_ASSUMPTION

FP32_RUNNING_MAX
FP32_RUNNING_DENOMINATOR
FP32_SHARED_ALPHA_BETA
FP32_WEIGHTED_V_NUMERATOR
FP32_FINAL_CONTEXT

F32_FP16_BF16_PROFILES_PRESERVED
WG32_WORKGROUP_ONLY_BASELINE_PRESERVED
WG64_WG128_PARENT_SHADERS_PRESERVED
INDEPENDENT_F32_ORACLE_PRESERVED
PARENT_CONTEXT_TOLERANCE_UNCHANGED

CANDIDATE_SUBGROUP_CONTRACT_STATUS_LANE
NO_MID_REPLAY_REDUCTION_SWAP
NO_RUNTIME_FAILURE_FALLBACK

ZERO_RETAINED_SCORE
ZERO_STAGE11_TRANSITION_TAPE
ZERO_PROBABILITY_MATRIX
ZERO_SECONDARY_CANDIDATE_QK_RECOMPUTE

LOGICAL_BARRIER_RETIREMENT_RECEIPT
PARTIAL_DOT_RETIREMENT_RECEIPT
SUBGROUP_COLLECTIVE_RECEIPT

NO_UNMEASURED_SPEEDUP_CLAIM
NO_R4_PROMOTION_TABLE_MUTATION

SEALED
```