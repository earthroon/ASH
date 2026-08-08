# ASH-BASETRAIN-BT-CHEONJIIN-STRUCTURE-04

## R03 Exact Physical Parent / Canonical Jamo Atom → CJI Primitive Map / Onset·Vowel·Coda Separated Basis / Compound Atom Ordered Accumulation / Tense·Compound Topology Preservation / Per-Syllable CJI Vector / Token Multi-Syllable CJI Ledger / Inter-Syllable CJI Delta / Legacy KRTSS LUT Comparison Arm / Legacy LUT Authority Zero / Q-wave Zero / Hidden Fusion Zero / Logit Mutation Zero Seal

> Parent SSOT: `ASH-BASETRAIN-BT-HANGUL-STRUCTURE-03` physical PASS
>
> Primitive map revision: `ASH-CJI-PRIMITIVE-MAP-V1`
>
> Frozen V1 map digest: `b002e9501611ca19f314938b8c48c9e1665e53674cf307a42874b7bd25d2cbe5`
>
> Canonical root: R03 exact Jamo atom topology → ordered C/J/I primitive stream → discrete role basis → deterministic 18D vector
>
> Legacy `CHEON_LUT/JI_LUT/IN_LUT`: comparison-only, authority=0
>
> Q-wave / hidden fusion / logit mutation / sampler mutation / model forward / training mutation: BLOCKED
>
> Proof ledger: HOLD

---

# 1. Goal

R04 interprets the exact R03 Hangul/Jamo topology as a deterministic Cheon-Ji-In structural coordinate system without mutating R03 structure.

For every admitted R03 structure row:

```text
R03 ordered onset/vowel/coda Jamo atoms
  → versioned CJI primitive sequences
  → role-separated discrete sums and first moments
  → deterministic role-local 6D projections
  → fixed 18D syllable CJI vector
```

It also preserves token→multi-syllable ordering, future multi-token scalar ownership, and deterministic adjacent-syllable CJI deltas.

---

# 2. Parent admission

Required parent evidence:

```text
BT-KOREAN-INGRESS-01 physical PASS
BT-TOKEN-SPAN-ALIGNMENT-02 physical PASS
BT-HANGUL-STRUCTURE-03 physical PASS
R03 structure_row_count = parent Hangul scalar count
R03 roundtrip_failure_count = 0
R03 PAD structure ownership = 0
R03 reproducibility = 1
R03 cheonjiin/qwave/g2p/morphology/model_forward/loss/backward/optimizer = 0
```

Latest observed R03 parent:

```text
structure_row_count = 8
modern_precomposed_count = 8
multi_structure_token_count = 1
multi_token_structure_count = 0
discrete_tensor_row_width = 16
```

R04 invokes exactly one R03 parent session. It does not independently rebuild R01/R02/R03 membership or tokenization.

---

# 3. Meaning of canonical

`canonical` means canonical **inside the versioned ASH engineering contract**.

The vowel construction map directly preserves explicit Cheon-Ji-In construction sequences. The consonant map is an explicit ASH stroke-skeleton extension and is not claimed as a universal Unicode, historical, or linguistic standard.

Any map change requires a new revision such as `ASH-CJI-PRIMITIVE-MAP-V2`. V1 table mutation while keeping the V1 name is rejected by the hard expected digest.

---

# 4. Primitive alphabet and roles

```rust
CjiPrimitive = Cheon | Ji | In
CjiRole = Onset | Vowel | Coda
```

Conceptual encoding:

```text
Cheon C = point/dot/oblique/curve-like non-axis primitive in the ASH consonant extension
Ji    J = horizontal/base primitive
In    I = vertical/upright primitive
```

Primitive sequences are authoritative. Count vectors alone are insufficient because `I,C` and `C,I` have identical counts but different construction order.

---

# 5. Vowel leaf map V1

```text
ㅏ -> I C
ㅐ -> I C I
ㅑ -> I C C
ㅒ -> I C C I
ㅓ -> C I
ㅔ -> C I I
ㅕ -> C C I
ㅖ -> C C I I
ㅗ -> C J
ㅛ -> C C J
ㅜ -> J C
ㅠ -> J C C
ㅡ -> J
ㅣ -> I
```

