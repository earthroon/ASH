# ASH-BASETRAIN-BT-STRUCTURAL-MEDUSA-HEADS-06B

## R06A Exact Physical Target Parent / Canonical Final-RMSNorm Hidden Read-Only Tap / LM-Head-Input Activation Authority / Same-Device Zero-Copy WGPU Binding / Target-Independent Packet Capacity Manifest / Ragged Packet Envelope Prediction / Hangul Packet Encoder Candidate / CJI18 Future Regression Head / QWave Local12 Future Regression Head / QWave Edge10 Future Regression Head / Horizon +1·+2·+3·+4 Independent Parameter Banks / Full BQH Prediction Atlas / R06A Slot·Factor Mask Exact Binding / Target Buffer Absent From Head Dispatch / Deterministic Head Initialization / Base Weight Immutability / Prediction Double-Dispatch Reproducibility / Zero Prediction Payload Readback / Zero Loss / Zero Backward / Zero Optimizer / Zero Head-Weight Update / Zero LM-Head Forward / Zero Logit Mutation / Zero Decode Selection Mutation Seal

> Revision: `BT-STRUCTURAL-MEDUSA-HEADS-06B`
>
> Parent target SSOT: `ASH-BASETRAIN-BT-STRUCTURAL-MEDUSA-TARGETS-06A` physical PASS
>
> Latest observed R06A authority digest: `f3cd207c0cc0754a3973bc9284773035158f8b762d08b28b0b91ab3488313a54`
>
> Latest observed R05 semantic authority digest: `8294f0d9b0e996918ee0a6ad25ded93099c59f6f68d075575940057569318f48`
>
> Current target geometry: `B=1`, `Q=32`, `H=4`, valid prefix=`8`
>
> Canonical hidden source: post-final-RMSNorm activation, exact LM-head input
>
> Proof ledger: `HOLD`

---

# 1. Goal

R06B is a prediction-head admission stage, not a training stage.

```text
R06A exact structural targets / masks
        |
        | label SSOT only
        v
canonical Korean runtime sequence authority
        v
22-layer decoder forward
        v
canonical final hidden
        v
canonical model.norm RMSNorm
        v
normalized hidden [B,Q,D]
        +--> H+1 factor heads
        +--> H+2 factor heads
        +--> H+3 factor heads
        +--> H+4 factor heads
                v
        fixed structural prediction atlas
                v
        exact R06A slot/factor-mask binding
```

No head result may mutate the source hidden, LM-head input, KV state, logits, sampler, or token selection.

---

# 2. Exact Korean runtime sequence binding

The existing R6R6/R6R8/R6R9 forward path historically admitted a fixed `B1,Q32,valid=32` fixture. R06B must not reuse that fixture hidden for an R06A target authority built from the physically admitted Korean valid prefix of 8 tokens.

R06B therefore publishes an exact runtime sequence override file containing:

```text
R01 BaseTrainRuntimeInputSequenceAuthority
R01 deterministic position_ids
R01 sequence authority digest
```

R6R6 consumes that override when `--require-r6-r6-runtime-sequence-override=true`. R6R8 and R6R9-C7 use the runtime authority's `row_valid_lengths` and `position_ids`, not CLI fixture assumptions.

R06B gate requires:

```text
runtime_sequence_override_used = 1
runtime input sequence authority digest == R06A ancestry R01 sequence authority digest
runtime position_ids == R06A ancestry R01 position_ids
runtime row_valid_lengths == R06A ancestry R01 row_valid_lengths
```

This is mandatory before decoder hidden can be accepted as the source for structural prediction.

---

# 3. Canonical hidden tap

Hidden source is exactly:

```text
final decoder residual
  -> canonical model.norm RMSNorm
  -> normalized hidden that would be consumed by the canonical LM head
```

Required:

```text
decoder_forward_count = 1
final_rmsnorm_forward_count = 1
lm_head_forward_count = 0
canonical_logit_surface_count = 0
```

Bind exact:

```text
checkpoint set digest
final hidden pointer digest
final hidden buffer identity digest
final hidden completion token digest
final hidden layer/generation
model.norm.weight tensor identity
RMSNorm epsilon bits
normalized hidden shape [B,Q,D]
```

Final hidden and normalized hidden are read-only.

---

# 4. Same-device zero-copy hidden

Use the admitted Burn-to-raw-WGPU bridge on the final RMSNorm output.

Required:

```text
normalized_hidden_raw_borrow_count = 1
normalized_hidden_host_upload_count = 0
normalized_hidden_payload_readback_count = 0
normalized_hidden_nonfinite_count = 0
```

Forbidden:

```text
GPU hidden -> CPU Vec -> GPU
full hidden readback
JSON hidden transport
cross-device hidden shuttle
```

---

# 5. Target-independent packet capacity

R06A packets are ragged. Current future label lengths must never determine R06B head shape.

R06B performs a frozen tokenizer-manifest-wide audit:

```text
K_row = max Hangul structural scalar capacity across tokenizer vocab, with minimum 1 for byte/unknown fallback ownership
```

The current batch is used only for overflow validation.

Because R05 QW03 is a linear adjacent-scalar graph, a target packet with `k` Hangul rows has at most one incoming edge plus `k-1` internal edges. V1 therefore seals:

```text
K_edge = K_row
```

Overflow is fail-closed. No truncation, pooling, batch-specific resize, or first-K repair is permitted.

---

# 6. Full BQH geometry

Prediction geometry is fixed:

```text
[B,Q,H]
H = 4
H1 = +1
H2 = +2
H3 = +3
H4 = +4
```

Current fixture address space remains:

```text
1 * 32 * 4 = 128 prediction slots
```

R06A currently marks 22 active and 106 masked slots. R06B derives expected active/masked counts from the runtime valid prefix and verifies exact mask parity. Prediction storage does not shrink to active labels.

---

# 7. Factor-separated logical head family

Each horizon owns six logical terminal projections:

```text
HangulRowPresenceHead
HangulRowCountHead
HangulRowDescriptorHead
CJI18RegressionHead
QWLocal12RegressionHead
QWEdge10RegressionHead
```

Therefore:

```text
6 logical families * 4 horizons = 24 logical terminal projections
```

Physical execution may fuse all factor slices for one horizon into one GEMM, yielding four physical fused horizon projections, only if logical factor slice identities and parameter digests remain separately recoverable.

---

# 8. Horizon separation

H1/H2/H3/H4 use distinct deterministic parameter banks.

Forbidden:

```text
silent horizon weight tying
H1 output -> H2 input
H2 output -> H3 input
teacher-forced future target -> later horizon input
```

V1 is parallel horizon prediction from the same source hidden.

---

# 9. Head math and admitted WGPU kernel

V1 terminal math is deliberately simple:

```text
Y_h = X * W_h^T + implicit_zero_bias
```

where `X` is exact canonical final-RMSNorm hidden.

Reuse the already admitted BaseTrain R6R10 same-device f32 reference GEMM path:

```text
BaseTrainLmHeadWaveReferencePipeline
```

Precision contract:

```text
input f32
weight f32
accumulator f32
output f32
```

No unverified new matmul kernel is silently introduced.

---

# 10. Hangul packet encoder candidate

R06A ragged R03 Hangul packet remains semantic authority. R06B defines a deterministic fixed descriptor candidate only for future comparison/training geometry.

V1 descriptor dimension: `16`.

Field order:

```text
0 scalar_kind_code_norm
1 choseong_present
2 choseong_index_norm
3 jungseong_present
4 jungseong_index_norm
5 jongseong_present
6 jongseong_slot_norm
7 has_jongseong
8 role_onset
9 role_vowel
10 role_coda
11 onset_atom_count_norm
12 vowel_atom_count_norm
13 coda_atom_count_norm
14 nonmodern_registry_kind
15 nonmodern_registry_index_norm
```

The encoder excludes:

```text
target token ID
token piece string
decoded future text
absolute normalized scalar index as semantic channel
absolute owner-token position as semantic channel
```

Modern precomposed syllables retain choseong/jungseong/jongseong distinctions; direct/nonmodern/compatibility Jamo use explicit structural registry classes.

---

# 11. Output surfaces

For every `[B,Q,H]` slot:

```text
Hangul presence:        [K_row]
Hangul count:           [K_row + 1]
Hangul descriptor:      [K_row,16]
CJI18:                  [K_row,18]
QWLocal12:              [K_row,12]
QWEdge10:               [K_edge,10]
```

Canonical logical flat order is batch -> query -> horizon -> row/edge slot -> channel. Physical fused storage must publish exact slice boundaries.

---

# 12. Target-independent forward

Allowed head-forward bindings:

```text
normalized hidden
head weights
output buffer
static geometry constants
```

Forbidden:

```text
R06A target values
R06A future Hangul/CJI/Q-wave buffers
target token IDs/pieces/text
R06A factor availability as prediction input
row/edge occupancy masks as prediction input
```

