# ASH-BASETRAIN-BT-QWAVE-STRUCTURE-05

## R04 Exact Physical Parent / Canonical CJI Syllable Vector Binding / Canonical Ordered Primitive Stream Binding / QW01 Syllable Cell Root Rebase / QW02 Structural Pulse Vector Rebase / QW03 R04-Transition-Owned Inter-Syllable Dynamics / QW04 Maximal Connected Hangul-Run Eojeol Chain / QW05 Span-Bound Morph Overlay Candidate / QW06 Ordered Sentence Transition Graph Candidate / Static CJI vs Dynamic Q-wave Authority Separation / Legacy ASH·KRTTS QW01~QW06 Comparison and Selective Transplant / Zero Hidden Fusion / Zero Logit Mutation / Zero Sampler Mutation / Zero Medusa Prediction / Zero Model Forward / Zero Training Mutation Seal

> Revision: `BT-QWAVE-STRUCTURE-05`
>
> Parent SSOT: `ASH-BASETRAIN-BT-CHEONJIIN-STRUCTURE-04` physical PASS
>
> Parent map revision: `ASH-CJI-PRIMITIVE-MAP-V1`
>
> Parent map digest: `b002e9501611ca19f314938b8c48c9e1665e53674cf307a42874b7bd25d2cbe5`
>
> Parent physically observed: CJI rows=8, vector dim=18, CJI transitions=4, multi-CJI token count=1, legacy LUT authority=0
>
> Canonical static language structure: R03 + R04 only
>
> Q-wave authority class: deterministic derived dynamics, not replacement orthographic truth
>
> Legacy ASH/KRTTS QW01~QW06: comparison/transplant source, never automatic canonical override
>
> Hidden fusion: BLOCKED
>
> Logit mutation: BLOCKED
>
> Sampler mutation: BLOCKED
>
> Structural Medusa prediction: BLOCKED
>
> Model forward/loss/backward/optimizer/weight mutation: BLOCKED
>
> Proof ledger: `HOLD`

---

# 0. Status vocabulary

```text
CANONICAL-STATIC
  exact parent structural truth owned by R03/R04

DERIVED-DYNAMIC
  deterministic Q-wave value derived from canonical-static parents

EDGE-OWNED
  edge membership inherited from an already admitted parent ledger

BOUNDARY-DERIVED
  boundary metadata derived from exact parent span/gap ledgers, never substring search

CONTEXT-CANDIDATE
  morphology/sentence-level interpretation that is useful but not linguistic ground truth

COMPARISON-ONLY
  legacy implementation output that may be measured but cannot override the new route

TRANSPLANT-ELIGIBLE
  legacy mechanism whose contract can be retained after its parent inputs are rebound

BLOCKED
  no active authority and no same-operation fallback
```

R05 is the first stage that gives the Korean structural stack an explicit **dynamic state**.

R03 answers what the Hangul composition is.
R04 answers where its static C/J/I structure lies.
R05 answers how that structure is represented as local pulse and relational flow.

---

# 1. Goal

`BT-QWAVE-STRUCTURE-05` must construct a deterministic QW01→QW06 structure graph from the physically admitted R04 authority without reintroducing legacy `HangulFeatureRow` heuristics as root truth.

Required chain:

```text
R04 exact CJI row + ordered primitive streams
        ↓
QW01 rebased syllable cell
        ↓
QW02 rebased pulse vector
        ↓
R04 exact inter-syllable edge membership
        ↓
QW03 dynamic transition values
        ↓
QW04 maximal transition-connected chain
        ↓
QW05 span-bound morph overlay candidate
        ↓
QW06 ordered sentence graph candidate
```

No stage may mutate R03/R04.

---

# 2. Parent physical admission

R05 accepts exactly one physically passing R04 parent session.

Required parent conditions:

```text
parent_r04_physical_pass = 1
parent_hangul_authority_bound = 1
parent_structure_row_count > 0
parent_jamo_atom_ledger_bound = 1
map_revision = ASH-CJI-PRIMITIVE-MAP-V1
map_digest = b002e9501611ca19f314938b8c48c9e1665e53674cf307a42874b7bd25d2cbe5
primitive_map_missing_atom_count = 0
atom_order_mismatch_count = 0
cji_row_count = parent R03 structure_row_count
cji_vector_dim = 18
discrete_to_continuous_mismatch_count = 0
nonfinite_cji_value_count = 0
token_binding_mismatch_count = 0
nonadjacent_transition_count = 0
nonfinite_transition_value_count = 0
legacy_lut_authority = 0
legacy_canonical_override_count = 0
legacy_blend_count = 0
reproducibility_match = 1
qwave = 0
hidden_fusion = 0
logit_mutation = 0
sampler_mutation = 0
model_forward = 0
loss = 0
backward = 0
optimizer = 0
weight_mutation = 0
```

Latest observed parent fixture:

```text
CJI row count                = 8
CJI vector dimension        = 18
R04 adjacent transition count = 4
multi-CJI token count       = 1
multi-token CJI row count   = 0
```

R05 code derives these values from the parent. They are not architecture constants except vector dimension 18 under R04 V1.

---

# 3. Parent lineage rule

R05 invokes exactly one R04 parent session.

Through that single session it may read the already-bound immutable lineage needed for span/boundary provenance:

```text
R04 CJI authority
R03 Hangul structure authority
R02 token-span alignment authority
R01 normalized-text/tokenizer lineage
```

R05 must not independently re-run:

```text
R01 tokenization
R02 span alignment
R03 Hangul structure build
R04 Cheon-Ji-In build
```

No source text retokenization is permitted.

---

# 4. Static CJI and dynamic Q-wave are different authorities

This separation is mandatory.

```text
R04 static authority
  primitive streams
  discrete role basis
  18D CJI vector
  exact adjacent CJI edge membership/delta

R05 dynamic authority
  pulse direction
  amplitude
  phase
  pressure
  closure
  resonance
  onset/vowel/coda dynamic components
  transition flow/energy
  chain-level binding values
  contextual overlays/graph features
```

R05 never writes a replacement CJI vector.

Required runtime fields:

