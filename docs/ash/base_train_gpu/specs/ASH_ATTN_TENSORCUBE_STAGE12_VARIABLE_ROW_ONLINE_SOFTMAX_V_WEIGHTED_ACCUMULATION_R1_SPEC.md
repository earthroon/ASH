# ASH-ATTN-TENSORCUBE-STAGE12-VARIABLE-ROW-ONLINE-SOFTMAX-V-WEIGHTED-ACCUMULATION-R1

## Status

```text
Patch ID:
ASH-ATTN-TENSORCUBE-STAGE12-VARIABLE-ROW-ONLINE-SOFTMAX-V-WEIGHTED-ACCUMULATION-R1

Mode:
ACTUAL STAGE12 CANDIDATE BACKEND BINDING

Stage10 score authority:
existing TensorCube Stage10 candidate score computation

Stage11 softmax-state authority:
actual vendor-backed TensorCube Stage11 candidate_global_state

Stage12 candidate numerator authority:
Stage10 retained score tile + Stage11 transition tape + V texture

Stage12 oracle authority:
existing independent raw-Q/K/V replay oracle
```

## Parent SSOT

```text
ASH-ATTN-TENSORCUBE-STAGE11-VARIABLE-ROW-VENDOR-PRIMITIVE-ADOPTION-R1

ASH-BURN-VENDOR-VARIABLE-ROW-ONLINE-SOFTMAX-DESCRIPTOR-DISPATCH-AND-FP32-STATE-REDUCTION-R1

ASH-BURN-VENDOR-MIXED-PRECISION-TENSOR-PRIMITIVES-FP16-BF16-STORAGE-FP32-ACCUMULATION-R1

ASH-BURN-VENDOR-GPU-RESIDENT-VERIFICATION-COMPACT-READBACK-RECEIPT-ASYNC-STAGING-RING-AND-SUBMISSION-COALESCING-R1
```

## Central closure

The pre-existing TensorCube Stage12 already accumulated weighted V without materializing a full probability matrix, but its candidate path recomputed Q x K during the W7 replay pass.

This revision removes that candidate QK replay.

```text
Stage10 candidate QK score
        |
        +--> existing local max / exp-sum / count statistics
        |
        `--> retained chunk x q-tile score tile on GPU
                         |
                         v
Stage11 vendor pre-reduced merge
        |
        +--> candidate_global_state
        |
        `--> per-row/head/chunk prior-max -> merged-max transition tape
                         |
                         v
Stage12 candidate
retained score tile + transition tape + V texture
        |
        v
online FP32 weighted-V numerator rescale/accumulation
        |
        v
existing final denominator normalization
        |
        v
candidate attention context
```

The existing raw-Q/K/V Stage12 oracle remains independent and continues to recompute QK for verification. Candidate QK recomputation is zero; oracle QK recomputation is intentionally preserved.

## Stage10 retained score-tile surface

New retained score-tile ABI:

```text
ash.tensorcube.stage10.score-tile.qh-token.f32.v1
```

Stage10's existing candidate shader continues to compute the canonical scaled score using Q and K. In addition to the existing Stage10 statistics, each chunk / q-tile execution now writes the exact candidate score into a derived GPU-resident score tile:

```text
[active_query_row][query_head][chunk_local_token] -> f32 score
```

Masked or causally inadmissible positions retain the existing negative-infinity score representation. Stage10 numerical score semantics are not changed.

The score tile is a derived execution surface. It is not parameter, optimizer, checkpoint, or new semantic attention authority.

Stage10 receipts now bind:

```text
candidate_score_tile_buffer_digest
candidate_score_tile_element_count
candidate_score_tile_bytes
candidate_score_tile_abi
```

The score tile is transferred through W5 and W6 and retained by the Stage11 global-state handle until Stage12 replay consumes it.

## No monolithic full-score matrix

The retained surfaces are scoped per existing chunk x q-tile execution. This revision does not allocate one global Q x KV score matrix and does not materialize a probability matrix.

```text
full_score_matrix_allocation_count = 0
full_probability_matrix_allocation_count = 0
```

The retained score tiles increase GPU-resident transient storage and therefore require physical memory/performance receipts before any speedup claim.

## Stage11 transition tape

Stage12 online numerator recurrence needs the same maximum transition that Stage11 used when each chunk was merged.

