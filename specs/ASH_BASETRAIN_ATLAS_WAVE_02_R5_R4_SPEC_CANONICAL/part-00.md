# ASH-BASETRAIN-ATLAS-WAVE-02-R5-R4

## GQA Physical Geometry Authority /
## Unequal Query·KV Head Profile /
## Distinct Q·K·V Projection Width /
## KV Buffer Stride Closure /
## Q-Head To KV-Head Mapping /
## Resident K·V Shape Adoption /
## CPU-f64 GQA Numerical Parity /
## No Production Admission Seal

> Status: SPEC RELEASE rev.1  
> Patch ID: `ASH-BASETRAIN-ATLAS-WAVE-02-R5-R4`  
> Direct code parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R5-R3-R5`  
> Geometry authority parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R5-R3`  
> Parent physical gate: PASS observed  
> Patch class: synthetic GQA physical execution and unequal-width buffer closure  
> Model geometry writer: `BaseTrainAtlasWave02R5ModelGeometryAuthority`  
> GQA physical execution authority: opened only for the R5-R4 synthetic fixture  
> RoPE pairing-convention authority: none  
> Production checkpoint authority: none  
> Proof-ledger requalification authority: none  
> Production model admission: forbidden  
> R6 admission after this patch alone: forbidden

---

# 0. Purpose

`ASH-BASETRAIN-ATLAS-WAVE-02-R5-R4` promotes grouped-query attention from a statically representable geometry into a physically executed GPU path.

The patch must prove one concrete unequal-head profile through the complete R5 forward fixture:

```text
ModelSpec
  -> ModelGeometryAuthority
  -> resident Q/K/V weight shapes
  -> derived projection widths
  -> Q/K/V projection buffers
  -> Q/K RoPE buffers
  -> grouped query-to-KV mapping
  -> causal attention context
  -> CPU-f64 numerical parity
  -> live handoff shape receipt
```

The patch is not complete when only these statements are true:

```text
num_key_value_heads < num_attention_heads is accepted
K/V checkpoint shapes are smaller than Q shape
Params validation permits GQA
```

R5-R4 is complete only when the smaller K/V width is used by actual buffer allocation, actual WGSL indexing, actual dispatch geometry, actual readback cardinality, actual CPU reference calculation, and actual attention output.

The target distinction is:

```text
static GQA geometry
  != physical GQA execution
```

---

# 1. Parent physical state

The R5-R3 geometry authority gate has physically passed with the following explicit boundary:

```text
ModelSpec-derived Params              PASS
checkpoint/header shape binding       PASS
Q/KV projection shape distinction     PASS_STATIC
GQA geometry                          STATIC_ONLY
RoPE pairing convention               UNBOUND
production admission                  BLOCKED
R6 admission                          BLOCKED
```

R5-R4 inherits the first two PASS states.

R5-R4 must not rewrite or weaken the R5-R3 authority direction:

```text
CheckpointIdentity
  + SafetensorsHeader
  + CanonicalModelSpec
    -> ModelGeometryAuthority
    -> Params
```

R5-R4 adds physical execution beneath that authority.

---

# 2. Confirmed current-source findings

The following findings are confirmed against the R5-R3-R5 body.

## 2.1 Geometry authority already permits GQA

`BaseTrainAtlasWave02R5ModelGeometryAuthority::validate()` already requires:

```text
hidden_size == num_attention_heads × head_dim
num_key_value_heads <= num_attention_heads
num_attention_heads % num_key_value_heads == 0
q_projection_dim == num_attention_heads × head_dim
kv_projection_dim == num_key_value_heads × head_dim
```

It also requires distinct physical weight shapes:

```text
Q [q_projection_dim, hidden_size]
K [kv_projection_dim, hidden_size]
V [kv_projection_dim, hidden_size]
```

This is the correct static geometry direction.

## 2.2 Current canonical fixture remains MHA

The current canonical fixture declares:

```text
hidden_size              8
num_attention_heads      2
num_key_value_heads      2
head_dim                  4
q_projection_dim          8
kv_projection_dim         8
```

Therefore:

```text
q_projection_dim == kv_projection_dim
```

The currently passing fixture cannot reveal unequal-width indexing faults.

## 2.3 Resident validation is already shape-distinct

The resident weight validator separately compares:

```text
Q view -> geometry.q_projection_shape
K view -> geometry.k_projection_shape
V view -> geometry.v_projection_shape
```

This part is structurally ready for GQA.

R5-R4 must consume this distinction rather than flatten it downstream.

## 2.4 QKV projection still uses one hidden-width domain

The current QKV shader calculates:

```text
total       = batch_size × seq_len × hidden_size
output_lane = index % hidden_size
weight_base = output_lane × hidden_size
```

It writes Q, K and V at the same `index`.

The host allocates all three outputs with the same byte count:

```text
q_output bytes = token_count × hidden_size × 4
k_output bytes = token_count × hidden_size × 4
v_output bytes = token_count × hidden_size × 4
```

This remains an MHA-shaped execution even when resident K/V weights have smaller first dimensions.

Under unequal GQA geometry, the current shader may read past the logical K/V weight extent or treat padded allocation as semantic K/V channels.

## 2.5 K/V RoPE still uses Q width and Q head count

The current RoPE stage dispatches:

```text
batch_size × seq_len × num_attention_heads × head_dim/2
```

It derives one common base:

```text
base = token_index × hidden_size + head_index × head_dim
```

That base is used for both Q and K.

For GQA:

```text
Q stride = q_projection_dim = hidden_size
K stride = kv_projection_dim
```

