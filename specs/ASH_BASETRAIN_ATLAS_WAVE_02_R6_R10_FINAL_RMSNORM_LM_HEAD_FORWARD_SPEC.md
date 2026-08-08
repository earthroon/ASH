# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R10

## Final RMSNorm / C9 Final Hidden Exact Consumption / Final Decoder Completion Binding / Final Norm Weight Authority / LM Head Weight Residency / Streaming Materialization / Logit Surface Publication / Runtime-Derived BQV Coverage / Zero Hidden Recompute / Zero Decoder Weight Reload / Zero Payload Readback / Forward Loss Still Blocked Seal

> Physical admission parent SSOT: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R9-C10-D1` physical PASS  
> Parent health verdict: `HEALTHY`  
> Parent decoder completion: checkpoint-bounded final decoder completion sealed  
> Final hidden source: live `LayerHiddenAuthoritySlot` pointer bound through C10 -> C9 completion lineage  
> Decoder-weight runtime authority: `BaseTrainLayerWeightResidencySlot`, final decoder block remains resident and immutable in R6-R10  
> Checkpoint tensor-set authority: `BaseTrainAtlasWave02R5CheckpointTensorSetAuthority`  
> Final norm physical tensor: `model.norm.weight`  
> LM-head source authority: checkpoint `tie_word_embeddings` + logical alias authority, never filename guessing  
> Full LM-head host materialization: `FORBIDDEN`  
> Full LM-head GPU residency: `FORBIDDEN`  
> Canonical logits publication: one final `LogitSurfaceAuthoritySlot` adoption after all vocab waves pass  
> Forward loss / backward / optimizer / sampling / production inference: `BLOCKED`  
> Proof ledger: `HOLD`

---

# 1. Purpose

R6-R9-C9 proved that the real decoder stack can advance from its admitted starting layer to the checkpoint-defined final decoder layer through the canonical decoder-weight atlas-wave transport.

R6-R9-C10 and C10-D1 proved that the repeated destructive rebind path remained healthy across the long run and that the final decoder completion state is still live and internally consistent.

R6-R10 is the first patch allowed to **consume the final decoder hidden state** and cross the decoder/output-head boundary.

The canonical forward boundary becomes:

```text
C10-D1 HEALTHY parent
    ↓
exact live final Hidden-L lease
    ↓
checkpoint-authoritative model.norm.weight
    ↓
Final RMSNorm exactly once
    ↓
normalized hidden [B,Q,H]
    ↓
resolve logical LM-head source
    ↓
stream contiguous vocab-row waves from [V,H]
    ↓
per-wave candidate projection + independent same-device reference parity
    ↓
private full logits surface [B,Q,V]
    ↓
full wave coverage + finite + ownership/fence seal
    ↓
ONE canonical LogitSurfaceAuthoritySlot adoption
```

R6-R10 does not compute loss and does not mutate model/checkpoint weights.

---

# 2. Parent state is consumed, not reconstructed

R6-R10 runs one same-invocation C10-D1 parent session.

It does not rerun C9 after C10 completion and does not reconstruct the final hidden from historical receipts.

Required live-parent relation:

```text
C10 decoder completion health final hidden pointer
    == C9 final completion hidden pointer
    == live LayerHiddenAuthoritySlot current pointer
```

The exact final hidden tensor is obtained only through a live hidden execution lease.

Forbidden:

```text
re-embed input tokens
re-run Layer0..final decoder
re-run only the final decoder layer
reconstruct Hidden-L from debug JSON
load Hidden-L from disk
read back Hidden-L to CPU and rebuild a tensor
```

---

# 3. Parent health gate

R6-R10 requires the C10 parent to satisfy all current observable health requirements before any output-head checkpoint payload is read.

At minimum:

```text
parent C10 pass = true
parent C10 health verdict = HEALTHY
parent decoder completion health verdict = HEALTHY
parent payload readback = 0
parent weight payload readback = 0
parent generation drift = 0
parent pointer lineage break = 0
parent runtime authority overlap = 0
parent progressive legacy runtime loader = 0
parent same-operation legacy fallback = 0
parent final weight active lease = 0
parent final hidden active lease = 0
```

If the parent is not healthy, R6-R10 does not attempt output-head execution.

---

# 4. Final decoder completion binding

R6-R10 binds the typed `R6R9C10DecoderCompletionHealthSeal` to the live runtime.

Required final decoder relations:

```text
final_decoder_layer = checkpoint.num_hidden_layers - 1
final_hidden_layer   = checkpoint.num_hidden_layers
final Weight state   = Resident
final Weight pointer = C10 final weight pointer
final Hidden pointer = C10 final hidden pointer
```

The following final hidden fields must match exactly:

```text
layer index
hidden generation
pointer digest
buffer identity digest
completion token digest
semantic BQH shape
```

No digest-shape-only validation is sufficient.

---

# 5. C9 final hidden exact consumption

R6-R10 takes one `LayerHiddenExecutionLease` against the current final hidden pointer.

Required:

```text
captured_layer_index            = final_hidden_layer
captured_generation             = final_hidden_generation
captured_pointer_digest         = C10 final hidden pointer digest
captured_buffer_identity_digest = C10 final hidden buffer identity digest
captured_completion_token       = C10 final hidden completion token
captured_semantic_shape_bqh     = C10 final hidden BQH
```

The lease is validated before final RMSNorm use and again before release.

The original hidden slot remains unchanged through all of R6-R10.

---

# 6. Hidden generation is not bumped

Final RMSNorm is an output-head consumer, not a hidden-state commit.

R6-R10 must not call:

```text
LayerHiddenAuthoritySlot::commit_next_layer(...)
```

Required:

```text
hidden commit count = 0
hidden layer before = hidden layer after
hidden generation before = hidden generation after
hidden pointer before = hidden pointer after
hidden buffer identity before = hidden buffer identity after
hidden completion token before = hidden completion token after
```

The normalized hidden is a new output-head activation, not `Hidden-L+1`.

---

# 7. Decoder weight authority remains untouched

R6-R10 does not need a decoder block to perform final RMSNorm or LM-head projection.

The final decoder weight slot remains resident exactly as C10 left it.

Required before/after equality:

```text
final decoder weight layer
final decoder weight generation
final decoder weight transition serial
final decoder weight pointer digest
final decoder block identity digest
resident decoder block count = 1
resident decoder weight tensor count = 9
```

Forbidden:

```text
C8 rebind
C5 decoder staging
C4 decoder-wave plan
legacy decoder loader
final decoder rebuild
decoder checkpoint reread
final decoder source eviction
```

R6-R10 decoder weight reload count is exactly zero.

---

# 8. Output-head checkpoint authority is already present

The current checkpoint authority explicitly models the output-head tensors.

The canonical expected schema already contains:

```text
model.norm.weight
    canonical role = final_norm
    shape          = [hidden_size]
