# ASH-BASETRAIN-BT-HANGUL-STRUCTURE-03

## BT-TOKEN-SPAN-ALIGNMENT-02 Physical Parent / Exact Hangul Scalar Reclassification / Modern Precomposed Syllable Canonical Decomposition / Canonical Jamo Role and Composition Topology / Compound Vowel·Final Cluster·Tense-Onset Atom Ledger / Token-to-Multi-Syllable Structure Preservation / Multi-Token Byte-Fallback Scalar Reunification / Discrete U32x16 Structure Tensor Candidate / Exact Round-Trip Composition / Zero Heuristic Acoustic Feature / Zero Cheon-Ji-In / Zero Q-wave / Zero Model-Forward Seal

> Revision: `BT-HANGUL-STRUCTURE-03`
>
> Parent SSOT: `ASH-BASETRAIN-BT-TOKEN-SPAN-ALIGNMENT-02` physical PASS
>
> Parent physical observation: source bytes=28, valid tokens=8, Hangul scalars=8, multi-scalar tokens=1, multi-token scalar count=0, PAD suffix=24
>
> Canonical input authority: `BaseTrainTokenSpanAlignmentAuthority`
>
> Canonical structural unit: one exact normalized Hangul scalar, not one token
>
> Canonical output authority: `BaseTrainHangulStructureAuthority`
>
> Exact decomposition scope: modern precomposed Hangul syllables `U+AC00..U+D7A3`, modern Jamo in `U+1100..U+11FF`, compatibility Jamo in `U+3130..U+318F`
>
> Existing `HangulFeatureRow`, `CHEON_LUT`, `JI_LUT`, `IN_LUT`: reference-only and forbidden as canonical R03 output
>
> Cheon-Ji-In: BLOCKED
>
> Q-wave: BLOCKED
>
> Morphology / G2P: BLOCKED
>
> Model forward / loss / backward / optimizer: BLOCKED
>
> Proof ledger: `HOLD`

---

# 0. Status vocabulary

```text
CANONICAL
  exact structural truth for the explicitly admitted domain

PARENT-BOUND
  copied or derived only from an already admitted parent authority

DISCRETE-DERIVED
  integer packing deterministically derived from canonical structure rows

REFERENCE-ONLY
  existing implementation may be inspected but may not define R03 truth

BLOCKED
  no active authority and no same-operation fallback

EVIDENCE_INSUFFICIENT
  no structural claim is made for an unsupported scalar or mapping
```

R03 creates an exact orthographic composition authority.

It does not create phonetic likelihoods, acoustic weights, semantic scores, Cheon-Ji-In coordinates, Q-wave values, or learned features.

---

# 1. Goal

`BT-HANGUL-STRUCTURE-03` converts the physically admitted Hangul scalar ownership ledger from R02 into a canonical discrete Hangul composition graph.

For each parent Hangul scalar it must answer exactly:

```text
What codepoint is this?
Is it a modern precomposed syllable, modern Jamo, compatibility Jamo, or unsupported Hangul-range scalar?
If precomposed, what exact choseong, jungseong, and optional jongseong compose it?
What are the canonical Jamo codepoints for those slots?
Does its vowel have an exact compound-jamo component structure?
Does its coda have an exact final-cluster component structure?
Does its onset have an exact doubled/tensed composition structure?
Which token positions own this scalar?
Does decomposition compose back to the original scalar exactly?
```

The output must preserve both directions already proven by R02:

```text
one token -> many Hangul structure rows
one Hangul structure row -> many token positions
```

No one-token-one-syllable assumption is admitted.

---

# 2. Parent physical authority

R03 accepts exactly one physically passing R02 parent session.

Required parent conditions:

```text
BT-KOREAN-INGRESS-01 physical parent pass = 1
BT-TOKEN-SPAN-ALIGNMENT-02 physical pass = 1
trace token mismatch = 0
manifest piece mismatch = 0
coverage gap bytes = 0
coverage overlap bytes = 0
PAD source ownership = 0
alignment reproducibility = 1
parent ingress authority unchanged = 1
parent sequence authority unchanged = 1
```

Latest physically observed parent:

```text
source_byte_count           = 28
valid_token_count           = 8
seq_len                     = 32
pad_suffix_count            = 24
material_token_count        = 8
normalized_gap_count        = 3
material_covered_byte_count = 25
gap_byte_count              = 3
hangul_scalar_count         = 8
multi_scalar_token_count    = 1
multi_token_scalar_count    = 0
```

These are current fixture observations, not general architecture constants except where a parent geometry explicitly fixes them.

---

# 3. Why the existing `HangulFeatureRow` cannot be the R03 authority

The current ASH/KRTTS `hangul_tensor.rs` mixes exact composition facts with heuristic continuous features.

Exact portions include:

```text
precomposed syllable decomposition
choseong index
jungseong index
jongseong index
has jongseong
```

The same row also contains derived or heuristic fields:

```text
vowel_openness
frontness
sonority
weight
coda_weight
syllable_mass
curvature_bias
final_consonant_class
cheon_core
ji_support
in_bridge
axis_bits
```

It also derives Cheon-Ji-In from:

```text
CHEON_LUT[21]
JI_LUT[21]
IN_LUT[21]
```

plus openness, sonority, and coda weights.

R03 therefore must not publish `HangulFeatureRow` as canonical structure truth.

Required separation:

```text
R03 canonical truth
  = codepoint + composition topology + ownership

existing HangulFeatureRow
  = reference / later derived feature source only
```

Forbidden R03 call edge:

```text
build_hangul_feature_rows()
```

---

# 4. Scope

R03 must implement and physically prove:

```text
1. exact parent Hangul scalar binding
2. exact codepoint reclassification
3. modern precomposed syllable decomposition
4. modern precomposed syllable exact compose round-trip
5. modern choseong Jamo classification
6. modern jungseong Jamo classification
7. modern jongseong Jamo classification
8. non-modern Jamo preservation without invented modern role
9. compatibility Jamo preservation without silent contextual composition
10. exact onset doubled/tensed composition metadata where defined
11. exact compound-vowel component metadata where defined
12. exact compound-final-cluster component metadata where defined
13. token-to-structure binding preservation
14. multi-token scalar ownership preservation
15. byte-fallback scalar reunification preservation
16. deterministic discrete structure tensor packing
17. double-build reproducibility
18. parent authority immutability
19. zero Cheon-Ji-In calculation
20. zero Q-wave calculation
21. zero model forward
```

---

# 5. Explicit non-goals

R03 does not implement:

```text
Cheon-Ji-In basis
Cheon/Ji/In float coordinates
axis_bits from Cheon/Ji/In thresholds
vowel openness
vowel frontness
sonority
coda pressure weights
syllable mass
curvature bias
phonetic final-consonant classes
G2P rewrite
phonology transition
morphology lattice
eojeol chain
QW01 cell
QW02 pulse
QW03 transition
QW04 eojeol
QW05 morph overlay
QW06 sentence graph
structural Medusa target
structural Medusa head
embedding conditioning
logit prior
model forward
loss
backward
optimizer
```

Those require later authorities.

---

# 6. Canonical scalar ownership source

R03 consumes only:

```rust
BaseTrainTokenSpanAlignmentAuthority::hangul_scalars
```

Every structure row must bind exactly one:

```rust
BaseTrainHangulScalarRef
```

Required exact fields:

```text
normalized_scalar_index
normalized_byte_start
normalized_byte_end
scalar
codepoint
owner_token_positions
ownership_mode
scalar_digest
```

R03 does not rescan the normalized source text to discover additional Hangul scalars.

The R02 ledger is the membership authority.

R03 may reclassify the structural kind from the exact codepoint because R02's `scalar_kind` is only a coarse alignment classification.

---

# 7. R02 coarse classification is not R03 structure truth

Current R02 classification includes:

```text
U+AC00..U+D7AF -> precomposed_hangul_syllable
```

The existing exact decomposition function accepts only:

```text
U+AC00..U+D7A3
```

Therefore R03 must not trust the parent kind string as exact composition authority.

R03 reclassifies from `codepoint`.

Required modern precomposed range:

```text
U+AC00 <= codepoint <= U+D7A3
```

If a parent scalar falls in:

```text
U+D7A4..U+D7AF
```

R03 must fail closed with an unsupported/unassigned structural classification error.

It must not fabricate choseong/jungseong/jongseong indices.

---

# 8. Initial admitted Unicode domains

R03 initial admitted domains:

```text
Modern precomposed Hangul syllables
  U+AC00..U+D7A3

Hangul Jamo block
  U+1100..U+11FF

Hangul Compatibility Jamo
  U+3130..U+318F
```

R03 does not silently expand to:

```text
Hangul Jamo Extended-A U+A960..U+A97F
Hangul Jamo Extended-B U+D7B0..U+D7FF
Halfwidth Hangul
historic composition grammars
archaic conjoining algorithms
```

Those require a later explicit Unicode-domain admission.

---

# 9. Exact modern precomposed constants

Canonical composition constants:

```text
S_BASE = U+AC00
S_END  = U+D7A3
L_BASE = U+1100
V_BASE = U+1161
T_BASE = U+11A7

L_COUNT = 19
V_COUNT = 21
T_SLOT_COUNT = 28
N_COUNT = V_COUNT * T_SLOT_COUNT = 588
S_COUNT = L_COUNT * N_COUNT = 11172
```

R03 may expose these constants in one pure structural module.

They must not be duplicated across orchestrator code.

---

# 10. Canonical decomposition algorithm

For modern precomposed syllable scalar `S`:

```text
SIndex = codepoint(S) - S_BASE
LIndex = SIndex / 588
VIndex = (SIndex % 588) / 28
TSlot  = SIndex % 28
```

Canonical R03 fields:

```text
choseong_index = LIndex       // 0..18
jungseong_index = VIndex       // 0..20
jongseong_slot = TSlot        // 0..27, 0 means no jongseong
jongseong_index = None        if TSlot == 0
jongseong_index = TSlot - 1   otherwise, 0..26
has_jongseong = TSlot != 0
```

No float normalization of these indices occurs in R03.

---

# 11. Canonical Jamo codepoints from decomposition

For a precomposed syllable:

```text
choseong_jamo_codepoint = U+1100 + LIndex
jungseong_jamo_codepoint = U+1161 + VIndex
jongseong_jamo_codepoint = None if TSlot == 0
jongseong_jamo_codepoint = U+11A7 + TSlot otherwise
```

Because R03 uses exact discrete composition, these codepoints become canonical component identities.

Compatibility glyphs are presentation references only and do not replace these canonical conjoining Jamo codepoints.

---

# 12. Exact compose round-trip

R03 must provide one pure inverse composition function.

For each precomposed parent scalar:

```text
decompose(original)
  -> LIndex, VIndex, optional TIndex
  -> compose(...)
  -> reconstructed scalar
```

Required:

```text
reconstructed scalar == original scalar
roundtrip_pass = true
```

Any failure is fatal:

```text
BTHangulStructurePrecomposedRoundTripMismatch
```

R03 cannot publish an authority with a failed round-trip row.

---

# 13. Canonical scalar kind taxonomy

Minimum R03 kinds:

```rust
pub enum BaseTrainHangulScalarStructureKind {
    ModernPrecomposedSyllable,
    ModernChoseongJamo,
    ModernJungseongJamo,
    ModernJongseongJamo,
    HangulJamoOther,
    CompatibilityJamo,
}
```

