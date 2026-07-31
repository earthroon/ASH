# ASH-ATTN-HEADWISE-TEXTURE-01

## Headwise Physical Executor Authority /
## BufferAtlas·KvTexture Executor Classification /
## Kernel Bundle Digest /
## Device Capability Binding /
## No Route Authority Mutation Seal

> 상태: SPEC RELEASE rev.1  
> Patch ID: `ASH-ATTN-HEADWISE-TEXTURE-01`  
> Build revision: `HEADWISE-TEXTURE-01-physical-executor-authority-v1`  
> Parent: `ASH-ATTN-INTERCONNECT-W3-C6-R1` PASS  
> Canonical local source SHA-256: `a6617a67872430d1dc30bd09b751a8c424206f93d0e050243af605c240fe23fb`  
> Canonical local source lines: `1312`  
> Canonical local source bytes: `34498`  
> Production route authority: unchanged  
> Production output authority: `HeadwiseFullActive` unchanged  
> TensorCube role: `ShadowObserverOnly` unchanged

---

# 0. Purpose

W3-C6 seals Headwise as the model-scoped production attention output authority. The current physical executor is the storage-buffer based `HeadwiseAtlasDispatcher`. A separate K/V tensor-texture subsystem already exists with `Rgba32Float` D2-array residency, integer `textureLoad`, GQA4 topology, parity probes, health tokens and soak surfaces, but it is not part of the production route graph.

TEXTURE-01 does not switch the production executor. It introduces a distinct physical-executor authority that classifies and binds the existing BufferAtlas executor and the KvTexture candidate while preserving all W3 route and output authority.

```text
route authority
  W3-C1 through W3-C5

output authority
  W3-C6 HeadwiseFullActive

physical executor authority
  TEXTURE-01
```

---

# 1. Executor classification

```rust
pub enum HeadwisePhysicalExecutorKind {
    BufferAtlasV1,
    KvTextureGqa4V1,
}

pub enum HeadwisePhysicalExecutorRole {
    ProductionActive,
    ClassifiedCandidate,
}

pub enum HeadwisePhysicalExecutorReadiness {
    ProductionBound,
    CapabilityBoundCandidate,
    CapabilityUnavailable,
    Unknown,
}
```

Canonical state:

```text
BufferAtlasV1
  role       ProductionActive
  readiness  ProductionBound

KvTextureGqa4V1
  role       ClassifiedCandidate
  readiness  CapabilityBoundCandidate
           | CapabilityUnavailable
```

`CapabilityUnavailable` is an explicit device-bound classification and may PASS. `Unknown` is fail-closed and cannot PASS.

TEXTURE-01 forbids:

```text
production executor switch
KvTexture production dispatch
KvTexture output commit
KvTexture KV commit
route readiness mutation
HeadwiseFullActive pointer CAS
TensorCube texture consumer admission
```

---

# 2. Kernel bundle identity

Each physical executor is represented by an ordered kernel bundle whose digest binds shader sources, host implementation sources, parameter ABI, bind-group ABI and storage contract.

## BufferAtlasV1 components

```text
headwise_atlas_attention_production_rw.wgsl
headwise_atlas_attention_production_long_kv_optimized_v2.wgsl
HeadwiseAtlasGpuParams ABI
HeadwiseAtlasDispatcher host implementation
route LUT
finite guard
production receipt ABI
same-device raw buffer lease contract
```

## KvTextureGqa4V1 components

```text
headwise_kv_texture_population.wgsl
headwise_kv_texture_residency_validation.wgsl
headwise_gqa4_cluster_attention.wgsl
headwise_gqa4_cluster_attention_topology.wgsl
HeadwiseKvTextureLayout ABI
PopulationParams ABI
Gqa4Params ABI
HeadwiseKvTextureResidency host implementation
GQA4 validation host implementation
logical-to-physical page-table policy
integer texture-coordinate policy
```

Bundle digest serialization is ordered UTF-8 with explicit component kind, canonical path, source SHA-256 and ABI identity. Component reordering changes the digest.

