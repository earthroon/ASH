# ASH-BASETRAIN-ATLAS-WAVE-00

## Training Step Transaction SSOT /
## Causal·Padding·Position·RoPE Authority /
## Same-Generation Fence /
## Atlas Route Random-Init Rejection /
## No Generic Attention Fallback /
## Legacy G206D Namespace Disambiguation Seal

> Status: SPEC RELEASE rev.1  
> Patch ID: `ASH-BASETRAIN-ATLAS-WAVE-00`  
> Build revision: `ATLAS-WAVE-00-training-step-transaction-ssot-v1`  
> Physical parent: `ASH-BASETRAIN-G206D-ISOLATED-WEIGHT-DELTA-MATERIALIZATION-01`  
> Physical parent state: `PASS_ASH_BASETRAIN_G206D_..._NO_SILENT_FALLBACK_SEALED`  
> Legacy audit predecessor: `ASH-BASETRAIN-GPU-70K-G197D`  
> Implementation SSOT: attached G206D-R3 body  
> GitHub lineage reference: `earthroon/ASH`, inspected `main` head `e7d1e7cbd21612eacb82274f8c934c04f2decc92`  
> Runtime mutation authority: none  
> Forward, backward, optimizer, apply, commit authority: none

---

# 0. Purpose

`ASH-BASETRAIN-ATLAS-WAVE-00` establishes the first non-fixture authority boundary for the Atlas Parallel Sequential Wave training line.

This patch does not train the model. It defines exactly what one training step is allowed to read, which component owns its state, which sequence geometry is authoritative, and which generation identities must remain immutable until a later atomic commit patch.

The patch closes six structural holes before any live Headwise, TensorCube, backward, optimizer, or weight apply path is connected.

```text
AtlasGroupedSequential route
  -> explicit checkpoint-backed model source
  -> explicit dataset batch sequence authority
  -> explicit causal + padding + position + RoPE authority
  -> explicit source generation fence
  -> one BaseTrain-owned step transaction
  -> future Headwise/TensorCube execution admission packet
```

Forbidden canonical flow:

```text
AtlasGroupedSequential
  -> grouped load deferred
  -> AshModel::new random weights
  -> generic Burn grouped_query_attention
  -> unmasked softmax
  -> loss labelled causal
```

The patch therefore converts the current Atlas route from an unsafe executable placeholder into a fail-closed prepared transaction surface.

---

# 1. Source-grounded problem statement

## 1.1 Atlas route currently constructs a random model

Current source:

```text
crates/base_train/src/training.rs:386-393
```

Current behavior:

```rust
BaseTrainRoute::AtlasGroupedSequential => {
    println!("... grouped checkpoint load is deferred ...");
    model_core::AshModel::<B>::new(spec.clone(), device)
}
```

`AshModel::new` initializes token embedding, LM head, attention projections, and MLP projections with random tensors. Therefore the current Atlas route is not checkpoint-backed even though `BaseTrainRoute::AtlasGroupedSequential` is the default route.

AW-00 must make this path unrepresentable for Atlas execution.

## 1.2 Generic training attention has no causal or padding mask

Current source:

```text
crates/model_core/src/model_layers.rs:284-312
```

Current behavior:

```rust
let scores = q
    .matmul(k.swap_dims(3, 4))
    .div_scalar((head_dim as f32).sqrt());
let attn = softmax(scores, 4);
let ctx = attn.matmul(v);
```

No causal mask, key padding mask, query padding zeroing, explicit position IDs, or RoPE application is present in this generic function.

The generic primitive may remain for explicit reference and fixture use. It must not remain a silent fallback for `AtlasGroupedSequential`.

## 1.3 Existing `base_train_step.rs` is an audit-only G197D contract

Current source:

```text
crates/base_train/src/base_train_step.rs:39-180
```

The existing `BaseTrainStepInputContract`, `BaseTrainStepOutputContract`, and `base_train_step_contract` belong to `ASH-BASETRAIN-GPU-70K-G197D`. The output is hard-bound to `BaseTrainRunKind::AuditOnly`, and optimizer, weight commit, checkpoint mutation, and route promotion remain blocked.

AW-00 must not silently repurpose or overwrite this legacy audit contract. The new canonical public type is:

```rust
BaseTrainAtlasWaveStepTransaction
```

The bare alias `BaseTrainStepTransaction` is not introduced in AW-00.

## 1.4 Two different G206D identities already coexist

Legacy decision route:

```text
ASH-BASETRAIN-GPU-70K-G206D
module: ash_basetrain_gpu_70k_g206d_decision_outcome_routing
```

Physical delta materialization route:

```text
ASH-BASETRAIN-G206D-ISOLATED-WEIGHT-DELTA-MATERIALIZATION-01
module: base_train_g206d_isolated_weight_delta_materialization
```

A bare `G206D` parent key, directory, log label, or receipt field is ambiguous. AW-00 introduces typed full lineage identities and forbids new bare-G206D authority fields.

