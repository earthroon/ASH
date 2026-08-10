# ASH-BASETRAIN-BT-WGSL-REAL-LOSS-LOGIT-VJP-FINAL-RMSNORM-BACKWARD-06C-R24

## Revision

- Patch ID: `ASH-BASETRAIN-BT-WGSL-REAL-LOSS-LOGIT-VJP-FINAL-RMSNORM-BACKWARD-06C-R24`
- Build revision: `bt-wgsl-real-loss-logit-vjp-final-rmsnorm-backward-06c-r24`
- Physical parent: `ASH-BASETRAIN-BT-WGSL-FINAL-LOGITS-REAL-LOSS-AUTHORITY-06C-R23`
- Next consumer: `R25 REAL-LOSS-SELECTED-LAYER-BACKWARD-REBASE`
- Proof ledger: `HOLD`

## SSOT

R24 consumes the exact live R23 Real Loss Tape and closes the first real-loss backward authority. It replays the exact R23 LM Head vocabulary-wave plan, recomputes only active-row transient logits, forms the exact cross-entropy VJP from retained R23 LogZ and targets, applies loss-mean and logit-scale derivatives exactly once, executes only the R16 TensorCube DX path, deterministically merges per-wave dNormalizedHidden partials, scatters them to canonical B1/Q32/H2048 geometry, and reuses the existing R14 RMSNorm backward executor to publish `REAL dFinalHidden` plus a noncanonical FinalNorm dGamma sidecar.

R24 does **not** publish LM Head parameter gradients, selected-layer real gradients, a canonical gradient atlas, optimizer state, weight mutation, checkpoint state or production training-state authority.

## Physical-parent requirements

```text
r23_physical_parent=1
real_loss_authority=1
final_loss_authority=1
real_loss_backward_authority=0
r24_handoff_ready=1
```

The live `R23RealLossTape` is the authority. Receipt-only reconstruction, target re-derivation, vocabulary re-planning and fixture substitution are forbidden.

R24 binds the exact R23 sequence authority digest, real-loss authority digest, loss-policy digest, LM Head source authority digest, vocabulary-wave-plan digest, active-row map, target IDs, LogZ GPU lease, loss-values GPU lease and LM-head-input hidden lease.

## Hidden semantic boundary

`R23RealLossTape.final_hidden` is semantically **Final RMSNorm output / LM Head input hidden**. It is not the decoder hidden before Final RMSNorm.

```text
r23_final_hidden_semantic_role=LM_HEAD_INPUT_NORMALIZED_HIDDEN
pre_final_hidden_alias_count=0
```

The live sealed geometry remains:

```text
batch=1
seq=32
hidden=2048
valid_token_count=8
active_rows=7
inactive_rows=25
vocab_size=48259
lm_head_binding_mode=UNTIED_LM_HEAD
lm_head_weight_shape=[48259,2048]
```

Dynamic B/Q and production multi-microbatch geometry remain deferred.

## Final RMSNorm backward tape

06B is extended so its existing Final RMSNorm forward uses the same operation's tape-capable path and retains backward witnesses without changing normalized-output authority.

Retained/bound state:

```text
pre_final_hidden pointer/buffer/completion lineage
pre_final_hidden layer/generation
final_norm tensor identity
rms_norm epsilon
final_norm gamma raw GPU alias
forward-epoch inv_rms raw GPU lease
normalized hidden authority digest
```

Required:

```text
final_norm_backward_tape=1
final_norm_gamma_raw_alias=1
final_norm_invrms_tape=1
second_final_norm_checkpoint_read=0
second_final_rmsnorm_output_forward=0
```

The exact pre-final hidden is reacquired read-only from the canonical runtime hidden slot. No host upload, payload readback or mutation is admitted.

The tape extension must preserve the R23 normalized hidden and real-loss semantics. Loss drift caused by the extension is fail-closed.

## Exact vocabulary-wave replay