```text
parent_cji_mutation_count = 0
parent_primitive_stream_mutation_count = 0
static_cji_recompute_count = 0
legacy_cji_root_used = 0
```

---

# 5. Why legacy QW01/QW02 cannot remain the root

Existing ASH/KRTTS QW01 consumes `HangulFeatureRow` values such as:

```text
cheon_core
ji_support
in_bridge
syllable_mass
curvature_bias
coda_weight
axis_bits
```

and builds pulse seeds from those heuristic floats.

Existing QW02 then derives:

```text
direction_cheon/direction_ji/direction_in
amplitude
phase
pressure
closure
resonance
onset_push
vowel_flow
coda_drag
```

from the legacy seed.

That root is no longer admissible because R04 established a newer static authority from exact R03 atom topology.

Therefore:

```text
legacy QW01 seed source            RETIRED from R05 canonical route
legacy QW02 input seed             RETIRED from R05 canonical route
QW01/QW02 output concept           RETAINED
QW01/QW02 parent source            REBASED to R03/R04
```

---

# 6. R05 policy versioning

All dynamic formulas are project policies, not Unicode truth.

Required revisions:

```text
ASH-QW01-CJI-CELL-REBASE-V1
ASH-QW02-STRUCTURAL-PULSE-V1
ASH-QW03-CJI-TRANSITION-V1
ASH-QW04-CHAIN-V1
ASH-QW05-MORPH-OVERLAY-V1
ASH-QW06-SENTENCE-GRAPH-V1
```

Each policy serializes every mode, scalar constant, field order, and boundary flag into a policy digest.

A policy table/formula change requires either:

```text
new revision
```

or a gate-breaking expected digest change explicitly admitted by a later patch.

No hidden constants outside the policy module may affect canonical R05 results.

---

# 7. QW01 rebased syllable cell

R05 QW01 creates exactly one dynamic seed cell per R04 CJI row.

Required cardinality:

```text
QW01 cell count == R04 CJI row count
```

Current fixture expectation:

```text
8
```

Recommended type:

```rust
pub struct BaseTrainQWaveSyllableCellV1 {
    pub cell_index: u32,

    pub parent_cji_row_index: u32,
    pub parent_cji_row_digest: String,
    pub parent_structure_row_index: u32,
    pub parent_structure_digest: String,

    pub normalized_scalar_index: u32,
    pub normalized_byte_start: u32,
    pub normalized_byte_end: u32,
    pub scalar: char,
    pub codepoint: u32,
    pub owner_token_positions: Vec<u32>,

    pub onset_primitive_stream: Vec<CjiPrimitive>,
    pub vowel_primitive_stream: Vec<CjiPrimitive>,
    pub coda_primitive_stream: Vec<CjiPrimitive>,

    pub cji_vector_18: [f32; 18],

    pub onset_primitive_count: u32,
    pub vowel_primitive_count: u32,
    pub coda_primitive_count: u32,
    pub has_coda: bool,

    pub ordered_phasor_re: f32,
    pub ordered_phasor_im: f32,
    pub ordered_phasor_norm: f32,

    pub cell_policy_id: String,
    pub cell_policy_digest: String,
    pub cell_digest: String,
}
```

QW01 does not yet publish final amplitude/phase/pressure.

It publishes structurally sufficient deterministic seeds.

---

# 8. QW01 primitive phasor seed

To preserve primitive order without depending on legacy curvature heuristics, define a project phasor basis:

```text
Cheon angle = 0
Ji angle    = 2π/3
In angle    = 4π/3
```

For each role stream, each primitive contributes its unit phasor multiplied by an order weight.

Default V1 order weight:

```text
w_k = (k + 1) / n
```

Role weights are explicit policy constants.

The total ordered phasor is:

```text
Z = Σ_role role_weight * Σ_k w_k * exp(i * primitive_angle)
```

Store:

```text
ordered_phasor_re
ordered_phasor_im
ordered_phasor_norm
```

The phasor is **derived dynamic seed metadata**.
It does not replace R04 ordered first moments.

---

# 9. QW01 static-input provenance

Every cell must bind exact parent digests:

```text
R04 CJI row digest
R04 vector digest
R04 primitive stream/basis digest
R03 structure row digest
R03 atom ledger digest
```

Forbidden QW01 sources:

```text
HangulFeatureRow.cheon_core
HangulFeatureRow.ji_support
HangulFeatureRow.in_bridge
HangulFeatureRow.syllable_mass
HangulFeatureRow.curvature_bias
HangulFeatureRow.coda_weight
legacy axis_bits
CHEON_LUT
JI_LUT
IN_LUT
```

---

# 10. QW02 structural pulse vector

QW02 converts each QW01 cell into one deterministic dynamic pulse.

Required cardinality:

```text
QW02 vector count == QW01 cell count
```

Recommended retained output surface:

```rust
pub struct BaseTrainQWavePulseVectorV1 {
    pub vector_index: u32,
    pub source_cell_index: u32,
    pub source_cell_digest: String,

    pub direction_cheon: f32,
    pub direction_ji: f32,
    pub direction_in: f32,
    pub direction_norm: f32,

    pub amplitude: f32,
    pub phase: f32,
    pub pressure: f32,
    pub closure: f32,
    pub resonance: f32,

    pub onset_push: f32,
    pub vowel_flow: f32,
    pub coda_drag: f32,

    pub finite: bool,
    pub pulse_policy_id: String,
    pub pulse_policy_digest: String,
    pub vector_digest: String,
}
```

Legacy `mass`, `curvature`, and phonetic final-class fields are not required in the canonical R05 pulse vector.

---

# 11. QW02 direction derivation

Extract role-local mean axis triplets from the parent 18D vector:

```text
O = onset mean C/J/I
V = vowel mean C/J/I
C = coda mean C/J/I
```

V1 raw direction:

```text
D_raw = w_o * O + w_v * V + w_c * C
```

Only present roles participate.
The policy stores `w_o`, `w_v`, `w_c`.

Normalize with L2 when norm exceeds epsilon:

```text
D = D_raw / ||D_raw||
```

Zero norm produces exact zero direction with a typed neutral-direction receipt. It does not invoke legacy CJI fallback.

---

# 12. QW02 phase derivation

Phase comes from the QW01 ordered primitive phasor:

```text
phase = atan2(ordered_phasor_im, ordered_phasor_re)
```

Canonical range:

```text
(-π, π]
```

If phasor norm is below epsilon:

```text
phase = 0
phase_neutral = true
```

No `curvature_bias`, normalized Jamo index, or legacy `axis_bits` contributes to R05 phase.

---

# 13. QW02 onset/vowel/coda dynamic components

V1 derives three role-local strengths from exact primitive counts and role vectors.

Required properties:

```text
finite
non-negative
absent coda -> coda_drag = 0
no role can read another role's parent slice by mistake
```

Recommended policy form:

```text
onset_push = f(role_norm(O), onset_primitive_count)
vowel_flow = f(role_norm(V), vowel_primitive_count)
coda_drag  = f(role_norm(C), coda_primitive_count) when coda present else 0
```

The exact `f` is versioned and digest-bound in `ASH-QW02-STRUCTURAL-PULSE-V1`.

R05 must expose raw component inputs in the receipt so the formula is auditable.

---

# 14. QW02 closure

Closure is derived from exact R03/R04 coda topology, never old `coda_weight`.

V1 closure source inputs:

```text
has_coda
coda_atom_count
coda_primitive_count
coda role vector norm
compound-coda topology flag
```

Required monotonic structural condition:

```text
no coda -> structural closure base = 0
coda present -> structural closure base > 0
```

No claim is made that this value is a phonetic stop-closure probability.
It is a Q-wave structural closure coordinate.

---

# 15. QW02 amplitude, pressure, resonance

These are deterministic dynamic coordinates, not acoustic measurements.

V1 policy must derive:

```text
amplitude
  from normalized structural direction strength + role-complexity contribution

pressure
  from onset_push + vowel_flow + coda_drag with policy weights

resonance
  from role/axis balance and primitive-stream coherence
```

Required:

```text
all outputs finite
explicit clamps documented in policy
no data-dependent silent fallback
no legacy seed input
```

Every clamp hit count is published.

---

# 16. QW02 numerical receipt

Required counters:

```text
pulse_vector_count
neutral_direction_count
neutral_phase_count
amplitude_clamp_count
pressure_clamp_count
closure_clamp_count
resonance_clamp_count
nonfinite_pulse_value_count
```

Physical PASS requires:

```text
nonfinite_pulse_value_count = 0
```

Clamp counts are observations and do not automatically fail unless a policy-specific maximum is explicitly set.

---

# 17. QW03 edge membership authority

This is a critical R05 rule.

**QW03 must not rediscover adjacency from text.**

R04 already publishes exact adjacent CJI transitions.

Therefore:

```text
QW03 edge membership == R04 transition ledger membership
```

Required current fixture expectation:

```text
QW03 edge count = 4
```

because R04 physically observed four adjacent CJI transitions.

Any mismatch is fatal.

---

# 18. QW03 parent binding

Each QW03 edge binds:

```text
source R04 transition digest
from CJI row digest
to CJI row digest
from QW02 vector digest
to QW02 vector digest
```

Recommended output fields:

```text
pulse_delta
phase_delta
direction_alignment
amplitude_transfer
pressure_delta
closure_release
coda_to_onset_bridge
resonance_carry
flow_continuity
transition_energy
```

No QW03 edge exists where R04 has no transition.

---

# 19. QW03 phase delta

Use wrapped angular delta:

```text
Δφ = wrap_to_pi(phi_to - phi_from)
phase_delta = abs(Δφ)
```

No degree/radian ambiguity is permitted.
Policy stores unit=`radian` and wrap range.

---

# 20. QW03 direction/pulse delta

Recommended deterministic terms:

```text
direction_delta = ||D_to - D_from||_2
amplitude_delta = abs(A_to - A_from)
pulse_delta = sqrt(direction_delta² + amplitude_delta²)
```

`direction_alignment` is the clamped dot product of normalized directions when both are non-neutral.

Neutral direction cases are explicit and counted.

---

# 21. QW03 closure release and coda bridge

These values use exact role separation:

```text
closure_release
  = from.closure against to.onset_push

coda_to_onset_bridge
  = from.coda_drag against to.onset_push
```

No phonological coda rewrite occurs.

The exact V1 formula and clamps are policy-digest bound.

---

# 22. QW03 resonance carry and flow continuity

`resonance_carry` measures retained pulse compatibility across an admitted R04 edge.

`flow_continuity` combines:

```text
direction alignment
phase continuity
amplitude continuity
resonance carry
```

All weights are explicit policy fields.

No morphology is used in QW03.

---

# 23. QW03 transition energy

Transition energy is a weighted non-negative combination of:

```text
direction delta
amplitude delta
phase delta
pressure delta
closure release mismatch
coda bridge mismatch
resonance discontinuity
```

Required bounds are explicit in policy.

`transition_energy` is a derived Q-wave metric, not a physical energy measurement.

---

# 24. Neutral zero-edge semantics

KRTTS contains a useful repair not present in the older ASH copy: a valid input with zero admitted adjacent pairs can publish a neutral transition batch instead of raising a hard error.

R05 adopts this semantics.

Required:

```text
R04 transition count = 0
→ QW03 batch edge_count = 0
→ decision = NoAdjacentSyllablePairsFound
→ guard_passed = true
→ QW04 readiness preserved
```

This is a **selective KRTTS transplant**.

It does not weaken parent edge authority.

---

# 25. QW04 chain membership

R05 QW04 does not rediscover words through substring search.

A QW04 chain is a maximal ordered connected component of QW01 cells under admitted QW03 edges.

For linear scalar order:

```text
cell A -- admitted QW03 edge -- cell B
```

keeps A and B in one chain.

A missing QW03 edge creates a chain boundary.

Thus QW04 chain membership is determined by already-proven R04/QW03 adjacency.

---

# 26. QW04 chain boundary metadata

Chain boundary metadata may additionally bind exact parent evidence inherited through the R04 session:

```text
R02 normalized gaps
R02 token/material spans
R02 synthetic anchors
exact normalized scalar indices
```

No `.find()`, `.rfind()`, decode-based reverse alignment, or fuzzy surface search is permitted.