---

# 2. Scope

## 2.1 In scope

```text
BaseTrain Atlas Wave step transaction schema
Single writer and state ownership contract
Checkpoint-backed Atlas model-source admission
Causal mask semantic authority
Attention padding semantic authority
Explicit position-ID authority
RoPE configuration authority
Source and candidate generation fence
Atlas route random-init rejection
Atlas route generic-attention fallback rejection
Legacy G197D step-contract separation
Legacy 70K G206D and physical G206D identity separation
Deterministic receipt digest and replay
Host-side validation gate
Source-surface static closure checks
```

## 2.2 Out of scope

```text
WGPU adapter or device creation
Native runtime handle borrowing
Safetensors slice upload
Atlas triple-ring allocation
Headwise training prefill execution
TensorCube Stage10, Stage11, or Stage12 execution
Loss computation
Backward execution
Gradient accumulation
Optimizer candidate execution
G206D live delta consumption
Inactive weight application
Resident weight mutation
Optimizer-state mutation
Training cursor mutation
Pointer swap
Checkpoint write or finalization
Decode route mutation
Quality or convergence claim
```

AW-00 PASS means the training step can be prepared safely. It does not mean the training loop has executed.

---

# 3. Authority map

## 3.1 State ownership

| State or contract | Canonical owner | Mutation authority | Forbidden owner |
|---|---|---|---|
| Step transaction schema | `model_core` | none, immutable schema methods only | backend, gate |
| Live transaction instance | `base_train::BaseTrainAtlasWaveStepCoordinator` | BaseTrain coordinator only | `orchestrator_local`, backend |
| Sequence geometry receipt | `model_core` | constructed once by BaseTrain, then sealed | attention kernel |
| Generation fence | `model_core` | constructed once by BaseTrain, later consumed read-only | optimizer probe |
| Route admission | `base_train` | BaseTrain route validator | model layer |
| Raw GPU execution ABI | future `burn_webgpu_backend` patch | backend-local only | `model_core` importing backend receipts backward |
| Physical verification | `orchestrator_local` | fixture and artifact writer only | resident training owner |

Dependency direction remains:

```text
burn_webgpu_backend
        ^
        |
model_core
        ^
        |
base_train
        ^
        |
orchestrator_local
```

Forbidden:

```text
burn_webgpu_backend -> model_core import
orchestrator_local as transaction owner
physical gate receipt becoming live runtime SSOT
model_core mutating training cursor or weight pointers
```

## 3.2 Single writer

Exactly one live writer may own a prepared transaction.

```rust
pub struct BaseTrainAtlasWaveStepWriterLease {
    pub transaction_id: String,
    pub owner_kind: BaseTrainAtlasWaveStepOwnerKind,
    pub owner_instance_id: String,
    pub lease_generation: u64,
    pub revoked: bool,
    pub lease_digest: String,
}
```

```rust
pub enum BaseTrainAtlasWaveStepOwnerKind {
    BaseTrainCoordinator,
}
```

No second owner enum variant is admitted in AW-00.

Required counters:

```text
step_transaction_writer_acquire_count  1
step_transaction_writer_release_count  1
step_transaction_double_writer_count   0
step_transaction_backend_writer_count  0
step_transaction_gate_writer_count     0
```

---

# 4. Canonical patch and lineage identity

## 4.1 Typed lineage ID

New module:

```text
crates/model_core/src/base_train_patch_lineage.rs
```

Required type:

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum BaseTrainPatchLineageId {
    AtlasWave00,
    Gpu70kG197dAuditStepKernel,
    Gpu70kG206dDecisionOutcomeRouting,
    G206dIsolatedWeightDeltaMaterialization,
}
```

Canonical serialization:

```text
AtlasWave00
  ASH-BASETRAIN-ATLAS-WAVE-00

Gpu70kG197dAuditStepKernel
  ASH-BASETRAIN-GPU-70K-G197D

Gpu70kG206dDecisionOutcomeRouting
  ASH-BASETRAIN-GPU-70K-G206D

G206dIsolatedWeightDeltaMaterialization
  ASH-BASETRAIN-G206D-ISOLATED-WEIGHT-DELTA-MATERIALIZATION-01
```

`Display`, JSON serialization, logs, and artifact fields must emit the complete patch ID.

Forbidden new field names:

```text
g206d_parent
g206d_receipt
g206d_digest
g206d_path
g206d_pass
```

Required explicit field names:

```text
weight_delta_materialization_parent_patch_id
weight_delta_materialization_parent_receipt_digest
legacy_70k_decision_patch_id
legacy_audit_step_patch_id
```

## 4.2 Parent lineage receipt

```rust
pub struct BaseTrainAtlasWaveParentLineageReceipt {
    pub patch_id: String,
    pub build_revision: String,

    pub physical_parent_patch_id: String,
    pub physical_parent_pass_token_digest: String,
    pub physical_parent_runtime_artifact_digest: String,

