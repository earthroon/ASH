# ASH-BASETRAIN-BT-WGSL-NEOX-ROPE-QKV-INPUT-RMSNORM-BACKWARD-06C-R15

## Revision identity

```text
Patch ID: ASH-BASETRAIN-BT-WGSL-NEOX-ROPE-QKV-INPUT-RMSNORM-BACKWARD-06C-R15
Build revision: bt-wgsl-neox-rope-qkv-input-rmsnorm-backward-06c-r15
Physical parent: ASH-BASETRAIN-BT-WGSL-POST-RMSNORM-OPROJ-ACTUAL-CHAIN-06C-R14
Corrected source parent: R14-R1-P2
Proof ledger: HOLD
```

## Scope seal

```text
R14 Physical Parent /
R14 Actual dContext Chain Parent /
R14 Fixture Gradient Retirement Parent /
R14ToR15 Exact Handoff Adoption /
Actual dQbase Post-RoPE Authority /
Actual Shared dK Post-RoPE Authority /
Actual Shared dV Authority /
Attention Residual Carrier Authority /
NeoX RoPE Exact VJP /
Q RoPE Backward /
K RoPE Backward /
V No-RoPE Preservation /
Exact Forward RoPE Coefficient Identity /
Zero Second Attention Scale /
Zero GQA Head Expansion /
Q/K Pre-RoPE Gradient Publication /
Canonical Q Projection Backward /
Canonical K Projection Backward /
Canonical V Projection Backward /
Canonical OUT_IN Weight Layout /
Actual Q/K/V Weight-Gradient Tile Publication /
Deterministic Q+K+V Input-Gradient Merge /
Input RMSNorm Retained-Inverse Authority /
Input RMSNorm Exact VJP /
Input RMSNorm Weight Gradient /
No Input RMS Forward Recomputation /
Attention Residual Gradient Reuse /
dInputHiddenTotal Deterministic Merge /
Canonical Selected-Layer Input Gradient Authority /
R14 Structural DeltaQ/Gate Carrier Preservation /
R13 Linear Backward Executor Reuse /
R14 RMSNorm Backward Executor Reuse /
R13 Add2 Executor Reuse /
Micro-Atlas TensorCube Transport Preservation /
Bounded QKV Gradient Tiles /
Commit-GC Preservation /
NeoX CPU-f64 Oracle /
NeoX Directional Finite-Difference /
Input-RMS CPU-f64 Oracle /
Input-RMS Directional Finite-Difference /
GQA Shape-Parity Canary /
Fail-Closed Numerics /
Zero-Is-Observation Not Failure /
No Gradient Fabrication /
Production Payload Readback Zero /
Atlas Parallel Wave Streaming Receipt /
No Monolithic Final json! Macro /
No Forward/QKV Recomputation /
No Checkpoint Reopen /
No TrainingBackend Decoder Clone /
No Structural Projector/Head Backward /
No Gradient Atlas /
No Optimizer /
No Weight Mutation /
Final Loss Authority Deferred /
Double-Run Reproducibility /
Proof Ledger HOLD Seal
```

## One-line SSOT

R15 consumes only R14 actual-chain base Q/K/V gradients, applies the exact transpose VJP of the production NeoX split-half RoPE to Q and K without touching V or structural DeltaQ/gate carriers, executes canonical Q/K/V projection backward against the retained selected-layer normalized input and resident Q/K/V weights, passes the deterministic Q→K→V merged projection-input gradient through the retained-inverse input RMSNorm VJP, and finally merges that result with R14's attention residual carrier to publish canonical `dInputHiddenTotal`.

## Authority qualification

`actual` means a connected derivative chain through the canonical selected-layer forward surfaces. R15 does not promote the deterministic upstream fixture to final-loss authority.

```text
final_loss_authority = 0
dfinal_deterministic_fixture_lineage = 1
optimizer = 0
weight_mutation = 0
proof_ledger = HOLD
```

## Current admitted geometry

```text
selectedLayerCount = 1
B = 1
Q = 32
hiddenWidth = 2048
qHeads = 32
kvHeads = 4
headDim = 64
qProjectionWidth = 2048
kProjectionWidth = 256
vProjectionWidth = 256
```

## R14 handoff

R15 consumes exactly:

```text
dInputHiddenAttentionResidual
dQbasePostRopeActual
dKsharedPostRopeActual
dVsharedActual
```

R15 carries through unchanged and does not consume:

```text
dDeltaQ_H1..H4Actual
dGate_H1..H4Actual
```

## Forward-tape authority

The selected-layer R10 tape already retains `input_hidden`, `input_rms_inv`, `normalized_hidden`, `q_pre_rope`, `k_pre_rope`, `canonical_v`, `q_post_rope`, and `k_post_rope`. R15 reuses these read-only. Decoder forward, QKV forward, input-RMS forward, and checkpoint reopen are prohibited.

