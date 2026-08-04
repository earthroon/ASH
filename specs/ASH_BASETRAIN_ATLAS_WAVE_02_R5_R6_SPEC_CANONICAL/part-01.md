It is not sufficient to prove:

```text
all transformer layers exist
attention output tensors exist
post-attention norms exist
MLP tensors exist
final norm exists
LM head representation is valid
no unexpected trainable tensor exists
```

## 2.4 A planned full-model registry exists but is not payload truth

The existing planned registry generator describes the Llama-family logical key set:

```text
model.embed_tokens.weight

for every layer L:
  model.layers.L.input_layernorm.weight
  model.layers.L.self_attn.q_proj.weight
  model.layers.L.self_attn.k_proj.weight
  model.layers.L.self_attn.v_proj.weight
  model.layers.L.self_attn.o_proj.weight
  model.layers.L.post_attention_layernorm.weight
  model.layers.L.mlp.gate_proj.weight
  model.layers.L.mlp.up_proj.weight
  model.layers.L.mlp.down_proj.weight

model.norm.weight
lm_head.weight
```

It also defines the correct major shapes for Q, K, V, O and MLP tensors.

However, that registry explicitly describes planned logical keys without payload trust. R5-R6 may reuse its canonical schema rules, but it must not import its planned entries as proof that physical tensors exist.

## 2.5 The current R5-R5 config snapshot is deliberately incomplete

The reviewed R5-R5 RoPE snapshot contains fields needed for the RoPE convention gate, including:

```text
architecture
model_type
hidden_size
query heads
KV heads
head_dim
max positions
rope_theta
rope_scaling
```

It does not contain every field required for a full tensor inventory, including at least:

```text
num_hidden_layers
intermediate_size
vocab_size
rms_norm_eps
tie_word_embeddings
attention bias policy
MLP bias policy
primary torch dtype or equivalent checkpoint dtype policy
```

R5-R6 must use a production-candidate configuration source complete enough to derive the full expected schema. It must not silently fill missing fields from the minimal R5-R5 RoPE snapshot.

---

# 3. Authority model

R5-R6 introduces one immutable authority:

```rust
pub struct BaseTrainAtlasWave02R5CheckpointTensorSetAuthority {
    pub authority_version: String,
    pub patch_id: String,

    pub parent_r5_r5_manifest_digest: String,
    pub checkpoint_root_kind: CheckpointRootKind,
    pub checkpoint_root_path: String,
    pub checkpoint_set_id: String,

    pub config_source_path: String,
    pub config_source_sha256: String,
    pub model_spec_digest: String,
    pub geometry_authority_digest: String,
    pub external_rope_authority_digest: String,

    pub index_source: Option<CheckpointIndexAuthority>,
    pub shards: Vec<CheckpointShardAuthority>,
    pub tensors: Vec<CheckpointTensorAuthority>,
    pub canonical_roles: Vec<CanonicalTensorRoleBinding>,

    pub physical_tensor_count: u32,
    pub logical_role_count: u32,
    pub total_parameter_count: u64,
    pub total_tensor_payload_bytes: u64,
    pub tied_role_count: u32,

    pub synthetic_tensor_count: u32,
    pub unresolved_tensor_count: u32,
    pub duplicate_tensor_key_count: u32,
    pub missing_required_role_count: u32,
    pub unexpected_trainable_tensor_count: u32,

    pub forward_authority: bool,
    pub gpu_upload_authority: bool,
    pub production_admitted: bool,
    pub proof_ledger_admitted: bool,
    pub r6_admitted: bool,

    pub authority_digest: String,
}
```

The authority is the single source of truth for:

```text
which checkpoint set is being discussed
which files physically constitute that set
which tensor key lives in which shard
which byte range stores each tensor
which canonical model role each key satisfies
which dtype and shape each role physically has
how tied logical roles map to physical tensors
```

It is not the authority for:

```text
GPU residency
forward execution
layer scheduling
activation lifetime
loss
backward
optimizer
checkpoint writes
```

---

# 4. Checkpoint root modes

R5-R6 supports exactly two explicit root modes.

## 4.1 SingleSafetensors

```text
checkpoint root kind = SingleSafetensors
index present        = false
shard count          = 1
```

The single file is still represented as one shard authority. No synthetic index file is generated.

## 4.2 IndexedSafetensors

```text
checkpoint root kind = IndexedSafetensors
index present        = true
shard count          >= 1
```

The index must contain a `weight_map` object mapping every tensor key to exactly one shard filename.

## 4.3 Forbidden ambiguity

The gate must reject:

```text
both single-file and index paths supplied
neither supplied
index mode with an empty weight_map
single-file mode with multiple payload candidates
implicit directory scanning as authority
newest-file selection
lexicographic fallback selection
network download or remote resolution
```

Directory scanning may be used only to detect unreferenced or foreign files. It must not choose the authoritative set.

---

# 5. Config authority

## 5.1 Required source

R5-R6 consumes one pinned local production-candidate config file.

The config bytes must be hashed before semantic parsing.

Required receipt fields:

```text
source path
source byte count
source SHA-256
JSON parse status
model family
architecture
model type
model identifier
```

## 5.2 Minimum semantic fields

The configuration or the canonical ModelSpec derived from it must explicitly provide:

```text
vocab_size
hidden_size