    pub legacy_audit_step_patch_id: String,
    pub legacy_audit_step_reused_as_live_transaction: bool,

    pub legacy_70k_decision_patch_id: String,
    pub legacy_70k_decision_is_physical_parent: bool,

    pub all_patch_ids_distinct: bool,
    pub bare_g206d_authority_field_count: u32,
    pub receipt_digest: String,
}
```

Required values:

```text
legacy_audit_step_reused_as_live_transaction     false
legacy_70k_decision_is_physical_parent           false
all_patch_ids_distinct                           true
bare_g206d_authority_field_count                  0
```

---

# 5. Atlas model-source authority

## 5.1 Canonical model source enum

`BaseTrainModelSourceAuthority` has exactly two explicit variants in AW-00:

```rust
pub enum BaseTrainModelSourceAuthority {
    ExplicitFreshInit {
        initialization_seed_digest: String,
    },
    CheckpointAtlas {
        checkpoint_path: String,
        checkpoint_digest: String,
        tensor_group_manifest_path: String,
        tensor_group_manifest_digest: String,
        atlas_group_plan_path: String,
        atlas_group_plan_digest: String,
        sequential_load_plan_path: String,
        sequential_load_plan_digest: String,
    },
}
```

There is no `Auto`, `Default`, `Deferred`, or nullable source variant.

## 5.2 Route-source matrix

| Route | Admitted source | Result |
|---|---|---|
| `FreshInit` | `ExplicitFreshInit` | admitted outside Atlas |
| `FreshInit` | `CheckpointAtlas` | reject |
| `AtlasGroupedSequential` | `CheckpointAtlas` | prepare transaction |
| `AtlasGroupedSequential` | `ExplicitFreshInit` | reject |
| `LegacyFullCheckpoint` | legacy loader | unchanged, not Atlas authority |

Required error:

```text
ERR_ASH_BASETRAIN_ATLAS_WAVE_00_ATLAS_RANDOM_INIT_FORBIDDEN
```

## 5.3 Atlas route construction firewall

`BaseTrainRoute::AtlasGroupedSequential` must not reach:

```rust
AshModel::new(...)
build_hybrid_train_model(...)
HybridTrainModel::new(...)
```

Required source arrangement:

```rust
match route {
    BaseTrainRoute::AtlasGroupedSequential => {
        let prepared = prepare_atlas_wave_00_transaction(...)?;
        return Err(BaseTrainError::AtlasWaveForwardNotYetAdmitted {
            transaction_digest: prepared.receipt_digest,
        });
    }
    BaseTrainRoute::FreshInit => {
        // explicit FreshInit-only construction
    }
    BaseTrainRoute::LegacyFullCheckpoint => {
        // existing legacy path
    }
}
```

The exact implementation may use a dedicated preparation API rather than the sketch above. The semantic order is mandatory:

```text
validate checkpoint source
  -> seal sequence authority
  -> seal generation fence
  -> publish prepared transaction
  -> return typed HOLD before model construction
```

Forbidden behavior:

```text
print warning and continue
construct random model then return HOLD
construct hybrid model then return HOLD
fall through to generic training loop
```

---

# 6. Batch sequence metadata SSOT

## 6.1 Dataset-owned metadata

The batching stage is the only authority allowed to derive row validity from raw sample lengths.

`BaseBatchCpu` gains:

```rust
pub struct BaseBatchCpu {
    pub batch_size: usize,
    pub seq_len: usize,
    pub input_ids: Vec<i64>,
    pub target_ids: Vec<i64>,
    pub loss_mask: Vec<f32>,
    pub sequence_metadata: BaseTrainBatchSequenceMetadata,
}
```

Canonical metadata:

```rust
pub struct BaseTrainBatchSequenceMetadata {
    pub batch_size: u32,
    pub padded_seq_len: u32,
    pub row_valid_lengths: Vec<u32>,
    pub padding_side: BaseTrainPaddingSide,
    pub attention_validity_source: BaseTrainAttentionValiditySource,
    pub loss_selection_source: BaseTrainLossSelectionSource,
    pub receipt_digest: String,
}
```

```rust
pub enum BaseTrainPaddingSide {
    Right,
}

pub enum BaseTrainAttentionValiditySource {
    PreservedSourceSequenceLength,
}

pub enum BaseTrainLossSelectionSource {
    DatasetLossMask,
}
```

## 6.2 Attention validity and loss selection are distinct

Required distinction:

```text
attention_valid[b, s]
  s < row_valid_lengths[b]

loss_selected[b, s]
  dataset loss_mask[b, s] > 0
