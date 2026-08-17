# ASH-ATTN-TENSORCUBE-FUSED-STREAMING-ATTENTION-SUBGROUP-MATRIX-TILE-AND-ADAPTIVE-WORKGROUP-R2

## Status

```text
Patch ID:
ASH-ATTN-TENSORCUBE-FUSED-STREAMING-ATTENTION-SUBGROUP-MATRIX-TILE-AND-ADAPTIVE-WORKGROUP-R2

Parent semantic authority:
ASH-ATTN-TENSORCUBE-STAGE10-11-12-FUSED-STREAMING-ATTENTION-NO-PROBABILITY-MATERIALIZATION-R1

Physical variants:
WG32 / WG64 / WG128
WorkgroupOnly / SubgroupAssisted

Running softmax state:
FP32

Weighted-V numerator:
FP32

Retained score tile:
0

Stage11 transition tape:
0

Probability matrix:
0
```

## Central closure

R1 fused attention remains the numerical/state-ownership SSOT. R2 changes lane and workgroup decomposition only.

```text
WG32  -> 1 KV token physical tile
WG64  -> 2 KV token physical tile
WG128 -> 4 KV token physical tile
```

Each variant has an explicit `WorkgroupOnly` and `SubgroupAssisted` reduction path. Runtime benchmark autotuning is not used.

## Deterministic selection authority

Selection table revision:

```text
FUSED_ATTN_VARIANT_SELECTION_TABLE_R1
```

Current candidate table:

```text
first replay chunk active KV <= 64 -> WG32
65..256                            -> WG64
>256                               -> WG128
```

The preferred workgroup is admitted against:

```text
max_compute_invocations_per_workgroup
max_compute_workgroup_storage_size
```

If the preferred size exceeds a known device limit, the selector chooses the largest admitted lower variant before dispatch. This is deterministic capability admission, not a runtime failure fallback.

The first replay chunk seals the selected workgroup/reduction path into `TensorCubeStage12ReplayState`. Later chunks reuse the same selection. No attention-state-chain mid-stream WG128->WG32 or subgroup->workgroup switch is allowed.

## Host surface

New module:

```text
crates/burn_webgpu_backend/src/tensorcube_fused_attention_r2_variants.rs
```

Key types:

```rust
pub enum FusedAttentionWorkgroupVariant {
    Wg32,
    Wg64,
    Wg128,
}

pub enum FusedAttentionReductionPath {
    WorkgroupOnly,
    SubgroupAssisted,
}
```

Pipeline-set identity binds:

```text
selection table revision
subgroup contract revision
tile geometry revision
SUBGROUP feature availability
device compute-invocation limit
device workgroup-storage limit
all six physical shader digests
```

## Physical shader set

```text
tensorcube_fused_attention_r2_wg32_workgroup.wgsl
tensorcube_fused_attention_r2_wg64_workgroup.wgsl
tensorcube_fused_attention_r2_wg128_workgroup.wgsl

tensorcube_fused_attention_r2_wg32_subgroup.wgsl
tensorcube_fused_attention_r2_wg64_subgroup.wgsl
tensorcube_fused_attention_r2_wg128_subgroup.wgsl
```

Admitted pipelines are created with the persistent Stage12 pipeline object and reused across chunk dispatches.

## Q cooperative reuse

The current fused profile remains `head_dim = 64`.

Each row/head workgroup loads Q once into:

```text
var<workgroup> q_cache: array<f32,64>
```

and reuses it across the chunk's KV tokens.

`q_global_read_elements` is derived from the R2 physical contract. `q_reuse_opportunity_elements` is a derived opportunity metric relative to repeated per-token Q reads. It is not a measured hardware DRAM counter.

## WorkgroupOnly path

No subgroup WGSL builtin is used.

Each 32-lane logical segment owns one token's 64-dimensional QK dot. WG64 therefore owns two simultaneous token segments and WG128 owns four. Dot products are reduced through workgroup scratch/barriers.

This is the explicit compatibility path when `wgpu::Features::SUBGROUP` is absent.

## SubgroupAssisted path

Subgroup pipelines are created only if the already-created WGPU device exposes:

```text
wgpu::Features::SUBGROUP
```

Each exact 32-lane subgroup owns one token QK dot and uses:

```text
subgroupAdd(local_dot)
```

The first subgroup performs physical token-tile reduction with:

```text
subgroupMax(score)
subgroupAdd(exp(score - tile_max))
```

The WGSL uses the WGPU26/Naga subgroup contract already present in ASH and does not add `enable subgroups;`.

SUBGROUP feature availability is not treated as proof of exact subgroup size 32. The shader requires `subgroup_size == 32`; a mismatch records a contract failure and does not switch physical backend mid-replay.

## Online softmax and weighted-V authority

For one physical token tile:

```text
m_tile = max(score_i)
l_tile = sum(exp(score_i - m_tile))
A_tile[d] = sum(exp(score_i - m_tile) * V[i,d])
```

