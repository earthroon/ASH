# ASH-BASETRAIN-BT-STRUCTURAL-MEDUSA-TARGETS-06A

## R05-R2 Exact Physical Parent / Factor-Separated Future Structural Target Authority / Full BQH Slot Geometry / Token Structural Packet Atlas / Ragged Multi-Syllable Preservation / Hangul Orthographic Target Binding / CJI Static Target Binding / QW01·QW02 Local Dynamic Target Binding / Causally-Closed QW03 Incoming·Internal Edge Binding / QW04·QW05·QW06 Context-Candidate Support Mask / Horizon +1·+2·+3·+4 Ledger / No Synthetic EOS / Source-PAD and Out-of-Valid-Prefix Mask / Shared Multi-Token Scalar Ownership Preservation / No Future-Support Leakage Beyond Target Position / Target Token ID Provenance-Only / Zero Medusa Head / Zero Hidden Fusion / Zero Model Forward / Zero Loss / Zero Backward / Zero Optimizer / Zero Logit Mutation Seal

> Revision: `BT-STRUCTURAL-MEDUSA-TARGETS-06A`
>
> Parent semantic SSOT: `ASH-BASETRAIN-BT-QWAVE-STRUCTURE-05-R2` physical PASS
>
> Parent semantic Q-wave authority digest observed on current fixture: `8294f0d9b0e996918ee0a6ad25ded93099c59f6f68d075575940057569318f48`
>
> Parent atlas execution digest observed on current fixture: `0baddedaaad7768464792ddf7f957e63c2d7ea4b00644f2c156e6eef828b0b84`
>
> Current geometry: `B=1`, `Q=32`, valid token prefix=`8`, PAD suffix=`24`, `H={+1,+2,+3,+4}`
>
> Current expected slots: total=`128`, active=`22`, masked=`106`, source-PAD=`96`, out-of-valid-prefix=`10`, synthetic EOS=`0`
>
> Proof ledger: `HOLD`

---

# 1. Goal

R06A creates exact future structural labels only. It does not create or train a Medusa head.

```text
R02 token positions and ownership
  -> R03 exact Hangul rows
  -> R04 static CJI rows
  -> R05 dynamic Q-wave rows/edges/context candidates
  -> one absolute structural target packet per valid token position
  -> full [B,Q,H=4] horizon slot ledger
  -> slot references target packet at q+h
```

The canonical target is a ragged packet, not a single token vector. R02 already physically proved `multi_scalar_token_count=1`, so one tokenizer token may own multiple Hangul scalars.

---

# 2. Parent admission

R06A accepts exactly one physically passing R05-R2 parent session. Required parent invariants include:

```text
R05 static CJI recompute = 0
R05 parent CJI/primitive mutation = 0
QW01 parent binding mismatch = 0
QW01 legacy root = 0
QW02 nonfinite = 0
QW03 edge owner = r04_transition_ledger
QW03 edge membership mismatch = 0
QW03 text adjacency rediscovery = 0
QW04 owner = qw03_connected_components
QW04 substring search = 0
QW05 autofill/cross-chain/span mismatch = 0
QW06 nonadjacent edge/boundary mismatch = 0
legacy Q-wave authority/override/blend = 0
R05 reproducibility = 1
hidden fusion = 0
logit/sampler/token-selection mutation = 0
medusa head = 0
model forward/loss/backward/optimizer/weight mutation = 0
```

R06A calls R05 exactly once and must not independently rebuild R01/R02/R03/R04.

---

# 3. Semantic authority vs execution provenance

R06A semantic targets bind `parent_qwave_structure_authority_digest`.

R05 atlas page size, worker count, scheduling, and `parent_qwave_compute_atlas_digest` are execution provenance only. Changing execution scheduling while preserving R05 semantic output must not change R06A semantic target meaning.

---

# 4. Geometry

Canonical target geometry:

```text
[B,Q,H]
H index 0 = +1
H index 1 = +2
H index 2 = +3
H index 3 = +4

slot_index = ((batch * Q + source_q) * H) + horizon_index
target_position = source_q + horizon_distance
```