```

LM head authority is determined by `config.tie_word_embeddings`.

R6-R10 must use the existing checkpoint tensor-set authority rather than invent a separate model-config parser.

---

# 9. Final norm source authority

R6-R10 resolves exactly one physical tensor:

```text
key   = model.norm.weight
role  = final_norm
shape = [H]
```

Required:

```text
tensor exists exactly once
tensor canonical role == final_norm
tensor layer_index == None
tensor shape == [checkpoint.config.hidden_size]
tensor dtype is admitted by R6 checkpoint decode
tensor identity digest is bound to checkpoint set digest
```

No layer norm tensor may substitute for `model.norm.weight`.

---

# 10. LM-head logical authority resolution

R6-R10 resolves a logical LM-head source with two mutually exclusive modes.

```rust
pub enum R6R10LmHeadSourceMode {
    TiedEmbeddingAlias,
    UntiedPhysicalLmHead,
}
```

The mode comes only from:

```text
checkpoint.config.tie_word_embeddings
checkpoint.logical_aliases
checkpoint.tensors
```

No file-existence heuristic may select the mode.

---

# 11. Tied LM-head authority

When:

```text
tie_word_embeddings = true
```

R6-R10 requires one logical alias:

```text
logical_role      = lm_head
source_tensor_key = model.embed_tokens.weight
reason            = tie_word_embeddings=true
```

The physical projection source is therefore:

```text
model.embed_tokens.weight
shape = [V,H]
```

R6-R10 does not require a physical `lm_head.weight` tensor in this mode.

The tied path does **not** reuse the tiny R6-R6 input-token micro-atlas as an LM-head weight source because that atlas contains only selected token rows, not the full vocab projection domain.

---

# 12. Untied LM-head authority

When:

```text
tie_word_embeddings = false
```

R6-R10 requires one physical tensor:

```text
key   = lm_head.weight
role  = lm_head
shape = [V,H]
```

No tied alias may override the physical tensor.

The physical tensor identity digest becomes the LM-head projection source identity.

---

# 13. Unified logical LM-head source receipt

Recommended:

```rust
pub struct R6R10LmHeadSourceAuthority {
    pub schema_version: u32,
    pub checkpoint_set_digest: String,
    pub mode: R6R10LmHeadSourceMode,
    pub tie_word_embeddings: bool,
    pub logical_role: String,
    pub physical_tensor_key: String,
    pub physical_tensor_identity_digest: String,
    pub dtype: String,
    pub shape_vh: [u64; 2],
    pub vocab_size: u32,
    pub hidden_size: u32,
    pub logical_alias_reason: Option<String>,
    pub authority_digest: String,
}
```

Required:

```text
shape_vh = [checkpoint.config.vocab_size, checkpoint.config.hidden_size]
```

---

# 14. No full `AshModel` construction

R6-R10 must not call `AshModel::new(...)` as a way to reach `final_norm` or `lm_head`.

That constructor creates full random token embedding, full random LM head, and all decoder layers, which violates the current residency model.

Required:

```text
full AshModel construction count = 0
random output-head parameter creation count = 0
all-layer decoder construction count = 0
```

Only the exact final norm and one LM-head vocab wave may be materialized.

---

# 15. Output-head state domains

R6-R10 introduces three explicit state domains distinct from decoder residency.

```text
FinalNormWeightAuthoritySlot
LmHeadWaveResidencySlot
LogitSurfaceAuthoritySlot
```

These domains must not masquerade as `BaseTrainLayerWeightResidencySlot` entries.

Decoder weight authority and output-head weight authority are different semantic domains.

---

# 16. Final norm weight authority slot

Recommended model-core state:

```rust
pub enum FinalNormWeightAuthorityState {
    Vacant,
    Resident,
}

