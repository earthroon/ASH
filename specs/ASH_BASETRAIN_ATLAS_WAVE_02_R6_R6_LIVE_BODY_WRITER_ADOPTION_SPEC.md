# ASH-BASETRAIN-ATLAS-WAVE-02-R6-R6

## Canonical Shared-Runtime Live Body Writer Adoption / Unified Actual Layer-0 DecoderBlock / Actual Attention Writer Switch / Single QKV + Single OProj / Residual + Post-Attn Norm + SwiGLU MLP / Layer-1 Hidden Authority Commit / Headwise Rollback-Only / No Shadow Writer Seal

> Patch ID: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R6`  
> Build revision: `canonical-shared-runtime-live-layer0-body-writer-v1`  
> Direct physical parent: `ASH-BASETRAIN-ATLAS-WAVE-02-R6-R5-C7`  
> Parent PASS token: `PASS_ASH_BASETRAIN_ATLAS_WAVE_02_R6_R5_CANONICAL_BODY_SHARED_RUNTIME_REBASE_..._SEALED`  
> BaseTrain live-route admission target: `ADMITTED`  
> Production inference admission: `BLOCKED`  
> Backward/optimizer admission: `BLOCKED`  
> Proof ledger before physical run: `HOLD`

---

# 0. Correction seal

R6-R6 is **not** a shadow body-output patch.

The shared W5/W6/W7 runtime becomes the selected BaseTrain FullPrefill layer-0 attention writer. Its context is consumed by the actual layer-0 body, its final decoder-block hidden state is committed once, and that committed hidden state becomes the canonical layer-1 input lease.

```text
forbidden interpretation:
  shared runtime computes a body-shaped candidate
  Headwise remains the real writer
  shared result is compared and discarded

required interpretation:
  shared runtime is selected before execution
  shared result enters the actual layer-0 decoder block continuation
  final layer-0 hidden is committed once
  committed output is published as layer-1 input authority
```

Headwise is retained as an explicit rollback writer only. It is not executed as a mandatory parallel writer on the live hot path.

---

# 1. Parent SSOT

R6-R6 requires the physical R6-R5-C7 result, not merely source presence.

Required parent evidence:

```text
R6-R5 physical gate = PASS
shared Stage10 dispatch count = 2
shared Stage11 dispatch count = 1
shared Stage12 dispatch count = 4
three context comparison pairs = PASS
context mismatch count = 0
three actual OProj comparison pairs = PASS
OProj mismatch count = 0
context payload readback count = 0
OProj payload readback count = 0
writer mutation count = 0
```

The R6-R5 parent proves that the shared W5/W6/W7 context is numerically equivalent to the Headwise and R6 reference contexts and that the existing actual checkpoint OProj produces equivalent output.

R6-R6 changes the authority and body-consumption boundary. It does not reopen the Stage10/11/12 formulas.

---

# 2. Scope decision

## 2.1 Admitted route

```text
subsystem = BaseTrain
route = FullPrefill
selected layer = 0
batch = 1
sequence length = 32
query heads = 32
KV heads = 4
head dimension = 64
hidden size = 2048
```

## 2.2 Actual live boundary

R6-R6 executes and commits:

```text
input hidden
input RMSNorm
Q projection
K projection
V projection
shared W5/W6/W7 attention
actual O projection
attention residual add
post-attention RMSNorm
SwiGLU gate projection
SwiGLU up projection
SiLU(gate) * up
MLP down projection
FFN residual add
layer-1 hidden publication
```

## 2.3 Not admitted

```text
layer > 0 shared-runtime writer adoption
incremental decode writer adoption
chunked decode writer adoption
production inference default-route mutation
backward graph
optimizer step
weight mutation
checkpoint mutation
automatic silent fallback
```

---

# 3. Authority model

The existing `ProductionAttentionOutputAuthoritySlot` is Headwise-specific and belongs to production inference. R6-R6 must not repurpose its `HeadwiseFullActive` state or silently rename a TensorCube writer as Headwise.

R6-R6 introduces a BaseTrain-specific live route authority.

```rust
pub enum BaseTrainLayerAttentionWriter {
    Headwise,
    SharedRuntimeW5W6W7,
}

