# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R11

## Causal Forward Loss / Canonical Logit Surface Exact Lease / Runtime Input Sequence Authority / Causal Target Shift Authority / Row-Valid-Length Loss Selection / Same-Device Stable LogSumExp NLL / Independent GPU Reference Parity / Hierarchical Loss Reduction / Compact Loss Surface Publication / Zero Logit Payload Readback / Zero Hidden Recompute / Zero LM-Head Reprojection / Backward Still Blocked Seal

> Physical admission parent SSOT: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R10` physical PASS  
> Parent output state: canonical `LogitSurfaceAuthoritySlot` Resident  
> Parent physical geometry observed: `B=1`, `Q=32`, `V=48259`, `BQV=1544288`  
> Parent logit payload readback: `0`  
> Parent final hidden recompute: `0`  
> Parent decoder weight reload/rebind: `0/0`  
> Current R6 input fixture: token ids `1..32`, row valid length `32`  
> Current physically derivable causal target count: `31`, not `32`  
> Forward loss: `ADMITTED only after R6-R11 physical PASS`  
> Backward / optimizer / parameter mutation / production inference: `BLOCKED`  
> Proof ledger: `HOLD`

---

# 1. Purpose

R6-R10 physically produced and canonically published one complete GPU-resident logit surface `[B,Q,V]` without rereading the full LM-head weight, without recomputing the final hidden, and without reading the logit payload back to CPU.

R6-R11 is the first patch allowed to consume that canonical logit surface as a training result.

Its only numerical purpose is the causal next-token forward loss:

```text
canonical logits [B,Q,V]
        +
actual R6 input token sequence
        +
actual row valid lengths
        ↓
causal target pairs q -> q+1
        ↓
GPU stable logsumexp NLL per valid target
        ↓
GPU hierarchical sum / mean reduction
        ↓
one canonical forward-loss surface
```

R6-R11 does not rerun the decoder, final RMSNorm, or LM head.

---

# 2. Critical target-availability fact

The current R6 physical fixture contains:

```text
Q = 32
token_ids = [1,2,3,...,32]
row_valid_lengths = [32]
```

There is no separately supplied 33rd token.

Therefore R6-R11 must not fabricate a target for the final position `q=31`.

The physically available causal pairs are:

```text
q=0  -> target token_ids[1]
q=1  -> target token_ids[2]
...
q=30 -> target token_ids[31]
```

and:

```text
q=31 -> NO TARGET AVAILABLE
```

For the current fixture:

```text
valid_target_count = 31
```

Any R6-R11 implementation claiming 32 valid targets from the current input evidence is structurally invalid.

---

# 3. General causal target-count rule

For batch row `b` with valid input length `L_b`:

```text
valid causal target positions = q where q + 1 < L_b
```

Therefore:

```text
row_target_count = max(L_b - 1, 0)
```

and globally:

```text
N_valid = sum_b max(L_b - 1, 0)
```

All arithmetic uses checked operations.

R6-R11 requires:

```text
N_valid > 0
```

No target may cross a batch-row boundary.

---

# 4. Target identity rule

For every admitted pair `(b,q)`:

```text
target_token_id(b,q)
    = input_token_ids[b * Q + (q + 1)]
```

Required:

```text
target_token_id < V
```

The last valid token of each row is an input context token only for R6-R11 and contributes no forward-loss target unless an external next-token authority is admitted by a later patch.

---

# 5. R6-R11 must not reparse CLI as target SSOT

Today R6-R6 parses:

```text
--token-ids
--row-valid-lengths
```

and uses those values to construct the actual embedding input.

However the live session does not currently retain a typed copy of the exact sequence values that were used.

R6-R11 must not independently parse the args file again and assume those values equal the values used by R6-R6.

That would create a second input-sequence authority.

The actual R6-R6 input values must be retained at origin.

---

# 6. Runtime input-sequence authority

Introduce one immutable authority type, recommended in `model_core`:

```rust
pub struct BaseTrainRuntimeInputSequenceAuthority {
    pub schema_version: u32,
    pub batch_size: u32,
    pub seq_len: u32,
    pub token_ids: Vec<u32>,
    pub row_valid_lengths: Vec<u32>,
    pub token_ids_digest: String,
    pub row_valid_lengths_digest: String,
    pub authority_digest: String,
}
```

This is host metadata/identity authority, not a GPU tensor authority.

---

# 7. Input authority construction point

The authority is constructed exactly once in R6-R6 immediately after the existing input validation:

```text
parse token ids
parse row valid lengths
validate B*Q cardinality
validate each valid length
seal BaseTrainRuntimeInputSequenceAuthority
pass authority.token_ids into the existing embedding micro-atlas execution
retain the authority in R6R6LiveBodySession
```

The embedding path and target-loss path thereby share one actual sequence SSOT.

---

# 8. R6-R6 live-session extension

Recommended extension:

```rust
pub struct R6R6LiveBodySession {
    ... existing fields ...
    pub input_sequence_authority: BaseTrainRuntimeInputSequenceAuthority,
}
```

The R6-R6 final receipt should bind only the authority digest and geometry, not duplicate the full token vector unless debug output explicitly needs it.

Existing decoder numerical behavior is unchanged.

---

# 9. Input authority validation

Required:

```text
batch_size > 0
seq_len > 0
token_ids.len() == B*Q
row_valid_lengths.len() == B
for each L_b: 1 <= L_b <= Q
```

The current R6-R6 physical gate may continue requiring `B=1`, `Q=32`, and `L_0=32` as fixture admission, but the authority type itself must not encode those numbers as architectural constants.

---

# 10. No parent-chain spelunking

R6-R11 must not recover runtime state with a long expression such as:

```rust
self.parent.parent.parent.parent....
```

The recent R6-R10 compile closure demonstrated that raw parent-chain depth is a fragile implementation detail.

Use typed accessors.

Recommended:

```rust
impl R6R10FinalRmsNormLmHeadForwardSession {
    pub fn runtime(&self) -> &R6R6LiveBodySession;
    pub fn input_sequence_authority(&self) -> &BaseTrainRuntimeInputSequenceAuthority;
    pub fn canonical_logit_pointer(&self) -> Result<LogitSurfaceAuthorityPointer>;
}
```

R6-R11 consumes those accessors only.

---

# 11. Canonical logit source

The sole numerical logit source is:

```text
R6-R10 LogitSurfaceAuthoritySlot
```

R6-R11 must not use:

```text
private R6-R10 candidate logits
per-wave candidate logits
per-wave reference logits
CPU logits
new LM-head forward output
new final-norm output
```

The canonical pointer produced by R6-R10 is the exact source authority.

---

# 12. Exact logit pointer binding

Before loss computation require exact equality between the R6-R10 final receipt and the live logit slot for:

```text
pointer digest
checkpoint set digest
source final hidden pointer digest
final norm activation identity digest
LM-head source authority digest
shape [B,Q,V]
scalar count B*Q*V
buffer identity digest
completion token digest
publication generation
writer id
operation id
```

No digest-shape-only admission.

---

# 13. Logit execution lease

R6-R11 acquires exactly one:

```text
LogitSurfaceExecutionLease
```

using the R6-R10 canonical pointer digest.

Required:

```text
logit lease acquisition count = 1
logit lease exact pointer bound = true
logit active consumer leases before = 0
logit active consumer leases during = 1
logit active consumer leases after = 0
```

The lease remains valid until all loss kernels and the loss completion fence are bound.

---

# 14. Logit immutability

R6-R11 reads the canonical logits buffer but never writes it.

Required before/after:

```text
logit pointer digest unchanged
logit buffer identity unchanged
logit completion token unchanged
logit publication generation unchanged
canonical logit publication count remains 1
```

No second logit adoption.

---

# 15. Causal target-shift authority

R6-R11 derives one immutable target authority from the retained input sequence and the canonical logit geometry.

Recommended:

```rust
pub struct R6R11CausalTargetEntry {
    pub ordinal: u32,
    pub batch_index: u32,
    pub query_index: u32,
    pub flat_logit_row_index: u32,
    pub source_next_token_flat_index: u32,
    pub target_token_id: u32,
}