## Exact NeoX VJP

Production split-half identity for `half=headDim/2`, `a=x[j]`, `b=x[j+half]`:

```text
yA = a*cos - b*sin
yB = a*sin + b*cos
```

with the same production coefficient path:

```text
position = position_ids[token]
exponent = -2 * pair_index / headDim
frequency = rope_theta ^ exponent
angle = position * frequency
```

R15 transpose VJP:

```text
dA = dYA*cos + dYB*sin
dB = -dYA*sin + dYB*cos
```

Q and K dispatch independently with native head cardinalities. V has no RoPE backward. Non-null rope scaling is not silently approximated and fails closed.

Required:

```text
v_rope_backward_dispatch = 0
second_attention_scale = 0
gqa_kv_head_expansion = 0
```

K/V remain 4-head canonical GQA gradients and are never expanded to 32 heads.

## Q/K/V projection backward

R15 reuses the R13 linear-backward executor. Canonical weight layout remains `W[out,in]`.

```text
Qpre = Xn * Wq^T
Kpre = Xn * Wk^T
V    = Xn * Wv^T

dX_Q = dQpre * Wq
dW_Q = dQpre^T * Xn

dX_K = dKpre * Wk
dW_K = dKpre^T * Xn

dX_V = dV * Wv
dW_V = dV^T * Xn
```

Current shapes:

```text
Wq = [2048,2048]
Wk = [256,2048]
Wv = [256,2048]
```

No QKV bias gradient is fabricated when the resident decoder block has no bias authority. With the current admitted 1024-row dW policy, expected tiles are Q=2, K=1, V=1.

## Deterministic QKV input merge

```text
dNormalizedInputFromQKV = ((dX_Q + dX_K) + dX_V)
```

Merge order is fixed `Q -> K -> V` using the admitted R13 add executor. Unordered floating-point atomic merging is forbidden.

## Input RMSNorm backward

R15 reuses the R14 exact retained-inverse RMSNorm executor under role `INPUT_RMSNORM`.

```text
a[t,i] = dy[t,i] * gamma[i]
rowDot[t] = sum_j a[t,j] * x[t,j]

dInputHiddenFromInputNorm[t,i]
= r[t] * (a[t,i] - x[t,i] * (r[t]^2/H) * rowDot[t])

dInputNormGamma[i]
= sum_t dy[t,i] * x[t,i] * r[t]
```

Production inverse recomputation, silent epsilon replacement, and alternate numerical policy are prohibited.

## Canonical dInputHiddenTotal

```text
dInputHiddenTotal
= dInputHiddenAttentionResidual
+ dInputHiddenFromInputNorm
```

Merge order is fixed `ATTENTION_RESIDUAL -> INPUT_RMSNORM`. Publication occurs only after Q/K/V backward, input-RMS backward, completion, finite checks, and the final merge pass.

## Zero and fail-closed policy

R15 intentionally has no `BTR15GradientZero` error class. Finite all-zero output after exact completion/coverage/lineage/reproducibility is a valid observation.

Forbidden: sigma/log/lambda amplification, epsilon gradient fabrication, NaN/Inf clamp, gradient clamp, partial-row continuation, or silent row zeroing.

## Micro-Atlas / TensorCube transport

Large linear/RMS/parity surfaces preserve the R13-R2 path:

```text
1D logical surface
-> bounded Micro Atlas page
-> TensorCube residency map
-> direct canonical-buffer execution
-> completion -> commit -> GC eligibility -> release
```

TensorCube remains scheduling/residency authority in R15, not R16 matmul-compute authority. Payload copy and host shuttle remain zero.

## Production readback boundary

Production gradient/weight payload readback remains zero for pre-RoPE gradients, Q/K/V dx and dW, merged normalized-input gradient, input-RMS dx/dgamma, and `dInputHiddenTotal`. Only compact status/parity evidence is allowed. Synthetic oracle readback is isolated from production authority.

## Oracles

R15 adds a synthetic asymmetric-GQA NeoX GPU↔CPU-f64 VJP oracle plus directional finite difference:

```text
L(x) = <dy, RoPE(x)>
FD = [L(x+eps*v)-L(x-eps*v)]/(2*eps)
AN = <dX,v>
```

It separately validates Q and K shapes with `qHeads != kvHeads`. Input RMSNorm reuses the R14 GPU↔CPU-f64 oracle and directional finite-difference method.

## Double-run reproducibility

The complete R15 production chain executes twice without mutation and exact-compares Q/K pre-RoPE gradients, Q/K/V projection dx and dW tiles, Q+K and Q+K+V merges, input-RMS dx/dgamma, and `dInputHiddenTotal`.