pub enum BaseTrainLayerRouteState {
    HeadwiseLive,
    SharedRuntimeLive,
    RollbackRequired,
}
```

Canonical authority key:

```text
(model_instance_id, training_session_id, route_id, layer_index)
```

First admitted key:

```text
route_id = FullPrefill
layer_index = 0
```

The authority pointer records:

```text
schema
model instance ID
training session ID
route ID
layer index
state
writer ID
generation
R6-R5 parent manifest digest
R6-R5 physical PASS receipt digest
actual decoder-block identity digest
checkpoint tensor-set digest
runtime LoRA-set digest
operation ID
previous pointer digest
pointer digest
```

## 3.1 Allowed transition

```text
HeadwiseLive
  -> SharedRuntimeLive
```

Requirements:

```text
active invocation count = 0
R6-R5 physical PASS verified
writer eligibility receipt verified
input-hidden authority uncommitted
no pending rollback operation
new generation = previous generation + 1
previous pointer digest exact match
```

## 3.2 Rollback transition

```text
SharedRuntimeLive
  -> RollbackRequired
  -> HeadwiseLive
```

Rollback is explicit. No failed shared-runtime invocation may silently execute Headwise and commit under the same operation ID.

The failed invocation emits a rollback-required receipt and exits without layer-hidden commit. A subsequent invocation may execute Headwise after the authority transition is complete.

---

# 4. One actual decoder-block instance

R6-R5 used an actual standalone `AshLinear` OProj module for parity. R6-R6 must replace that split surface with one actual checkpoint-backed layer-0 `AshDecoderBlock<InferenceBackend>` instance.

The instance owns:

```text
layers.0.input_norm
layers.0.attn.q_proj
layers.0.attn.k_proj
layers.0.attn.v_proj
layers.0.attn.o_proj
layers.0.post_attn_norm
layers.0.ffn.gate_proj
layers.0.ffn.up_proj
layers.0.ffn.down_proj
```

Checkpoint source keys:

```text
model.layers.0.input_layernorm.weight
model.layers.0.self_attn.q_proj.weight
model.layers.0.self_attn.k_proj.weight
model.layers.0.self_attn.v_proj.weight
model.layers.0.self_attn.o_proj.weight
model.layers.0.post_attention_layernorm.weight
model.layers.0.mlp.gate_proj.weight
model.layers.0.mlp.up_proj.weight
model.layers.0.mlp.down_proj.weight
```

Required counts:

```text
actual decoder-block instance count = 1
checkpoint tensor payload read count = 9
checkpoint weight upload count = 9
standalone OProj module count = 0
duplicate layer module count = 0
synthetic weight count = 0
```

The same prepared runtime LoRA set is bound once to all seven linear projections.

```text
runtime LoRA set construction count = 1
runtime LoRA target binding count = 7
trainable LoRA slot count = 0
```

---

# 5. Split-forward API

`AshDecoderBlock::forward_prepared_set()` cannot be reused directly because it owns the internal generic attention calculation. R6-R6 adds a split-forward API whose body semantics remain identical to the existing block.

## 5.1 Attention preparation

```rust
pub struct PreparedLiveAttentionInput<B: Backend> {
    pub residual: Tensor<B, 3>,
    pub normalized_hidden: Tensor<B, 3>,
    pub q_bqhd: Tensor<B, 4>,
    pub k_bqhd: Tensor<B, 4>,
    pub v_bqhd: Tensor<B, 4>,
    pub qkv_generation: u64,
    pub source_hidden_generation: u64,
    pub receipt: ActualQkvPreparationReceipt,
}
```

Proposed method:

```rust
pub fn prepare_external_attention_prepared_set(
    &self,
    x: Tensor<B, 3>,
    runtime_loras: &PreparedRuntimeLoraSet<B>,
    trainable_loras: &[TrainableLoraSlot<B>],
) -> PreparedLiveAttentionInput<B>
```

Required behavior:

```text
residual clone count = 1
input_norm dispatch count = 1
Q projection count = 1
K projection count = 1
V projection count = 1
Q/K/V layout = BQHD
Q/K/V host readback count = 0
Q/K/V host upload count = 0
```

## 5.2 Body continuation from external context

```rust
pub struct LiveDecoderBlockOutput<B: Backend> {
    pub after_attention: Tensor<B, 3>,
    pub normalized_ffn_input: Tensor<B, 3>,
    pub final_hidden: Tensor<B, 3>,
    pub receipt: LiveDecoderBlockContinuationReceipt,
}
```

Proposed method:

```rust
pub fn continue_from_external_preoproj_context_prepared_set(
    &self,
    residual: Tensor<B, 3>,
    context_bqhd: Tensor<B, 4>,
    runtime_loras: &PreparedRuntimeLoraSet<B>,
    trainable_loras: &[TrainableLoraSlot<B>],
) -> LiveDecoderBlockOutput<B>
```

Exact arithmetic:

```text
ctx_bqh = reshape(context_bqhd, [B,Q,H*D])
attn_out = o_proj(ctx_bqh)
after_attention = residual + attn_out
ffn_input = post_attn_norm(after_attention)
gate = SiLU(gate_proj(ffn_input))
up = up_proj(ffn_input)
ff = down_proj(gate * up)
final_hidden = after_attention + ff
```

Required dispatch counts:

```text
OProj = 1
attention residual add = 1
post-attention RMSNorm = 1
gate projection = 1
up projection = 1
SiLU/multiply = 1 fused or equivalent deterministic sequence
down projection = 1
FFN residual add = 1
```

Forbidden:

```text
internal generic grouped_query_attention dispatch
second QKV projection
second OProj dispatch
standalone shadow body calculation
CPU materialization
hidden-state host roundtrip
```

---

# 6. Actual shared-runtime live route

The live route is:

```text
LayerInputHiddenLease(layer=0, generation=g)
  -> actual layer-0 input_norm + QKV once
  -> PreparedAtlasInputs(input_layout=BQHD)
  -> W4 Texture06 direct pack
  -> W5 Stage10
  -> W6 Stage11 global softmax
  -> W7 Stage12 weighted value
  -> TensorCubeStage12ContextCandidateHandle(BQHD)
  -> same-device Burn context adoption
  -> actual layer-0 body continuation
  -> LiveDecoderBlockOutput.final_hidden
  -> LayerInputHiddenLease(layer=1, generation=g+1)