pub struct R6R11CausalTargetShiftAuthority {
    pub schema_version: u32,
    pub input_sequence_authority_digest: String,
    pub logit_surface_pointer_digest: String,
    pub batch_size: u32,
    pub seq_len: u32,
    pub vocab_size: u32,
    pub row_valid_lengths: Vec<u32>,
    pub valid_target_count: u32,
    pub entries: Vec<R6R11CausalTargetEntry>,
    pub entries_digest: String,
    pub authority_digest: String,
}
```

---

# 16. Target entry ordering

Entries are emitted in canonical order:

```text
batch ascending
then query ascending
```

No later sort by target token id or digest.

The ordinal is exactly the vector position.

---

# 17. Target entry relation

For every entry:

```text
flat_logit_row_index = b*Q + q
source_next_token_flat_index = b*Q + q + 1
target_token_id = token_ids[source_next_token_flat_index]
q + 1 < row_valid_lengths[b]
target_token_id < V
```

Required globally:

```text
entries.len() = valid_target_count
flat logit row indices unique
target ordinals contiguous 0..N_valid
```

---

# 18. Loss selection is valid-length-driven

R6-R11 does not infer valid targets by token value.

In particular it does not automatically ignore:

```text
pad token id
EOS token id
BOS token id
UNK token id
```

when those values occur within the admitted valid length.

The current loss-selection SSOT is solely:

```text
row_valid_lengths + causal q+1 availability
```

A later dataset/assistant-only-loss patch may introduce a stronger explicit target mask authority.

---

# 19. Relationship to historical BaseTrain batch metadata

The repository already contains `BaseTrainBatchSequenceMetadata` with:

```text
input_ids_digest
target_ids_digest
row_valid_lengths
loss_selection_digest
```

That contract remains valid for the older dataset/training path where explicit `target_ids` exist.

R6-R11 does not silently pretend those explicit targets exist in the current R6 fixture.

Instead R6-R11 owns a narrower **causal-shift-derived target authority** from the actual runtime input sequence.

Future unification may bind explicit dataset targets to this authority, but that is not required for R6-R11.

---

# 20. No phantom terminal target

R6-R11 explicitly forbids:

```text
target for q = L_b - 1
wrap to next batch row
repeat final token as target
use EOS unless an EOS token is actually present at q+1
invent target from tokenizer metadata
invent target from checkpoint metadata
```

For the current `L=32` row, q=31 is masked from loss.

---

# 21. Target GPU upload

R6-R11 uploads only the compact causal target-entry array to the existing WGPU device.

Recommended packed entry:

```text
u32 flat_logit_row_index
u32 target_token_id
```

8 bytes per valid target.

Batch/query indices remain host receipt metadata and need not occupy GPU bytes when flat row identity is sufficient.

---

# 22. Target upload receipt

Recommended:

```rust
pub struct R6R11TargetUploadReceipt {
    pub schema_version: u32,
    pub target_authority_digest: String,
    pub valid_target_count: u32,
    pub entry_stride_bytes: u32,
    pub upload_bytes: u64,
    pub upload_count: u32,
    pub target_buffer_identity_digest: String,
    pub host_to_gpu_upload_count: u32,
    pub gpu_to_host_payload_readback_count: u32,
    pub pass: bool,
    pub receipt_digest: String,
}
```

Required:

```text
upload count = 1
upload bytes = N_valid * 8
gpu-to-host target payload readback = 0
```

---

# 23. Forward-loss formula

For each valid target entry `i` selecting logit row `z_i` and target `y_i`:

```text
m_i = max_v z_i[v]
logZ_i = m_i + ln(sum_v exp(z_i[v] - m_i))
NLL_i = logZ_i - z_i[y_i]
```

Final forward mean loss:

```text
loss_sum  = sum_i NLL_i
mean_loss = loss_sum / N_valid
```

No label smoothing in R6-R11.

---

# 24. Label smoothing authority

R6-R11 fixes:

```text
label_smoothing = 0
```

because the current R6 runtime provides no admitted label-smoothing policy authority.

The existing generic training path may support optional label smoothing, but R6-R11 must not inherit it implicitly.

A future patch may add a sealed training-loss policy.

---

# 25. No softmax probability tensor

R6-R11 computes stable logsumexp directly.

Forbidden:

```text
full probability surface [B,Q,V]
full log-softmax surface [B,Q,V]
second full logits-sized temporary tensor for probabilities
```

Required:

```text
softmax_probability_materialization_count = 0
log_softmax_full_surface_materialization_count = 0
```

---

# 26. Candidate loss kernel

R6-R11 introduces one canonical raw-WGPU candidate row-NLL kernel.

Recommended dispatch:

```text
one workgroup per valid target entry
```

Each workgroup:

```text
reads target entry
binds one canonical logit row
first strided vocab pass: compute row maximum
workgroup reduce max
second strided vocab pass: compute exp(logit-max) sum
workgroup reduce exp sum
read exact target logit
write one NLL scalar
```

No CPU numerical participation.

---

# 27. Candidate workgroup size

Workgroup size is a compile-time kernel parameter chosen within adapter limits, recommended `256` for the initial implementation.

The workgroup size is not a model semantic authority.

The semantic coverage is:

```text
all V logits in every selected row visited
```

not a fixed number of loop iterations.

---

# 28. Stable maximum reduction

Every candidate row requires:

```text
visited vocab scalar count = V
row maximum finite
```

No sentinel initialization that can incorrectly dominate all-negative logits.

Initialize local maximum from negative infinity or another mathematically exact equivalent supported by WGSL.

---

# 29. Stable exp-sum reduction

Second pass requires:

```text
sum_exp > 0
sum_exp finite
```

with each term:

```text
exp(z_v - row_max)
```

No direct `exp(z_v)` accumulation.

---

# 30. Target logit gather

The target logit is read from exactly:

```text
row_base + target_token_id
```

with:

```text
target_token_id < V
```

The gather must not depend on a sampled candidate subset.

Full-vocabulary normalization is mandatory.

---

# 31. Candidate per-target output

The candidate kernel writes exactly one F32 NLL per target authority entry.

Buffer shape:

```text
[N_valid]
```

Required:

```text
candidate NLL output scalar count = N_valid
candidate NLL nonfinite count = 0
```

The per-target NLL buffer is private, not canonical training state.

---

# 32. Independent GPU reference

R6-R11 must not certify the new NLL kernel solely by comparing it with itself.

Introduce an independent same-device reference path with a different decomposition.

Recommended reference stages:

```text
Stage A: row max kernel -> [N_valid]
Stage B: row exp-sum + target gather -> [N_valid] logZ/target components
Stage C: reference NLL combine -> [N_valid]
```

The reference is non-authoritative and never publishes the loss.

---

# 33. Candidate/reference independence

Candidate and reference may share:

```text
canonical logits buffer
target-entry buffer
adapter/device/queue
```

They must not share the same NLL implementation body or copy candidate NLLs into the reference buffer.

Required:

```text
reference runtime authority count = 0
candidate-to-reference copy count = 0
```

---

# 34. Same-device contract

All loss kernels run on the same device/queue lineage as R6-R10.

Required:

```text
new device creation count = 0
CPU logits computation count = 0
CPU cross-entropy computation count = 0
```

---

# 35. Per-target NLL parity

Use an existing compact GPU parity mechanism when compatible, preferably the already-admitted mixed-envelope comparator.

Compare:

```text
candidate_nll[N_valid]
reference_nll[N_valid]
```

Required:

```text
compared scalar count = N_valid
nonfinite count = 0
envelope violation count = 0
tensor payload readback count = 0
```

---

# 36. Loss parity tolerances

R6-R11 owns fixed startup tolerances:

```text
--r6-r11-loss-absolute-tolerance
--r6-r11-loss-relative-tolerance
--r6-r11-loss-relative-floor
```

Requirements:

```text
finite
non-negative
relative floor > 0
constant for the whole invocation
sealed into receipt
```

No tolerance widening after observing a failure.

---

# 37. No logit parity rerun

R6-R10 already proved LM-head candidate/reference parity before canonical logit publication.

R6-R11 must not rerun the LM-head parity/reference projection.

It validates only the **new loss operator**.

Required:

```text
LM-head candidate projection count in R6-R11 = 0
LM-head reference projection count in R6-R11 = 0
```

---

# 38. Hierarchical candidate loss reduction

After per-target NLL parity passes, R6-R11 reduces the candidate NLL buffer on GPU.

Use a deterministic hierarchical reduction, not a CPU sum.

Recommended per pass:

```text
input N scalars
one output scalar per workgroup
repeat until one loss_sum scalar remains
```

All intermediate buffers are private.

---

# 39. Reduction topology authority

The reduction plan is derived from `N_valid` and the fixed reduction workgroup width.

Recommended receipt fields:

```text
input scalar count
pass count
per-pass input counts
per-pass output counts
final scalar count = 1
```

No hard-coded `N_valid=31` branch.

---

# 40. Mean loss finalize

One final same-device kernel computes:

```text
mean_loss = loss_sum / f32(N_valid)
```

Required:

```text
N_valid > 0
loss_sum finite
mean_loss finite
mean_loss >= 0 within numerical tolerance
```

Do not clamp a negative mean loss to zero.

A materially negative NLL result is failure.

---

# 41. Valid-target count GPU binding

The target authority's `N_valid` is uploaded/bound as part of the loss operation.

The GPU reduction output also records or verifies the selected target count using a compact counter or equivalent dispatch-bound evidence.

Required:

```text
GPU observed valid target count = target authority valid target count
```

No loss denominator may use `B*Q` when masked targets exist.

---

# 42. Current fixture denominator

For the current physical parent:

```text
B=1
Q=32
row_valid_lengths=[32]
```

Expected:

```text
N_valid=31
```

The mean loss denominator is 31.

`32` is not an admissible denominator in the current fixture.

---

# 43. Forward loss authority state

Introduce a distinct model-core state domain:

```text
ForwardLossAuthoritySlot
```

It is not part of `LogitSurfaceAuthoritySlot` and does not mutate logits.

Recommended state:

```rust
pub enum ForwardLossAuthorityState {
    Vacant,
    Resident,
}
```

---

# 44. Forward loss pointer

Recommended:

```rust
pub struct ForwardLossAuthorityPointer {
    pub schema_version: u32,
    pub checkpoint_set_digest: String,
    pub source_logit_pointer_digest: String,
    pub source_logit_completion_token_digest: String,
    pub input_sequence_authority_digest: String,
    pub target_shift_authority_digest: String,
    pub valid_target_count: u32,
    pub reduction_plan_digest: String,
    pub loss_sum_buffer_identity_digest: String,
    pub mean_loss_buffer_identity_digest: String,
    pub completion_token_digest: String,
    pub publication_generation: u64,
    pub writer_id: String,
    pub operation_id: String,
    pub pointer_digest: String,
}
```

---

# 45. Forward loss material

The slot owns a compact GPU-resident loss material.

Recommended minimum buffers:

```text
loss_sum: 1 x f32
mean_loss: 1 x f32
```

or one aligned compact result buffer containing both fields if ABI is explicit.

The canonical loss is the GPU material, not the printed CPU diagnostic value.

---

# 46. Single loss adoption

`ForwardLossAuthoritySlot` starts Vacant.

Only after:

```text
target authority pass
candidate NLL finite pass
candidate/reference parity pass
hierarchical reduction pass
mean loss finite pass
exact valid-target count pass
completion fence pass
```

may the compact loss material be adopted once.

Required:

```text
canonical forward-loss publication count = 1
parallel loss authority count = 0
```

---

# 47. Partial loss is never canonical

Before final loss adoption, all buffers are private operation state.

If any target row, parity comparison, or reduction stage fails:

```text
ForwardLossAuthoritySlot remains Vacant
private NLL buffers discarded
private reduction buffers discarded
canonical logits remain Resident and unchanged
```

No partial mean/sum becomes authoritative.

---

# 48. Loss completion token

The loss completion token binds at minimum:

```text
source logit pointer/completion
input sequence authority digest
target shift authority digest
candidate NLL evidence digest
reference NLL evidence digest
parity receipt digest
reduction plan digest
loss reduction receipt digest
valid target count
writer/operation id
```

No token is minted before the completion fence.

---

# 49. Persistent loss identity

Loss buffer identities are semantic/publication identities.

They must not be redefined by later raw-WGPU bridge seam IDs.

This follows the same identity discipline established by C8-D1 and R6-R10 logits.

---

# 50. Compact scalar diagnostic readback

R6-R11 may read back a compact diagnostic result after canonical GPU loss completion.

Allowed diagnostic values:

```text
loss_sum f32
mean_loss f32
valid_target_count u32
nonfinite/error counters
```

This compact readback is observational.

It is not the canonical forward-loss authority.

---

# 51. Zero logit payload readback

Required:

```text
canonical logit payload readback count = 0
per-row logit readback count = 0
CPU logsumexp count = 0
CPU target-logit gather count = 0
CPU cross-entropy count = 0
```

Reading one compact final loss scalar does not violate zero logit payload readback.

---

# 52. No hidden access required

R6-R11 consumes logits, not hidden states.

Required:

```text
final hidden lease acquisition count in R6-R11 = 0
hidden recompute count = 0
hidden mutation count = 0
final RMSNorm forward count in R6-R11 = 0
```

R6-R10's hidden/final-norm evidence is lineage metadata only.

---

# 53. No LM-head weight access required

R6-R11 does not read checkpoint LM-head weights.

Required:

```text
LM-head checkpoint range read count = 0
LM-head decode count = 0
LM-head wave material commit count = 0
LM-head wave residency count = 0
LM-head reprojection count = 0
```

The canonical logits already contain the complete projection result.

---

# 54. No decoder access required

Required:

```text
decoder execution count in R6-R11 = 0
decoder weight reload count = 0
decoder weight rebind count = 0
decoder checkpoint read count = 0
```

The final decoder weight may remain resident but is not leased by the loss path.

---

# 55. No checkpoint payload access

R6-R11 needs no weight payload from the checkpoint.

Required:

```text
checkpoint weight read count = 0
checkpoint weight decode count = 0
checkpoint mutation count = 0
```

Checkpoint identity is carried only for lineage sealing.

---

# 56. No tokenizer rerun

The token IDs already exist as runtime input authority.

R6-R11 must not rerun tokenizer normalization/tokenization to rediscover targets.

Required:

```text
tokenizer execution count = 0
text normalization count = 0
G2P or frontend processing count = 0
```

This is a tensor-level training boundary.

---

# 57. Sequence-authority immutability

The retained R6 input sequence authority is immutable.

R6-R11 may derive a target-shift authority but must not alter:

```text
token_ids
row_valid_lengths
batch size
seq len
input sequence digest
```

Required mutation count = 0.

---

# 58. No pad-value heuristic

The loss mask is not `target != pad_token_id` in R6-R11 because no explicit target tensor/pad-loss policy is currently admitted in the R6 runtime.

The sole current rule is causal next-token availability under row valid lengths.

This avoids silently importing dataset-training behavior from a different path.

---

# 59. Assistant-only loss remains outside scope

The repository dataset path supports assistant-only masking for some samples.

R6-R11 current runtime input authority does not carry prompt/assistant segment masks.

Therefore:

```text
assistant_only_loss = NOT ADMITTED in R6-R11
```

R6-R11 must not claim assistant-only semantics.

A later dataset-to-R6 sequence authority patch can add explicit loss-selection masks.

---

# 60. Explicit target override is forbidden

R6-R11 base patch does not accept:

```text
--target-token-ids
--labels
--loss-mask
```

as a second authority.

Targets are derived from the exact runtime input sequence only.

Future explicit-dataset-target adoption must be a separate SSOT change.

---

# 61. Candidate NLL evidence

Recommended:

```rust
pub struct R6R11CandidateNllEvidence {
    pub schema_version: u32,
    pub source_logit_pointer_digest: String,
    pub target_shift_authority_digest: String,
    pub batch_size: u32,
    pub seq_len: u32,
    pub vocab_size: u32,
    pub valid_target_count: u32,
    pub workgroup_size: u32,
    pub workgroup_dispatch_count: u32,
    pub expected_vocab_visit_count: u64,
    pub observed_vocab_visit_count: u64,
    pub candidate_nll_scalar_count: u32,
    pub non_finite_count: u32,
    pub tensor_payload_readback_count: u32,
    pub pass: bool,
    pub evidence_digest: String,
}
```

Expected vocab visit relation:

```text
N_valid * V * 2
```

if the candidate implementation performs exactly two full vocab passes per target row.

If implementation topology changes, record topology-derived visits rather than hard-coding two as a semantic requirement.

---

# 62. Reference NLL evidence

Recommended:

```rust
pub struct R6R11ReferenceNllEvidence {
    pub schema_version: u32,
    pub source_logit_pointer_digest: String,
    pub target_shift_authority_digest: String,
    pub valid_target_count: u32,
    pub row_max_dispatch_count: u32,
    pub exp_sum_target_dispatch_count: u32,
    pub nll_combine_dispatch_count: u32,
    pub reference_nll_scalar_count: u32,
    pub non_finite_count: u32,
    pub runtime_authority_count: u32,
    pub tensor_payload_readback_count: u32,
    pub pass: bool,
    pub evidence_digest: String,
}
```

Reference runtime authority count must be zero.

---

# 63. NLL parity receipt

Recommended:

```rust
pub struct R6R11NllParityReceipt {
    pub schema_version: u32,
    pub valid_target_count: u32,
    pub compared_scalar_count: u32,
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
    pub receipt_digest: String,
}
```

---

# 64. Reduction plan

Recommended:

```rust
pub struct R6R11LossReductionPassPlan {
    pub pass_ordinal: u32,
    pub input_scalar_count: u32,
    pub output_scalar_count: u32,
    pub workgroup_count: u32,
}