R03 compound vowel atoms are concatenated in exact source atom order. Example:

```text
ㅘ = ㅗ + ㅏ
(C J) + (I C)
→ C J I C
```

No atom sorting or legacy jungseong LUT collapse is permitted.

---

# 6. Consonant stroke-skeleton extension V1

Leaf set:

```text
ㄱ ㄴ ㄷ ㄹ ㅁ ㅂ ㅅ ㅇ ㅈ ㅊ ㅋ ㅌ ㅍ ㅎ
```

Explicit project table:

```text
ㄱ -> J I
ㄴ -> I J
ㄷ -> J I J
ㄹ -> J I J I J
ㅁ -> J I J I
ㅂ -> J I J I J
ㅅ -> C C
ㅇ -> C
ㅈ -> J C C
ㅊ -> J J C C
ㅋ -> J I J
ㅌ -> J J I J
ㅍ -> J J I I
ㅎ -> J C
```

Onset and coda conjoining-Jamo codepoints map to the same leaf identity through explicit finite tables. No font-pixel inference, Unicode-index vector guessing, runtime learning, or corpus fitting is allowed.

---

# 7. R03 compound/tense topology preservation

R03 already decomposes structures such as:

```text
ㄲ → ㄱ + ㄱ
ㅘ → ㅗ + ㅏ
ㄳ → ㄱ + ㅅ
```

R04 expands each R03 atom exactly once, preserves atom ordinal, preserves primitive order within each atom, and preserves atom boundaries in the expansion ledger.

No special-case CJI formula may collapse tense or compound forms after R03 has already exposed their topology.

---

# 8. Discrete role basis

For an ordered primitive stream `p_0 ... p_(n-1)`:

```text
S_r = Σ p_i
M_r = Σ (i+1) * p_i
```

with one-hot primitive numeric encoding:

```text
Cheon = [1,0,0]
Ji    = [0,1,0]
In    = [0,0,1]
```

Each role therefore stores:

```text
present
atom_count
primitive_count
sum_cheon / sum_ji / sum_in
moment_cheon / moment_ji / moment_in
primitive_presence_bits
primitive_stream_digest
basis_digest
```

Onset, vowel, and coda bases never overwrite or collapse into one another.

---

# 9. Deterministic continuous projection

For a present role with `n > 0` primitives:

```text
mean_axis = sum_axis / n
D_n = n(n+1)/2
order_axis = moment_axis / D_n
```

Absent role returns six exact zeros and `present=false` before division.

Role vector:

```text
[cheon_mean, ji_mean, in_mean, cheon_order, ji_order, in_order]
```

Syllable vector:

```text
18D = onset6 + vowel6 + coda6
```

Frozen field-order version:

```text
ash_cji_syllable_vector18_v1
```

The 18D vector is derived only from the discrete basis. One `project6()` route owns the formula and is reused for parity verification.

Required:

```text
discrete_to_continuous_mismatch_count = 0
nonfinite_cji_value_count = 0
```

---

# 10. Per-syllable CJI authority

Each R04 row binds exactly one R03 structure row:

```text
cji_row_index
parent_structure_row_index
parent_structure_digest
normalized_scalar_index
scalar/codepoint
owner_token_positions
onset_basis
vowel_basis
coda_basis
cji_vector_18
vector_field_order_version
vector_digest
row_digest
```

For the current physical parent:

```text
cji_row_count = 8
```

Unsupported/unmapped parent atoms fail closed. No zero-vector or legacy-LUT fallback exists.

---

# 11. Token multi-syllable ledger

R03 token binding order is preserved exactly:

```text
token_position
  → ordered Vec<cj_row_index>
```

Current expected topology:

```text
multi_cji_token_count = 1
multi_token_cji_row_count = 0
```

No token-level mean replaces the ordered row sequence at authority root.

---

# 12. Inter-syllable CJI delta

A transition is created only when:

```text
right.normalized_scalar_index == left.normalized_scalar_index + 1
```

No gap crossing or word/morpheme inference occurs.

Transition fields:

```text
left/right CJI row indices
left/right normalized scalar indices
delta_vector_18 = V_right - V_left
l1_delta
l2_delta
cji_role_change_bits
transition_digest
```