```

R6-R2/R3/R4 is not executed in the normal live invocation.

Headwise is not executed in the normal live invocation.

Those routes remain admission evidence and rollback implementations, not parallel hot-path writers.

---

# 7. Same-device context adoption

R6-R6 adopts only one context: the selected W7 BQHD live context.

```text
source context count = 1
same-device copy count = 1
source COPY_SRC capability = true
destination COPY_DST capability = true
source and destination device identity equal = true
source and destination queue lineage equal = true
context host readback count = 0
context host upload count = 0
implicit transpose count = 0
zero-copy claim count = 0
```

The physical BQHD tensor shape remains:

```text
[B,Q,H,D]
```

The body continuation performs a metadata reshape to `[B,Q,H*D]`. It must not relabel a BHQD allocation as BQHD.

---

# 8. Layer-hidden state SSOT

R6-R6 introduces a generation-sealed layer-hidden authority.

```rust
pub struct LayerHiddenAuthorityPointer {
    pub model_instance_id: String,
    pub training_session_id: String,
    pub route_id: String,
    pub layer_index: u32,
    pub hidden_generation: u64,
    pub writer_id: String,
    pub buffer_identity_digest: String,
    pub semantic_shape_bqh: [u32; 3],
    pub completion_token_digest: String,
    pub previous_pointer_digest: Option<String>,
    pub pointer_digest: String,
}
```

## 8.1 Input authority

```text
layer_index = 0
shape = [1,32,2048]
writer = token_embedding_or_prior_body_authority
hidden generation = g
```

## 8.2 Output authority

```text
layer_index = 1
shape = [1,32,2048]
writer = SharedRuntimeW5W6W7Layer0Body
hidden generation = g + 1
```

## 8.3 Commit CAS

The final hidden state is committed only after:

```text
shared-runtime authority lease revalidation
input-hidden generation revalidation
W7 completion observed
body continuation completion observed
finite compact guard PASS
shape guard PASS
same-device guard PASS
no previous output commit for operation ID
```

Required:

```text
layer-hidden commit count = 1
layer-hidden generation increment count = 1
layer-hidden duplicate commit count = 0
layer-hidden stale-generation commit count = 0
partial attention-state commit count = 0
partial FFN-state commit count = 0
```

The internal attention residual and FFN residual are tensor arithmetic. The external state mutation is one final layer-hidden CAS.

---

# 9. Live writer semantics

R6-R6 must produce the following receipt values:

```text
selected_attention_writer = SharedRuntimeW5W6W7
selected_body_writer = ActualLayer0AshDecoderBlock
headwise_parallel_dispatch_count = 0
r6_parallel_dispatch_count = 0
shared_context_discard_count = 0
shared_output_commit_count = 1
layer1_hidden_publish_count = 1
```

A result that computes shared output but returns the Headwise result is a failure.

A result that compares shared output and discards it is a failure.

A result that writes both shared and Headwise outputs is a failure.

---

# 10. Admission oracle and gate-only comparison

The R6-R6 physical gate may execute one non-committing reference block to prove final layer output parity before the first live-authority commit.

This comparison is gate-only evidence, not the installed live route.

Reference route:

```text
same input hidden
same actual checkpoint layer-0 block
Headwise or canonical generic attention context
same OProj/post-norm/MLP weights
no LayerHiddenAuthority commit permission
```

Required gate comparison:

```text
shared live final hidden vs reference final hidden
shape = [1,32,2048]
scalar count = 65536
mismatch count = 0
non-finite count = 0
payload readback count = 0
compact comparison status readback only
```

Commit ordering:

```text
1. produce shared live candidate
2. produce non-committing gate reference
3. GPU full-surface compare
4. revalidate live authority lease
5. commit only shared live final hidden
6. publish layer-1 input lease
```

After physical admission, normal live invocations do not require the reference dispatch.

---

# 11. Headwise rollback-only contract

Headwise remains available but is not a co-writer.

```text
normal live invocation:
  Headwise dispatch count = 0

