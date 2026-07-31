# ASH-ATTN-HEADWISE-TEXTURE-02

## Persistent KV Buffer Lease /
## Layer-Scoped Texture Residency /
## Decode Session Generation Binding /
## Same-Device Population /
## No Fixture Source Seal

> Status: SPEC RELEASE rev.1  
> Patch ID: `ASH-ATTN-HEADWISE-TEXTURE-02`  
> Build revision: `HEADWISE-TEXTURE-02-persistent-kv-buffer-lease-v1`  
> Parent: `ASH-ATTN-HEADWISE-TEXTURE-01` PASS  
> Canonical local source SHA-256: `d0da4a99d561469b0ea3cba838b0853ea5251f9b93a17bd8f2691bd7f0fbfd46`  
> Canonical local source lines: `2227`  
> Canonical local source bytes: `49558`  
> Active production executor: `BufferAtlasV1`  
> Texture candidate: `KvTextureGqa4V1`  
> Production output authority: `HeadwiseFullActive` unchanged

---

# 0. Purpose

TEXTURE-01 classified `BufferAtlasV1` as the production-bound physical executor and `KvTextureGqa4V1` as a device-capability-bound candidate. TEXTURE-02 connects that candidate residency subsystem to the actual committed `DecodeState` K/V buffers without permitting texture production dispatch or output commitment.

Canonical flow:

```text
DecodeState::kv
  -> committed KvLayerCache K/V tensors
  -> strict same-device raw buffer leases
  -> layer-scoped Rgba32Float D2Array population
  -> all-layer sealed generation snapshot
```

The persistent K/V cache remains authoritative. Texture residency is a derived candidate snapshot and cannot mutate K/V state, token history, route authority, output authority, or physical executor selection.

---

# 1. Source authority

The source SSOT is the committed persistent K/V cache:

```text
DecodeState::kv.lifecycle.content_generation
DecodeState::kv.lifecycle.committed_past_len
KvLayerCache.key_cache
KvLayerCache.value_cache
KvLayerCache.key_content_generation
KvLayerCache.value_content_generation
KvLayerCache.committed_token_count
KvLayerCache.used_tokens
```

Population is forbidden when:

```text
staged_generation is present
staged_append_len != 0
committed generation differs across lifecycle, K and V
committed token count differs across lifecycle, shape and layer metadata
K/V shapes differ
K/V rank is not 4
K/V source is not strict raw borrowed same-device storage
```

Texture residency never writes back into persistent K/V or token history.

---

# 2. Persistent source layout

Actual persistent K/V uses contiguous `[batch, kv_head, sequence, head_dim]` layout. The existing fixture population shader uses page-major source data and cannot be reused.

New shader:

```text
crates/burn_webgpu_backend/src/shaders/
  headwise_kv_texture_population_persistent_cache_rgba4.wgsl
```

Canonical scalar address:

```text
(((batch * kv_head_count + kv_head)
  * source_seq_len + absolute_token)
  * head_dim + dimension)
```

The shader writes four adjacent f32 dimensions into one `rgba32float` texel. `head_dim` must be positive and divisible by four.

Partial final pages are deterministic:

```text
absolute_token < source_seq_len
  -> load committed K/V values

absolute_token >= source_seq_len
  -> write vec4<f32>(0.0)
```

The page table records the exact `valid_token_count`; zero padding is not interpreted as valid K/V.

---

# 3. Persistent raw buffer lease

Allowed lease:

```text
BridgeMode::RawBorrowed
ActiveTensorHandleState::BorrowedBuffer
f32
rank 4
contiguous BHSV
same existing device and queue lineage
read-only source use
committed generation only
```

Forbidden:

```text
UploadedFromHost
MetadataOnly
CPU materialization
host page-major repack
K/V payload readback
cross-device copy
cross-session lease reuse
cross-generation lease reuse
fixture source admission
```

The bind group must use the authorized binding window:

```rust
source_k.as_binding_resource()
source_v.as_binding_resource()
```

The following is forbidden for persistent sources:

```rust
source_k.buffer.as_entire_binding()
source_v.buffer.as_entire_binding()
```

`buffer_offset` must satisfy the device storage-buffer offset alignment. `buffer_offset + byte_count` must remain inside the lease binding window.

---

# 4. Layer-scoped residency

The existing texture array-layer axis represents:

```text
physical_page × batch × kv_head
```

It does not contain the transformer model-layer axis. TEXTURE-02 therefore owns one K/V texture residency pair per model layer.

