# ASH-BASETRAIN-INFERENCE-CANARY-01

## R6-R10 Physical Forward Parent / Canonical Logit Surface Exact Lease / Runtime Input Sequence Authority Binding / Last Valid Query Selection / GPU Full-Vocab Top-1 Argmax / Compact Token-ID·Logit Readback / Tokenizer Vocabulary Exact Decode / Single Next-Token Observation / Input-to-Output Provenance Receipt / Zero Logit Payload Readback / Zero Loss Execution / Zero Backward / Zero Weight Mutation / No Sampling / No Autoregressive Loop / No KV Cache / No Production Inference Claim Seal

> Branch role: BaseTrain forward-side inference validation canary
> Physical parent SSOT: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R10` physical PASS
> Forward numerical SSOT: `LogitSurfaceAuthoritySlot`
> Runtime input SSOT: `BaseTrainRuntimeInputSequenceAuthority`
> Finite SSOT: `burn_webgpu_backend::wgsl_numeric_contract`
> Tokenizer decode SSOT: explicit `TokenizerManifest` + `tokenizer_core::decode_ssot`
> Selection: deterministic full-vocab GPU argmax
> Sampling / autoregressive loop / KV cache / loss / backward / optimizer / production inference claim: BLOCKED
> Proof ledger: HOLD

---

# 1. Purpose

CANARY-01 proves one narrow statement only:

```text
actual R6-R10 input
→ actual full decoder forward
→ canonical [B,Q,V] logits
→ last runtime-valid query row
→ deterministic GPU full-vocab top-1
→ compact token-id/logit observation
→ exact tokenizer manifest lookup/decode
→ one next-token observation
```

It is not a sampler, generator, chat runtime, quality gate, or production inference admission.

---

# 2. Branch authority

The inference canary branches directly from R6-R10:

```text
                                      ┌─ R6-R11 loss → R6-R12 backward
R6-R10 canonical logits ──────────────┤
                                      └─ INFERENCE-CANARY-01
```

Required:

```text
run_r6_r10_final_rmsnorm_lm_head_forward_session() = exactly 1
run_r6_r11_causal_forward_loss_session() = 0
run_r6_r12_causal_loss_backward_seed_session() = 0
```

The dedicated canary gate must not import R6-R11/R6-R12 as active parents.

---

# 3. Typed parent access

Use R6-R10 typed accessors:

```rust
runtime()
input_sequence_authority()
canonical_logit_pointer()
```

Raw `.parent.parent...` traversal is forbidden.

---

# 4. Canonical logit lease

The only selection source is the live R6-R10 `LogitSurfaceAuthoritySlot`.

Before dispatch bind the exact final receipt identity:

```text
pointer digest
completion token
checkpoint set digest
shape BQV
scalar count
buffer identity
publication generation
```

Lease lifecycle:

```text
state before = Resident
active leases before = 0
acquire = 1
active during = 1
release = 1
active after = 0
state after = Resident
```

After observation the canonical logit pointer must be byte-semantic equal to its pre-canary snapshot.

---

# 5. Runtime input authority

Do not reparse token IDs as an inference SSOT.

Use the exact retained `BaseTrainRuntimeInputSequenceAuthority`, reseal it, and require exact equality.

Initial CANARY-01 admission requires:

```text
batch_size == 1
input B/Q == canonical logit B/Q
row_valid_lengths.len() == 1
1 <= valid_length <= Q
```

Input authority must remain unchanged after the canary.

---

# 6. Last valid query

Inference position authority:

```text
valid_length = row_valid_lengths[0]
last_valid_query = valid_length - 1
selected_flat_row = last_valid_query
```

Do not reuse the R6-R11 causal-loss target range.

For the current admitted fixture:

```text
B=1
Q=32
V=48259
BQV=1544288
valid_length=32
loss rows = q0..q30
inference query = q31
row_offset = 31*48259 = 1496029
```

Using q30 is an inference semantic failure.

---

# 7. GPU full-vocab top-1

CANARY-01 introduces a dedicated raw-WGPU argmax operator, not a sampling pipeline.

Implementation:

```text
Stage 1:
  workgroup width = 256
  each selected-row vocab scalar is visited exactly once
  one deterministic local winner per workgroup

Stage 2:
  reduce Stage-1 winners to one candidate