R24 reuses the exact `R23VocabWavePlan`.

```text
vocab_wave_repartition=0
vocab_wave_gap=0
vocab_wave_overlap=0
peak_lm_head_weight_waves=1
```

Each wave follows:

```text
bounded checkpoint row decode
→ one LM Head weight wave resident
→ active-row logit recompute
→ dLogit VJP
→ R16 TensorCube DX-only
→ ordered dHidden merge
→ completion fence
→ wave GC
```

No full LM Head host materialization or full LM Head GPU residency is required.

## Cross-entropy VJP

For active row `i` and vocabulary item `j`:

```text
p_ij = exp(z_ij - logZ_i)
dZ_ij = (p_ij - 1[j == target_i]) / active_loss_count
```

Current `active_loss_count=7`.

The R23 loss-mean divisor is applied exactly once. No second batch/sequence/active-count division is allowed.

For explicit R23 logit scale:

```text
z = logit_scale × prelogit
dPreLogit = dZ × logit_scale
```

The logit-scale derivative is also applied exactly once. A synthetic non-unit scale canary prevents an identity-scale implementation bug from hiding.

R23 label-smoothing and class-weighting policy remain zero/none.

## Scratch boundary

Only one vocabulary-wave-local transient logits/dLogits surface is permitted.

```text
full_vocab_logits_surface=0
full_dlogits_surface=0
cross_wave_logit_retention=0
cross_wave_dlogit_retention=0
```

No persistent `[7,48259]` or `[32,48259]` logits/gradient surface is admitted.

## LM Head VJP only

For normalized hidden row `i`:

```text
dH_i = Σ_j dPreLogit_ij × W_j
```

The live untied LM Head contains `48259 × 2048 = 98,834,432` parameters. R24 therefore explicitly defers its parameter gradient.

```text
lm_head_weight_gradient_dispatch=0
lm_head_weight_gradient_publication=0
lm_head_bias_gradient_dispatch=0
lm_head_bias_gradient_publication=0
mega_lm_head_gradient_buffer=0
```

LM Head parameter gradients belong to the later full-model gradient-atlas stage.

## R16 TensorCube DX-only reuse

R24 exposes a DX-only wrapper over the already-proven R16 `tensorcube_dx` semantic kernel.

```text
r16_tensorcube_dx_kernel_reused=1
tensorcube_tile=16x16x16
tensorcube_dw_dispatch=0
```

The full R16 linear-backward wrapper must not be used when doing so would also dispatch `tensorcube_dw_tile`.

Current per-wave geometry:

```text
M=7
K=2048
N=vocab_wave_rows
```

Tail lanes may use exact mathematical zero masking. NaN/Inf repair is forbidden.

## dNormalizedHidden merge and BQH scatter

Each vocabulary wave emits a non-authoritative `[7,2048]` dNormalizedHidden partial. Partials merge strictly by ascending vocabulary start.

```text
partial_gradient_authority=0
dnormalized_hidden_ordered_merge=1
global_float_atomic=0
real_dnormalized_hidden_authority=1
```

The merged active derivative is scattered through the exact R23 active-row map into canonical `[1,32,2048]` BQH geometry.

```text
active_row_scatter_count=7
inactive_zero_row_count=25
```

The terminal valid token and padded suffix have exact zero derivative because no next-token loss is defined for them. No synthetic EOS gradient is introduced.

## Final RMSNorm backward

R24 reuses the proven R14 RMSNorm backward executor:

```text
x       = exact pre-final hidden
inv_rms = retained forward-epoch FinalNorm tape
gamma   = exact FinalNorm gamma raw alias
dy      = canonical [1,32,2048] dNormalizedHidden
```

R24 does not redefine R14 RMSNorm mathematics or its CPU-F64 oracle.

The resulting `dGamma[2048]` is retained as a **device-local noncanonical sidecar** only:

```text
final_norm_dgamma_sidecar=1
final_norm_dgamma_canonical_gradient_authority=0
final_norm_dgamma_optimizer_visibility=0
```