Role change bits are determined by exact role-basis digest changes:

```text
bit0 onset changed
bit1 vowel changed
bit2 coda changed
```

No phase, pressure, resonance, flow, energy, or other Q-wave dynamics are computed in R04.

---

# 13. Legacy KRTSS comparison quarantine

Existing legacy values may be observed through a dedicated comparison API:

```text
legacy_cheon_core
legacy_ji_support
legacy_in_bridge
legacy_axis_bits
```

Every comparison record has:

```text
legacy_authority = false
```

Required runtime invariants:

```text
legacy_comparison_enabled = 1
legacy_lut_authority = 0
legacy_canonical_override_count = 0
legacy_blend_count = 0
```

Canonical calculation modules contain no `CHEON_LUT`, `JI_LUT`, `IN_LUT`, or `derive_cheon_ji_in` call edge. Legacy values cannot repair, blend, clamp, or override canonical CJI output.

---

# 14. Reproducibility and immutability

Build the R04 authority twice from one immutable R03 parent.

Required exact matches:

```text
map digest
atom expansion ledger
role basis ledger
18D rows
token bindings
transitions
legacy comparison ledger
authority digest
```

Parent digests captured before and verified unchanged after R04:

```text
R03 Hangul authority
R03 structure-row ledger
R03 Jamo-atom ledger
R03 token-binding ledger
R03 u32x16 tensor pack
R02 alignment authority
R01 ingress authority
runtime input sequence authority
```

---

# 15. Implementation surface

```text
crates/tokenizer_core/src/cheonjiin_primitive_map.rs
crates/tokenizer_core/src/hangul_tensor.rs
crates/tokenizer_core/src/lib.rs
crates/model_core/src/base_train_cheonjiin_structure_authority.rs
crates/model_core/src/lib.rs
crates/orchestrator_local/src/base_train_cheonjiin_structure_04.rs
crates/orchestrator_local/src/bin/ash_basetrain_cheonjiin_structure_04_gate.rs
crates/orchestrator_local/Cargo.toml
specs/cli/ash_basetrain_cheonjiin_structure_04.args
```

No JS/TS/Python enters BaseTrain core/runtime code.

---

# 16. Runtime receipts

Default directory:

```text
workspace/runtime/basetrain/cheonjiin_structure/04
```

Receipts:

```text
parent_binding_receipt.json
primitive_map_receipt.json
atom_expansion_ledger.json
role_basis_ledger.json
syllable_cji_vector_ledger.json
token_cji_binding_ledger.json
cji_transition_ledger.json
legacy_krtss_comparison_receipt.json
reproducibility_receipt.json
final_receipt.json
```

---

# 17. Required zero boundaries

```text
Q-wave = 0
G2P = 0
Morphology = 0
Hidden fusion = 0
Logit mutation = 0
Sampler mutation = 0
Model forward = 0
Loss = 0
Backward = 0
Optimizer = 0
Weight mutation = 0
```

R04 is deterministic structural metadata only.

---

# 18. Physical PASS evidence

Expected terminal shape:

```text
[bt-cheonjiin-structure-04]
parent_r03_physical_pass=1
parent_hangul_authority_bound=1
parent_structure_row_count=8
parent_jamo_atom_ledger_bound=1
map_revision=ASH-CJI-PRIMITIVE-MAP-V1
map_digest=b002e9501611ca19f314938b8c48c9e1665e53674cf307a42874b7bd25d2cbe5
primitive_kind_count=3
vowel_leaf_map_count=14
consonant_leaf_map_count=14
primitive_map_missing_atom_count=0
atom_expansion_count=<runtime>
onset_atom_expansion_count=<runtime>
vowel_atom_expansion_count=<runtime>
coda_atom_expansion_count=<runtime>
atom_order_mismatch_count=0
cji_row_count=8
cji_vector_dim=18
discrete_to_continuous_mismatch_count=0
nonfinite_cji_value_count=0
multi_cji_token_count=1
multi_token_cji_row_count=0
token_binding_mismatch_count=0
transition_count=<runtime>
nonadjacent_transition_count=0
nonfinite_transition_value_count=0
legacy_comparison_enabled=1
legacy_record_count=8
legacy_lut_authority=0
legacy_canonical_override_count=0
legacy_blend_count=0
reproducibility_runs=2
reproducibility_match=1
parent_hangul_authority_unchanged=1
parent_alignment_authority_unchanged=1
parent_ingress_authority_unchanged=1
parent_sequence_authority_unchanged=1
qwave=0
hidden_fusion=0
logit_mutation=0
sampler_mutation=0
model_forward=0
loss=0
backward=0
optimizer=0
weight_mutation=0
...
proof_ledger=HOLD
```

