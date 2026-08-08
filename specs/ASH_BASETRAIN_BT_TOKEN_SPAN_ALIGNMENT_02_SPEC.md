# ASH-BASETRAIN-BT-TOKEN-SPAN-ALIGNMENT-02

## Korean Ingress Exact Parent / Tokenizer Encode-Trace Single Authority / Normalized Text Byte·Scalar Span Ledger / Vocab Piece Exact Binding / Control·Byte-Fallback·Whitespace Gap Semantics / Multi-Syllable Token Preservation / Hangul Scalar Ownership / Padding Isolation / No One-Token-One-Syllable Assumption / No Hangul Tensor Aggregation Yet / No Cheon-Ji-In Yet / No Q-wave Yet Seal

> Parent SSOT: `ASH-BASETRAIN-BT-KOREAN-INGRESS-01` physical PASS
> Parent observed fixture: source bytes=28, valid tokens=8, B=1, Q=32, PAD suffix=24
> Token selection SSOT: `tokenizer_core::NativeTokenizer`
> Span selection SSOT: the same canonical encode loop that emits token IDs
> Normalized text SSOT: parent `TokenizerEncodeWithAuthorityResult.normalized_text`
> Numerical sequence SSOT: parent `BaseTrainRuntimeInputSequenceAuthority`
> Output SSOT: `BaseTrainTokenSpanAlignmentAuthority`
> Hangul structure tensor / canonical Cheon-Ji-In / Q-wave: BLOCKED
> Model forward / loss / backward / optimizer / weight mutation: BLOCKED
> Proof ledger: HOLD

---

# 1. Goal

Create one deterministic topology ledger binding every valid parent token position to the exact normalized UTF-8 range that caused its emission, while preserving non-1:1 relationships.

```text
BT-KOREAN-INGRESS-01 physical parent
        ↓
exact normalized text
+ exact valid token IDs
+ frozen tokenizer manifest
        ↓
tokenizer_core canonical encode trace
        ↓
token position
↔ token id
↔ exact vocab piece
↔ normalized byte span
↔ normalized scalar span
↔ Hangul scalar ownership
        ↓
BaseTrainTokenSpanAlignmentAuthority
```

Required topology support:

```text
one token -> many Hangul scalars
many byte tokens -> one Unicode scalar
synthetic control -> zero-width normalized anchor
whitespace delimiter -> explicit normalized gap
PAD suffix -> no text ownership
```

No token ID may be changed by R02.

---

# 2. Parent physical authority

Invoke exactly one:

```rust
run_base_train_korean_ingress_01_session()
```

Require:

```text
parent final pass=true
parent PASS token exact
parent reproducibility pass=true
fixture token authority used=0
model forward=0
loss=0
backward=0
optimizer=0
weight mutation=0
```

Current parent evidence:

```text
source_byte_count=28
model_vocab_size=48259
tokenizer_vocab_size=48259
valid_token_count=8
batch_size=1
seq_len=32
pad_suffix_count=24
```

Only B=1 and Q=32 are fixed geometry here. Other counts remain runtime evidence.

---

# 3. Normalized text authority

Alignment domain is exactly the parent's tokenizer-owned normalized text, not raw source text.

Require:

```text
SHA256(normalized UTF-8 bytes) == parent encode normalized_text_sha256
normalized byte count == parent encode authority
normalized scalar count == parent encode authority
```

No raw-to-normalized positional identity is assumed. Normalization may alter whitespace, punctuation forms, case, or Unicode representation according to the frozen tokenizer manifest.

---

# 4. Decode reverse-alignment is forbidden

Forbidden:

```text
token IDs -> decode -> search normalized source -> invent spans
normalized_text.find(vocab_piece)
normalized_text.rfind(vocab_piece)
regex/Levenshtein alignment
strip ▁ then search
replace <br> after the fact to invent source range
```

The decoder is allowed only for piece classification and output provenance. It cannot own span selection.

---

