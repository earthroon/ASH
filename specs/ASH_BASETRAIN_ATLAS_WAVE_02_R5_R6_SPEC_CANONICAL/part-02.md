num_hidden_layers
num_attention_heads
num_key_value_heads
head_dim or a uniquely derivable equivalent
intermediate_size
max_position_embeddings
rms_norm_eps
rope_theta
rope_scaling
tie_word_embeddings
attention bias policy
MLP bias policy
expected checkpoint dtype policy
```

Missing fields must not be replaced by:

```text
hard-coded TinyLlama literals
fixture profile values
CLI values
header-shape guesses
planned registry defaults
```

## 5.3 Config-to-parent convergence

The production config must converge exactly with the imported R5 authorities for:

```text
hidden_size
num_attention_heads
num_key_value_heads
head_dim
q_projection_dim
kv_projection_dim
rope_theta bits
rope scaling
pairing convention record
model family
architecture
```

A mismatch blocks the candidate even when every shard digest is valid.

---

# 6. Index authority

## 6.1 Structure

```rust
pub struct CheckpointIndexAuthority {
    pub index_path: String,
    pub index_sha256: String,
    pub index_byte_count: u64,
    pub metadata_digest: Option<String>,
    pub weight_map_entry_count: u32,
    pub referenced_shards: Vec<String>,
    pub weight_map_digest: String,
}
```

## 6.2 Exact weight-map rules

For indexed mode:

```text
every weight_map key is non-empty
every shard filename is a relative normalized path
no absolute path
no parent traversal
no duplicate key after normalization
no duplicate shard identity after canonical path resolution
every referenced shard exists inside the checkpoint root
every physical header tensor is represented by weight_map
no weight_map key is absent from its referenced shard header
no tensor key exists in more than one shard header
```

## 6.3 Index metadata

Index metadata may report a total size, but that value is a witness only.

The authoritative payload byte count is derived from the verified physical shards and headers.

A metadata size mismatch must be recorded and rejected under production-candidate policy.

---

# 7. Shard CAS authority

```rust
pub struct CheckpointShardAuthority {
    pub shard_id: String,
    pub normalized_relative_path: String,
    pub file_byte_count: u64,
    pub file_sha256: String,

    pub safetensors_header_len: u64,
    pub safetensors_header_sha256: String,
    pub data_section_start: u64,
    pub header_tensor_count: u32,

    pub first_payload_offset: u64,
    pub last_payload_offset: u64,
    pub mapped_payload_bytes: u64,
    pub unmapped_payload_bytes: u64,

    pub whole_file_retained_in_memory: bool,
    pub full_payload_deserialized: bool,
    pub pass: bool,
}
```

## 7.1 CAS identity

A shard identity is:

```text
sha256(file bytes) + exact file byte count
```

Filename alone is never a shard identity.

## 7.2 Streaming requirement

Shard hashing and tensor-range verification must use bounded streaming buffers.

Required policy:

```text
whole_file_retained_in_memory          false
full_payload_deserialized              false
typed_full_tensor_materialization      0
host dtype conversion                   0
checkpoint mutation                     0
```

## 7.3 Range domain

Tensor data offsets remain relative to that shard's Safetensors data section.

Each tensor authority must store both:

```text
relative data offset [start,end)
absolute file offset [data_section_start+start, data_section_start+end)
```

No range from one shard may be numerically compared as if it belonged to another shard.

---

# 8. Physical tensor authority

```rust
pub struct CheckpointTensorAuthority {
    pub physical_tensor_id: String,
    pub tensor_key: String,
    pub shard_id: String,
    pub shard_sha256: String,
    pub header_sha256: String,

    pub dtype: String,
    pub dtype_width_bytes: u32,
    pub shape: Vec<u64>,
    pub element_count: u64,
    pub payload_byte_count: u64,

    pub relative_data_offset_start: u64,
    pub relative_data_offset_end: u64,
    pub absolute_file_offset_start: u64,
    pub absolute_file_offset_end: u64,

    pub canonical_role_id: String,
    pub layer_index: Option<u32>,
    pub family: String,
    pub role: String,

    pub synthetic: bool,
    pub payload_materialized: bool,
    pub gpu_uploaded: bool,
    pub forward_consumed: bool,

    pub tensor_identity_digest: String,
}
```

The tensor identity digest must include at least:

```text
checkpoint set ID
shard digest
header digest
tensor key
dtype
shape
relative offsets
absolute offsets
canonical role
```

It must not include a mutable filesystem timestamp.

---

# 9. Canonical tensor schema

R5-R6 derives the expected logical schema from the production ModelSpec and one versioned Llama-family schema registry.

## 9.1 Global roles

```text
global.embedding
  key   model.embed_tokens.weight
  shape [vocab_size, hidden_size]

global.final_norm
  key   model.norm.weight
  shape [hidden_size]

global.lm_head
  key   lm_head.weight
  shape [vocab_size, hidden_size]
```

`global.lm_head` physical representation is governed by `tie_word_embeddings`.

## 9.2 Per-layer roles

For every layer `L` in `[0, num_hidden_layers)`:

```text
layer.L.input_norm
  model.layers.L.input_layernorm.weight
  [hidden_size]

layer.L.attention.q
  model.layers.L.self_attn.q_proj.weight
  [q_projection_dim, hidden_size]

layer.L.attention.k
  model.layers.L.self_attn.k_proj.weight
