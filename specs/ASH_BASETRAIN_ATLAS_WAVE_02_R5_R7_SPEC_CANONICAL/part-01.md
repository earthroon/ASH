  -> consumed by embedding, RMSNorm and Q/K/V projection
  -> rotated with the R5-R5 external NeoX RoPE convention
  -> consumed by the R5-R4 GQA mapping
  -> compared against a CPU-f64 reference from the same raw bytes
  -> published as a selected-surface authority
```

R5-R7 must not claim that the full transformer block, all 22 layers, Headwise, TensorCube, logits, loss, backward, optimizer or durable training checkpointing are proven.

The core distinction is:

```text
real checkpoint inventory is complete
  != real checkpoint forward is physically consumed

one selected attention surface passes
  != full model passes
```

---

# 1. Confirmed parent state

R5-R7 imports physical evidence from the following chain.

```text
R5-R3  Model Geometry Authority
R5-R4  GQA Physical Geometry Authority
R5-R5  External RoPE Convention Authority
R5-R6  Production Candidate Checkpoint Tensor-Set Authority
```

The parent state currently proves the following production-candidate geometry.

```text
model_type                  llama
architecture                LlamaForCausalLM
vocab_size                  48259
hidden_size                 2048
intermediate_size           5632
num_hidden_layers           22
num_attention_heads         32
num_key_value_heads         4
head_dim                    64
q_projection_dim            2048
kv_projection_dim           256
q_heads_per_kv_head         8
max_position_embeddings     2048
rope_theta                  10000
rope_scaling                null
attention_bias             false
tie_word_embeddings         false
rms_norm_eps                1e-5
```

The parent checkpoint has physically confirmed tensor shapes including:

```text
model.embed_tokens.weight                         [48259, 2048]
model.layers.0.input_layernorm.weight              [2048]
model.layers.0.self_attn.q_proj.weight             [2048, 2048]
model.layers.0.self_attn.k_proj.weight             [256, 2048]
model.layers.0.self_attn.v_proj.weight             [256, 2048]
lm_head.weight                                    [48259, 2048]
```

R5-R7 must import the exact R5-R6 `checkpointSetDigest`, `inventoryDigest`, `authorityDigest`, config digest, shard CAS digest and tensor identity digests. It must not rediscover the checkpoint by scanning a directory.

---

# 2. Current-source findings that constrain R5-R7

## 2.1 Existing R5 staged prefill already defines the intended selected surface

The current backend has a staged path with these stages:

```text
embedding
RMSNorm
Q/K/V projection
RoPE
attention oracle
```

It returns:

```text
embedding
norm
q
k
v
q_rope
k_rope
context
```

It also returns live Q, K, V and context buffers with runtime holder, device epoch, queue epoch, source weight generation and atlas residency generation.

This is the correct surface boundary for R5-R7.

## 2.2 Existing R5 resident views already carry useful lineage

`BaseTrainAtlasWave01BackendResidentTensorView` and `BaseTrainAtlasWave02R5ResidentWeights` already expose:

```text
tensor_key
shape
group_id
runtime_holder_id
source_weight_generation
atlas_residency_generation
device_epoch
queue_epoch
slot_index
buffer
byte_offset
byte_len
```

R5-R7 must extend this lineage back to:

```text
R5-R6 checkpointSetDigest
R5-R6 tensorIdentityDigest
source shard SHA-256
source header SHA-256
source absolute byte range
source physical dtype
decode authority digest
resident upload digest
```

## 2.3 Current full-shape R5 RoPE is not externally admissible

The existing full-shape shader pairs lanes as:

```text
(0,1), (2,3), ...
```

That is adjacent interleaving.

R5-R5 physically proved that this checkpoint uses:

```text
NeoXHalfSplit
```

For head dimension 64, the external pairing is:

```text
(0,32), (1,33), ... (31,63)
```

Therefore the existing `base_train_atlas_wave_02_r5_rope.wgsl` must not be admitted unchanged in R5-R7.

R5-R7 must either:

```text
replace the full-shape live RoPE kernel with a NeoXHalfSplit kernel
```

or:

```text
introduce an explicit versioned full-shape R5-R7 NeoX kernel
```

The known-vector R5-R5 fixture kernel alone is insufficient because it is pinned to a small 4-head/2-KV-head fixture.

## 2.4 Current resident group ID is layer-0 hardcoded

The existing R5 resident validation expects:

```text
aw02.layer0.prefill_bundle
```

R5-R7 must replace this literal with:

```text
aw02.layer{selected_layer}.prefill_bundle
```

The physical admission fixture for rev.1 remains pinned to selected layer `0`, but the authority implementation must not silently clamp or rewrite other layer indices to zero.

## 2.5 Existing shaders consume f32 resident weights

The current embedding, RMSNorm and Q/K/V WGSL bindings use:

```wgsl
array<f32>
```

R5-R7 therefore needs an explicit physical-source-to-runtime decode authority:

```text
F16 or BF16 checkpoint payload
  -> canonical f32 resident representation
```

This conversion must be part of the receipt chain. It must not be treated as an invisible loader detail.

---

# 3. Scope

R5-R7 includes only:

```text
one selected transformer layer index
one bounded token fixture
actual embedding tensor consumption
actual selected-layer input RMSNorm tensor consumption
actual selected-layer Q/K/V tensor consumption
F16 or BF16 payload decode to canonical f32 residency
one same-device resident lease set
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