Unsupported or unassigned Hangul-range codepoints fail before authority publication.

No generic `OtherHangul` value may hide unsupported composition semantics.

---

# 14. Modern Jamo role ranges

R03 exact modern role ranges:

```text
Modern choseong Jamo
  U+1100..U+1112
  count = 19

Modern jungseong Jamo
  U+1161..U+1175
  count = 21

Modern jongseong Jamo
  U+11A8..U+11C2
  count = 27
```

For these direct Jamo scalars, R03 records an exact slot role and role-local index.

Examples:

```text
U+1100 -> choseong index 0
U+1112 -> choseong index 18
U+1161 -> jungseong index 0
U+1175 -> jungseong index 20
U+11A8 -> jongseong index 0
U+11C2 -> jongseong index 26
```

Direct Jamo are not silently composed with neighbors.

---

# 15. Hangul Jamo block outside modern role ranges

Codepoints in:

```text
U+1100..U+11FF
```

that are outside the admitted modern role subranges are preserved as:

```text
HangulJamoOther
```

with:

```text
exact codepoint
exact source span
exact token ownership
role = none/unsupported-modern-role
```

R03 does not invent a modern choseong/jungseong/jongseong index.

This preserves evidence while preventing false modern decomposition.

---

# 16. Compatibility Jamo policy

Compatibility Jamo:

```text
U+3130..U+318F
```

are preserved as exact source scalars.

R03 does not silently convert an isolated compatibility consonant such as `ㄱ` into either:

```text
choseong U+1100
or
jongseong U+11A8
```

because the visible compatibility shape alone does not establish contextual slot ownership.

Canonical R03 representation includes:

```text
scalar_kind = CompatibilityJamo
compatibility_codepoint = exact source codepoint
role_mask = structural candidate mask if an exact table exists
resolved_slot_role = none unless exact source representation proves it
```

No IME-style contextual composition occurs in R03.

---

# 17. No silent Jamo-sequence composition

Input sequence:

```text
ㅎ ㅏ ㄴ
```

must not automatically become:

```text
한
```

inside R03.

Why:

```text
R02 owns exact normalized scalars.
R03 owns exact structure of those scalars.
Composing multiple source scalars would mutate source topology.
```

A later optional Jamo-binding candidate layer may propose compositional groups, but it must remain derived and preserve the original scalar ledger.

---

# 18. Canonical precomposed syllable row

Recommended model-core type:

```rust
pub struct BaseTrainHangulStructureRow {
    pub structure_row_index: u32,

    pub parent_scalar_digest: String,
    pub normalized_scalar_index: u32,
    pub normalized_byte_start: u32,
    pub normalized_byte_end: u32,
    pub scalar: char,
    pub codepoint: u32,
    pub scalar_kind: BaseTrainHangulScalarStructureKind,

    pub owner_token_positions: Vec<u32>,
    pub ownership_mode: String,

    pub choseong_index: Option<u8>,
    pub jungseong_index: Option<u8>,
    pub jongseong_index: Option<u8>,
    pub jongseong_slot: Option<u8>,
    pub has_jongseong: bool,

    pub choseong_jamo_codepoint: Option<u32>,
    pub jungseong_jamo_codepoint: Option<u32>,
    pub jongseong_jamo_codepoint: Option<u32>,

    pub onset_atoms: Vec<BaseTrainHangulJamoAtom>,
    pub vowel_atoms: Vec<BaseTrainHangulJamoAtom>,
    pub coda_atoms: Vec<BaseTrainHangulJamoAtom>,

    pub roundtrip_required: bool,
    pub roundtrip_pass: bool,
    pub reconstructed_codepoint: Option<u32>,

    pub structure_digest: String,
}
```

All optional fields have exact kind-dependent invariants.

---

# 19. Canonical Jamo atom

Recommended atom:

```rust
pub struct BaseTrainHangulJamoAtom {
    pub slot_role: String,
    pub canonical_jamo_codepoint: u32,
    pub component_ordinal: u8,
    pub component_count: u8,
    pub composition_kind: String,
    pub atom_digest: String,
}
```

Allowed `composition_kind` examples:

```text
atomic
repeated_base
compound_vowel_component
compound_final_component
compatibility_unresolved
```

R03 atoms describe exact orthographic composition topology only.

They do not carry acoustic weights.

---

# 20. Tense/doubled onset topology

For modern precomposed syllables whose onset is an exact doubled/tensed orthographic form, R03 may expose component topology.

Required table is explicit and finite.

Conceptual mappings:

```text
ㄲ -> ㄱ + ㄱ
ㄸ -> ㄷ + ㄷ
ㅃ -> ㅂ + ㅂ
ㅆ -> ㅅ + ㅅ
ㅉ -> ㅈ + ㅈ
```

The canonical onset codepoint remains the exact choseong Jamo produced by the syllable decomposition.

Atom expansion is derived topology and never changes the syllable's LIndex.

No claim about phonetic tension strength is made.

---

# 21. Compound vowel topology

R03 may expand exact modern compound vowels into ordered atomic vowel components.

Required explicit mappings include the modern compound set:

```text
ㅘ -> ㅗ + ㅏ
ㅙ -> ㅗ + ㅐ
ㅚ -> ㅗ + ㅣ
ㅝ -> ㅜ + ㅓ
ㅞ -> ㅜ + ㅔ
ㅟ -> ㅜ + ㅣ
ㅢ -> ㅡ + ㅣ
```

Simple vowels remain one atom.

The canonical `jungseong_index` remains the exact 0..20 index from the precomposed syllable.

The atom ledger exists to expose composition topology for later Cheon-Ji-In structure derivation.

---

# 22. Compound final-cluster topology

R03 may expand exact compound jongseong clusters into ordered atomic coda components.

Required modern cluster mappings:

```text
ㄳ -> ㄱ + ㅅ
ㄵ -> ㄴ + ㅈ
ㄶ -> ㄴ + ㅎ
ㄺ -> ㄹ + ㄱ
ㄻ -> ㄹ + ㅁ
ㄼ -> ㄹ + ㅂ
ㄽ -> ㄹ + ㅅ
ㄾ -> ㄹ + ㅌ
ㄿ -> ㄹ + ㅍ
ㅀ -> ㄹ + ㅎ
ㅄ -> ㅂ + ㅅ
```

Simple codas remain one atom.

No phonological simplification is performed.

For example:

```text
ㄳ does not become ㄱ or ㅅ based on pronunciation context in R03.
```

That belongs to G2P/phonology stages.

---

# 23. Doubled coda topology

Exact doubled coda identities such as:

```text
ㄲ
ㅆ
```

may expose repeated-base topology while retaining their canonical jongseong codepoint and index.

Again, this is orthographic composition metadata only.

---

# 24. Role mask

For a canonical structure row R03 may publish a discrete role mask:

```text
bit 0 = choseong role present
bit 1 = jungseong role present
bit 2 = jongseong role present
bit 3 = compatibility representation
bit 4 = direct Jamo representation
bit 5 = precomposed representation
bit 6 = multi-token owner
bit 7 = byte-fallback reunified owner
```

This role mask is exact structural metadata.

It is not the existing Cheon-Ji-In `axis_bits`.

Naming must prevent confusion:

```text
hangul_role_bits
```

not:

```text
axis_bits
```

---

# 25. Parent scalar exact binding

For every R03 row:

```text
row.parent_scalar_digest
== parent.hangul_scalars[i].scalar_digest

row.normalized_scalar_index
== parent.hangul_scalars[i].normalized_scalar_index

row.codepoint
== parent.hangul_scalars[i].codepoint

row.owner_token_positions
== parent.hangul_scalars[i].owner_token_positions
```

Required row count:

```text
R03 structure row count == parent Hangul scalar count
```

For the current physical fixture this should be:

```text
8
```

but code must derive it from the parent.

---

# 26. Ownership preservation

R03 must preserve parent ownership exactly.

If one token owns three Hangul scalars:

```text
token k
  -> structure row a
  -> structure row b
  -> structure row c
```

all rows remain separate.

If one Hangul scalar is represented by multiple byte fallback tokens:

```text
structure row s
  -> owner tokens [k, k+1, k+2]
```

R03 creates one structure row, not three duplicate syllable rows.

---

# 27. Byte-fallback scalar reunification

R02 already proves byte fallback groups reconstruct exact original UTF-8 scalars.

R03 consumes the scalar ownership after that proof.

Required rule:

```text
structure cardinality follows normalized scalar cardinality,
not byte-token cardinality.
```

For parent scalars with multiple owner token positions:

```text
byte_fallback_reunified = true
```

may be recorded as exact provenance.

R03 must not decode the byte tokens a second time to decide scalar identity.

---

# 28. Token-to-structure binding ledger

Recommended type:

```rust
pub struct BaseTrainTokenHangulStructureBinding {
    pub token_position: u32,
    pub token_id: u32,
    pub hangul_structure_row_indices: Vec<u32>,
    pub hangul_structure_count: u32,
    pub binding_digest: String,
}
```

Required:

```text
one binding entry per valid token position
```

Tokens containing no Hangul scalars receive:

```text
hangul_structure_row_indices = []
```

not a synthetic zero structure row.

Ordering follows normalized scalar order.

---

# 29. Multi-syllable token preservation gate

Parent physically observed:

```text
multi_scalar_token_count = 1
```

R03 must preserve the exact parent topology.

Required:

```text
R03 multi-row token count == R02 multi-scalar token count
```

unless a parent scalar is structurally unsupported, in which case the operation fails rather than silently dropping it.

---

# 30. Multi-token scalar preservation gate

Parent current fixture observed:

```text
multi_token_scalar_count = 0
```

The implementation must nevertheless support nonzero future values.

Required:

```text
R03 multi-token-owner structure row count
== R02 multi-token scalar count
```

No duplication by owner token.

---

# 31. No PAD structure rows

PAD positions are numerical sequence padding only.

Required:

```text
PAD structure row count = 0
PAD Jamo atom count = 0
PAD token-to-structure binding indices = []
```

R03 must not manufacture an all-zero Hangul row for PAD.

---

# 32. Discrete structure tensor candidate

R03 may publish a deterministic GPU-friendly discrete packing derived from each canonical structure row.

Recommended row type:

```text
u32[16]
```

Suggested lanes:

```text
0  normalized_scalar_index
1  Unicode codepoint
2  scalar_kind_code
3  hangul_role_bits
4  choseong_index_or_sentinel
5  jungseong_index_or_sentinel
6  jongseong_index_or_sentinel
7  jongseong_slot_or_sentinel
8  has_jongseong
9  onset_atom_count
10 vowel_atom_count
11 coda_atom_count
12 owner_token_count
13 roundtrip_pass
14 byte_fallback_reunified
15 reserved_zero
```

Sentinel:

```text
0xFFFF_FFFF
```

for unavailable index lanes.

This is a **discrete derived pack**, not a learned float tensor.

---

# 33. Why R03 uses integer packing

At this boundary the following are exact categories:

```text
codepoints
indices
component counts
role bits
ownership counts
round-trip booleans
```

Converting them immediately into normalized floats would blur exact symbolic structure and make later feature changes harder to audit.

Therefore:

```text
R03 canonical = discrete
R04 Cheon-Ji-In = derived structural coordinates
R05 Q-wave = derived dynamic values
R06 Medusa = learned prediction surface
```

---

# 34. Tensor pack does not replace row authority

Canonical hierarchy:

```text
BaseTrainHangulStructureRow
        ↓ deterministic projection
u32x16 discrete tensor row
```