pub struct FinalNormWeightAuthorityPointer {
    pub schema_version: u32,
    pub checkpoint_set_digest: String,
    pub tensor_key: String,
    pub tensor_identity_digest: String,
    pub hidden_size: u32,
    pub norm_eps_bits: u64,
    pub generation: u64,
    pub pointer_digest: String,
}
```

The slot owns exactly one `AshRmsNorm<InferenceBackend>` when resident.

R6-R10 generation begins at one for the first final-norm materialization in the session.

---

# 17. Final norm weight decode

The final norm tensor is small and may use the existing full-tensor decoder:

```rust
decode_checkpoint_tensor_f32(...)
```

Required counts:

```text
final norm checkpoint read count = 1
final norm decode count = 1
final norm source owner acquire/release = 1/1
final norm decoded owner acquire/release = 1/1
final norm material commit count = 1
final norm payload readback count = 0
```

The decoded vector length must equal `H` exactly.

---

# 18. Final norm materialization

R6-R10 may reuse the current checkpoint RMSNorm materialization logic, preferably through a generic name extracted from the current C5-specific helper.

Canonical semantics:

```text
weight tensor [H]
+ checkpoint config rms_norm_eps
+ same Burn WGPU device
→ AshRmsNorm<InferenceBackend>
```

If a generic helper is extracted, the existing C5 function remains a wrapper for backward source compatibility.

No duplicate RMSNorm formula implementation is required.

---

# 19. Exact `rms_norm_eps` authority

Final RMSNorm epsilon comes from:

```text
checkpoint.config.rms_norm_eps_bits
```

The materialized `AshRmsNorm.eps` must match exactly.

No CLI epsilon override is allowed.

No layer-norm epsilon inference is allowed.

---

# 20. Final RMSNorm execution

R6-R10 executes exactly one final norm forward:

```text
input  = live final Hidden-L tensor [B,Q,H]
weight = model.norm.weight [H]
output = final normalized hidden [B,Q,H]
```

Required:

```text
final RMSNorm forward count = 1
input shape exact = [B,Q,H]
output shape exact = [B,Q,H]
input pointer exact = C10 final hidden pointer
hidden recompute count = 0
hidden slot mutation count = 0
```

---

# 21. Final norm activation identity

The normalized hidden receives an output-head activation identity separate from the hidden slot.

Recommended:

```rust
pub struct R6R10FinalNormActivationEvidence {
    pub schema_version: u32,
    pub source_hidden_pointer_digest: String,
    pub source_hidden_buffer_identity_digest: String,
    pub source_hidden_completion_token_digest: String,
    pub final_norm_weight_pointer_digest: String,
    pub shape_bqh: [u32; 3],
    pub runtime_scalar_count: u64,
    pub dispatch_count: u32,
    pub non_finite_count: u32,
    pub tensor_payload_readback_count: u32,
    pub compact_diagnostic_readback_count: u32,
    pub activation_identity_digest: String,
    pub pass: bool,
}
```

The activation identity must not depend on a second raw-bridge seam identity.

---

# 22. Final norm finite verification

R6-R10 requires same-device finite verification over all `B*Q*H` final-norm output scalars.

A compact reduction receipt may be read back.

Required:

```text
compared/visited scalar count = checked(B*Q*H)
non_finite_count = 0
tensor payload readback count = 0
```

Compact diagnostic readback is not tensor payload readback.

---

# 23. Hidden lease release ordering

The final hidden lease must remain valid through final RMSNorm dispatch submission and completion binding.

Then:

```text
validate lease before use
execute final norm
bind activation evidence
release hidden lease
```

LM-head waves consume the final-norm activation, not the hidden lease directly.

Required after release:

```text
LayerHiddenAuthoritySlot active execution lease count = 0
```

---

# 24. No hidden recompute

After final RMSNorm activation exists, R6-R10 must not reacquire Hidden-L to recompute final norm for each LM-head wave.

Required:

```text
final hidden execution lease acquisition count = 1
final RMSNorm execution count = 1
LM-head wave count may be >1
final norm recompute per wave = 0
```

The same final-norm activation is reused for every vocab wave.

---

# 25. LM-head cannot be fully materialized

The physical LM-head source shape is `[V,H]` and may be large.

R6-R10 explicitly forbids:

```text
full LM-head source payload Vec<u8>
full LM-head decoded Vec<f32>
full LM-head AshLinear
full LM-head GPU storage buffer
full tied embedding GPU reupload for output projection
mega vocab atlas
```

Required:

```text
full_lm_head_host_materialization_count = 0
full_lm_head_gpu_materialization_count = 0
full_embedding_reupload_count = 0
mega_vocab_atlas_create_count = 0
```

---

# 26. Vocab-row streaming planner

R6-R10 introduces a planner for contiguous row ranges of the physical `[V,H]` LM-head source tensor.

Recommended:

```rust
pub struct R6R10LmHeadVocabWavePlan {
    pub schema_version: u32,
    pub checkpoint_set_digest: String,
    pub lm_head_source_authority_digest: String,
    pub vocab_size: u32,
    pub hidden_size: u32,
    pub batch_size: u32,
    pub seq_len: u32,
    pub source_dtype: String,
    pub source_bytes_per_row: u64,
    pub decoded_bytes_per_row: u64,
    pub inherited_host_transient_budget_bytes: u64,
    pub device_max_buffer_size: u64,
    pub device_max_storage_binding_size: u64,
    pub rows_per_wave: u32,
    pub wave_count: u32,
    pub full_logits_scalar_count: u64,
    pub full_logits_bytes: u64,
    pub waves: Vec<R6R10LmHeadVocabWavePlanEntry>,
    pub plan_digest: String,
}
```

---

# 27. Host transient budget SSOT

R6-R10 does not invent a second hidden host-transient budget.

It inherits the already admitted C4/C10 host-transient ceiling from the same CLI policy currently used by decoder weight waves.

The output-head planner may use that byte ceiling as a shared process-local checkpoint decode budget.

If the project later introduces a global memory-budget authority, both C4 and R6-R10 should bind that authority rather than duplicate constants.

---

# 28. Rows-per-wave derivation

Rows per wave are derived, not hard-coded to a model-specific number.

At minimum the planner checks capacities for:

```text
source checkpoint row-range bytes
host decoded F32 row-range bytes
LM-head wave weight GPU buffer
candidate compact logits wave buffer
reference compact logits wave buffer
full canonical logits storage buffer
```

Derived capacity must satisfy:

```text
rows_per_wave > 0
rows_per_wave <= V
```

No silent fallback to full LM-head upload is allowed when one capacity is zero.

---

# 29. Full logits buffer admission

R6-R10 uses one canonical full logits surface in this patch.

Runtime dimensions:

```text
B = final hidden batch
Q = final hidden sequence length
V = checkpoint vocab_size
```

Checked:

```text
BQV = B * Q * V
logits_bytes = BQV * sizeof(f32)
```

Require the full logits buffer to fit all WGPU limits required by the publication/future-consumer binding.

If it does not fit, R6-R10 fails explicitly.

It must not silently switch to paged logits because paged canonical logits would be a separate state contract.

---

# 30. Runtime-derived BQV coverage

No fixed vocab-size or scalar-count literal is an authority.

Required:

```text
expected_logits_scalar_count = checked(B * Q * V)
```

The current fixture may observe a concrete number, but the PASS condition always uses the runtime-derived count.

No fixed `48259` or other historical vocab width may appear in R6-R10 control flow.

---

# 31. Vocab wave plan entry

Recommended:

```rust
pub struct R6R10LmHeadVocabWavePlanEntry {
    pub wave_ordinal: u32,
    pub vocab_row_start: u32,
    pub vocab_row_count: u32,
    pub vocab_row_end_exclusive: u32,
    pub source_file_start: u64,
    pub source_file_end: u64,
    pub source_payload_bytes: u64,
    pub decoded_f32_bytes: u64,
    pub candidate_logit_scalar_count: u64,
    pub candidate_logit_bytes: u64,
    pub plan_entry_digest: String,
}
```

Plan entries are contiguous, non-overlapping, and cover exactly `[0,V)`.

---

# 32. Row-range checkpoint decode primitive

The existing full-tensor `decode_checkpoint_tensor_f32(...)` is not acceptable for LM-head streaming because it reads the whole `[V,H]` payload.

R6-R10 introduces one generic range decoder in the R6 checkpoint-decode layer.

Recommended:

```rust
pub fn decode_checkpoint_tensor_row_range_f32(
    authority: &BaseTrainAtlasWave02R5CheckpointTensorSetAuthority,
    tensor: &BaseTrainAtlasWave02R5R6TensorAuthority,
    row_start: u32,
    row_count: u32,
    expected_row_width: u32,
    ownership: Option<&CheckpointTensorDecodeOwnershipLedger>,
) -> Result<DecodedCheckpointTensorRowRangeF32>;
```

This is a generic checkpoint primitive, not an LM-head-only file reader.

---

# 33. Row-range decode contract

The range decoder requires a rank-2 contiguous tensor:

```text
shape = [rows, columns]
columns = expected_row_width
```

Checked source byte math:

```text
source_element_width = dtype width
source_row_bytes = columns * source_element_width
row_byte_offset = row_start * source_row_bytes
range_byte_len = row_count * source_row_bytes
absolute_start = tensor.absolute_file_start + row_byte_offset
absolute_end   = absolute_start + range_byte_len
absolute_end <= tensor.absolute_file_end
```

All arithmetic is checked.

---

# 34. Row-range decode output

Recommended:

```rust
pub struct DecodedCheckpointTensorRowRangeF32 {
    pub tensor_key: String,
    pub tensor_identity_digest: String,
    pub row_start: u32,
    pub row_count: u32,
    pub row_width: u32,
    pub source_file_start: u64,
    pub source_file_end: u64,
    pub source_payload_bytes: u64,
    pub decoded_f32_bytes: u64,
    pub values: Vec<f32>,
    pub source_owner_release_count: u32,
    pub decode_count: u32,
    pub decode_receipt_digest: String,
}
```

Required decoded element count:

```text
row_count * H
```

---

# 35. LM-head source ownership

Every vocab wave uses `CheckpointTensorDecodeOwnershipLedger`.

Required per wave:

```text
source owner acquire count = 1
source owner release count = 1
decoded owner acquire count = 1
decoded owner release count = 1
current source owned bytes after materialization = 0
current decoded owned bytes after materialization = 0
current host transient bytes before fence = 0
```

The long-run peak must remain under the inherited host-transient budget.

---

# 36. LM-head wave residency slot

Recommended state:

```rust
pub enum LmHeadWaveResidencyState {
    Vacant,
    Resident,
}

