# `BT-WGSL-OPROJ-FFN-BACKWARD-06C-R13`

```text
R12 Five-Lane Structural Attention Backward Physical Parent /
Canonical Final-Hidden Upstream Gradient Ingress /
Final Residual Gradient Split /
DownProj Explicit WGSL Backward /
SwiGLU Product Backward /
Exact SiLU Derivative /
GateProj Explicit WGSL Backward /
UpProj Explicit WGSL Backward /
Deterministic FFN Input-Gradient Merge /
FFN Parameter Gradient Tile Publication /
Post-RMSNorm Backward Boundary Publication /
OProj Backward Executor Live Promotion /
Canonical Stage12 Context Direct Adoption /
OProj Parameter Gradient Tile Capability /
OProj dContext Candidate Publication /
Actual OProj Chain Authority Deferred Until Post-RMSNorm Backward /
No Partial dAfterAttention Promotion /
No Burn Autodiff Decoder Authority /
Canonical Weight Layout /
Atlas-Wave Bounded Gradient Tiles /
No Mega Parameter-Gradient Atlas /
Zero Gradient Payload Readback /
Zero Weight Payload Readback /
No RoPE Backward /
No QKV Projection Backward /
No RMSNorm Backward /
No δQ·Gate Projector Backward /
No Optimizer /
No Weight Mutation /
Proof Ledger HOLD Seal
```

## 0. Revision identity

```text
Patch ID:
ASH-BASETRAIN-BT-WGSL-OPROJ-FFN-BACKWARD-06C-R13

Build revision:
bt-wgsl-oproj-ffn-backward-06c-r13

Physical parent:
BT-STRUCTURAL-BRANCH-ATTENTION-BACKWARD-06C-R12

Proof ledger:
HOLD
```

R13 expands explicit WGSL backward from the attention operator into the decoder block FFN and linear-projection surfaces.

R13 does **not** yet close the complete decoder-layer backward chain because post-attention RMSNorm VJP remains R14 authority.

---

# 1. R12 physical parent

Required parent:

```text
r11PhysicalParent = 1

attentionLaneCount = 5

dQBasePublished = 1
dDeltaQPublished = 4

dKSharedPublished = 1
dVSharedPublished = 1

dGateCarrierPublished = 4

gradientNonfinite = 0
totalGradientNonzero = 1

gradientPayloadReadback = 0
optimizer = 0
weightMutation = 0
```

R13 may not reconstruct R12 gradients through another attention-backward path.

---

# 2. Current physical admission scope

Current physically proven selected-decoder geometry:

```text
selectedLayerCount = 1
selectedLayer = final decoder layer
Q = 32
hidden = runtime-derived
```

R13 physical gate remains:

```text
selectedLayerCount = 1
```

until reverse multi-layer weight residency is promoted later.

This is intentional.

Earlier selected layers may have retained forward tape, but their nine canonical decoder weights are no longer resident after progressive forward execution.

Multi-layer reverse residency remains deferred.

---

# 3. Canonical FFN forward equation

Forward tape from R10 contains:

```text
Xn = normalized_ffn_input

Gpre = GateProj(Xn)
Gsilu = SiLU(Gpre)

U = UpProj(Xn)

P = Gsilu * U

D = DownProj(P)

Y = after_attention + D
```

where:

```text
Y = final_hidden
```

All R13 backward equations must correspond exactly to this forward.

---

# 4. Upstream gradient ingress

R13 introduces:

```text
dFinalHidden
```

as the upstream gradient to the selected final decoder layer.

Because the full LM/loss backward is not yet connected, physical R13 admission uses a deterministic GPU-generated fixture.

Required:

```text
dFinalHiddenGpuResident = true
dFinalHiddenFinite = true
dFinalHiddenNonzero = true

hostPayloadUploadCount = 0
payloadReadbackCount = 0
```

This fixture is **not** a final training-loss gradient authority.

---

# 5. Final residual split

Because:

```text
final_hidden =
    after_attention
  + down_output
```

the immediate backward split is:

```text
dDownOutput = dFinalHidden

dAfterAttentionResidual = dFinalHidden
```

These are exact.

R13 publishes:

```text
dDownOutput
dAfterAttentionResidual
```

as GPU-resident surfaces.

---

# 6. DownProj backward

Forward:

```text
D[t,o]
=
Σ_i P[t,i] * Wdown[o,i]
```