The tensor pack may be regenerated.

The semantic row is the authority.

A future GPU atlas may consume the packed rows without redefining their meaning.

---

# 35. Structure tensor digest

Required separate digests:

```text
structure_row_ledger_digest
jamo_atom_ledger_digest
token_structure_binding_digest
discrete_tensor_pack_digest
```

The final `BaseTrainHangulStructureAuthority` binds all four.

---

# 36. Canonical authority schema

Recommended:

```rust
pub struct BaseTrainHangulStructureAuthority {
    pub schema_version: u32,

    pub parent_alignment_authority_digest: String,
    pub parent_hangul_ownership_digest: String,
    pub parent_ingress_authority_digest: String,
    pub tokenizer_identity_digest: String,
    pub normalized_text_sha256: String,

    pub valid_token_count: u32,
    pub parent_hangul_scalar_count: u32,
    pub structure_row_count: u32,

    pub precomposed_syllable_count: u32,
    pub modern_choseong_jamo_count: u32,
    pub modern_jungseong_jamo_count: u32,
    pub modern_jongseong_jamo_count: u32,
    pub hangul_jamo_other_count: u32,
    pub compatibility_jamo_count: u32,

    pub multi_structure_token_count: u32,
    pub multi_token_structure_count: u32,
    pub byte_fallback_reunified_structure_count: u32,

    pub roundtrip_required_count: u32,
    pub roundtrip_pass_count: u32,
    pub roundtrip_failure_count: u32,

    pub structure_rows: Vec<BaseTrainHangulStructureRow>,
    pub token_bindings: Vec<BaseTrainTokenHangulStructureBinding>,
    pub discrete_tensor_rows: Vec<[u32; 16]>,

    pub structure_row_ledger_digest: String,
    pub jamo_atom_ledger_digest: String,
    pub token_structure_binding_digest: String,
    pub discrete_tensor_pack_digest: String,
    pub authority_digest: String,
}
```

---

# 37. Authority publication invariants

Required before publication:

```text
structure_row_count == parent_hangul_scalar_count
roundtrip_failure_count == 0
all parent scalar digests consumed exactly once
all parent owner token positions preserved exactly
all row indices contiguous 0..M-1
all token binding indices valid
all precomposed indices in exact bounds
all direct modern Jamo role indices in exact bounds
all PAD structure ownership zero
all discrete tensor rows cardinality == structure_row_count
```

---

# 38. Pure structural core module

Recommended tokenizer/model-neutral implementation surface:

```text
crates/tokenizer_core/src/hangul_structure_core.rs
```

or an equivalent pure module.

It owns only:

```text
Unicode constants
exact scalar classification
precomposed decompose
precomposed compose
modern Jamo role classification
exact atom expansion tables
```

It must not import:

```text
Q-wave
morphology
runtime sampler
GPU runtime
model hidden state
```

---

# 39. Existing `hangul_tensor.rs` migration rule

Do not duplicate the exact decomposition algorithm in two permanent SSOTs.

Preferred refactor:

```text
hangul_structure_core.rs
  owns exact decompose/compose/classification

hangul_tensor.rs
  imports exact core
  continues to own legacy/reference derived features
```

This lets Q-wave/KRTTS-style existing code continue using decomposition while R03 gets a clean exact structural authority.

---

# 40. Existing heuristic fields remain reference-only

R03 static gate must ensure no output schema contains:

```text
vowel_openness
frontness
sonority
weight
coda_weight
syllable_mass
curvature_bias
cheon_core
ji_support
in_bridge
axis_bits
```

Those names may exist elsewhere in the repository but must not be members of the R03 authority types.

---

# 41. Final consonant classification is deferred

Current `FinalConsonantClass` groups codas into categories such as:

```text
Nasal
Liquid
Stop
Fricative
Affricate
Cluster
```

That is useful later, but it mixes orthographic and phonetic interpretation.

R03 therefore does not publish `FinalConsonantClass`.

R03 publishes exact coda Jamo identity and exact cluster atom topology only.

Later derived structure may classify it with an explicit authority.

---

# 42. No Cheon-Ji-In leakage

R03 must have zero references in its live path to:

```text
CHEON_LUT
JI_LUT
IN_LUT
derive_cheon_ji_in
cheon_core
ji_support
in_bridge
CheonjiinJasoStrokeFacade
```

The next `BT-CHEONJIIN-STRUCTURE-04` consumes the exact R03 Jamo/atom topology.

That ordering is mandatory.

---

# 43. No Q-wave leakage

R03 live call edge must not invoke:

```text
build_qwave_syllable_cells
build_qwave_pulse_vectors
build_qwave_syllable_transitions
build_qwave_eojeol_chains
build_qwave_morph_overlay
build_qwave_sentence_graph
```

or equivalent Q-wave builders.

R03 output can be consumed by R05 later.

---

# 44. No G2P rewrite

R03 describes source-normalized orthography.

It does not mutate a syllable according to pronunciation rules.

Example:

```text
source orthographic coda remains exact source coda
```

G2P rewrite evidence later may refer back to the R03 row but cannot rewrite the canonical R03 row.

---

# 45. No morphology

R03 must not call KRTTS-style:

```text
morph lattice
particle classification
ending classification
honorific classification
addressivity
boundary entropy
```

Those are sentence-level or morph-level derived structures.

R03 remains scalar composition truth.

---

# 46. Tokenizer identity preservation

R03 binds the same frozen tokenizer identity inherited from R02.

It does not load an alternate tokenizer or retokenize input.

Required:

```text
R03 tokenizer_identity_digest == R02 tokenizer_identity_digest
```

---

# 47. Parent authority immutability

Before and after R03 build, capture:

```text
parent alignment authority digest
parent hangul ownership digest
parent ingress authority digest
parent sequence authority digest
parent tokenizer identity digest
```