```

A valid prompt token may participate in attention while being excluded from loss. Therefore:

```text
attention mask != loss mask
```

Forbidden inference:

```text
target_ids == ignore_index       -> attention padding
loss_mask == 0                    -> attention padding
token_id == tokenizer pad ID      -> sole attention authority
```

The actual source lengths must be preserved before target shifting, ignore-index insertion, or assistant-only loss masking.

## 6.3 Metadata validation

Required:

```text
row_valid_lengths.len == batch_size
0 < row_valid_lengths[b] <= padded_seq_len
padding side == Right
metadata batch size == tensor batch size
metadata padded sequence length == tensor sequence length
input/target/loss-mask flattened lengths all match
receipt digest replay exact
```

---

# 7. Causal and padding authority

## 7.1 Semantic attention predicate

For batch row `b`, query position `q`, and key position `k`:

```text
query_valid = q < row_valid_lengths[b]
key_valid   = k < row_valid_lengths[b]
causal      = k <= q
admitted    = query_valid && key_valid && causal
```

Required output semantics:

```text
invalid key
  score is excluded before softmax

invalid query
  output context is exact zero
```

A masked row must not become a uniform softmax row.

## 7.2 Canonical authority type

```rust
pub struct BaseTrainAttentionMaskAuthority {
    pub causal: bool,
    pub padding_side: BaseTrainPaddingSide,
    pub row_valid_lengths: Vec<u32>,
    pub invalid_key_score_policy: BaseTrainInvalidKeyScorePolicy,
    pub invalid_query_output_policy: BaseTrainInvalidQueryOutputPolicy,
    pub source_metadata_digest: String,
    pub receipt_digest: String,
}
```

```rust
pub enum BaseTrainInvalidKeyScorePolicy {
    ExcludeBeforeSoftmax,
}

pub enum BaseTrainInvalidQueryOutputPolicy {
    ExactZero,
}
```

AW-00 seals the semantics. It does not construct or upload a GPU mask tensor.

---

# 8. Position authority

## 8.1 Explicit position mode

The only admitted Atlas Wave position mode in AW-00 is:

```rust
pub enum BaseTrainPositionMode {
    ExplicitPerRowZeroBased,
}
```

For a right-padded row with valid length `L`:

```text
position_ids[b, 0..L] = 0, 1, ..., L - 1
position_ids[b, L..S] = 0
```

The padded values are inert because invalid queries are zeroed and invalid keys are excluded.

## 8.2 Position receipt

```rust
pub struct BaseTrainPositionAuthorityReceipt {
    pub mode: BaseTrainPositionMode,
    pub batch_size: u32,
    pub padded_seq_len: u32,
    pub row_valid_lengths: Vec<u32>,
    pub position_ids: Vec<u32>,
    pub model_max_sequence_length: u32,
    pub source_metadata_digest: String,
    pub receipt_digest: String,
}
```

Required:

```text
position_ids.len == batch_size * padded_seq_len
valid positions strictly equal their zero-based sequence index
last valid position < model max sequence length
padded positions equal zero
```

Position IDs must not be reconstructed independently inside Headwise, TensorCube, or backward kernels.

---

# 9. RoPE authority

## 9.1 Canonical RoPE receipt

```rust
pub struct BaseTrainRopeAuthorityReceipt {
    pub theta: f32,
    pub rotary_dim: u32,
    pub head_dim: u32,
    pub interleaving: BaseTrainRopeInterleaving,
    pub q_applied: bool,
    pub k_applied: bool,
    pub v_applied: bool,
    pub position_authority_digest: String,
    pub model_spec_digest: String,
    pub receipt_digest: String,
}
```

```rust
pub enum BaseTrainRopeInterleaving {
    EvenOddPairs,
}
```

Required:

```text
theta finite and > 0
rotary_dim > 0
rotary_dim <= head_dim
rotary_dim even
q_applied true
k_applied true
v_applied false
position authority digest exact
model spec digest exact
```

## 9.2 ModelSpec binding

AW-00 must derive RoPE configuration from the authoritative `ModelSpec` used to identify the checkpoint.

If current `ModelSpec` does not expose all required fields, AW-00 introduces a validated adapter that yields:

```text
rope theta
rotary dimension
head dimension
maximum sequence length
model spec digest
```

Hard-coded kernel-local defaults are forbidden as authority.

---

# 10. Combined sequence authority

```rust
pub struct BaseTrainSequenceAuthorityReceipt {
    pub batch_metadata_digest: String,
    pub attention_mask_authority: BaseTrainAttentionMaskAuthority,
    pub position_authority: BaseTrainPositionAuthorityReceipt,
    pub rope_authority: BaseTrainRopeAuthorityReceipt,
    pub combined_sequence_authority_digest: String,
}
```

The combined digest is the only sequence-geometry parent admitted by later execution patches.

Later receipts must carry this exact digest:

```text
Headwise forward invocation
TensorCube forward invocation
loss
backward
G204D
G205D
G206D live adoption
weight apply
atomic commit
```

A later stage may add an implementation-specific physical mask digest, but it must remain a child of the AW-00 semantic authority digest.

---

# 11. Same-generation fence

## 11.1 Generation fence type

```rust
pub struct BaseTrainAtlasWaveGenerationFence {
    pub model_instance_id: String,
    pub checkpoint_digest: String,