Current fixture:

```text
valid_token_count = 8
seq_len = 32
h1 active = 7
h2 active = 6
h3 active = 5
h4 active = 4
active_slot_count = 22
slot_count = 128
source_pad_slot_count = 96
target_outside_valid_prefix_slot_count = 10
masked_slot_count = 106
```

No token skipping and no nearest-structural-token fallback.

---

# 5. No synthetic EOS

Current parent has `implicit_bos=0`, `implicit_eos=0`. If `q+h >= valid_token_count`, the slot is masked as `TargetOutsideValidPrefix`; no EOS structure is fabricated.

---

# 6. Token structural packet

One packet is created for every valid absolute token position.

```rust
pub struct StructuralMedusaTokenTargetPacketV1 {
    pub packet_index: u32,
    pub batch_index: u32,
    pub token_position: u32,
    pub parent_token_id: u32,
    pub parent_token_entry_digest: String,
    pub hangul_ref_offset: u32,
    pub hangul_ref_count: u32,
    pub cji_ref_offset: u32,
    pub cji_ref_count: u32,
    pub qw01_ref_offset: u32,
    pub qw01_ref_count: u32,
    pub qw02_ref_offset: u32,
    pub qw02_ref_count: u32,
    pub qw03_ref_offset: u32,
    pub qw03_ref_count: u32,
    pub context_ref_offset: u32,
    pub context_ref_count: u32,
    pub factor_available_bits: u32,
    pub shared_ownership_bits: u32,
    pub support_min_token_position: u32,
    pub support_max_token_position: u32,
    pub causal_closed: bool,
    pub packet_digest: String,
}
```

`parent_token_id` is provenance-only. Token IDs, vocab pieces, and decoded future text are forbidden as learned structural input features.

---

# 7. Ragged multi-syllable preservation

The packet stores ordered references to all Hangul rows owned by the token. Forbidden authority transformations:

```text
first syllable only
last syllable only
mean pooling
max pooling
fixed one-row truncation
silent fixed-width zero padding presented as semantics
```

Fixed-width packet encoding belongs to R06B or later.

---

# 8. Hangul target

For token position `p`:

```text
hangul refs = ordered R03 structure rows whose owner_token_positions contain p
```

Derived materialization copies exact R03 `u32[16]` rows. No new Hangul decomposition occurs in R06A.

---

# 9. CJI target

Every admitted Hangul row binds one exact R04 CJI row. Derived materialization copies exact R04 `f32[18]` with field order `ash_cji_syllable_vector18_v1`.

Required:

```text
cji_ref_count == hangul_ref_count
CJI recompute = 0
legacy CJI recompute = 0
```

---

# 10. QW local target

Every supported syllable binds exact R05 QW01/QW02 rows.

Derived QW-local pack:

```text
ash_qwave_local12_target_v1
0 direction_cheon
1 direction_ji
2 direction_in
3 direction_norm
4 amplitude
5 phase
6 pressure
7 closure
8 resonance
9 onset_push
10 vowel_flow
11 coda_drag
```

No transform beyond exact field selection is allowed.

---

# 11. QW03 causal edge target

For target token position `p`, an R05 QW03 edge may enter the packet only when:

```text
the edge's to-row is owned by p
and
max(all owner token positions of both endpoint rows) <= p
```

This admits incoming and internal target edges and rejects outgoing edges requiring later token evidence.

```text
incoming earlier -> target       allowed
internal target -> target        allowed
target -> target+1               forbidden
```

Derived QW-edge pack:

```text
ash_qwave_edge10_target_v1
0 pulse_delta
1 phase_delta
2 direction_alignment
3 amplitude_transfer
4 pressure_delta
5 closure_release
6 coda_to_onset_bridge
7 resonance_carry
8 flow_continuity
9 transition_energy
```

---

# 12. Left-closed target support

General target rule:

```text
factor_support_max_token_position <= target_token_position
```

Reading `q+h` to construct the `q+h` label is valid label construction. Leakage means using evidence beyond `q+h`, or writing future label data into source-side model state.