pub struct LmHeadWaveResidencyPointer {
    pub schema_version: u32,
    pub lm_head_source_authority_digest: String,
    pub wave_ordinal: u32,
    pub vocab_row_start: u32,
    pub vocab_row_count: u32,
    pub tensor_identity_digest: String,
    pub generation: u64,
    pub material_identity_digest: String,
    pub pointer_digest: String,
}
```

The resident material is one `AshLinear<InferenceBackend>` with:

```text
out_dim = vocab_row_count
in_dim  = H
bias     = None
```

---

# 37. LM-head wave materialization

For each wave:

```text
read exact row range
→ decode F16/BF16/F32 to F32
→ materialize one AshLinear [R,H]
→ release host source/decode ownership
→ mark one wave resident
```

Required:

```text
material commit count = 1 per wave
full lm-head material commit count = 0
resident LM-head wave count <= 1
resident LM-head row count <= rows_per_wave
```

---

# 38. Wave generation monotonicity

LM-head wave residency generation is independent from vocab row number.

For sequential waves:

```text
wave generation: G -> G+1
wave ordinal:    n -> n+1
```

R6-R10 must not use `generation == wave_ordinal` as the primary authority.

The first generation may numerically begin at one, but lineage is checked from the previous pointer.

---

# 39. Candidate LM-head projection

The canonical numerical candidate for each vocab wave is the existing `AshLinear<InferenceBackend>` operator.

Input:

```text
final normalized hidden [B,Q,H]
```

Weight:

```text
wave rows [R,H]
```

Output:

```text
candidate logits wave [B,Q,R]
```

Required:

```text
candidate projection count = 1 per wave
candidate bias = absent
candidate output scalar count = B*Q*R
```

---

# 40. Independent same-device reference

R6-R10 adds a raw-WGPU reference projection for the same wave.

The reference reads:

```text
raw borrowed final-norm activation
raw borrowed current AshLinear wave weight
```

and writes a private compact reference buffer `[B,Q,R]`.

The reference is non-authoritative and never publishes logits.

Required:

```text
same WGPU device = true
same WGPU queue lineage = true
second device create count = 0
reference runtime authority = 0
```

---

# 41. Why the reference is per wave

A full independent `[B,Q,V]` reference would defeat the streaming residency goal.

Therefore parity is performed per vocab wave:

```text
candidate [B,Q,R]
vs
reference [B,Q,R]
```

Only a passing candidate wave may be copied into the private full logits candidate surface.

---

# 42. Candidate/reference raw bridge

R6-R10 reuses the existing Burn-to-raw WGPU bridge.

The final-norm activation may be bridged once and reused for all waves.

Each candidate wave output and wave weight may be bridged for parity/reference.

Bridge-local seam identities are observational only.

Persistent R6-R10 activation/logit identities must not be regenerated from later seam IDs, following the C8-D1 identity lesson.

---

# 43. Per-wave parity comparator

R6-R10 may reuse `HeadwiseOutputParityPipeline` because it already supports compact GPU-side tensor comparison with only compact diagnostics read back.

Recommended mode:

```text
compare_mixed_envelope
```

because independent matmul implementations may legally differ in floating accumulation order.

Required:

```text
compared scalar count = checked(B*Q*R)
nonfinite count = 0
envelope violation count = 0
tensor payload readback count = 0
```

---

# 44. Logit parity tolerance authority

R6-R10 introduces explicit fixed CLI tolerances for LM-head cross-implementation parity.

Recommended keys:

```text
--r6-r10-logit-absolute-tolerance
--r6-r10-logit-relative-tolerance
--r6-r10-logit-relative-floor
```

They must be finite, non-negative, and sealed into the pass receipt.

No runtime tolerance widening is allowed after observing a failure.

No per-wave adaptive tolerance is allowed.

---

# 45. Private full logits candidate surface

R6-R10 allocates one raw WGPU F32 buffer large enough for `[B,Q,V]`.

During streaming it is **private candidate state**, not canonical output authority.

Recommended state:

```text
LogitSurfaceAuthoritySlot = Vacant
private_candidate_logits_buffer = allocated
```

Partial wave publication writes only into this private candidate buffer.

A failed later wave cannot leave a partially written canonical logits surface.

---

# 46. Wave publication kernel

After one wave passes parity, a small raw-WGPU publication kernel copies/scatters the compact candidate `[B,Q,R]` into the correct vocab slice of private `[B,Q,V]`.

Mapping:

```text
candidate[b,q,r]
→ private_logits[b,q,vocab_row_start+r]
```

Required:

```text
one publication dispatch per passing wave
no writes outside assigned vocab span
no overlap with previous wave spans
```

---

# 47. Publication coverage ledger

Recommended:

```rust
pub struct R6R10LogitWavePublicationReceipt {
    pub wave_ordinal: u32,
    pub vocab_row_start: u32,
    pub vocab_row_count: u32,
    pub candidate_scalar_count: u64,
    pub parity_receipt_digest: String,
    pub publication_scalar_count: u64,
    pub publication_dispatch_count: u32,
    pub coverage_start_scalar: u64,
    pub coverage_end_scalar_exclusive: u64,
    pub overlap_count: u32,
    pub pass: bool,
    pub receipt_digest: String,
}
```

Coverage is derived from the actual wave row span and BQ geometry.

---

# 48. Global BQV coverage seal

After the last vocab wave:

```text
sum(publication scalar counts) = B*Q*V
first vocab row = 0
last vocab row end = V
all row spans contiguous
coverage gap count = 0
coverage overlap count = 0
wave count = planner wave count
```

Required:

```text
published_scalar_count = runtime_expected_BQV
```

No payload readback is required to prove the combinatorial coverage relation.

---

# 49. Final full-surface finite audit

Before canonical adoption, R6-R10 performs one GPU-side finite scan of the private `[B,Q,V]` candidate surface.

Required:

```text
visited scalar count = BQV
nonfinite count = 0
tensor payload readback count = 0
compact diagnostic readback count = 1 or the exact bounded implementation count
```

The finite scan does not make the buffer canonical by itself.

---

# 50. Sequential wave fence

After each wave has completed:

```text
candidate projection
reference projection
parity comparison
private publication
```

R6-R10 waits on same-device completion before evicting/replacing the LM-head wave residency.

Required:

```text
wave fence wait count = planner wave count
concurrent LM-head wave residency count = 1
wave overlap count = 0
```

No next-wave checkpoint decode is admitted before the previous wave's GPU weight residency can be safely retired under the declared strict sequential contract.

---

# 51. LM-head wave eviction

At each successful fence:

```text
current wave material owner released
LmHeadWaveResidencySlot -> Vacant
next row range may be decoded
```

Required:

```text
stale LM-head wave lease count = 0
source/target LM-head wave residency overlap = 0
```

No destructive RecoveryRequired state is needed because a failed output-head wave does not destroy the decoder or hidden SSOT.

---

# 52. Output-head failure ownership

R6-R10 is fail-closed but non-destructive to parent decoder/hidden state.

On any failure before final logits adoption:

```text
C10 parent runtime stays intact
final decoder weight pointer stays intact
final hidden pointer stays intact
LogitSurfaceAuthoritySlot remains Vacant
private partial logits candidate is discarded
no forward loss runs
```

No fallback to a full LM-head upload is allowed.

---

# 53. Final norm failure boundary

If final norm checkpoint resolution/decode/materialization/execution fails:

```text
Hidden-L remains canonical
final decoder weight remains canonical
logits slot remains Vacant
LM-head checkpoint read count = 0
```

No hidden mutation or recompute fallback.

---

# 54. LM-head source resolution failure

If tied/untied authority is ambiguous or inconsistent:

```text
logits slot remains Vacant
projection does not start
```

Examples of hard failure:

```text
tie_word_embeddings=true but lm_head alias missing
tied alias points to unexpected key
tie_word_embeddings=false but physical lm_head missing
source shape != [V,H]
source canonical role invalid
```

No silent alias repair.

---

# 55. Wave decode/materialization failure

If one vocab wave fails before GPU publication:

```text
current private full logits candidate may contain earlier private waves
canonical logits slot remains Vacant
current wave slot is released/aborted
future waves do not run
```

Earlier private writes do not become user-visible/canonical output.

---

# 56. Wave parity failure

If candidate/reference parity fails:

```text
failed wave publication count = 0
current wave is not copied into private full logits
later waves do not execute
canonical logits adoption count = 0
```

No tolerance widening, reference bypass, or candidate-only fallback.

---

# 57. Private publication failure

If the raw publication kernel fails after parity:

```text
canonical logits slot remains Vacant
private candidate buffer is discarded
later waves do not run
```

No attempt is made to reconstruct the missing slice on CPU.

---

# 58. Canonical logit surface authority

Only after all waves and global finite/coverage checks pass may R6-R10 adopt the private full buffer into a runtime authority slot.

Recommended pointer:

```rust
pub struct LogitSurfaceAuthorityPointer {
    pub schema_version: u32,
    pub checkpoint_set_digest: String,
    pub source_final_hidden_pointer_digest: String,
    pub final_norm_activation_identity_digest: String,
    pub lm_head_source_authority_digest: String,
    pub shape_bqv: [u32; 3],
    pub scalar_count: u64,
    pub buffer_identity_digest: String,
    pub completion_token_digest: String,
    pub publication_generation: u64,
    pub writer_id: String,
    pub operation_id: String,
    pub pointer_digest: String,
}
```

---

# 59. Logit surface slot

Recommended:

```rust
pub enum LogitSurfaceAuthorityState {
    Vacant,
    Resident,
}
```

The slot owns exactly one raw WGPU logits buffer after adoption.

Future R6-R11 forward-loss work consumes the buffer through an exact execution lease.

R6-R10 adoption generation begins at one in this session.

---

# 60. Persistent logits buffer identity

The canonical logits `buffer_identity_digest` is sealed from stable semantic/publication facts such as:

```text
checkpoint set digest
source final hidden pointer digest
final norm activation identity
LM-head source authority digest
BQV shape
writer id
publication generation
operation id
```

It must not be redefined by later raw-bridge seam IDs.

This follows the identity classification discipline established by C8-D1/C10-D1.

---

# 61. Single canonical logits writer

Required:

```text
private wave publication writer count >= 1
canonical LogitSurfaceAuthoritySlot adoption count = 1
parallel canonical logits authority count = 0
```

No Burn full-logits tensor and raw canonical logits buffer may coexist as equal authorities.

The raw adopted buffer is the sole canonical logits surface in R6-R10.

---

# 62. Logit completion token

The completion token is sealed only after:

```text
all vocab waves passed
all wave fences completed
all per-wave parity passed
BQV coverage exact
full-surface finite scan passed
```

It binds ordered wave publication receipt digests.

No partially completed wave set may mint a completion token.

---

# 63. Logit authority postcondition

After successful adoption:

```text
LogitSurfaceAuthoritySlot state = Resident
shape = [B,Q,V]
scalar count = BQV
active consumer lease count = 0
canonical publication count = 1
```

The final decoder weight and final hidden remain unchanged.

---

# 64. Final norm weight lifetime

R6-R10 may keep the small final norm weight resident in `FinalNormWeightAuthoritySlot` after logits publication.

That slot is separate from decoder weight authority.

Keeping it resident is preferred for future backward/final-norm gradient work and costs only `H` values.

R6-R10 does not claim LM-head full-weight residency after completion.

---

# 65. LM-head final residency

After the final vocab wave and fence:

```text
LmHeadWaveResidencySlot = Vacant
resident LM-head rows = 0
full LM-head resident = 0
```

The canonical output is the logits surface, not a persistent full LM-head weight.

---

# 66. Tied embedding path does not mutate embedding authority

When the LM head is tied to `model.embed_tokens.weight`, R6-R10 performs read-only checkpoint row-range streaming.

Required:

```text
embedding checkpoint mutation count = 0
R6-R6 embedding micro-atlas mutation count = 0
embedding micro-atlas rebind count = 0
```

The existing embedding execution evidence remains historical parent evidence only.

---

# 67. Output-head checkpoint mutation seal

Across final norm and LM-head streaming:

```text
checkpoint mutation count = 0
weight writeback count = 0
optimizer mutation count = 0
```

The checkpoint remains read-only.

---

# 68. Zero payload readback definition

R6-R10 defines tensor payload readback as mapping/copying a tensor's numerical payload to CPU for validation or downstream computation.

Required:

```text
final hidden tensor payload readback = 0
final norm activation payload readback = 0
final norm weight GPU payload readback = 0
LM-head weight wave GPU payload readback = 0
candidate logits wave payload readback = 0
reference logits wave payload readback = 0
full logits payload readback = 0
```

Compact parity/finite counters may be read back.

---

# 69. Compact diagnostic readback

Allowed compact diagnostics include:

```text
per-wave parity compared count
per-wave parity nonfinite count
per-wave envelope violation count
per-wave max absolute/relative error
full-surface finite count
first-fault index when implemented
```

They are receipts, not tensor payloads.

All compact diagnostic counts must be explicitly reported separately from payload readback.

---

# 70. No CPU logits authority

R6-R10 must not create a full CPU `Vec<f32>` of BQV logits.

Required:

```text
CPU full logits materialization count = 0
CPU full logits authority count = 0
```

Future loss remains a same-device consumer of the GPU logit surface.

---

# 71. No sampling or decode

Although logits become available, R6-R10 is a BaseTrain forward boundary, not a generation patch.

Forbidden:

```text
top-k
top-p
argmax decode
token sampling
generation state mutation
KV-cache decode mutation
production inference output commit
```

Production inference remains blocked.

---

# 72. Forward loss remains blocked

R6-R10 terminates immediately after canonical logits publication.

Required counters:

```text
forward_loss_count = 0
cross_entropy_count = 0
label_shift_count = 0
backward_count = 0
optimizer_count = 0
weight_mutation_count = 0
```

No labels are consumed in R6-R10.

---

# 73. Output-head numerical parity evidence

Recommended per-wave evidence:

```rust
pub struct R6R10LmHeadWaveParityEvidence {
    pub schema_version: u32,
    pub wave_ordinal: u32,
    pub vocab_row_start: u32,
    pub vocab_row_count: u32,
    pub candidate_projection_count: u32,
    pub reference_projection_count: u32,
    pub compared_scalar_count: u64,
    pub expected_scalar_count: u64,
    pub non_finite_count: u32,
    pub envelope_violation_count: u32,
    pub max_absolute_error_bits: u32,
    pub max_relative_error_bits: u32,
    pub absolute_tolerance_bits: u32,
    pub relative_tolerance_bits: u32,
    pub relative_floor_bits: u32,
    pub compact_readback_count: u32,
    pub tensor_payload_readback_count: u32,
    pub pass: bool,
    pub evidence_digest: String,
}
```

---

# 74. LM-head wave execution receipt

Recommended:

```rust
pub struct R6R10LmHeadWaveExecutionReceipt {
    pub schema_version: u32,
    pub wave_ordinal: u32,
    pub plan_entry_digest: String,
    pub source_tensor_identity_digest: String,
    pub source_mode: R6R10LmHeadSourceMode,
    pub vocab_row_start: u32,
    pub vocab_row_count: u32,
    pub source_payload_bytes: u64,
    pub decoded_f32_bytes: u64,
    pub source_read_count: u32,
    pub decode_count: u32,
    pub material_commit_count: u32,
    pub source_owner_release_count: u32,
    pub decoded_owner_release_count: u32,
    pub candidate_projection_count: u32,
    pub reference_projection_count: u32,
    pub parity_evidence_digest: String,
    pub private_publication_receipt_digest: String,
    pub fence_wait_count: u32,
    pub payload_readback_count: u32,
    pub pass: bool,
    pub receipt_digest: String,
}
```

---

# 75. LM-head streaming aggregate

Recommended:

```rust
pub struct R6R10LmHeadStreamingReceipt {
    pub schema_version: u32,
    pub source_authority_digest: String,
    pub plan_digest: String,
    pub wave_count: u32,
    pub wave_execution_receipt_digests: Vec<String>,
    pub total_checkpoint_range_reads: u32,
    pub total_decodes: u32,
    pub total_material_commits: u32,
    pub total_source_owner_releases: u32,
    pub total_decoded_owner_releases: u32,
    pub total_candidate_projections: u32,
    pub total_reference_projections: u32,
    pub total_parity_comparisons: u32,
    pub total_private_publications: u32,
    pub total_wave_fence_waits: u32,
    pub observed_peak_host_transient_bytes: u64,
    pub full_lm_head_host_materialization_count: u32,
    pub full_lm_head_gpu_materialization_count: u32,
    pub mega_vocab_atlas_create_count: u32,
    pub payload_readback_count: u32,
    pub pass: bool,
    pub receipt_digest: String,
}
```

---

# 76. Streaming aggregate exact relations

Let:

```text
W = planner wave count
```

Required:

```text
range reads             = W
decodes                 = W
material commits        = W
source owner releases   = W
decoded owner releases  = W
candidate projections   = W
reference projections   = W
parity comparisons      = W
private publications    = W
wave fence waits        = W
```

No hidden extra wave is permitted.

---

# 77. Host peak health

The LM-head streaming ownership ledger records the observed peak source+decoded host bytes.

Required:

```text
observed peak > 0
observed peak <= inherited host transient budget
current source owned bytes at completion = 0
current decoded owned bytes at completion = 0
current host transient bytes at completion = 0
```

No full-tensor host peak is allowed.

---

# 78. Final output-head receipt

Recommended:

```rust
pub struct R6R10FinalOutputHeadReceipt {
    pub schema_version: u32,
    pub patch_id: String,
    pub build_revision: String,
    pub parent_c10_receipt_digest: String,
    pub parent_decoder_completion_health_digest: String,
    pub checkpoint_set_digest: String,