Boundary classifications such as whitespace/punctuation/protected anchor are derived only at exact parent spans.

---

# 27. QW04 naming caution

The existing type name `QWaveEojeolChain` may be retained for compatibility, but R05 physical PASS does **not** prove Korean morphological eojeol truth.

R05 QW04 authority means:

```text
maximal Q-wave-connected Hangul structural run
```

Any stronger linguistic interpretation belongs to a separate morph authority.

Recommended receipt field:

```text
eojeol_semantics = qwave_connected_run_candidate
```

---

# 28. QW04 aggregate fields

A chain may aggregate:

```text
pulse sum C/J/I
pulse mean C/J/I
amplitude sum/mean
circular phase mean
pressure sum/mean
closure sum/mean
resonance mean
transition energy sum/mean
flow continuity mean
boundary open
boundary close
binding energy
```

All fields derive from QW02/QW03.

No R04 static vector is modified.

---

# 29. QW04 circular phase mean

Do not arithmetic-average wrapped phases.

Required:

```text
mean_phase = atan2(mean(sin(phi_i)), mean(cos(phi_i)))
```

Neutral case is explicit when vector resultant norm is below epsilon.

---

# 30. QW04 current fixture expectation

Because the latest R04 parent has:

```text
8 CJI rows
4 admitted adjacent transitions
```

and the transition graph is an ordered acyclic chain graph, current expected connected component count is:

```text
QW04 chain count = 8 - 4 = 4
```

The gate should derive this from graph connectivity and assert it against the produced chain count.

Do not hardcode `4` as a general constant.

---

# 31. QW05 morphology authority class

R05 QW05 is **CONTEXT-CANDIDATE**, not canonical morphology truth.

It may consume the existing ASH/KRTTS morph lattice builder if and only if:

```text
one lattice binds one exact QW04 chain
lattice surface == exact chain surface
best path exists
morph pieces exactly cover the chain span
no node crosses the chain boundary
no missing-node autofill
no cross-chain overlay
```

The canonical QW01-QW04 path must remain valid independent of QW05 interpretation.

---

# 32. QW05 KRTTS multi-lattice transplant

KRTTS adds a live builder that accepts one `MorphLattice` per admitted QW04 chain and publishes one aggregate QW05 batch.

R05 adopts that **multi-lattice binding mechanism** rather than the older single-lattice-only compatibility path.

Required behavior:

```text
lattice_count == QW04 chain_count
zip by exact chain order
surface equality required
span coverage required
cross-chain node = fail
missing lattice = fail when QW05 required
```

This transplant does not promote morph guesses to canonical linguistic truth.

---

# 33. QW05 overlay roles

Existing role kinds may be retained:

```text
Stem
Particle
Ending
Honorific
Title
Vocative
Prefix
Suffix
Unknown
```

Overlay fields may include:

```text
role_pressure
particle_boundary_weight
ending_closure_weight
honorific_modulation
title_addressivity_weight
vocative_call_pressure
pulse_modulation_cheon
pulse_modulation_ji
pulse_modulation_in
boundary_open_adjustment
boundary_close_adjustment
binding_adjustment
overlay_confidence
```

All are derived candidate context features.

---

# 34. QW05 no silent completion

Forbidden:

```text
missing morph autofill
cross-chain morph borrowing
surface substring guessing
role invention to satisfy required role count
canonical CJI rewrite
QW02 pulse rewrite
QW03 edge rewrite
QW04 chain rewrite
```

If QW05 is configured optional and no morph evidence exists, publish an explicit neutral/absent overlay state.

If configured required, missing evidence fails closed.

The chosen mode must be a CLI/policy SSOT, not implicit behavior.

---

# 35. QW06 graph node authority

QW06 nodes are exactly the ordered QW04 chains.

Required:

```text
sentence_graph_node_count == QW04 chain_count
node order == chain order
```

QW06 never invents or removes a QW04 chain.

---

# 36. QW06 edge membership

Graph edges may connect only immediately adjacent QW04 chain indices:

```text
i -> i+1
```

Boundary evidence is inherited from exact parent span/gap classification.

QW05 overlays may modulate edge features but cannot create a non-adjacent edge.

Required:

```text
nonadjacent_sentence_edge_count = 0
```

---

# 37. QW06 candidate semantics

QW06 may compute dynamic candidate features such as:

```text
boundary bridge
particle bridge
ending tension flow
honorific continuity
title/addressivity flow
vocative call pressure
predicate flow
pulse direction alignment
edge pressure
edge binding continuity
edge energy
```

These do not constitute a canonical parse tree or syntactic truth.

Recommended authority label:

```text
qwave_sentence_transition_graph_candidate
```

---

# 38. QW06 sentence boundaries

Sentence-closing punctuation may label an edge boundary only when the exact punctuation span is present in inherited parent evidence.

No textual suffix search such as `ends_with('.')` on reconstructed guessed surfaces is allowed as authority.

A compatibility helper may inspect exact bound surface bytes, but its source span must already be known.

---

# 39. Legacy ASH/KRTTS QW comparison arm

R05 must run a non-authoritative comparison arm for the same admitted input where feasible.

Compare:

```text
QW01 cell cardinality
QW02 direction/amplitude/phase/pressure/closure/resonance
QW03 edge cardinality and dynamic fields
QW04 chain cardinality and binding fields
QW05 overlay cardinality/roles
QW06 graph cardinality/edge fields
```

Required:

```text
legacy_qwave_comparison_enabled = 1
legacy_qwave_authority = 0
legacy_qwave_override_count = 0
legacy_qwave_blend_count = 0
```

Legacy values may differ because their root CJI/heuristic seeds differ.
That difference is observation, not an error by itself.

---

# 40. Selective transplant matrix

R05 explicitly classifies old mechanisms.

