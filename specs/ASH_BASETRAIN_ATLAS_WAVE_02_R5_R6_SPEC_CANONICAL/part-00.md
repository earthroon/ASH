# ASH-BASETRAIN-ATLAS-WAVE-02-R5-R6

## Production Candidate Checkpoint Tensor-Set Authority /
## Safetensors Index·Shard CAS Binding /
## All-Layer Tensor Inventory /
## Dtype·Shape·Byte-Range Closure /
## Config·Header·Payload Identity Convergence /
## Canonical Tensor Name Resolution /
## No Synthetic Tensor Admission /
## No Forward Authority Seal

> Status: SPEC RELEASE rev.1  
> Patch ID: `ASH-BASETRAIN-ATLAS-WAVE-02-R5-R6`  
> Direct physical parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R5-R5`  
> Parent state: external RoPE convention physical PASS observed  
> Patch class: production-candidate checkpoint tensor-set identity and inventory closure  
> New SSOT: `BaseTrainAtlasWave02R5CheckpointTensorSetAuthority`  
> Payload execution authority: none  
> GPU upload authority: none  
> Forward authority: none  
> Training authority: none  
> Production admission: forbidden  
> Proof-ledger promotion: forbidden  
> R6 headwise admission after this patch alone: forbidden

---

# 0. Purpose

`ASH-BASETRAIN-ATLAS-WAVE-02-R5-R6` binds one real production-candidate checkpoint tensor set to the geometry and RoPE authorities physically proven by R5-R3 through R5-R5.

The patch must prove that every model tensor required by the selected architecture belongs to one immutable checkpoint set and that every physical payload range can be traced through:

```text
production config bytes
  + checkpoint root identity
  + optional Safetensors index bytes
  + ordered shard CAS set
  + per-shard Safetensors headers
  + canonical architecture schema
    -> complete physical tensor inventory
    -> canonical tensor-role inventory
    -> dtype/shape/range closure
    -> config/header/payload identity convergence
    -> CheckpointTensorSetAuthority
```

The patch is not complete when only these statements are true:

```text
a checkpoint file SHA-256 matches
one selected layer has Q/K/V tensors
Safetensors headers parse
planned tensor names exist in an operator-authored registry
```

R5-R6 is complete only when all required layers and all required global tensors are accounted for, every index-to-shard relation is exact, every header-to-payload range is valid, every canonical role is unique, and no synthetic fixture tensor is admitted into the candidate authority.

The core distinction is:

```text
checkpoint file exists
  != complete production-candidate tensor set is authoritative
```

---

# 1. Parent physical state

R5-R6 imports and verifies the physical PASS artifacts from:

```text
R5-R3  Model Geometry Authority
R5-R4  GQA Physical Geometry Authority
R5-R5  External RoPE Convention Authority
```

The imported parent state must establish:

```text
ModelSpec digest                         sealed
ModelGeometryAuthority digest            sealed
query/KV head geometry                   physically proven
Q/K/V projection width distinction       physically proven
contiguous Q-head to KV-head mapping     physically proven
external RoPE convention                 physically proven
checkpoint config source digest          sealed
rope_theta source bits                   sealed
production admission                     false
proof ledger                             HOLD
R6 admission                             false
```

R5-R6 must reject any parent manifest that:

```text
contains a non-PASS parent token
uses a synthetic-only checkpoint identity as production evidence
changes the ModelSpec digest
changes the geometry digest
changes the external RoPE authority digest
claims production admission
claims proof-ledger promotion
claims R6 admission
```

---

# 2. Confirmed current-source findings

The following findings are confirmed against the R5-R5-R3 body.

## 2.1 AW-01 verifies one physical Safetensors file

The current AW-01 checkpoint reader already performs:

```text
streaming whole-file SHA-256
bounded header-length read
header JSON parse
F32/F16/BF16 dtype admission
shape product validation
data_offsets bounds validation
byte-length equals element-count × dtype-width
intra-file tensor-range overlap rejection
```

It emits:

```text
BaseTrainAtlasWaveCheckpointIdentityReceipt
BaseTrainAtlasWaveSafetensorsHeaderReceipt
```

This is valid evidence for one file.

It is not yet a tensor-set authority because it does not model:

```text
model.safetensors.index.json
multiple shard files
weight_map ownership
per-shard CAS ordering
cross-shard duplicate keys
all-layer canonical role completeness
config/header/inventory convergence
```

## 2.2 Current tensor locations are relative to one data section

`BaseTrainAtlasWaveSafetensorsTensor` currently stores:

```text
tensor_key
dtype
shape
data_offset_start
data_offset_end
```

It does not store:

```text
shard identity
shard digest
header digest owner
absolute payload range
canonical role
layer index
logical alias relation
```

R5-R6 must not reinterpret the existing offsets as globally unique across multiple shards.

## 2.3 R5-R3 inspects only a selected subset

The current geometry authority requires five keys:

```text
model.embed_tokens.weight
model.layers.L.input_layernorm.weight
model.layers.L.self_attn.q_proj.weight
model.layers.L.self_attn.k_proj.weight
model.layers.L.self_attn.v_proj.weight
```

That subset is sufficient for the R5 staged attention fixture.

