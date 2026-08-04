# ASH-BASETRAIN-ATLAS-WAVE-02-R5-R3

## Checkpoint Model Geometry Authority /
## Header·Config To ModelSpec Binding /
## ModelSpec-Derived Params /
## Projection Shape Derivation /
## Fixture Profile Explicit Isolation /
## No Independent Geometry Literal /
## No Production Admission Seal

> Status: SPEC RELEASE rev.1  
> Patch ID: `ASH-BASETRAIN-ATLAS-WAVE-02-R5-R3`  
> Direct code parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R5-R2`  
> Physical compute parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R5-R1`  
> Lineage parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R5-R2`  
> Patch class: model-geometry authority and parameter-derivation closure  
> Runtime shader algorithm mutation authority: none, except shape-derived indexing required by this contract  
> GQA physical execution authority: none  
> RoPE pairing-convention authority: none  
> Production model admission: forbidden  
> R6 admission after this patch alone: forbidden

---

# 0. Purpose

`ASH-BASETRAIN-ATLAS-WAVE-02-R5-R3` establishes one authoritative direction for model geometry:

```text
checkpoint identity
  + Safetensors header tensor shapes
  + canonical ModelSpec configuration
  + batch sequence authority
    -> ModelGeometryAuthority
    -> derived backend Params
    -> resident tensor shape validation
    -> stage dispatch geometry
```

R5-R3 removes independent declarations of the same geometry from:

```text
fixture_spec()
gate-local BaseTrainAtlasWave02R5Params literal
resident Q/K/V common [hidden, hidden] assertion
shader-side implicit geometry assumptions
```

R5-R3 does not claim that Safetensors alone contains the complete model architecture.

Safetensors provides physical tensor keys, dtypes and shapes. The canonical `ModelSpec` provides architecture semantics that cannot be recovered uniquely from those shapes, including:

```text
num_attention_heads
num_key_value_heads
head_dim interpretation
RoPE theta
RoPE scaling
RMS epsilon
maximum positions
model family and architecture
```

Therefore the authoritative binding is:

```text
CheckpointIdentityReceipt
  + SafetensorsHeaderReceipt
  + CanonicalModelSpec
  -> sealed ModelGeometryAuthorityReceipt
```

No one input may independently override another.

---

# 1. Confirmed current-source findings

The R5-R2 body contains three independent geometry declaration surfaces.

## 1.1 Fixture ModelSpec literal

Current gate function:

```rust
fn fixture_spec() -> ModelSpec
```

Current independent assignments include:

```text
vocab_size                32
hidden_size                8
num_layers                 1
num_attention_heads        2
num_key_value_heads        2
head_dim                    4
intermediate_size         16
max_position_embeddings   16
rope.theta             10000
```

## 1.2 Gate-local Params literal

The same gate separately constructs:

```rust
BaseTrainAtlasWave02R5Params {
    batch_size: 2,
    seq_len: 4,
    vocab_size: 32,
    hidden_size: 8,
    num_heads: 2,
    num_kv_heads: 2,
    head_dim: 4,
    selected_layer: 0,
    rope_theta: 10_000.0,
    rms_epsilon: 1e-5,
    attention_scale: 0.5,
    flags: 0,
}
```

This is not derived from `ModelSpec` or the checkpoint header.

## 1.3 Resident projection shape common assertion

Current resident validation uses one common shape for Q, K and V:

```rust
for view in [&self.q, &self.k, &self.v] {
    ensure!(
        view.shape == &[params.hidden_size as u64, params.hidden_size as u64],
        "AW02R5ProjectionShapeMismatch"
    );
}
```

That assertion silently encodes MHA geometry.

## 1.4 Generic Params validation forces MHA

Current validation requires both:

```text
hidden_size == num_heads × head_dim
hidden_size == num_kv_heads × head_dim
```

The second equality forces:

```text
num_kv_heads == num_heads
```

when the first equality also holds.

A GQA checkpoint is therefore rejected before its K/V geometry can be tested.

## 1.5 ModelSpec already contains the required architecture dimensions

The existing `model_core::ModelSpec` contains:

```text
dimensions.vocab_size
dimensions.hidden_size
dimensions.num_layers
dimensions.num_attention_heads
dimensions.num_key_value_heads
dimensions.head_dim
dimensions.intermediate_size
dimensions.max_position_embeddings
rope.kind
rope.theta
rope.scaling
norm.kind
norm.eps
```

The generic `validate_spec_consistency()` already permits grouped-query attention by requiring:

```text
hidden_size == num_attention_heads × head_dim
num_key_value_heads <= num_attention_heads
num_attention_heads % num_key_value_heads == 0
```

R5-R3 must reuse that direction rather than install a contradictory local rule.

---

# 2. Authority direction

## 2.1 Required direction

The only admitted direction is:

```text
canonical ModelSpec source
  -> ModelSpec digest
  -> validate_spec_consistency
  -> checkpoint/header reconciliation
  -> ModelGeometryAuthority
  -> BaseTrainAtlasWave02R5Params::derive(...)
  -> resident tensor validation
  -> GPU parameter binding