    pub final_hidden_pointer_before_digest: String,
    pub final_hidden_generation: u64,
    pub final_hidden_layer: u32,
    pub final_hidden_shape_bqh: [u32; 3],
    pub final_hidden_exact_bound: bool,

    pub final_decoder_weight_pointer_before_digest: String,
    pub final_decoder_weight_pointer_after_digest: String,
    pub decoder_weight_reload_count: u32,
    pub decoder_weight_rebind_count: u32,

    pub final_norm_weight_authority_digest: String,
    pub final_norm_activation_evidence_digest: String,
    pub final_norm_checkpoint_read_count: u32,
    pub final_norm_decode_count: u32,
    pub final_norm_material_commit_count: u32,
    pub final_norm_forward_count: u32,

    pub lm_head_source_authority_digest: String,
    pub lm_head_source_mode: R6R10LmHeadSourceMode,
    pub lm_head_streaming_receipt_digest: String,

    pub shape_bqv: [u32; 3],
    pub runtime_expected_bqv_scalar_count: u64,
    pub published_bqv_scalar_count: u64,
    pub coverage_gap_count: u32,
    pub coverage_overlap_count: u32,
    pub logit_non_finite_count: u32,

    pub logit_surface_pointer_digest: String,
    pub logit_surface_completion_token_digest: String,
    pub canonical_logit_publication_count: u32,

