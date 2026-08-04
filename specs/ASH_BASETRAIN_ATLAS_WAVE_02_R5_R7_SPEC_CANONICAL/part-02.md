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

Implementation rules:

```text
selected_layer must be explicit
selected_layer < num_hidden_layers
selected_layer must match every selected tensor key
resident group ID must derive from selected_layer
receipt must record selected_layer
no hidden default
no clamping
no fallback
```

Canonical group ID:

```text
aw02.layer{selected_layer}.prefill_bundle
```

---

# 8. Physical payload read authority

R5-R7 must not open arbitrary tensor paths supplied independently by the user or CLI.

The loader receives only:

```text
R5-R6 checkpoint root
R5-R6 shard authority
R5-R6 tensor authority
```

For each selected tensor:

1. Resolve the shard path under the sealed checkpoint root.
2. Verify the resolved path remains under that root.
3. Verify shard byte count and SHA-256 against R5-R6.
4. Seek to the exact `absolute_file_start`.
5. Read exactly `payload_bytes`.
6. Reject short read, extra range read, overflow or range escape.
7. Decode only that tensor range.

The forward path must not:

```text
scan the checkpoint directory
reparse the full index
recompute tensor names heuristically
open an unlisted shard
read the whole checkpoint into RAM
read LM head, O projection or MLP tensors
mutate checkpoint bytes
```

---

# 9. BF16 and F16 decode authority

## 9.1 Accepted source dtypes

R5-R7 accepts only the dtype physically sealed by R5-R6:

```text
BF16
F16
```

F32 is not part of the R5-R7 half-decode promotion gate. A separate counter-profile may prove F32 later, but it must not silently bypass this patch's BF16/F16 proof obligation.

All five selected tensors must use one consistent physical dtype unless a later explicit per-role mixed-dtype authority is introduced.

## 9.2 Canonical runtime representation

The current R5 shaders consume `array<f32>`. Therefore R5-R7's canonical resident representation is:

```text
IEEE-754 little-endian f32
```

Decode rules:

```text
BF16 -> f32 by exact high-16-bit expansion
F16  -> f32 by IEEE-754 binary16 conversion
NaN payloads remain NaN and are rejected by finite-value admission
Inf values are rejected
negative zero is preserved through decode receipt
subnormal values follow one pinned software conversion rule
```

The decode rule ID must be versioned, for example:

```text
ash.aw02.r5.r7.decode.bf16_to_f32.v1
ash.aw02.r5.r7.decode.f16_to_f32.ieee_rne.v1
```

## 9.3 Atlas parallel streaming-wave decode and upload

The loader must decode in bounded pages and publish them through an explicit Atlas Parallel Streaming Wave authority. A single serial host expansion or a whole-tensor `Vec<f32>` is forbidden.

Rev.2 canonical vocabulary upload profile:

```text
source page bytes          4,194,304
pages per wave            4
parallel decode workers   4
wave readback policy      every wave
resident representation   f32
atlas allocation count    1