shared live failure before commit:
  layer-hidden commit count = 0
  rollback-required receipt count = 1
  silent Headwise fallback count = 0

subsequent invocation after authority rollback:
  Headwise may execute as selected writer
```

The rollback pointer must reference:

```text
failed operation ID
failed shared-runtime authority generation
last-good Headwise authority pointer digest
input-hidden generation preserved for replay
failure stage
failure receipt digest
```

No rollback is permitted after the layer-1 hidden commit has succeeded.

---

# 12. Weight and module authority

R6-R6 selects the nine layer-0 body tensors from the existing R5-R6 checkpoint tensor-set authority.

Required tensor roles:

```text
input_layernorm
self_attn_q_proj
self_attn_k_proj
self_attn_v_proj
self_attn_o_proj
post_attention_layernorm
mlp_gate_proj
mlp_up_proj
mlp_down_proj
```

Validation:

```text
selected layer = 0
all tensor identity digests present
all shard digests match checkpoint authority
all shapes match production config
all dtypes identical to checkpoint canonical dtype
payload mutation count = 0
weight upload authorization = true
weight mutation authorization = false
```

Expected shapes for the current profile:

```text
input norm = [2048]
Q = [2048,2048]
K = [256,2048]
V = [256,2048]
O = [2048,2048]
post-attn norm = [2048]
gate = [intermediate_size,2048]
up = [intermediate_size,2048]
down = [2048,intermediate_size]
```

---

# 13. Runtime LoRA boundary

R6-R6 preserves the actual body runtime LoRA binding surface.

```text
prepared runtime LoRA set = one SSOT
Q/K/V/O/gate/up/down bind from same set
fixture runtime LoRA attachment count = 0
trainable LoRA slot count = 0
LoRA payload mutation count = 0
```

No projection may silently construct an empty local set if a prepared set has already been supplied.

---

# 14. Finite and completion guard

Before layer-hidden commit, the final hidden output must pass a GPU guard.

Required checks:

```text
expected element count = 65536
non-finite count = 0
first non-finite index = NONE
completion token observed = true
same-device output identity = true
output buffer covers expected byte range = true
compact guard readback bytes <= 256
output payload readback count = 0
```

The guard may reject the commit. It may not repair or clamp values.

---

# 15. Determinism and replay

The physical gate executes the same live operation twice without committing the second execution.

```text
first execution = commit candidate
second execution = deterministic replay witness
```

Required:

```text
same input-hidden authority digest
same checkpoint tensor-set digest
same runtime LoRA-set digest
same QKV source generation
same atlas residency generation
same W5/W6/W7 result digest
same final hidden digest
full-surface replay mismatch count = 0
second layer-hidden commit count = 0
```

The replay cannot acquire a new writer generation or mutate the output pointer.

---

# 16. Failure atomicity

Failure before final commit must leave:

```text
layer-0 input hidden authority unchanged
layer-1 hidden authority absent
writer pointer either unchanged or explicitly RollbackRequired
checkpoint unchanged
weights unchanged
LoRA unchanged
optimizer unchanged
```

Forbidden:

```text
commit after incomplete W7 context
commit after partial MLP
commit before finite guard
commit under stale writer lease
commit under stale input-hidden generation
commit both shared and Headwise outputs
catch error and silently return Headwise output
```

---

# 17. Baked source changes

## 17.1 Model core

```text
crates/model_core/src/headwise_texture_06_live_binding.rs
crates/model_core/src/base_train_atlas_wave_02_r6_r5_body_splice.rs
crates/model_core/src/base_train_layer_attention_authority.rs
crates/model_core/src/actual_decoder_block_split_forward.rs
crates/model_core/src/lib.rs
```

The split-forward methods are implemented as an extension `impl` in
`actual_decoder_block_split_forward.rs`. Existing `model_layers.rs` `forward()` and
`forward_prepared_set()` semantics remain unchanged.

The W4 execution boundary is generalized through `AttentionExecutionAuthorityLease`.
R6-R5 continues to use the existing production-authority lease, while R6-R6 supplies
a BaseTrain-specific shared-live lease. No synthetic production pointer is created.

`base_train_layer_attention_authority.rs` owns both:

```text
BaseTrain layer attention writer authority
actual Burn Tensor-backed layer-hidden authority
operation-ID duplicate commit registry
rollback-required transition receipt
```

The layer-hidden authority stores the actual committed `Tensor<InferenceBackend, 3>`.
A pointer-only publication without tensor ownership is forbidden.

## 17.2 Base train

```text
crates/base_train/src/base_train_atlas_wave_02_r6_r6_authority.rs
crates/base_train/src/lib.rs
```

The authority loader selects and decodes the nine actual checkpoint tensors. Gate
receipts are emitted directly by the physical gate so no parallel receipt authority
module is introduced.

## 17.3 Backend

```text
crates/burn_webgpu_backend/src/base_train_atlas_wave_02_r6_r6_live_body.rs
crates/burn_webgpu_backend/src/lib.rs
```

This module owns the embedding-only live input stage and the actual NeoX BQHD RoPE
stage. Existing `HeadwiseFiniteGuard` and `HeadwiseOutputParityPipeline` are reused
for `[B,Q,H]` finite guarding, full-surface final-hidden comparison, deterministic
replay comparison and publication comparison. No duplicate WGSL is introduced.

## 17.4 Gate and CLI

```text
crates/orchestrator_local/src/bin/ash_basetrain_atlas_wave_02_r6_r6_live_body_writer_gate.rs
crates/orchestrator_local/Cargo.toml
specs/cli/ash_basetrain_atlas_wave_02_r6_r6.args
```

---

# 18. Commit sequence

## R6-R6-C0: Authority decision record

```text
BaseTrain route ownership separated from production inference authority
FullPrefill layer-0 route key fixed
SharedRuntimeLive state defined
Headwise rollback-only state defined
no global Headwise pointer repurposing
```

## R6-R6-C1: Unified actual decoder-block authority

```text
nine checkpoint tensors selected
one AshDecoderBlock instance created
one prepared runtime LoRA set bound
standalone R6-R5 OProj module retired from the R6-R6 route
```

## R6-R6-C2: Split-forward body API

```text
prepare external attention QKV
continue from external pre-OProj context
existing full forward unchanged
formula parity tests added
```

## R6-R6-C3: Shared-runtime live route

```text
actual QKV single source
W5/W6/W7 selected writer
one W7 context adoption
actual body continuation
no Headwise/R6 parallel hot-path dispatch
```

## R6-R6-C4: Layer-hidden authority CAS

```text
layer-0 input lease
layer-1 output pointer
single commit
stale generation rejection
idempotent operation registry
```

## R6-R6-C5: Final-hidden guard and gate parity

```text
non-finite guard
full-surface final-hidden compare
compact status readback
reference output non-committing
shared output committed
```

## R6-R6-C6: Explicit rollback contract

```text
rollback-required receipt
no same-invocation silent fallback
Headwise selected only after pointer transition
failed invocation commits nothing
```

## R6-R6-C7: Physical live-body gate

```text
seq32 layer0 actual run
deterministic replay
one layer1 hidden commit
PASS token and manifest seal
```

---

# 19. CLI policy

Required true gates:

```text
--require-r6-r5-physical-pass
--require-unified-actual-decoder-block
--require-shared-runtime-live-writer
--require-single-qkv-projection
--require-single-oproj-dispatch
--require-post-attn-norm
--require-actual-swiglu-mlp
--require-single-layer-hidden-commit
--require-layer1-hidden-publication
--require-headwise-hotpath-zero
--require-r6-hotpath-zero
--require-no-silent-fallback
--require-output-payload-readback-zero
--require-checkpoint-mutation-zero
--require-weight-mutation-zero
--require-backward-zero
--require-optimizer-zero
```

Required false allowances:

```text
--allow-shadow-body-output false
--allow-parallel-headwise-writer false
--allow-parallel-r6-writer false
--allow-duplicate-qkv false
--allow-duplicate-oproj false
--allow-same-invocation-fallback false
--allow-partial-layer-hidden-commit false
--allow-production-inference-route-mutation false
```

Output directory:

```text
workspace/runtime/basetrain/atlas_wave/02/r6_r6/live-layer0-body-writer-v1
```

---

# 20. Required receipts

```text
00_parent_r6_r5_c7_physical_pass
01_base_train_route_authority_before
02_shared_runtime_live_writer_promotion
03_actual_layer0_decoder_block_authority
04_layer0_input_hidden_authority
05_actual_qkv_single_source
06_w4_texture06_live_pack
07_w5_stage10_live_statistics
08_w6_stage11_live_softmax
09_w7_stage12_live_context
10_context_same_device_adoption
11_actual_body_continuation
12_final_hidden_finite_guard
13_gate_reference_noncommitting
14_final_hidden_full_surface_parity
15_live_authority_revalidation
16_layer1_hidden_commit
17_layer1_hidden_publication
18_deterministic_replay
19_headwise_hotpath_zero
20_failure_atomicity
21_live_body_writer_final
```

---

# 21. Final receipt fields

```text
patch_id
build_revision
selected_layer
route_id
parent_r6_r5_manifest_digest
parent_r6_r5_pass_receipt_digest
checkpoint_tensor_set_digest
actual_decoder_block_identity_digest
runtime_lora_set_digest
input_hidden_authority_digest
input_hidden_generation
selected_attention_writer
selected_body_writer
actual_qkv_projection_count
shared_stage10_dispatch_count
shared_stage11_dispatch_count
shared_stage12_dispatch_count
same_device_context_copy_count
actual_oproj_dispatch_count
attention_residual_add_count
post_attn_norm_dispatch_count
gate_proj_dispatch_count
up_proj_dispatch_count
silu_multiply_dispatch_count
down_proj_dispatch_count
ffn_residual_add_count
headwise_hotpath_dispatch_count
r6_hotpath_dispatch_count
reference_gate_dispatch_count
final_hidden_compared_scalar_count
final_hidden_mismatch_count
final_hidden_nonfinite_count
output_payload_readback_count
layer_hidden_commit_count
layer_hidden_generation_increment_count
layer1_hidden_publish_count
silent_fallback_count
rollback_required_receipt_count
backward_dispatch_count
optimizer_step_count
weight_mutation_count
checkpoint_mutation_count
base_train_live_admission
production_inference_admission
proof_ledger_admission
pass
receipt_digest
```

Required terminal values:

```text
selected_attention_writer = SharedRuntimeW5W6W7
selected_body_writer = ActualLayer0AshDecoderBlock
actual_qkv_projection_count = 1
actual_oproj_dispatch_count = 1
attention_residual_add_count = 1
post_attn_norm_dispatch_count = 1
gate_proj_dispatch_count = 1
up_proj_dispatch_count = 1
silu_multiply_dispatch_count = 1
down_proj_dispatch_count = 1
ffn_residual_add_count = 1
headwise_hotpath_dispatch_count = 0
r6_hotpath_dispatch_count = 0
final_hidden_compared_scalar_count = 65536
final_hidden_mismatch_count = 0
final_hidden_nonfinite_count = 0
output_payload_readback_count = 0
layer_hidden_commit_count = 1
layer_hidden_generation_increment_count = 1
layer1_hidden_publish_count = 1
silent_fallback_count = 0
backward_dispatch_count = 0
optimizer_step_count = 0
weight_mutation_count = 0
checkpoint_mutation_count = 0
base_train_live_admission = ADMITTED
production_inference_admission = BLOCKED
proof_ledger_admission = HOLD
```

---

# 22. Cargo commands

Type-check:

```powershell
cargo check `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r6_live_body_writer_gate
```