R14 `dx` becomes:

```text
REAL dFinalHidden
shape=[1,32,2048]
```

and opens:

```text
real_dnormalized_hidden_authority=1
real_dfinal_hidden_authority=1
real_loss_backward_authority=1
```

`REAL dFinalHidden` receives an R25 owner pin.

## R13-R22 isolation

R24 does not yet feed this gradient into the selected-layer backward stack.

```text
r13_r22_fixture_authority_unchanged=1
selected_layer_real_backward=0
canonical_gradient_atlas_publication=0
optimizer=0
weight_mutation=0
checkpoint_write=0
production_training_state_authority=0
```

R25 is responsible for replacing the deterministic selected-layer upstream fixture with this real authority.

## Status ABI

```text
R24StatusV1
0 = INCOMPLETE
1 = COMPLETE
2 = NONFINITE
3 = LOSS_TAPE_MISMATCH
4 = LINEAGE_MISMATCH
5 = WAVE_COVERAGE_FAILURE
6 = TARGET_GEOMETRY_FAILURE
```

Host success requires `status == 1`. WGSL success explicitly writes status 1; untouched zero is not success.

## Numerical and readback policy

Any nonfinite recomputed logit, softmax term, dLogit, scaled dPreLogit, TensorCube partial, merged dNormalizedHidden, invRMS, RMS reduction, dFinalHidden or dGamma is a hard failure.

Forbidden:

```text
NaN-to-zero
Inf-to-zero
gradient clamp
loss-gradient clamp
silent wave drop
partial wave continuation
```

Production payload readback remains zero for dLogits, dNormalizedHidden, dFinalHidden, dGamma and LM Head weights. Compact status/counters/digests are permitted.

## Oracles

R24 requires:

- GPU vs CPU-F64 small-vocab logit VJP oracle
- non-identity logit-scale canary
- bias-present canary
- target placement in first, middle and final vocabulary waves
- directional finite difference for `dL/dNormalizedHidden`
- existing R14 RMSNorm CPU-F64 oracle
- Final RMSNorm directional finite-difference evidence
- two-run GPU-side exact parity for dNormalizedHidden, dFinalHidden and dGamma

Synthetic payload readback is oracle-only and does not become production payload authority.

## Negative canaries

Exactly 12 fail-closed canaries:

1. target ID out of range
2. empty active-row set
3. target cardinality mismatch
4. LogZ shape mismatch
5. LM Head weight shape mismatch
6. vocabulary-wave range overflow
7. zero-sized vocabulary wave
8. nonfinite logit scale
9. duplicate scatter row
10. scatter row out of range
11. scatter gradient shape mismatch
12. nonfinite LogZ

Each passes only if the injected invalid condition is rejected.

## Receipt atlas

Exactly nine ordered receipt waves:

```text
0 R23 parent and loss tape
1 FinalNorm backward tape and lineage
2 LM Head exact vocab-wave replay
3 logit VJP and TensorCube DX-only
4 dNormalized merge and BQH scatter
5 Final RMSNorm backward and dGamma sidecar
6 fail-closed lifetime/readback boundary
7 oracles, negative canaries and reproducibility
8 R25 boundary, PASS and HOLD seal
```

```text
receipt_atlas_waves=9
monolithic_final_json=0
proof_ledger=HOLD
```

## CLI gate authority

R24 has exactly **136** `--require-bt-wgsl-r24-*` gates. The exact gate set is identical and exact-once across:

```text
runtime R24 validation      136 / 136
short args                  136 / 136
full args                   136 / 136
resolved-args repair input  136 / 136
```

The concrete gate strings in those four implementation surfaces are the CLI SSOT. No silent missing/default-true R24 gate is admitted.

## Expected physical summary

