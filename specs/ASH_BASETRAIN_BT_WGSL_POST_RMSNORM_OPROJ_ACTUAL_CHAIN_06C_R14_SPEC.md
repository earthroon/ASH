# ASH-BASETRAIN-BT-WGSL-POST-RMSNORM-OPROJ-ACTUAL-CHAIN-06C-R14

## Revision identity

```text
Patch ID:
ASH-BASETRAIN-BT-WGSL-POST-RMSNORM-OPROJ-ACTUAL-CHAIN-06C-R14

Build revision:
bt-wgsl-post-rmsnorm-oproj-actual-chain-06c-r14

Physical parent:
BT-WGSL-MICRO-ATLAS-TENSORCUBE-RESIDENCY-GC-06C-R13-R2

Corrected source parent:
R13-R2-R3 OProj Validation Candidate Zero-Observation Fix

Proof ledger:
HOLD
```

## Scope seal

```text
R13-R2 Physical Parent /
R13-R2-R3 Corrected Source Parent /
PostRmsBackwardPendingV1 Exact Consumption /
Retained Post-RMS Inverse Authority /
Resident Post-RMS Weight Exact Reacquisition /
No RMS Forward Recomputation /
Exact RMSNorm Input VJP /
Exact RMSNorm Weight Gradient /
Deterministic Row-Dot Reduction /
Post-RMS Gradient Publication /
FFN Residual Gradient Reuse /
dAfterAttentionFromPostNorm Publication /
dAfterAttentionTotal Deterministic Merge /
Attention Residual Carrier Publication /
Actual OProj Backward Promotion /
Actual Stage12 Context Exact Reuse /
Actual OProj dContext Publication /
Actual OProj Weight-Gradient Tile Publication /
R13 OProj Fixture Candidate Retirement /
Actual dContext Structural Attention Rebind /
BASE + H1-H4 Five-Lane Actual Backward /
Canonical Shared K/V Gradient Authority /
Actual dQbase / dDeltaQ / dK / dV Publication /
Actual Gate Carrier Publication /
R12 Fixture dContext Retirement /
R12 Fixture-Derived Attention Gradient Retirement /
R15 QKV-RoPE Handoff Authority /
Micro-Atlas TensorCube Transport Preservation /
Commit-GC Preservation /
Fail-Closed Numerics Preservation /
Zero-Is-Observation Not Failure /
Zero Gradient Fabrication Prohibition /
Production Payload Readback Zero /
No Forward Attention Recomputation /
No Checkpoint Reopen /
No TrainingBackend Decoder Clone /
No Input-RMSNorm Backward /
No RoPE Backward /
No QKV Projection Backward /
No DeltaQ Projector Backward /
No Gate Projector Backward /
No Optimizer /
No Weight Mutation /
Double-Run Reproducibility /
Proof Ledger HOLD Seal
```

## One-line SSOT

R14 consumes the exact R13 `PostRmsBackwardPendingV1` tape, computes the post-attention RMSNorm VJP without forward recomputation, merges it with the FFN residual gradient into canonical `dAfterAttentionTotal`, promotes OProj backward from validation-only to actual authority, then rebinds the resulting actual `dContext` into the retained BASE+H1-H4 attention backward so R15 receives only actual-chain post-RoPE gradients.

## Physical geometry

```text
selectedLayerCount = 1
selectedLayer = final decoder layer
B = 1
Q = 32
Q heads = 32
KV heads = 4
head dim = 64
hidden width = 2048 on current admitted model
```

R14 does not claim broader physical geometry than the admitted Q32 path.

## Required pending authority

```text
PostRmsBackwardPendingV1 {
    layer_index,
    after_attention_tape,
    post_rms_inverse,
    post_rms_weight_identity,
    normalized_ffn_input,
    d_normalized_ffn_input,
    d_after_attention_residual,
}
```

Required:

```text
pendingCount = 1
selectedLayerExactMatch = true
sameDevice = true
sameRuntime = true
checkpointReopenCount = 0
forwardRmsRecomputeCount = 0
```

## Resident weight reacquisition

R14 reacquires `post_attn_norm.weight` and `o_proj.weight` from the same selected-layer resident weight authority and validates layer, generation, pointer digest, and the pending post-RMS weight identity. No checkpoint reopen, host weight reconstruction, parallel parameter bank, or silent pointer substitution is permitted.

The post-RMS identity is bound to `SHA256(weight_pointer_digest + ":post_attn_norm")`.

## Exact RMSNorm backward

Production forward identity:

```text
x[t,i]   = after_attention_tape[t,i]
r[t]     = retained post_rms_inverse[t]
gamma[i] = post_attn_norm.weight[i]
y[t,i]   = x[t,i] * r[t] * gamma[i]
```