Physical live-body gate:

```powershell
cargo run --release `
  --manifest-path crates/orchestrator_local/Cargo.toml `
  --features orchestrator_tcu_audit_bins `
  --bin ash_basetrain_atlas_wave_02_r6_r6_live_body_writer_gate `
  -- "@specs/cli/ash_basetrain_atlas_wave_02_r6_r6.args"
```

---

# 23. PASS token

```text
PASS_ASH_BASETRAIN_ATLAS_WAVE_02_R6_R6_CANONICAL_SHARED_RUNTIME_LIVE_BODY_WRITER_ADOPTION_R6_R5_C7_PHYSICAL_PASS_PARENT_UNIFIED_ACTUAL_LAYER0_ASH_DECODER_BLOCK_SINGLE_CHECKPOINT_TENSOR_SET_SINGLE_RUNTIME_LORA_SET_SINGLE_INPUT_NORM_SINGLE_QKV_PROJECTION_W4_BQHD_TEXTURE06_DIRECT_PACK_W5_STAGE10_W6_STAGE11_W7_STAGE12_SELECTED_LIVE_ATTENTION_WRITER_SINGLE_SAME_DEVICE_CONTEXT_ADOPTION_SINGLE_ACTUAL_OPROJ_ATTENTION_RESIDUAL_POST_ATTN_RMSNORM_ACTUAL_SWIGLU_GATE_UP_SILU_MULTIPLY_DOWN_FFN_RESIDUAL_LAYER1_HIDDEN_SINGLE_GENERATION_COMMIT_AND_PUBLICATION_HEADWISE_AND_R6_HOTPATH_ZERO_REFERENCE_GATE_NONCOMMITTING_FINAL_HIDDEN_FULL_SURFACE_PARITY_ZERO_MISMATCH_NONFINITE_ZERO_PAYLOAD_READBACK_ZERO_NO_SHADOW_BODY_OUTPUT_PARALLEL_WRITER_DUPLICATE_QKV_DUPLICATE_OPROJ_SILENT_FALLBACK_PARTIAL_COMMIT_BACKWARD_OPTIMIZER_WEIGHT_OR_CHECKPOINT_MUTATION_BASETRAIN_LIVE_ADMITTED_PRODUCTION_INFERENCE_BLOCKED_PROOF_LEDGER_HOLD_SEALED
```

---

# 24. Final seal

```text
R6-R6 is the point where the shared W5/W6/W7 attention path stops being a compared candidate and becomes the actual BaseTrain FullPrefill layer-0 writer.

One actual checkpoint-backed AshDecoderBlock owns the layer. It prepares QKV once, accepts the selected shared-runtime BQHD context, executes OProj, both residual additions, post-attention RMSNorm and the actual SwiGLU MLP, then atomically publishes the resulting [1,32,2048] hidden state as the layer-1 input authority.

Headwise is not a parallel writer and is not silently invoked on failure. It remains an explicit rollback route selected only by a generation-sealed authority transition. Production inference and backward remain outside this patch.
```