pub struct R6R11LossReductionPlan {
    pub schema_version: u32,
    pub valid_target_count: u32,
    pub workgroup_size: u32,
    pub passes: Vec<R6R11LossReductionPassPlan>,
    pub final_scalar_count: u32,
    pub plan_digest: String,
}
```

Required final scalar count = 1.

---

# 65. Reduction receipt

Recommended:

```rust
pub struct R6R11LossReductionReceipt {
    pub schema_version: u32,
    pub plan_digest: String,
    pub input_nll_scalar_count: u32,
    pub reduction_dispatch_count: u32,
    pub final_sum_scalar_count: u32,
    pub valid_target_count: u32,
    pub gpu_observed_valid_target_count: u32,
    pub loss_sum_finite: bool,
    pub mean_loss_finite: bool,
    pub compact_diagnostic_readback_count: u32,
    pub tensor_payload_readback_count: u32,
    pub pass: bool,
    pub receipt_digest: String,
}
```

---

# 66. Forward-loss publication receipt

Recommended:

```rust
pub struct R6R11ForwardLossReceipt {
    pub schema_version: u32,
    pub patch_id: String,
    pub build_revision: String,
    pub parent_r6_r10_receipt_digest: String,
    pub checkpoint_set_digest: String,
    pub source_logit_pointer_digest: String,
    pub source_logit_completion_token_digest: String,
    pub input_sequence_authority_digest: String,
    pub target_shift_authority_digest: String,
    pub target_upload_receipt_digest: String,
    pub candidate_nll_evidence_digest: String,
    pub reference_nll_evidence_digest: String,
    pub nll_parity_receipt_digest: String,
    pub reduction_plan_digest: String,
    pub reduction_receipt_digest: String,
    pub valid_target_count: u32,
    pub loss_surface_pointer_digest: String,
    pub loss_completion_token_digest: String,
    pub canonical_loss_publication_count: u32,
    pub logit_lease_acquire_count: u32,
    pub logit_pointer_unchanged: bool,
    pub logit_payload_readback_count: u32,
    pub hidden_recompute_count: u32,
    pub final_norm_recompute_count: u32,
    pub lm_head_reprojection_count: u32,
    pub decoder_execution_count: u32,
    pub checkpoint_weight_read_count: u32,
    pub backward_count: u32,
    pub optimizer_count: u32,
    pub weight_mutation_count: u32,
    pub production_inference_count: u32,
    pub pass: bool,
    pub receipt_digest: String,
}
```

---

# 67. Final receipt invariants

Required:

```text
valid target count > 0
canonical loss publication = 1
logit lease acquisition = 1
logit pointer unchanged = true
logit payload readback = 0
hidden recompute = 0
final norm recompute = 0
LM-head reprojection = 0
decoder execution = 0
checkpoint weight reads = 0
backward = 0
optimizer = 0
weight mutation = 0
production inference = 0
```

---

# 68. Loss scalar observation

The terminal gate may print:

```text
loss_sum=<finite f32 diagnostic>
mean_loss=<finite f32 diagnostic>
```

when compact scalar readback is enabled by the fixed R6-R11 contract.

These numbers are observations of the canonical GPU loss material after completion.

They are not recomputed on CPU.

---

# 69. Fail-closed target-authority boundary

Before any loss dispatch, hard fail if:

```text
input sequence authority missing
input authority digest invalid
B/Q mismatch with logit pointer
row valid length out of range
valid target count = 0
any target id >= V
entry count mismatch
duplicate flat logit row index
```

Canonical logits remain unchanged.

---

# 70. Candidate failure boundary

If candidate NLL fails:

```text
ForwardLossAuthoritySlot remains Vacant
reference/reduction do not publish canonical state
canonical logit lease is released after safe completion/error handling
canonical logits remain unchanged
```

No CPU fallback.

---

# 71. Reference/parity failure boundary

If reference or parity fails:

```text
loss publication count = 0
reduction may not become canonical
canonical logits remain intact
```

No `candidate-only` admission.

---

# 72. Reduction failure boundary

If hierarchical reduction or mean finalize fails:

```text
ForwardLossAuthoritySlot remains Vacant
private per-target NLL buffers discarded
canonical logits remain intact
```

No CPU summation fallback.

---

# 73. Loss adoption failure boundary

If final slot adoption fails after GPU completion:

```text
no second adoption attempt with a modified operation id
no mutation of logit authority
no backward
```

Return explicit failure.

---

# 74. No same-operation fallback

Forbidden:

```text
GPU loss failure -> Burn training.rs CrossEntropyLoss
GPU loss failure -> CPU cross entropy
GPU parity failure -> accept candidate
GPU reduction failure -> CPU mean
missing final target -> fabricate EOS
```

Same-operation fallback count must remain zero.

---

# 75. Forward-only autograd boundary

R6-R11 does not claim a Burn autodiff graph survives the raw-WGPU loss path.

It proves the forward causal loss numerically and publishes a GPU-resident loss authority.

Backward remains a separate patch that must define its gradient authority explicitly.

Required:

```text
backward graph admitted = false
backward dispatch count = 0
```

---

# 76. Why existing training.rs loss is not canonical here

The current generic training helper:

```rust
causal_lm_loss(...)
```

calls:

```text
model.forward_logits(...)
CrossEntropyLoss::forward(...)
```

and the scalar helper can read loss data to CPU.

That route does not consume the R6-R10 canonical raw logit surface and would rerun a different model forward authority.

Therefore R6-R11 must not call it.

It may remain historical/generic training infrastructure outside this admission path.

---

# 77. No full logits clone

The loss kernels borrow the canonical logit buffer through the lease.

Forbidden:

```text
full BQV logit buffer clone
full BQV CPU copy
full BQV second canonical buffer
```

Private reference logic reads the same borrowed canonical source.

---

# 78. Memory envelope

R6-R11 adds only compact target/NLL/reduction/reference buffers.

Expected largest new buffers are proportional to:

```text
N_valid
```

not:

```text
B*Q*V
```

because the canonical BQV logits already exist.

No second full BQV temporary is required.

---

# 79. Runtime target memory

For compact packed target entries:

```text
target_upload_bytes = N_valid * 8
```

For current fixture:

```text
N_valid = 31
target_upload_bytes = 248 bytes
```

This is an expected observation, not an architectural constant.

---

# 80. Per-target private memory

Candidate and reference NLL buffers each contain:

```text
N_valid * 4 bytes
```

Reference max/sum intermediates may add small multiples of `N_valid`.

C10's decoder host-transient budget is not repurposed as a fake GPU allocator budget for these buffers.

Device limits are checked independently.

---

# 81. Same-device completion fence

Before loss authority adoption require completion of:

```text
candidate NLL
reference NLL
parity
candidate reduction
mean finalize
compact finite/count validation
```

The completion token binds the exact submitted operation lineage.

---

# 82. Loss finite requirements

Required:

```text
candidate per-target nonfinite = 0
reference per-target nonfinite = 0
loss_sum finite = true
mean_loss finite = true
```

No NaN/Inf replacement.

---

# 83. Non-negativity diagnostic

For exact cross entropy/NLL, loss should be non-negative.

R6-R11 requires:

```text
mean_loss >= -absolute_tolerance
```

A tiny negative value within fixed numerical tolerance may be treated as diagnostic zero-equivalence, but the GPU value itself is not clamped or rewritten.

A value below `-absolute_tolerance` is failure.

---

# 84. No perplexity authority yet

R6-R11 does not need to publish perplexity.

`exp(mean_loss)` may overflow and is not required for forward-loss admission.

If printed later, it is a derived diagnostic, not loss SSOT.

---

# 85. Operation identity

Recommended operation id binds:

```text
checkpoint set digest
source logit pointer digest
source logit completion token
input sequence authority digest
target shift authority digest
valid target count
loss policy/tolerance digest
```

No random nonce as semantic authority.

---

# 86. Writer identity

Recommended canonical writer id:

```text
ash-basetrain-r6-r11-causal-forward-loss
```

Only that writer may adopt the R6-R11 `ForwardLossAuthoritySlot` in the physical gate.

---

# 87. Loss policy receipt

Recommended fixed policy:

```rust
pub struct R6R11CausalLossPolicy {
    pub schema_version: u32,
    pub target_mode: String,              // "next_input_token_shift"
    pub final_position_without_target: String, // "exclude"
    pub valid_length_authority: String,   // "runtime_row_valid_lengths"
    pub label_smoothing_bits: u32,        // 0.0
    pub reduction: String,                // "mean_over_valid_targets"
    pub absolute_tolerance_bits: u32,
    pub relative_tolerance_bits: u32,
    pub relative_floor_bits: u32,
    pub policy_digest: String,
}
```

No mutable runtime policy.

---

# 88. CLI additions

Recommended:

```text
--require-r6-r11-causal-forward-loss true
--require-r6-r11-r6-r10-physical-parent true
--require-r6-r11-canonical-logit-exact-lease true
--require-r6-r11-runtime-input-sequence-authority true
--require-r6-r11-causal-target-shift true
--require-r6-r11-row-valid-length-loss-selection true
--require-r6-r11-terminal-position-without-target-excluded true
--require-r6-r11-valid-target-count-runtime-derived true
--require-r6-r11-same-device-stable-logsumexp true
--require-r6-r11-independent-gpu-reference true
--require-r6-r11-nll-parity true
--require-r6-r11-hierarchical-loss-reduction true
--require-r6-r11-mean-over-valid-targets true
--require-r6-r11-canonical-loss-single-adoption true
--require-r6-r11-zero-logit-payload-readback true
--require-r6-r11-zero-hidden-recompute true
--require-r6-r11-zero-final-norm-recompute true
--require-r6-r11-zero-lm-head-reprojection true
--require-r6-r11-zero-decoder-execution true
--require-r6-r11-zero-checkpoint-weight-read true
--require-r6-r11-zero-backward true
--require-r6-r11-zero-optimizer true
--require-r6-r11-zero-weight-mutation true