---

# 13. QW04/QW05/QW06 context candidates

QW04/QW05/QW06 remain context candidates. They may enter a packet only if their complete parent support is at or before the target token.

```text
support_max <= target -> available
support_max > target  -> factor masked
```

No partial QW04 aggregate is synthesized. QW05 absent morphology stays explicitly absent. Whole-sentence/future-complete QW06 context cannot become an oracle label for an earlier target.

Current R05 fixture has `qw05_chain_lattice_count=0`, so current R06A must produce zero synthetic morph targets.

---

# 14. Factor bits

```text
bit0 Hangul orthographic
bit1 CJI static
bit2 QW01/QW02 local
bit3 QW03 causal edge
bit4 QW04 closed-chain context
bit5 QW05 morph candidate
bit6 QW06 sentence candidate
bit7 shared-ownership present
```

Bits 0..6 describe factor availability. Shared ownership is separately preserved and not silently resolved into a training policy.

---

# 15. Horizon slot

```rust
pub struct StructuralMedusaHorizonTargetSlotV1 {
    pub slot_index: u32,
    pub batch_index: u32,
    pub source_query_position: u32,
    pub horizon_index: u8,
    pub horizon_distance: u8,
    pub target_token_position: Option<u32>,
    pub target_packet_index: Option<u32>,
    pub slot_active: bool,
    pub slot_mask_reason: StructuralMedusaSlotMaskReason,
    pub factor_available_bits: u32,
    pub factor_mask_bits: u32,
    pub target_support_max_position: Option<u32>,
    pub target_causal_closed: bool,
    pub slot_digest: String,
}
```

Mask reasons:

```text
Active
SourcePad
TargetOutsideValidPrefix
```

A valid token with no Hangul rows remains an active slot with structural factors masked. Sequence geometry is never changed by structural availability.

---

# 16. Packet reuse

Packets are absolute-token SSOTs. Multiple horizon slots may reference the same packet. Current fixture packets 1..7 are future targets; packet 0 exists for complete token coverage but has no earlier source slot.

Expected current counts:

```text
token_packet_count = 8
referenced_target_packet_count = 7
```

---

# 17. Ragged and materialized atlases

Semantic ragged atlases:

```text
hangul_ref_atlas
cji_ref_atlas
qw01_ref_atlas
qw02_ref_atlas
qw03_ref_atlas
context_ref_atlas
```

Derived materialization:

```text
hangul_u32x16_atlas
cji_f32x18_atlas
qwave_local_f32x12_atlas
qwave_edge_f32x10_atlas
```

Materialized rows must be exact parity copies/selections from R03/R04/R05. Semantic refs remain authority.

---

# 18. Target token provenance and leakage boundaries

Required zero counters:

```text
target_token_id_training_feature_count = 0
target_piece_training_feature_count = 0
decoded_future_text_training_feature_count = 0
future_target_to_input_sequence_write = 0
future_target_to_embedding_write = 0
future_target_to_hidden_write = 0
future_target_to_kv_write = 0
future_target_to_logit_write = 0
```

R06A does not invoke model forward or decode.

---

# 19. Authority schema

Top-level authority includes parent semantic digests, geometry, packets, horizon slots, factor masks, ragged refs, materialized packs, and deterministic digests:

```text
packet_ledger_digest
slot_ledger_digest
factor_mask_ledger_digest
ragged_ref_atlas_digest
materialized_target_atlas_digest
causal_support_receipt_digest
authority_digest
```

R05 execution atlas digest is retained as provenance and excluded from semantic target digesting.

---

# 20. Determinism and parent immutability

Build the entire R06A authority twice from the same immutable R05 parent.

Required exact match:

```text
packet ledger
slot ledger
factor masks
ragged refs
materialized targets
causal support
final authority digest
```

Capture and verify unchanged:

```text
R05 authority + QW01..QW06 digests
R04 authority
R03 authority
R02 authority
R01 authority
runtime sequence authority
```

No worker completion order enters semantic target digests.

---

# 21. Execution shape