    pub source_weight_generation: u64,
    pub source_optimizer_state_generation: u64,
    pub source_training_cursor_generation: u64,

    pub expected_candidate_weight_generation: u64,
    pub expected_candidate_optimizer_state_generation: u64,
    pub expected_candidate_training_cursor_generation: u64,

    pub atlas_schedule_digest: String,
    pub atlas_residency_generation: Option<u64>,

    pub runtime_binding_state: BaseTrainRuntimeBindingState,
    pub device_epoch: Option<u64>,
    pub queue_epoch: Option<u64>,

    pub fence_digest: String,
}
```

```rust
pub enum BaseTrainRuntimeBindingState {
    UnboundPrepared,
    BoundSameDevice,
}
```

AW-00 required state:

```text
runtime_binding_state          UnboundPrepared
atlas_residency_generation     none
device_epoch                   none
queue_epoch                    none
```

AW-01 may fill those values. AW-00 must not invent them.

## 11.2 Candidate generation contract

Required:

```text
expected_candidate_weight_generation
  == source_weight_generation + 1

expected_candidate_optimizer_state_generation
  == source_optimizer_state_generation + 1

expected_candidate_training_cursor_generation
  == source_training_cursor_generation + 1
```

Overflow fails closed.

## 11.3 Fence consumption rules

Every later stage must present:

```text
transaction ID
model instance ID
checkpoint digest
source weight generation
source optimizer generation
source cursor generation
atlas schedule digest
sequence authority digest
```

Additional requirements after AW-01:

```text
atlas residency generation
device epoch
queue epoch
```

Forbidden:

```text
latest generation substitution
partial generation acceptance
weight generation inferred from pointer identity
optimizer generation inferred from step index
cursor generation advanced before weight commit
mixed checkpoint tensors in one transaction
```

---

# 12. Canonical transaction

## 12.1 Transaction type

```rust
pub struct BaseTrainAtlasWaveStepTransaction {
    pub patch_id: String,
    pub build_revision: String,

    pub transaction_id: String,
    pub run_id: String,
    pub step_index: u64,
    pub microbatch_window_index: u64,
    pub microbatch_set_digest: String,

    pub route: BaseTrainRouteIdentity,
    pub model_source: BaseTrainModelSourceAuthority,
    pub attention_executor: BaseTrainAttentionExecutorAuthority,
    pub fallback_policy: BaseTrainFallbackPolicy,

    pub dataset_pack_digest: String,
    pub tokenizer_digest: String,
    pub model_spec_digest: String,
    pub atlas_schedule_digest: String,

    pub sequence_authority: BaseTrainSequenceAuthorityReceipt,
    pub generation_fence: BaseTrainAtlasWaveGenerationFence,
    pub parent_lineage: BaseTrainAtlasWaveParentLineageReceipt,

    pub state: BaseTrainAtlasWaveStepState,
    pub admitted_transition_ceiling: BaseTrainAtlasWaveStepState,

    pub mutation_firewall: BaseTrainAtlasWave00MutationFirewallReceipt,
    pub receipt_digest: String,
}
```

## 12.2 Route identity

```rust
pub enum BaseTrainRouteIdentity {
    FreshInit,
    AtlasGroupedSequential,
    LegacyFullCheckpoint,
}
```

For an AW-00 transaction:

```text
route == AtlasGroupedSequential
```

## 12.3 Executor and fallback

```rust
pub enum BaseTrainAttentionExecutorAuthority {
    HeadwiseTrainPrefillRequired,
    BurnGenericReferenceExplicit,
}
```

```rust
pub enum BaseTrainFallbackPolicy {
    FailClosed,
}
```

For Atlas:

```text
attention_executor == HeadwiseTrainPrefillRequired
fallback_policy == FailClosed
```

There is no `Auto` executor variant.

## 12.4 State machine

```rust
pub enum BaseTrainAtlasWaveStepState {
    Prepared,
    ForwardWaveActive,
    LossSealed,
    BackwardWaveActive,
    GradientSealed,
    OptimizerCandidateActive,
    DeltaMaterialized,
    InactiveWeightApplied,
    CommitReady,
    Committed,
    Poisoned,
    RolledBack,
}
```

AW-00 admitted state:

```text
Prepared
```

AW-00 transition ceiling:

```text
Prepared
```

Therefore every transition beyond `Prepared` is rejected in this patch.

## 12.5 Existing parent byte preservation

AW-00 must not modify the physical G206D implementation modules and shaders:

```text
crates/model_core/src/base_train_g206d_isolated_weight_delta_materialization.rs
crates/base_train/src/base_train_g206d_isolated_weight_delta_materialization.rs
crates/burn_webgpu_backend/src/base_train_g206d_weight_delta_materialization_probe.rs
crates/burn_webgpu_backend/src/shaders/base_train_g206d_weight_delta_materialize.wgsl
```

AW-00 consumes parent identity and runtime artifact digest only.

---

# 13. Mutation firewall

```rust
pub struct BaseTrainAtlasWave00MutationFirewallReceipt {
    pub gpu_device_create_count: u32,
    pub gpu_queue_create_count: u32,
    pub gpu_buffer_create_count: u32,
    pub gpu_texture_create_count: u32,
    pub queue_submit_count: u32,