# 5. Tokenizer encode-trace SSOT

Refactor `tokenizer_core` so all public encode paths project from one canonical traced route:

```rust
fn encode_canonical_with_trace(&self, text: &str)
    -> Result<TokenizerCanonicalEncodeTrace>
```

Trace carries at least:

```rust
pub struct TokenizerCanonicalEncodeTrace {
    pub normalized_text: String,
    pub token_ids: Vec<u32>,
    pub token_emissions: Vec<TokenizerTokenEmission>,
    pub normalized_gaps: Vec<TokenizerNormalizedGap>,
    pub synthetic_anchors: Vec<TokenizerSyntheticAnchor>,
    pub byte_fallback_groups: Vec<TokenizerByteFallbackGroup>,
    pub trace_digest: String,
}
```

`TokenizerEngine::encode()` and `NativeTokenizer::encode_with_authority()` must consume this same route. No parallel normalization, pretokenization, longest-match, byte-fallback, or UNK implementation is admitted for alignment.

---

# 6. Span-bearing pretokenization

Canonical pretoken units:

```rust
pub enum PretokenUnitKind {
    Material,
    NewlineBridge,
    SyntheticPrefixControl,
    SyntheticSuffixControl,
}
```

Each unit owns normalized half-open byte/scalar coordinates. The previous string-only pretokenizer, if retained, is a projection of this span-bearing result.

Whitespace not represented by a token is recorded in a `TokenizerNormalizedGap` ledger rather than disappearing.

---

# 7. Token emission authority

Every emitted valid token binds:

```text
token position
token id
exact manifest vocab piece
emission kind
pretoken ordinal
normalized byte [start,end)
normalized scalar [start,end)
material coverage flag
zero-width anchor flag
byte-fallback group/component metadata
surface SHA-256
emission digest
```

Token positions must be exactly `0..N-1`, where N is the parent valid-token count.

Exact parent parity:

```text
trace token IDs == parent TokenizerEncodeAuthority token IDs
trace token IDs == parent RuntimeInputSequence valid prefix
```

---

# 8. Emission taxonomy

Minimum stable kinds:

```text
exact_core_special
exact_pretoken_match
hot_token_match
longest_piece_match
byte_fallback_component
unknown_scalar_fallback
newline_bridge
synthetic_control_prefix
synthetic_control_suffix
```

No generic `Other` may hide these distinctions.

---

# 9. Exact manifest binding

For every emission:

```text
manifest vocab id resolution cardinality = 1
manifest piece == trace vocab piece
0 <= token id < V
```

No nearest token, alternate vocab, reserved-token remap, readability rewrite, or historical tokenizer fallback.

---

# 10. Material spans

For material pretoken units, longest-piece selection advances a local scalar cursor over the exact pretoken unit. Selected candidate length maps directly to normalized scalar boundaries and then to normalized UTF-8 byte boundaries.

Repeated substrings therefore require no search and introduce no ambiguity.

SentencePiece-style `▁` remains decode semantics only unless the literal `▁` scalar was actually present and selected from normalized input.

---

# 11. Newline and synthetic control semantics

Normalized newline mapped to `<br>` is a material bridge:

```text
emission kind=newline_bridge
source span=the exact normalized newline scalar
material coverage=true
```

Synthetic time wrappers such as `<time>` and `</time>` are zero-width controls anchored to the literal timecode start/end:

```text
material coverage=false
zero_width_anchor=true
byte_start==byte_end
scalar_start==scalar_end
```

They consume no normalized bytes.

---

# 12. Whitespace gap authority

Normalized whitespace discarded by pretokenization must be represented exactly once in `TokenizerNormalizedGap` with byte/scalar ranges and surface digest.

Material token coverage plus normalized gap coverage must partition the normalized byte domain exactly:

```text
material bytes + gap bytes = normalized_text_byte_count
coverage_gap_bytes=0
coverage_overlap_bytes=0
```

---

# 13. Byte fallback groups