```text
reproducibility_runs = 2
reproducibility_match = 1
```

## Atlas final receipt

The final R15 receipt is not a giant `json!({...})`. It uses seven ordered Atlas waves with parallel lane construction and deterministic streaming merge:

```text
wave ordinal -> lane ordinal -> lexicographic key
receipt_atlas_waves = 7
parallel_receipt_lane_build = 1
streaming_receipt_merge = 1
deterministic_receipt_merge = 1
monolithic_final_json = 0
```

Duplicate lane/root/reserved keys fail closed.

## CLI authority gates

Exactly 46 R15 gates are required exactly once in both canonical 06C response files and in regenerated `resolved.args`:

```text
--require-bt-wgsl-r15-r14-physical-parent
--require-bt-wgsl-r15-r14-exact-handoff
--require-bt-wgsl-r15-selected-layer-forward-tape
--require-bt-wgsl-r15-rope-coefficient-authority
--require-bt-wgsl-r15-neox-q-exact-vjp
--require-bt-wgsl-r15-neox-k-exact-vjp
--require-bt-wgsl-r15-v-no-rope
--require-bt-wgsl-r15-zero-second-attention-scale
--require-bt-wgsl-r15-zero-gqa-kv-head-expansion
--require-bt-wgsl-r15-q-projection-backward
--require-bt-wgsl-r15-k-projection-backward
--require-bt-wgsl-r15-v-projection-backward
--require-bt-wgsl-r15-q-weight-gradient-tiles
--require-bt-wgsl-r15-k-weight-gradient-tiles
--require-bt-wgsl-r15-v-weight-gradient-tiles
--require-bt-wgsl-r15-qkv-input-gradient-deterministic-merge
--require-bt-wgsl-r15-input-rms-retained-inverse
--require-bt-wgsl-r15-input-rms-exact-vjp
--require-bt-wgsl-r15-input-rms-weight-gradient
--require-bt-wgsl-r15-input-hidden-total-merge
--require-bt-wgsl-r15-input-hidden-total-authority
--require-bt-wgsl-r15-structural-deltaq-preserved
--require-bt-wgsl-r15-structural-gate-carriers-preserved
--require-bt-wgsl-r15-neox-cpu-f64-oracle
--require-bt-wgsl-r15-neox-directional-finite-difference
--require-bt-wgsl-r15-input-rms-cpu-f64-oracle
--require-bt-wgsl-r15-input-rms-directional-finite-difference
--require-bt-wgsl-r15-gqa-shape-canary
--require-bt-wgsl-r15-micro-atlas-tensorcube-preserved
--require-bt-wgsl-r15-fail-closed-numerics-preserved
--require-bt-wgsl-r15-zero-observation-not-failure
--require-bt-wgsl-r15-production-payload-readback-zero
--require-bt-wgsl-r15-atlas-wave-streaming-receipt
--require-bt-wgsl-r15-zero-monolithic-final-json
--require-bt-wgsl-r15-zero-forward-decoder-recompute
--require-bt-wgsl-r15-zero-qkv-forward-recompute
--require-bt-wgsl-r15-zero-checkpoint-reopen
--require-bt-wgsl-r15-zero-training-decoder-clone
--require-bt-wgsl-r15-zero-deltaq-projector-backward
--require-bt-wgsl-r15-zero-gate-projector-backward
--require-bt-wgsl-r15-zero-structural-head-backward
--require-bt-wgsl-r15-final-loss-authority-deferred
--require-bt-wgsl-r15-zero-gradient-atlas
--require-bt-wgsl-r15-zero-optimizer
--require-bt-wgsl-r15-zero-weight-mutation
--require-bt-wgsl-r15-double-run-reproducibility
```

The resolved-args repair utility enforces exact cardinality for all 46 R15 keys, preventing a stale pre-R15 response file from being admitted.

## Required receipts

```text
r15_parent_r14_receipt.json
r15_r14_handoff_adoption_receipt.json
r15_forward_tape_reacquire_receipt.json
r15_rope_coefficient_authority_receipt.json
r15_neox_q_backward_receipt.json
r15_neox_k_backward_receipt.json
r15_v_identity_gradient_receipt.json
r15_q_projection_backward_receipt.json
r15_k_projection_backward_receipt.json
r15_v_projection_backward_receipt.json
r15_q_weight_gradient_tiles_receipt.json
r15_k_weight_gradient_tiles_receipt.json
r15_v_weight_gradient_tiles_receipt.json
r15_qkv_input_gradient_merge_receipt.json
r15_input_rms_backward_receipt.json
r15_input_rms_weight_gradient_receipt.json
r15_input_hidden_total_receipt.json
r15_structural_carrier_preservation_receipt.json
r15_neox_cpu_f64_oracle_receipt.json
r15_neox_directional_fd_receipt.json
r15_input_rms_cpu_f64_oracle_receipt.json
r15_input_rms_directional_fd_receipt.json
r15_gqa_shape_canary_receipt.json
r15_micro_atlas_gc_receipt.json
r15_reproducibility_receipt.json
bt_wgsl_neox_rope_qkv_input_rmsnorm_backward_06c_r15_final.json
```