Required unchanged after publication.

R03 is derived metadata only.

---

# 48. Deterministic double build

R03 builds the exact structure authority twice from the same parent.

Required equality:

```text
structure rows
Jamo atom ledgers
token bindings
discrete tensor rows
all ledger digests
authority digest
```

No timestamp, random seed, pointer address, or hash-map iteration order may enter canonical digests.

---

# 49. Reproducibility receipt

Recommended:

```rust
pub struct BaseTrainHangulStructureReproducibilityReceipt {
    pub schema_version: u32,
    pub build_count: u32,
    pub structure_rows_match: bool,
    pub token_bindings_match: bool,
    pub tensor_rows_match: bool,
    pub structure_ledger_digest_match: bool,
    pub atom_ledger_digest_match: bool,
    pub token_binding_digest_match: bool,
    pub tensor_pack_digest_match: bool,
    pub authority_digest_match: bool,
    pub pass: bool,
    pub receipt_digest: String,
}
```

Required:

```text
build_count = 2
pass = true
```

---

# 50. Dedicated gate

Add:

```text
ash_basetrain_hangul_structure_03_gate
```

It invokes exactly one R02 parent session.

It does not invoke the physical decoder.

The orchestrator crate uses explicit `[[bin]]` registration, so Cargo target registration is mandatory.

---

# 51. CLI response file

Add:

```text
specs/cli/ash_basetrain_hangul_structure_03.args
```

R03 is run together with parent ingress/alignment args:

```text
@specs/cli/ash_basetrain_korean_ingress_01.args
@specs/cli/ash_basetrain_token_span_alignment_02.args
@specs/cli/ash_basetrain_hangul_structure_03.args
```

No new text source or tokenizer source is introduced.

---

# 52. Required policy flags

Required true:

```text
--require-bt-hangul-structure-r02-physical-parent
--require-bt-hangul-structure-parent-scalar-exact-binding
--require-bt-hangul-structure-codepoint-reclassification
--require-bt-hangul-structure-modern-precomposed-exact-range
--require-bt-hangul-structure-exact-lvt-decomposition
--require-bt-hangul-structure-exact-compose-roundtrip
--require-bt-hangul-structure-modern-direct-jamo-role-classification
--require-bt-hangul-structure-compatibility-jamo-noncomposition
--require-bt-hangul-structure-exact-atom-topology
--require-bt-hangul-structure-token-multi-scalar-preservation
--require-bt-hangul-structure-multi-token-scalar-preservation
--require-bt-hangul-structure-byte-fallback-reunification
--require-bt-hangul-structure-pad-isolation
--require-bt-hangul-structure-discrete-u32x16-pack
--require-bt-hangul-structure-reproducibility
--require-bt-hangul-structure-parent-authority-immutability
--require-bt-hangul-structure-zero-heuristic-float-features
--require-bt-hangul-structure-zero-cheonjiin
--require-bt-hangul-structure-zero-qwave
--require-bt-hangul-structure-zero-model-forward
```

---

# 53. Forbidden policy flags

Required false:

```text
--allow-bt-hangul-structure-parent-kind-blind-trust
--allow-bt-hangul-structure-d7a4-d7af-fabrication
--allow-bt-hangul-structure-extended-jamo-silent-admission
--allow-bt-hangul-structure-compatibility-context-guess
--allow-bt-hangul-structure-jamo-sequence-auto-compose
--allow-bt-hangul-structure-token-syllable-collapse
--allow-bt-hangul-structure-byte-token-row-duplication
--allow-bt-hangul-structure-pad-row
--allow-bt-hangul-structure-hangul-feature-row-authority
--allow-bt-hangul-structure-phonetic-final-class
--allow-bt-hangul-structure-heuristic-float-feature
--allow-bt-hangul-structure-legacy-cheon-lut
--allow-bt-hangul-structure-legacy-ji-lut
--allow-bt-hangul-structure-legacy-in-lut
--allow-bt-hangul-structure-chemy-derived-axis-bits
--allow-bt-hangul-structure-qwave
--allow-bt-hangul-structure-g2p
--allow-bt-hangul-structure-morphology
--allow-bt-hangul-structure-model-forward
```

---

# 54. Error taxonomy

Minimum stable errors:

```text
BTHangulStructureParentNotPhysicalPass
BTHangulStructureParentHangulScalarCountMismatch
BTHangulStructureParentScalarDigestMismatch
BTHangulStructureParentScalarOwnerMismatch
BTHangulStructureUnsupportedHangulCodepoint
BTHangulStructureUnassignedPrecomposedRange
BTHangulStructurePrecomposedIndexOutOfRange
BTHangulStructurePrecomposedDecompositionFailed
BTHangulStructurePrecomposedRoundTripMismatch
BTHangulStructureDirectJamoRoleIndexOutOfRange
BTHangulStructureCompatibilityRoleGuessForbidden
BTHangulStructureJamoAutoCompositionForbidden
BTHangulStructureAtomTableMismatch
BTHangulStructureDuplicateParentScalarConsumption
BTHangulStructureMissingParentScalarConsumption
BTHangulStructureTokenBindingMismatch
BTHangulStructureMultiScalarTokenMismatch
BTHangulStructureMultiTokenScalarMismatch
BTHangulStructurePadOwnershipNonZero
BTHangulStructureTensorPackCardinalityMismatch
BTHangulStructureTensorReservedLaneNonZero
BTHangulStructureReproducibilityMismatch
BTHangulStructureParentAuthorityMutation
BTHangulStructureForbiddenHeuristicFeature
BTHangulStructureForbiddenCheonjiin
BTHangulStructureForbiddenQWave
BTHangulStructureForbiddenModelForward
```

No error triggers an automatic structural fallback.

---

# 55. Runtime receipts

