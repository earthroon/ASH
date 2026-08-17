# ASH-ATTN-TENSORCUBE-FUSED-STREAMING-ATTENTION-WG32-EXACT-SUBGROUP32-SINGLE-TOKEN-SCALARIZED-STATE-AND-Q-REGISTER-RESIDENCY-R3A1

## Status

```text
Patch ID:
ASH-ATTN-TENSORCUBE-FUSED-STREAMING-ATTENTION-WG32-EXACT-SUBGROUP32-SINGLE-TOKEN-SCALARIZED-STATE-AND-Q-REGISTER-RESIDENCY-R3A1

Direct attention parent:
ASH-ATTN-TENSORCUBE-FUSED-STREAMING-ATTENTION-EXACT-SUBGROUP32-QK-REDUCTION-AND-STATE-BROADCAST-R3A

Code parent SSOT:
ASH-BASETRAIN-TENSORCUBE-LOCAL-MUON-FIRST-CANDIDATE-REGISTRY-CANONICAL-LOAD-VERIFY-SSOT-AND-UNCONDITIONAL-RECURSION-REPAIR-R1 full body

Scope:
WG32 + ExactSubgroup32 + TOKENS_PER_TILE=1 only

Production promotion:
not automatic
```

## Central SSOT

R3A1 specializes only the exact physical WG32 subgroup path whose tile geometry is already fixed at one KV token.

```text
WG32
+ exact observed subgroup size = 32
+ single subgroup covers workgroup
+ TOKENS_PER_TILE = 1
    -> Q0/Q1 invocation-local FP32 register residency
    -> no q_cache[64]
    -> no Q-ready workgroupBarrier
    -> QK subgroupAdd retained
    -> tile max = score
    -> tile denominator = 1.0
    -> tile count = 1 for a valid token
    -> no single-token subgroupMax
    -> no single-token tile-sum subgroupAdd
    -> elected owner keeps running max/sum/count lane-local
    -> only alpha/beta are subgroupBroadcastFirst values
```

R1 fused-attention math, R2 WG64/WG128 geometry, R3 F32/FP16/BF16 profiles, R3A exact subgroup admission, independent F32 oracle, and existing tolerances remain authoritative.

## Exact physical admission

R3A1 does not infer subgroup size from `@workgroup_size(32,1,1)`.

It consumes the existing physical chain:

```text
device bootstrap subgroup probe
    -> runtime handle
    -> W7
    -> Stage12
    -> R2/R3 pipeline selection
```

The subgroup path remains admissible only when:

```text
SUBGROUP feature available
observed subgroup size = 32
selected workgroup = WG32
single_subgroup_workgroup = true
TOKENS_PER_TILE = 1
```

No same-replay reduction-path fallback or retile is added.

## Q register residency

Parent R3A exact WG32 used:

```text
64 FP32 Q scalars
    -> q_cache[64]
    -> 256 B workgroup scratch
    -> Q-ready workgroupBarrier
    -> each subgroup lane reads its two Q dimensions
```

R3A1 uses:

```wgsl
let d0 = subgroup_lane;
let d1 = subgroup_lane + 32u;
let q0 = load_q_scalar(query_head, global_query_row, d0);
let q1 = load_q_scalar(query_head, global_query_row, d1);
```

`q0` and `q1` are loaded once before the KV loop and remain invocation-local FP32 values for the full chunk loop.

The exact WG32 subgroup shaders contain no `var<workgroup>` declarations and no `workgroupBarrier()` calls. The final `storageBarrier()` is retained.

Structural retirement:

```text
q_cache scratch:          256 B -> 0 B
Q-ready workgroupBarrier: 1 / WG32 dispatch -> 0
logical Q element loads:  unchanged, 64 per query-row/head
```

This also removes any need to equate `local_invocation_index` with `subgroup_invocation_id`. Q dimension ownership is derived directly from `subgroup_invocation_id`.

## QK reduction

The R3A exact subgroup reduction remains the semantic QK reduction:

```wgsl
let reduced_dot = subgroupAdd(local_dot);
```

There is exactly one `subgroupAdd` call in each R3A1 exact WG32 shader source, and it is the FP32 QK reduction.

The following remain retired:

```text
partial_dot[32]
stride 16 -> 8 -> 4 -> 2 -> 1 tree
QK workgroup barriers
```

R3A logical accounting is updated to the actual R3A1 broadcast count while retaining its zero QK-tree barrier and zero partial-dot scratch authority.

## Single-token tile scalarization

For WG32:

```text
TOKENS_PER_TILE = 1
```

For a valid admitted token:

```text
m_tile = score
l_tile = exp(score - score) = 1
count_tile = 1
A_tile[d] = V[d]
```

R3A1 therefore directly uses:

```text
owner_max = score
owner_sum = 1.0
owner_count = 1
```

