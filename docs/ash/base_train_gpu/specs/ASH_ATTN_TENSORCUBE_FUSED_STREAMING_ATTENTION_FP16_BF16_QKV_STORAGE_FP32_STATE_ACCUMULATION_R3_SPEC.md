# ASH-ATTN-TENSORCUBE-FUSED-STREAMING-ATTENTION-FP16-BF16-QKV-STORAGE-FP32-STATE-ACCUMULATION-R3

## Status

```text
Patch ID:
ASH-ATTN-TENSORCUBE-FUSED-STREAMING-ATTENTION-FP16-BF16-QKV-STORAGE-FP32-STATE-ACCUMULATION-R3

Parent physical authority:
ASH-ATTN-TENSORCUBE-FUSED-STREAMING-ATTENTION-SUBGROUP-MATRIX-TILE-AND-ADAPTIVE-WORKGROUP-R2

Precision profiles:
F32Safe
Fp16QkvStorageF32State
Bf16QkvStorageF32State

Default profile:
F32Safe

Half representation:
packed u32 pairs

Half decode destination:
FP32 working values

Running softmax state:
FP32

Weighted-V numerator:
FP32

Final context:
FP32
```

## Parent SSOT

Direct parent:

```text
ASH-ATTN-TENSORCUBE-FUSED-STREAMING-ATTENTION-SUBGROUP-MATRIX-TILE-AND-ADAPTIVE-WORKGROUP-R2
```

Semantic parent:

```text
ASH-ATTN-TENSORCUBE-STAGE10-11-12-FUSED-STREAMING-ATTENTION-NO-PROBABILITY-MATERIALIZATION-R1
```

Precision primitive parent:

```text
ASH-BURN-VENDOR-MIXED-PRECISION-TENSOR-PRIMITIVES-FP16-BF16-STORAGE-FP32-ACCUMULATION-R1
```

R3 preserves the R2 WG32/WG64/WG128 and WorkgroupOnly/SubgroupAssisted selection authority and the R1 fused-attention equations. It changes only candidate Q/K/V execution-storage representation for explicit half-storage profiles.

## Central authority

```text
F32 canonical Q/K/V source authority
        |
        +----------------------+----------------------+
        |                      |                      |
        v                      v                      v
     F32Safe                 FP16                  BF16
        |                      |                      |
        v                      v                      v
R2 F32 texture path    packed-u32 Q/K/V      packed-u32 Q/K/V
                               |                      |
                               +----------+-----------+
                                          v
                                  explicit F32 decode
                                          |
                                          v
                               R2 fused execution geometry
                                          |
                                          v
                           FP32 QK / softmax / weighted-V
```

Half buffers are derived execution representations. They do not become model, checkpoint, optimizer, or master-tensor authority.

## Precision profiles

```rust
pub enum FusedAttentionR3PrecisionProfile {
    F32Safe,
    Fp16QkvStorageF32State,
    Bf16QkvStorageF32State,
}
```

Physical paths:

```text
F32Safe                -> F32_R2_TEXTURE_BASELINE
FP16 QKV storage       -> PACKED_FP16_U32_TO_FP32
BF16 QKV storage       -> PACKED_BF16_U32_TO_FP32
```

`TensorCubeStage12WeightedValuePipeline::new()` and the default W7 constructors remain F32Safe. Half profiles require explicit precision-aware construction. There is no automatic default promotion.

## Precision identity revisions

```text
PACKED_HALF_U32_PAIR_R1
PACKED_HALF_EXPLICIT_TO_FP32_R1
FP32_MAX_DENOM_WEIGHTED_V_CONTEXT_R1
QKV_PACKED_U32_PAIR_LAYOUT_PRESERVE_R1
```

The R3 identity binds precision profile, physical path, storage/decode/state/layout revisions, the parent R2 pipeline identity digest, the quantizer digest, and all six half-candidate shader digests.

## Replay-scoped Q/K/V derivation

R3 deliberately does not introduce a cross-invocation generation-level half KV cache.

For an explicit FP16/BF16 replay:

```text
first replay descriptor
    -> allocate packed Q
    -> allocate packed K
    -> allocate packed V
    -> quantize Q once
    -> quantize K once
    -> quantize V once
    -> reuse packed buffers for the remaining replay descriptors
```

`precision_buffers_initialized` seals this one-shot conversion boundary. There is no per-dispatch requantization.

This R3 therefore proves bounded replay-scoped half-buffer reuse, not persistent generation-level half KV residency.

## Quantizer

New shader:

```text
crates/burn_webgpu_backend/src/shaders/tensorcube_fused_attention_r3_qkv_quantize.wgsl
```

### FP16

```text
F32 pair -> pack2x16float -> packed u32
```

No shader-f16 arithmetic is required.

### BF16