## Expected physical terminal summary

```text
[bt-wgsl-neox-rope-qkv-input-rmsnorm-backward-06c-r15]
r14_physical_parent=1 selected_layers=1 r14_handoff_adopted=1
q_post_rope_actual_adopted=1 k_post_rope_actual_adopted=1 v_actual_adopted=1
rope_q_backward_dispatch=2 rope_k_backward_dispatch=2 v_rope_backward_dispatch=0
rope_policy_identity_match=1 second_attention_scale=0 gqa_kv_head_expansion=0
q_pre_rope_published=1 k_pre_rope_published=1
qproj_backward_dispatch=2 kproj_backward_dispatch=2 vproj_backward_dispatch=2
q_dw_tiles=2 k_dw_tiles=1 v_dw_tiles=1
qkv_input_merge_published=1 input_rms_inverse_recompute=0
input_rms_gradient_nonfinite=0 input_rms_write_completion=1
input_rms_dx_published=1 input_rms_dgamma_published=1
attention_residual_carrier_adopted=1
dinput_hidden_total_published=1 dinput_hidden_total_authority=1
structural_deltaq_consumed=0 structural_gate_carrier_consumed=0
structural_deltaq_mutation=0 structural_gate_mutation=0
neox_cpu_f64_oracle=1 neox_directional_finite_difference=1
input_rms_cpu_f64_oracle=1 input_rms_directional_finite_difference=1
gqa_shape_canary=1 micro_atlas_tensorcube=1 page_gc_closed=1
production_gradient_payload_readback=0 production_weight_payload_readback=0
forward_decoder_recompute=0 qkv_forward_recompute=0 checkpoint_reopen=0 training_decoder_clone=0
deltaq_projector_backward=0 gate_projector_backward=0 structural_head_backward=0
gradient_atlas=0 optimizer=0 weight_mutation=0
final_loss_authority=0 dfinal_deterministic_fixture_lineage=1
reproducibility_runs=2 reproducibility_match=1
receipt_atlas_waves=7 parallel_receipt_lane_build=1 streaming_receipt_merge=1 deterministic_receipt_merge=1 monolithic_final_json=0
proof_ledger=HOLD
```

## Source surface

Relative to R14-R1-P2, R15 changes exactly seven files:

```text
ADD crates/burn_webgpu_backend/src/base_train_r15_neox_rope_backward.rs
ADD crates/burn_webgpu_backend/src/shaders/base_train_r15_neox_rope_backward.wgsl
MOD crates/burn_webgpu_backend/src/lib.rs
MOD crates/orchestrator_local/src/base_train_structural_lookahead_decoder_coupling_06c.rs
MOD specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c.args
MOD specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c_full.args
MOD tools/repair_r13r2r2_resolved_args.ps1
```

The repair-script change is response-file preflight safety; it does not alter the numerical R15 chain.

## Physical verification boundary

The bake environment has no project Rust toolchain or physical WGPU adapter. Static source/diff/archive checks are bake authority only. Rust/WGSL compilation, GPU dispatch, oracle execution, exact reproducibility, and final PASS remain operator-machine physical authority.

## PASS seal

```text
PASS_ASH_BASETRAIN_BT_WGSL_NEOX_ROPE_QKV_INPUT_RMSNORM_BACKWARD_06C_R15
```

The full runtime token additionally seals exact parent/handoff lineage, zero second attention scale, zero GQA head expansion, Q/K/V backward/tile authority, deterministic merges, retained-inverse input RMSNorm, structural carrier isolation, fail-closed numerics, zero production readback, seven-wave receipt, final-loss authority deferred, and double-run reproducibility.

## Next boundary

R16 may accelerate already-admitted linear backward mathematics with TensorCube compute but cannot change R13-R15 equations, weight layout, merge order, zero policy, or authority. R17 later consumes the preserved structural DeltaQ and gate carriers.

## Final SSOT

R15 reverses only the canonical base decoder input path. It transforms R14 actual Q/K post-RoPE gradients through the exact production NeoX transpose VJP, preserves canonical shared V, reuses the admitted linear backward executor for Q/K/V, merges their normalized-input gradients in fixed Q→K→V order, reuses the retained-inverse exact RMSNorm VJP, and finally combines that result with the R14 attention-residual carrier to publish canonical selected-layer `dInputHiddenTotal`. Structural DeltaQ/gate carriers remain untouched for R17, and final-loss authority remains deferred.