```text
Legacy QW01 HangulFeatureRow seed root
  -> RETIRE from canonical route

Legacy QW01 cell identity/receipt concept
  -> TRANSPLANT after R03/R04 rebind

Legacy QW02 output surface
  -> TRANSPLANT

Legacy QW02 old mass/curvature/coda-weight formulas
  -> RETIRE from canonical route

Legacy QW03 transition output surface
  -> TRANSPLANT

Legacy QW03 text-discovered edge membership
  -> RETIRE; R04 owns edges

KRTTS QW03 neutral zero-edge batch behavior
  -> TRANSPLANT

Legacy QW04 chain aggregation concept
  -> TRANSPLANT after graph-membership rebase

KRTTS QW05 per-chain multi-lattice aggregate builder
  -> TRANSPLANT

Legacy QW05 canonical-morph interpretation
  -> NOT ADMITTED

Legacy QW06 ordered graph mechanics
  -> TRANSPLANT with exact boundary provenance
```

---

# 41. R05 authority schema

Recommended top-level model-core authority:

```rust
pub struct BaseTrainQWaveStructureAuthority {
    pub schema_version: u32,

    pub parent_cheonjiin_authority_digest: String,
    pub parent_hangul_authority_digest: String,
    pub parent_alignment_authority_digest: String,
    pub parent_ingress_authority_digest: String,

    pub qwave_policy_set_digest: String,

    pub qw01_cells: Vec<BaseTrainQWaveSyllableCellV1>,
    pub qw02_vectors: Vec<BaseTrainQWavePulseVectorV1>,
    pub qw03_edges: Vec<BaseTrainQWaveTransitionV1>,
    pub qw04_chains: Vec<BaseTrainQWaveChainV1>,
    pub qw05_overlays: Vec<BaseTrainQWaveMorphOverlayV1>,
    pub qw06_graph: BaseTrainQWaveSentenceGraphV1,

    pub static_dynamic_binding_digest: String,
    pub qw01_ledger_digest: String,
    pub qw02_ledger_digest: String,
    pub qw03_ledger_digest: String,
    pub qw04_ledger_digest: String,
    pub qw05_ledger_digest: String,
    pub qw06_ledger_digest: String,
    pub legacy_comparison_digest: String,
    pub authority_digest: String,
}
```

---

# 42. Static/dynamic binding ledger

Every Q-wave layer must retain a path back to R04/R03 static truth.

At minimum:

```text
QW01 cell -> R04 CJI row
QW02 vector -> QW01 cell -> R04 CJI row
QW03 edge -> R04 CJI transition + QW02 endpoints
QW04 chain -> ordered QW01/QW02 nodes + QW03 edges
QW05 overlay -> QW04 chain span
QW06 node -> QW04 chain
QW06 edge -> adjacent QW04 chain pair
```

No floating Q-wave object without parent lineage is publishable.

---

# 43. Token multi-syllable preservation

R05 retains the R04 token→ordered CJI row ledger and derives token→QW01/QW02 bindings.

Required current fixture:

```text
multi_qwave_token_count == R04 multi_cji_token_count == 1
```

One token containing multiple Hangul scalars owns multiple ordered QW01/QW02 rows.

No token-level averaging replaces those rows.

---

# 44. Multi-token scalar preservation

Future R04 rows may be owned by multiple tokenizer positions due to byte fallback.

R05 creates one QW01/QW02 row per scalar/CJI row, not one per token owner.

Required:

```text
multi_token_qwave_row_count == R04 multi_token_cji_row_count
```

Current fixture expectation is zero.

---

# 45. Non-Hangul behavior

R05 does not create fake Hangul pulse cells for non-Hangul material.

Non-Hangul exact spans may contribute only to:

```text
boundary metadata
punctuation boundary classification
protected-span boundary classification
```

when explicitly present in inherited parent ledgers.

No all-zero non-Hangul QW01 cell is inserted into the Hangul pulse sequence.

---

# 46. PAD isolation

PAD remains numerical padding only.

Required:

```text
PAD QW01 cell count = 0
PAD QW02 vector count = 0
PAD QW03 edge count = 0
PAD QW04 chain membership = 0
PAD QW05 overlay count = 0
PAD QW06 node count = 0
```

---

# 47. No hidden/model coupling

R05 may not import or invoke the decoder hidden-state path.

Required counters:

```text
hidden_fusion = 0
hidden_projection = 0
embedding_mutation = 0
model_forward = 0
```

R05 is a structure-side authority only.

---

# 48. No decode coupling

Required:

```text
logit_mutation = 0
sampler_mutation = 0
token_selection_mutation = 0
vocab_mutation = 0
hard_token_mask = 0
```

The later decode structural prior patch is responsible for any candidate interaction.

---

# 49. No Medusa prediction yet

R05 builds the targets/features that Medusa can later learn.

It does not predict future structure.

Required:

```text
medusa_head_count = 0
future_horizon_prediction_count = 0
structural_prediction_loss = 0
```

Natural next stage after R05 is target generation, not live decode mutation.

---

# 50. No training mutation

Required:

```text
loss = 0
backward = 0
optimizer = 0
weight_mutation = 0
checkpoint_mutation = 0
```

R05 can serialize training-target-ready structure, but cannot train from it yet.

---

# 51. Numerical hygiene

All continuous R05 values must be finite.

Required global counters:

```text
nonfinite_qw01_count = 0
nonfinite_qw02_count = 0
nonfinite_qw03_count = 0
nonfinite_qw04_count = 0
nonfinite_qw05_count = 0
nonfinite_qw06_count = 0
```

NaN/Inf never converts to zero silently.
It is a typed failure.

---

# 52. Deterministic double build

Build the full R05 authority twice from the same immutable R04 parent and identical policies.

Required exact equality:

```text
QW01 cells
QW02 vectors
QW03 edges
QW04 chains
QW05 overlays
QW06 graph
all layer digests
policy-set digest
legacy comparison ledger
authority digest
```

No timestamps, pointer addresses, random seeds, unordered map iteration, or filesystem order enter canonical digests.

---

# 53. Parent immutability

Capture before and after:

```text
R04 CJI authority digest
R04 atom expansion digest
R04 role basis digest
R04 vector ledger digest
R04 token binding digest
R04 transition ledger digest
R03 Hangul authority digest
R02 alignment authority digest
R01 ingress authority digest
runtime input sequence authority digest
```

Required unchanged after R05.

---

# 54. Dedicated gate

Add:

```text
ash_basetrain_qwave_structure_05_gate
```

The gate invokes exactly one R04 session.

No decoder/model forward is invoked.