Default output:

```text
workspace/runtime/basetrain/hangul_structure/03
```

Required receipts:

```text
parent_binding_receipt.json
scalar_reclassification_receipt.json
precomposed_roundtrip_receipt.json
jamo_atom_ledger.json
token_structure_binding_ledger.json
discrete_tensor_pack_receipt.json
reproducibility_receipt.json
final_receipt.json
```

Do not emit complete source text by default.

---

# 56. Scalar reclassification receipt

Recommended fields:

```text
parent_hangul_scalar_count
modern_precomposed_count
modern_choseong_jamo_count
modern_jungseong_jamo_count
modern_jongseong_jamo_count
hangul_jamo_other_count
compatibility_jamo_count
unsupported_count
unassigned_precomposed_range_count
```

Required:

```text
unsupported_count = 0
unassigned_precomposed_range_count = 0
```

for physical PASS.

---

# 57. Round-trip receipt

Recommended:

```text
roundtrip_required_count
roundtrip_pass_count
roundtrip_failure_count
```

Required:

```text
roundtrip_pass_count == roundtrip_required_count
roundtrip_failure_count = 0
```

Only modern precomposed rows require composition round-trip.

---

# 58. Atom ledger receipt

Record counts only by default:

```text
onset_atom_count
vowel_atom_count
coda_atom_count
tense_onset_row_count
compound_vowel_row_count
compound_coda_row_count
```

The detailed atom ledger may be stored in the dedicated JSON receipt.

No float weights are present.

---

# 59. Tensor pack receipt

Required:

```text
row_width_u32 = 16
row_count = structure_row_count
reserved_lane_nonzero = 0
sentinel_value = 4294967295
pack_digest=<sha256>
```

No GPU upload is required in R03.

This pack prepares future structural atlas work.

---

# 60. Static closure checks

Before bake, verify:

```text
R02 parent invocation count = 1
R01 not independently invoked by R03
no tokenizer re-encode in R03
no normalized source rescan for membership
parent Hangul scalar count exact binding
codepoint-based exact structural classifier present
modern precomposed upper bound exactly D7A3
D7A4-D7AF rejection present
exact L/V/T integer decomposition present
exact inverse compose present
round-trip gate present
modern direct Jamo role ranges present
compatibility Jamo no-context-guess gate present
no Jamo sequence auto-compose
exact tense onset atom map present
exact compound vowel atom map present
exact final cluster atom map present
token structure binding ledger present
multi-scalar token parity gate present
multi-token scalar parity gate present
byte-fallback reunification semantics present
PAD structure count zero gate present
u32x16 pack present
reserved lane zero gate present
build_hangul_feature_rows call count = 0
CHEON_LUT live reference count = 0
JI_LUT live reference count = 0
IN_LUT live reference count = 0
derive_cheon_ji_in call count = 0
QWave live call count = 0
G2P live call count = 0
morph live call count = 0
model forward call count = 0
loss/backward/optimizer call count = 0
double-build reproducibility present
parent authority immutability gate present
explicit Cargo bin registration present
```

---

# 61. Physical PASS terminal evidence

Expected shape:

```text
[bt-hangul-structure-03]
parent_r02_physical_pass=1
parent_alignment_authority_bound=1
parent_hangul_scalar_count=8
structure_row_count=8
parent_scalar_digest_mismatch=0
parent_owner_mismatch=0
modern_precomposed_count=<runtime>
modern_choseong_jamo_count=<runtime>
modern_jungseong_jamo_count=<runtime>
modern_jongseong_jamo_count=<runtime>
hangul_jamo_other_count=<runtime>
compatibility_jamo_count=<runtime>
unsupported_count=0
unassigned_precomposed_range_count=0
roundtrip_required_count=<runtime>
roundtrip_pass_count=<same-runtime-count>
roundtrip_failure_count=0
multi_structure_token_count=1
multi_token_structure_count=0
byte_fallback_reunified_structure_count=0
token_structure_binding_mismatch=0
pad_structure_row_count=0
discrete_tensor_row_width=16
discrete_tensor_row_count=8
discrete_tensor_reserved_nonzero=0
structure_reproducibility_runs=2
structure_reproducibility_match=1
parent_alignment_authority_unchanged=1
parent_ingress_authority_unchanged=1
parent_sequence_authority_unchanged=1
heuristic_float_features=0
cheonjiin=0
qwave=0
g2p=0
morphology=0
model_forward=0
loss=0
backward=0
optimizer=0
weight_mutation=0
structure_row_ledger_digest=<sha256>
jamo_atom_ledger_digest=<sha256>
token_structure_binding_digest=<sha256>
discrete_tensor_pack_digest=<sha256>
hangul_structure_authority_digest=<sha256>
proof_ledger=HOLD
```

Only parent-observed counts are predeclared. Structural distribution counts remain runtime evidence.

---

# 62. PASS token

