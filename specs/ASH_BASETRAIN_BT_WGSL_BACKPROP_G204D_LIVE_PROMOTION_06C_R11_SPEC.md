# ASH-BASETRAIN-BT-WGSL-BACKPROP-G204D-LIVE-PROMOTION-06C-R11

## R10 Live Tape Physical Parent / Existing G204D Attention-Backward Asset Promotion / Canonical Selected-Layer Base Attention Backward / Runtime B·Q·QHead·KVHead Geometry / Q32 Production Admission / R10 Post-RoPE Q·K Direct Lease / R10 Canonical V Direct Lease / R10 Stage11 Global Softmax State Direct Adoption / Stage12 Context Lineage Binding / GPU dContext Ingress / Raw-WGPU dQ·dK·dV Publication / Causal·GQA Geometry Preservation / Exact Softmax Backward State Reuse / No Forward Attention Recomputation / No Q·K·V Reconstruction / No TrainingBackend Autodiff Authority / No Host Gradient Payload / GPU Finite·Nonzero Receipt / Directional Probe Heritage Preservation / Canonical Shared-KV Gradient Identity / Single Base-Attention Lane Only / Structural H1·H2·H3·H4 Branch Backward Deferred / RoPE Backward Deferred / QKV Projection Backward Deferred / Gradient Atlas Accumulation Deferred / Optimizer = 0 / Weight Mutation = 0 / Proof Ledger HOLD Seal

> Patch ID: `ASH-BASETRAIN-BT-WGSL-BACKPROP-G204D-LIVE-PROMOTION-06C-R11`
>
> Build revision: `bt-wgsl-backprop-g204d-live-promotion-06c-r11`
>
> Physical parent: `BT-WGSL-BACKPROP-LIVE-TAPE-AUTHORITY-06C-R10`
>
> Proof ledger: `HOLD`

---

## 1. Purpose

R11 is the first 06C patch that executes an explicit decoder backward WGSL dispatch.

It does not create a new attention backward implementation. It promotes the existing G204D attention-backward asset to consume the exact R10 selected-layer live tape and publish device-resident base-attention gradients.

The active path is:

```text
R10 q_post_rope
R10 k_post_rope
R10 canonical_v
R10 Stage11 candidate global_state
GPU-resident deterministic dContext ingress
        ↓
G204D live attention backward
        ↓
dQ_post_rope
dK_post_rope
dV
```

R11 stops at those three gradient surfaces.

---

## 2. R10 parent authority

R11 revalidates the R10 live tape in the same physical 06C invocation before dispatching G204D.

Required parent properties:

```text
R6-R9 C9 physical forward bound
selected top-N tape captured
raw borrowed tape surfaces present
Stage11 global state retained
Stage12 context retained
training decoder clone = 0
selected-decoder checkpoint reopen = 0
payload readback = 0
```

R11 writes an explicit R10 parent receipt before executing G204D.

No R9 `TrainingBackend` selected-decoder reconstruction is restored.

---

## 3. Existing G204D preservation

The existing shader remains:

```text
crates/burn_webgpu_backend/src/shaders/base_train_g204d_attention_backward.wgsl
```

Existing probe entrypoints remain:

```text
backward_dq_rowdot
backward_dkdv
```

Legacy G204D probe behavior remains available and non-authoritative for the R11 live path.

The legacy probe keeps its historical layout mode and directional/CPU parity role.

R11 introduces a live execution mode rather than deleting the probe.

---

## 4. BQHD live-layout correction

R10 live Q/K/V leases use BQHD physical order.

The historical G204D probe used head-major HQD/HKD indexing.

Directly binding the R10 leases to the historical index formula would silently read the wrong elements.

R11 therefore adds an explicit layout mode to the existing G204D params ABI using a previously reserved field:

```text
reserved0 = 0 → legacy probe head-major layout
reserved0 = 1 → R11 live BQHD layout
```

Live Q indexing:

```text
((q_row * q_heads + q_head) * head_dim) + dim
```

Live K/V indexing:

```text
((key_row * kv_heads + kv_head) * head_dim) + dim
```

Legacy indexing remains unchanged when `reserved0 == 0`.

This is a required R11 correctness condition, not an optimization.

---

## 5. Q32 production admission

The historical probe gate:

```text
q_seq <= 16
```

is not used by the R11 live API.

The current physical R10 parent uses:

```text
B = 1
Q = 32
QH = 32
KVH = 4
D = 64
```

R11 live execution requires Q32 for this physical admission and records:

```text
q32ProductionAdmitted = true
```

No Q32-to-Q16 slicing or multi-dispatch emulation is allowed.

---

## 6. Runtime geometry source

R11 derives geometry from the R10 leases and Stage12 lineage:

```text
q_post_rope.shape
k_post_rope.shape
canonical_v.shape
Stage12 q_seq
Stage12 query_head_count
Stage12 head_dim
```

Required relations:

```text
Q.shape = [1,Q,QH,D]
K.shape = [1,K,KVH,D]
V.shape = [1,K,KVH,D]
QH % KVH = 0
gqa_group_size = QH / KVH
```

R11 does not reconstruct geometry from a second decoder manifest path.

---

## 7. Exact Stage11 softmax-state reuse

R11 consumes:

```text
R10.stage11_global_state.candidate_global_state
```

directly.

The Stage11 record order is the same query-row-major / query-head-minor order used by the live G204D path.

Each record remains 16 bytes and carries the forward max, denominator, valid/all-masked/final-write state required by G204D.

Forbidden:

```text
forward softmax recomputation
CPU global-state reconstruction
full probability surface materialization
full score matrix materialization
```

---

## 8. Stage12 lineage binding

R11 verifies that the R10 Q geometry matches the retained Stage12 context lineage.

The temporary R11 dContext ingress has the exact Stage12 context coordinate system:

```text
[1,Q,QH,D]
```

R11 does not yet compute the real OProj-origin dContext. That arrives in the later OProj/FFN backward patch.

---

## 9. GPU-only dContext fixture

R11 requires a nonzero deterministic dContext to physically validate G204D live promotion before OProj backward exists.

R11 adds:

```text
base_train_g204d_live_dcontext_seed.wgsl
```

The seed kernel writes the complete dContext payload directly on the GPU.

Required:

```text
dContext payload host upload = 0
dContext payload readback = 0
finite = true
nonzero = true
deterministic = true
```

Only small uniform metadata such as element count and seed is host supplied.

The dContext fixture is a G204D promotion fixture, not a training-loss gradient authority.

---

## 10. Live G204D API

R11 introduces a live API alongside the historical probe API:

```text
create_base_train_g204d_live_dcontext_fixture(...)
run_base_train_g204d_attention_backward_live(...)
```

Live input is entirely GPU-resource based:

```text
RawWgpuBufferLease q_post_rope
RawWgpuBufferLease k_post_rope
RawWgpuBufferLease canonical_v
Stage11 candidate global-state buffer
RawWgpuBufferLease dContext
runtime geometry and lineage metadata
```

There are no `Vec<f32>` gradient inputs or outputs in this API.

---

## 11. Raw GPU gradient publication

R11 publishes:

```text
dQ_post_rope [1,Q,QH,D]
dK_post_rope [1,K,KVH,D]
dV           [1,K,KVH,D]
```

as `RawWgpuBufferLease` resources.

The buffers remain GPU resident for child patches.

Required:

```text
dqGpuPublicationCount = selectedLayerCount
dkGpuPublicationCount = selectedLayerCount
dvGpuPublicationCount = selectedLayerCount
gradientPayloadReadbackCount = 0
```

---

## 12. GPU finite and nonzero status

The G204D shader extends its compact status buffer with:

```text
dQ nonzero count
dK nonzero count
dV nonzero count

dQ XOR fingerprint
dK XOR fingerprint
dV XOR fingerprint
```

The fingerprints use integer atomics and never require gradient payload readback.

Existing nonfinite and bounds status remains active.

PASS requires:

```text
invalidGlobalState = 0
nonFinite = 0
boundsViolation = 0
aggregateGradientNonzero = true
```

An individual dQ/dK/dV surface may report `ROLE_LOCAL_ZERO`, but the aggregate three-surface result may not be all zero.

---

## 13. Double-dispatch reproducibility

For each selected layer R11 runs the live G204D execution twice against the same immutable R10 tape and the same GPU dContext fixture.

The two runs must match exactly on:

```text
dQ nonzero count + XOR fingerprint
dK nonzero count + XOR fingerprint
dV nonzero count + XOR fingerprint
dispatch counts
all-masked count
```

The resulting compact `gradient_summary_digest` must match.

Required:

```text
reproducibilityRuns = 2
reproducibilityMatch = true
```

The second run's dQ/dK/dV leases are retained as the R11 published gradient surfaces.

---

## 14. Causal and GQA preservation

G204D retains the existing causal rule:

```text
kv_position_base + key_row <= q_position_base + q_row
```

and GQA mapping:

```text
kv_head = q_head / gqa_group_size
```

For the current parent:

```text
gqa_group_size = 8
```

No backward-only causal mask is introduced.

---

## 15. Shared canonical K/V semantics

R11 executes only the base attention lane.

Its dK/dV semantics are therefore:

```text
BASE_CANONICAL_ATTENTION_ONLY
```

They already refer to the canonical shared K/V objects, not branch-local K/V.