R14 never recomputes production `r[t]`.

Given:

```text
dy[t,i] = d_normalized_ffn_input[t,i]
a[t,i]  = dy[t,i] * gamma[i]
rowDot[t] = sum_j a[t,j] * x[t,j]
```

Canonical input VJP:

```text
dAfterAttentionFromPostNorm[t,i]
= r[t] * (
    a[t,i]
    - x[t,i] * (r[t]^2 / H) * rowDot[t]
  )
```

Canonical weight gradient:

```text
dGamma[i]
= sum_t dy[t,i] * x[t,i] * r[t]
```

Parameter-gradient role is `POST_ATTN_NORM`; there is no RMSNorm bias-gradient authority.

## Deterministic row-dot authority

The production WGSL row dot uses fixed row-major sequential accumulation. No unordered floating-point atomic reduction is used. R14 prioritizes deterministic auditability over premature subgroup optimization.

## Fail-closed numerics and zero policy

Any nonfinite production value in `x`, `dy`, `gamma`, retained inverse, row dot, `dX`, or `dGamma` is a hard fault before publication. NaN-to-zero, Inf clamping, gradient clamping, and silent epsilon fabrication are forbidden.

R14 intentionally has no `GradientZero` hard failure. A finite zero with exact write completion, exact coverage, and reproducibility is a valid observation. Zero must not be amplified or fabricated inside R14. Any future Delta-K observability layer is a separate explicit patch.

## dAfterAttentionTotal

R14 publishes:

```text
dAfterAttentionTotal
= dAfterAttentionResidual
+ dAfterAttentionFromPostNorm
```

Merge order is fixed `RESIDUAL -> POST_RMS`.

The resulting surface is both the attention residual carrier and actual OProj upstream:

```text
dInputHiddenAttentionResidual = dAfterAttentionTotal
dOProjOutput = dAfterAttentionTotal
```

R14 does not yet claim full `dInputHiddenTotal`.

## Actual OProj backward promotion

R13's OProj path was validation-only. R14 reuses the admitted R13 linear-backward executor with exact retained Stage12 context and current canonical `W_o[out,in]` layout:

```text
dContextActual[t,in]
= sum_out dO[t,out] * W_o[out,in]

dWOProj[out,in]
= sum_t dO[t,out] * Context[t,in]
```

Authority transition:

```text
r13 candidate actual feed = 0
r13 candidate authority = 0
r14 OProj actual chain authority = 1
r14 dContextActual authority = 1
r14 dWOProj tile authority = 1
```

The R13 candidate remains historical evidence only.

## Actual structural attention rebind

R14 does not feed R12's synthetic fixture-derived attention gradients to later stages. Instead:

```text
dContextActual
-> retained BASE/H1/H2/H3/H4 context and gate tapes
-> exact dContext split
-> retained G204D live backward executor
-> actual dQ/dK/dV/gate carriers
```

No attention forward recomputation occurs.

Retained structural relation:

```text
Cfinal
= C0
+ G1*(C1-C0)
+ G2*(C2-C0)
+ G3*(C3-C0)
+ G4*(C4-C0)
```

Therefore:

```text
dC_H1 = dCfinal * G1
...
dC_H4 = dCfinal * G4

dC_BASE
= dCfinal * (1 - G1 - G2 - G3 - G4)
```

Gate carriers retain the R12 exact definition based on `dCfinal * (C_h - C0)` reduced over hidden dimensions.

## Five-lane actual gradient authority

R14 reuses the R13-R1 fail-closed G204D path for BASE, H1, H2, H3, H4 with exact retained post-RoPE Q, branch Q+deltaQ, canonical shared K/V, Stage11 global state, and Stage12 context lineage.

Canonical merges:

```text
dQbaseActual = dQ0 + dQ1 + dQ2 + dQ3 + dQ4

dDeltaQ_H1Actual = dQ1
...
dDeltaQ_H4Actual = dQ4

dKsharedActual = dK0 + dK1 + dK2 + dK3 + dK4

dVsharedActual = dV0 + dV1 + dV2 + dV3 + dV4
```

Merge order is fixed `BASE -> H1 -> H2 -> H3 -> H4` with no unordered floating-point merge.

## R12 fixture retirement

After R14 passes:

```text
r12FixtureDContextAuthority = 0
r12FixtureGradientAuthority = 0
fixtureGradientFeedToR15 = 0
fixtureGradientFeedToR17 = 0
```

R12 outputs/receipts may remain as historical physical validation evidence, not downstream gradient authority.

## R15 handoff

R14 publishes:

```text
dInputHiddenAttentionResidual

dQbasePostRopeActual
dKsharedPostRopeActual
dVsharedActual

dDeltaQ_H1..H4Actual
dGate_H1..H4Actual

postAttnNormWeightGradient
OProjWeightGradientTiles
```

R15 consumes base Q/K/V plus the residual carrier for inverse-RoPE, QKV projection backward, input-RMSNorm backward, and selected-layer `dInputHiddenTotal`. R17 later consumes DeltaQ and gate carriers.

R14 reports zero for input-RMSNorm backward, RoPE backward, QKV projection backward, DeltaQ projector backward, gate projector backward, optimizer, and weight mutation.

## Micro-Atlas/TensorCube preservation

R14 preserves R13-R2 transport:

```text
1D logical surface
-> bounded Micro Atlas pages
-> TensorCube residency
-> canonical direct write
-> completion
-> commit
-> GC eligibility
-> release
```

Post-RMS dX and OProj dW use bounded execution, and headwise parity remains paged. Direct giant dispatch, mega comparison mirrors, mega parameter-gradient staging atlases, TensorCube payload copies, and host shuttles are forbidden.

## Production readback boundary

Production payload readback remains zero for post-RMS dX/dGamma, `dAfterAttentionTotal`, actual OProj dW/dContext, actual dQ/dK/dV, and actual gate carriers. Only compact status/parity evidence is allowed.

## Synthetic CPU-f64 RMS oracle

R14 includes a small synthetic RMSNorm fixture. GPU R14 `dX` and `dGamma` are compared against CPU f64. The tiny synthetic outputs may be read back; production payload readback remains zero.

Directional finite difference uses:

```text
L(x) = sum_i dy_i * RMSNorm(x)_i
FD = [L(x + eps*v) - L(x - eps*v)] / (2*eps)
analytic = <dX, v>
```

Both GPU-vs-CPU and directional checks must pass.

## Double-run reproducibility

The complete R14 production chain runs twice without mutation and exact-compares post-RMS dX/dGamma, `dAfterAttentionTotal`, actual OProj dContext/dW tiles, actual dQbase, dDeltaQ H1-H4, shared dK/dV, and gate carriers H1-H4.

Required:

```text
reproducibilityRuns = 2
reproducibilityMatch = 1
```

## Required runtime receipts

```text
r14_parent_r13_r2_receipt.json
r14_post_rms_pending_adoption_receipt.json
r14_post_rms_weight_reacquire_receipt.json
r14_post_rms_backward_receipt.json
r14_post_rms_weight_gradient_receipt.json
r14_after_attention_total_receipt.json
r14_attention_residual_carrier_receipt.json
r14_oproj_actual_backward_receipt.json
r14_oproj_actual_gradient_tiles_receipt.json
r14_actual_dcontext_receipt.json
r14_actual_attention_rebind_receipt.json
r14_actual_attention_gradient_receipt.json
r14_fixture_authority_retirement_receipt.json
r14_r15_handoff_receipt.json
r14_reproducibility_receipt.json
r14_micro_atlas_gc_receipt.json
r14_rms_cpu_f64_oracle_receipt.json
bt_wgsl_post_rmsnorm_oproj_actual_chain_06c_r14_final.json
```

## CLI gates

```text
--require-bt-wgsl-r14-r13-r2-physical-parent
--require-bt-wgsl-r14-post-rms-pending-v1
--require-bt-wgsl-r14-resident-post-rms-weight-reacquire
--require-bt-wgsl-r14-retained-rms-inverse-no-recompute
--require-bt-wgsl-r14-post-rms-exact-vjp
--require-bt-wgsl-r14-post-rms-weight-gradient
--require-bt-wgsl-r14-after-attention-total-merge
--require-bt-wgsl-r14-attention-residual-carrier
--require-bt-wgsl-r14-oproj-actual-backward
--require-bt-wgsl-r14-oproj-actual-dcontext
--require-bt-wgsl-r14-oproj-actual-gradient-tiles
--require-bt-wgsl-r14-r12-actual-dcontext-rebind
--require-bt-wgsl-r14-five-lane-actual-attention-backward
--require-bt-wgsl-r14-r12-fixture-dcontext-retirement
--require-bt-wgsl-r14-r12-fixture-gradient-retirement
--require-bt-wgsl-r14-r15-handoff
--require-bt-wgsl-r14-rms-cpu-f64-oracle
--require-bt-wgsl-r14-rms-directional-finite-difference
--require-bt-wgsl-r14-micro-atlas-tensorcube-preserved
--require-bt-wgsl-r14-fail-closed-numerics-preserved
--require-bt-wgsl-r14-zero-observation-not-failure
--require-bt-wgsl-r14-production-payload-readback-zero
--require-bt-wgsl-r14-zero-forward-attention-recompute
--require-bt-wgsl-r14-zero-checkpoint-reopen
--require-bt-wgsl-r14-zero-training-decoder-clone
--require-bt-wgsl-r14-zero-input-rmsnorm-backward
--require-bt-wgsl-r14-zero-rope-backward
--require-bt-wgsl-r14-zero-qkv-backward
--require-bt-wgsl-r14-zero-deltaq-projector-backward
--require-bt-wgsl-r14-zero-gate-projector-backward
--require-bt-wgsl-r14-zero-optimizer
--require-bt-wgsl-r14-zero-weight-mutation
--require-bt-wgsl-r14-double-run-reproducibility
```