Explicit Cargo `[[bin]]` registration is mandatory under feature:

```text
orchestrator_tcu_audit_bins
```

---

# 55. CLI response file

Add:

```text
specs/cli/ash_basetrain_qwave_structure_05.args
```

Run with the complete parent response chain:

```text
@specs/cli/ash_basetrain_korean_ingress_01.args
@specs/cli/ash_basetrain_token_span_alignment_02.args
@specs/cli/ash_basetrain_hangul_structure_03.args
@specs/cli/ash_basetrain_cheonjiin_structure_04.args
@specs/cli/ash_basetrain_qwave_structure_05.args
```

No alternate source text or tokenizer authority is introduced.

---

# 56. Required policy flags

Required true:

```text
--require-bt-qwave-r04-physical-parent
--require-bt-qwave-static-cji-exact-binding
--require-bt-qwave-primitive-stream-exact-binding
--require-bt-qwave-qw01-r04-root-rebase
--require-bt-qwave-qw02-structural-pulse-rebase
--require-bt-qwave-qw03-r04-edge-membership
--require-bt-qwave-qw03-neutral-zero-edge-admission
--require-bt-qwave-qw04-connected-component-chain
--require-bt-qwave-qw04-parent-gap-span-boundaries
--require-bt-qwave-qw05-chain-lattice-exact-binding
--require-bt-qwave-qw05-no-autofill
--require-bt-qwave-qw06-adjacent-chain-graph
--require-bt-qwave-static-dynamic-separation
--require-bt-qwave-token-multi-syllable-preservation
--require-bt-qwave-multi-token-scalar-preservation
--require-bt-qwave-pad-isolation
--require-bt-qwave-legacy-comparison-arm
--require-bt-qwave-legacy-authority-zero
--require-bt-qwave-reproducibility
--require-bt-qwave-parent-immutability
--require-bt-qwave-zero-hidden-fusion
--require-bt-qwave-zero-logit-mutation
--require-bt-qwave-zero-sampler-mutation
--require-bt-qwave-zero-medusa-prediction
--require-bt-qwave-zero-model-forward
--require-bt-qwave-zero-training-mutation
```

---

# 57. Forbidden policy flags

Required false:

```text
--allow-bt-qwave-hangul-feature-row-root
--allow-bt-qwave-legacy-chellut-root
--allow-bt-qwave-legacy-mass-curvature-root
--allow-bt-qwave-qw03-text-adjacency-rediscovery
--allow-bt-qwave-qw03-edge-outside-r04
--allow-bt-qwave-qw04-substring-boundary-search
--allow-bt-qwave-qw04-chain-outside-qw03-connectivity
--allow-bt-qwave-qw05-missing-morph-autofill
--allow-bt-qwave-qw05-cross-chain-overlay
--allow-bt-qwave-qw06-nonadjacent-chain-edge
--allow-bt-qwave-legacy-canonical-override
--allow-bt-qwave-legacy-blend
--allow-bt-qwave-parent-cji-mutation
--allow-bt-qwave-hidden-fusion
--allow-bt-qwave-logit-mutation
--allow-bt-qwave-sampler-mutation
--allow-bt-qwave-medusa-prediction
--allow-bt-qwave-model-forward
--allow-bt-qwave-training-mutation
```

---

# 58. Error taxonomy

Minimum stable errors:

```text
BTQWaveR04ParentNotPhysicalPass
BTQWaveParentCjiAuthorityMismatch
BTQWaveParentPrimitiveStreamMismatch
BTQWaveParentTransitionLedgerMismatch
BTQWavePolicyDigestMismatch
BTQWaveQW01CardinalityMismatch
BTQWaveQW01ForbiddenLegacyRoot
BTQWaveQW01NonFiniteSeed
BTQWaveQW02CardinalityMismatch
BTQWaveQW02NonFiniteVector
BTQWaveQW03EdgeOutsideParent
BTQWaveQW03EdgeCardinalityMismatch
BTQWaveQW03NonFiniteTransition
BTQWaveQW04ConnectivityMismatch
BTQWaveQW04BoundaryProvenanceMismatch
BTQWaveQW04ChainCardinalityMismatch
BTQWaveQW05MissingMorphLattice
BTQWaveQW05MorphSurfaceMismatch
BTQWaveQW05MorphSpanMismatch
BTQWaveQW05CrossChainOverlay
BTQWaveQW05MissingMorphAutofillForbidden
BTQWaveQW06NodeCardinalityMismatch
BTQWaveQW06NonAdjacentEdge
BTQWaveQW06BoundaryProvenanceMismatch
BTQWaveLegacyAuthorityViolation
BTQWaveStaticCjiMutation
BTQWaveMultiSyllableTokenMismatch
BTQWaveMultiTokenScalarMismatch
BTQWavePadOwnershipNonZero
BTQWaveNonFiniteValue
BTQWaveReproducibilityMismatch
BTQWaveParentAuthorityMutation
BTQWaveForbiddenHiddenFusion
BTQWaveForbiddenLogitMutation
BTQWaveForbiddenSamplerMutation
BTQWaveForbiddenMedusaPrediction
BTQWaveForbiddenModelForward
BTQWaveForbiddenTrainingMutation
```

No error invokes a silent compatibility fallback.

---

# 59. Runtime receipts

Default directory:

```text
workspace/runtime/basetrain/qwave_structure/05
```

Required receipts:

```text
parent_binding_receipt.json
qwave_policy_set_receipt.json
qw01_cell_ledger.json
qw02_pulse_vector_ledger.json
qw03_transition_ledger.json
qw04_chain_ledger.json
qw05_morph_overlay_ledger.json
qw06_sentence_graph_receipt.json
static_dynamic_binding_receipt.json
legacy_qwave_comparison_receipt.json
reproducibility_receipt.json
final_receipt.json
```

Do not emit full normalized source text by default.

---

# 60. Required receipt digests

At minimum:

```text
qw01_cell_ledger_digest
qw02_pulse_ledger_digest
qw03_transition_ledger_digest
qw04_chain_ledger_digest
qw05_overlay_ledger_digest
qw06_graph_digest
static_dynamic_binding_digest
legacy_qwave_comparison_digest
qwave_policy_set_digest
qwave_structure_authority_digest
```

