# ASH-BASETRAIN-ATLAS-WAVE-02-R5-R5

## External RoPE Convention Authority /
## Checkpoint rope_theta Binding /
## Rotary Pairing Layout Authority /
## NeoX·Interleaved Convention Separation /
## Q·K Unequal Head-Domain Rotation /
## CPU-f64 External Convention Parity /
## Known-Vector Fixture /
## No Production Admission Seal

> Status: SPEC RELEASE rev.1  
> Patch ID: `ASH-BASETRAIN-ATLAS-WAVE-02-R5-R5`  
> Direct code parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R5-R4-R2`  
> Physical parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R5-R4` GQA gate PASS observed  
> Patch class: externally bound RoPE convention and physical pairing-layout closure  
> Geometry authority: `BaseTrainAtlasWave02R5ModelGeometryAuthority`  
> New convention authority: `BaseTrainAtlasWave02R5ExternalRopeConventionAuthority`  
> Checkpoint scope: pinned local configuration evidence only  
> Network access during gate: forbidden  
> Production checkpoint execution: forbidden  
> Proof-ledger promotion: forbidden  
> R6 admission after this patch alone: forbidden

---

# 0. Purpose

`ASH-BASETRAIN-ATLAS-WAVE-02-R5-R5` closes the remaining RoPE convention gap below the R5-R4 grouped-query attention path.

R5-R4 proved that unequal query and KV head domains physically survive:

```text
4 query heads
2 KV heads
Q width 16
K/V width 8
quotient Q-to-KV mapping
CPU-f64 GQA parity
```

R5-R4 intentionally left the following state unbound:

```text
External RoPE pairing convention = UNBOUND
```

The current GPU and CPU implementations can agree numerically while both use a pairing layout different from the external checkpoint family. Therefore GPU-to-CPU parity alone is not sufficient evidence.

R5-R5 adds a second authority axis:

```text
checkpoint config bytes
  + checkpoint identity
  + model family declaration
  + pinned convention-registry evidence
    -> ExternalRopeConventionAuthority
    -> exact pair map
    -> exact inverse-frequency schedule
    -> exact Q/K physical rotation
    -> independent known-vector proof
```

The patch must distinguish:

```text
internal numerical agreement
  != external checkpoint convention agreement
```

---

# 1. Parent physical state

The physical parent has emitted:

```text
PASS_ASH_BASETRAIN_ATLAS_WAVE_02_R5_R4_...
ROPE_PAIRING_EXTERNAL_UNBOUND
NO_PRODUCTION_ADMISSION
PROOF_LEDGER_HOLD
R6_BLOCKED
```

R5-R5 imports the R5-R4 physical manifest and verifies:

```text
parent patch ID              ASH-BASETRAIN-ATLAS-WAVE-02-R5-R4
parent pass token            exact match
parent profile kind          SyntheticGqaFixture
query heads                  4
KV heads                     2
head dimension               4
Q projection width           16
KV projection width           8
Q heads per KV                2
modulo counterfactual        rejected
padding exact-zero           true
production admitted          false
proof ledger                 HOLD
R6 admitted                  false
```

No R5-R5 gate may reconstruct these facts from defaults when the parent manifest is missing.

---

# 2. Confirmed current-source findings

The following findings are confirmed against the R5-R4-R2 full body.

## 2.1 `rope_theta` is represented, pairing layout is not

The current `RopeSection` contains:

```rust
pub struct RopeSection {
    pub kind: String,
    pub theta: f64,
    pub scaling: String,
}
```

It has no field for:

```text
pairing layout
frequency layout
rotary dimension source
architecture convention revision
external implementation evidence digest
```

## 2.2 Sequence authority does not seal pairing

`BaseTrainRopeAuthority` currently seals:

```text
model_spec_id
model_spec_digest
rope_kind
theta_bits
scaling
head_dim
rotary_dim
max_position_embeddings
position_ids_digest
apply_to_q/apply_to_k/apply_to_v
```

It does not seal a pair map or a convention ID.

Two mathematically incompatible kernels can therefore consume the same current authority receipt.

## 2.3 Current WGSL is adjacent-interleaved

The current WGSL computes:

```wgsl
let lane0 = pair_index * 2u;
let lane1 = lane0 + 1u;
```

This pairs:

```text
(0,1), (2,3), (4,5), ...
```

R5-R5 names this convention:

```text
InterleavedAdjacent
```

## 2.4 Current CPU-f64 reference mirrors adjacent-interleaved

The CPU reference loops:

```rust
for lane0 in (0..head_dim).step_by(2) {
    let lane1 = lane0 + 1;
}
```

GPU and CPU can therefore produce a clean parity receipt while remaining externally wrong.

## 2.5 Frequency schedule is already structurally compatible

The current GPU and CPU use:

```text
frequency = theta ^ (-lane0 / head_dim)
```

For adjacent pairs where `lane0 = 2i`, this is equivalent to:

```text
inv_freq[i] = theta ^ (-2i / rotary_dim)
```

The frequency values may be correct while their assigned lanes are wrong.

This is why pairing and frequency schedule must be separately sealed.

## 2.6 Q/K unequal physical domains are already separated

R5-R4 already separates:

```text
Q head count / Q width / Q bytes
KV head count / KV width / KV bytes
Q RoPE dispatch count
K RoPE dispatch count
```

R5-R5 must preserve that separation while changing the within-head pair map.

## 2.7 Fixture theta is not production checkpoint evidence

The current synthetic fixture authors:

```text
rope_theta = 10000.0
rope_kind = rope
rope_scaling = none
```

That proves fixture consistency only.

R5-R5 must load a pinned local external configuration snapshot and bind the exact source bytes into the authority. It must not claim that a matching fixture literal proves checkpoint provenance.

---

# 3. External evidence boundary

## 3.1 Review-time external observation

The intended TinyLlama family configuration declares, at review time:

```text
architecture             LlamaForCausalLM
model_type               llama
hidden_size              2048
num_attention_heads      32
num_key_value_heads       4
rope_theta               10000.0
rope_scaling             null
max_position_embeddings  2048
```

The reviewed Llama implementation uses:

```text