Required:

```text
head_dispatch_target_binding_count = 0
head_forward_target_value_read_count = 0
teacher_forcing_target_input_count = 0
row_occupancy_mask_forward_binding_count = 0
```

R06A masks are post-forward eligibility metadata only.

---

# 13. Deterministic initialization

New structural Medusa parameters are created deterministically and live in a namespace separate from the base model.

V1:

```text
Xavier-uniform
implicit bias = 0
seed = SHA256(head manifest digest + horizon/factor role) -> deterministic SplitMix64 stream
```

Initialization is executed twice and parameter digests must match.

Required:

```text
head_parameter_init_runs = 2
head_parameter_init_digest_match = 1
horizon_parameter_alias_count = 0
factor_parameter_alias_count = 0
base_parameter_alias_count = 0
head_parameter_post_init_mutation_count = 0
base_weight_mutation_count = 0
```

Initialization is not training. No optimizer or gradient exists in R06B.

---

# 14. Same-device prediction and parity

For H1..H4:

```text
same normalized hidden
same deterministic horizon weight
  -> prediction A
  -> prediction B
```

Both outputs receive same-device finite guards and exact GPU parity comparison.

Required:

```text
all prediction nonfinite counts = 0
prediction_reproducibility_runs = 2
prediction_reproducibility_match = 1
prediction_parity_mismatch_count = 0
prediction_parity_nonfinite_count = 0
full prediction payload readback = 0
```

Only compact finite/parity receipts may cross to host.

---

# 15. Mask and target geometry binding

After prediction, bind exact R06A:

```text
slot ledger digest
factor mask ledger digest
packet ledger digest
```

Current expected physical values from R06A:

```text
prediction slots = 128
active = 22
masked = 106
source PAD = 96
out of valid prefix = 10
synthetic EOS = 0
H1/H2/H3/H4 active = 7/6/5/4
```

These counts are derived from runtime valid length and compared to R06A, not used to size the heads.

---

# 16. Parent/base immutability

Capture and verify unchanged:

```text
R06A authority
R05 authority
R04 authority
R03 authority
R02 authority
R01 authority
runtime input sequence authority
checkpoint set digest
final hidden pointer/buffer/completion identities
final hidden generation
base parameter identities
```

No Medusa output is added to the hidden residual or LM-head input.

---

# 17. Training and decode boundary

R06B must keep:

```text
loss = 0
backward = 0
gradient buffers = 0
optimizer = 0
optimizer steps = 0
parameter updates = 0
head checkpoint writes = 0

LM-head forward = 0
canonical logits = 0
logit mutation = 0
KV mutation = 0
sampler mutation = 0
token selection = 0
argmax/topk = 0
speculative decode = 0
```

---

# 18. Runtime receipts

Default directory:

```text
workspace/runtime/basetrain/structural_medusa_heads/06b
```

Required receipts:

```text
parent_binding_receipt.json
canonical_final_norm_hidden_tap_receipt.json
structural_medusa_capacity_manifest_receipt.json
hangul_packet_encoder_manifest_receipt.json
structural_medusa_head_manifest_receipt.json
structural_medusa_head_parameter_bank_receipt.json
structural_medusa_prediction_atlas_receipt.json
structural_medusa_prediction_mask_binding_receipt.json
structural_medusa_prediction_finite_receipt.json
structural_medusa_prediction_reproducibility_receipt.json
parent_immutability_receipt.json
final_receipt.json
```

No full hidden/prediction arrays are written to receipts.

---

# 19. Required CLI policy

Required true gates cover:

```text
R06A physical parent
final-RMSNorm LM-head-input tap
hidden read-only
zero-copy same-device
frozen tokenizer-wide capacity audit
Kedge derived from Krow
full BQH prediction atlas
horizon-separated parameters
factor-separated logical heads
Hangul descriptor candidate
CJI18/QWLocal12/QWEdge10 heads
exact R06A slot/factor masks
target buffers absent from forward
deterministic initialization
base and head-post-init immutability
double prediction dispatch
zero payload readback
zero LM-head forward
zero loss/backward/optimizer
zero logit/decode mutation
```

Forbidden false gates cover batch-derived capacity, row/edge truncation, target-conditioned forward, token/text future features, horizon weight sharing, recurrence, hidden fusion, LM-head/logit/decode paths, all training updates, and prediction payload readback.

---

# 20. Physical terminal evidence shape