One Unicode scalar may emit multiple byte tokens. Represent this as a group:

```text
group scalar index
source byte range
token positions[]
byte values[]
reconstructed UTF-8 validity
reconstructed scalar
```

Each component token owns its exact source-byte subrange but references the same scalar range. Concatenated component bytes must equal the original scalar UTF-8 bytes exactly. No replacement-character repair.

If no byte token can be emitted, an UNK emission retains the exact original scalar span and source-surface digest.

---

# 14. Scalar coverage and Hangul ownership

Every normalized scalar must be either materially tokenized or contained in one normalized gap. Synthetic controls own no scalar.

R02 identifies Hangul scalars only. It does not generate numeric Hangul features.

Canonical scalar kinds:

```text
precomposed_hangul_syllable
hangul_jamo
hangul_compatibility_jamo
```

Each `BaseTrainHangulScalarRef` binds:

```text
normalized scalar index
normalized byte range
scalar/codepoint
scalar kind
owner token positions[]
ownership mode
scalar digest
```

The owner relation is bipartite:

```text
one token may own 0..N Hangul scalars
one Hangul scalar may be owned by multiple byte-fallback token positions
```

No one-token-one-syllable or one-syllable-one-token assumption.

---

# 15. Canonical output authority

`BaseTrainTokenSpanAlignmentAuthority` binds:

```text
parent ingress authority digest
parent sequence authority digest
parent tokenizer encode authority digest
tokenizer identity digest
normalized text digest
B/Q/N/PAD counts
token entries
normalized gap ledger
byte fallback group ledger
Hangul scalar ownership ledger
material/gap byte counts
coverage gap/overlap counts
multi-scalar token count
multi-token scalar count
synthetic token count
byte fallback token count
unknown token count
encode trace digest
ledger digests
authority digest
```

Exactly one authority is published per R02 operation.

---

# 16. Padding isolation

Parent Q32 right-padding remains numerical-only state:

```text
pad_start=N
pad_end=Q
all parent IDs [N,Q) == manifest PAD id
PAD token-span entry count=0
PAD Hangul ownership count=0
```

R02 never gives PAD source text ownership.

---

# 17. Reproducibility

Execute canonical encode trace twice against the exact same parent source and frozen tokenizer manifest.

Require exact equality of:

```text
token IDs
token emission ledger
normalized gap ledger
byte-fallback group ledger
trace digest
alignment authority digest
```

Any mismatch fails closed with `BTTokenSpanAlignmentReproducibilityMismatch`.

---

# 18. Parent immutability

Before/after require exact equality of:

```text
parent ingress authority digest
parent sequence authority digest
parent tokenizer encode authority digest
parent normalized text digest
parent token IDs
```

R02 is derived metadata only and cannot mutate its parent.

---

# 19. Structural boundary

Explicitly blocked in R02:

```text
build_hangul_feature_rows
HangulFeatureRow publication
choseong/jungseong/jongseong feature authority
cheon_core / ji_support / in_bridge
axis_bits structural derivation
QW01-QW06
structural projection
hidden-state fusion
model forward
loss
backward
optimizer
weight mutation
```

Existing Hangul/Q-wave modules remain reference-only until later stages.

---

# 20. Runtime receipts

Default directory:

```text
workspace/runtime/basetrain/token_span_alignment/02
```

Receipts:

```text
parent_binding_receipt.json
encode_trace_receipt.json
token_span_ledger.json
normalized_gap_ledger.json
byte_fallback_group_ledger.json
hangul_scalar_ownership_ledger.json
coverage_receipt.json
reproducibility_receipt.json
final_receipt.json
```

The full normalized source string is not emitted by default.

---

# 21. Dedicated binary and CLI

Binary:

```text
ash_basetrain_token_span_alignment_02_gate
```

It is explicitly registered in `crates/orchestrator_local/Cargo.toml` with `orchestrator_tcu_audit_bins`.

Dedicated response file:

```text
specs/cli/ash_basetrain_token_span_alignment_02.args
```