```text
r23_physical_parent=1
real_loss_authority=1
final_loss_authority=1
r23_loss_tape_adopted=1
lm_head_binding_mode=UNTIED_LM_HEAD
batch=1
seq=32
hidden=2048
active_rows=7
inactive_rows=25
vocab_size=48259
vocab_wave_count=3
vocab_wave_repartition=0
backward_logit_recompute=1
decoder_forward_recompute=0
final_rmsnorm_forward_recompute=0
full_vocab_logits_surface=0
full_dlogits_surface=0
loss_mean_vjp_scale_application_count=1
logit_scale_vjp_application_count=1
r16_tensorcube_dx_kernel_reused=1
tensorcube_tile=16x16x16
tensorcube_dw_dispatch=0
lm_head_weight_gradient_dispatch=0
lm_head_bias_gradient_dispatch=0
dnormalized_hidden_wave_partial_count=3
dnormalized_hidden_ordered_merge=1
global_float_atomic=0
real_dnormalized_hidden_authority=1
canonical_bqh_dy_rows=32
active_row_scatter_count=7
inactive_zero_row_count=25
final_norm_backward_tape=1
final_norm_source_hidden_reacquire=1
final_norm_gamma_raw_alias=1
final_norm_invrms_tape=1
second_final_norm_checkpoint_read=0
second_final_rmsnorm_output_forward=0
r14_rmsnorm_backward_executor_reused=1
final_rmsnorm_backward_dispatch=1
final_rmsnorm_dgamma_sidecar=1
final_rmsnorm_dgamma_canonical_authority=0
real_dfinal_hidden_authority=1
real_loss_backward_authority=1
logit_vjp_cpu_f64_oracle=1
logit_vjp_directional_finite_difference=1
final_rmsnorm_cpu_f64_oracle=1
final_rmsnorm_directional_finite_difference=1
nonidentity_logit_scale_canary=1
bias_present_canary=1
target_first_middle_last_wave_canary=1
negative_canaries=12
status_abi=R24StatusV1
status_success_value=1
peak_lm_head_weight_waves=1
lm_head_weight_gradient_publication=0
r13_r22_fixture_authority_unchanged=1
real_dfinal_hidden_r25_owner_pin=1
production_gradient_payload_readback=0
production_weight_payload_readback=0
selected_layer_real_backward=0
canonical_gradient_atlas_publication=0
optimizer=0
weight_mutation=0
checkpoint_write=0
production_training_state_authority=0
reproducibility_runs=2
reproducibility_match=1
r25_handoff_ready=1
receipt_atlas_waves=9
monolithic_final_json=0
proof_ledger=HOLD
```

## PASS seal

```text
PASS_ASH_BASETRAIN_BT_WGSL_REAL_LOSS_LOGIT_VJP_FINAL_RMSNORM_BACKWARD_06C_R24
```

Publication requires R23 real-loss parent binding, exact loss-tape adoption, exact vocabulary-wave replay, active-row CE VJP, mean and logit-scale application exactly once, R16 TensorCube DX-only with zero DW, deterministic dHidden merge, canonical BQH scatter, R14 RMSNorm backward reuse, noncanonical dGamma sidecar, real dNormalizedHidden, real dFinalHidden, real-loss backward authority, fail-closed numerics, zero production gradient payload readback, oracle/negative/reproducibility closure, zero selected-layer real backward, zero gradient-atlas publication, zero optimizer/weight/checkpoint mutation, R25 handoff and `proof_ledger=HOLD`.

## Authority transition

```text
R23 REAL LOSS
     │
     ▼
LogZ + targets + exact LM Head vocab waves
     │
     ▼
wave-local dLogits
     │
     ▼
R16 TensorCube DX-only
     │
     ▼
REAL dNormalizedHidden [7,2048]
     │
     ▼
canonical BQH scatter [1,32,2048]
     │
     ▼
R14 Final RMSNorm backward
     │
     ├── FinalNorm dGamma noncanonical sidecar
     │
     ▼
REAL dFinalHidden
     │
     ▼
R25
```