```

For current V=48259:

```text
Stage-1 partials = ceil(48259/256) = 189
Stage-2 output = 1
```

These are runtime-derived, not model constants.

Plan admission binds:

```text
max_compute_workgroups_per_dimension
max_storage_buffer_binding_size
max_buffer_size
```

Fail closed if the reduction cannot be admitted.

---

# 8. Comparator

Exact ordering:

1. all selected-row logits must be finite;
2. larger logit wins;
3. exact equal logit uses lower token id.

```text
same logit → min(token_id)
```

No random tie break.

---

# 9. Finite contract

New shaders consume the shared backend numeric contract:

```wgsl
fn finite_f32(value: f32) -> bool {
    let exponent_bits = bitcast<u32>(value) & 0x7f800000u;
    return exponent_bits != 0x7f800000u;
}
```

No local `isFinite` assumption.

Local selected-row receipt requires:

```text
visited = V
finite = V
nonfinite = 0
final candidate count = 1
selected token id < V
selected logit finite
```

Any nonfinite observation fails the canary. It is not ignored.

---

# 10. No probability/sampling path

Forbidden:

```text
softmax
log-softmax
temperature
top-k filtering
top-p filtering
min-p
random sampling
sampling seed
repetition/frequency penalties
reranking
```

Top-1 means mathematical argmax across all V canonical logits.

---

# 11. Readback boundary

Raw canonical logit payload readback is forbidden:

```text
full BQV readback = 0
selected [V] row readback = 0
CPU argmax = 0
CPU finite scan = 0
```

Only compact reduction output and counters may be mapped.

Semantic winner payload:

```text
u32 token_id
f32 logit
= 8 bytes
```

The current aligned status/staging ABI is 32 bytes. Report both semantic compact bytes and physical readback bytes truthfully.

---

# 12. Tokenizer manifest input

CANARY-specific response file uses:

```text
--inference-canary-tokenizer-manifest
${ASH_TOKENIZER_MANIFEST}
```

The tokenizer manifest remains an external runtime input and is not embedded in the baked code ZIP.

Relative paths are resolved against `--repo-root`; absolute paths are accepted explicitly. Missing environment value or missing file fails closed.

---

# 13. Tokenizer identity admission

Before textual decode require:

```text
manifest parses as tokenizer_core::TokenizerManifest
manifest.trainer.vocab_size == V
manifest.vocab.len() == V
embedded manifest hash recomputes exactly under the existing manifest convention
vocab hash recomputes exactly
reserved-token hash recomputes exactly
canonical vocab ids are unique
canonical ids cover exactly 0..V-1
all ids are in range
reserved id/token entries agree with canonical vocab
core special id/token entries agree with canonical vocab
selected token id resolves exactly once
```

No vocab padding, truncation, remap, resize, nearest-id fallback, historical tokenizer fallback, or alternate manifest search.

The authority binds both exact file SHA-256 and intrinsic manifest/hash identities.

---

# 14. Exact decode

Selected integer id is passed unchanged to the canonical tokenizer vocabulary.

Use:

```text
decode_ssot_token_piece_from_manifest
decode_manifest_token_sequence
decode_single_token_fragment
```

The raw vocab piece is always retained as provenance.

Decode states distinguish at minimum:

```text
text
sentencepiece_text
byte
control
unknown
invalid_utf8
```

A control token or incomplete byte fragment is not replaced by second-best top-1. Its token identity remains the observation; printable text may be suppressed/deferred.

Linguistic quality is not a PASS criterion.

---

# 15. Provenance receipt

Seal one input-to-output receipt binding:

```text
checkpoint set digest
input sequence authority digest
input token-ids digest
row-valid-lengths digest
canonical logit pointer/completion/buffer identity
B/Q/V
valid length
last valid query
selected flat row
top1 reduction receipt digest
selected token id
selected logit bits
tokenizer authority digest
selected vocab piece
decoded fragment/classification
```

This is an observation receipt only. It is not a generated-token authority.

---

# 16. No generation mutation

Required zeros:

```text
loss execution = 0
backward = 0
optimizer = 0
weight mutation = 0
sampling = 0
autoregressive loop = 0
sequence append = 0
second forward = 0
KV cache = 0
production inference claim = 0
```

The selected token is not appended to runtime input state.

---

# 17. Output evidence

Runtime evidence directory:

```text
workspace/runtime/basetrain/inference_canary/01/
```

Recommended files:

```text
top1_receipt.json
tokenizer_authority_receipt.json
provenance_receipt.json
final_receipt.json
```

These runtime receipts are not baked package inputs.

---

# 18. Implementation surface

```text
crates/burn_webgpu_backend/src/
  base_train_inference_top1.rs
  lib.rs

crates/burn_webgpu_backend/src/shaders/
  base_train_inference_top1_stage1.wgsl
  base_train_inference_top1_stage2.wgsl

crates/orchestrator_local/src/
  base_train_inference_canary_01.rs

crates/orchestrator_local/src/bin/
  ash_basetrain_inference_canary_01_gate.rs