---

# 19. PASS token

```text
PASS_ASH_BASETRAIN_BT_CHEONJIIN_STRUCTURE_04_BT_HANGUL_STRUCTURE_03_PHYSICAL_PARENT_EXACT_HANGUL_AUTHORITY_STRUCTURE_ROW_JAMO_ATOM_AND_TOKEN_BINDING_DIGEST_LINEAGE_ASH_CJI_PRIMITIVE_MAP_V1_EXPLICIT_REVISION_AND_DIGEST_THREE_PRIMITIVE_CHEON_JI_IN_ALPHABET_VOWEL_CHEONJIIN_CONSTRUCTION_SEQUENCE_EXACT_CONSONANT_ASH_STROKE_SKELETON_EXTENSION_EXPLICIT_PROJECT_CONVENTION_ZERO_FONT_PIXEL_INFERENCE_ZERO_RUNTIME_MAP_LEARNING_ONSET_VOWEL_CODA_ROLE_SEPARATION_R03_COMPOUND_ATOM_ORDER_PRESERVATION_TENSE_REPEATED_ATOM_PRESERVATION_FINAL_CLUSTER_ORDER_PRESERVATION_ALL_PARENT_JAMO_ATOMS_EXACTLY_MAPPED_ZERO_MISSING_ATOM_FALLBACK_ORDERED_PRIMITIVE_STREAM_AUTHORITY_DISCRETE_AXIS_SUM_AND_FIRST_MOMENT_ACCUMULATION_ORDER_SENSITIVE_ROLE_BASIS_DETERMINISTIC_18D_PER_SYLLABLE_CJI_VECTOR_EXACT_DISCRETE_TO_CONTINUOUS_PARITY_TOKEN_TO_MULTI_SYLLABLE_ORDERED_CJI_LEDGER_MULTI_TOKEN_SCALAR_SINGLE_CJI_ROW_PRESERVATION_ADJACENT_INTER_SYLLABLE_CJI_DELTA_AND_ROLE_CHANGE_BITS_ZERO_QWAVE_DYNAMICS_LEGACY_KRTSS_CHEON_JI_IN_LUT_COMPARISON_ARM_PRESENT_LEGACY_LUT_AUTHORITY_ZERO_LEGACY_OVERRIDE_ZERO_LEGACY_BLEND_ZERO_DOUBLE_BUILD_REPRODUCIBILITY_EXACT_PARENT_AUTHORITIES_UNCHANGED_ZERO_HIDDEN_FUSION_ZERO_LOGIT_MUTATION_ZERO_SAMPLER_MUTATION_ZERO_MODEL_FORWARD_ZERO_LOSS_ZERO_BACKWARD_ZERO_OPTIMIZER_ZERO_WEIGHT_MUTATION_PROOF_LEDGER_HOLD_SEALED
```

---

# 20. Natural next boundary

```text
ASH-BASETRAIN-BT-QWAVE-STRUCTURE-05

BT-CHEONJIIN-STRUCTURE-04 Exact Physical Parent /
Canonical CJI Syllable Vector Binding /
Canonical Discrete Primitive Stream Binding /
QW01 Syllable Cell Rebase /
QW02 Pulse Vector Rebase /
QW03 Inter-Syllable Transition Rebase /
QW04 Eojeol Chain Candidate /
QW05 Morph Overlay Candidate /
QW06 Sentence Graph Candidate /
Static CJI vs Dynamic Q-wave Separation /
KRTTS QW01-QW06 Comparison and Transplant /
No Hidden Fusion Yet /
No Logit Mutation Yet /
No Medusa Prediction Yet Seal
```

R05 must consume R04 canonical CJI rather than recompute Cheon/Ji/In from legacy `HangulFeatureRow` LUTs.