--r6-r11-loss-absolute-tolerance <finite f32>
--r6-r11-loss-relative-tolerance <finite f32>
--r6-r11-loss-relative-floor <finite positive f32>

--allow-r6-r11-explicit-target-override false
--allow-r6-r11-terminal-target-fabrication false
--allow-r6-r11-pad-token-mask-inference false
--allow-r6-r11-assistant-only-loss-inference false
--allow-r6-r11-full-softmax-surface false
--allow-r6-r11-cpu-cross-entropy false
--allow-r6-r11-logit-payload-readback false
--allow-r6-r11-loss-tolerance-widening false
--allow-r6-r11-backward false
```

---

# 89. No new sequence geometry authority

R6-R11 uses:

```text
B,Q from canonical logit pointer
B,Q from retained input sequence authority
V from canonical logit pointer/checkpoint lineage
```

Required:

```text
logit B == sequence B
logit Q == sequence Q
```

No new `--batch-size` or `--seq-len` R6-R11 override.

---

# 90. Required implementation surface

Recommended semantic files:

```text
crates/model_core/src/
  base_train_runtime_input_sequence_authority.rs
  base_train_output_head_authority.rs
  lib.rs

crates/burn_webgpu_backend/src/
  base_train_causal_nll.rs
  base_train_causal_nll_reference.rs
  base_train_loss_reduce.rs
  lib.rs