specs/cli/
  ash_basetrain_inference_canary_01.args
```

Canonical execution remains Rust + WGPU/WGSL + Rust `tokenizer_core`. No JS/TS/Python inference core.

---

# 19. CLI policy

Required true:

```text
--require-inference-canary-r6-r10-physical-parent
--require-inference-canary-canonical-logit-exact-lease
--require-inference-canary-runtime-input-authority
--require-inference-canary-single-batch
--require-inference-canary-last-valid-query
--require-inference-canary-full-vocab-top1
--require-inference-canary-finite-selected-row
--require-inference-canary-deterministic-lowest-id-tie-break
--require-inference-canary-compact-result-readback
--require-inference-canary-tokenizer-manifest-identity
--require-inference-canary-exact-vocab-id-lookup
--require-inference-canary-shared-tokenizer-decode-ssot
--require-inference-canary-input-output-provenance
--require-inference-canary-zero-logit-payload-readback
--require-inference-canary-zero-loss
--require-inference-canary-zero-backward
--require-inference-canary-zero-weight-mutation
--require-inference-canary-no-sampling
--require-inference-canary-no-autoregressive-loop
--require-inference-canary-no-kv-cache
--require-inference-canary-no-production-claim
```

Required false:

```text
--allow-inference-canary-cpu-argmax
--allow-inference-canary-logit-payload-readback
--allow-inference-canary-softmax
--allow-inference-canary-temperature
--allow-inference-canary-top-k
--allow-inference-canary-top-p
--allow-inference-canary-random-sampling
--allow-inference-canary-token-remap
--allow-inference-canary-sequence-append
--allow-inference-canary-second-forward
--allow-inference-canary-kv-cache
--allow-inference-canary-loss
--allow-inference-canary-backward
--allow-inference-canary-optimizer
--allow-inference-canary-production-inference-claim
```

Response files remain separate. Do not nest one `@file` inside another.

---

# 20. Cargo run

```powershell
$env:ASH_TOKENIZER_MANIFEST = "D:\path\to\tokenizer_manifest.json"

cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_inference_canary_01_gate `
  -- "@specs/cli/ash_basetrain_atlas_wave_02_r6_r9.args" `
     "@specs/cli/ash_basetrain_inference_canary_01.args"