R12 will add H1-H4 lane contributions and deterministically merge:

```text
dK_shared = dK_base + dK_H1 + dK_H2 + dK_H3 + dK_H4
dV_shared = dV_base + dV_H1 + dV_H2 + dV_H3 + dV_H4
```

R11 performs no such merge yet.

---

## 16. Gradient readback prohibition

The historical G204D probe still contains gradient payload readback for its oracle/parity role.

The R11 live method does not call that path.

Within `run_live`:

```text
map_f32_buffer = 0
dQ copy-to-readback = 0
dK copy-to-readback = 0
dV copy-to-readback = 0
```

Only the 64-byte compact status buffer is copied and mapped.

Required receipt:

```text
compactStatusReadbackCount = 1 / live run
gradientPayloadReadbackCount = 0
```

---

## 17. R11 dispatch accounting

R11 defines one logical live G204D run as the paired execution of:

```text
backward_dq_rowdot
backward_dkdv
```

With:

```text
selectedLayerCount = N
reproducibilityRuns = 2
```

required logical count is:

```text
g204dLiveDispatchCount = N * 2
```

For the current top1 fixture:

```text
g204dLiveDispatchCount = 2
```

---

## 18. R11 zero-operation boundaries

R11 does not execute:

```text
H1/H2/H3/H4 structural attention backward
NeoX RoPE backward
Q/K/V projection backward
OProj backward
FFN backward
RMSNorm backward
gradient atlas accumulation
optimizer step
weight mutation
checkpoint write
```

Required:

```text
structuralBranchBackwardCount = 0
ropeBackwardCount = 0
qkvProjectionBackwardCount = 0
gradientAtlasAccumulationCount = 0
optimizerCount = 0
weightMutationCount = 0
```

---

## 19. Runtime receipts

R11 writes:

```text
bt_wgsl_backprop_live_tape_authority_06c_r10_parent.json
g204d_live_promotion_receipt.json
g204d_live_layer_XXXX_receipt.json
g204d_reproducibility_receipt.json
bt_wgsl_backprop_g204d_live_promotion_06c_r11_final.json
```

The existing R10 tape receipts may also be re-emitted because the live tape is revalidated in the same invocation.

---

## 20. Required CLI gates

All must be true:

```text
--require-bt-wgsl-backprop-r11-r10-physical-parent
--require-bt-wgsl-backprop-r11-g204d-live-authority
--require-bt-wgsl-backprop-r11-runtime-attention-geometry
--require-bt-wgsl-backprop-r11-q32-production
--require-bt-wgsl-backprop-r11-r10-qkv-direct-adoption
--require-bt-wgsl-backprop-r11-stage11-state-direct-adoption
--require-bt-wgsl-backprop-r11-stage12-lineage-binding
--require-bt-wgsl-backprop-r11-gpu-dcontext-ingress
--require-bt-wgsl-backprop-r11-raw-gradient-publication
--require-bt-wgsl-backprop-r11-gpu-finite-receipt
--require-bt-wgsl-backprop-r11-gpu-nonzero-receipt
--require-bt-wgsl-backprop-r11-double-dispatch-reproducibility
--require-bt-wgsl-backprop-r11-zero-forward-recompute
--require-bt-wgsl-backprop-r11-zero-checkpoint-reopen
--require-bt-wgsl-backprop-r11-zero-training-decoder-clone
--require-bt-wgsl-backprop-r11-zero-gradient-payload-readback
--require-bt-wgsl-backprop-r11-zero-structural-branch-backward
--require-bt-wgsl-backprop-r11-zero-optimizer
--require-bt-wgsl-backprop-r11-zero-weight-mutation
```

---

## 21. Failure families

Representative fail-closed errors:

```text
BTG204DLiveR10ParentMissing
BTG204DLiveR10ParentNotPass
BTG204DLiveTapeDigestMismatch
BTG204DLiveSelectedLayerMissing
BTG204DLiveGeometryMismatch
BTG204DLiveQSeqUnsupported
BTG204DLiveGqaMismatch
BTG204DLiveStage12LineageMissing
BTG204DLiveDContextNotGpuResident
BTG204DLiveAggregateGradientZero
BTG204DLiveGradientNonFinite
BTG204DLivePayloadReadbackDetected
BTG204DLiveReproducibilityMismatch
BTG204DLiveUnexpectedStructuralBranchBackward
BTG204DLiveUnexpectedOptimizer
BTG204DLiveUnexpectedWeightMutation
```

The backend live executor also retains G204D-specific fail-closed geometry, state, bounds, and dispatch errors.

---

## 22. Changed source surface

Relative to the supplied R10 parent, R11 changes exactly 8 files:

```text
crates/burn_webgpu_backend/src/base_train_g204d_attention_backward_probe.rs
crates/burn_webgpu_backend/src/lib.rs
crates/burn_webgpu_backend/src/shaders/base_train_g204d_attention_backward.wgsl
crates/burn_webgpu_backend/src/shaders/base_train_g204d_live_dcontext_seed.wgsl
crates/orchestrator_local/src/base_train_atlas_wave_02_r6_r9_c9_progressive_n_layer_wave_advancement.rs
crates/orchestrator_local/src/base_train_structural_lookahead_decoder_coupling_06c.rs
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c.args
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c_full.args
```

No specification, artifact, manifest, or `.sha256` sidecar is embedded in the baked code ZIP.

---

## 23. R12 handoff

Natural child:

```text
BT-STRUCTURAL-BRANCH-ATTENTION-BACKWARD-06C-R12
```

R12 will reuse the R11 live G204D executor for:

```text
base
H1
H2
H3
H4
```

then perform deterministic shared-K/V gradient reduction.

R12 must not create branch-local K/V authority.

---

## 24. Physical target

For the current R10 top1/Q32 fixture, expected R11 terminal summary is structurally:

```text
[bt-wgsl-backprop-g204d-live-promotion-06c-r11]
r10_physical_parent=1
selected_layers=1
q_seq=32
q32_production=1
q_post_rope_adopted=1
k_post_rope_adopted=1
canonical_v_adopted=1
stage11_state_adopted=1
stage12_lineage_bound=1
dcontext_gpu_ingress=1
g204d_live_dispatches=2
dq_published=1
dk_published=1
dv_published=1
aggregate_gradient_nonzero=1
gradient_nonfinite=0
reproducibility_runs=2
reproducibility_match=1
forward_recompute=0
training_decoder_clone=0
checkpoint_reopen=0
gradient_payload_readback=0
structural_branch_backward=0
optimizer=0
weight_mutation=0
proof_ledger=HOLD
```

---

## 25. PASS seal

```text
PASS_ASH_BASETRAIN_BT_WGSL_BACKPROP_G204D_LIVE_PROMOTION_06C_R11
R10_LIVE_TAPE_EXACT_PHYSICAL_PARENT /
EXISTING_G204D_ATTENTION_BACKWARD_ASSET_PROMOTED /
CANONICAL_SELECTED_LAYER_BASE_ATTENTION_BACKWARD /
RUNTIME_B_Q_QHEAD_KVHEAD_GEOMETRY /
Q32_PRODUCTION_ADMITTED /
R10_POST_ROPE_Q_DIRECT_LEASE /
R10_POST_ROPE_K_DIRECT_LEASE /
R10_CANONICAL_V_DIRECT_LEASE /
R10_STAGE11_GLOBAL_SOFTMAX_STATE_DIRECT_ADOPTION /
R10_STAGE12_CONTEXT_LINEAGE_BOUND /
GPU_DCONTEXT_INGRESS /
RAW_WGPU_DQ_PUBLICATION /
RAW_WGPU_DK_PUBLICATION /
RAW_WGPU_DV_PUBLICATION /
CAUSAL_SEMANTICS_PRESERVED /
GQA_SEMANTICS_PRESERVED /
EXACT_FORWARD_SOFTMAX_STATE_REUSED /
SHARED_CANONICAL_KV_GRADIENT_IDENTITY /
GPU_FINITE_RECEIPT /
GPU_NONZERO_RECEIPT /
DOUBLE_DISPATCH_REPRODUCIBILITY /
LEGACY_DIRECTIONAL_PROBE_PRESERVED_NON_AUTHORITY /
ZERO_FORWARD_ATTENTION_RECOMPUTATION /
ZERO_QKV_RECONSTRUCTION /
ZERO_TRAININGBACKEND_DECODER_CLONE /
ZERO_SELECTED_DECODER_CHECKPOINT_REOPEN /
ZERO_GRADIENT_PAYLOAD_READBACK /
ZERO_STRUCTURAL_H1_H2_H3_H4_BRANCH_BACKWARD /
ZERO_ROPE_BACKWARD /
ZERO_QKV_PROJECTION_BACKWARD /
ZERO_GRADIENT_ATLAS_ACCUMULATION /
ZERO_OPTIMIZER /
ZERO_WEIGHT_MUTATION /
PROOF_LEDGER_HOLD_SEALED
```

---

## 26. Bake-time verification status

The bake environment does not contain `cargo`, `rustc`, or `rustfmt`.

Therefore this bake is verified by source-level contract checks, response-file cardinality/uniqueness checks, live-path payload-readback audit, source delimiter checks, changed-surface comparison, ZIP integrity, and overlay/full byte parity.

Physical Rust compilation, WGSL validation by wgpu, and GPU execution remain `HOLD` until the operator-machine Cargo run.