crates/burn_webgpu_backend/src/shaders/
  base_train_causal_nll.wgsl
  base_train_causal_nll_reference_max.wgsl
  base_train_causal_nll_reference_sum_target.wgsl
  base_train_causal_nll_reference_combine.wgsl
  base_train_loss_reduce.wgsl
  base_train_loss_finalize.wgsl

crates/orchestrator_local/src/
  base_train_atlas_wave_02_r6_r6_runtime.rs
  base_train_atlas_wave_02_r6_r10_final_rmsnorm_lm_head_forward.rs
  base_train_atlas_wave_02_r6_r11_causal_forward_loss.rs

crates/orchestrator_local/src/bin/
  ash_basetrain_atlas_wave_02_r6_r9_forward_coordinator_gate.rs

specs/cli/
  ash_basetrain_atlas_wave_02_r6_r9.args
```

Exact file count may be reduced if modules are combined, but state ownership must remain explicit.

---

# 91. No JS/TS/Python canonical path

R6-R11 canonical runtime remains:

```text
Rust orchestration/state
+ WGPU/WGSL numerical compute
```

No JS/TS core execution path.

No Python loss oracle.

---

# 92. Static forbidden call inventory

R6-R11 canonical module must have zero direct calls to:

```text
run_r6_r9_c9_progressive_n_layer_wave_advancement_session
advance_resident_decoder_to_checkpoint_end
rebind_resident_decoder_layer
execute_canonical_resident_decoder_layer
run_r6_r10_final_rmsnorm_lm_head_forward_session   // physical gate owns the one parent call
causal_lm_loss from existing training.rs
HybridTrainModel::forward_logits
AshModel::new
LM-head wave planner/materializer
checkpoint tensor decode for weights
```

R6-R11 consumes an already-completed R6-R10 session.

---

# 93. Physical gate sequence

Canonical gate order:

```text
run R6-R10 physical parent exactly once
    ↓