Canonical checkpoint weight layout:

```text
Wdown = [out_dim, in_dim]
```

Backward:

```text
dP[t,i]
=
Σ_o dD[t,o] * Wdown[o,i]
```

and:

```text
dWdown[o,i]
=
Σ_t dD[t,o] * P[t,i]
```

No bias gradient exists unless the actual resident module exposes a bias.

R13 may not fabricate one.

---

# 7. SwiGLU product backward

Forward:

```text
P = Gsilu * U
```

Backward:

```text
dGsilu = dP * U

dU = dP * Gsilu
```

Both operations are GPU elementwise kernels.

---

# 8. Exact SiLU derivative

Forward:

```text
SiLU(x) = x * sigmoid(x)
```

Derivative:

```text
s = sigmoid(x)

SiLU'(x)
=
s * (1 + x * (1 - s))
```

Therefore:

```text
dGpre
=
dGsilu * SiLU'(Gpre)
```

R13 must use retained:

```text
gate_linear_pre_activation
```

from R10.

Forbidden:

```text
recompute GateProj forward
derive preactivation from SiLU output
approximate SiLU derivative
```

---

# 9. GateProj backward

Forward:

```text
Gpre = GateProj(Xn)
```

Backward:

```text
dX_gate
=
dGpre * Wgate
```

and:

```text
dWgate
=
dGpreᵀ * Xn
```

using canonical `[out,in]` weight layout.

---

# 10. UpProj backward

Forward:

```text
U = UpProj(Xn)
```

Backward:

```text
dX_up
=
dU * Wup
```

and:

```text
dWup
=
dUᵀ * Xn
```

---

# 11. Deterministic FFN input-gradient merge

The normalized FFN input participates in both GateProj and UpProj.

Therefore:

```text
dNormalizedFfnInput
=
dX_gate + dX_up
```

Merge order is fixed:

```text
GATE
→ UP
```

Forbidden:

```text
unordered floating atomic merge
CPU merge
completion-order-dependent merge
```

Publication:

```text
dNormalizedFfnInput
```

This is the exact gradient on the **output coordinate of post-attention RMSNorm**.

---

# 12. Post-RMSNorm pending boundary

R13 cannot directly add `dNormalizedFfnInput` to `dAfterAttentionResidual`.

They are gradients in different coordinates.

Required publication bundle:

```text
PostRmsBackwardPendingV1 {
    after_attention_tape,
    post_rms_inverse,
    post_rms_weight_identity,
    normalized_ffn_input,
    d_normalized_ffn_input,
    d_after_attention_residual,
}
```

R14 will compute:

```text
dAfterAttentionFromPostNorm
=
PostRmsNormBackward(
    dNormalizedFfnInput
)
```

then:

```text
dAfterAttentionTotal
=
dAfterAttentionResidual
+
dAfterAttentionFromPostNorm
```

---

# 13. Forbidden partial-gradient promotion

R13 must not claim:

```text
dAfterAttentionResidual
```

alone is the complete:

```text
dAfterAttention
```

authority.

Required:

```text
actualAfterAttentionGradientAuthority = false

postRmsBackwardPending = true
```

This is a hard SSOT boundary.

---

# 14. OProj dependency

Forward:

```text
attention_context
→ OProj
→ attention_output
→ + input residual
→ after_attention
```

Exact OProj backward requires:

```text
dAttentionOutput
=
dAfterAttentionTotal
```

but `dAfterAttentionTotal` cannot exist until R14 post-RMSNorm backward executes.

Therefore R13 separates:

```text
OPROJ BACKWARD EXECUTOR VALIDATION
```

from:

```text
OPROJ ACTUAL CHAIN AUTHORITY
```

---

# 15. OProj live executor promotion

R13 promotes the same explicit linear backward primitive used by FFN to support OProj geometry.

Input tape:

```text
canonical Stage12 context
resident OProj weight
```

Physical validation uses a separate deterministic GPU:

```text
dAttentionOutputFixture
```

with exact shape.

It produces candidate:

```text
dContextCandidate
dWOProjCandidateTiles
```

for executor validation.

Required:

```text
oprojBackwardExecutorAdmitted = true

oprojActualChainAuthority = false
oprojFixtureAuthority = true
```

---

# 16. OProj fixture isolation

The OProj validation fixture must never enter R12 as if it were the real decoder gradient.

Forbidden:

```text
R13 dContextCandidate
→ R12 canonical dContext authority
```