---

# 3. Source identity baseline

Canonical source digests used by the gate:

```text
BufferAtlas short shader
927fe3f2d6488909c92579e96776db352839df53c5d0ed3095a01507d297fc8f

BufferAtlas long shader
8c6405eea959ce54c7a4e73ba0621d78fb03ea0fcb8dac849a1207830ea0d717

HeadwiseAtlasDispatcher host
b3dd13934a52f8407a870f9198363af44e2b3ac87644ca7228b06cd40f8b8599

Route LUT
682f597f1b073fbcbd933a6265e9defebf112c615f30e79903c08ae8657552ba

Finite guard
119b9b9e68c8122d3a816b1489f55d16307a3e41fa4be86eb52db872951b1546

KvTexture population shader
fc14ca942d5bbd71b19dd913f128fd88cd2911c111610f5aa4ef096997f9e53c

KvTexture residency validation shader
9ef263b67a51468c469fedb6c51937d929ac1c99af8cd60336945d3cc125796f

GQA4 texture attention shader
52d795f98e726b3d30cf85cd3a7df697bc2c3c7b3a996a7665a096ea5a76e875

GQA4 topology shader
e3dd7fbf1996f4c82686f68e2a74d7bca49e82e736d4c86320ef0b37a43d6de6

KvTexture residency host
540d9d32ddaf9abc955441b0335e3843d45368499ad75935f09da0cdb28cfbbc

GQA4 validation host
906f3a896315858a8905e17566d12523d9f4c23f7cc9685e697d16cb40dfbd3c
```

Any baseline mismatch fails closed before authority publication.

---

# 4. Device capability binding

The authority receipt binds the exact existing device and queue identity used by the C6 production model. A second device or silently recreated queue is forbidden.

## BufferAtlasV1 requirements

```text
existing production device exact
storage-buffer limits satisfy model profile
required workgroup limits satisfy active shaders
short and long pipeline validation pass
same-device raw buffer lease available
```

## KvTextureGqa4V1 requirements

```text
SUBGROUP feature available
observed subgroup size == 32
max compute invocations per workgroup >= 128
max workgroup storage >= 10048 bytes
Rgba32Float supports STORAGE_BINDING write
Rgba32Float supports non-filterable TEXTURE_BINDING read
D2Array texture and view creation succeeds
required texture dimensions and array layers fit device limits
population, validation, topology and GQA4 pipelines validate
same existing device and queue exact
```

The probe performs real texture, view, bind-group layout and pipeline creation under WebGPU error scopes. Feature bits alone do not establish readiness.

Result states:

```text
all requirements and creation probes pass
  -> CapabilityBoundCandidate

known unsupported feature, format or limit
  -> CapabilityUnavailable

probe missing, incomplete or internally inconsistent
  -> Unknown / HOLD
```

---

# 5. Authority snapshot

```rust
pub struct HeadwisePhysicalExecutorAuthoritySnapshot {
    pub model_instance_id: String,
    pub fullactive_pointer_digest: String,
    pub fullactive_pointer_generation: u64,
    pub device_identity_digest: String,
    pub active_executor: HeadwisePhysicalExecutorRecord,
    pub candidate_executor: HeadwisePhysicalExecutorRecord,
    pub route_authority_mutation_count: u64,
    pub output_authority_mutation_count: u64,
    pub production_executor_switch_count: u64,
    pub kv_texture_production_dispatch_count: u64,
    pub kv_texture_output_commit_count: u64,
    pub kv_texture_kv_commit_count: u64,
    pub tensorcube_texture_consumer_count: u64,
    pub snapshot_digest: String,
}
```

Canonical counters are all zero.

The snapshot is model-scoped, bind-once and read-mostly. Idempotent replay requires the same digest. A conflicting rebind fails closed.

The snapshot does not own route registration, route readiness, output authority, KV lifecycle or selector state.

---

# 6. No-route-mutation seal

TEXTURE-01 proves that classification does not mutate W3 authority:

```text
C2 prefill route digest unchanged
C3 incremental route digest unchanged
C4 chunked route digest unchanged
C5 generic delegation digest unchanged
C6 FullActive pointer state unchanged
C6 FullActive pointer generation unchanged
C6 FullActive pointer digest unchanged
production output authority remains HeadwiseFullActive
TensorCube remains ShadowObserverOnly
```

The gate does not expose an executor switch method or a texture production dispatch entrypoint.

---

# 7. Implementation surface

New:

```text
crates/model_core/src/headwise_physical_executor_authority.rs
crates/orchestrator_local/src/headwise_texture_01_cli_registry.rs
crates/orchestrator_local/src/bin/ash_attn_headwise_texture_01_gate.rs
specs/cli/ash_attn_headwise_texture_01.args
```

Modified:

```text
crates/model_core/src/lib.rs
crates/model_core/src/native_wgpu.rs
crates/orchestrator_local/Cargo.toml
```

`NativeWgpuModel` owns a model-scoped `HeadwisePhysicalExecutorAuthoritySlot`. Binding requires an existing exact W3-C6 `HeadwiseFullActive` pointer.

---

# 8. Validation contract

```text
positive cases              >= 120
implementation target       128
negative controls           >= 128
implementation target       136
decision counters           88
child artifacts             76
CLI key/value pairs         78
response file lines         156 non-empty
```

Child artifact ordered-list digest:

```text
a5fda0430c828bacb6b5d79bae4c0054209920035489bedf2f28ae00e46d4094
```

Required static closure:

```text
physical authority module exported
NativeWgpuModel authority slot present
BufferAtlas production owner exact
KvTexture host and shader owner exact
Rgba32Float D2Array contract exact
integer textureLoad contract exact
model_core texture production consumer absent
TensorCube texture consumer absent
executor switch CAS absent
route/output authority mutation APIs absent
```

Negative controls cover source drift, component reorder, ABI drift, device mismatch, format/limit failures, unknown capability, parent C6 drift, attempted executor switch, texture production dispatch, output/KV commit, route mutation and TensorCube consumer admission.

---

# 9. Runtime artifacts

```text
workspace/runtime/attention/headwise/texture/01/
workspace/runtime/attention/headwise/texture/ash_attn_headwise_texture_01_runtime_artifact.json
workspace/runtime/attention/headwise/texture/ash_attn_headwise_texture_01_local_manifest.json
```

Code packages exclude Markdown, pre-generated runtime artifacts, local manifests, hash sidecars and PowerShell/CMD helpers.

---

# 10. Direct execution

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_attn_headwise_texture_01_gate `
  -- `
  "@specs/cli/ash_attn_headwise_texture_01.args"
```

Expected revision:

```text
HEADWISE-TEXTURE-01-physical-executor-authority-v1
```

A supported device reports the texture candidate as `capability_bound_candidate`. A device without required texture/subgroup support reports `capability_unavailable`; this remains a valid classified state. `unknown` cannot PASS.

PASS token:

```text
PROMOTE_ASH_ATTN_HEADWISE_TEXTURE_01_PHYSICAL_EXECUTOR_AUTHORITY_BUFFER_ATLAS_KV_TEXTURE_EXECUTOR_CLASSIFICATION_KERNEL_BUNDLE_DIGEST_DEVICE_CAPABILITY_BINDING_NO_ROUTE_AUTHORITY_MUTATION_SEALED
```

---

# 11. Final seal

TEXTURE-01 establishes a dedicated physical-executor SSOT below the existing Headwise route and output authorities. `BufferAtlasV1` remains the only production-bound executor. `KvTextureGqa4V1` becomes a digest-bound, device-bound candidate or an explicit unavailable candidate. No production route, output pointer, KV state, selector state or TensorCube authority is mutated.

The next stage is `ASH-ATTN-HEADWISE-TEXTURE-02`, which binds persistent same-device DecodeState K/V buffers to layer-scoped texture residency without fixture sources.