Registry key:

```rust
pub struct HeadwiseTextureLayerResidencyKey {
    pub model_instance_id: String,
    pub decode_session_id: String,
    pub session_epoch: u64,
    pub layer_index: usize,
}
```

For a 22-layer model, a published generation requires exactly 22 independent layer records. Duplicate, missing or out-of-order layer authority fails closed.

Each layer generation binds:

```text
model instance
session ID and epoch
layer index
committed K/V generation
committed token count
K lease digest
V lease digest
texture layout digest
logical-to-physical page LUT digest
population shader digest
submission serial
layer content digest
```

---

# 5. Fixture-free residency construction

The existing `HeadwiseKvTextureResidency::new()` path remains available for diagnostic fixtures and smoke tests.

TEXTURE-02 adds:

```rust
HeadwiseKvTextureResidency::new_persistent(...)
```

`new_persistent()` creates:

```text
K and V Rgba32Float D2Array textures
persistent population pipeline
residency validation pipeline
page table and resource identities
```

It does not create the fixture generator pipeline.

Runtime persistent synchronization must contain zero references to:

```text
build_smoke_source_buffers
headwise_kv_source_fixture_generate
fixture_logical_pages as source authority
DiagnosticFixture admission
fixture generation dispatch
```

Diagnostic fixture code is preserved outside the persistent runtime path.

---

# 6. Decode session and generation binding

Every population request binds:

```text
model_instance_id
decode_session_id
session_epoch
layer_index
committed_generation
committed_token_count
synchronization trigger digest
```

Required generation equality:

```text
KvPositionLifecycle.content_generation
  == KvLayerCache.key_content_generation
  == KvLayerCache.value_content_generation
  == population request generation
  == texture page generation
```

Required token equality:

```text
lifecycle.committed_past_len
  == DecodeState.kv.past_len
  == layer.committed_token_count
  == layer.used_tokens
  == K shape sequence length
  == V shape sequence length
```

A generation or session mismatch is never repaired by relabeling a texture record.

---

# 7. Same-device population

Population uses the exact runtime device and queue already bound to the model and TEXTURE-01 physical-executor authority.

Forbidden:

```text
new adapter request
new device request
new queue lineage
host staging source
host-visible K/V payload
cross-device texture population
```

The population compute pass reads strict borrowed K/V storage bindings and writes the candidate K/V textures directly on the same device.

Receipt counters on PASS:

```text
same_device_population       true
raw_borrowed_k               true
raw_borrowed_v               true
host_upload_count            0
host_repack_count            0
cpu_materialize_count        0
readback_count               0
fixture_source_count         0
```

---

# 8. Page population and seal

For committed token count `S` and page size `P`:

```text
logical_page_count = ceil(S / P)
```

TEXTURE-02 uses identity logical-to-physical mapping for the canonical gate fixture. Runtime ownership still records the explicit page LUT and does not infer identity implicitly.

Page lifecycle:

```text
PopulationPending
  -> PopulationSubmitted
  -> SealPending
  -> SealedImmutable
```

Content digest is committed after GPU submission and before immutable seal. A sealed page cannot be repopulated under the same generation.

---

# 9. All-layer generation transaction

A session generation is published only after every expected layer has a sealed population receipt.

```text
Initialized
  -> LayersPopulating
  -> AllLayersPopulated
  -> AllLayersSealed
  -> Published
```

Any layer failure causes:

```text
new generation publication forbidden
new generation layer residencies removed/quarantined
previous published generation preserved
persistent K/V unchanged
BufferAtlas production execution unchanged
```

Texture population failure does not roll back already committed K/V because texture residency is still a derived candidate surface.

Published snapshot contains:

```text
expected and populated layer count
committed generation and token count
page size and page count
trigger kind and digest
all layer population receipts
all K/V raw lease digests
same-device population count
movement prohibition counters
nonmutation counters
snapshot digest
```

---

# 10. Synchronization policy

TEXTURE-02 does not run automatically on every token append.

```rust
pub enum HeadwiseTextureSynchronizationPolicy {
    Disabled,
    ExplicitAuditSnapshot,
}
```

Canonical policy:

```text
ExplicitAuditSnapshot
```

Supported explicit triggers may identify prefill, incremental, chunked, or operator audit snapshots, but all consume only committed K/V generations.

Incremental texel append, chunk-range append, joint K/V-texture commit and hot-path automatic synchronization are deferred to TEXTURE-03.

---

# 11. Runtime integration

