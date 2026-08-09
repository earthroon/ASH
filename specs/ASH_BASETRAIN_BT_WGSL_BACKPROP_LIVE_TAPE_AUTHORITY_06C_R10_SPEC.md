# ASH-BASETRAIN-BT-WGSL-BACKPROP-LIVE-TAPE-AUTHORITY-06C-R10

## R6-R9 C9 Exact Physical Forward Parent / No Parallel Training Decoder Reconstruction / Canonical Resident Weight Authority Reuse / Selected Top-N Forward Tape Capture / Input RMSNorm Tape / Pre·Post NeoX QK Tape / Canonical V Lease / Stage11 Global Softmax State Retention / Stage12 Context Lease / OProj Input·Output Tape / Post-RMSNorm Tape / SwiGLU Gate·Up·Product Tape / Final Hidden Tape / Layer·Generation·Weight-Pointer Lineage / Backward Owner Lease / Reverse Residency Preparation / Zero Checkpoint Reopen / Zero TrainingBackend Selected-Decoder Clone / Zero Payload Readback / Backward Dispatch = 0 / Optimizer = 0 / Weight Mutation = 0 Seal

> Patch ID: `ASH-BASETRAIN-BT-STRUCTURAL-LOOKAHEAD-DECODER-COUPLING-06C-R10`
>
> Build revision: `bt-wgsl-backprop-live-tape-authority-06c-r10`
>
> Physical parent: R06B structural heads → R6-R9 C10 health → exact R6-R9 C9 progressive live decoder execution
>
> Proof ledger: `HOLD`

---

## 1. Purpose

R10 does not execute decoder backward, optimizer, or parameter mutation.

R10 changes the selected-decoder training authority from the R9 parallel `TrainingBackend` decoder reconstruction path to the already admitted R6-R9 physical live decoder forward path.

The patch captures the selected top-N layer forward intermediates as same-device GPU-resident backward tape and binds every tape to the exact live weight, hidden, layer, generation, pointer, and completion lineage that produced it.

The next backward patch must consume this tape. It may not rebuild an independent selected decoder or reopen selected-layer checkpoint payloads to reproduce the forward graph.

---

## 2. Authority transition

### R9 active route retired

The following R9 selected-decoder execution model is no longer an active 06C authority:

```text
checkpoint tensor lookup
→ checkpoint decode to Vec<f32>
→ Tensor<TrainingBackend>::from_data
→ AshDecoderBlock<TrainingBackend> reconstruction
→ parallel selected-layer forward
→ Burn/autodiff decoder backward
```

R10 final receipt requires:

```text
trainingDecoderCloneCount = 0
parallelTrainingDecoderForwardCount = 0
additionalCheckpointReadCount = 0
additionalCheckpointDecodeCount = 0
```

### R10 canonical route

```text
R6-R9 C9 physical progressive decoder
→ resident weight slot
→ canonical live layer execution
→ selected top-N capture policy
→ same-device raw forward tape
→ retained Stage11 / Stage12 handles
→ R10 tape authority receipt
```

There is exactly one selected decoder forward authority.

---

## 3. Parent requirements

R10 requires both:

```text
PASS_ASH_BASETRAIN_BT_STRUCTURAL_MEDUSA_HEADS_06B_...
PASS_ASH_BASETRAIN_ATLAS_WAVE_02_R6_R9_C9_...
```

R10 obtains C9 through the existing R06B decoder parent chain and verifies the C9 final receipt and pass token before publishing tape authority.

R10 does not create an alternate C9 session.

---

## 4. Selected top-N capture

The existing 06C CLI authority:

```text
--bt-struct-lookahead-top-n
```

determines tape capture scope.

Given:

```text
checkpointLayerCount = L
selectedTopN = N
```

R10 derives:

```text
selectedLayerStart = L - N
selectedLayerEnd = L - 1
```

C9 captures tape only when:

```text
executedLayer >= selectedLayerStart
```

Required:

```text
capturedLayerTapeCount = N
forwardOrder = [selectedLayerStart ... selectedLayerEnd]
```

All earlier layers remain canonical live forward-only layers.

No all-layer backward tape retention is admitted by this patch.

---

## 5. Canonical tape types

R10 introduces:

```rust
R6R8SelectedDecoderForwardTapeMetadata
R6R8SelectedDecoderForwardTape
```

The tape is owned by the C9 progressive execution object and remains reachable through the R06B/C10 parent chain during the 06C R10 gate.

### Metadata

Each selected-layer tape seals:

```text
schema_version
selected_layer
weight_generation
weight_pointer_digest
weight_transition_serial
decoder_block_identity_digest
input_hidden_generation
input_hidden_pointer_digest
output_hidden_generation
output_hidden_pointer_digest
raw_borrow_lease_count
stage11_state_record_count
stage11_state_record_bytes
stage12_context_element_count
backward_owner_id
payload_readback_count
host_upload_count
backward_dispatch_count
optimizer_count
weight_mutation_count
tape_digest
```

The tape therefore cannot be identified by layer index alone.

---

## 6. Input RMSNorm tape

`AshRmsNorm` gains a single-computation tape-producing forward:

```rust
forward_with_tape(x) -> (normalized, inverse_rms)
```

The normal `forward()` delegates to this implementation and returns `.0`.

The selected live-body tape retains:

```text
input_hidden
input_rms_inv
normalized_hidden
```

The tape path does not execute a second RMSNorm pass.

Required semantic count:

```text
inputRmsTapeCount = selectedTopN
```

---

## 7. QKV and NeoX tape

The canonical live decoder QKV preparation remains the only QKV projection execution.

R10 retains:

```text
q_pre_rope
k_pre_rope
canonical_v
q_post_rope
k_post_rope
```

`canonical_v` is a single V lease derived from the live QKV preparation.

R10 does not create per-horizon V or K copies.

The future structural branch backward must continue to treat K/V as shared canonical authority.

---

## 8. Stage11 global softmax-state retention

The existing Stage11 handle gains a backward-tape clone operation:

```rust
TensorCubeStage11GlobalSoftmaxStateHandle::clone_for_backward_tape(...)
```

The clone:

- shares the same `Arc<Buffer>` candidate/oracle global-state allocations,
- preserves partition and submission lineage,
- does not copy the GPU payload,
- extends ownership through a backward-tape owner resource ID.

Required:

```text
state_record_bytes = 16
completion_observed = true
owner_resource_ids contains "backward-tape"
```

The canonical Stage12 consumer may finish and drain its original ownership path while the backward tape retains the shared GPU allocation.

No Stage11 CPU reconstruction is admitted.

---

## 9. Stage12 context retention

The existing Stage12 context handle gains:

```rust
TensorCubeStage12ContextCandidateHandle::clone_for_backward_tape(...)
```

It retains the canonical candidate context buffer by `Arc` without payload duplication.

Required:

```text
completion_observed = true
owner_resource_ids contains "backward-tape"
stage12ContextTapeCount = selectedTopN
```

The future OProj backward path must consume this canonical context lineage.

---

## 10. OProj / post-attention tape

The canonical live continuation now exposes without extra forward dispatch:

```text
oproj_output
after_attention
```

The existing attention residual addition remains authoritative.

No second OProj execution is introduced for tape capture.

---

## 11. Post-RMSNorm tape

The same `forward_with_tape` RMSNorm implementation is used for the post-attention norm.

R10 retains:

```text
after_attention
post_rms_inv
normalized_ffn_input
```

Required:

```text
postRmsTapeCount = selectedTopN
```

No post-RMSNorm recomputation is introduced.

---

## 12. SwiGLU tape

The canonical live continuation now explicitly preserves:

```text
gate_linear_pre_activation
silu_gate
up_linear
ffn_product
down_output
final_hidden
```

The live forward arithmetic remains:

```text
gate_linear = GateProj(normalized_ffn_input)
silu_gate = SiLU(gate_linear)
up_linear = UpProj(normalized_ffn_input)
ffn_product = silu_gate * up_linear
down_output = DownProj(ffn_product)
final_hidden = after_attention + down_output
```

The additional fields are retained intermediate values, not duplicate dispatches.

---

## 13. Raw borrowed GPU lease contract

All tensor surfaces captured by R10 are converted through the existing strict live bridge.

Each captured tensor must produce:

```text
BridgeMode::RawBorrowed
```

The R10 tape currently contains 18 raw tensor leases per selected layer:

```text
1  input_hidden
2  input_rms_inv
3  normalized_hidden
4  q_pre_rope
5  k_pre_rope
6  canonical_v
7  q_post_rope
8  k_post_rope
9  oproj_output
10 after_attention
11 post_rms_inv
12 normalized_ffn_input
13 gate_linear_pre_activation
14 silu_gate
15 up_linear
16 ffn_product
17 down_output
18 final_hidden
```

Stage11 and Stage12 are retained through their native buffer-handle types and are not included in the `raw_borrow_lease_count` value.

Required:

```text
raw_borrow_lease_count = 18 / selected layer
hostUploadCount = 0
payloadReadbackCount = 0
```

---

## 14. Layer / generation / pointer lineage

Tape capture occurs inside the exact C9 canonical resident-layer execution.