The gate receives both the existing ingress response file and the R02 response file. Their keys must be disjoint.

Required true policies include parent physical binding, traced encode single authority, exact token parity, exact manifest-piece binding, byte/scalar span ledgers, whitespace gaps, synthetic anchors, byte-fallback groups, full coverage, Hangul scalar ownership, padding isolation, reproducibility, parent immutability, and zero model/structure execution.

Required false policies include decode reverse alignment, string search alignment, span guessing, token mutation, retokenization, PAD source ownership, 1:1 syllable assumptions, Hangul feature-row publication, Cheon-Ji-In, Q-wave, and model forward.

---

# 22. Expected current physical evidence

```text
[bt-token-span-alignment-02]
parent_ingress_physical_pass=1
parent_source_byte_count=28
parent_valid_token_count=8
parent_seq_len=32
parent_pad_suffix_count=24
normalized_text_digest_bound=1
normalization_owner=tokenizer_core
encode_trace_owner=tokenizer_core
encode_trace_runs=2
trace_token_count=8
trace_token_id_mismatch=0
manifest_piece_resolution_mismatch=0
material_token_count=<runtime>
synthetic_token_count=<runtime>
byte_fallback_token_count=<runtime>
unknown_token_count=<runtime>
normalized_gap_count=<runtime>
material_covered_byte_count=<runtime>
gap_byte_count=<runtime>
coverage_gap_bytes=0
coverage_overlap_bytes=0
hangul_scalar_count=<runtime>
multi_scalar_token_count=<runtime>
multi_token_scalar_count=<runtime>
pad_source_ownership_count=0
alignment_authority_publication=1
reproducibility_match=1
parent_ingress_authority_unchanged=1
parent_sequence_authority_unchanged=1
model_forward=0
hangul_tensor=0
cheonjiin=0
qwave=0
loss=0
backward=0
optimizer=0
weight_mutation=0
encode_trace_digest=<sha256>
token_entry_ledger_digest=<sha256>
gap_ledger_digest=<sha256>
hangul_ownership_digest=<sha256>
alignment_authority_digest=<sha256>
proof_ledger=HOLD
```

---

# 23. PASS token

```text
PASS_ASH_BASETRAIN_BT_TOKEN_SPAN_ALIGNMENT_02_BT_KOREAN_INGRESS_01_PHYSICAL_PARENT_EXACT_SOURCE_TOKENIZER_ENCODE_SEQUENCE_AND_NORMALIZED_TEXT_BINDING_TOKENIZER_CORE_SINGLE_ENCODE_TRACE_AUTHORITY_SAME_NORMALIZATION_PRETOKENIZATION_LONGEST_MATCH_BYTE_FALLBACK_AND_UNK_PATH_AS_CANONICAL_TOKEN_EMISSION_ZERO_DECODE_REVERSE_ALIGNMENT_ZERO_STRING_SEARCH_ALIGNMENT_VALID_TOKEN_POSITIONS_ZERO_TO_N_MINUS_ONE_EXACT_PARENT_TOKEN_ID_PARITY_EXACT_FROZEN_MANIFEST_VOCAB_PIECE_BINDING_NORMALIZED_HALF_OPEN_BYTE_AND_SCALAR_SPAN_LEDGER_NEWLINE_BRIDGE_LITERAL_NEWLINE_OWNERSHIP_SYNTHETIC_CONTROL_ZERO_WIDTH_ANCHOR_WHITESPACE_DELIMITER_EXPLICIT_GAP_LEDGER_BYTE_FALLBACK_COMPONENT_AND_GROUP_UTF8_RECONSTRUCTION_EXACT_UNKNOWN_SCALAR_ORIGINAL_SPAN_RETENTION_FULL_NORMALIZED_BYTE_COVERAGE_ZERO_GAP_ZERO_OVERLAP_MONOTONIC_MATERIAL_EMISSION_PADDING_SUFFIX_ZERO_TEXT_OWNERSHIP_HANGUL_SCALAR_IDENTITY_AND_BIPARTITE_TOKEN_OWNERSHIP_MULTI_SYLLABLE_TOKEN_PRESERVED_MULTI_TOKEN_SINGLE_SCALAR_PRESERVED_ZERO_ONE_TOKEN_ONE_SYLLABLE_ASSUMPTION_ZERO_HANGUL_FEATURE_AGGREGATION_ZERO_CHEONJIIN_ZERO_QWAVE_DOUBLE_TRACE_REPRODUCIBILITY_EXACT_PARENT_AUTHORITIES_UNCHANGED_ZERO_MODEL_FORWARD_ZERO_LOSS_ZERO_BACKWARD_ZERO_OPTIMIZER_ZERO_WEIGHT_MUTATION_PROOF_LEDGER_HOLD_SEALED
```