With prior state:

```text
m_old
l_old
A_old
```

R2 computes:

```text
m_new = max(m_old, m_tile)
alpha = exp(m_old  - m_new)
beta  = exp(m_tile - m_new)

l_new = l_old * alpha + l_tile * beta
A_new = A_old * alpha + A_tile * beta
```

The same workgroup `alpha` and `beta` values drive both denominator and numerator. There is no separate Stage11/Stage12 rescale authority.

## V channel ownership

```text
WG32  -> each lane owns at most 2 of 64 V channels
WG64  -> first 64 lanes own one V channel each
WG128 -> first 64 lanes own one V channel each; remaining lanes own no V channel
```

This prevents one invocation from carrying the entire 64-channel numerator vector.

## FP32 authority preservation

R2 retains:

```text
Q/K/V working values = existing F32 contract
QK partials = FP32
score = FP32
tile max = FP32
tile denominator = FP32
running max = FP32
running denominator = FP32
weighted-V numerator = FP32
final normalization = FP32
```

No FP16/BF16 QKV storage adoption is included in R2.

## R1 invariants preserved

```text
candidate retained score read = 0
candidate Stage11 transition read = 0
full score matrix allocation = 0
probability matrix allocation = 0
secondary candidate QK recompute = 0
candidate K direct read > 0
candidate V direct read > 0
independent raw-Q/K/V oracle preserved
```

## Stage12/W7 receipts

Stage12/W7 now expose:

```text
selected_wg32_dispatch_count
selected_wg64_dispatch_count
selected_wg128_dispatch_count
subgroup_assisted_dispatch_count
workgroup_only_dispatch_count
q_global_read_elements
q_reuse_opportunity_elements
workgroup_scratch_high_water_bytes
```

Admission requires:

```text
WG32 + WG64 + WG128 dispatch counts
== candidate dispatch count

subgroup-assisted + workgroup-only dispatch counts
== candidate dispatch count
```

## Scratch/register evidence boundary

`declared_workgroup_storage_bytes` and `workgroup_scratch_high_water_bytes` are static diagnostics derived from declared WGSL workgroup variables and are checked against the device workgroup-storage limit.

`register_pressure_proxy_scalars_per_lane` is a static scheduling proxy. It is not an actual hardware register count and does not prove zero spilling. Physical profiler evidence remains required when available.

## Numerical parity boundary

R2 changes the FP32 reduction tree relative to R1's fixed WG32 token-at-a-time implementation. Mathematical authority is preserved, but bit-exact equality is not assumed without physical evidence.

The existing independent Stage12 oracle remains authoritative and the existing final verification tolerances are not changed:

```text
absolute tolerance = 2.0e-4
relative tolerance = 2.0e-3
relative floor = 1.0e-4
```

R2 does not silently widen them.

## Static validation

```text
tools/validate_ash_attn_tensorcube_fused_streaming_attention_subgroup_matrix_tile_adaptive_workgroup_r2_static.py
126/126 PASS
```

Static coverage includes:

```text
WG32/WG64/WG128 variants
WorkgroupOnly/SubgroupAssisted paths
SUBGROUP feature admission
device invocation/storage limit admission
deterministic selection table
state-chain variant seal
six physical shader variants
Q workgroup cache
1/2/4-token physical tiles
subgroup QK reduction
subgroup tile-max reduction
subgroup denominator reduction
shared alpha/beta recurrence
bounded V ownership
FP32 state/numerator
zero retained-score path
zero transition-tape path
zero probability matrix
W7 variant accounting
```

Parent gates retained in the bake environment:

```text
Stage11 active vendor adoption                 83/83 PASS
Vendor variable-row softmax                  100/100 PASS
Vendor mixed precision                        70/70 PASS
Vendor compact readback                       64/64 PASS
Generation-sealed Muon immutable cache        66/66 PASS
Muon backend surface rebind                    35/35 PASS
FFN multi-slot                                 78/78 PASS
FFN persistent resource slab                  66/66 PASS
FFN timestamp/resource-churn guard           101/101 PASS
FFN physical-perf harness static              72/72 PASS
FFN fused production                          45/45 PASS
GPU70K G45                                    42/42 PASS
GPU70K G27                                    35/35 PASS
Atlas/HOTPATH                                 56/56 PASS
HOTPATH allocation                            26/26 PASS
```

## Evidence status

The bake environment contains no Cargo/rustc/rustfmt/WGSL physical compiler or GPU runner.

```text
STATIC_BAKED_READY
NO_LOCAL_RUST_COMPILE_CLAIM
NO_LOCAL_WGSL_COMPILE_CLAIM
NO_SUBGROUP_PHYSICAL_TOPOLOGY_CLAIM
NO_GPU_PERFORMANCE_CLAIM
PHYSICAL_W7_GATE_REQUIRED
```