---

# 61. Physical PASS terminal evidence

Expected shape:

```text
[bt-qwave-structure-05]
parent_r04_physical_pass=1
parent_cji_authority_bound=1
parent_cji_row_count=8
parent_cji_vector_dim=18
parent_cji_transition_count=4
parent_primitive_stream_bound=1
static_cji_recompute_count=0
parent_cji_mutation_count=0
parent_primitive_stream_mutation_count=0

qw01_policy_revision=ASH-QW01-CJI-CELL-REBASE-V1
qw01_cell_count=8
qw01_parent_binding_mismatch=0
qw01_forbidden_legacy_root_count=0
qw01_nonfinite_seed_count=0

qw02_policy_revision=ASH-QW02-STRUCTURAL-PULSE-V1
qw02_vector_count=8
qw02_nonfinite_value_count=0
qw02_legacy_mass_curvature_input_count=0

qw03_policy_revision=ASH-QW03-CJI-TRANSITION-V1
qw03_edge_membership_owner=r04_transition_ledger
qw03_parent_edge_count=4
qw03_edge_count=4
qw03_edge_membership_mismatch=0
qw03_text_adjacency_rediscovery_count=0
qw03_nonfinite_value_count=0

qw04_policy_revision=ASH-QW04-CHAIN-V1
qw04_membership_owner=qw03_connected_components
qw04_chain_count=4
qw04_connectivity_mismatch=0
qw04_substring_search_count=0
qw04_nonfinite_value_count=0

qw05_policy_revision=ASH-QW05-MORPH-OVERLAY-V1
qw05_authority_class=context_candidate
qw05_chain_lattice_count=<runtime>
qw05_missing_morph_autofill_count=0
qw05_cross_chain_overlay_count=0
qw05_span_mismatch_count=0
qw05_nonfinite_value_count=0

qw06_policy_revision=ASH-QW06-SENTENCE-GRAPH-V1
qw06_authority_class=context_candidate
qw06_node_count=4
qw06_nonadjacent_edge_count=0
qw06_boundary_provenance_mismatch=0
qw06_nonfinite_value_count=0

multi_qwave_token_count=1
multi_token_qwave_row_count=0
pad_qwave_ownership_count=0

legacy_qwave_comparison_enabled=1
legacy_qwave_authority=0
legacy_qwave_override_count=0
legacy_qwave_blend_count=0

reproducibility_runs=2
reproducibility_match=1
parent_r04_authority_unchanged=1
parent_r03_authority_unchanged=1
parent_r02_authority_unchanged=1
parent_r01_authority_unchanged=1

hidden_fusion=0
logit_mutation=0
sampler_mutation=0
token_selection_mutation=0
medusa_head_count=0
future_horizon_prediction_count=0
model_forward=0
loss=0
backward=0
optimizer=0
weight_mutation=0

qw01_cell_ledger_digest=<sha256>
qw02_pulse_ledger_digest=<sha256>
qw03_transition_ledger_digest=<sha256>
qw04_chain_ledger_digest=<sha256>
qw05_overlay_ledger_digest=<sha256>
qw06_graph_digest=<sha256>
static_dynamic_binding_digest=<sha256>
legacy_qwave_comparison_digest=<sha256>
qwave_policy_set_digest=<sha256>
qwave_structure_authority_digest=<sha256>
proof_ledger=HOLD
```

The current fixture expectations `8/4/4` are derived from the physically observed R04 graph and must still be checked at runtime rather than hardcoded as global constants.

---

# 62. PASS token

```text
PASS_ASH_BASETRAIN_BT_QWAVE_STRUCTURE_05_BT_CHEONJIIN_STRUCTURE_04_PHYSICAL_PARENT_EXACT_CJI_AUTHORITY_VECTOR18_ORDERED_PRIMITIVE_STREAM_AND_R04_TRANSITION_LEDGER_BINDING_STATIC_CJI_CANONICAL_PARENT_DYNAMIC_QWAVE_DERIVED_CHILD_STRICT_AUTHORITY_SEPARATION_QW01_R04_ROOT_REBASE_ZERO_HANGUL_FEATURE_ROW_CJI_ROOT_ZERO_LEGACY_CHEON_JI_IN_LUT_ROOT_ZERO_LEGACY_MASS_CURVATURE_CODA_WEIGHT_ROOT_ORDERED_CJI_PRIMITIVE_PHASOR_SEED_QW02_STRUCTURAL_PULSE_DIRECTION_AMPLITUDE_PHASE_PRESSURE_CLOSURE_RESONANCE_ONSET_VOWEL_CODA_ROLE_SEPARATION_ALL_FINITE_QW03_EDGE_MEMBERSHIP_SINGLE_OWNER_R04_TRANSITION_LEDGER_ZERO_TEXT_ADJACENCY_REDISCOVERY_WRAPPED_PHASE_DELTA_DIRECTION_ALIGNMENT_CLOSURE_RELEASE_CODA_TO_ONSET_BRIDGE_RESONANCE_CARRY_FLOW_CONTINUITY_TRANSITION_ENERGY_KRTTS_ZERO_EDGE_NEUTRAL_BATCH_SEMANTICS_ADOPTED_QW04_MAXIMAL_QW03_CONNECTED_COMPONENT_CHAIN_ZERO_SUBSTRING_BOUNDARY_SEARCH_EXACT_PARENT_GAP_SPAN_BOUNDARY_PROVENANCE_QW05_CONTEXT_CANDIDATE_EXACT_CHAIN_TO_MORPH_LATTICE_BINDING_KRTTS_MULTI_LATTICE_LIVE_BUILDER_TRANSPLANT_ZERO_MISSING_MORPH_AUTOFILL_ZERO_CROSS_CHAIN_OVERLAY_QW06_CONTEXT_CANDIDATE_ORDERED_CHAIN_NODE_AUTHORITY_ADJACENT_CHAIN_EDGES_ONLY_ZERO_NONADJACENT_EDGE_STATIC_DYNAMIC_PARENT_LINEAGE_EXACT_TOKEN_MULTI_SYLLABLE_QWAVE_PRESERVATION_MULTI_TOKEN_SCALAR_SINGLE_QWAVE_ROW_PRESERVATION_PAD_ZERO_QWAVE_OWNERSHIP_LEGACY_ASH_KRTTS_QW01_TO_QW06_COMPARISON_ARM_PRESENT_LEGACY_QWAVE_AUTHORITY_ZERO_OVERRIDE_ZERO_BLEND_ZERO_DOUBLE_BUILD_REPRODUCIBILITY_EXACT_PARENT_AUTHORITIES_UNCHANGED_ZERO_HIDDEN_FUSION_ZERO_LOGIT_MUTATION_ZERO_SAMPLER_MUTATION_ZERO_TOKEN_SELECTION_MUTATION_ZERO_MEDUSA_PREDICTION_ZERO_MODEL_FORWARD_ZERO_LOSS_ZERO_BACKWARD_ZERO_OPTIMIZER_ZERO_WEIGHT_MUTATION_PROOF_LEDGER_HOLD_SEALED
```