New backend surface:

```text
crates/burn_webgpu_backend/src/
  headwise_kv_texture_persistent_population.rs
  shaders/headwise_kv_texture_population_persistent_cache_rgba4.wgsl
```

Modified backend:

```text
headwise_kv_texture_residency.rs
lib.rs
```

New model surface:

```text
crates/model_core/src/headwise_texture_persistent_kv_binding.rs
```

Modified model runtime:

```text
decode_state.rs
native_wgpu.rs
lib.rs
```

Model-owned registry:

```rust
HeadwiseTextureSessionResidencyRegistry
```

Explicit synchronization entrypoint:

```rust
NativeWgpuModel::synchronize_headwise_texture_from_committed_kv(...)
```

Session teardown entrypoint:

```rust
NativeWgpuModel::retire_headwise_texture_session(...)
```

`DecodeState` stores the latest published texture-generation snapshot and the latest population failure receipt. Neither field is an output-authority pointer.

---

# 12. Nonmutation boundary

TEXTURE-02 PASS requires:

```text
active physical executor             BufferAtlasV1
candidate executor                   KvTextureGqa4V1
candidate persistent residency       bound
Headwise output authority            HeadwiseFullActive

physical executor switch             0
KvTexture production dispatch        0
KvTexture output commit              0
KvTexture KV authority commit        0
route authority mutation             0
output authority mutation            0
TensorCube texture consumer          0
```

The candidate remains forbidden from producing production attention output.

---

# 13. Validation contract

```text
positive cases              >= 136
implementation target       144
negative controls           >= 144
implementation target       152
decision counters           112
child artifacts             92
CLI key/value pairs         88
response-file lines         176 non-empty
expected model layers       22
expected raw K/V leases     44
```

Source identities:

```text
persistent population shader SHA-256
2706a496a7d8e11d5074daece7ce3520dabcfb4a7f23a93ea0fc1c17da2fea9c

persistent residency host SHA-256
eb24309c19cd371b11e00b03e2ace3fe8d168999d35154ccaec708b1de954989
```

Child artifact ordered-list digest:

```text
a3d91ffba0e22b500f56a3658c379bf63450985d018a409f9c7080638dd168d2
```

Negative controls cover uploaded leases, metadata-only handles, wrong rank/dtype/layout, offset/range violation, generation/session/layer mismatch, staged K/V, token/shape mismatch, partial publication, fixture source, host repack, CPU materialization, readback, new device/queue, production dispatch/output/KV commit, route/output mutation, physical switch and TensorCube consumer admission.

---

# 14. Runtime artifacts

```text
workspace/runtime/attention/headwise/texture/02/
workspace/runtime/attention/headwise/texture/
  ash_attn_headwise_texture_02_runtime_artifact.json
workspace/runtime/attention/headwise/texture/
  ash_attn_headwise_texture_02_local_manifest.json
```

Code packages exclude Markdown, PowerShell/CMD helpers, hash sidecars and pre-generated TEXTURE-02 runtime output.

---

# 15. Direct execution

Binary:

```text
ash_attn_headwise_texture_02_gate
```

Response file:

```text
specs/cli/ash_attn_headwise_texture_02.args
```

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_headwise_texture_02_gate `
  -- `
  "@specs/cli/ash_attn_headwise_texture_02.args"
```

Expected revision:

```text
HEADWISE-TEXTURE-02-persistent-kv-buffer-lease-v1
```

Expected PASS token:

```text
PROMOTE_ASH_ATTN_HEADWISE_TEXTURE_02_PERSISTENT_KV_BUFFER_LEASE_LAYER_SCOPED_TEXTURE_RESIDENCY_DECODE_SESSION_GENERATION_BINDING_SAME_DEVICE_POPULATION_NO_FIXTURE_SOURCE_SEALED
```

---

# 16. Final seal

TEXTURE-02 establishes fixture-free, layer-scoped texture residency derived from committed persistent DecodeState K/V buffers. It proves strict same-device raw lease use, actual BHSV source addressing, generation/session/layer binding, deterministic partial-page zero fill, all-layer publication and prior-generation preservation while retaining BufferAtlas as the only production executor and HeadwiseFullActive as the unchanged output authority.

Next stage:

```text
ASH-ATTN-HEADWISE-TEXTURE-03

Incremental KV Texel Append /
Single-Token Page Update /
Chunk Multi-Token Population Transaction /
Atomic Page Seal /
KV·Texture Generation Parity Seal
```