All 33 gates must appear exactly once in both canonical 06C response files and resolve to `true`.

## Physical target

```text
[bt-wgsl-post-rmsnorm-oproj-actual-chain-06c-r14]
r13_r2_physical_parent=1
selected_layers=1
post_rms_pending_adopted=1
post_rms_weight_reacquired=1
post_rms_inverse_recompute=0
post_rms_backward_dispatch>0
post_rms_weight_gradient_dispatch=2
post_rms_gradient_nonfinite=0
post_rms_write_completion=1
dafter_from_post_rms_published=1
dafter_residual_adopted=1
dafter_total_published=1
attention_residual_carrier_published=1
oproj_actual_backward_dispatch=2
oproj_actual_chain_authority=1
oproj_actual_dcontext_published=1
oproj_actual_dw_tiles>0
r13_oproj_candidate_actual_feed=0
r13_oproj_candidate_authority=0
r12_actual_dcontext_rebind=1
g204d_actual_base_dispatch=2
g204d_actual_structural_dispatch=8
actual_dqbase_published=1
actual_deltaq_published=4
actual_shared_dk_published=1
actual_shared_dv_published=1
actual_gate_carriers_published=4
r12_fixture_dcontext_authority=0
r12_fixture_gradient_authority=0
fixture_gradient_r15_feed=0
r15_handoff_ready=1
rms_cpu_f64_oracle=1
rms_directional_finite_difference=1
micro_atlas_tensorcube=1
page_gc_closed=1
production_gradient_payload_readback=0
production_weight_payload_readback=0
forward_attention_recompute=0
checkpoint_reopen=0
training_decoder_clone=0
input_rmsnorm_backward=0
rope_backward=0
qkv_projection_backward=0
deltaq_projector_backward=0
gate_projector_backward=0
optimizer=0
weight_mutation=0
reproducibility_runs=2
reproducibility_match=1
proof_ledger=HOLD
```

`post_rms_gradient_nonzero`, `oproj_actual_gradient_nonzero`, and `actual_attention_gradient_nonzero` are observations only and never determine PASS by themselves.

## Changed source surface

Relative to R13-R2-R3, R14 changes exactly six files:

```text
ADD crates/burn_webgpu_backend/src/base_train_r14_post_rmsnorm_backward.rs
MOD crates/burn_webgpu_backend/src/lib.rs
ADD crates/burn_webgpu_backend/src/shaders/base_train_r14_rmsnorm_backward.wgsl
MOD crates/orchestrator_local/src/base_train_structural_lookahead_decoder_coupling_06c.rs
MOD specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c.args
MOD specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c_full.args
```

## Bake-time verification boundary

The bake environment has no Rust toolchain and no physical WGPU adapter. Bake authority is limited to static/source/archive verification. Rust compile, WGSL validation, GPU execution, synthetic RMS oracle execution, actual OProj publication, five-lane actual attention replay, and the final PASS token remain operator-machine physical authority.

## PASS seal

```text
PASS_ASH_BASETRAIN_BT_WGSL_POST_RMSNORM_OPROJ_ACTUAL_CHAIN_06C_R14
```

The seal requires the complete scope above, including exact post-RMS VJP, actual OProj promotion, actual dContext five-lane rebind, fixture-authority retirement, R15 handoff, fail-closed numerics, zero-as-observation policy, zero production payload readback, zero optimizer/weight mutation, double-run reproducibility, and `proof_ledger=HOLD`.

## Final SSOT

R14 exactly reverses the post-attention RMSNorm using the retained inverse and resident norm weight, merges that result with the FFN residual gradient into `dAfterAttentionTotal`, and uses only that surface as the actual OProj upstream. The resulting actual `dContext` is rebound into the retained BASE+H1-H4 attention tapes, retiring fixture-derived attention gradients from downstream authority. R15 receives only actual-chain post-RoPE Q/K/V gradients and the attention-residual carrier.