    pub forward_execution_count: u32,
    pub loss_compute_count: u32,
    pub backward_execution_count: u32,
    pub optimizer_execution_count: u32,
    pub delta_materialization_count: u32,

    pub resident_weight_write_count: u32,
    pub optimizer_state_write_count: u32,
    pub training_cursor_write_count: u32,
    pub pointer_swap_count: u32,
    pub checkpoint_write_count: u32,

    pub route_promotion_count: u32,
    pub decode_route_mutation_count: u32,
    pub random_init_count: u32,
    pub generic_attention_fallback_count: u32,

    pub pass: bool,
    pub receipt_digest: String,
}
```

All counters must equal zero.

AW-00 is a host-only transaction and validation patch. A GPU dispatch in its gate is a failure, not stronger evidence.

---

# 14. Preparation API

Canonical preparation flow:

```rust
pub struct BaseTrainAtlasWave00PrepareInput {
    pub run_id: String,
    pub step_index: u64,
    pub microbatch_window_index: u64,
    pub microbatch_set_digest: String,

    pub model_source: BaseTrainModelSourceAuthority,
    pub batch_sequence_metadata: BaseTrainBatchSequenceMetadata,
    pub model_spec: ModelSpec,

    pub source_weight_generation: u64,
    pub source_optimizer_state_generation: u64,
    pub source_training_cursor_generation: u64,

    pub atlas_schedule_digest: String,
    pub physical_parent_pass_token_digest: String,
    pub physical_parent_runtime_artifact_digest: String,
}
```

```rust
pub fn prepare_base_train_atlas_wave_00_step(
    coordinator: &mut BaseTrainAtlasWaveStepCoordinator,
    input: BaseTrainAtlasWave00PrepareInput,
) -> Result<BaseTrainAtlasWaveStepTransaction>
```

Required order:

```text
validate route-source pair
validate checkpoint and plan identity
validate preserved sequence metadata
build attention mask authority
build explicit positions
bind RoPE authority
build same-generation fence
build parent lineage receipt
seal transaction digest
acquire single writer lease
publish Prepared transaction
return transaction
```

The preparation API must be deterministic for equivalent normalized input.

---

# 15. Runtime route behavior

## 15.1 Atlas invocation before AW-01

When an operator invokes the existing training entry point with `AtlasGroupedSequential` after AW-00:

```text
transaction preparation success
  -> write or expose prepared transaction receipt
  -> return typed HOLD
```

Required typed HOLD:

```text
HOLD_ASH_BASETRAIN_ATLAS_WAVE_00_FORWARD_WAVE_NOT_YET_ADMITTED
```

The HOLD must include or reference:

```text
transaction ID
transaction receipt digest
model-source authority digest
sequence-authority digest
generation-fence digest
```

## 15.2 FreshInit and legacy routes

AW-00 must not globally ban `AshModel::new`. It only forbids that constructor from the Atlas route.

```text
FreshInit
  explicit random initialization permitted

LegacyFullCheckpoint
  existing behavior preserved

AtlasGroupedSequential
  random initialization forbidden
```

This distinction must be visible in source layout and route validation. A whole-file grep that bans `AshModel::new` everywhere is not sufficient.

---

# 16. Static closure checks

The dedicated gate must inspect source, not merely test helper behavior.

## 16.1 Required module closure

Required declarations and exports:

```text
model_core/src/lib.rs
  pub mod base_train_patch_lineage;
  pub mod base_train_atlas_wave_sequence_authority;
  pub mod base_train_atlas_wave_generation_fence;
  pub mod base_train_atlas_wave_step_transaction;

base_train/src/lib.rs
  pub mod base_train_atlas_wave_step_coordinator;
  pub mod base_train_atlas_wave_00_preflight;