for first-token initialization.

For continuation:

```text
merged = max(owner_max, score)
alpha  = exp(owner_max - merged)
beta   = exp(score - merged)

owner_max   = merged
owner_sum   = owner_sum * alpha + beta
owner_count = owner_count + 1

A_new = A_old * alpha + V * beta
```

The old single-token operations are retired:

```text
subgroupMax(score)                    -> 0
tile denominator subgroupAdd(exp(0)) -> 0
exp(score - tile_max) for V weight   -> 0
```

Masked/inactive or non-finite tokens do not receive a fabricated denominator contribution. They leave owner state unchanged and use the parent fail/receipt behavior.

## Owner-local running state

Parent R3A broadcast running max, denominator and count across the subgroup at replay entry and after each token, even though only the elected transition owner required those values.

R3A1 keeps:

```text
owner_max
owner_sum
owner_count
```

as lane-local state on the elected subgroup owner across the KV loop.

Only weighted-V lanes require transition coefficients:

```text
alpha
beta
```

so the active per-token state broadcasts are reduced to:

```text
subgroupBroadcastFirst(owner_alpha)
subgroupBroadcastFirst(owner_beta)
```

Runtime logical accounting changes from:

```text
R3A state broadcasts: 5 / physical token iteration
R3A1 state broadcasts: 2 / physical token iteration
```

and the three initial running-state broadcasts per dispatch are also retired.

The shader retains `subgroupElect()` as the canonical single state-transition owner. It does not use indexed `subgroupBroadcast(value, 0)` and does not assume local-lane/subgroup-lane identity.

## FP32 authority

All precision profiles retain:

```text
Q register values             FP32
K/V decoded working values    FP32
QK partial                    FP32
QK subgroup reduction         FP32
score                         FP32
running maximum               FP32
running denominator           FP32
alpha / beta                  FP32
weighted-V numerator          FP32
final context                 FP32
```

FP16 and BF16 remain packed execution-storage formats only.

```text
packed FP16/BF16 Q -> explicit FP32 decode -> q0/q1 registers
packed FP16/BF16 K/V -> explicit FP32 decode -> fused math
```

No native BF16 arithmetic or half softmax/numerator state is introduced.

## Selector scratch authority

The R2 selector geometry remains:

```text
WG32  -> 1 token / tile
WG64  -> 2 tokens / tile
WG128 -> 4 tokens / tile
```

`FUSED_ATTN_VARIANT_SELECTION_TABLE_R1` is unchanged.

Only the declared WG32 SubgroupAssisted workgroup scratch is updated from the old Q-cache footprint to the actual R3A1 value:

```text
WG32 + SubgroupAssisted declared workgroup scratch = 0
```

WG64/WG128 selection behavior is unchanged.

## R3A1 identity

New identity revisions:

```text
WG32_EXACT_SUBGROUP32_SINGLE_TOKEN_SCALARIZATION_R1
WG32_Q_REGISTER_RESIDENCY_R1
SINGLE_TOKEN_DIRECT_TILE_STATE_R1
TOKENS_PER_TILE = 1
```

Stage12 pipeline identity binds these revisions in addition to the parent R2/R3/R3A identities and shader digests.

If WG32 `TOKENS_PER_TILE` changes in a future revision, this specialization must not be reused silently.

## R3A1 receipts

New logical/runtime evidence includes:

```text
wg32_single_token_r3a1_dispatch_count
q_cache_scratch_bytes_retired
q_ready_workgroup_barrier_count
q_ready_barrier_invocation_points_avoided
tile_max_subgroup_reduce_count
tile_sum_subgroup_reduce_count
redundant_state_broadcast_count
alpha_beta_broadcast_count
subgroup_collectives_avoided
```

For an active R3A1 replay the W7 final gate requires:

```text
exact subgroup32 admission
observed subgroup size = 32
R3A1 dispatch count = exact WG32 subgroup dispatch count
q_cache_scratch_bytes_retired = 256
q_ready_workgroup_barrier_count = 0
q_ready barrier avoided = one per R3A1 dispatch
tile_max_subgroup_reduce_count = 0
tile_sum_subgroup_reduce_count = 0
redundant_state_broadcast_count = 0
alpha_beta_broadcast_count = subgroup_broadcast_first_count
subgroup_collectives_avoided > 0
```

If all Stage12 candidate dispatches are R3A1 WG32, the final gate requires:

```text
workgroup_scratch_high_water_bytes = 0
```

Non-R3A1 variants continue to require their declared positive workgroup scratch where applicable.

## Structural operation retirement

Per physical token iteration in the R3A1 exact WG32 path:

```text
QK subgroupAdd                    retained: 1
state transition subgroupElect    retained: 1 normal transition owner
alpha/beta broadcast-first        retained: 2
single-token subgroupMax          retired: 0 active
tile-sum subgroupAdd              retired: 0 active
merged max/sum/count broadcasts   retired: 0 active
```

Additionally per WG32 dispatch:

```text
Q-ready workgroup barrier         retired: 1 -> 0
initial max/sum/count broadcasts  retired: 3 -> 0
```

`subgroup_collectives_avoided` is a logical structural count. It is not a GPU stall-cycle counter.

## Preserved physical references

The following parent shaders remain byte-identical:

```text
F32 WG32 WorkgroupOnly
half WG32 WorkgroupOnly
F32 WG64 WorkgroupOnly
F32 WG64 SubgroupAssisted
F32 WG128 WorkgroupOnly
F32 WG128 SubgroupAssisted
half WG64 WorkgroupOnly
half WG64 SubgroupAssisted
half WG128 WorkgroupOnly
half WG128 SubgroupAssisted
Stage12 independent raw-Q/K/V oracle
Stage12 context normalize/verify shader
```

This preserves direct A/B references for R3A/R3A1 promotion evidence.

## Forbidden regressions

R3A1 preserves:

```text
candidate retained-score read = 0
candidate Stage11-transition read = 0
full score matrix allocation = 0
full probability matrix allocation = 0
secondary candidate QK recompute = 0
same-replay fallback = absent
runtime retile = absent
```

The existing F32 oracle and context tolerance remain unchanged:

```text
absolute tolerance = 2.0e-4
relative tolerance = 2.0e-3
relative floor     = 1.0e-4
```

## Static verification

New validator:

```text
tools/validate_ash_attn_tensorcube_wg32_exact_subgroup32_single_token_scalarized_state_q_register_residency_r3a1_static.py
227/227 PASS
```

It checks the WG32 specialization, Q register residency, absence of workgroup scratch/barriers, single-token algebraic reduction, two alpha/beta broadcasts only, exact subgroup admission, identity/receipt closure, parent precision/oracle/tolerance authority, and parent SHA preservation for untouched WG32 WorkgroupOnly/WG64/WG128/oracle/finalizer shaders.

### Retained related gates

```text
Stage11 vendor adoption                         83/83 PASS
Vendor variable-row online softmax             100/100 PASS
Vendor mixed precision                          70/70 PASS
Vendor compact readback                         64/64 PASS
FirstCandidate registry                         97/97 PASS
Production Muon callsite                        63/63 PASS
TensorCube local Muon optimizer                101/101 PASS
Generation-sealed immutable Muon cache          66/66 PASS
Muon immutable-cache backend rebind             35/35 PASS
Muon registry recursion repair                  38/38 PASS
```

### Historical validator supersession

The old structural validators intentionally describe the pre-R3A1 WG32 subgroup implementation and therefore no longer fully pass:

```text
R2 historical validator    117/126
R3 historical validator    280/293
R3A historical validator   187/215
```

Their failures are limited to superseded WG32 subgroup expectations such as q_cache/shared scratch, single-token subgroup max/sum, five state broadcasts, old backend/W7 revisions, and the old positive scratch gate. The R3A1 227-gate validator rechecks the preserved parent invariants under the new specialization.

## Changed files

Overlay contains exactly nine files:

```text
crates/burn_webgpu_backend/src/lib.rs
crates/burn_webgpu_backend/src/shaders/tensorcube_fused_attention_r2_wg32_subgroup.wgsl
crates/burn_webgpu_backend/src/shaders/tensorcube_fused_attention_r3_wg32_subgroup_packed_half.wgsl
crates/burn_webgpu_backend/src/tensorcube_fused_attention_r2_variants.rs
crates/burn_webgpu_backend/src/tensorcube_fused_attention_r3a_exact_subgroup32.rs
crates/burn_webgpu_backend/src/tensorcube_fused_attention_r3a1_wg32_single_token.rs
crates/burn_webgpu_backend/src/tensorcube_stage12_weighted_value_accumulation.rs
crates/model_core/src/attention_interconnect_w7.rs
tools/validate_ash_attn_tensorcube_wg32_exact_subgroup32_single_token_scalarized_state_q_register_residency_r3a1_static.py
```

Code ZIPs contain no Markdown, `*.sha256`, or Python cache artifacts.

## Evidence boundary

The bake environment has no Cargo/rustc/WGSL compiler or physical GPU execution authority.

```text
STATIC_BAKED_READY
NO_LOCAL_RUST_COMPILE_CLAIM
NO_LOCAL_WGSL_COMPILE_CLAIM
NO_PHYSICAL_GPU_SPEEDUP_CLAIM
NO_OCCUPANCY_IMPROVEMENT_CLAIM
NO_REGISTER_SPILL_CLAIM
PHYSICAL_W7_GATE_REQUIRED
```