---

# 24. Implementation surface

Pass63 changes only:

```text
crates/tokenizer_core/src/lib.rs
crates/model_core/src/lib.rs
crates/model_core/src/base_train_token_span_alignment_authority.rs
crates/orchestrator_local/Cargo.toml
crates/orchestrator_local/src/base_train_token_span_alignment_02.rs
crates/orchestrator_local/src/bin/ash_basetrain_token_span_alignment_02_gate.rs
specs/cli/ash_basetrain_token_span_alignment_02.args
```

Static closure before physical execution: `66/66 PASS`.

No JS/TS/Python path is added to BaseTrain core.

---

# 25. Package hygiene

Baked ZIP excludes:

```text
*.md
*.sha256
artifacts/
manifests/
runtime receipts
source text copy
tokenizer manifest copy
checkpoint copies
KSS corpus
```

---

# 26. Admission state after physical PASS

```text
BT-KOREAN-INGRESS-01 actual Korean text -> exact token candidate = ADMITTED
BT-TOKEN-SPAN-ALIGNMENT-02 token -> normalized span -> Hangul scalar ownership = ADMITTED on physical PASS
Live real-text R6 forward = BLOCKED
Hangul structure tensor = BLOCKED
Canonical Cheon-Ji-In basis = BLOCKED
QW01-QW06 = BLOCKED
Structural conditioning = BLOCKED
INFERENCE-CANARY-02 = BLOCKED
Production inference = BLOCKED
Proof ledger = HOLD
```

---

# 27. Natural next boundary

```text
ASH-BASETRAIN-BT-HANGUL-STRUCTURE-03

BT-TOKEN-SPAN-ALIGNMENT-02 Exact Parent /
Hangul Scalar Ownership Exact Binding /
Precomposed Syllable and Jamo Classification /
Canonical Choseong·Jungseong·Jongseong Decomposition /
Non-Hangul Isolation /
Per-Syllable Structural Row Authority /
Token-to-Multi-Syllable Structure Preservation /
Multi-Token Byte-Fallback Scalar Reunification /
No Cheon-Ji-In Derived Basis Yet /
No Q-wave Yet /
No Token Projection Yet /
No Hidden Fusion Seal
```

Existing `hangul_tensor` code may be reused only after decomposition/feature semantics are audited against the new ownership authority. Existing heuristic `cheon_core/ji_support/in_bridge` must not be silently promoted to canonical Cheon-Ji-In truth.

---

# 28. Architecture seal

R02 turns the physically admitted Korean token sequence into a reproducible topology ledger without changing any token. The tokenizer's real encode path owns alignment. Material token spans plus explicit delimiter gaps partition normalized UTF-8 bytes exactly once; synthetic controls are zero-width; byte-fallback groups preserve many-token-to-one-scalar ownership; multi-syllable tokens retain ordered Hangul scalar references; PAD positions own no text. The alignment authority binds parent ingress/sequence/tokenizer identities and is reproduced twice. No Hangul numeric feature tensor, Cheon-Ji-In basis, Q-wave, model forward, or training mutation is admitted at this boundary.