BF16 uses deterministic round-to-nearest-even bit conversion and stores two BF16 bit patterns per u32. BF16 storage does not imply native BF16 arithmetic.

## Compact precision status

The quantizer writes a 32-byte GPU status surface:

```text
word 0  nonfinite F32 input count
word 1  FP16 finite overflow count
word 2  FP16 underflow-to-zero count
word 3  BF16 overflow count
word 4  BF16 underflow-to-zero count
word 5  odd packed-pair tail count
word 6  quantize dispatch count
word 7  reserved
```

There is no silent FP16 clamp.

For a normal half replay:

```text
quantize_dispatch_count = 3
requantize_element_count = 0
```

The status copy/readback is attached to the existing Stage12/W7 final gate. The quantization primitive itself owns no queue submit, MAP_READ, or PollType::Wait. Existing final-gate pipeline readback/wait authority remains and is not claimed retired.

## Candidate bind surface

Half profiles use a dedicated storage-buffer candidate bind layout:

```text
binding 0  chunk params
binding 1  packed Q u32
binding 2  packed K u32
binding 3  packed V u32
binding 4  candidate softmax state
binding 5  FP32 weighted-V numerator
binding 6  candidate write counts
binding 7  candidate status
```

F32Safe continues to use the exact R2 F32 texture candidate path.

The independent oracle continues to use F32 raw Q/K/V and does not share the half decoder.

## Six half execution variants

R2 geometry is retained:

```text
WG32  WorkgroupOnly
WG64  WorkgroupOnly
WG128 WorkgroupOnly
WG32  SubgroupAssisted
WG64  SubgroupAssisted
WG128 SubgroupAssisted
```

The same `FusedAttentionR2VariantSelection` chooses the workgroup/reduction path. Precision does not retune `FUSED_ATTN_VARIANT_SELECTION_TABLE_R1` in R3.

## Explicit decode boundary

Packed shaders implement:

```text
FP16 packed u32 -> unpack2x16float -> F32
BF16 packed u32 -> BF16 bits << 16 -> F32
```

Q decodes into the existing FP32 workgroup q-cache and is reused across KV tokens. K and V are decoded only for admitted physical elements. Exact element-count guards prevent an odd packed pair's invalid high half from becoming a tensor element.

## FP32 numerical authority

All profiles retain:

```text
Q working value             F32
K working value             F32
V working value             F32
QK partial                  F32
QK accumulator              F32
scaled score                F32
tile max                    F32
tile denominator            F32
running max                 F32
running denominator         F32
alpha / beta                F32
weighted-V numerator        F32
final normalization         F32
final context               F32
```

There is no FP16/BF16 running state and no half weighted-V accumulator.

## Shared alpha/beta authority

R1/R2 recurrence remains unchanged:

```text
m_new = max(m_old, m_tile)
alpha = exp(m_old  - m_new)
beta  = exp(m_tile - m_new)

l_new = l_old * alpha + l_tile * beta
A_new = A_old * alpha + A_tile * beta
```

The same FP32 alpha/beta values update denominator and weighted-V numerator.

## Precision state-chain seal

A replay fixes:

```text
precision profile
physical precision path
R2 WG32/WG64/WG128 selection
R2 WorkgroupOnly/SubgroupAssisted selection
```

No same-replay FP16->BF16, FP16->F32, or BF16->F32 switch is allowed. If a requested half pipeline is unavailable, execution fails closed instead of silently changing precision inside the active replay state chain.

## R2 authority preservation

R3 does not change:

```text
FUSED_ATTN_VARIANT_SELECTION_TABLE_R1
WG32/WG64/WG128 geometry
WorkgroupOnly/SubgroupAssisted capability admission
first-chunk variant seal
subgroup-size-32 runtime contract
```

The original six R2 F32 shaders remain present and precision-unmodified as the F32 physical performance baseline.

## Intermediate materialization remains retired

R3 preserves:

```text
candidate retained-score read = 0
candidate Stage11-transition read = 0
full probability-matrix allocation = 0
secondary candidate QK recompute = 0
```

Half profiles do not reintroduce those surfaces.

## Precision telemetry

Stage12/W7 receipts expose:

```text
precision profile / physical path
Q/K/V quantized element counts
Q/K/V decoded element counts
requantize element count
Q/K/V storage bytes
F32-equivalent storage bytes
storage bytes avoided
nonfinite input count
FP16 overflow / underflow
BF16 overflow / underflow
odd pair tail count
quantize dispatch count
```

Q/K/V decode counts are logical counts derived from admitted geometry, not hardware DRAM transaction counters. `storage_bytes_avoided` is a representation-size receipt and is not proof that realized memory bandwidth is reduced by exactly the same fraction.

## Context error receipt

When the existing gate/debug full context readback is enabled, R3 also surfaces:

```text
context_error_distribution_available = true
candidate_oracle_max_abs_error
candidate_oracle_mean_abs_error
```

When diagnostic context readback is disabled, the distribution is explicitly unavailable rather than fabricated.

R3 does not widen the existing Stage12 candidate/oracle tolerance contract.

## Independent references

```text
correctness reference  = independent F32 raw-Q/K/V oracle
performance reference  = R2 F32 fused candidate
```

FP16/BF16 therefore have an independent semantic reference and an unchanged F32 fused execution baseline.

## Admission behavior

W7 rejects, among other cases:

```text
F32 profile unexpectedly performing half-storage work
half profile unexpectedly using candidate K/V texture reads
incomplete half precision receipt
requantize_element_count != 0
quantize_dispatch_count != 3
precision nonfinite input count != 0
FP16 finite overflow count != 0 for FP16
BF16 overflow count != 0 for BF16
R2 variant/reduction accounting mismatch
retained-score/transition/probability regression
```

Underflow is observed and reported. R3 does not invent a universal underflow rejection threshold without physical evidence.

## Static validation

```text
tools/validate_ash_attn_tensorcube_fused_streaming_attention_fp16_bf16_qkv_storage_fp32_state_accumulation_r3_static.py
293/293 PASS
```

Coverage includes explicit F32/FP16/BF16 profiles, deterministic packed quantization, compact status, six half variants, FP32 decode/state/accumulation authority, R2 geometry preservation, one-shot replay derivation, zero requantization, direct packed Q/K/V binding, independent F32 oracle, R2 F32 baseline, context error receipt surfaces, and zero retained-score/transition/probability regressions.

Parent gates retained in the bake environment:

```text
Stage11 active vendor adoption                  83/83 PASS
Vendor variable-row softmax                   100/100 PASS
Vendor mixed precision                         70/70 PASS
Vendor compact readback                        64/64 PASS
Generation-sealed Muon immutable cache         66/66 PASS
Muon backend surface rebind                    35/35 PASS
FFN multi-slot                                  78/78 PASS
FFN persistent resource slab                   66/66 PASS
FFN timestamp/resource-churn guard            101/101 PASS
FFN physical-perf harness static               72/72 PASS
FFN fused production                           45/45 PASS
GPU70K G45                                     42/42 PASS
GPU70K G27                                     35/35 PASS
Atlas/HOTPATH                                  56/56 PASS
HOTPATH allocation                             26/26 PASS
```

The old R2 validator expects the R2 W7 revision literal and is superseded for the upgraded W7 surface. The R3 validator directly revalidates the R2 geometry, reduction-path, and state-chain invariants.

## Bake files

Overlay contains exactly twelve files:

```text
crates/burn_webgpu_backend/src/lib.rs
crates/burn_webgpu_backend/src/tensorcube_fused_attention_r3_precision.rs
crates/burn_webgpu_backend/src/tensorcube_stage12_weighted_value_accumulation.rs
crates/model_core/src/attention_interconnect_w7.rs
crates/burn_webgpu_backend/src/shaders/tensorcube_fused_attention_r3_qkv_quantize.wgsl
crates/burn_webgpu_backend/src/shaders/tensorcube_fused_attention_r3_wg32_workgroup_packed_half.wgsl
crates/burn_webgpu_backend/src/shaders/tensorcube_fused_attention_r3_wg64_workgroup_packed_half.wgsl
crates/burn_webgpu_backend/src/shaders/tensorcube_fused_attention_r3_wg128_workgroup_packed_half.wgsl
crates/burn_webgpu_backend/src/shaders/tensorcube_fused_attention_r3_wg32_subgroup_packed_half.wgsl
crates/burn_webgpu_backend/src/shaders/tensorcube_fused_attention_r3_wg64_subgroup_packed_half.wgsl
crates/burn_webgpu_backend/src/shaders/tensorcube_fused_attention_r3_wg128_subgroup_packed_half.wgsl
tools/validate_ash_attn_tensorcube_fused_streaming_attention_fp16_bf16_qkv_storage_fp32_state_accumulation_r3_static.py
```

Code ZIPs contain no Markdown, no `*.sha256`, and no Python cache artifacts.

## Evidence status

The bake environment has no Rust/Cargo/WGSL physical compile or GPU execution authority.

```text
STATIC_BAKED_READY
NO_LOCAL_RUST_COMPILE_CLAIM
NO_LOCAL_WGSL_COMPILE_CLAIM
NO_PHYSICAL_FP16_ERROR_DISTRIBUTION_CLAIM
NO_PHYSICAL_BF16_ERROR_DISTRIBUTION_CLAIM
NO_MEMORY_BANDWIDTH_HALVED_CLAIM
NO_GPU_SPEEDUP_CLAIM
PHYSICAL_W7_GATE_REQUIRED
```

