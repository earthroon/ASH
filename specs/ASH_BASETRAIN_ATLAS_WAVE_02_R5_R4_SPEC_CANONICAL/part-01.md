The current common base is therefore invalid for K when `kv_projection_dim < hidden_size`.

## 2.6 Attention uses modulo mapping

The current attention oracle selects:

```wgsl
let kv_head = head_index % params.num_kv_heads;
```

For the required R5-R4 profile:

```text
query heads = 4
KV heads    = 2
```

modulo produces:

```text
Q0 -> KV0
Q1 -> KV1
Q2 -> KV0
Q3 -> KV1
```

Canonical contiguous GQA grouping requires:

```text
Q0 -> KV0
Q1 -> KV0
Q2 -> KV1
Q3 -> KV1
```

The correct mapping is:

```text
q_heads_per_kv = num_attention_heads / num_key_value_heads
kv_head = query_head / q_heads_per_kv
```

No modulo, clamp, minimum, fallback, or wraparound is admitted.

## 2.7 CPU reference mirrors the same MHA assumptions

The current CPU reference:

```text
requires Q/K/V weight length == hidden_size × hidden_size
allocates Q/K/V as token_count × hidden_size
rotates K over num_attention_heads
maps kv_head = query_head % num_key_value_heads
indexes K/V through the hidden-width index helper
```

GPU and CPU can therefore agree on the same wrong GQA interpretation.

R5-R4 must change both implementations and add an independent wrong-mapping counterfactual.

## 2.8 Readback and stage receipt cardinality are common-width

The current backend uses one `element_bytes` value for:

```text
Q
K
V
Q_RoPE
K_RoPE
context
```

The QKV stage receipt also emits all output identities with the same byte count.

This is factually incorrect for GQA and must be separated.

---

# 3. R5-R4 physical fixture profile

R5-R4 introduces one explicit synthetic GQA profile.

## 3.1 Required profile

```text
profile kind             SyntheticGqaFixture
vocab_size               32
hidden_size              16
num_layers               1
num_attention_heads      4
num_key_value_heads      2
head_dim                  4
q_projection_dim         16
kv_projection_dim        8
q_heads_per_kv           2
intermediate_size        32
max_position_embeddings  16
rope_theta               10000.0
rope_kind                rope
rope_scaling             none
rms_epsilon              1e-5
batch_size               2
seq_len                   4
selected_layer           0
production               false
```

Required inequalities:

```text
num_attention_heads != num_key_value_heads
q_projection_dim != kv_projection_dim
hidden_size != kv_projection_dim
```

Required exact relations:

```text
hidden_size == q_projection_dim
q_projection_dim == num_attention_heads × head_dim
kv_projection_dim == num_key_value_heads × head_dim
q_heads_per_kv == num_attention_heads / num_key_value_heads
q_heads_per_kv == 2
```

## 3.2 Profile isolation

The existing R5-R3 MHA fixture remains historical and must not be silently changed.

The R5-R4 fixture must be selected through an explicit constructor or profile ID, such as:

```rust
Aw02R5FixtureProfileV1::gqa_physical_v1()
```

or an equivalent dedicated type.

The gate must record:

```text
profileKind = SyntheticGqaFixture
profileVersion = ash.aw02.r5.r4.synthetic_gqa_fixture.v1
production = false
mhaEqualityIncidental = false
```

A default constructor must not choose between MHA and GQA based on environment variables.

---

# 4. Single geometry authority

R5-R4 continues to use `BaseTrainAtlasWave02R5ModelGeometryAuthority` as the geometry SSOT.

The authority must contain or derive:

```text
num_attention_heads
num_key_value_heads
head_dim
q_projection_dim
kv_projection_dim
q_heads_per_kv
Q/K/V checkpoint shapes
selected layer
geometry digest
```

`q_heads_per_kv` must be derived from the sealed authority.

```rust
q_heads_per_kv = num_attention_heads
    .checked_div(num_key_value_heads)
```

Required validation:

```text
num_key_value_heads > 0
num_attention_heads % num_key_value_heads == 0
q_heads_per_kv > 0
q_heads_per_kv × num_key_value_heads == num_attention_heads
```

The mapping group size must not be independently authored in Params, WGSL constants, CLI arguments, or fixture receipts.

---

# 5. Scalar-count and byte-count authority

R5-R4 defines distinct logical scalar domains.

Let:

```text
T  = batch_size × seq_len
H  = hidden_size
QW = q_projection_dim
KW = kv_projection_dim
D  = head_dim
QH = num_attention_heads
KH = num_key_value_heads
```

Required counts:

```text
hidden_scalar_count  = T × H
q_scalar_count       = T × QW
kv_scalar_count      = T × KW
context_scalar_count = T × H
q_pair_count         = T × QH × (D / 2)
kv_pair_count        = T × KH × (D / 2)
```

Required byte counts for `f32`:

```text
hidden_bytes  = hidden_scalar_count × 4
q_bytes       = q_scalar_count × 4
kv_bytes      = kv_scalar_count × 4
context_bytes = context_scalar_count × 4
```

For the canonical R5-R4 fixture:

```text
T            = 8
hidden bytes = 512
Q bytes      = 512
K bytes      = 256
V bytes      = 256
Q_RoPE bytes = 512
K_RoPE bytes = 256
context bytes= 512
```

All products must use checked arithmetic before allocation or dispatch.

A common `element_bytes` variable may remain only for hidden-width surfaces. It must not be used for K, V, or K_RoPE.

---

# 6. Q/K/V projection execution

## 6.1 Semantic output domains

```text
Q output shape = [batch, seq, q_projection_dim]
K output shape = [batch, seq, kv_projection_dim]
V output shape = [batch, seq, kv_projection_dim]
```

The output shapes must not be represented as three hidden-width arrays with an unused tail.

## 6.2 Admitted fused dispatch

