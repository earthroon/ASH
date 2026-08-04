The current `RopeSection` must be extended without silently defaulting legacy specs.

Admitted shape:

```rust
pub struct RopeSection {
    #[serde(rename = "type")]
    pub kind: String,
    pub theta: f64,
    pub scaling: String,

    #[serde(default)]
    pub pairing_layout: Option<String>,
    #[serde(default)]
    pub rotary_dim: Option<usize>,
    #[serde(default)]
    pub convention_record_id: Option<String>,
}
```

Parsing compatibility and admission authority are separate.

```text
legacy file parses                         allowed
legacy pairing_layout missing              R5-R5 admission denied
legacy rotary_dim missing                  R5-R5 admission denied
legacy convention_record_id missing        R5-R5 admission denied
```

No deserializer default may convert missing pairing data to `NeoXHalfSplit` or `InterleavedAdjacent`.

The external config importer and registry resolver populate these fields explicitly before sealing the R5-R5 ModelSpec snapshot.

---

# 8. External config binding

## 8.1 Accepted source fields

The external config reader extracts, when present:

```text
architectures
model_type
hidden_size
num_attention_heads
num_key_value_heads
head_dim
max_position_embeddings
rope_theta
rope_parameters.rope_theta
rope_scaling
rope_parameters.rope_type
```

## 8.2 Theta alias policy

Legacy and current schemas may expose theta at different paths.

Admitted resolution:

```text
legacy_theta = root.rope_theta
nested_theta = root.rope_parameters.rope_theta
```

Rules:

```text
neither present       fail
one present           use exact parsed f64
both present equal    accept and record both paths
both present unequal  fail
```

No `10000.0` fallback is permitted.

## 8.3 Head dimension derivation

Admitted resolution:

```text
explicit head_dim present
  -> use explicit

head_dim absent
  -> derive hidden_size / num_attention_heads
```

Derived head dimension requires exact divisibility.

The receipt records:

```text
headDimSource = explicit | derived
```

## 8.4 Scaling normalization

For R5-R5 only, the following normalize to `none`:

```text
missing
null
"none"
{"rope_type":"default"} with no additional active scaling parameters
```

The raw JSON fragment digest remains recorded.

Any other scaling object is rejected.

## 8.5 Model-family resolution

The registry lookup key includes:

```text
model_type
architectures sorted
registry version
```

The TinyLlama/Llama fixture resolves to:

```text
pairing_layout       NeoXHalfSplit
rotary_dim           head_dim
frequency formula    theta_pow_neg_2i_over_rotary_dim
apply Q              true
apply K              true
apply V              false
```

Unknown architecture keys fail closed.

---

# 9. Versioned convention registry

R5-R5 introduces a local immutable registry file, for example:

```text
specs/fixtures/ash_basetrain_atlas_wave_02_r5_r5_rope_convention_registry_v1.json
```

Required record shape:

```json
{
  "registryVersion": "ash.rope.convention_registry.v1",
  "records": [
    {
      "recordId": "llama.default_rope.neox_half_split.v1",
      "modelType": "llama",
      "architectures": ["LlamaForCausalLM"],
      "ropeKind": "rope",
      "acceptedScaling": ["none"],
      "pairingLayout": "NeoXHalfSplit",
      "rotaryDimPolicy": "HeadDim",
      "frequencyFormulaId": "ash.rope.frequency.theta_pow_neg_2i_over_rotary_dim.v1",
      "signConventionId": "ash.rope.rotation.xa_cos_minus_xb_sin__xa_sin_plus_xb_cos.v1",
      "externalSourceRevision": "PINNED",
      "externalSourcePath": "src/transformers/models/llama/modeling_llama.py",
      "externalSourceEvidenceSha256": "REQUIRED"
    }
  ]
}
```

## 9.1 Registry ownership

The registry is the only writer of pairing layout from an external model-family declaration.

The following may not independently choose pairing:

```text
WGSL
CPU reference
CLI
fixture constructor
ModelSpec deserializer
checkpoint loader
backend Params
orchestrator gate
```

## 9.2 Registry mutation control

The gate records:

```text
registry byte digest
selected record digest
record count
selected record index
selected record ID
```

Duplicate matching records are a failure.

Zero matching records are a failure.

---

# 10. Geometry and sequence-authority integration

## 10.1 Geometry authority extension

`BaseTrainAtlasWave02R5ModelGeometryAuthority` gains or binds:

```text
rope convention digest
pairing layout ID
rotary dimension
pair map digest
```

The geometry digest must change when any of these change.

## 10.2 Sequence authority extension

`BaseTrainRopeAuthority` gains:

```rust
pub pairing_layout_id: String,
pub rotary_pair_map_digest: String,
pub frequency_formula_id: String,
pub sign_convention_id: String,
pub external_convention_digest: String,
```

The `rope_config_digest` transcript includes these fields.

## 10.3 Required parity chain

```text
external convention authority
  -> ModelSpec rope section
  -> geometry authority
  -> sequence rope authority
  -> backend rope params
  -> pipeline selection
  -> stage receipt
```

Every edge must compare exact IDs and digests.

A theta-only parity receipt is insufficient after R5-R5.

---

# 11. Backend ABI

## 11.1 Dedicated RoPE params

R5-R5 should not continue treating pairing layout as an incidental interpretation of the general prefill params.

Admitted ABI:

```rust
#[repr(C)]
#[derive(Clone, Copy, Pod, Zeroable)]
pub struct BaseTrainAtlasWave02R5RopeParams {
    pub batch_size: u32,
    pub seq_len: u32,
    pub num_q_heads: u32,
    pub num_kv_heads: u32,
    pub head_dim: u32,
    pub rotary_dim: u32,
    pub q_width: u32,
    pub kv_width: u32,
    pub rope_theta: f32,
    pub pairing_layout_code: u32,
    pub flags: u32,
    pub reserved0: u32,
}
```

## 11.2 Pairing codes

```text
1 = NeoXHalfSplit
2 = InterleavedAdjacent
0 = invalid
```

Unknown codes fail before dispatch.

## 11.3 Pipeline separation

Preferred physical separation:

```text
base_train_atlas_wave_02_r5_rope_neox_half_split.wgsl