validate exact R6-R10 PASS receipt
    ↓
obtain typed runtime/input-sequence/logit accessors
    ↓
acquire exact canonical logit lease
    ↓
build causal target-shift authority
    ↓
upload compact target entries
    ↓
run candidate NLL
    ↓
run independent reference NLL
    ↓
GPU parity
    ↓
hierarchical candidate NLL reduction
    ↓
mean finalize
    ↓
completion fence
    ↓
adopt canonical ForwardLossAuthoritySlot exactly once
    ↓
optional compact scalar diagnostic readback
    ↓
release logit lease
    ↓
print R6-R11 terminal/PASS
```

---

# 94. Parent execution count

The gate must not run R6-R10 twice.

Required:

```text
R6-R10 parent session count = 1
R6-R11 loss execution count = 1
```

Loss retry after a partial failed operation requires a new top-level invocation unless a later explicit retry protocol is admitted.

---

# 95. Current physical expected shape

Given the currently admitted R6-R10 parent, expected observations are:

```text
B=1
Q=32
V=48259
BQV=1544288
row_valid_lengths=32
valid_target_count=31
```

The exact numeric loss value is unknown until physical execution and must not be predeclared.

---

# 96. Expected terminal line

Recommended:

```text
[r6-r11-causal-forward-loss]
checkpoint_layers=<L>
logit_pointer_exact_bound=1
logit_shape_bqv=<B>x<Q>x<V>
logit_scalar_count=<B*Q*V>
logit_lease_acquire=1
input_sequence_authority_bound=1
input_token_count=<B*Q>
row_valid_lengths=<canonical compact representation>
target_mode=next_input_token_shift
terminal_position_without_target=exclude
valid_target_count=<sum(L_b-1)>
target_upload_count=1
target_upload_bytes=<N*8>
candidate_nll_dispatches=<N or implementation-derived>
reference_nll_passes=<implementation-derived>
nll_compared=<N>
nll_nonfinite=0
nll_envelope_violation=0
loss_reduction_passes=<derived>
gpu_valid_target_count=<N>
loss_sum=<finite compact diagnostic>
mean_loss=<finite compact diagnostic>
canonical_loss_publication=1
logit_pointer_unchanged=1
logit_payload_readback=0
hidden_recompute=0
final_norm_recompute=0
lm_head_reprojection=0
decoder_execution=0
checkpoint_weight_read=0
checkpoint_mutation=0
backward=0
optimizer=0
weight_mutation=0
production_inference=0
target_shift_authority_digest=<sha256>
nll_parity_receipt_digest=<sha256>
loss_reduction_receipt_digest=<sha256>
forward_loss_pointer_digest=<sha256>
loss_completion_token_digest=<sha256>
receipt_digest=<sha256>
proof_ledger=HOLD
```

---

# 97. Current fixture expected target line

For the current physical fixture, the terminal line must report:

```text
valid_target_count=31
```

If it reports 32, the gate must fail because the final q position has no admitted next token.

---

# 98. PASS token

```text
PASS_ASH_BASETRAIN_ATLAS_WAVE_02_R6_R11_CAUSAL_FORWARD_LOSS_R6_R10_PHYSICAL_PARENT_CANONICAL_LOGIT_SURFACE_EXACT_POINTER_BUFFER_COMPLETION_AND_BQV_LEASE_RUNTIME_INPUT_SEQUENCE_AUTHORITY_RETAINED_AT_R6_R6_ORIGIN_AND_BOUND_TO_ACTUAL_EMBEDDING_INPUT_CAUSAL_NEXT_INPUT_TOKEN_SHIFT_PER_BATCH_ROW_ROW_VALID_LENGTH_DERIVED_TARGET_SELECTION_FINAL_VALID_POSITION_WITHOUT_NEXT_TOKEN_EXCLUDED_NO_PHANTOM_TERMINAL_TARGET_RUNTIME_DERIVED_VALID_TARGET_COUNT_TARGET_TOKEN_VOCAB_RANGE_EXACT_COMPACT_TARGET_ENTRY_SINGLE_UPLOAD_SAME_DEVICE_CANONICAL_GPU_STABLE_LOGSUMEXP_NLL_FULL_VOCAB_NORMALIZATION_ZERO_FULL_SOFTMAX_PROBABILITY_SURFACE_INDEPENDENT_RAW_WGPU_REFERENCE_DECOMPOSITION_PER_TARGET_NLL_GPU_MIXED_ENVELOPE_PARITY_ZERO_NONFINITE_ZERO_ENVELOPE_VIOLATION_HIERARCHICAL_GPU_LOSS_SUM_REDUCTION_MEAN_OVER_EXACT_VALID_TARGET_COUNT_SINGLE_CANONICAL_FORWARD_LOSS_SURFACE_ADOPTION_COMPACT_SCALAR_DIAGNOSTIC_ONLY_ZERO_CANONICAL_LOGIT_PAYLOAD_READBACK_LOGIT_POINTER_AND_COMPLETION_UNCHANGED_ZERO_HIDDEN_RECOMPUTE_ZERO_FINAL_RMSNORM_RECOMPUTE_ZERO_LM_HEAD_REPROJECTION_ZERO_DECODER_EXECUTION_ZERO_CHECKPOINT_WEIGHT_READ_ZERO_CHECKPOINT_MUTATION_ZERO_CPU_CROSS_ENTROPY_ZERO_SAME_OPERATION_FALLBACK_LABEL_SMOOTHING_ZERO_BACKWARD_OPTIMIZER_WEIGHT_MUTATION_AND_PRODUCTION_INFERENCE_BLOCKED_PROOF_LEDGER_HOLD_SEALED
```

---

# 99. Physical PASS meaning

R6-R11 physical PASS proves:

```text
the exact R6-R10 canonical GPU logit surface can be consumed without reprojection
the loss targets are derived from the exact token sequence that entered R6-R6, not from a reparsed duplicate authority
next-token target pairing is row-local and constrained by actual row valid lengths
the last valid input position is excluded when no next token is available
all admitted target ids are in vocabulary range
the stable full-vocabulary logsumexp NLL is computed on the same GPU device
an independently decomposed GPU reference agrees for every valid target under fixed tolerances
no full softmax/probability surface is materialized
candidate NLL values are reduced entirely on GPU
one mean causal forward loss is published as canonical GPU state
canonical logits remain unchanged and are never payload-read back
no hidden/final-norm/LM-head/decoder forward is recomputed
no checkpoint weights are reread or mutated
no backward or optimizer work occurs
```

---

# 100. Physical PASS does not prove

R6-R11 PASS does **not** prove:

```text
explicit dataset target-id parity
assistant-only loss masking
pad-token ignore semantics outside row-valid-length masking
label smoothing
backward cross-entropy gradient
logit gradient correctness
LM-head gradient correctness
final RMSNorm gradient correctness
decoder gradient correctness
activation checkpointing/recompute strategy
optimizer update correctness
training convergence
multi-step training loop correctness
sampling or production inference readiness
```

Those are separate admissions.

---

# 101. Static closure checklist

Before physical run require:

```text
R6-R6 input sequence authority is constructed before embedding execution
embedding receives the authority's exact token ids / valid lengths
R6R6LiveBodySession retains input sequence authority
R6-R10 provides typed runtime/input/logit accessors
R6-R11 has no long parent.parent chain
R6-R10 parent called exactly once
canonical logit pointer exact lease present
logit state remains Resident through loss
B/Q sequence/logit geometry exact
causal target q+1 relation exact
target never crosses row boundary
last valid position excluded
valid target count derived from row valid lengths
target id < V checked
no explicit target override CLI
no pad heuristic target mask
no assistant-only mask inference
candidate NLL stable max/logsumexp implementation present
reference implementation structurally independent
full probability tensor creation = 0
NLL parity GPU-only except compact diagnostics
hierarchical GPU reduction present
mean denominator = N_valid
canonical loss adoption occurs once after all gates
logit payload readback = 0
hidden recompute = 0
final norm recompute = 0
LM-head reprojection = 0
decoder execution = 0
checkpoint weight read = 0
CPU cross entropy = 0
backward = 0
optimizer = 0
weight mutation = 0
```

---

# 102. Baked package policy

R6-R11 bake produces:

```text
full code ZIP
overlay ZIP
```

Exclude unless explicitly requested:

```text
*.md
*.sha256
artifacts/
manifests/
accumulated historical reports
manifest JSON debug bundles
```

The standalone specification remains outside the baked ZIP and may be committed separately.

---

# 103. Admission state after physical PASS

```text
R6-R6 actual decoder Layer0                       = ADMITTED
R6-R8 resident decoder execution                  = ADMITTED
R6-R9-C8 canonical decoder weight wave loader     = ADMITTED
R6-R9-C9 full checkpoint-bounded decoder loop     = ADMITTED
R6-R9-C10 long-horizon residency health           = ADMITTED
R6-R9-C10-D1 role identity classification         = ADMITTED
R6-R10 final RMSNorm + streamed LM-head logits    = ADMITTED
R6-R11 causal forward loss                        = ADMITTED on physical PASS

