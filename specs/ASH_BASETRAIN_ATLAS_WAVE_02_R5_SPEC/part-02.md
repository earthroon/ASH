---

# 5. AW-01 compute-capable residency

## 5.1 Ring usage contract

Canonical slot usage:

```rust
wgpu::BufferUsages::COPY_DST
    | wgpu::BufferUsages::COPY_SRC
    | wgpu::BufferUsages::STORAGE
```

Forbidden:

```text
MAP_WRITE
UNIFORM substitution for model weights
new AW-02 weight buffer allocation
copying resident weight ranges into an AW-02 staging GPU buffer
```

## 5.2 Resident tensor view

Required type:

```rust
pub struct BaseTrainAtlasWave01ResidentTensorView<'a> {
    pub tensor_key: &'a str,
    pub group_id: &'a str,
    pub buffer: &'a wgpu::Buffer,
    pub buffer_identity_digest: &'a str,
    pub slot_index: u32,
    pub byte_offset: u64,
    pub byte_len: u64,
    pub dtype: &'a str,
    pub shape: &'a [u64],
    pub source_slice_digest: &'a str,
    pub address_digest: &'a str,
    pub source_weight_generation: u64,
    pub atlas_residency_generation: u64,
    pub runtime_holder_id: &'a str,
    pub device_epoch: u64,
    pub queue_epoch: u64,
}
```

The exact representation may differ, but all semantic fields are mandatory.

## 5.3 Canonical R5 resident group

The physical fixture must place these tensors in one current-resident group:

```text
model.embed_tokens.weight
model.layers.0.input_layernorm.weight
model.layers.0.self_attn.q_proj.weight
model.layers.0.self_attn.k_proj.weight
model.layers.0.self_attn.v_proj.weight
```

Canonical group ID:

```text
aw02.layer0.prefill_bundle
```

All five ranges must be:

```text
contiguous per tensor
non-overlapping
inside one live slot arena
F32 for the canonical R5 fixture
aligned to storage-binding requirements
covered by the AW-01 plan and upload receipts
```

R5 does not admit a tensor assembled from multiple non-contiguous views.

Segmented tensor binding is deferred.

## 5.4 Resident-view validation

For every tensor view:

```text
view tensor key equals plan tensor key
view group ID equals current resident group
slot index equals AW-01 handoff slot
buffer identity digest exists in AW-01 ring topology
address digest exists in AW-01 handoff
byte offset + byte length does not overflow
range lies within slot capacity
byte length equals dtype-width * shape product
source weight generation exact
atlas residency generation exact
runtime holder exact
device epoch exact
queue epoch exact
```

---

# 6. No host weight reupload contract

## 6.1 Backend input change

Forbidden R5 input fields:

```rust
embedding: &[f32]
rms_weight: &[f32]
q_weight: &[f32]
k_weight: &[f32]
v_weight: &[f32]
```

Required semantic input:

```rust
pub struct BaseTrainAtlasWave02R5ResidentWeights<'a> {
    pub embedding: BaseTrainAtlasWave01ResidentTensorView<'a>,
    pub rms: BaseTrainAtlasWave01ResidentTensorView<'a>,
    pub q: BaseTrainAtlasWave01ResidentTensorView<'a>,
    pub k: BaseTrainAtlasWave01ResidentTensorView<'a>,
    pub v: BaseTrainAtlasWave01ResidentTensorView<'a>,
}
```

## 6.2 Allowed queue writes in AW-02 R5

```text
token IDs
row-valid lengths
position IDs
small immutable parameter block
optional zero initialization for output buffers when required
```

## 6.3 Required zero counters

```text
AW-02 checkpoint open count                     0
AW-02 checkpoint payload read bytes             0
AW-02 weight buffer create count                0
AW-02 weight queue-write count                  0
AW-02 weight queue-write bytes                  0
AW-02 host full-tensor materialization count    0
AW-02 resident-to-replacement copy count        0
```

## 6.4 CPU-reference fixture exception

The physical gate may retain deterministic small fixture arrays solely to calculate an independent CPU-f64 oracle.

That exception is admitted only when:

```text
the arrays are created before Safetensors serialization
the GPU weight source is still the AW-01 resident ring
the reference arrays are never passed to the AW-02 GPU backend
the reference arrays never trigger queue.write_buffer in AW-02
the artifact marks fixture_cpu_reference_only = true
production_path_host_weight_materialization = false
```

---

# 7. WGPU26 WGSL ABI audit

## 7.1 Canonical shader set

R5 replaces the monolithic shader with:

```text
base_train_atlas_wave_02_r5_embedding.wgsl
base_train_atlas_wave_02_r5_rmsnorm.wgsl
base_train_atlas_wave_02_r5_qkv_projection.wgsl
base_train_atlas_wave_02_r5_rope.wgsl
base_train_atlas_wave_02_r5_attention_oracle.wgsl
```

If a real Headwise training adapter is implemented, its existing dispatcher shaders remain owned by the Headwise subsystem and are referenced by identity rather than copied into AW-02.

## 7.2 Parse and validation requirements

Every canonical shader must pass:

```text
WGSL parse
Naga module validation
WGPU shader-module creation
pipeline creation
bind-group-layout compatibility
entry-point existence
workgroup-size validation
```

Static brace counting is supplementary only.

It is not a WGSL parser.

## 7.3 Forbidden WGSL forms

```text
ptr<storage> user-function arguments
resource pointer aliasing between Q, K and V
hardcoded rope theta
implicit position = sequence index
hardcoded batch, sequence or hidden geometry in address helpers
unchecked index arithmetic
read_write weight bindings
write access to AW-01 resident weights
runtime-sized output arrays without validated byte bounds
NaN sentinel accepted as valid output
```

## 7.4 Shader ABI manifest

For every entry point, Rust must publish:

```text
shader source SHA-256
entry-point name
workgroup size
bind group number
binding number
binding semantic ID
buffer access mode
minimum binding size
parameter layout digest
dispatch geometry formula
source validation result
runtime shader-module result
pipeline creation result
```

## 7.5 Repository-wide inventory claim boundary

The gate must scan all backend WGSL files for forbidden resource-pointer signatures.

Artifact fields:

```text
repository_wgsl_file_count
repository_ptr_storage_hit_count
aw02_r5_canonical_hit_count
external_legacy_hit_paths
external_legacy_hits_repaired
claim_scope
```

Required R5 values:

```text
aw02_r5_canonical_hit_count = 0
claim_scope = AW02_R5_CANONICAL_SHADER_SET_ONLY
```

External legacy hits do not fail R5 unless they are imported or dispatched by R5.

They must remain visible in the artifact.

---

# 8. Explicit parameter authority

## 8.1 Parameter block

Required semantic fields:

```rust
#[repr(C)]
pub struct BaseTrainAtlasWave02R5Params {
    pub batch_size: u32,
    pub seq_len: u32,
    pub vocab_size: u32,
    pub hidden_size: u32,
    pub num_heads: u32,
    pub num_kv_heads: u32,
    pub head_dim: u32,
    pub selected_layer: u32,
    pub rope_theta: f32,
    pub rms_epsilon: f32,
    pub attention_scale: f32,
    pub flags: u32,
}
```

The physical representation must satisfy WGSL uniform-layout alignment.

The Rust and WGSL layout digests must match.

## 8.2 Required validation

```text
batch_size > 0
seq_len > 0
vocab_size > 0
hidden_size > 0
num_heads > 0
num_kv_heads > 0
head_dim > 0
hidden_size == num_heads * head_dim for canonical profile
