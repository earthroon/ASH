# ASH-ATTN-TENSORCUBE-STAGE10-11-12-FUSED-STREAMING-ATTENTION-NO-PROBABILITY-MATERIALIZATION-R1

## Status

```text
Patch ID:
ASH-ATTN-TENSORCUBE-STAGE10-11-12-FUSED-STREAMING-ATTENTION-NO-PROBABILITY-MATERIALIZATION-R1

Actual output candidate authority:
W7 fused Q/K/V streaming candidate

Verification authority:
existing W5/W6 Stage10/Stage11 preflight + independent raw-Q/K/V Stage12 oracle

Score lifetime in fused candidate:
register/workgroup only

Retained score tile transport:
retired

Stage11 transition tape transport:
retired

Probability matrix:
never materialized
```

## Parent SSOT

```text
ASH-ATTN-TENSORCUBE-STAGE12-VARIABLE-ROW-ONLINE-SOFTMAX-V-WEIGHTED-ACCUMULATION-R1
ASH-ATTN-TENSORCUBE-STAGE11-VARIABLE-ROW-VENDOR-PRIMITIVE-ADOPTION-R1
ASH-BURN-VENDOR-VARIABLE-ROW-ONLINE-SOFTMAX-DESCRIPTOR-DISPATCH-AND-FP32-STATE-REDUCTION-R1
ASH-BURN-VENDOR-MIXED-PRECISION-TENSOR-PRIMITIVES-FP16-BF16-STORAGE-FP32-ACCUMULATION-R1
ASH-BURN-VENDOR-GPU-RESIDENT-VERIFICATION-COMPACT-READBACK-RECEIPT-ASYNC-STAGING-RING-AND-SUBMISSION-COALESCING-R1
```

## Central closure

The previous Stage12 candidate removed a second QK reconstruction by retaining Stage10 scores and a Stage11 maximum-transition tape across stage boundaries.

This revision removes those intermediate global surfaces from the actual output candidate path.

```text
Q + K texture
    |
    v
scaled QK score
    |
    | score exists only inside fused workgroup lifetime
    v
FP32 online max / denominator update
    |
    +------ same alpha / beta ------+
    |                                |
    v                                v
FP32 softmax state             FP32 weighted-V numerator
                                     |
                                     v
                         final denominator normalization
                                     |
                                     v
                           candidate attention context
```

The candidate score is computed once per active token in the fused candidate invocation, consumed immediately, and not written to a global score buffer or probability buffer.

### Evidence boundary

This does not claim that the complete verification invocation performs QK only once globally. W5/W6 preflight verification and the independent Stage12 raw-Q/K/V oracle intentionally remain and may perform their own QK work. The single-pass claim applies to the actual fused output candidate authority.

## Stage10 retained-score retirement

Stage10 keeps its existing statistics production for W5/W6 verification but no longer allocates, owns, reports, or transports a candidate retained-score tile.

New score-lifetime identity:

```text
ash.tensorcube.stage10.score-register-workgroup-lifetime.f32.v1
```

Removed from Stage10/W5/W6 transport:

```text
candidate_score_tile
candidate_score_tile_buffer_digest
candidate_score_tile_element_count
candidate_score_tile_bytes
candidate_score_tile_abi
```

The Stage10 candidate WGSL has no retained-score storage binding and performs no global score-tile write.

## Stage11 transition-tape retirement

The vendor pre-reduced Stage11 verifier still consumes Stage10 local max / exp-sum / count statistics and preserves the existing FP32 online denominator merge formula.

Removed from the physical transport contract:

```text
transition_record_index
transition_records GPU buffer
candidate_transition_records
transition_record_base
transition_record_count
retained_score_tiles
```

The vendor pre-reduced bind group contracts from seven resources to six and no longer writes a transition record.

Stage11 backend identity advances to:

```text
ASH-ATTN-TENSORCUBE-STAGE11-VENDOR-PREREDUCED-ACTIVE-R1-FUSED-DOWNSTREAM-R1
```

W5/W6 Stage11 output remains verification evidence. The fused W7 candidate clears the candidate state at the first replay descriptor and becomes the actual candidate state producer for final context generation.

## Fused candidate shader

New shader:

```text
crates/burn_webgpu_backend/src/shaders/
tensorcube_stage10_11_12_fused_streaming_attention_candidate.wgsl
```

Candidate bindings:

```text
0  chunk/replay params
1  Q F32 storage
2  K rgba32f texture
3  V rgba32f texture
4  candidate fused softmax state, read/write
5  FP32 weighted-V numerator, read/write
6  candidate chunk write counts
7  candidate status lane
```

There is no retained-score binding and no transition-tape binding.

## Fused state recurrence

For each canonical active token:

```text
score = scaled dot(Q, K)
```

The running state is:

```text
m = running maximum
l = running denominator
A = running weighted-V numerator vector
```

For a newly admitted score `s`:

```text
m_next = max(m, s)
alpha  = exp(m - m_next)
beta   = exp(s - m_next)

l_next = l * alpha + beta
A_next = A * alpha + V * beta
```

