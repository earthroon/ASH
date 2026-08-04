full-shape NeoX RoPE for actual Q and K
actual 32-query-head / 4-KV-head GQA attention oracle
CPU-f64 selected-surface reference
full readback for the bounded selected surface
physical parity receipts
negative counterfactuals
```

R5-R7 excludes:

```text
attention output projection
attention residual addition
post-attention RMSNorm
MLP gate/up/down projection
SwiGLU
layer output authority
multiple transformer layers
final RMSNorm
LM head
logits
loss
backward
optimizer
Headwise output authority
TensorCube output authority
production inference admission
production training admission
```

---

# 4. New SSOTs

## 4.1 Selected-layer forward authority

```rust
pub struct BaseTrainAtlasWave02R5R7SelectedLayerForwardAuthority {
    pub schema_version: u32,
    pub patch_id: String,
    pub build_revision: String,

    pub parent_r5_r6_manifest_digest: String,
    pub parent_r5_r6_checkpoint_set_digest: String,
    pub parent_r5_r6_inventory_digest: String,
    pub parent_r5_r6_authority_digest: String,

    pub parent_r5_r5_manifest_digest: String,
    pub parent_r5_r5_rope_authority_digest: String,
    pub pairing_layout: String,

    pub checkpoint_identity: String,
    pub selected_layer: u32,
    pub selected_surface_id: String,

    pub token_fixture_digest: String,
    pub geometry_digest: String,
    pub decode_authority_digest: String,
    pub lease_set_digest: String,
    pub gpu_execution_digest: String,
    pub cpu_f64_reference_digest: String,
    pub parity_receipt_digest: String,

    pub executed_layer_count: u32,
    pub headwise_dispatch_count: u32,
    pub tensorcube_dispatch_count: u32,
    pub o_projection_dispatch_count: u32,
    pub mlp_dispatch_count: u32,
    pub full_model_dispatch_count: u32,

    pub production_admission: String,
    pub proof_ledger_admission: String,
    pub r6_admission: String,
    pub full_model_admission: String,
    pub pass: bool,
    pub authority_digest: String,
}
```

## 4.2 Tensor decode authority

```rust
pub struct BaseTrainAtlasWave02R5R7TensorDecodeAuthority {
    pub checkpoint_set_digest: String,
    pub source_dtype: String,
    pub target_runtime_dtype: String,
    pub decode_rule_id: String,
    pub decode_chunk_bytes: u64,
    pub tensor_receipts: Vec<BaseTrainAtlasWave02R5R7TensorDecodeReceipt>,
    pub source_payload_bytes: u64,
    pub decoded_runtime_bytes: u64,
    pub host_full_tensor_materialization_count: u32,
    pub source_range_reopen_count: u32,
    pub pass: bool,
    pub authority_digest: String,
}
```

Each tensor receipt must bind:

```text
tensor key
canonical role
layer index
R5-R6 tensorIdentityDigest
shard ID
shard SHA-256
header SHA-256
absolute source range
source dtype
source element count
source payload byte count
decode rule ID
decoded f32 byte count
decoded f32 stream digest
chunk count
```

## 4.3 Resident tensor lease set

```rust
pub struct BaseTrainAtlasWave02R5R7ResidentTensorLeaseSet {
    pub checkpoint_set_digest: String,
    pub selected_layer: u32,
    pub group_id: String,
    pub runtime_holder_id: String,
    pub device_epoch: u64,
    pub queue_epoch: u64,
    pub source_weight_generation: u64,
    pub atlas_residency_generation: u64,
    pub slot_index: u32,
    pub leases: Vec<BaseTrainAtlasWave02R5R7ResidentTensorLease>,
    pub lease_acquire_count: u32,
    pub lease_release_count: u32,
    pub mixed_generation_count: u32,
    pub stale_lease_count: u32,
    pub checkpoint_reopen_during_forward_count: u32,
    pub weight_write_during_forward_count: u32,
    pub pass: bool,
    pub lease_set_digest: String,
}
```

Each lease binds the physical tensor to one resident buffer range:

```text
tensorIdentityDigest
source shard digest
source range
source dtype
decode digest
runtime buffer identity digest
runtime byte offset
runtime byte length
runtime representation f32
buffer usage
lease generation
```

The lease set, not the checkpoint path, is the only weight source accepted by the GPU forward function.

---

# 5. Parent authority import

R5-R7 must consume the R5-R6 local manifest and the R5-R6 checkpoint tensor-set authority receipt.

Required checks:

```text
R5-R6 pass              true
R5-R6 pass token        exact
productionAdmission     BLOCKED
proofLedgerAdmission    HOLD
r6Admission             BLOCKED
syntheticTensorCount    0
missingTensorCount      0
unexpectedTensorCount   0
shapeMismatchCount      0
dtypeMismatchCount      0
rangeGapCount           0
rangeOverlapCount       0
unmappedPayloadBytes    0
```

R5-R7 must also import the R5-R5 local manifest and require:

```text
R5-R5 pass              true
pairingLayout           NeoXHalfSplit
ropeThetaBits           exact match with R5-R6 config
model type              exact match
architecture            exact match
```

The gate must reject a parent manifest with a valid filename but mismatched content digest.

---

# 6. Selected-layer tensor set

For selected layer `L`, R5-R7 may consume exactly these five physical tensors:

```text
model.embed_tokens.weight
model.layers.L.input_layernorm.weight
model.layers.L.self_attn.q_proj.weight
model.layers.L.self_attn.k_proj.weight
model.layers.L.self_attn.v_proj.weight
```

Expected shapes derive only from R5-R6 config authority:

```text
embedding     [vocab_size, hidden_size]
input norm    [hidden_size]
Q             [num_attention_heads * head_dim, hidden_size]
K             [num_key_value_heads * head_dim, hidden_size]
V             [num_key_value_heads * head_dim, hidden_size]
```

For the current checkpoint:

```text
embedding     [48259, 2048]
input norm    [2048]
Q             [2048, 2048]
K             [256, 2048]
V             [256, 2048]
```

The gate must reject:

```text
shape-only tensor selection
suffix matching
case-fold matching
layer index clamping
layer index wraparound
fallback to layer 0
wrong checkpoint tensor with matching shape
planned registry entries without payload authority
```

---

# 7. Selected layer policy

The rev.1 physical admission fixture is pinned to:

```text
selected_layer = 0
```

This is a fixture policy, not a model limitation.