```

## 16.2 Atlas route constructor scan

Within every `BaseTrainRoute::AtlasGroupedSequential` match arm:

```text
AshModel::new                        absent
build_hybrid_train_model             absent
HybridTrainModel::new                absent
prepare_atlas_wave_00                present
ForwardNotYetAdmitted typed HOLD     present
```

## 16.3 Generic fallback scan

Atlas route and AW-00 preparation modules must not call:

```text
grouped_query_attention
AshSelfAttention::forward
HybridTrainModel forward
```

The generic implementation may remain elsewhere.

## 16.4 G206D namespace scan

Within new Atlas Wave source and artifacts:

```text
bare JSON field prefix g206d_          0
bare artifact directory /g206d/        0
bare parent label G206D                0
full physical parent patch ID          1 or more
full legacy decision patch ID          1 or more in namespace audit only
```

## 16.5 Physical parent preservation

Required byte identity for the physical delta materialization implementation and shader files listed in section 12.5.

---

# 17. Verification matrix

## 17.1 Positive cases, minimum 40

Must include:

```text
Atlas checkpoint source with all digests
FreshInit explicit source remains valid outside Atlas
optimizer generation zero to candidate one
cursor generation zero to candidate one
nonzero generation progression
batch size one
batch size greater than one
uniform row lengths
mixed row lengths with right padding
assistant-only loss mask distinct from attention mask
explicit per-row position IDs
valid RoPE theta and even rotary dimension
transaction deterministic replay
writer lease acquire and release
full lineage ID round trip
physical and legacy G206D identities remain distinct
Prepared transaction serialization round trip
relative path normalization
```

## 17.2 Negative controls, minimum 64

Must include:

```text
Atlas route with ExplicitFreshInit
Atlas route with missing checkpoint path
Atlas route with missing checkpoint digest
missing tensor group manifest digest
missing atlas plan digest
missing sequential plan digest
plan checkpoint identity mismatch
model spec digest mismatch

missing row valid lengths
row count not equal to batch size
zero valid length
valid length greater than padded sequence length
left-padding declaration
attention mask derived from target IDs
loss mask used as attention mask
future key admitted
invalid query context not zeroed
missing causal authority

implicit position mode
position count mismatch
non-monotonic valid positions
padded nonzero position
position exceeds model maximum
missing RoPE authority
nonfinite theta
zero theta
odd rotary dimension
rotary dimension greater than head dimension
RoPE applied to V
RoPE model-spec digest mismatch

candidate weight generation not source plus one
candidate optimizer generation not source plus one
candidate cursor generation not source plus one
forward receipt generation mismatch
backward receipt generation mismatch
checkpoint identity mismatch
atlas schedule mismatch
runtime bound state without device epoch
runtime bound state without queue epoch

Atlas generic attention explicit request
Auto executor variant attempt
fallback policy other than FailClosed
Atlas HybridTrainModel construction
Atlas AshModel::new construction
silent Headwise-unavailable fallback

second writer lease
orchestrator writer owner
backend writer owner
same transaction published twice
illegal Prepared to LossSealed transition
illegal Prepared to Committed transition
receipt digest mutation

bare G206D parent field
legacy G206D decision marked as physical parent
legacy G197D type reused as live transaction
physical G206D module mutation
physical G206D shader mutation

GPU device creation
GPU buffer creation
queue submission
forward execution
loss execution
backward execution
optimizer execution
weight write
optimizer-state write
cursor write
pointer swap
checkpoint write
route promotion
decode mutation
```

---

# 18. Dedicated verification gate

Binary:

```text
ash_basetrain_atlas_wave_00_verification_gate
```

The gate must validate:

```text
parent G206D physical PASS identity
full patch lineage disambiguation
model-source route matrix
batch sequence metadata construction
causal and padding semantic fixtures
explicit position authority
RoPE authority binding to ModelSpec
same-generation fence
transaction deterministic sealing
single writer lease
Prepared-only transition ceiling
Atlas route source closure
legacy G197D byte preservation
physical G206D byte preservation
zero mutation firewall
artifact atomic write and readback
```

The gate does not request a GPU adapter and does not initialize Burn or Native WGPU.

Required zero observations:

```text
request_adapter call count
request_device call count
NativeWgpuRuntimeHandles bootstrap count
Burn model construction count
shader module creation count
queue submit count
```

---

# 19. CLI contract

Response file:

```text
specs/cli/ash_basetrain_atlas_wave_00.args
```

Required keys:

```text
--repo-root
.

--patch-id
ASH-BASETRAIN-ATLAS-WAVE-00

--expected-build-revision
ATLAS-WAVE-00-training-step-transaction-ssot-v1

--physical-parent-patch-id
ASH-BASETRAIN-G206D-ISOLATED-WEIGHT-DELTA-MATERIALIZATION-01

--physical-parent-runtime-artifact
workspace/runtime/basetrain/g206d/ash_basetrain_g206d_physical_runtime_artifact.json

--physical-parent-local-manifest
workspace/runtime/basetrain/g206d/ash_basetrain_g206d_physical_local_manifest.json

--legacy-audit-step-patch-id
ASH-BASETRAIN-GPU-70K-G197D

--legacy-70k-decision-patch-id
ASH-BASETRAIN-GPU-70K-G206D

--require-checkpoint-atlas-source
true

--require-explicit-sequence-authority
true

--require-same-generation-fence
true

--require-explicit-position-ids
true

--require-rope-authority
true

--deny-atlas-random-init
true

--deny-atlas-generic-attention
true

--deny-forward
true

--deny-backward
true

--deny-optimizer
true

--deny-weight-mutation
true

--out-dir
workspace/runtime/basetrain/atlas_wave/00
```

Direct execution:

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_00_verification_gate `
  -- `
  "@specs/cli/ash_basetrain_atlas_wave_00.args"
```