```

Batch-local dimensions use a parallel source:

```text
BaseBatchCpu
  + BaseTrainSequenceAuthorityReceipt
    -> batch_size
    -> seq_len
    -> row_valid_lengths
    -> position IDs
```

The two sources meet only in the parameter builder.

## 2.2 Forbidden directions

```text
Params -> ModelSpec
resident tensor shapes -> silent ModelSpec replacement
shader constants -> host geometry
fixture constants -> production geometry
checkpoint file name -> model family inference
Q weight shape -> num_heads guess
K weight shape -> num_kv_heads guess without ModelSpec
receipt JSON -> live geometry authority reconstruction
```

## 2.3 No dual writers

After R5-R3:

```text
ModelSpec is the semantic geometry writer.
Safetensors header is the physical tensor-shape witness.
ModelGeometryAuthority is the sealed reconciliation result.
Params is a derived transport object only.
```

`BaseTrainAtlasWave02R5Params` must not be treated as an independently authored configuration.

---

# 3. Canonical ModelSpec source

## 3.1 Production source

Production ModelSpec must be loaded from an explicit configuration artifact whose identity is provided to the runtime.

Examples of admitted source forms:

```text
repository ModelSpec TOML
checkpoint-adjacent immutable model config converted to ModelSpec
signed or digest-pinned model architecture manifest
```

The source path, byte count and SHA-256 must be recorded.

No default `ModelSpec::default()` followed by scattered field assignments is admitted for production.

## 3.2 Fixture source

The R5 canonical fixture may use a generated ModelSpec, but all fixture geometry literals must exist in exactly one fixture profile declaration.

Required type:

```rust
pub struct Aw02R5FixtureProfileV1 {
    pub vocab_size: u32,
    pub hidden_size: u32,
    pub num_layers: u32,
    pub num_attention_heads: u32,
    pub num_key_value_heads: u32,
    pub head_dim: u32,
    pub intermediate_size: u32,
    pub max_position_embeddings: u32,
    pub rope_theta: f64,
    pub rope_kind: String,
    pub rope_scaling: String,
    pub rms_epsilon: f64,
    pub batch_size: u32,
    pub seq_len: u32,
    pub selected_layer: u32,
}
```

The fixture profile is the only location where the fixture values may be authored.

From that single value, the gate must derive:

```text
fixture ModelSpec
fixture checkpoint tensor shapes
fixture tensor payload element counts
fixture atlas slice lengths
fixture BaseBatchCpu
fixture selected layer
expected resident shapes
expected parameter transport
```

The following separate functions may exist only if they accept the profile and do not redeclare dimensions:

```rust
build_fixture_model_spec(&profile)
generate_fixture_checkpoint(&profile)
build_fixture_batch(&profile)
build_fixture_atlas_plan(&profile)
```

A zero-argument `fixture_spec()` containing geometry literals is forbidden.

## 3.3 Fixture profile classification

The canonical R5-R3 fixture is explicitly:

```text
profile kind     SyntheticMhaFixture
production       false
GQA exercised    false
model family     fixture-only
```

The fixture profile may prove authority direction and MHA shape reconciliation. It may not prove production checkpoint compatibility or GQA execution.

---

# 4. Model geometry authority object

R5-R3 introduces a sealed host-side authority object.

```rust
pub struct BaseTrainAtlasWave02R5ModelGeometryAuthority {
    pub authority_version: String,
    pub profile_kind: BaseTrainAtlasWave02R5GeometryProfileKind,

    pub checkpoint_identity_digest: String,
    pub checkpoint_header_digest: String,
    pub model_spec_id: String,
    pub model_spec_digest: String,
    pub model_spec_source_digest: String,

    pub vocab_size: u32,
    pub hidden_size: u32,
    pub num_layers: u32,
    pub num_attention_heads: u32,
    pub num_key_value_heads: u32,
    pub head_dim: u32,
    pub q_projection_dim: u32,
    pub kv_projection_dim: u32,
    pub intermediate_size: u32,
    pub max_position_embeddings: u32,

    pub rope_kind: String,
    pub rope_theta_bits: u64,