    pub hidden_recompute_count: u32,
    pub hidden_mutation_count: u32,
    pub tensor_payload_readback_count: u32,
    pub checkpoint_mutation_count: u32,
    pub forward_loss_count: u32,
    pub backward_count: u32,
    pub optimizer_count: u32,
    pub production_inference_count: u32,

    pub pass: bool,
    pub receipt_digest: String,
}
```

---

# 79. Final receipt invariants

Required:

```text
final hidden exact bound = true
final hidden recompute = 0
final hidden mutation = 0
final decoder weight reload = 0
final decoder weight rebind = 0
final decoder pointer unchanged = true
final norm read/decode/material/forward = 1/1/1/1
BQV expected = BQV published
coverage gap = 0
coverage overlap = 0
logit nonfinite = 0
canonical logit publication = 1
tensor payload readback = 0
checkpoint mutation = 0
forward loss = 0
backward = 0
optimizer = 0
production inference = 0
```

---

# 80. CLI contract

Recommended additions:

```text
--require-r6-r10-final-rmsnorm-lm-head-forward true
--require-r6-r10-c10-healthy-parent true
--require-r6-r10-c9-final-hidden-exact-consumption true
--require-r6-r10-final-decoder-completion-binding true
--require-r6-r10-final-norm-checkpoint-authority true
--require-r6-r10-final-norm-single-forward true
--require-r6-r10-lm-head-logical-source-authority true
--require-r6-r10-lm-head-streaming-materialization true
--require-r6-r10-runtime-derived-bqv true
--require-r6-r10-per-wave-reference-parity true
--require-r6-r10-private-before-canonical-logit-publication true
--require-r6-r10-full-logit-finite-scan true
--require-r6-r10-canonical-logit-single-adoption true
--require-r6-r10-zero-hidden-recompute true
--require-r6-r10-zero-hidden-mutation true
--require-r6-r10-zero-decoder-weight-reload true
--require-r6-r10-zero-payload-readback true
--require-r6-r10-zero-checkpoint-mutation true
--require-r6-r10-forward-loss-blocked true
--require-r6-r10-backward-blocked true
--require-r6-r10-optimizer-blocked true
--require-r6-r10-production-inference-blocked true