User-local Cargo/WGPU execution remains final physical SSOT.

## Physical promotion targets

```text
workgroup-only candidate compiles/runs without SUBGROUP feature
subgroup candidate compiles/runs only with SUBGROUP feature
observed subgroup size = 32 for subgroup-assisted promotion
candidate/oracle context mismatch = 0
nonfinite state/context = 0
write-order violation = 0
missing/duplicate final writes = 0
retained score read = 0
transition read = 0
probability matrix = 0
selected variant accounting exact
one selected variant identity per replay state chain
```

Performance evidence must compare R1 fused baseline against WG32/WG64/WG128 and subgroup/workgroup paths using actual GPU timing. No geometry class is promoted as faster before those receipts exist.

## Changed files

Overlay contains eleven files:

```text
crates/burn_webgpu_backend/src/lib.rs
crates/burn_webgpu_backend/src/tensorcube_fused_attention_r2_variants.rs
crates/burn_webgpu_backend/src/tensorcube_stage12_weighted_value_accumulation.rs
crates/burn_webgpu_backend/src/shaders/tensorcube_fused_attention_r2_wg32_workgroup.wgsl
crates/burn_webgpu_backend/src/shaders/tensorcube_fused_attention_r2_wg64_workgroup.wgsl
crates/burn_webgpu_backend/src/shaders/tensorcube_fused_attention_r2_wg128_workgroup.wgsl
crates/burn_webgpu_backend/src/shaders/tensorcube_fused_attention_r2_wg32_subgroup.wgsl
crates/burn_webgpu_backend/src/shaders/tensorcube_fused_attention_r2_wg64_subgroup.wgsl
crates/burn_webgpu_backend/src/shaders/tensorcube_fused_attention_r2_wg128_subgroup.wgsl
crates/model_core/src/attention_interconnect_w7.rs
tools/validate_ash_attn_tensorcube_fused_streaming_attention_subgroup_matrix_tile_adaptive_workgroup_r2_static.py
```

Code ZIPs contain no Markdown and no `*.sha256` files.

## Non-goals

```text
No FP16/BF16 fused QKV adoption
No half running max/denominator
No half weighted-V numerator
No runtime benchmark autotuner
No attention-state mid-stream variant swap
No cross-layer batching
No oracle retirement
No tolerance relaxation
No automatic performance promotion
```

## Next line

```text
ASH-ATTN-TENSORCUBE-FUSED-STREAMING-ATTENTION-FP16-BF16-QKV-STORAGE-FP32-STATE-ACCUMULATION-R3
```

## Promotion seal

```text
PROMOTE_ASH_ATTN_TENSORCUBE_FUSED_STREAMING_ATTENTION_SUBGROUP_MATRIX_TILE_AND_ADAPTIVE_WORKGROUP_R2

R1_FUSED_SEMANTIC_AUTHORITY_PRESERVED
DETERMINISTIC_VARIANT_SELECTION
FUSED_ATTN_VARIANT_SELECTION_TABLE_R1
STATE_CHAIN_VARIANT_SEALED
NO_MID_STREAM_VARIANT_SWAP
WG32_PHYSICAL_VARIANT
WG64_PHYSICAL_VARIANT
WG128_PHYSICAL_VARIANT
WORKGROUP_ONLY_COMPATIBILITY_PATH
SUBGROUP_ASSISTED_PATH
SUBGROUP_FEATURE_EXPLICIT_ADMISSION
SUBGROUP32_RUNTIME_CONTRACT
Q_WORKGROUP_COOPERATIVE_REUSE
ONE_TOKEN_WG32_TILE
TWO_TOKEN_WG64_TILE
FOUR_TOKEN_WG128_TILE
SUBGROUP_QK_REDUCTION
SUBGROUP_TILE_MAX_REDUCTION
SUBGROUP_TILE_DENOMINATOR_REDUCTION
FP32_RUNNING_MAX
FP32_RUNNING_DENOMINATOR
FP32_WEIGHTED_V_NUMERATOR
SHARED_ALPHA_BETA_RESCALE_AUTHORITY
BOUNDED_V_CHANNEL_OWNERSHIP
DECLARED_WORKGROUP_SCRATCH_GUARD
REGISTER_PRESSURE_PROXY_RECEIPT
NO_FAKE_PHYSICAL_REGISTER_CLAIM
NO_RETAINED_SCORE_TILE
NO_STAGE11_TRANSITION_TAPE
NO_PROBABILITY_MATRIX
NO_SECONDARY_CANDIDATE_QK_RECOMPUTE
INDEPENDENT_RAW_QKV_ORACLE_PRESERVED
PARENT_CONTEXT_TOLERANCE_UNCHANGED
NO_FP16_BF16_ADOPTION_YET
NO_RUNTIME_BENCHMARK_AUTOTUNE
NO_AUTOMATIC_PERFORMANCE_PROMOTION
SEALED
```