in this revision.

Required:

```text
r12ActualDContextRebindCount = 0
```

R14 performs the actual promotion after post-RMSNorm VJP closes.

---

# 17. Why R13 does not promote actual dContext

Exact dependency:

```text
dFinalHidden
     │
     ├───────────────┐
     │               │
     │           residual branch
     ↓               │
FFN backward         │
     │               │
dNormalizedFFN       │
     │               │
     ↓               │
POST RMS BACKWARD    │   ← R14
     │               │
     └───────┬───────┘
             ↓
    dAfterAttentionTotal
             │
             ↓
        OProj backward
             │
             ↓
        actual dContext
```

Skipping the RMSNorm node would be structurally incorrect.

---

# 18. Explicit linear-backward kernel authority

R13 introduces a common explicit WGSL linear-backward service.

Suggested logical API:

```rust
run_base_train_r13_linear_backward(...)
```

Inputs:

```text
X
W [out,in]
dY
runtime M/K/N geometry
role identity
gradient tile policy
```

Outputs:

```text
dX
dW tile stream
compact receipt
```

It is reused by:

```text
DownProj
GateProj
UpProj
OProj validation
```

---

# 19. No TensorCube acceleration yet

R13 correctness kernels remain ordinary explicit WGSL kernels.

R13 does not generalize K6P or require TensorCube matmul.

Required:

```text
tensorCubeBackwardMatmulCount = 0
```

TensorCube backward acceleration remains R16.

---

# 20. dX kernel

For each input-gradient element:

```text
dX[t,i]
=
Σ_o dY[t,o] * W[o,i]
```

One logical output element has one deterministic owner.

Forbidden:

```text
float atomic accumulation into dX
```

---

# 21. dW kernel

For each weight-gradient element:

```text
dW[o,i]
=
Σ_t dY[t,o] * X[t,i]
```

Token/query reduction order must be deterministic.

Current B1/Q32 geometry permits a fixed:

```text
t = 0 → 31
```

reduction.

Runtime Q remains metadata-derived.

---

# 22. Atlas-Wave parameter-gradient tiles

R13 must not allocate a permanent mega gradient atlas for:

```text
GateProj
UpProj
DownProj
OProj
```

Instead use bounded row tiles.

Example logical representation:

```text
LinearGradientTile {
    role,
    output_row_start,
    output_row_count,
    input_width,
    gpu_buffer,
    completion,
    tile_digest,
}
```

---

# 23. Tile ordering

Canonical role order:

```text
DOWN
GATE
UP
OPROJ
```

Within each role:

```text
output row ascending
```

Required:

```text
gradientTileOrderDeterministic = true
```

---

# 24. Gradient tile authority

For actual FFN roles:

```text
dWdown
dWgate
dWup
```

are authoritative raw gradient tiles.

For OProj in R13:

```text
dWOProjCandidate
```

is validation-only because upstream gradient is a fixture.

Metadata must distinguish:

```text
ACTUAL_FFN_GRADIENT

OPROJ_EXECUTOR_FIXTURE_GRADIENT
```

No silent equivalence.

---

# 25. Gradient-atlas boundary

R13 parameter-gradient tiles are not yet G205D gradient-atlas entries.

Required:

```text
g205dAccumulationCount = 0
gradientAtlasCommitCount = 0
```

R19 will adopt and accumulate the canonical tiles.

---

# 26. Weight authority

All linear backward operations use the canonical resident selected-layer weight slot.

Forbidden:

```text
checkpoint reopen
TrainingBackend block rebuild
host-side weight reconstruction
second parameter bank
```

Required:

```text
residentWeightAuthorityReuse = true

checkpointReopenCount = 0
weightPayloadReadbackCount = 0
```

---

# 27. Weight-layout contract

Exact layout remains:

```text
checkpoint / resident weight
=
[out_dim, in_dim]
```

R13 must not transpose persisted weight authority.

Transpose exists only in mathematical indexing.

Receipt per role:

```text
weightLayout = OUT_IN
```

---

# 28. Same-device requirement

All:

```text
forward tapes
resident weights
dFinalHidden
dX
dW tiles
OProj fixture
```

must belong to the same physical device/runtime epoch.

Required:

```text
crossDeviceTransferCount = 0
hostShuttleCount = 0
```

---

# 29. GPU finite guards

GPU compact receipts for:

```text
dDownOutput
dFfnProduct
dGatePre
dUp
dNormalizedFfnInput

dWdown tiles
dWgate tiles
dWup tiles

OProj candidate dContext
OProj candidate dW tiles
```

Required:

```text
nonfiniteCount = 0
```

No payload readback.

---

# 30. Nonzero semantics

With deterministic nonzero `dFinalHidden` fixture, FFN aggregate backward must show pressure.

Required:

```text
ffnAggregateGradientNonzero = true
```

Individual parameter tile zero values remain legal.

OProj fixture validation also requires:

```text
oprojCandidateAggregateNonzero = true
```

---

# 31. Reproducibility

R13 performs two executions against immutable forward tape and identical fixtures.

Compare GPU-side compact fingerprints for:

```text
dNormalizedFfnInput

dWdown
dWgate
dWup

OProj dContext candidate
OProj dW candidate
```

Required:

```text
reproducibilityRuns = 2
reproducibilityMatch = true
```

---

# 32. R12 gradient preservation

R13 must not modify:

```text
dQbase_post_rope

dDeltaQ H1-H4

dKshared_post_rope
dVshared

dGate H1-H4
```

Required:

```text
r12GradientMutationCount = 0
```

R12's current fixture-origin attention gradients remain separate until R14 promotes actual dContext.

---

# 33. No Burn decoder backward authority

R13 must not reactivate:

```text
TrainingBackend selected decoder

Burn backward through decoder block

zero-value VJP surrogate
```

Required:

```text
burnDecoderBackwardCount = 0
trainingDecoderCloneCount = 0
```

---

# 34. R13 publication surfaces

Authoritative:

```text
dAfterAttentionResidual

dNormalizedFfnInput

dWdown tile stream
dWgate tile stream
dWup tile stream

PostRmsBackwardPendingV1
```

Validation-only:

```text
OProj dContext candidate

OProj dW candidate tile stream
```

---

# 35. Explicitly deferred to R14

R14:

```text
BT-WGSL-RMSNORM-BACKWARD-06C-R14
```

must consume:

```text
PostRmsBackwardPendingV1
```

and produce:

```text
dAfterAttentionFromPostNorm

dAfterAttentionTotal
```

Then R14 invokes the already admitted R13 OProj backward executor with the actual gradient:

```text
dAfterAttentionTotal
        ↓
actual OProj backward
        ↓
actual dContext
actual dWOProj
```

At that point:

```text
r12FixtureDContextAuthority
```

can be retired.

---

# 36. Input RMSNorm remains pending

Even after R14 closes post-RMSNorm + OProj:

```text
input RMSNorm backward
```

still cannot be fully driven until R15 supplies:

```text
dNormalizedHidden
```

from QKV/RoPE backward.

Therefore R14 may provide the primitive and post-RMS live execution while input-RMS final application remains downstream-bound.

No fake ordering.

---

# 37. Explicitly deferred beyond R14

```text
R15:
NeoX inverse rotation
QKV projection backward

R16:
TensorCube backward matmul acceleration

R17:
δQ + gate projector backward

R18:
structural TensorCube factor/head backward

R19:
G205D gradient atlas

R20:
optimizer candidate + materialization
```

---

# 38. Runtime receipts

Minimum:

```text
r13_parent_r12_receipt.json

r13_final_hidden_gradient_ingress.json

r13_downproj_backward_receipt.json

r13_swiglu_backward_receipt.json

r13_gateproj_backward_receipt.json

r13_upproj_backward_receipt.json

r13_ffn_input_merge_receipt.json

r13_ffn_gradient_tiles_receipt.json

r13_post_rms_pending_receipt.json

r13_oproj_executor_receipt.json

r13_reproducibility_receipt.json

bt_wgsl_oproj_ffn_backward_06c_r13_final.json
```

---

# 39. FFN receipt minimum

```text
selectedLayer

dFinalHiddenGpuIngress

downBackwardDispatch
swiGluBackwardDispatch
gateBackwardDispatch
upBackwardDispatch

dNormalizedFfnInputPublished

downGradientTileCount
gateGradientTileCount
upGradientTileCount

ffnAggregateNonzero
ffnNonfiniteCount

payloadReadbackCount

pass
```

---

# 40. OProj receipt minimum