--r6-r10-logit-absolute-tolerance <finite f32>
--r6-r10-logit-relative-tolerance <finite f32>
--r6-r10-logit-relative-floor <finite positive f32>

--allow-r6-r10-full-lm-head-host-materialization false
--allow-r6-r10-full-lm-head-gpu-materialization false
--allow-r6-r10-mega-vocab-atlas false
--allow-r6-r10-logit-payload-readback false
--allow-r6-r10-cpu-logit-authority false
--allow-r6-r10-tolerance-widening false
--allow-r6-r10-full-model-construction false
--allow-r6-r10-hidden-recompute false
--allow-r6-r10-decoder-weight-reload false
--allow-r6-r10-sampling false
--allow-r6-r10-loss false
```

The inherited host-transient byte ceiling is reused from the already admitted wave policy rather than duplicated in a new R6-R10 budget key.

---

# 81. Existing CLI geometry reuse

R6-R10 reuses the physical parent/runtime geometry already established by the same session:

```text
batch size
sequence length
checkpoint hidden size
checkpoint vocab size
same WGPU device/queue epochs
checkpoint identity
model instance identity
training session identity
```

No second geometry authority is parsed from ad-hoc literals.

---

# 82. Static forbidden call inventory

The R6-R10 canonical module must have zero direct calls to:

```text
run_r6_r9_c9_progressive_n_layer_wave_advancement_session  // C10 parent already owns C9
advance_resident_decoder_to_checkpoint_end
rebind_resident_decoder_layer
rebind_resident_decoder_layer_legacy_full_loader_reference
execute_layer_weight_build_staging_private_candidate
plan_decoder_weight_atlas_waves
load_base_train_atlas_wave_02_r6_r7_decoder_block_weights
AshModel::new
```

The physical wrapper calls one C10 parent session only.

---

# 83. Required new implementation surface

Recommended semantic files:

```text
crates/base_train/src/
  base_train_atlas_wave_02_r6_checkpoint_tensor_decode.rs

crates/model_core/src/
  base_train_output_head_authority.rs
  actual_decoder_block_split_forward.rs   // generic materialization helper extraction only if needed

crates/burn_webgpu_backend/src/
  base_train_lm_head_wave_reference.rs
  base_train_logit_wave_publish.rs
  base_train_logit_finite_audit.rs

crates/burn_webgpu_backend/src/shaders/
  base_train_lm_head_wave_reference.wgsl
  base_train_logit_wave_publish.wgsl
  base_train_logit_finite_audit.wgsl

crates/orchestrator_local/src/
  base_train_atlas_wave_02_r6_r10_final_rmsnorm_lm_head_forward.rs

crates/orchestrator_local/src/bin/
  ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate.rs

specs/cli/
  ash_basetrain_atlas_wave_02_r6_r9.args
