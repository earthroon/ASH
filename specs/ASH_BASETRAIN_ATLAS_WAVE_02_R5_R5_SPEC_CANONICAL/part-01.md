inv_freq[i] = 1 / theta^(2i / head_dim)
half-split rotation
first half paired with second half
```

These observations guide the registry entry but are not runtime evidence by themselves.

## 3.2 Runtime evidence must be local and pinned

The physical gate must not read a moving network branch.

Required local evidence inputs:

```text
external checkpoint config snapshot
external convention descriptor snapshot
source revision string
source path string
source byte digest
normalization algorithm version
```

The gate reads bytes from local files only.

No HTTP, Git, Hugging Face Hub, package registry, or implicit cache lookup is admitted during the gate.

## 3.3 No architecture-name-only inference

This is forbidden:

```rust
if model_type == "llama" {
    pairing = NeoXHalfSplit;
}
```

unless the mapping is produced by a versioned, digested registry record that is itself part of the gate evidence.

The admitted direction is:

```text
config model_type/architectures
  + registry record
  + registry digest
  + source revision evidence
    -> pairing layout
```

Unknown or ambiguous model families fail closed.

---

# 4. Canonical terminology

R5-R5 uses stable internal enum names. These names define indexing behavior and do not depend on inconsistent naming across third-party libraries.

```rust
pub enum BaseTrainAtlasWave02R5RopePairingLayout {
    NeoXHalfSplit,
    InterleavedAdjacent,
}
```

## 4.1 `NeoXHalfSplit`

For even `rotary_dim = D` and pair index `i`:

```text
0 <= i < D/2
lane_a = i
lane_b = i + D/2
```

Pair map for `D = 4`:

```text
(0,2), (1,3)
```

Pair map for `D = 8`:

```text
(0,4), (1,5), (2,6), (3,7)
```

## 4.2 `InterleavedAdjacent`

For pair index `i`:

```text
lane_a = 2i
lane_b = 2i + 1
```

Pair map for `D = 4`:

```text
(0,1), (2,3)
```

Pair map for `D = 8`:

```text
(0,1), (2,3), (4,5), (6,7)
```

## 4.3 Pairing is not a presentation label

The layout changes which scalar lanes form a complex plane.

The following are semantically different:

```text
same theta
same position
same head dimension
same cosine and sine values
same Q/K buffers
```

when their pair maps differ.

No adapter may relabel one layout as the other without an explicit tensor permutation stage and a receipt proving that permutation.

---

# 5. Frequency and rotation authority

## 5.1 Canonical inverse-frequency schedule

Let:

```text
D = rotary_dim
P = D / 2
0 <= i < P
```

The default schedule is:

```text
inv_freq[i] = theta ^ (-2i / D)
angle(position, i) = position × inv_freq[i]
```

Required validation:

```text
theta finite
theta > 0
D > 0
D <= head_dim
D even
position < max_position_embeddings
```

## 5.2 Canonical two-lane rotation

For a pair `(a,b)` and angle `t`:

```text
y[a] = x[a] × cos(t) - x[b] × sin(t)
y[b] = x[a] × sin(t) + x[b] × cos(t)
```

The sign convention is part of the authority.

R5-R5 does not admit a reverse-sign variant under the same convention ID.

## 5.3 Partial rotary dimension

The authority must carry `rotary_dim` separately from `head_dim`.

For R5-R5 fixture and TinyLlama evidence:

```text
rotary_dim == head_dim
```

If a future model uses `rotary_dim < head_dim`:

```text
lanes [0, rotary_dim)      rotated
lanes [rotary_dim, head_dim) copied bitwise
```

R5-R5 does not promote partial rotary execution. It only prevents the ABI from baking in an unchangeable equality.

## 5.4 Scaling

R5-R5 admits only:

```text
rope scaling = none/default/null-normalized
```

Dynamic, linear, YaRN, LongRoPE, Llama3 scaling, and other schedule mutations remain blocked.

A non-empty scaling object must produce a hard gate failure, not a best-effort fallback.

---

# 6. New external convention authority

R5-R5 introduces:

```rust
pub struct BaseTrainAtlasWave02R5ExternalRopeConventionAuthority {
    pub authority_version: String,

    pub checkpoint_identity_digest: String,
    pub checkpoint_config_path: String,
    pub checkpoint_config_sha256: String,
    pub checkpoint_config_byte_count: u64,

    pub model_spec_id: String,
    pub model_spec_digest: String,
    pub model_type: String,
    pub architectures: Vec<String>,

    pub rope_kind: String,
    pub rope_theta_bits_f64: u64,
    pub rope_scaling_canonical: String,
    pub rope_scaling_digest: String,

    pub head_dim: u32,
    pub rotary_dim: u32,
    pub pairing_layout: BaseTrainAtlasWave02R5RopePairingLayout,
    pub pairing_layout_id: String,
    pub pair_map_digest: String,

    pub frequency_formula_id: String,
    pub sign_convention_id: String,
    pub apply_to_q: bool,
    pub apply_to_k: bool,
    pub apply_to_v: bool,

    pub registry_version: String,
    pub registry_record_id: String,
    pub registry_record_digest: String,
    pub external_source_revision: String,
    pub external_source_path: String,
    pub external_source_evidence_digest: String,

    pub convention_digest: String,
}
```

## 6.1 Required IDs

```text
authority_version
  ash.basetrain.atlas_wave.02.r5.r5.external_rope_convention.v1

pairing_layout_id
  ash.rope.pairing.neox_half_split.v1
  ash.rope.pairing.interleaved_adjacent.v1

frequency_formula_id
  ash.rope.frequency.theta_pow_neg_2i_over_rotary_dim.v1

sign_convention_id
  ash.rope.rotation.xa_cos_minus_xb_sin__xa_sin_plus_xb_cos.v1
```

## 6.2 Authority validation

The authority validates:

```text
checkpoint identity present
config source present
config digest present
model spec lineage present
model family present
theta finite and positive
head_dim even
rotary_dim even
rotary_dim <= head_dim
Q true
K true
V false
registry record present
external source revision pinned
pair map digest recomputable
convention digest recomputable
```

## 6.3 Pair map digest

The pair map digest is computed from a canonical transcript:

```text
domain tag
pairing layout ID
rotary_dim
pair count
for each pair in ascending pair index:
    pair index
    lane_a
    lane_b
```

The digest must not be computed from a human-readable label alone.

---

# 7. ModelSpec extension