```text
selectedLayer

canonicalStage12ContextBound
residentOProjWeightBound

fixtureDAttentionOutputGpuResident

oprojBackwardExecutorAdmitted

dContextCandidatePublished
dWOProjCandidateTilesPublished

actualChainAuthority = false
r12ActualDContextRebindCount = 0

payloadReadbackCount = 0

pass
```

---

# 41. Aggregate counters

Current top1 physical target:

```text
r12PhysicalParentBound = 1

selectedLayerCount = 1

finalHiddenGradientIngressCount = 1

downProjBackwardCount = 2
gateProjBackwardCount = 2
upProjBackwardCount = 2

swiGluBackwardCount = 2

ffnInputGradientPublicationCount = 1

ffnParameterGradientRoleCount = 3

oprojBackwardFixtureDispatchCount = 2
oprojActualChainDispatchCount = 0

postRmsBackwardCount = 0

r12ActualDContextRebindCount = 0

gradientPayloadReadbackCount = 0
weightPayloadReadbackCount = 0

checkpointReopenCount = 0
trainingDecoderCloneCount = 0

ropeBackwardCount = 0
qkvProjectionBackwardCount = 0

optimizerCount = 0
weightMutationCount = 0
```

Counts above assume reproducibility runs = 2.

---

# 42. Hard failures

```text
BTR13R12ParentMissing
BTR13R12ParentNotPass

BTR13SelectedLayerCountUnsupported

BTR13FinalHiddenTapeMissing
BTR13FinalHiddenGradientIngressMissing

BTR13ResidentWeightAuthorityMissing

BTR13DownProjBackwardFailed
BTR13SwiGluBackwardFailed
BTR13GateProjBackwardFailed
BTR13UpProjBackwardFailed

BTR13WeightLayoutMismatch

BTR13FfnInputGradientMissing
BTR13FfnGradientTileMissing

BTR13PostRmsPendingBoundaryMissing

BTR13PartialAfterAttentionPromoted

BTR13Stage12ContextMissing

BTR13OProjExecutorAdmissionFailed
BTR13OProjActualAuthorityUnexpected

BTR13GradientNonFinite
BTR13FfnAggregateGradientZero

BTR13GradientPayloadReadbackDetected
BTR13WeightPayloadReadbackDetected

BTR13CheckpointReopenDetected
BTR13TrainingDecoderCloneDetected

BTR13UnexpectedRmsNormBackward
BTR13UnexpectedRoPEBackward
BTR13UnexpectedQKVBackward

BTR13UnexpectedGradientAtlas
BTR13UnexpectedOptimizer
BTR13UnexpectedWeightMutation

BTR13ReproducibilityMismatch
```

---

# 43. CLI gates

```text
--require-bt-wgsl-r13-r12-physical-parent
true

--require-bt-wgsl-r13-selected-final-layer-residency
true

--require-bt-wgsl-r13-gpu-final-hidden-gradient
true

--require-bt-wgsl-r13-downproj-backward
true

--require-bt-wgsl-r13-swiglu-backward
true

--require-bt-wgsl-r13-gateproj-backward
true

--require-bt-wgsl-r13-upproj-backward
true

--require-bt-wgsl-r13-ffn-input-gradient-merge
true

--require-bt-wgsl-r13-ffn-gradient-tiles
true

--require-bt-wgsl-r13-post-rms-pending-boundary
true

--require-bt-wgsl-r13-oproj-executor
true

--require-bt-wgsl-r13-oproj-actual-chain-deferred
true

--require-bt-wgsl-r13-out-in-weight-layout
true

--require-bt-wgsl-r13-zero-gradient-payload-readback
true

--require-bt-wgsl-r13-zero-weight-readback
true

--require-bt-wgsl-r13-zero-checkpoint-reopen
true

--require-bt-wgsl-r13-zero-training-decoder-clone
true

--require-bt-wgsl-r13-zero-rmsnorm-backward
true

--require-bt-wgsl-r13-zero-rope-backward
true

--require-bt-wgsl-r13-zero-qkv-backward
true

--require-bt-wgsl-r13-zero-gradient-atlas
true

--require-bt-wgsl-r13-zero-optimizer
true

--require-bt-wgsl-r13-zero-weight-mutation
true

--require-bt-wgsl-r13-double-run-reproducibility
true
```

---

# 44. Expected physical summary