For the first valid score:

```text
alpha = 0
beta  = 1
m     = score
l     = 1
A     = V
```

The exact same `alpha` and `beta` workgroup values drive denominator and numerator evolution. Stage11-like softmax state and Stage12-like V numerator therefore cannot silently diverge through separately recomputed rescale factors in the fused candidate.

## FP32 authority

R1 keeps:

```text
Q/K/V decoded working values = existing F32 contract
QK score = F32
running max = F32
running denominator = F32
weighted-V numerator = F32
final context normalization = F32
```

No FP16/BF16 accumulator or half softmax state is introduced.

## Variable active domain / causal contract

The fused candidate preserves the existing TensorCube absolute-position causal test:

```text
key_absolute <= query_absolute
```

Only admitted tokens perform QK contribution, exponential weight generation, V read, denominator contribution, and numerator contribution. Inactive physical tail values are not admitted.

Existing GQA mapping is preserved:

```text
kv_head = query_head / gqa_group_size
```

No new attention policy is introduced in the vendor layer.

## Canonical candidate state ownership

`TensorCubeStage12ReplayState` keeps the candidate global-state GPU buffer identity received from W6.

At the first fused replay descriptor:

```text
candidate_global_state clear
candidate numerator clear
candidate write-count clear
status clear
```

The fused W7 candidate then rewrites candidate state from Q/K/V in canonical chunk order. Final normalization therefore consumes fused-produced candidate max / denominator state rather than the earlier W6 candidate values.

The independent W6 oracle state remains untouched and is used by the existing raw-Q/K/V Stage12 oracle.

## Finalization

Existing Stage12 final normalize/verify remains:

```text
candidate context = fused candidate numerator / fused candidate denominator
oracle context    = oracle numerator / oracle denominator
```

Existing contracts remain for candidate/oracle context mismatch, nonfinite context, all-masked/inactive zero context, denominator validity, missing/duplicate final writes, and canonical chunk write counts.

## No intermediate materialization

Actual fused candidate receipt seals:

```text
candidate_stage10_score_tile_read_count = 0
candidate_transition_record_read_count = 0
full_score_matrix_allocation_count = 0
full_probability_matrix_allocation_count = 0
```

The previous retained-score shader source may remain in the snapshot as unused historical source, but the fused candidate pipeline does not include or bind it.

## Candidate direct-read telemetry

The fused Stage12 receipt requires:

```text
candidate_k_texture_read_count > 0
candidate_v_texture_read_count > 0
candidate_stage10_score_tile_read_count = 0
candidate_transition_record_read_count = 0
candidate_qk_recompute_count = 0
```

`candidate_qk_recompute_count` remains the secondary replay counter. The primary fused QK calculation is the actual candidate calculation and is not classified as a recompute.

W7 pass token explicitly names:

```text
FUSED_STREAMING_ATTENTION_CANDIDATE_QK_SINGLE_PASS
```

rather than making a system-wide QK-once claim.

## Independent oracle preservation

The existing raw-Q/K/V Stage12 oracle remains unchanged and independently reads Q, reads raw K, computes QK, uses oracle global state, reads raw V, and accumulates oracle numerator.

This keeps the fused candidate from verifying itself.

## Submission/readback boundary

The fused shader contains no:

```text
queue.submit
MAP_READ
PollType::Wait
```

W7 keeps caller-owned chunk encoding. Existing Stage12 final-gate submission/readback remains outside the fused primitive and is not claimed retired.

## Static validation

```text
tools/validate_ash_attn_tensorcube_stage10_11_12_fused_streaming_attention_no_probability_materialization_r1_static.py
72/72 PASS
```

It verifies Stage10 retained-score retirement, W5/W6 score-tile transport retirement, Stage11 transition-tape retirement, vendor transition binding retirement, fused direct Q/K/V candidate binding, fused candidate state write, shared alpha/beta denominator and numerator recurrence, zero retained-score/transition reads, zero probability materialization, independent raw-Q/K/V oracle preservation, W7 fused direct K/V admission, and FP32 state/numerator authority.

Parent gates retained in the bake environment:

```text
Stage11 active vendor adoption                 83/83 PASS
Vendor variable-row softmax                   100/100 PASS
Vendor mixed precision                         70/70 PASS
Vendor compact readback                        64/64 PASS
Generation-sealed Muon cache                   66/66 PASS
Muon backend surface rebind                    35/35 PASS
```

The immediate prior Stage12 retained-score validator is intentionally superseded because its required score-tile and transition-tape surfaces are the retirement target of this revision.

## Changed files

Overlay contains exactly twelve files:

```text
crates/burn_webgpu_backend/src/shaders/tensorcube_stage10_11_12_fused_streaming_attention_candidate.wgsl
crates/burn_webgpu_backend/src/shaders/tensorcube_stage10_texture_k_candidate.wgsl
crates/burn_webgpu_backend/src/tensorcube_stage10_texture_k_live_shadow.rs
crates/burn_webgpu_backend/src/tensorcube_stage11_online_softmax_merge.rs
crates/burn_webgpu_backend/src/tensorcube_stage12_weighted_value_accumulation.rs
crates/model_core/src/attention_interconnect_w5.rs
crates/model_core/src/attention_interconnect_w6.rs
crates/model_core/src/attention_interconnect_w7.rs
crates/orchestrator_local/src/bin/ash_attn_interconnect_w6_verification_gate.rs
tools/validate_ash_attn_tensorcube_stage10_11_12_fused_streaming_attention_no_probability_materialization_r1_static.py
vendor_fork_scaffold/burn-wgpu-local/src/shaders/variable_row_prereduced_softmax_merge.wgsl
vendor_fork_scaffold/burn-wgpu-local/src/variable_row_softmax.rs
```

Code ZIPs contain no Markdown and no `*.sha256` files.

## Evidence status

The bake environment has no Cargo/Rust/WGSL physical compile or GPU execution authority.

```text
STATIC_BAKED_READY
NO_LOCAL_RUST_COMPILE_CLAIM
NO_LOCAL_WGSL_COMPILE_CLAIM
PHYSICAL_W5_W6_W7_GPU_GATE_REQUIRED
NO_UNMEASURED_PERFORMANCE_CLAIM
```

User-local Cargo/WGPU output is final execution SSOT.

## Physical gate targets

```text
fused candidate WGSL compiles
vendor pre-reduced Stage11 shader compiles
fused candidate K texture read > 0
fused candidate V texture read > 0
retained score read = 0
transition read = 0
secondary candidate QK recompute = 0
candidate/oracle context mismatch = 0
nonfinite candidate state/context = 0
prior-write-order violations = 0
missing/duplicate final writes = 0
all-masked/inactive context violations = 0
full score matrix allocation = 0
probability matrix allocation = 0
```

## Performance receipt targets

This revision removes score-tile/tape global traffic but can increase fused-kernel register/workgroup pressure. Physical promotion must compare previous retained-score bytes, previous transition-tape bytes, fused candidate GPU time, prior Stage12 candidate GPU time, candidate K/V read bytes, workgroup/register spill evidence when available, GPU memory high-water, and end-to-end W5->W7 latency.

No speedup percentage is sealed before those receipts exist.

## Non-goals

```text
No FP16/BF16 fused QKV adoption yet
No half running state
No half weighted-V numerator
No oracle retirement
No W5/W6 preflight retirement yet
No cross-layer attention batching
No dynamic kernel autotuner
No checkpoint schema mutation
No automatic performance promotion
```

## Next optimization line

```text
ASH-ATTN-TENSORCUBE-FUSED-STREAMING-ATTENTION-SUBGROUP-MATRIX-TILE-AND-ADAPTIVE-WORKGROUP-R2

ASH-ATTN-TENSORCUBE-FUSED-STREAMING-ATTENTION-FP16-BF16-QKV-STORAGE-FP32-STATE-ACCUMULATION-R2
```

## Promotion seal

```text
PROMOTE_ASH_ATTN_TENSORCUBE_STAGE10_11_12_FUSED_STREAMING_ATTENTION_NO_PROBABILITY_MATERIALIZATION_R1

ACTUAL_FUSED_OUTPUT_CANDIDATE
FUSED_CANDIDATE_QK_SINGLE_PASS
SCORE_REGISTER_WORKGROUP_LIFETIME
NO_RETAINED_SCORE_TILE_ALLOCATION
NO_RETAINED_SCORE_TILE_TRANSPORT
NO_RETAINED_SCORE_TILE_READ
NO_STAGE11_TRANSITION_TAPE_ALLOCATION
NO_STAGE11_TRANSITION_TAPE_TRANSPORT
NO_STAGE11_TRANSITION_TAPE_READ
NO_FULL_SCORE_MATRIX
NO_PROBABILITY_MATRIX
DIRECT_Q_READ
DIRECT_K_TEXTURE_READ
DIRECT_V_TEXTURE_READ
FP32_RUNNING_MAX
FP32_RUNNING_DENOMINATOR
FP32_WEIGHTED_V_NUMERATOR
SHARED_ALPHA_BETA_STATE_NUMERATOR_RECURRENCE
FP32_FINAL_NORMALIZATION
CANONICAL_CHUNK_ORDER
EXPLICIT_CAUSAL_ADMISSION
GQA_MAPPING_PRESERVED
FUSED_CANDIDATE_GLOBAL_STATE_AUTHORITY
INDEPENDENT_RAW_QKV_ORACLE_PRESERVED
CANDIDATE_ORACLE_CONTEXT_VERIFY_PRESERVED
CALLER_OWNED_CHUNK_ENCODER
NO_FUSED_PRIMITIVE_SUBMIT
NO_FUSED_PRIMITIVE_READBACK
NO_FUSED_PRIMITIVE_BLOCKING_POLL
NO_SYSTEM_WIDE_QK_ONCE_CLAIM_WHILE_VERIFICATION_ORACLES_REMAIN
NO_AUTOMATIC_PERFORMANCE_PROMOTION
SEALED
```