---

# 63. Static closure checks before bake

Required static checks include:

```text
R04 parent session invocation count = 1
independent R01/R02/R03 rebuild count = 0
R04 CJI authority exact binding present
R04 primitive stream exact binding present
R04 transition edge ownership present
QW01 cardinality derived from R04 rows
QW01 legacy HangulFeatureRow seed root absent
QW01 CHEON_LUT/JI_LUT/IN_LUT root absent
QW01 ordered phasor seed present
QW02 single project route present
QW02 legacy mass/curvature/coda-weight root absent
QW02 role separation present
QW03 membership loop iterates R04 transitions, not text pairs
QW03 zero-edge neutral batch semantics present
QW04 connected-component/maximal-run membership present
QW04 `.find()`/`.rfind()` membership search absent
QW04 exact parent span/gap boundary binding present
QW05 exact one-lattice-per-chain live builder present
QW05 missing-autofill forbidden
QW05 cross-chain overlay forbidden
QW06 nodes exactly QW04 chains
QW06 only i->i+1 edges
static CJI mutation call edge absent
hidden fusion call edge absent
logit mutation call edge absent
sampler mutation call edge absent
Medusa head construction absent
model forward/loss/backward/optimizer call edge absent
double-build reproducibility present
parent immutability receipt present
explicit Cargo bin registration present
```

---

# 64. Physical PASS meaning

A physical R05 PASS proves:

```text
R04 static CJI and primitive topology are bound without recomputation.
Each admitted Hangul scalar receives one R04-rooted QW01 cell and QW02 pulse vector.
QW03 dynamic edges exist exactly where R04 admitted static CJI transitions.
QW04 chains are deterministic maximal components of those edges.
QW05 overlays, when enabled, are exactly span-bound to QW04 chains with no autofill/cross-chain repair.
QW06 graph nodes are exactly QW04 chains and edges are adjacent-only.
Legacy ASH/KRTTS Q-wave outputs are observational only.
The entire QW01→QW06 structure reproduces exactly from the same parent and policies.
```

It does **not** prove:

```text
phonetic correctness
morphological ground truth
syntactic ground truth
speech acoustic quality
language-model accuracy
structural Medusa prediction quality
logit improvement
production inference improvement
```

---

# 65. Admission state after PASS

```text
BT-KOREAN-INGRESS-01
  actual Korean text -> exact token authority                  ADMITTED

BT-TOKEN-SPAN-ALIGNMENT-02
  token <-> exact span <-> Hangul scalar ownership             ADMITTED

BT-HANGUL-STRUCTURE-03
  Hangul scalar -> exact orthographic/Jamo topology            ADMITTED

BT-CHEONJIIN-STRUCTURE-04
  Jamo atoms -> canonical ASH CJI static structure             ADMITTED

BT-QWAVE-STRUCTURE-05
  CJI static structure -> deterministic QW01-QW06 dynamics     ADMITTED on physical PASS

BT-STRUCTURAL-MEDUSA-TARGETS-06A                              BLOCKED
BT-STRUCTURAL-MEDUSA-HEADS-06B                                BLOCKED
BT-STRUCTURAL-MEDUSA-TRAIN-06C                                BLOCKED
DECODE-STRUCTURAL-ATLAS                                       BLOCKED
DECODE-STRUCTURAL-MEDUSA-SHADOW                               BLOCKED
Live structural logit prior                                   BLOCKED
Production inference                                          BLOCKED
Proof ledger                                                   HOLD
```

---

# 66. Natural next patch

```text
ASH-BASETRAIN-BT-STRUCTURAL-MEDUSA-TARGETS-06A

BT-QWAVE-STRUCTURE-05 Exact Physical Parent /
Factor-Separated Structural Target Schema /
Hangul Orthographic Target Binding /
CJI Static Target Binding /
Q-wave Dynamic Target Binding /
Morph·Boundary Candidate Target Masking /
Future Horizon +1·+2·+3·+4 Target Ledger /
End-of-Sequence Horizon Mask /
Token Multi-Syllable Target Preservation /
No Future Token Leakage /
No Medusa Head Yet /
No Training Yet /
No Hidden Fusion /
No Logit Mutation Seal
```

R06A should **serialize future structure targets first** before any learned Medusa head exists.

---

# 67. Architecture seal

> `BT-QWAVE-STRUCTURE-05` is the dynamic-structure bridge between exact Korean composition/CJI truth and later learned Structural Medusa prediction. It does not restore the old Q-wave root. QW01 and QW02 are rebased onto physically admitted R03/R04 structure: exact ordered Jamo/CJI primitive streams, role-separated 18D vectors, and topology. QW03 edge membership is owned solely by the physically admitted R04 transition ledger, preventing a second text-adjacency authority. QW04 chains are maximal connected runs of those edges, with any boundary labels tied only to exact inherited span/gap evidence. QW05 may transplant KRTTS's per-chain multi-lattice live morph builder, but morphology remains a context candidate and cannot repair or overwrite the static/dynamic base. QW06 retains ordered graph mechanics with adjacent-chain edges only and exact boundary provenance. Legacy ASH/KRTTS QW01~QW06 remain a comparison arm with authority zero. No hidden fusion, decode mutation, Medusa prediction, model forward, or training mutation is admitted at this stage.