Each tape binds:

```text
selected layer
weight residency generation
weight pointer digest
weight transition serial
decoder block identity digest
input hidden generation
input hidden pointer digest
output hidden generation
output hidden pointer digest
```

The 06C R10 gate rejects malformed pointer digests and incorrect selected-layer ordering.

The future reverse residency loader must rebind weights matching this tape lineage rather than reconstructing an independent decoder block.

---

## 15. Backward owner lease semantics

R10 does not keep the live forward weight execution lease open.

The existing R6-R9 weight residency lifecycle remains valid:

```text
execute layer N
→ release execution lease
→ evict N when required
→ adopt N+1
```

Backward tape ownership retains only the intermediate GPU resources needed by later backward dispatches.

Required receipt:

```text
weightExecutionLeaseRetainedCount = 0
hiddenExecutionLeaseRetainedCount = 0
tapeOwnerLeaseCount = selectedTopN
```

This separation prevents R10 from defeating the one-resident-block weight policy.

---

## 16. Reverse residency preparation

R10 prepares but does not execute reverse residency.

For forward order:

```text
[s, s+1, ... L-1]
```

R10 publishes:

```text
[L-1, ... s+1, s]
```

as the future backward residency order.

Required:

```text
reverseResidencyPlanPrepared = true
reverseResidencyExecutionCount = 0
checkpointReadCount = 0
weightMutationCount = 0
```

---

## 17. Zero selected-decoder checkpoint reopen

`Zero Checkpoint Reopen` in R10 means:

> no additional selected-decoder checkpoint lookup/decode is performed for a parallel training decoder after the canonical C9 forward has executed.

It does not prohibit the canonical R6-R9 forward weight-wave loader from reading the model checkpoint as part of its already admitted residency transition.

R10 reports:

```text
additionalCheckpointReadCount = 0
additionalCheckpointDecodeCount = 0
trainingDecoderCloneCount = 0
```

---

## 18. R10 zero-operation boundary

R10 must not perform:

```text
backward WGSL dispatch
gradient buffer publication
optimizer step
parameter update
checkpoint mutation
LM backward
structural decoder backward
```

Required counters:

```text
backwardDispatchCount = 0
gradientBufferCount = 0
optimizerCount = 0
optimizerStepCount = 0
parameterUpdateCount = 0
checkpointMutationCount = 0
```

This boundary is intentional. R10 is the tape-authority patch, not the backward-execution patch.

---

## 19. Runtime receipts

R10 writes:

```text
live_tape_authority_receipt.json
live_tape_layer_XXXX_receipt.json     # one per selected layer
backward_owner_lease_receipt.json
reverse_residency_plan_receipt.json
bt_wgsl_backprop_live_tape_authority_06c_r10_final.json
```

### Authority receipt minimum fields

```text
r6R9C9PhysicalParentBound
checkpointLayerCount
selectedLayerStart
selectedLayerEnd
selectedLayerCount
capturedLayerTapeCount
canonicalResidentWeightAuthorityReuse
trainingDecoderCloneCount
parallelTrainingDecoderForwardCount
additionalCheckpointReadCount
additionalCheckpointDecodeCount
rawBorrowTapeCount
stage11GlobalStateRetainedCount
stage12ContextTapeCount
inputRmsTapeCount
postRmsTapeCount
qkvTapeCount
swiGluTapeCount
hostUploadCount
payloadReadbackCount
backwardDispatchCount
gradientBufferCount
optimizerCount
optimizerStepCount
parameterUpdateCount
checkpointMutationCount
tapeAuthorityDigest
pass
```

---

## 20. Required CLI gates

All must be `true`:

```text
--require-bt-wgsl-backprop-r6-r9-c9-physical-parent
--require-bt-wgsl-backprop-canonical-resident-weight-authority
--require-bt-wgsl-backprop-selected-topn-live-tape
--require-bt-wgsl-backprop-stage11-global-state-retention
--require-bt-wgsl-backprop-stage12-context-retention
--require-bt-wgsl-backprop-backward-owner-lease
--require-bt-wgsl-backprop-reverse-residency-plan
--require-bt-wgsl-backprop-zero-training-decoder-clone
--require-bt-wgsl-backprop-zero-checkpoint-reopen
--require-bt-wgsl-backprop-zero-payload-readback
--require-bt-wgsl-backprop-zero-backward-dispatch
--require-bt-wgsl-backprop-zero-optimizer
--require-bt-wgsl-backprop-zero-weight-mutation
```

No R10 CLI flag is silently defaulted by the 06C gate.

---

## 21. Hard failures

Representative failure families:

```text
BTBackpropTapeR06BParentNotPass
BTBackpropTapeR06BPassTokenMismatch
BTBackpropTapeC9ParentNotPass
BTBackpropTapeC9PassTokenMismatch
BTBackpropTapeSelectedLayerCountMismatch
BTBackpropTapeSelectedLayerOrderMismatch
BTBackpropTapeWeightPointerMismatch
BTBackpropTapeHiddenGenerationMismatch
BTBackpropTapeStage11StateIncomplete
BTBackpropTapeOwnerLeaseMissing
BTBackpropTapeHostUploadDetected
```

Live-body capture also fails closed on missing required surfaces:

```text
R6R8R10TensorTapeMissing
R6R8R10Stage11TapeMissing
R6R8R10Stage12TapeMissing
R6R8R10QPreRopeTapeMissing
R6R8R10KPreRopeTapeMissing
R6R8R10CanonicalVTapeMissing
R6R8R10QPostRopeTapeMissing
R6R8R10KPostRopeTapeMissing
R6R8R10TapeLeaseNotRawBorrowed
```

---

## 22. Changed source surface

R10 changes exactly 11 files relative to the supplied R9 parent:

```text
crates/burn_webgpu_backend/src/tensorcube_stage11_online_softmax_merge.rs
crates/burn_webgpu_backend/src/tensorcube_stage12_weighted_value_accumulation.rs
crates/model_core/src/actual_decoder_block_split_forward.rs
crates/model_core/src/attention_interconnect_w7.rs
crates/model_core/src/base_train_atlas_wave_02_r6_r5_body_splice.rs
crates/model_core/src/model_layers.rs
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r8_layer1_live_body.rs
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r9_c9_progressive_n_layer_wave_advancement.rs
crates/orchestrator_local/src/base_train_structural_lookahead_decoder_coupling_06c.rs
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c.args
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c_full.args
```

No new WGSL backward shader is added by R10.

---

## 23. R11 handoff

Natural child:

```text
BT-WGSL-BACKPROP-G204D-LIVE-PROMOTION-06C-R11
```

R11 must consume the R10 tape rather than recomputing forward state.

Minimum R11 inputs already retained by R10:

```text
q_post_rope
k_post_rope
canonical_v
Stage11 global softmax state
Stage12 context
layer / weight / hidden lineage
```

R11 may introduce `dContext` and explicit attention backward dispatch. R10 itself must retain `backwardDispatchCount = 0`.

---

## 24. PASS seal

```text
PASS_ASH_BASETRAIN_BT_WGSL_BACKPROP_LIVE_TAPE_AUTHORITY_06C_R10
R6_R9_C9_EXACT_PHYSICAL_FORWARD_PARENT /
CANONICAL_RESIDENT_WEIGHT_AUTHORITY_REUSED /
SELECTED_TOP_N_LIVE_FORWARD_TAPE_CAPTURED /
INPUT_RMSNORM_TAPE_BOUND /
PRE_POST_NEOX_QK_TAPE_BOUND /
CANONICAL_V_SINGLE_LEASE_BOUND /
STAGE11_GLOBAL_SOFTMAX_STATE_RETAINED /
STAGE12_CONTEXT_LEASE_RETAINED /
OPROJ_INPUT_OUTPUT_TAPE_BOUND /
POST_RMSNORM_TAPE_BOUND /
SWIGLU_GATE_UP_PRODUCT_TAPE_BOUND /
FINAL_HIDDEN_POINTER_TAPE_BOUND /
LAYER_GENERATION_WEIGHT_POINTER_LINEAGE_EXACT /
BACKWARD_TAPE_OWNER_LEASE_BOUND /
REVERSE_RESIDENCY_PLAN_PREPARED /
ZERO_PARALLEL_TRAINING_DECODER_RECONSTRUCTION /
ZERO_SELECTED_DECODER_CHECKPOINT_REOPEN /
ZERO_TRAININGBACKEND_SELECTED_DECODER_CLONE /
ZERO_DUPLICATE_FORWARD_DISPATCH /
ZERO_HOST_UPLOAD /
ZERO_PAYLOAD_READBACK /
ZERO_BACKWARD_DISPATCH /
ZERO_GRADIENT /
ZERO_OPTIMIZER /
ZERO_WEIGHT_MUTATION /
PROOF_LEDGER_HOLD_SEALED
```

---

## 25. Verification status at bake time

The bake environment does not provide a Rust/Cargo toolchain, so this artifact is sealed with source-level/static verification and ZIP integrity verification only.

Physical Rust compilation and runtime PASS remain `HOLD` until the operator-machine Cargo run completes.

No compile PASS is claimed by this specification.
