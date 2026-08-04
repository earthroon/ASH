  [kv_projection_dim, hidden_size]

layer.L.attention.v
  model.layers.L.self_attn.v_proj.weight
  [kv_projection_dim, hidden_size]

layer.L.attention.o
  model.layers.L.self_attn.o_proj.weight
  [hidden_size, q_projection_dim]

layer.L.post_attention_norm
  model.layers.L.post_attention_layernorm.weight
  [hidden_size]

layer.L.mlp.gate
  model.layers.L.mlp.gate_proj.weight
  [intermediate_size, hidden_size]

layer.L.mlp.up
  model.layers.L.mlp.up_proj.weight
  [intermediate_size, hidden_size]

layer.L.mlp.down
  model.layers.L.mlp.down_proj.weight
  [hidden_size, intermediate_size]
```

For the current geometry where `q_projection_dim == hidden_size`, O projection becomes `[hidden_size, hidden_size]`. The formula must remain authority-derived rather than replaced by the incidental equality.

## 9.3 Bias policy

When the ModelSpec declares no attention or MLP biases, the following are forbidden:

```text
q_proj.bias
k_proj.bias
v_proj.bias
o_proj.bias
gate_proj.bias
up_proj.bias
down_proj.bias
```

When bias is declared, the schema must explicitly add the corresponding roles and shapes. Header presence must never decide architecture bias policy by itself.

---

# 10. Canonical name resolution

## 10.1 Resolver result

```rust
pub struct CanonicalTensorRoleBinding {
    pub canonical_role_id: String,
    pub physical_tensor_id: String,
    pub source_tensor_key: String,
    pub resolver_version: String,
    pub resolver_rule_id: String,
    pub layer_index: Option<u32>,
    pub tied_alias: bool,
    pub pass: bool,
}
```

## 10.2 Resolution policy

The default target profile requires exact Hugging Face Llama-style keys.

The resolver may use a versioned explicit alias table only when the selected architecture record authorizes that alias set.

Forbidden resolution methods:

```text
suffix-only guessing
case-insensitive guessing
edit-distance matching
first compatible shape wins
layer-number clamping
unknown prefix stripping
regex fallback without a registry rule ID
```

## 10.3 Ambiguity

One physical tensor key must resolve to at most one non-tied canonical role.

One non-tied canonical role must resolve to exactly one physical tensor.

Any many-to-one mapping requires an explicit tied-role rule.

---

# 11. Tied embedding and LM-head policy

`tie_word_embeddings` must be explicit in config authority.

## 11.1 Untied mode

```text
tie_word_embeddings = false
```

Required physical tensors:

```text
model.embed_tokens.weight
lm_head.weight
```

Both must have valid shapes. They may contain equal bytes, but equality does not convert them into a tied representation.

## 11.2 Tied mode

```text
tie_word_embeddings = true
```

The authority may represent `global.lm_head` as a logical alias of `global.embedding` without creating a synthetic payload tensor.

The allowed physical representation must be selected explicitly by the architecture record:

```text
embedding-only physical payload with logical LM-head alias
or
both keys physically present with an explicit exact-byte-equivalence policy
```

R5-R6 must record:

```text
physical tensor count
logical role count
tied role count
tied source physical tensor ID
```

`No Synthetic Tensor Admission` prohibits creating new bytes. It does not prohibit a sealed logical alias to an existing physical tensor.

---

# 12. Tensor count and layer continuity

For a bias-free untied Llama-family model with `L` layers:

```text
per-layer physical tensors = 9
global physical tensors    = 3
expected total             = 9L + 3
```

For `L = 22`:

```text
expected physical tensor count = 201
```

This numerical count is admitted only when the production config explicitly establishes:

```text
num_hidden_layers = 22
bias policy = none
tie_word_embeddings = false
```

R5-R6 must not infer those facts from the number 201.

Layer continuity checks:

```text
minimum layer index = 0
maximum layer index = num_hidden_layers - 1
every index appears
no negative or malformed index
no duplicate canonical role within a layer
no tensor with layer index >= num_hidden_layers
```

---

# 13. Dtype closure

## 13.1 Physical dtype

Every dtype is taken from the physical header.

Admitted payload dtypes for this patch:

```text
F16
BF16
F32
```

No host conversion is performed.

## 13.2 Policy convergence

The config or ModelSpec must define the admitted checkpoint dtype policy.

Examples of admissible policies:

```text
all trainable weights BF16
all trainable weights F16
explicit per-role mixed dtype table
```

A mixed physical dtype set without an explicit role policy is rejected.

## 13.3 Byte length

For every tensor:

```text
element_count = checked_product(shape)
payload_bytes = element_count × dtype_width
relative_end - relative_start == payload_bytes
absolute_end - absolute_start == payload_bytes
```

Every multiplication and offset addition must use checked arithmetic.

---

# 14. Range and coverage closure

Within each shard:

```text
all ranges are non-empty
all ranges begin at or after the data section
all ranges end within the file
all ranges are pairwise non-overlapping
header-relative and absolute ranges agree
weight_map owner agrees with header owner
```

R5-R6 records:

```text
mapped payload bytes
unmapped payload bytes
range overlap count
range out-of-bounds count
