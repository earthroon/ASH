# ASH-BASETRAIN-ATLAS-WAVE-02-R6

## Headwise Training Adapter Live Adoption

Status: SPEC RELEASE rev.2

Direct physical parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R5-R7`

### Scope

This patch binds the real selected-layer Q, K and V buffers physically produced by R5-R7 to the existing Headwise Atlas dispatcher on the same WebGPU device and queue. It promotes the Headwise selected-layer context to training output authority only after full-surface parity against the R5-R7 canonical GPU oracle.

The patch does not admit OProj, MLP, next-layer execution, TensorCube output commit, loss, backward, optimizer, checkpoint writing or full-model execution.

### Required authority chain

```text
R5-R6 checkpoint tensor-set authority
  -> R5-R7 real checkpoint selected-layer forward
  -> live NeoX Q/K and actual V buffer leases
  -> existing BufferAtlasV1 Headwise dispatcher
  -> FullPrefill causal route
  -> Headwise context candidate
  -> finite guard
  -> R5-R7 oracle parity
  -> Headwise selected-layer training context authority
  -> TensorCube candidate handoff preservation
```

### Live input SSOT

```rust
BaseTrainAtlasWave02R6LiveQkvLeaseSet
BaseTrainAtlasWave02R6TrainingInvocationIdentity
BaseTrainAtlasWave02R6HeadwiseTrainingAdapterAuthority
BaseTrainAtlasWave02R6HeadwiseContextAuthority
BaseTrainAtlasWave02R6TensorCubeHandoffAuthority
```

R5-R7 live Q/K/V buffers are the only admissible source. Independent Q, K or V file paths, host values, replacement buffers, Burn tensor fabrication, host round trips and reprojection are forbidden.

Required zero counters:

```text
burn_tensor_fabrication_count  0
qkv_replacement_buffer_count   0
qkv_copy_count                 0
qkv_map_async_count            0
qkv_host_read_bytes            0
qkv_host_upload_bytes          0
qkv_reprojection_count         0
rope_recompute_count           0
```

### Physical layout closure

R5-R7 physically stores Q/K/V as `BQHD`. Existing Headwise production kernels historically addressed Q/K/V as `BHQD`. R6 therefore requires an explicit layout-aware raw lease route.

```text
input layout   BQHD
output layout  BHQD
```

The existing 96-byte Headwise parameter ABI carries the input-layout discriminator. Production kernels must select the BQHD input address formula without copying or relabelling bytes. Headwise output remains BHQD.

### Geometry

```text
Q  [batch, seq_q,  32, 64]
K  [batch, seq_kv,  4, 64]
V  [batch, seq_kv,  4, 64]
query_heads_per_kv_head  8
rope_layout              NeoXHalfSplit
```

K/V physical expansion to 32 heads is forbidden. R6 consumes the already rotated NeoX Q/K produced by R5-R7 and must not execute RoPE again.

### Existing executor requirement

The imported Headwise physical executor manifest must prove:

```text
active_executor             BufferAtlasV1
active_executor_readiness   production_bound
production_dispatch         allowed
route_authority_mutation    0
output_authority_mutation   0
```

`KvTextureGqa4V1` may remain registered as a candidate but must not execute or gain authority in R6.

### Training invocation boundary

R6 uses `FullPrefill` causal semantics and a training invocation identity. It must not fabricate a decode session or mutate KV cache state.

```text
decode_session_creation_count  0
kv_cache_mutation_count        0
sampler_invocation_count       0
token_commit_count             0
```

Rev.2 physical gate is pinned to full-valid canonical-position rows because the existing Headwise dispatcher does not yet bind row-valid lengths into the production kernel. Padding-mask authority is therefore not admitted by R6.

### Full-surface parity

The gate compares the complete selected Headwise context against the R5-R7 canonical GPU oracle across every admitted batch, query position, query head and lane.

Required result:

```text
mismatch_count              0
first_mismatch_index        none
valid_row_mismatch_count    0
invalid_row_nonzero_count   0
finite_guard                PASS
```

The parity readback is gate validation only. It does not mutate the runtime writer or create a production decode output route.

### TensorCube handoff preservation

R6 publishes candidate lineage for:

```text
NeoX Q
NeoX K
actual V
Headwise context
R5-R7 oracle context
row-valid lengths
position IDs
```

But TensorCube authority remains closed:

```text
tensorcube_candidate_visible          true
tensorcube_forward_authority          false
tensorcube_output_commit_authorized   false
tensorcube_dispatch_count              0
tensorcube_route_mutation_count        0
tensorcube_writer_promotion_count      0
```

### Forbidden expansion

```text
OProj dispatch                  0
attention residual             0
post-attention RMSNorm         0
MLP dispatch                   0
next-layer dispatch            0
full-model dispatch            0
loss dispatch                  0
backward dispatch              0
optimizer step                 0
checkpoint write               0
production admission           BLOCKED
proof ledger                   HOLD
full-model admission           BLOCKED
```

### Required gate

```text
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_headwise_training_adapter_live_gate.rs
specs/cli/ash_basetrain_atlas_wave_02_r6.args
workspace/runtime/basetrain/atlas_wave/02/r6/headwise-training-adapter-live-v1
```

### PASS token

```text
PASS_ASH_BASETRAIN_ATLAS_WAVE_02_R6_HEADWISE_TRAINING_ADAPTER_LIVE_ADOPTION_R5_R7_REAL_CHECKPOINT_RESIDENT_LEASE_CONSUMPTION_EXISTING_DISPATCHER_SAME_DEVICE_BINDING_PRODUCTION_CANDIDATE_Q_K_V_LIVE_INPUT_NEOX_ROTATED_Q_K_ADOPTION_HEADWISE_CONTEXT_OUTPUT_R5_R7_ORACLE_HEADWISE_FULL_SURFACE_PARITY_TENSORCUBE_HANDOFF_AUTHORITY_PRESERVATION_NO_OPROJ_MLP_FULL_MODEL_ADMISSION_PRODUCTION_BLOCKED_PROOF_LEDGER_HOLD_SEALED
```

The full byte-exact rev.2 specification is sealed by SHA-256:

```text
1e172d750dbc28f5a4aa73b3a9b8fb2c3b85aaa48e650fce34bad6b08ad229ef
```