The following are structurally established without performance measurement:

```text
q_cache 256 B retired
Q-ready workgroup barrier retired
single-token subgroupMax retired
tile-sum subgroupAdd retired
merged max/sum/count broadcasts retired
initial running max/sum/count broadcasts retired
QK subgroupAdd preserved
alpha/beta broadcasts preserved
```

Actual GPU latency, occupancy, spill behavior, cache behavior, and power effects remain physical evidence questions.

## Physical promotion targets

```text
Cargo/WGSL compile PASS
observed subgroup size = 32
R3A1 subgroup contract failures = 0
F32 R3A1 candidate/oracle parity PASS
FP16 R3A1 candidate/oracle parity PASS
BF16 R3A1 candidate/oracle parity PASS
existing tolerance unchanged
q_cache retirement receipt = 256 B
Q-ready barrier active count = 0
tile max/sum reduction active count = 0
alpha/beta-only broadcast accounting PASS
workgroup scratch high-water = 0 for all-R3A1 replay
R3A vs R3A1 physical timestamp distribution recorded
```

## Non-goals

```text
No WG64 rewrite
No WG128 rewrite
No K/V vec4 remap
No TOKENS_PER_TILE increase
No new precision profile
No half running softmax state
No half numerator
No attention formula mutation
No causal/GQA mutation
No runtime autotuner
No R4 promotion table mutation
No automatic production promotion
```

## Natural next step

After physical R3A1 parity/performance evidence, the cleanest independent hotspot remains the TensorCube Local Muon norm path whose 256-element norm is currently serialized through one invocation. That should be handled as a separate patch with the current serial path retained as numerical oracle.

## Promotion seal

```text
PROMOTE_ASH_ATTN_TENSORCUBE_FUSED_STREAMING_ATTENTION_WG32_EXACT_SUBGROUP32_SINGLE_TOKEN_SCALARIZED_STATE_AND_Q_REGISTER_RESIDENCY_R3A1

R3A_EXACT_SUBGROUP32_AUTHORITY_PRESERVED
R3_PRECISION_AUTHORITY_PRESERVED
R2_VARIANT_AUTHORITY_PRESERVED
R1_FUSED_SEMANTIC_AUTHORITY_PRESERVED
WG32_ONLY
EXACT_PHYSICAL_SUBGROUP32
TOKENS_PER_TILE_ONE_SEALED
Q0_Q1_FP32_REGISTER_RESIDENCY
ZERO_Q_WORKGROUP_CACHE
256_BYTE_Q_CACHE_RETIREMENT
ZERO_Q_READY_WORKGROUP_BARRIER
NO_LOCAL_SUBGROUP_LANE_MAPPING_ASSUMPTION
SUBGROUP_INVOCATION_OWNED_Q_DIMENSIONS
QK_FP32_SUBGROUP_ADD_PRESERVED
ZERO_PARTIAL_DOT_SCRATCH
ZERO_QK_TREE_BARRIERS
SINGLE_TOKEN_TILE_MAX_EQUALS_SCORE
SINGLE_TOKEN_TILE_DENOMINATOR_EQUALS_ONE
SINGLE_TOKEN_TILE_COUNT_EQUALS_ONE
ZERO_SINGLE_TOKEN_SUBGROUP_MAX
ZERO_SINGLE_TOKEN_TILE_SUM_SUBGROUP_ADD
SUBGROUP_ELECT_STATE_OWNER_PRESERVED
OWNER_LOCAL_RUNNING_MAX_SUM_COUNT
ALPHA_BETA_ONLY_STATE_BROADCAST
ZERO_MERGED_MAX_BROADCAST
ZERO_MERGED_DENOMINATOR_BROADCAST
ZERO_MERGED_COUNT_BROADCAST
ZERO_INITIAL_RUNNING_STATE_BROADCAST
FP32_RUNNING_MAX
FP32_RUNNING_DENOMINATOR
FP32_ALPHA_BETA
FP32_WEIGHTED_V_NUMERATOR
FP32_FINAL_CONTEXT
F32_PROFILE_PRESERVED
FP16_PROFILE_PRESERVED
BF16_PROFILE_PRESERVED
WG32_WORKGROUP_ONLY_BASELINE_PRESERVED
WG64_PARENT_VARIANTS_UNTOUCHED
WG128_PARENT_VARIANTS_UNTOUCHED
INDEPENDENT_F32_ORACLE_PRESERVED
PARENT_CONTEXT_TOLERANCE_UNCHANGED
ZERO_RETAINED_SCORE
ZERO_STAGE11_TRANSITION_TAPE
ZERO_PROBABILITY_MATRIX
NO_R4_PROMOTION_MUTATION
NO_UNMEASURED_SPEEDUP_CLAIM
SEALED
```