R06A may use atlas-parallel execution but scheduling metadata is non-semantic. Recommended logical waves:

```text
Wave0 token packet/ref gathering
Wave1 Hangul/CJI/QW-local materialization
Wave2 causal QW03 targets
Wave3 causally-closed context refs
Wave4 [B,Q,H] slots
Wave5 deterministic authority reduction
```

---

# 22. CLI

Add `specs/cli/ash_basetrain_structural_medusa_targets_06a.args` and run with the full parent response-file chain.

Required policy includes exact R05 parent, BQH geometry, four horizons, ragged multi-syllable preservation, shared-owner preservation, exact R03/R04/R05 binding, QW03 target-owner causal rule, context support masking, PAD/out-of-prefix masks, zero synthetic EOS, provenance-only token ID, exact materialization parity, reproducibility, parent immutability, and zero head/model/training/decode mutation.

Forbidden policy includes one-token-one-syllable collapse, first-syllable-only, mean-as-authority, silent shared-owner anchoring, CJI/Q-wave recompute, outgoing future QW03 edge, support beyond target, synthetic EOS, nearest structural token fallback, target-token/text features, future-label input writes, Medusa head, hidden fusion, model forward, loss/backward/optimizer/weight mutation, logit/sampler mutation.

---

# 23. Runtime receipts

Default directory:

```text
workspace/runtime/basetrain/structural_medusa_targets/06a
```

Required:

```text
parent_binding_receipt.json
token_target_packet_ledger.json
hangul_target_ref_ledger.json
cji_target_ref_ledger.json
qwave_local_target_ref_ledger.json
qwave_edge_target_ref_ledger.json
context_candidate_target_ref_ledger.json
causal_support_receipt.json
horizon_slot_ledger.json
factor_mask_ledger.json
materialized_target_atlas_receipt.json
reproducibility_receipt.json
final_receipt.json
```

---

# 24. Expected physical evidence

```text
parent_r05_physical_pass=1
parent_qwave_authority_bound=1
parent_qwave_execution_atlas_bound=1
batch_size=1
seq_len=32
valid_token_count=8
horizon_count=4
token_packet_count=8
referenced_target_packet_count=7
slot_count=128
active_slot_count=22
masked_slot_count=106
source_pad_slot_count=96
target_outside_valid_prefix_slot_count=10
synthetic_eos_slot_count=0
h1_active_count=7
h2_active_count=6
h3_active_count=5
h4_active_count=4
shared_owner_target_packet_count=0
hangul_parent_ref_mismatch_count=0
cji_parent_ref_mismatch_count=0
qwave_local_parent_ref_mismatch_count=0
qwave_edge_parent_ref_mismatch_count=0
hangul_materialization_mismatch_count=0
cji_materialization_mismatch_count=0
qwave_local_materialization_mismatch_count=0
qwave_edge_materialization_mismatch_count=0
packet_causal_violation_count=0
qw03_future_support_violation_count=0
factor_support_beyond_target_count=0
morph_candidate_available_count=0
morph_candidate_synthetic_count=0
target_token_id_provenance_bound=1
target_token_id_training_feature_count=0
target_piece_training_feature_count=0
decoded_future_text_training_feature_count=0
future_target_to_input_sequence_write=0
future_target_to_embedding_write=0
future_target_to_hidden_write=0
future_target_to_kv_write=0
future_target_to_logit_write=0
nonfinite_cji_target_count=0
nonfinite_qwave_local_target_count=0
nonfinite_qwave_edge_target_count=0
reproducibility_runs=2
reproducibility_match=1
parent_r05_authority_unchanged=1
parent_r04_authority_unchanged=1
parent_r03_authority_unchanged=1
parent_r02_authority_unchanged=1
parent_r01_authority_unchanged=1
medusa_head_count=0
hidden_fusion=0
model_forward=0
loss=0
backward=0
optimizer=0
weight_mutation=0
logit_mutation=0
sampler_mutation=0
token_selection_mutation=0
proof_ledger=HOLD
```

---

# 25. PASS token