New transition ABI:

```text
ash.tensorcube.stage11.transition.prior-max-merged-max-flags.v1
16 bytes / record
```

One transition record is produced per:

```text
chunk x q-tile x active query row x query head
```

Each record contains:

```text
prior running-max f32 bits
merged running-max f32 bits
prior/merged valid flags
canonical merge-step ordinal
```

The transition record is written by the same vendor pre-reduced Stage11 merge that writes the canonical candidate global softmax state. No second softmax state machine is introduced.

The Stage11 candidate backend revision is advanced to:

```text
ASH-ATTN-TENSORCUBE-STAGE11-VENDOR-PREREDUCED-ACTIVE-R1-STAGE12-TRANSITION-TAPE-R1
```

This prevents transition-tape-capable Stage11 output from being confused with the previous physical surface revision.

## Stage12 candidate backend

New candidate backend revision:

```text
ASH-ATTN-TENSORCUBE-STAGE12-SCORE-TILE-V-ONLINE-RESCALE-ACTIVE-R1
```

Pipeline identity now binds:

```text
candidate backend revision
Stage10 retained-score-tile ABI
Stage11 transition-record ABI
candidate WGSL digest
oracle WGSL digest
normalization/verification WGSL digest
```

The Stage12 candidate bind group consumes:

```text
binding 0: chunk params
binding 1: retained Stage10 score tile
binding 2: V texture
binding 3: Stage11 transition records
binding 4: FP32 candidate context numerator
binding 5: candidate chunk write counts
binding 6: candidate status lane
```

There is no Q buffer and no K buffer/texture in the candidate bind group.

## Online weighted-V recurrence

For one row/head chunk, Stage11 provides:

```text
m_prev   = prior running maximum
m_merged = running maximum after this chunk
```

The previous numerator is rescaled by:

```text
previous_scale = exp(m_prev - m_merged)
A_prev_scaled  = A_prev * previous_scale
```

The current chunk uses the retained Stage10 score directly:

```text
weight_i = exp(score_i - m_merged)
A_chunk  = sum_i weight_i * V_i
```

The candidate numerator becomes:

```text
A_next = A_prev_scaled + A_chunk
```

All numerator, exponent, V decode/read, multiplication, and accumulation in this R1 remain FP32.

On the first valid chunk, the previous numerator contribution is zero. If Stage11 reports no valid merged state, the candidate does not invent a softmax state.

## Canonical denominator finalization

Stage12 does not create an independent production denominator authority.

The existing Stage11 candidate global state remains the denominator authority. The existing Stage12 normalization/verification pass divides the candidate numerator by the Stage11 canonical denominator to produce the final candidate context.

```text
context = candidate_numerator / Stage11_candidate_denominator
```

Existing all-masked, inactive-row, finite-state, denominator, write-count, and candidate/oracle verification contracts are retained.

## Exact active-score and V admission

Stage10 already writes negative infinity for causally inadmissible score positions. The Stage12 candidate reads the retained score tile and skips entries with the exact masked-score bit representation.

Only an admitted score causes a V read and weighted contribution.

Inactive or causally masked score positions therefore do not contribute to the numerator.

## GQA / head mapping

The existing Stage12 GQA mapping remains:

```text
kv_head = query_head / gqa_group_size
```

This revision does not alter model head semantics or introduce a new GQA/MQA policy. It preserves the current TensorCube Stage12 contract.

## Candidate QK replay retirement

Candidate telemetry is explicitly sealed as:

```text
candidate_stage10_score_tile_read_count = candidate dispatch count
candidate_transition_record_read_count = candidate dispatch count
candidate_qk_recompute_count = 0
candidate_k_texture_read_count = 0
candidate_v_texture_read_count = candidate dispatch count
```

The W7 integration gate requires score-tile reads, transition-tape reads, and V direct reads to be non-zero while candidate QK recomputation and K-texture reads remain zero.

The old W7 `FUSED_SCORE_RECOMPUTE` authority token is retired.

New W7 build revision:

```text
W7-stage11-vendor-state-stage10-score-tile-stage12-online-v-rescale-r1
```

## Independent oracle preservation

The existing Stage12 raw-Q/K/V oracle is intentionally not converted to the retained-score-tile path.

It continues to:

```text
read Q
read raw K
recompute QK score
use Stage11 oracle global max
read raw V
accumulate oracle numerator
```