---

# 20. PASS, HOLD, and FAIL semantics

## 20.1 Verification PASS token

```text
PASS_ASH_BASETRAIN_ATLAS_WAVE_00_TRAINING_STEP_TRANSACTION_SSOT_CAUSAL_PADDING_POSITION_ROPE_AUTHORITY_SAME_GENERATION_FENCE_ATLAS_ROUTE_RANDOM_INIT_REJECTION_NO_GENERIC_ATTENTION_FALLBACK_LEGACY_G206D_NAMESPACE_DISAMBIGUATION_LEGACY_G197D_AUDIT_CONTRACT_PRESERVATION_PREPARED_ONLY_NO_GPU_NO_FORWARD_NO_LOSS_NO_BACKWARD_NO_OPTIMIZER_NO_DELTA_MATERIALIZATION_NO_WEIGHT_WRITE_NO_OPTIMIZER_STATE_WRITE_NO_CURSOR_WRITE_NO_POINTER_SWAP_NO_CHECKPOINT_WRITE_NO_ROUTE_PROMOTION_NO_DECODE_MUTATION_SEALED
```

## 20.2 Runtime preparation HOLD token

```text
HOLD_ASH_BASETRAIN_ATLAS_WAVE_00_FORWARD_WAVE_NOT_YET_ADMITTED
```

## 20.3 FAIL token

```text
FAIL_ASH_BASETRAIN_ATLAS_WAVE_00_STEP_TRANSACTION_OR_SEQUENCE_AUTHORITY_OR_GENERATION_FENCE_OR_ROUTE_REJECTION_OR_NAMESPACE_SEAL_INVALID
```

PASS and HOLD are not interchangeable.

```text
verification gate PASS
  -> implementation contract is valid

Atlas training invocation HOLD
  -> prepared transaction exists, but AW-01/AW-02 execution authority is absent
```

---

# 21. Completion state

After AW-00 PASS:

```text
BaseTrain Atlas Wave step transaction
  SchemaBound
  SingleWriterBound
  PreparedOnly

AtlasGroupedSequential model source
  CheckpointIdentityBound
  RandomInitForbidden
  WeightPayloadLoadDeferredToAW01

Sequence geometry
  CausalAuthorityBound
  PaddingAuthorityBound
  PositionAuthorityBound
  RoPEAuthorityBound
  HostSealed
  GPUUnbound

Generation fence
  SourceGenerationsBound
  CandidateGenerationsPredeclared
  RuntimeDeviceUnbound
  MixedGenerationForbidden

Attention executor
  HeadwiseTrainPrefillRequired
  GenericFallbackForbidden
  ExecutionNotYetAdmitted

Legacy contracts
  G197DAuditStepPreserved
  Gpu70kG206dDecisionIdentityDistinct
  PhysicalG206dDeltaIdentityDistinct
```

AW-00 does not claim:

```text
checkpoint payload resident
same-device runtime lease acquired
Headwise training forward executed
TensorCube training forward executed
causal mask physically applied on GPU
RoPE physically applied on GPU
loss finite
backward finite
optimizer candidate valid
G206D delta live-adopted
weight generation advanced
training loop closed
```

---

# 22. Next patch handoff

Next patch:

```text
ASH-BASETRAIN-ATLAS-WAVE-01

Existing Native Runtime Handle Borrow /
Safetensors Slice-to-Atlas Residency /
Triple-Ring Lease /
Prepared Transaction Runtime Bind /
Same Device·Queue Epoch /
No Secondary Device Seal
```

AW-01 consumes:

```text
step_transaction_receipt.digest
model_source_authority_receipt.digest
generation_fence_receipt.digest
atlas_schedule_digest
checkpoint_digest
```

AW-01 may transition:

```text
runtime_binding_state
  UnboundPrepared -> BoundSameDevice
```

AW-01 still must not enter `ForwardWaveActive`. That transition belongs to the first live Headwise training-forward patch.

---

# 23. Final gate summary

```text
canonical live transaction type                 BaseTrainAtlasWaveStepTransaction
transaction live owner                          BaseTrainAtlasWaveStepCoordinator
legacy G197D transaction reuse                  forbidden
Atlas random initialization                     forbidden
Atlas generic attention                         forbidden
causal authority                                required
padding authority                               required
explicit position IDs                           required
RoPE authority                                  required
source-generation fence                         required
candidate generations                           source + 1
runtime device/queue                            unbound in AW-00
maximum admitted state                          Prepared
GPU execution                                   0
forward/loss/backward                           0 / 0 / 0
optimizer/delta/apply/commit                    0 / 0 / 0 / 0
resident mutation                               0
namespace ambiguity                             0
```

`ASH-BASETRAIN-ATLAS-WAVE-00` is complete only when the Atlas route can no longer accidentally become a random, unmasked Burn training route, and when every future training kernel is forced to present the same immutable transaction, sequence-authority, and generation-fence digests before execution.
