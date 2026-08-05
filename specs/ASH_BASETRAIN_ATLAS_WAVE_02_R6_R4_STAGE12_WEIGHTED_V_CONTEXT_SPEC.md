# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R4

## Stage12 Atlas Parallel Streaming Weighted-V Context

> Patch ID: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R4`  
> Build revision: `stage12-atlas-parallel-streaming-weighted-v-bhqd-v1`  
> Direct parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R3-C4`  
> Parent required state: physical PASS  
> Selected-layer writer after PASS: `R6HeadwiseTrainingAdapter`  
> Production admission: `BLOCKED`  
> Proof ledger: `HOLD`

## 0. SSOT

R6-R4 executes the physically passing R6-R3-C4 chain exactly once in the same process, consumes the live frozen Stage11 candidate/oracle global max, exp-sum and admitted-count state plus live RoPE-applied BQHD Q/K, BQHD V and retained rgba32float K/V texture chunks, reconstructs causal weights without materializing score or probability matrices, accumulates and normalizes BHQD weighted-V context, proves the texture candidate against an independent raw-QKV oracle and the authoritative R6 Headwise full surface on GPU, retains the TensorCube context as a non-authoritative candidate, and grants no writer, OProj, MLP, next-layer, production or proof-ledger promotion authority.

## 1. Authorized route

```text
R6-R3-C4 local manifest lineage proof
  -> same-process R6-R3-C4 execution exactly once
  -> frozen candidate/oracle global softmax state
  -> canonical Stage12 chunk replay plan
  -> candidate K/V texture weighted-V accumulation
  -> independent raw-QKV oracle weighted-V accumulation
  -> frozen exp-sum normalization
  -> candidate/oracle BHQD context
  -> candidate-oracle full-surface parity
  -> candidate-Headwise full-surface parity
  -> independent row/write/layout invariants
  -> 256-byte compact status only
  -> retained non-authoritative context candidate handoff
```

The prior R6-R3 manifest is lineage evidence only. It does not own or reconstruct live GPU buffers.

## 2. Numerical contract

For each query token `q`, query head `h`, admitted key `k` and output dimension `d`:

```text
kv_head(h) = floor(h / 8)
score(q,h,k) = dot(Q_rope[q,h,:], K_rope[k,kv_head(h),:]) * 0.125
weight(q,h,k) = exp(score(q,h,k) - global_max(q,h))
numerator(h,q,d) = sum_k weight(q,h,k) * V[k,kv_head(h),d]
context(h,q,d) = numerator(h,q,d) / global_exp_sum(q,h)
```

The output context layout is BHQD:

```text
context_index = ((query_head * seq_q + query_token) * head_dim) + dimension
```

Input Q/K/V layout remains BQHD. Hidden transpose, layout relabeling or use of the R5-R7 BQHD oracle as a BHQD surface is forbidden.

## 3. Fixed physical profile

```text
batch_size = 1
query_heads = 32
kv_heads = 4
q_heads_per_kv = 8
head_dim = 64
qk_scale = 0.125
expected_subgroup_size = 32
query_tile_rows = 16
K/V texture format = rgba32float
K/V texture view = 2d-array
Stage11 global-state record bytes = 16
context element bytes = 4
row-classification record bytes = 4
compact status bytes = 256
```

## 4. Candidate and oracle independence

Candidate route:

```text
Q source = live BQHD Q buffer
K source = retained rgba32float K texture
V source = retained rgba32float V texture
global state = R6-R3 candidate global state
```

Oracle route:

```text
Q source = live BQHD Q buffer
K source = live raw BQHD K buffer
V source = live raw BQHD V buffer
global state = R6-R3 oracle global state
textureLoad count = 0
```

Candidate raw K/V reads are forbidden. Oracle K/V texture reads are forbidden.

## 5. Canonical chunk schedule

```text
for replay_step_ordinal in ascending order:
    validate chunk ordinal, token range, KV block count and texture identities
    dispatch one candidate weighted-V wave across [query_head, query_token]
    dispatch one oracle weighted-V wave across [query_head, query_token]
    increment exactly one row write count for every global record
```

Expected counters:

```text
candidate_stage12_dispatch_count = canonical_chunk_count
oracle_stage12_dispatch_count = canonical_chunk_count
candidate_context_write_count = global_record_count * canonical_chunk_count
oracle_context_write_count = global_record_count * canonical_chunk_count
normalize_dispatch_count = 1
candidate_oracle_parity_dispatch_count = 1
headwise_parity_dispatch_count = 1
invariant_dispatch_count = 1
known_vector_dispatch_count = 1
```

## 6. GPU output ABI

```text
context ABI = ash.basetrain.atlas-wave.02.r6-r4.context.bhqd.f32.v1
status ABI = ash.basetrain.atlas-wave.02.r6-r4.stage12-status.v1
row ABI = ash.basetrain.atlas-wave.02.r6-r4.context-row-flags.v1
```

The compact status contains 64 u32 words, exactly 256 bytes. Production payload readback is prohibited.

Required PASS values:

```text
candidate_oracle_mismatch_count = 0
candidate_headwise_mismatch_count = 0
non_finite_context_count = 0
denominator_contract_violation_count = 0
missing_final_write_count = 0
duplicate_final_write_count = 0
v_generation_mismatch_count = 0
row_classification_mismatch_count = 0
layout_mismatch_count = 0
compared_candidate_oracle_scalar_count = context_scalar_count
compared_candidate_headwise_scalar_count = context_scalar_count
valid_row_count + all_masked_row_count = global_record_count
```

