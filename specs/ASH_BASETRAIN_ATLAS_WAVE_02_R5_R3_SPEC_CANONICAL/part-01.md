    pub rope_scaling: String,
    pub rms_epsilon_bits: u64,

    pub embedding_shape: Vec<u64>,
    pub input_norm_shape: Vec<u64>,
    pub q_projection_shape: Vec<u64>,
    pub k_projection_shape: Vec<u64>,
    pub v_projection_shape: Vec<u64>,

    pub selected_layer: u32,
    pub geometry_digest: String,
}
```

## 4.1 Profile enum

```rust
pub enum BaseTrainAtlasWave02R5GeometryProfileKind {
    SyntheticMhaFixture,
    ProductionCandidate,
}
```

R5-R3 physical admission permits only:

```text
SyntheticMhaFixture
```

`ProductionCandidate` may be parsed and audited but cannot receive PASS.

## 4.2 Derived projection dimensions

```text
q_projection_dim  = num_attention_heads × head_dim
kv_projection_dim = num_key_value_heads × head_dim
```

Required checked arithmetic:

```text
q_projection_dim multiplication overflow  -> HOLD
kv_projection_dim multiplication overflow -> HOLD
```

Required model consistency:

```text
hidden_size == q_projection_dim
num_key_value_heads <= num_attention_heads
num_attention_heads % num_key_value_heads == 0
```

Forbidden requirement:

```text
hidden_size == kv_projection_dim
```

That equality may happen for MHA, but it is not a generic model invariant.

## 4.3 Geometry digest

The geometry digest must include, in canonical order:

```text
authority version
profile kind
checkpoint identity digest
checkpoint header digest
model spec ID
model spec digest
model spec source digest
all model dimensions
q projection dimension
kv projection dimension
RoPE kind
theta bits
scaling
RMS epsilon bits
all expected tensor keys and shapes
selected layer
```

The digest must not include mutable runtime buffer identities or batch contents.

---

# 5. Header and ModelSpec reconciliation

## 5.1 Required tensor keys

For selected layer `L`, the physical header must contain:

```text
model.embed_tokens.weight
model.layers.L.input_layernorm.weight
model.layers.L.self_attn.q_proj.weight
model.layers.L.self_attn.k_proj.weight
model.layers.L.self_attn.v_proj.weight
```

R5-R3 canonical fixture uses `L = 0`.

## 5.2 Expected tensor shapes

Assuming Safetensors projection layout `[out_features, in_features]`:

```text
embedding  [vocab_size, hidden_size]
input RMS  [hidden_size]
Q weight   [q_projection_dim, hidden_size]
K weight   [kv_projection_dim, hidden_size]
V weight   [kv_projection_dim, hidden_size]
```

For the current synthetic MHA fixture:

```text
vocab_size          32
hidden_size          8
num_heads            2
num_kv_heads         2
head_dim              4
q_projection_dim      8
kv_projection_dim     8

embedding  [32, 8]
RMS         [8]
Q           [8, 8]
K           [8, 8]
V           [8, 8]
```

The fact that Q, K and V happen to share `[8, 8]` does not authorize a common generic assertion.

Each projection must be validated against its separately derived expected shape.

## 5.3 Reconciliation algorithm

Required order:

```text
1. Load canonical ModelSpec bytes.
2. Compute ModelSpec source digest.
3. Deserialize ModelSpec.
4. Run validate_spec_consistency().
5. Compute canonical ModelSpec semantic digest.
6. Verify checkpoint identity receipt.
7. Verify Safetensors header receipt.
8. Resolve exact required tensor entries by key.
9. Derive q_projection_dim and kv_projection_dim from ModelSpec.
10. Compare each header shape to its independently derived expected shape.
11. Verify selected layer is within num_layers.
12. Seal ModelGeometryAuthority.
```

No Params object may be created before step 12 succeeds.

## 5.4 Header limitations

The header must not be claimed to prove:

```text
num_attention_heads
num_key_value_heads
RoPE theta
RoPE pairing convention
RMS epsilon
model architecture family
```

It proves only the tensor facts physically present in the header.

The binding receipt proves that those tensor facts are compatible with the named ModelSpec.

---

# 6. ModelSpec digest authority

The existing AW-00 transaction already carries a `model_spec_digest` through sequence and RoPE authority.

R5-R3 must require exact parity among:

```text
AW-00 transaction model_spec_id
AW-00 transaction model_spec_digest
R5-R3 loaded ModelSpec ID
R5-R3 recomputed ModelSpec digest
ModelGeometryAuthority model_spec_id
ModelGeometryAuthority model_spec_digest
```

Any mismatch is terminal HOLD.

Forbidden:

```text
constructing a new fixture ModelSpec after AW-00 transaction creation
using one ModelSpec for AW-00 and another for AW-02
recomputing theta from a different config source