```text
[bt-structural-medusa-heads-06b]
parent_r06a_physical_pass=1
parent_targets_authority_bound=1
runtime_sequence_override_used=1
runtime_input_sequence_authority_match=1

decoder_forward_count=1
final_rmsnorm_forward_count=1
lm_head_forward_count=0
source_hidden_role=final_rmsnorm_lm_head_input
source_hidden_batch=1
source_hidden_seq=32
source_hidden_width=<checkpoint>
source_hidden_pointer_bound=1
source_hidden_buffer_bound=1
source_hidden_completion_bound=1
source_hidden_mutation_count=0

normalized_hidden_raw_borrow_count=1
normalized_hidden_host_upload_count=0
normalized_hidden_payload_readback_count=0
normalized_hidden_nonfinite_count=0

capacity_audit_scope=frozen_tokenizer_manifest
row_capacity=<tokenizer-wide audited>
edge_capacity=<row_capacity>
current_batch_max_target_rows=<runtime>
current_batch_max_target_edges=<runtime>
capacity_overflow_count=0

horizon_count=4
logical_terminal_head_count=24
physical_fused_head_count=4
horizon_parameter_alias_count=0
factor_parameter_alias_count=0
base_parameter_alias_count=0

head_parameter_init_runs=2
head_parameter_init_digest_match=1
head_parameter_post_init_mutation_count=0
base_weight_mutation_count=0

prediction_slot_count=128
prediction_active_mask_count=22
prediction_masked_count=106
source_pad_mask_count=96
target_outside_valid_prefix_mask_count=10
synthetic_eos_mask_count=0
h1_active_count=7
h2_active_count=6
h3_active_count=5
h4_active_count=4

prediction_target_geometry_mismatch_count=0
prediction_target_mask_binding_mismatch_count=0
horizon_mapping_mismatch_count=0
head_dispatch_target_binding_count=0
head_forward_target_value_read_count=0
teacher_forcing_target_input_count=0
row_occupancy_mask_forward_binding_count=0

all_prediction_nonfinite_count=0
all_prediction_payload_readback_count=0
prediction_reproducibility_runs=2
prediction_reproducibility_match=1
prediction_parity_mismatch_count=0
prediction_parity_nonfinite_count=0

hidden_fusion=0
lm_head_input_mutation=0
kv_cache_mutation=0
canonical_logit_surface_count=0
logit_mutation=0
sampler_mutation=0
token_selection_mutation=0
speculative_decode_count=0
loss_count=0
backward_count=0
gradient_buffer_count=0
optimizer_count=0
parameter_update_count=0

all_parent_authorities_unchanged=1
proof_ledger=HOLD
```

---

# 21. PASS token