## 7. State ownership

- R6-R3 owns the frozen global state and retained source leases until R6-R4 submission completion.
- `burn_webgpu_backend` owns Stage12 pipelines, GPU buffers, compact verification and the live context handoff.
- `base_train` owns replay-plan identity, parent import, invocation seal and Stage12 authority.
- the executable gate owns same-process lineage reconstruction and receipt publication.
- JSON owns identity, counters and digests only. JSON never owns GPU payloads.

The retained R6-R4 context handoff is visible for review but not authoritative as the selected-layer writer.

## 8. Forbidden substitutions

```text
Stage10 or Stage11 rerun after the R6-R3 live handoff
CPU score, softmax, weighted-V or parity calculation
full score matrix allocation
full probability matrix allocation
K/V texture-to-buffer rehydration
Stage11 global-state payload readback
Stage12 context payload readback
serialized context reconstruction
hidden BQHD/BHQD transpose
Headwise selected-layer writer mutation
TensorCube context commit
TensorCube output commit
OProj
MLP
next-layer execution
production promotion
proof-ledger promotion
```

## 9. Required implementation files

```text
crates/burn_webgpu_backend/src/base_train_atlas_wave_02_r6_r4_stage12_weighted_v.rs
crates/burn_webgpu_backend/src/shaders/base_train_atlas_wave_02_r6_r4_stage12_texture_weighted_v.wgsl
crates/burn_webgpu_backend/src/shaders/base_train_atlas_wave_02_r6_r4_stage12_raw_qkv_oracle.wgsl
crates/burn_webgpu_backend/src/shaders/base_train_atlas_wave_02_r6_r4_stage12_context_normalize.wgsl
crates/burn_webgpu_backend/src/shaders/base_train_atlas_wave_02_r6_r4_stage12_candidate_oracle_parity.wgsl
crates/burn_webgpu_backend/src/shaders/base_train_atlas_wave_02_r6_r4_stage12_headwise_parity.wgsl
crates/burn_webgpu_backend/src/shaders/base_train_atlas_wave_02_r6_r4_stage12_invariant_verify.wgsl
crates/burn_webgpu_backend/src/shaders/base_train_atlas_wave_02_r6_r4_stage12_known_vector_fixture.wgsl
crates/base_train/src/base_train_atlas_wave_02_r6_r4_stage12_authority.rs
crates/base_train/src/base_train_atlas_wave_02_r6_r4_stage12_replay_plan.rs
crates/base_train/src/base_train_atlas_wave_02_r6_r4_frozen_context_handoff.rs
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r4_stage12_weighted_v_context_gate.rs
specs/cli/ash_basetrain_atlas_wave_02_r6_r4.args
```

## 10. Negative counters

```text
full_score_matrix_allocation_count = 0
full_probability_matrix_allocation_count = 0
texture_to_buffer_rehydration_count = 0
global_state_payload_readback_count = 0
context_payload_readback_count = 0
compact_readback_count = 1
compact_readback_bytes = 256
source_lease_early_drop_count = 0
texture_early_drop_count = 0
output_early_publish_count = 0
headwise_writer_mutation_count = 0
route_mutation_count = 0
oproj_dispatch_count = 0
mlp_dispatch_count = 0
next_layer_dispatch_count = 0
tensorcube_output_commit_count = 0
production_promotion_attempt_count = 0
```

## 11. Response file and output

Response file:

```text
specs/cli/ash_basetrain_atlas_wave_02_r6_r4.args
```

Required parent manifest:

```text
workspace/runtime/basetrain/atlas_wave/02/r6_r3/stage11-atlas-parallel-streaming-wave-v2/ash_basetrain_atlas_wave_02_r6_r3_local_manifest.json
```

Output directory:

```text
workspace/runtime/basetrain/atlas_wave/02/r6_r4/stage12-weighted-v-context-v1
```

## 12. Build and physical gate

```powershell
cargo check `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r4_stage12_weighted_v_context_gate
```

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r4_stage12_weighted_v_context_gate `
  -- "@specs/cli/ash_basetrain_atlas_wave_02_r6_r4.args"
```

## 13. PASS token

```text
PASS_ASH_BASETRAIN_ATLAS_WAVE_02_R6_R4_TENSORCUBE_STAGE12_ATLAS_PARALLEL_STREAMING_WEIGHTED_V_CONTEXT_R6_R3_C4_FROZEN_GLOBAL_SOFTMAX_STATE_SAME_PROCESS_CONSUMPTION_ACTUAL_Q_BQHD_K_V_RGBA32FLOAT_TEXTURE_CANDIDATE_RAW_Q_K_V_ORACLE_CANONICAL_CHUNK_WAVE_CAUSAL_SCORE_RECONSTRUCTION_GLOBAL_MAX_EXP_SUM_NORMALIZED_NUMERATOR_BHQD_CONTEXT_FULL_SURFACE_CANDIDATE_ORACLE_AND_HEADWISE_PARITY_V_GENERATION_IDENTITY_ROW_CLASSIFICATION_COMPACT_STATUS_ONLY_NO_FULL_SCORE_PROBABILITY_MATRIX_TEXTURE_REHYDRATION_GLOBAL_STATE_CONTEXT_PAYLOAD_READBACK_HEADWISE_WRITER_MUTATION_TENSORCUBE_CONTEXT_COMMIT_OPROJ_MLP_NEXT_LAYER_PRODUCTION_PROMOTION_PROOF_LEDGER_HOLD_SEALED
```
