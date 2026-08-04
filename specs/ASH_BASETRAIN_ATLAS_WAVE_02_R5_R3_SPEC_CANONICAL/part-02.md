accepting matching dimensions with a mismatching ModelSpec digest
```

For the fixture gate, AW-00 transaction construction and checkpoint generation must both consume the same immutable `Aw02R5FixtureProfileV1` and the same derived ModelSpec bytes.

---

# 7. Params becomes a derived transport

## 7.1 Builder-only construction

External struct-literal construction of `BaseTrainAtlasWave02R5Params` is forbidden in the R5-R3 gate and runtime path.

Required constructor:

```rust
impl BaseTrainAtlasWave02R5Params {
    pub fn derive(
        geometry: &BaseTrainAtlasWave02R5ModelGeometryAuthority,
        batch: &BaseBatchCpu,
        sequence: &BaseTrainSequenceAuthorityReceipt,
        flags: u32,
    ) -> Result<Self>;
}
```

The fields may remain public only if ABI tooling requires it, but all admitted production and physical-gate callsites must use `derive()`.

## 7.2 Field sources

| Params field | Sole authority |
|---|---|
| `batch_size` | `BaseBatchCpu.batch_size` |
| `seq_len` | `BaseBatchCpu.seq_len` and sequence receipt parity |
| `vocab_size` | ModelGeometryAuthority |
| `hidden_size` | ModelGeometryAuthority |
| `num_heads` | ModelGeometryAuthority |
| `num_kv_heads` | ModelGeometryAuthority |
| `head_dim` | ModelGeometryAuthority |
| `selected_layer` | ModelGeometryAuthority |
| `rope_theta` | ModelGeometryAuthority, checked f64-to-f32 conversion |
| `rms_epsilon` | ModelGeometryAuthority, checked f64-to-f32 conversion |
| `attention_scale` | derived as `1 / sqrt(head_dim)` |
| `flags` | explicit ABI policy input only |

No caller may separately provide model geometry fields.

## 7.3 Checked floating conversion

`ModelSpec` stores RoPE theta and RMS epsilon as `f64`; the GPU Params ABI currently stores `f32`.

Required checks:

```text
source f64 finite
source f64 positive
converted f32 finite
converted f32 positive
round-trip or explicit conversion-error receipt recorded
```

The receipt must include both source bits and bound f32 bits.

R5-R3 does not authorize silent clamping.

## 7.4 Attention scale

The attention scale must be derived:

```text
attention_scale = 1 / sqrt(head_dim)
```

The literal `0.5` is forbidden outside expected-value assertions for the fixture where `head_dim == 4`.

## 7.5 Generic validation

`BaseTrainAtlasWave02R5Params::validate()` must require:

```text
batch_size > 0
seq_len > 0
vocab_size > 0
hidden_size > 0
num_heads > 0
num_kv_heads > 0
head_dim > 0 and even
hidden_size == num_heads × head_dim
num_kv_heads <= num_heads
num_heads % num_kv_heads == 0
selected_layer < num_layers, validated by geometry builder
finite positive theta
finite positive RMS epsilon
finite positive attention scale
checked tensor element products
ABI byte size and alignment
```

It must not require:

```text
hidden_size == num_kv_heads × head_dim
selected_layer == 0 as a generic invariant
```

Fixture-only admission may separately require selected layer 0 and MHA.

---

# 8. Resident tensor validation

## 8.1 Geometry-bound validation

Required signature:

```rust
pub fn validate(
    &self,
    geometry: &BaseTrainAtlasWave02R5ModelGeometryAuthority,
) -> Result<()>;
```

Validation against Params alone is insufficient because Params is a transport object and does not carry source digests.

## 8.2 Per-tensor shape checks

```text
embedding.shape == geometry.embedding_shape
rms.shape       == geometry.input_norm_shape
q.shape         == geometry.q_projection_shape
k.shape         == geometry.k_projection_shape
v.shape         == geometry.v_projection_shape
```

A shared Q/K/V loop comparing all three against one shape is forbidden.

## 8.3 Lineage checks

All resident views must match the authority receipt on:

```text
checkpoint identity digest through joined plan
header digest through joined plan
source weight generation
atlas residency generation
runtime holder ID
device epoch
queue epoch
group ID
selected-layer tensor keys
```

The geometry digest must be included in the resident-view admission receipt.

## 8.4 Layout orientation

R5-R3 explicitly defines checkpoint projection layout as:

```text
[out_features, in_features]
```

Any checkpoint using a different physical orientation requires an explicit conversion plan and is outside R5-R3.

No implicit transpose is admitted.

---

# 9. Atlas plan derivation

The fixture atlas plan must derive logical counts and byte lengths from the authoritative shapes.

For dtype width `W`:

```text
logical_element_count = product(shape)