```text
[bt-wgsl-oproj-ffn-backward-06c-r13]

r12_physical_parent=1
selected_layers=1

dfinal_gpu_ingress=1

downproj_backward=2
swiglu_backward=2
gateproj_backward=2
upproj_backward=2

ffn_input_gradient_published=1

dw_down_tiles>0
dw_gate_tiles>0
dw_up_tiles>0

ffn_gradient_nonfinite=0
ffn_gradient_nonzero=1

post_rms_pending=1

oproj_executor_admitted=1
oproj_fixture_dispatch=2
oproj_context_candidate=1

oproj_actual_chain=0
r12_actual_dcontext_rebind=0

reproducibility_runs=2
reproducibility_match=1

checkpoint_reopen=0
training_decoder_clone=0

gradient_payload_readback=0
weight_payload_readback=0

rmsnorm_backward=0
rope_backward=0
qkv_projection_backward=0

gradient_atlas=0
optimizer=0
weight_mutation=0

proof_ledger=HOLD
```

---

# 45. PASS seal

```text
PASS_ASH_BASETRAIN_BT_WGSL_OPROJ_FFN_BACKWARD_06C_R13

R12_FIVE_LANE_STRUCTURAL_ATTENTION_BACKWARD_EXACT_PHYSICAL_PARENT /
CANONICAL_SELECTED_FINAL_LAYER_RESIDENT_WEIGHT_AUTHORITY /
GPU_FINAL_HIDDEN_UPSTREAM_GRADIENT_INGRESS /
FINAL_HIDDEN_RESIDUAL_GRADIENT_SPLIT /
DOWNPROJ_EXPLICIT_WGSL_BACKWARD /
SWIGLU_PRODUCT_EXACT_BACKWARD /
SILU_EXACT_DERIVATIVE /
GATEPROJ_EXPLICIT_WGSL_BACKWARD /
UPPROJ_EXPLICIT_WGSL_BACKWARD /
DETERMINISTIC_GATE_PLUS_UP_FFN_INPUT_GRADIENT_MERGE /
FFN_PARAMETER_GRADIENT_TILE_PUBLICATION /
POST_RMSNORM_BACKWARD_PENDING_BOUNDARY /
OPROJ_BACKWARD_EXECUTOR_LIVE_PROMOTED /
CANONICAL_STAGE12_CONTEXT_DIRECT_ADOPTION /
OPROJ_PARAMETER_GRADIENT_TILE_CAPABILITY /
OPROJ_DCONTEXT_FIXTURE_CANDIDATE_PUBLICATION /
ZERO_PARTIAL_DAFTERATTENTION_PROMOTION /
ZERO_OPROJ_ACTUAL_CHAIN_AUTHORITY_BEFORE_POST_RMSNORM /
CANONICAL_OUT_IN_WEIGHT_LAYOUT /
ATLAS_WAVE_BOUNDED_GRADIENT_TILES /
ZERO_MEGA_PARAMETER_GRADIENT_ATLAS /
ZERO_BURN_DECODER_BACKWARD /
ZERO_TRAININGBACKEND_DECODER_CLONE /
ZERO_CHECKPOINT_REOPEN /
ZERO_GRADIENT_PAYLOAD_READBACK /
ZERO_WEIGHT_PAYLOAD_READBACK /
ZERO_RMSNORM_BACKWARD /
ZERO_ROPE_BACKWARD /
ZERO_QKV_PROJECTION_BACKWARD /
ZERO_GRADIENT_ATLAS_ACCUMULATION /
ZERO_OPTIMIZER /
ZERO_WEIGHT_MUTATION /
DOUBLE_RUN_REPRODUCIBILITY /
PROOF_LEDGER_HOLD_SEALED
```

## R13 한 줄 SSOT

> **최종 hidden의 upstream gradient를 실제 FFN 역전파로 내려 `dNormalizedFfnInput`과 Gate/Up/Down parameter-gradient tile까지 GPU에서 발행하고, OProj backward executor 자체는 실제 Stage12 context 위에서 검증하되 post-RMSNorm gradient가 아직 없으므로 `actual dContext` 권한은 R14 전까지 절대 승격하지 않는다.**

이렇게 잡으면 R13에서 의존성을 억지로 뛰어넘지 않으면서도 **FFN은 진짜 backward가 되고, OProj는 실제 weight/context에 결선된 준비 완료 상태**가 됩니다. R14가 post-RMSNorm 한 칸만 정확히 뒤집으면 그 즉시 실제 `dAfterAttentionTotal → OProj → dContext → R12 5-lane attention` 사슬을 닫을 수 있습니다.