Canonical logits surface                          = RESIDENT
Canonical forward loss                            = AVAILABLE after R6-R11 PASS
Backward                                           = BLOCKED
Optimizer                                          = BLOCKED
Weight mutation                                    = BLOCKED
Production inference                               = BLOCKED
Proof ledger                                       = HOLD
```

---

# 104. Natural next boundary

After R6-R11 physical PASS, the next training boundary should be a **loss-to-logit backward seed** rather than a full optimizer leap.

Recommended:

```text
ASH-BASETRAIN-ATLAS-WAVE-02-R6-R12

Causal Loss Backward Seed /
Canonical Forward Loss Exact Binding /
Canonical Logit Surface Exact Lease /
Target Shift Authority Reuse /
Per-Valid-Target Softmax-Minus-OneHot Gradient /
Mean-Loss Scaling /
GPU Logit-Gradient Surface Publication /
Runtime-Derived BQV Coverage with Masked Final Positions /
Zero Logit Payload Readback /
Zero LM-Head Weight Reload /
No Decoder Backward Yet Seal
```

R6-R12 should publish a canonical logit-gradient surface first. LM-head/final-norm/decoder backward should remain later staged boundaries.

---

# 105. Architecture seal

> R6-R11 is the point where ASH BaseTrain first turns its physically published logits into a training objective, but it does so without reopening any earlier forward authority. The loss path leases the exact canonical `[B,Q,V]` surface produced by R6-R10, binds it to an input-sequence authority retained at the original R6-R6 embedding boundary, and derives only causal target pairs that actually exist within each row's valid input length. It does not invent a target for the final valid token; with the current 32-token fixture, exactly 31 targets exist. Those compact target entries are uploaded to the same WGPU device, a stable full-vocabulary logsumexp kernel computes one NLL per target, an independently decomposed GPU reference verifies those NLL values under fixed tolerances, and a hierarchical GPU reduction produces the sum and mean over the exact valid-target count. No probability-sized softmax surface, CPU cross entropy, logit payload readback, hidden recompute, final-norm recompute, LM-head reprojection, decoder execution, or checkpoint-weight reread is allowed. Only after target identity, NLL parity, finite state, reduction count, and completion fencing all pass may one compact GPU-resident `ForwardLossAuthoritySlot` be adopted. The forward loss is then real and canonical, while backward, optimizer mutation, and production inference remain deliberately sealed.