```

No `cargo clean` is required unless independent evidence specifically indicates a stale binary.

---

# 21. Expected current terminal evidence

Current physical fixture should establish:

```text
checkpoint_layers=22
logit_shape_bqv=1x32x48259
logit_scalar_count=1544288
input_token_count=32
row_valid_length=32
last_valid_query=31
selected_flat_row=31
vocab_size=48259
top1_workgroup_size=256
top1_stage1_partials=189
top1_reduction_passes=2
top1_visited=48259
top1_finite=48259
top1_nonfinite=0
top1_final_candidate_count=1
selected_token_id=<physical observation>
selected_logit=<physical observation>
top1_compact_result_bytes=8
top1_physical_readback_bytes=32
tokenizer_identity_bound=1
exact_vocab_piece_resolved=1
logit_pointer_unchanged=1
input_authority_unchanged=1
raw_logit_payload_readback=0
loss_execution=0
backward=0
optimizer=0
weight_mutation=0
sampling=0
autoregressive_loop=0
sequence_append=0
second_forward=0
kv_cache=0
production_inference_claim=0
proof_ledger=HOLD
```

The selected token id/logit/piece/fragment are deliberately not predeclared.

---

# 22. Static closure

Implementation static closure requires:

```text
changed surface limited to the canary implementation/export/CLI files
new gate contains R6-R10 and no R6-R11/R6-R12 active module
R6-R10 call count = 1
raw parent.parent chain = 0
exact logit lease present
input authority reseal/equality present
single-batch gate present
last_valid_query = valid_length-1
no loss-target authority reuse
checked selected row offset
full-vocab visited/finite gates
shared finite contract used by both shaders
no isFinite builtin
lowest-token-id tie rule in both reduction stages
GPU hierarchical partial reduction present
only status/compact result mapped
storage/buffer/dispatch limits bound
TokenizerManifest trainer/vocab geometry exact
embedded manifest/vocab/reserved hashes revalidated
canonical id gaps/duplicates rejected
shared tokenizer decode SSOT used
combined response-file keys have no duplicates
manifest env placeholder present
forbidden training/sampling/generation claims remain zero
```

Current code bake static closure: `75/75 PASS`.

---

# 23. PASS token

```text
PASS_ASH_BASETRAIN_INFERENCE_CANARY_01_R6_R10_PHYSICAL_FORWARD_PARENT_SINGLE_SAME_INVOCATION_CANONICAL_LOGIT_SURFACE_EXACT_POINTER_BUFFER_COMPLETION_AND_BQV_LEASE_RUNTIME_INPUT_SEQUENCE_AUTHORITY_EXACT_BINDING_SINGLE_BATCH_LAST_RUNTIME_VALID_QUERY_SELECTION_NOT_CAUSAL_LOSS_TARGET_ROW_FULL_VOCAB_GPU_DETERMINISTIC_TOP1_ARGMAX_ALL_SELECTED_ROW_LOGITS_VISITED_ZERO_NONFINITE_LOWEST_TOKEN_ID_EXACT_TIE_BREAK_ZERO_SOFTMAX_ZERO_PROBABILITY_SURFACE_COMPACT_TOKEN_ID_AND_LOGIT_RESULT_READBACK_ZERO_RAW_LOGIT_PAYLOAD_READBACK_TOKEN_ID_VOCAB_RANGE_EXACT_TOKENIZER_MANIFEST_IDENTITY_AND_VOCAB_GEOMETRY_BINDING_SHARED_TOKENIZER_CORE_DECODE_SSOT_EXACT_SELECTED_VOCAB_PIECE_RESOLUTION_SINGLE_NEXT_TOKEN_OBSERVATION_INPUT_TO_OUTPUT_PROVENANCE_RECEIPT_CANONICAL_LOGIT_POINTER_UNCHANGED_RUNTIME_INPUT_AUTHORITY_UNCHANGED_ZERO_LOSS_EXECUTION_ZERO_BACKWARD_ZERO_OPTIMIZER_ZERO_WEIGHT_MUTATION_ZERO_SAMPLING_ZERO_AUTOREGRESSIVE_LOOP_ZERO_SEQUENCE_APPEND_ZERO_SECOND_FORWARD_ZERO_KV_CACHE_ZERO_PRODUCTION_INFERENCE_CLAIM_PROOF_LEDGER_HOLD_SEALED
```

---

# 24. PASS meaning

Physical PASS proves only:

```text
R6-R10 is usable as an exact one-step inference parent
the actual runtime valid length selects the correct final query row
the canonical logit buffer is consumed without payload readback
all V logits of that row participate in deterministic GPU argmax
one exact finite winner is compactly observed
the winning integer id belongs to the exact explicitly bound tokenizer vocabulary
the repository tokenizer decode SSOT resolves/classifies that id
input → logits → GPU selection → tokenizer identity is linked by one provenance receipt
no training/generation state is mutated
```

It does not prove language quality, multi-token generation, sampling, EOS/stop behavior, KV-cache correctness, long-context inference, batch inference, throughput, or production serving.

---

# 25. Admission state after physical PASS

```text
R6-R10 physical forward/logits                  = ADMITTED
R6-R11 causal forward loss                     = ADMITTED on training branch
R6-R12 logit-gradient backward seed            = ADMITTED on training branch
INFERENCE-CANARY-01 one-step top1 observation  = ADMITTED on canary PASS

Autoregressive generation                      = BLOCKED
Sampling                                       = BLOCKED
KV cache                                       = BLOCKED
Production inference                           = BLOCKED
Proof ledger                                   = HOLD
```

---

# 26. Natural next boundary

After CANARY-01 physical PASS:

```text
ASH-BASETRAIN-INFERENCE-CANARY-02

Single Token Append Candidate /
CANARY-01 Selected Token Provenance Exact Binding /
Runtime Sequence Extension Candidate /
Second Physical R6-R10 Forward /
Two-Step Token Lineage /
Tokenizer Decode Continuity /
No KV Cache Yet /
No Sampling Yet /
No Persistent Generation Session Yet Seal
```

KV-cache and stochastic sampling remain later independent authority boundaries.

---

# 27. Architecture seal

> CANARY-01 is a one-token observation branch rooted directly at the physically admitted R6-R10 canonical logit surface. It selects the final runtime-valid query, not the final causal-loss target row. One exact logit lease exposes no CPU payload; a dedicated same-device two-stage reduction visits the entire selected vocabulary row, rejects nonfinite evidence, and chooses the highest logit with a deterministic lowest-token-id tie rule. Only the compact winner and counters return to the host. That integer is admitted for textual interpretation only after an explicitly supplied TokenizerManifest proves exact file/intrinsic/hash/vocabulary identity against the model's V dimension, after which the existing tokenizer_core decode SSOT resolves the exact vocabulary piece and classifies its text fragment without remap or second-best substitution. The observation is sealed with input, logit, argmax, and tokenizer provenance. It is not appended, there is no second forward, no sampler, no KV cache, no training path, no mutation, and no production-inference claim.