User-local Cargo/WGPU execution remains the final physical SSOT.

## Physical promotion targets

```text
F32 R2 baseline compiles/runs
FP16 quantizer and admitted variants compile/run
BF16 quantizer and admitted variants compile/run
WorkgroupOnly path runs
SubgroupAssisted path runs where physically admitted
quantize_dispatch_count = 3
requantize_element_count = 0
precision_nonfinite_input_count = 0
profile-specific overflow count = 0
candidate/oracle final context gate PASS
FP16/BF16 context error receipt produced when diagnostic readback is enabled
retained-score read = 0
transition read = 0
probability matrix allocation = 0
secondary candidate QK recompute = 0
```

Performance receipts must compare R2 F32, R3 FP16, and R3 BF16 including conversion cost, storage bytes, GPU time, memory high-water, and repeated reuse. Storage-byte reduction alone is not sufficient evidence of realized bandwidth or speed improvement.

## Non-goals

```text
No half running softmax state
No half weighted-V numerator
No half final context
No native BF16 arithmetic claim
No shader-f16 requirement
No stochastic rounding
No loss scaling
No checkpoint/master precision migration
No optimizer precision mutation
No mixed Q/K/V dtype combinations
No generation-level persistent half KV cache yet
No precision-aware workgroup retuning yet
No dynamic precision autotuner
No oracle retirement
No automatic production default change
```

## Next line

```text
ASH-ATTN-TENSORCUBE-FUSED-STREAMING-ATTENTION-PRECISION-AWARE-VARIANT-SELECTION-AND-PER-GEOMETRY-PROMOTION-R4
```

## Promotion seal

```text
PROMOTE_ASH_ATTN_TENSORCUBE_FUSED_STREAMING_ATTENTION_FP16_BF16_QKV_STORAGE_FP32_STATE_ACCUMULATION_R3

R2_VARIANT_AUTHORITY_PRESERVED
R1_FUSED_SEMANTIC_AUTHORITY_PRESERVED
EXPLICIT_PRECISION_PROFILE
F32_SAFE_DEFAULT
FP16_QKV_PACKED_STORAGE
BF16_QKV_PACKED_STORAGE
PACKED_U32_PAIR_STORAGE
EXPLICIT_HALF_TO_FP32_DECODE
NO_NATIVE_BF16_ARITHMETIC_CLAIM
NO_SHADER_F16_REQUIREMENT
REPLAY_SCOPED_DERIVED_QKV_BUFFERS
ONE_SHOT_Q_K_V_QUANTIZATION
NO_PER_DISPATCH_REQUANTIZATION
FP32_Q_WORKING_VALUE
FP32_K_WORKING_VALUE
FP32_V_WORKING_VALUE
FP32_QK_ACCUMULATION
FP32_SCORE
FP32_TILE_MAX
FP32_TILE_DENOMINATOR
FP32_RUNNING_MAX
FP32_RUNNING_DENOMINATOR
FP32_ALPHA_BETA
FP32_WEIGHTED_V_NUMERATOR
FP32_FINAL_CONTEXT
NO_HALF_SOFTMAX_STATE
NO_HALF_WEIGHTED_V_ACCUMULATOR
NO_HALF_FINAL_CONTEXT
R2_WG32_WG64_WG128_PRESERVED
R2_WORKGROUP_SUBGROUP_PATHS_PRESERVED
NO_PRECISION_DRIVEN_VARIANT_RETUNING
PRECISION_PROFILE_REPLAY_CHAIN_SEAL
NO_MID_REPLAY_PRECISION_SWAP
NO_SILENT_F32_FALLBACK
COMPACT_PRECISION_STATUS_RECEIPT
FP16_OVERFLOW_UNDERFLOW_RECEIPT
BF16_OVERFLOW_UNDERFLOW_RECEIPT
ODD_PAIR_TAIL_RECEIPT
ZERO_RETAINED_SCORE
ZERO_STAGE11_TRANSITION_TAPE
ZERO_PROBABILITY_MATRIX
ZERO_SECONDARY_CANDIDATE_QK_RECOMPUTE
INDEPENDENT_F32_ORACLE_PRESERVED
R2_F32_PERFORMANCE_BASELINE_PRESERVED
PARENT_CONTEXT_TOLERANCE_UNCHANGED
CONTEXT_ERROR_DISTRIBUTION_WHEN_GATE_READBACK_AVAILABLE
NO_FAKE_ERROR_DISTRIBUTION_WHEN_UNAVAILABLE
NO_CHECKPOINT_AUTHORITY_MIGRATION
NO_OPTIMIZER_PRECISION_MUTATION
NO_AUTOMATIC_PRODUCTION_PROMOTION
NO_UNMEASURED_SPEEDUP_CLAIM
SEALED
```