Therefore candidate/oracle parity remains independent evidence rather than comparing two executions of the same candidate implementation.

## GPU residency and readback boundary

Candidate Stage12 consumes:

```text
Stage10 retained score tile: GPU resident
Stage11 transition tape: GPU resident
Stage11 candidate global state: GPU resident
V texture: GPU resident
```

There is no Stage10-score payload D2H -> Stage12 H2D loop.

The existing Stage12 final gate may still perform diagnostic/gate context readback when explicitly enabled. This revision does not claim elimination of all Stage12 final-gate readback. It eliminates candidate QK replay and does not add a new candidate payload readback.

## Submission boundary

Stage12 chunk encoding remains caller-owned. The candidate WGSL does not own:

```text
queue.submit
MAP_READ
PollType::Wait
```

Stage12 finalization retains its existing pipeline-level submission/completion authority.

## Replay-state integrity

`begin_replay` verifies:

```text
Stage11 transition record size == 16
transition record count > 0
retained score tile count == chunk_count x q_tile_count
```

Each Stage12 chunk verifies exact:

```text
chunk ordinal
q-tile index
token start / count
active query rows
query-head count
score-tile element/byte contract
transition-record count
transition-record buffer range
```

Replay descriptors remain unique and canonical chunk write order remains guarded by the existing write-count contract.

## Static validation

New validator:

```text
tools/validate_ash_attn_tensorcube_stage12_variable_row_online_softmax_v_weighted_accumulation_r1_static.py

140/140 PASS
```

The validator verifies the complete Stage10 -> Stage11 -> Stage12 surface, including:

```text
Stage10 score-tile production and ABI
W5/W6 score-tile lease transport
Stage11 transition-tape production
Stage11 transition ABI/revision
Stage12 score-tile/transition/V candidate binding
previous-numerator rescale
current weighted-V accumulation
zero candidate QK replay
zero candidate K-texture read
no candidate Q/K binding
no probability materialization
independent raw-QKV oracle preservation
W7 zero-QK-replay admission gate
```

Parent static gates retained in the bake environment:

```text
Stage11 active vendor adoption                 83/83 PASS
Vendor variable-row softmax                   100/100 PASS
Vendor mixed precision                         70/70 PASS
Vendor compact readback                        64/64 PASS
Generation-sealed Muon cache                   66/66 PASS
Muon backend surface rebind                    35/35 PASS

FFN multi-slot                                  PASS
FFN persistent resource slab                   PASS
FFN timestamp/resource-churn guard              PASS
FFN physical-perf harness static               PASS
FFN fused production                           PASS
GPU70K G45                                     42/42 PASS
GPU70K G27                                     35/35 PASS
Atlas/HOTPATH                                  56/56 PASS
HOTPATH allocation                             26/26 PASS
```

## Bake files

Overlay contains exactly twelve files:

```text
crates/burn_webgpu_backend/src/shaders/tensorcube_stage10_texture_k_candidate.wgsl
crates/burn_webgpu_backend/src/shaders/tensorcube_stage12_score_tile_v_candidate.wgsl
crates/burn_webgpu_backend/src/tensorcube_stage10_texture_k_live_shadow.rs
crates/burn_webgpu_backend/src/tensorcube_stage11_online_softmax_merge.rs
crates/burn_webgpu_backend/src/tensorcube_stage12_weighted_value_accumulation.rs
crates/model_core/src/attention_interconnect_w5.rs
crates/model_core/src/attention_interconnect_w6.rs
crates/model_core/src/attention_interconnect_w7.rs
crates/orchestrator_local/src/bin/ash_attn_interconnect_w6_verification_gate.rs
tools/validate_ash_attn_tensorcube_stage12_variable_row_online_softmax_v_weighted_accumulation_r1_static.py
vendor_fork_scaffold/burn-wgpu-local/src/shaders/variable_row_prereduced_softmax_merge.wgsl
vendor_fork_scaffold/burn-wgpu-local/src/variable_row_softmax.rs
```

Code ZIPs contain no Markdown and no `*.sha256` files.

## Evidence status

The bake environment does not contain Cargo, rustc, rustfmt, or a physical GPU execution path.

Therefore:

```text
STATIC_BAKED_READY
NO_LOCAL_RUST_COMPILE_CLAIM
NO_LOCAL_WGSL_COMPILE_CLAIM
PHYSICAL_W6_W7_GPU_GATE_REQUIRED
NO_UNMEASURED_PERFORMANCE_CLAIM
```

User-local Cargo and physical GPU results remain the final execution SSOT.

## Physical promotion gate

The physical run must establish at minimum:

```text
Stage10 score-tile WGSL compiles
Stage11 transition-tape vendor WGSL compiles
Stage12 score-tile/V candidate WGSL compiles

Stage11 candidate_oracle_mismatch_count = 0
Stage12 candidate_oracle_mismatch_count = 0

candidate_stage10_score_tile_read_count > 0
candidate_transition_record_read_count > 0
candidate_v_texture_read_count > 0
candidate_qk_recompute_count = 0
candidate_k_texture_read_count = 0

candidate prior-write-order violation = 0
candidate nonfinite score = 0
candidate nonfinite value = 0
candidate nonfinite numerator = 0
candidate duplicate-context-write = 0

denominator contract violations = 0
all-masked nonzero context = 0
inactive nonzero context = 0
missing final write = 0
duplicate final write = 0

full_score_matrix_allocation_count = 0
full_probability_matrix_allocation_count = 0
```

Performance receipts should compare the previous Stage12 QK replay path against the retained-score-tile path and must include:

```text
Stage10 score-tile retained bytes
removed Stage12 candidate Q/K read bytes
Stage12 candidate GPU time
oracle GPU time
GPU memory high-water delta
score-tile lifetime
transition-tape bytes
end-to-end W5->W7 latency
```

No speedup percentage is promoted before those physical receipts exist.

## Non-goals

```text
No Stage10 QK algorithm mutation
No Stage11 softmax formula mutation
No probability matrix materialization
No monolithic full-score matrix
No FP16/BF16 Stage12 numerator yet
No half Stage11 state
No half final attention context
No FlashAttention mega-kernel fusion
No Stage10/11/12 single-pass fusion
No oracle retirement
No automatic performance promotion
```

## Next optimization line

After physical parity and performance evidence close this R1, the natural next step is:

```text
ASH-ATTN-TENSORCUBE-STAGE10-11-12-FUSED-STREAMING-ATTENTION-NO-PROBABILITY-MATERIALIZATION-R1
```

That later revision may remove the separate retained-score-tile replay lifetime by consuming score -> softmax transition -> V contribution within one fused streaming tile lifetime. This R1 deliberately keeps the stage boundaries visible so correctness and performance deltas remain attributable.

## Promotion seal

```text
PROMOTE_ASH_ATTN_TENSORCUBE_STAGE12_VARIABLE_ROW_ONLINE_SOFTMAX_V_WEIGHTED_ACCUMULATION_R1

ACTUAL_STAGE12_CANDIDATE_BINDING

STAGE10_RETAINED_SCORE_TILE_GPU_AUTHORITY
NO_STAGE12_CANDIDATE_QK_RECOMPUTE
ZERO_CANDIDATE_K_TEXTURE_READ
DIRECT_CANDIDATE_V_TEXTURE_READ

STAGE11_VENDOR_GLOBAL_STATE_DIRECT_BINDING
STAGE11_PRIOR_MAX_TO_MERGED_MAX_TRANSITION_TAPE

FP32_PREVIOUS_NUMERATOR_RESCALE
FP32_CURRENT_BLOCK_WEIGHTED_V_ACCUMULATION
FP32_FINAL_DENOMINATOR_NORMALIZATION

CANONICAL_CHUNK_WRITE_ORDER
EXACT_SCORE_TILE_GEOMETRY_GUARD
EXACT_TRANSITION_RANGE_GUARD

NO_FULL_SCORE_MATRIX
NO_FULL_PROBABILITY_MATRIX
NO_GPU_CPU_GPU_SCORE_LOOP

INDEPENDENT_RAW_QKV_ORACLE_PRESERVED
CANDIDATE_ORACLE_CONTEXT_VERIFY_PRESERVED

NO_STAGE10_FORMULA_MUTATION
NO_STAGE11_SOFTMAX_FORMULA_MUTATION
NO_FLASH_ATTENTION_FUSION_YET
NO_AUTOMATIC_PERFORMANCE_CLAIM

SEALED
```