```text
PASS_ASH_BASETRAIN_BT_HANGUL_STRUCTURE_03_BT_TOKEN_SPAN_ALIGNMENT_02_PHYSICAL_PARENT_EXACT_PARENT_HANGUL_SCALAR_DIGEST_BYTE_SCALAR_AND_TOKEN_OWNERSHIP_BINDING_CODEPOINT_RECLASSIFICATION_ZERO_PARENT_KIND_BLIND_TRUST_MODERN_PRECOMPOSED_EXACT_AC00_TO_D7A3_RANGE_D7A4_TO_D7AF_ZERO_FABRICATION_EXACT_INTEGER_LVT_DECOMPOSITION_EXACT_CANONICAL_CONJOINING_JAMO_CODEPOINT_BINDING_EXACT_PRECOMPOSED_COMPOSE_ROUNDTRIP_ZERO_FAILURE_MODERN_CHOSEONG_JUNGSEONG_JONGSEONG_DIRECT_JAMO_ROLE_CLASSIFICATION_NONMODERN_JAMO_EVIDENCE_PRESERVATION_COMPATIBILITY_JAMO_ZERO_CONTEXT_GUESS_ZERO_JAMO_SEQUENCE_AUTO_COMPOSITION_EXACT_TENSE_ONSET_COMPOUND_VOWEL_AND_COMPOUND_FINAL_ATOM_TOPOLOGY_ONE_CANONICAL_STRUCTURE_ROW_PER_PARENT_HANGUL_SCALAR_MULTI_SYLLABLE_TOKEN_TO_MULTIPLE_STRUCTURE_ROWS_PRESERVED_MULTI_TOKEN_BYTE_FALLBACK_SCALAR_SINGLE_STRUCTURE_ROW_REUNIFICATION_TOKEN_TO_STRUCTURE_BINDING_LEDGER_PAD_ZERO_STRUCTURE_OWNERSHIP_DISCRETE_U32X16_STRUCTURE_TENSOR_DERIVED_PACK_RESERVED_ZERO_DOUBLE_BUILD_REPRODUCIBILITY_EXACT_PARENT_AUTHORITIES_UNCHANGED_ZERO_HANGUL_FEATURE_ROW_AUTHORITY_ZERO_HEURISTIC_FLOAT_FEATURE_ZERO_CHEONJIIN_ZERO_QWAVE_ZERO_G2P_ZERO_MORPHOLOGY_ZERO_MODEL_FORWARD_ZERO_LOSS_ZERO_BACKWARD_ZERO_OPTIMIZER_ZERO_WEIGHT_MUTATION_PROOF_LEDGER_HOLD_SEALED
```

---

# 63. Physical PASS meaning

A physical R03 PASS proves:

```text
Every Hangul scalar already admitted by R02 has one exact canonical structure row.
Modern precomposed syllables decompose and recompose exactly.
Direct modern Jamo receive exact role-local identities.
Compatibility Jamo are preserved without guessed slot roles.
Orthographic compound structure is represented as ordered atoms.
Token/scalar many-to-many ownership remains intact.
PAD never becomes language structure.
A deterministic discrete structure tensor candidate can be regenerated exactly.
```

It does not prove:

```text
Cheon-Ji-In correctness
Q-wave correctness
phonological pronunciation correctness
morphological correctness
language-model quality
structural Medusa prediction quality
```

---

# 64. Admission state after PASS

```text
BT-KOREAN-INGRESS-01
  real text -> exact token authority                 ADMITTED

BT-TOKEN-SPAN-ALIGNMENT-02
  token <-> normalized span <-> Hangul ownership    ADMITTED

BT-HANGUL-STRUCTURE-03
  exact scalar -> discrete composition topology     ADMITTED on physical PASS

Canonical Cheon-Ji-In basis                         BLOCKED
Q-wave structure                                    BLOCKED
Structural Medusa targets                           BLOCKED
Structural Medusa heads                             BLOCKED
Live structural decode prior                        BLOCKED
Real-text R6 forward adoption                       BLOCKED
Production inference                                BLOCKED
Proof ledger                                        HOLD
```

---

# 65. Natural next patch

```text
ASH-BASETRAIN-BT-CHEONJIIN-STRUCTURE-04

BT-HANGUL-STRUCTURE-03 Exact Physical Parent /
Canonical Jamo Atom Topology Binding /
Cheon·Ji·In Structural Basis From Jamo Composition /
No CHEON_LUT·JI_LUT·IN_LUT Truth /
Onset·Vowel·Coda Basis Separation /
Compound Atom Ordered Accumulation /
Per-Syllable CJI Vector /
Inter-Syllable Axis Transition /
Token Multi-Syllable CJI Preservation /
Discrete-to-Continuous Projection Receipt /
KRTTS Heuristic CJI Reference Comparison /
Zero Q-wave Yet /
Zero Hidden Fusion /
Zero Logit Mutation Seal
```

R04 should use the exact Jamo/atom ledger from R03 as its only structural source.

The existing KRTTS/ASH heuristic Cheon-Ji-In values may be measured as a reference arm, but may not override the canonical Jamo-derived basis.

---

# 66. Relation to Structural Medusa roadmap

R03 supplies exact training targets for the orthographic factor of Structural Medusa.

Future hierarchy:

```text
R03 Hangul discrete structure truth
        ↓
R04 canonical Cheon-Ji-In structure
        ↓
R05 Q-wave dynamic structure
        ↓
R06A future structural target generation
        ↓
R06B factor × horizon Medusa heads
```

This ordering means Medusa never learns from an ambiguous token-to-syllable collapse or heuristic Cheon-Ji-In root.

---

# 67. Architecture seal

> `BT-HANGUL-STRUCTURE-03` is the first BaseTrain stage that turns the physically proven token-to-Hangul ownership ledger into exact Korean orthographic structure, but it deliberately stops before interpretation. Each parent Hangul scalar becomes exactly one canonical structure row. Modern precomposed syllables use integer L/V/T decomposition and must compose back to their original Unicode scalar. Modern direct Jamo are classified by exact slot ranges; compatibility Jamo are preserved without guessed onset/coda roles; Jamo sequences are never silently recomposed. Tense onsets, compound vowels, and compound final clusters are represented as ordered orthographic atom topology while their canonical syllable indices remain unchanged. The many-to-many token/scalar ownership proven by R02 is preserved exactly, including future byte-fallback multi-token scalar cases, and PAD owns no structure. A deterministic `u32[16]` structure pack is derived for future GPU atlas and Structural Medusa use, but the semantic row ledger remains the authority. Existing `HangulFeatureRow` continuous heuristics, Cheon/Ji/In LUT values, Q-wave, G2P, morphology, model forward, and training mutation remain outside this boundary.