```text
PASS_ASH_BASETRAIN_BT_STRUCTURAL_MEDUSA_HEADS_06B_BT_STRUCTURAL_MEDUSA_TARGETS_06A_PHYSICAL_PARENT_EXACT_TARGET_PACKET_SLOT_FACTOR_MASK_AND_BQH4_GEOMETRY_BINDING_CANONICAL_FINAL_DECODER_HIDDEN_EXACT_POINTER_BUFFER_COMPLETION_LINEAGE_CANONICAL_MODEL_NORM_FINAL_RMSNORM_OUTPUT_AS_EXACT_LM_HEAD_INPUT_HIDDEN_SOURCE_DECODER_FORWARD_ONE_FINAL_RMSNORM_FORWARD_ONE_LM_HEAD_FORWARD_ZERO_SAME_DEVICE_ZERO_COPY_NORMALIZED_HIDDEN_RAW_BORROW_ZERO_HOST_UPLOAD_ZERO_HIDDEN_PAYLOAD_READBACK_HIDDEN_READ_ONLY_ZERO_HIDDEN_MUTATION_TARGET_INDEPENDENT_TOKENIZER_WIDE_PACKET_CAPACITY_MANIFEST_ZERO_BATCH_DERIVED_CAPACITY_KEDGE_EQUALS_KROW_UNDER_R05_LINEAR_ADJACENCY_CONTRACT_ZERO_ROW_OR_EDGE_TRUNCATION_FULL_BQH_PREDICTION_ATLAS_128_CURRENT_FIXTURE_FOUR_HORIZON_INDEPENDENT_PARAMETER_BANKS_ZERO_HORIZON_WEIGHT_ALIAS_FACTOR_SEPARATED_HANGUL_PRESENCE_COUNT_DESCRIPTOR_CJI18_QWLOCAL12_QWEDGE10_LOGICAL_HEAD_FAMILIES_24_LOGICAL_TERMINAL_PROJECTIONS_HANGUL_PACKET_ENCODER_CANDIDATE_EXCLUDES_TARGET_TOKEN_ID_PIECE_TEXT_AND_ABSOLUTE_SCALAR_INDEX_SEMANTIC_FEATURES_CJI18_EXACT_FIELD_ORDER_QWLOCAL12_EXACT_FIELD_ORDER_QWEDGE10_EXACT_FIELD_ORDER_HEAD_FORWARD_BINDINGS_HIDDEN_PLUS_HEAD_PARAMETERS_ONLY_ZERO_R06A_TARGET_BUFFER_BINDING_ZERO_TEACHER_FORCING_ZERO_FACTOR_MASK_FORWARD_CONDITIONING_DETERMINISTIC_HEAD_INITIALIZATION_DOUBLE_INIT_DIGEST_PARITY_BASE_PARAMETER_ZERO_ALIAS_BASE_WEIGHT_ZERO_MUTATION_HEAD_POST_INIT_ZERO_MUTATION_SAME_DEVICE_HEADWISE_ATLAS_EXECUTION_FINITE_ALL_OUTPUT_SURFACES_ZERO_PREDICTION_PAYLOAD_READBACK_DOUBLE_DISPATCH_PREDICTION_REPRODUCIBILITY_EXACT_R06A_SLOT_MASK_ACTIVE_22_MASKED_106_SOURCE_PAD_96_OUT_OF_PREFIX_10_SYNTHETIC_EOS_ZERO_H1_H2_H3_H4_ACTIVE_7_6_5_4_SHARED_OWNER_LOSS_POLICY_DEFERRED_ZERO_LOSS_ZERO_BACKWARD_ZERO_GRADIENT_ZERO_OPTIMIZER_ZERO_PARAMETER_UPDATE_ZERO_HEAD_CHECKPOINT_WRITE_ZERO_HIDDEN_FUSION_ZERO_LM_HEAD_INPUT_MUTATION_ZERO_KV_MUTATION_ZERO_CANONICAL_LOGIT_SURFACE_ZERO_LOGIT_MUTATION_ZERO_SAMPLER_MUTATION_ZERO_TOKEN_SELECTION_ZERO_SPECULATIVE_DECODE_PARENT_AUTHORITIES_UNCHANGED_PROOF_LEDGER_HOLD_SEALED
```

---

# 22. Next boundary

```text
ASH-BASETRAIN-BT-STRUCTURAL-MEDUSA-TRAIN-06C

R06B Exact Physical Head Parent /
R06A Exact Target Parent /
Factor-Separated Auxiliary Loss /
Hangul Presence·Count·Descriptor Loss Candidate /
CJI18 Regression Loss /
QWLocal12 Regression Loss /
QWEdge10 Regression Loss /
Horizon-Specific Loss Weights /
Exact Slot·Factor·Row·Edge Masks /
Shared-Owner Loss Eligibility Policy /
No Base-LM Loss Replacement /
Head-Only Backward First /
Base-Model Gradient Gate Closed /
Optimizer Head-Parameter Namespace Only /
Gradient Finite·Norm Receipt /
Single-Step Weight Mutation /
Pre/Post Parameter Digest /
No Logit Mutation /
No Decode Selection Mutation Seal
```

R06C begins with head-only training while the base decoder remains frozen. Base-model gradient coupling remains out of scope until the structural heads show finite, correctly masked gradients and deterministic single-step mutation.

---

# 23. Architecture seal

`BT-STRUCTURAL-MEDUSA-HEADS-06B` is the first learned-parameter surface in the Korean structural path, but not a training stage. The exact R06A Korean runtime sequence is injected into the physically admitted BaseTrain forward path so the tapped hidden belongs to the same token/valid-length authority as the structural labels. The tap is the exact post-final-RMSNorm activation that would feed the canonical LM head. Four horizon-specific same-device fused projections produce logically factor-separated Hangul/CJI/QWLocal/QWEdge predictions. Head capacity comes from a frozen tokenizer-wide audit, not current future labels. Target values and masks never enter forward math. Head initialization is deterministic, base weights and hidden remain immutable, prediction payloads remain on GPU, and admission is based on finite guards, exact target geometry/mask lineage, and double-dispatch parity. LM-head forward, logits, loss, backward, optimizer, parameter updates, sampler, and speculative decode remain blocked.