```

Exact file splitting may be reduced if repository conventions favor fewer files, but authority boundaries must remain explicit.

---

# 84. WGSL ownership

New WGSL is allowed only for:

```text
independent LM-head wave reference projection
private logit wave publication
full logit finite audit
```

The canonical candidate LM-head numerical projection remains `AshLinear`.

Final RMSNorm remains the existing `AshRmsNorm` implementation.

No duplicate decoder shader path is introduced.

---

# 85. Static closure checklist

Before physical run require:

```text
C10-D1 parent session called exactly once
C10 parent health exact binding present
C9 final hidden exact pointer/buffer/completion binding present
final hidden live lease acquired exactly once
final hidden commit count = 0
final norm source key exact model.norm.weight
final norm shape exact [H]
final norm epsilon from checkpoint config
final norm full decode count planned = 1
final norm materialization uses same Burn device
final norm forward count planned = 1
LM-head tied/untied resolver uses config + logical alias authority
no LM-head source filename heuristic
no fixed vocab size in control flow
no full LM-head host decode
no full LM-head GPU materialization
row-range decoder present
row-range source bounds checked
rows-per-wave plan derived from runtime limits/budget
plan covers [0,V) exactly
candidate projection = AshLinear wave
reference projection = raw same-device WGSL
per-wave parity = GPU compact diagnostics
no tolerance widening
private full logits allocated once
canonical logit slot remains vacant during waves
publication spans disjoint and contiguous
BQV checked runtime derivation present
full finite scan before adoption
canonical logit adoption count = 1
LM-head wave residency <= 1
wave fence count = plan wave count
final LM-head wave slot vacant
final decoder weight pointer unchanged
final hidden pointer unchanged
payload readback = 0
checkpoint mutation = 0
loss/backward/optimizer/sampling = 0
```

---

# 86. Physical expected terminal line

Recommended:

```text
[r6-r10-final-rmsnorm-lm-head-forward]
checkpoint_layers=<L>
final_decoder_layer=<L-1>
final_hidden_layer=<L>
final_hidden_generation=<HG>
final_hidden_exact_bound=1
final_hidden_lease_acquire=1
final_hidden_recompute=0
final_hidden_mutation=0
final_decoder_weight_reload=0
final_decoder_weight_rebind=0
final_decoder_pointer_unchanged=1
final_norm_tensor_key=model.norm.weight
final_norm_read=1
final_norm_decode=1
final_norm_material_commit=1
final_norm_forward=1
final_norm_nonfinite=0
lm_head_source_mode=<tied_embedding_alias|untied_physical_lm_head>
lm_head_source_key=<model.embed_tokens.weight|lm_head.weight>
vocab_size=<V>
hidden_size=<H>
batch=<B>
seq=<Q>
rows_per_wave=<R>
lm_head_waves=<W>
lm_head_range_reads=<W>
lm_head_decodes=<W>
lm_head_material_commits=<W>
lm_head_candidate_projections=<W>
lm_head_reference_projections=<W>
lm_head_parity_comparisons=<W>
lm_head_wave_publications=<W>
lm_head_wave_fence_waits=<W>
full_lm_head_host_materialization=0
full_lm_head_gpu_materialization=0
mega_vocab_atlas=0
runtime_bqv=<B*Q*V>
published_bqv=<B*Q*V>
coverage_gap=0
coverage_overlap=0
logit_nonfinite=0
canonical_logit_publication=1
payload_readback=0
checkpoint_mutation=0
forward_loss=0
backward=0
optimizer=0
production_inference=0
final_norm_activation_digest=<sha256>
lm_head_source_authority_digest=<sha256>
lm_head_streaming_receipt_digest=<sha256>
logit_surface_pointer_digest=<sha256>
logit_completion_token_digest=<sha256>
receipt_digest=<sha256>
proof_ledger=HOLD
```

---

# 87. PASS token

```text
PASS_ASH_BASETRAIN_ATLAS_WAVE_02_R6_R10_FINAL_RMSNORM_LM_HEAD_FORWARD_C10_D1_PHYSICAL_HEALTHY_PARENT_C9_FINAL_DECODER_COMPLETION_EXACT_LIVE_FINAL_HIDDEN_POINTER_BUFFER_COMPLETION_AND_BQH_BINDING_SINGLE_FINAL_HIDDEN_EXECUTION_LEASE_ZERO_HIDDEN_RECOMPUTE_ZERO_HIDDEN_MUTATION_MODEL_NORM_WEIGHT_CHECKPOINT_AUTHORITY_EXACT_SHAPE_AND_RMS_EPS_BINDING_SINGLE_CHECKPOINT_READ_SINGLE_DECODE_SINGLE_MATERIAL_COMMIT_SINGLE_ACTUAL_FINAL_RMSNORM_FORWARD_FULL_BQH_FINITE_COVERAGE_LM_HEAD_LOGICAL_AUTHORITY_RESOLVED_FROM_TIE_WORD_EMBEDDINGS_AND_CHECKPOINT_ALIAS_TIED_EMBEDDING_OR_UNTIED_PHYSICAL_WEIGHT_EXACT_VH_SOURCE_NO_FILENAME_HEURISTIC_NO_FULL_LM_HEAD_HOST_MATERIALIZATION_NO_FULL_LM_HEAD_GPU_MATERIALIZATION_CONTIGUOUS_VOCAB_ROW_RANGE_STREAMING_RUNTIME_BUDGET_AND_DEVICE_LIMIT_DERIVED_WAVE_PLAN_SINGLE_LM_HEAD_WAVE_RESIDENCY_ASH_LINEAR_CANDIDATE_RAW_WGPU_SAME_DEVICE_REFERENCE_PER_WAVE_GPU_MIXED_ENVELOPE_PARITY_ZERO_NONFINITE_ZERO_ENVELOPE_VIOLATION_ZERO_TENSOR_PAYLOAD_READBACK_PARITY_GATED_PRIVATE_LOGIT_WAVE_PUBLICATION_ONE_PRIVATE_FULL_BQV_CANDIDATE_SURFACE_DISJOINT_CONTIGUOUS_VOCAB_COVERAGE_RUNTIME_DERIVED_BQV_EXACT_ZERO_COVERAGE_GAP_ZERO_COVERAGE_OVERLAP_FULL_LOGIT_FINITE_SCAN_SINGLE_CANONICAL_LOGIT_SURFACE_ADOPTION_PERSISTENT_SEMANTIC_BUFFER_IDENTITY_ZERO_DECODER_WEIGHT_RELOAD_ZERO_DECODER_REBIND_FINAL_DECODER_POINTER_UNCHANGED_ZERO_CHECKPOINT_MUTATION_ZERO_FORWARD_LOSS_ZERO_BACKWARD_ZERO_OPTIMIZER_ZERO_SAMPLING_PRODUCTION_INFERENCE_BLOCKED_PROOF_LEDGER_HOLD_SEALED
```

---

# 88. Physical PASS meaning

R6-R10 physical PASS proves:

```text
the C10-healthy final decoder completion can be consumed directly without decoder replay
the exact live final Hidden-L is used once as final RMSNorm input
model.norm.weight is resolved from checkpoint authority and executed once
the final hidden slot is not mutated or advanced
LM-head logical weight source is resolved correctly for tied or untied checkpoints
the [V,H] projection weight is streamed by bounded row ranges rather than fully materialized
each vocab wave executes an actual AshLinear projection
each wave is checked against an independent same-device raw-WGPU reference before publication
all vocab spans cover exactly [0,V) without overlap/gap
one private full [B,Q,V] logits surface is completed and finite
one canonical logits authority is adopted only after all waves pass
the final decoder weight pointer is unchanged and never reloaded
no tensor payload is read back to CPU
checkpoint weights remain immutable
loss/backward/optimizer/sampling remain unexecuted
```

---

# 89. Physical PASS does not prove

R6-R10 PASS does **not** prove:

```text
cross-entropy/causal label shift correctness
loss scalar correctness
backward gradient correctness
LM-head gradient streaming correctness
final norm gradient correctness
decoder gradient correctness
optimizer update correctness
training convergence
sampling correctness
KV-cache decode correctness
production inference readiness
paged logits behavior when one full BQV buffer exceeds device limits
full long-run multi-step training memory stability
```

These remain later boundaries.

---

# 90. Admission after physical PASS

```text
R6-R6 actual Layer0 body                         = ADMITTED
R6-R7 historical decoder residency               = ADMITTED_HISTORY
R6-R8 resident decoder execution                 = ADMITTED
R6-R9-C4 decoder-weight wave planner             = ADMITTED
R6-R9-C5 decoder-weight wave staging             = ADMITTED
R6-R9-C6 runtime wave rebind canary              = ADMITTED
R6-R9-C7 wave execution parity                   = ADMITTED
R6-R9-C8 canonical decoder wave-loader authority = ADMITTED
R6-R9-C8-D1 hidden identity closure              = ADMITTED
R6-R9-C9 progressive decoder completion          = ADMITTED
R6-R9-C10 long-horizon residency health          = ADMITTED
R6-R9-C10-D1 role identity classification        = ADMITTED
R6-R10 final RMSNorm + streamed LM-head forward  = ADMITTED on physical PASS

Canonical decoder-weight transport               = DECODER_WEIGHT_ATLAS_WAVE
Canonical logits surface                         = AVAILABLE after R6-R10 PASS
Forward loss                                      = BLOCKED
Backward                                          = BLOCKED
Optimizer                                         = BLOCKED
Production inference                              = BLOCKED
Proof ledger                                      = HOLD
```

---

# 91. Natural next boundary

After R6-R10 physical PASS, the natural next training boundary is:

```text
ASH-BASETRAIN-ATLAS-WAVE-02-R6-R11

Causal Forward Loss /
Canonical Logit Surface Exact Lease /
Input Token Target Shift Authority /
Padding·Valid-Length Loss Mask /
Cross-Entropy Same-Device Reduction /
Runtime-Derived Valid Target Count /
Compact Loss Scalar Publication /
Zero Logit Payload Readback /
Zero Hidden Recompute /
Zero LM-Head Reprojection /
Backward Still Blocked Seal
```

R6-R11 must consume the canonical logit surface through an exact lease and must not rerun R6-R10 merely to obtain logits.

---

# 92. Architecture seal

> R6-R10 is the output-head handoff, not another decoder pass. It trusts only the C10-D1 HEALTHY parent, binds the exact live final hidden pointer and completion state that C9 produced, leases that hidden once, and executes checkpoint-authoritative `model.norm.weight` exactly once through the existing RMSNorm implementation. The LM head is then resolved as a logical checkpoint role: a tied checkpoint streams rows from `model.embed_tokens.weight`, while an untied checkpoint streams rows from physical `lm_head.weight`; neither path guesses from filenames or allocates the full `[V,H]` weight on host or GPU. Contiguous vocab-row ranges are decoded under the existing host-transient budget, materialized one wave at a time as `AshLinear`, compared against an independent raw-WGPU same-device reference, and only passing waves write into a private full `[B,Q,V]` candidate surface. The private surface is not canonical while partial. Once every planned vocab row has been written exactly once, runtime-derived `B*Q*V` coverage is exact, the full surface is finite, all wave fences are complete, and payload readback remains zero, one `LogitSurfaceAuthoritySlot` adoption publishes the sole canonical logits buffer. Throughout the operation the final decoder weight and final hidden SSOT remain unchanged, checkpoint weights remain read-only, the LM-head wave slot ends vacant, and loss/backward/optimizer/sampling/production inference remain explicitly blocked.