```text
PASS_ASH_BASETRAIN_BT_STRUCTURAL_MEDUSA_TARGETS_06A_BT_QWAVE_STRUCTURE_05_R2_PHYSICAL_PARENT_EXACT_R05_QWAVE_SEMANTIC_AUTHORITY_BINDING_R05_ATLAS_EXECUTION_PROVENANCE_SEPARATED_FULL_B1_Q32_H4_TARGET_SLOT_GEOMETRY_EXACT_Q_PLUS_H_TARGET_POSITION_MAPPING_ONE_ABSOLUTE_TARGET_PACKET_PER_VALID_TOKEN_POSITION_TOKEN_PACKET_COUNT_8_CURRENT_FIXTURE_HORIZON_ACTIVE_COUNTS_7_6_5_4_ACTIVE_SLOT_COUNT_22_FULL_SLOT_COUNT_128_SOURCE_PAD_SLOT_COUNT_96_OUT_OF_VALID_PREFIX_SLOT_COUNT_10_ZERO_SYNTHETIC_EOS_RAGGED_MULTI_SYLLABLE_TOKEN_TARGET_PRESERVATION_ZERO_ONE_TOKEN_ONE_SYLLABLE_COLLAPSE_SHARED_MULTI_TOKEN_SCALAR_OWNERSHIP_PRESERVED_ZERO_SILENT_OWNER_ANCHOR_R03_HANGUL_U32X16_EXACT_TARGET_BINDING_R04_CJI_F32X18_EXACT_TARGET_BINDING_R05_QW01_QW02_LOCAL_DYNAMIC_EXACT_TARGET_BINDING_R05_QW03_TO_TARGET_OWNER_CAUSAL_INCOMING_AND_INTERNAL_EDGE_BINDING_ZERO_OUTGOING_FUTURE_EDGE_TARGET_SUPPORT_MAX_LE_TARGET_POSITION_ALL_FACTORS_LEFT_CLOSED_QW04_QW05_QW06_CONTEXT_CANDIDATE_SUPPORT_MASK_ZERO_FUTURE_COMPLETE_CONTEXT_ORACLE_CURRENT_MORPH_EVIDENCE_ABSENT_EXPLICITLY_MASKED_ZERO_SYNTHETIC_MORPH_TARGET_TOKEN_ID_PROVENANCE_ONLY_ZERO_TARGET_TOKEN_ID_TRAINING_FEATURE_ZERO_DECODED_FUTURE_TEXT_FEATURE_ZERO_FUTURE_TARGET_WRITE_TO_INPUT_EMBEDDING_HIDDEN_KV_OR_LOGITS_DERIVED_HANGUL16_CJI18_QWLOCAL12_QWEDGE10_MATERIALIZATION_EXACT_PARITY_DOUBLE_BUILD_REPRODUCIBILITY_EXACT_PARENT_AUTHORITIES_UNCHANGED_ZERO_MEDUSA_HEAD_ZERO_HIDDEN_FUSION_ZERO_MODEL_FORWARD_ZERO_LOSS_ZERO_BACKWARD_ZERO_OPTIMIZER_ZERO_WEIGHT_MUTATION_ZERO_LOGIT_MUTATION_ZERO_SAMPLER_MUTATION_ZERO_TOKEN_SELECTION_MUTATION_PROOF_LEDGER_HOLD_SEALED
```

---

# 26. Next boundary

```text
ASH-BASETRAIN-BT-STRUCTURAL-MEDUSA-HEADS-06B

R06A Exact Physical Target Parent /
Decoder Hidden Read-Only Binding /
Factor-Separated Head Family /
Hangul Packet Encoder Candidate /
CJI18 Future Regression Head /
QWave Local12 Future Regression Head /
QWave Edge10 Future Regression Head /
Horizon +1·+2·+3·+4 Head Separation /
Factor and Horizon Masks /
No Loss Yet /
No Backward Yet /
No Weight Mutation Yet /
No Logit Mutation /
No Decode Selection Mutation Seal
```

R06B must first prove deterministic prediction tensors with exact R06A geometry and masks before any auxiliary loss is enabled.