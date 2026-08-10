# ASH-BASETRAIN-BT-WGSL-REAL-LOSS-SELECTED-LAYER-BACKWARD-REBASE-06C-R25

## Revision

- Patch ID: `ASH-BASETRAIN-BT-WGSL-REAL-LOSS-SELECTED-LAYER-BACKWARD-REBASE-06C-R25`
- Build revision: `bt-wgsl-real-loss-selected-layer-backward-rebase-06c-r25`
- Physical parent: `ASH-BASETRAIN-BT-WGSL-REAL-LOSS-LOGIT-VJP-FINAL-RMSNORM-BACKWARD-06C-R24`
- Next consumer: `R26 REAL-GRADIENT-ATLAS-PRODUCTION-FIRST-COMMIT`
- Proof ledger: `HOLD`

## SSOT

R25 consumes the exact R24 `REAL dFinalHidden` GPU authority and reruns the already-proven R13→R18 selected-final-layer backward mathematics with that real upstream. It does not introduce a new derivative, new forward path, new optimizer rule, or new parameter identity. The production-selected backward origin becomes `REAL_LOSS`; the deterministic dFinal fixture remains historical validation material only.

R25 closes exactly one scope: real-loss-lineaged selected-layer backward. The selected-layer parameter inventory remains 27 parameters / 42 linear tiles / 2 RMS vectors / 44 GPU gradient leases. R25 validates those sources with the existing R19 builder as a **noncanonical candidate descriptor** only. R19 canonical gradient-atlas publication, R20 accumulation, R21 optimizer, R22 production commit, full-model gradients, weight mutation and checkpoint writing remain closed.

## Parent authority

R24 must physically provide:

```text
real_loss_authority=1
real_loss_backward_authority=1
real_dfinal_hidden_authority=1
r25_handoff_ready=1
status_success_value=1
```

R25 binds the exact R24 final receipt PASS token and exact R24 `REAL dFinalHidden` lease. The current sealed geometry is `B1/Q32/H2048/F32` with 65,536 elements. Receipt-only reconstruction, CPU re-creation, stale lease reuse, silent zero substitution and deterministic-fixture fallback are forbidden.

## External upstream entry

The canonical R25 entry is an explicit `R25RealUpstreamBindingV1`. It validates dtype and geometry and carries the exact raw GPU lease plus a binding digest. No scale is applied at this boundary. R24 already applied CE mean and logit-scale derivatives exactly once.

```text
production_dfinal_fixture_creation=0
production_dfinal_fixture_consumption=0
fixture_to_real_upstream_promotion=0
upstream_gradient_scale_application_count=0
loss_recompute=0
logit_recompute=0
lm_head_backward=0
final_rmsnorm_rebackward=0
```

The historical deterministic dFinal fixture remains available only for a binding-identity oracle. That oracle proves the new external-upstream adapter is payload-preserving and zero-readback; it does not promote historical fixture gradients to real authority.

## Selected layer and forward tape

The selected layer is inherited from the exact parent forward/backward tape lineage. No hardcoded final-layer index is introduced. R25 requires one selected layer and preserves the exact layer identity, weight generation, hidden generation, weight-pointer identity, decoder-block identity and completion lineage.

The R13→R18 real replay reuses the retained forward tapes for FFN, Post-RMSNorm, Stage12/OProj, Q/K/V, NeoX/RoPE, Input-RMSNorm, DeltaQ/Gate projectors, structural cubes, factor projectors and horizon heads.

Backward-required owner pins remain alive through R25. The current frozen tape envelope is:

```text
base owner pins                16
structural projection pins     24
R18 horizon pins                8
R18 shared-factor pins          6
---------------------------------
total                           54
```

No decoder, attention, QKV, factor or horizon forward recomputation is admitted. Checkpoint reopen and selected-layer weight reload are zero.

## R13 real upstream replay

R13 is re-executed with `R24 REAL dFinalHidden` in place of the historical deterministic fixture. The exact existing R13 FFN mathematics is reused:

```text
REAL dFinalHidden
→ residual split
→ DownProj backward
→ exact SwiGLU VJP
→ GateProj backward
→ UpProj backward
→ deterministic Gate+Up input merge
→ Post-RMS backward boundary
```

The historical R13 OProj fixture executor probe is retained solely as noncanonical executor-validation work. It does not feed R14 or any real gradient authority:

```text
r13_oproj_fixture_validation_dispatch=2
production_oproj_fixture_candidate_authority=0
```

Zero gradient is a valid observation after complete finite writes; nonzero gradient is not a correctness precondition.

## R14 actual chain replay

R14 reuses the exact physical path already admitted by the historical chain:

```text
Post-Attention RMSNorm VJP
→ residual merge
→ actual OProj backward
→ actual dContext
→ base + H1/H2/H3/H4 attention backward
```

Historical R12 fixture dContext and fixture-derived attention gradient authority remain retired. No branch-local K/V parameter authority is created.

## R15 replay

R15 reuses the exact NeoX/RoPE/QKV/Input-RMS backward path:

```text
Q NeoX transpose VJP
K NeoX transpose VJP
V zero RoPE VJP
Q/K/V projection backward
Q+K+V input merge
Input RMSNorm VJP
after-attention residual merge
```

Second attention scale remains zero. GQA K/V expansion remains zero. The exact retained Input-RMS inverse and weight authorities are reused.

## R16 TensorCube correctness replay

R25 reruns the seven established TensorCube linear backward roles with the real upstream-derived intermediates:

```text
DownProj
GateProj
UpProj
OProj
QProj
KProj
VProj
```

TensorCube policy remains F32 input / F32 weight / F32 accumulation and `16×16×16` tiles. Structural TensorCube scope is not expanded.

R16-R1 performance measurement is **not rerun** in R25. The already-physical performance authority (`FASTER_PROMOTABLE`, preferred backend `TENSORCUBE`) is inherited. R25 correctness does not depend on a new performance result.

## R17 structural replay

R17 consumes exactly four real DeltaQ carriers and four real Gate carriers. It reuses the four horizon DeltaQ projector VJPs, four gate-transfer VJPs and four gate-projector backward paths. Projection-bias gradients remain absent. Structural inverse RoPE remains zero.

A mathematically zero gate-source gradient remains a valid observation and is never fabricated into a nonzero gradient.

## R18 factor/head/residual replay

R18 preserves the exact structural topology:

```text
4 horizons
6 shared factors
24 factor-source gradients
24 horizon-local shared-factor dW partials
6 canonical shared-factor dW outputs
4 horizon-head dW outputs
```

Shared-factor reduction order is H1→H2→H3→H4. Structural residual reduction order is H1→H2→H3→H4. The complete selected-layer input gradient is produced by deterministic `base then structural` merge and receives `REAL_LOSS` origin.

## Real selected-layer gradient inventory

R25 inventories the real replay outputs using the existing R19 structural validator without publishing R19 canonical authority. Exact current scope:

```text
canonical parameter identities = 27
base parameters                 = 9
structural parameters           = 18
linear gradient tiles           = 42
RMS gradient vectors            = 2
GPU gradient payload leases     = 44
logical scalar count            = 50,560,768
logical F32 bytes               = 202,243,072
```

The candidate descriptor must prove zero parameter gaps, zero duplicate parameters, zero tile gaps, zero tile overlaps, zero gradient/weight alias, zero payload copy and zero production payload readback.

The resulting R19-shaped object is a **candidate validation envelope**, not canonical R19 publication:

```text
canonical_gradient_atlas_publication=0
```

R26 owns the real canonical descriptor promotion.

## Excluded gradients

R25 selected-layer registry excludes:

```text
R24 FinalNorm dGamma sidecar
LM Head parameter gradient
Embedding gradient
bias gradient
complete dInput as parameter gradient
```

The R24 FinalNorm dGamma sidecar remains model-level, noncanonical state. LM Head and embedding gradients remain deferred to the later full-model gradient stage.

## R26 ownership handoff

All 44 real gradient leases remain pinned for R26. The real complete selected-layer dInput remains a valid backward boundary for later reverse-layer work.

R26 receives:

```text
R25 real selected-layer authority
REAL_LOSS origin seal
27 exact parameter identities
44 real GPU gradient leases
selected-layer identity and generation lineage
complete real dInputHidden
```

R25 itself performs no accumulation, norm, clipping, optimizer, weight mutation, checkpoint write, or production training-state promotion.

## Status and fail-closed policy

```text
R25StatusV1
0 = INCOMPLETE
1 = COMPLETE
2 = NONFINITE
3 = R24_LINEAGE_MISMATCH
4 = FORWARD_TAPE_LINEAGE_MISMATCH
5 = FIXTURE_AUTHORITY_LEAK
6 = PARAMETER_COVERAGE_FAILURE
7 = GRADIENT_COVERAGE_FAILURE
```

Success is 1, never untouched 0.

Forbidden:

```text
NaN → 0
Inf → 0
missing gradient → zero
fixture gradient → real gradient
silent backend fallback
gradient clamp
silent forward recompute
host gradient concatenation
```

Production gradient, weight and forward-tape payload readback remain zero.

## Oracles and negative canaries

R25 runs:

- upstream binding identity oracle using the historical deterministic fixture, GPU-side exact parity, zero payload readback
- double-run reproducibility inside the replayed backward stages
- deterministic candidate-atlas rebuild parity
- 15 fail-closed metadata/lineage/coverage canaries

The binding oracle scope is explicitly `UPSTREAM_BINDING_IDENTITY`. Historical R13-R18 receipt format reused under `r25_real_chain/` is noncanonical diagnostic output; only the R25 final receipt may assert `REAL_LOSS` origin.

## Receipt atlas

Exactly nine ordered R25 receipt waves:

```text
0 R24 parent / REAL dFinal / selected layer
1 forward tape lineage / owner pins / generation
2 R13 FFN / R14 Post-RMS + OProj + actual attention
3 R15 NeoX / RoPE / QKV / Input-RMS
4 R16 TensorCube seven base roles
5 R17 DeltaQ/Gate / R18 factor/head/residual
6 27 real parameter sources / 44 leases / complete dInput
7 binding oracle / negative canaries / reproducibility
8 zero atlas/optimizer / R26 handoff / PASS / HOLD
```

```text
receipt_atlas_waves=9
monolithic_final_json=0
proof_ledger=HOLD
```

## CLI gate authority

R25 contains exactly **148** required gates. The exact set is identical and exact-once across runtime validation, short args, full args and resolved-args repair input. The concrete `--require-bt-wgsl-r25-*` strings in those four implementation surfaces are the CLI SSOT; missing or default-true R25 gates are forbidden.

## Expected physical summary

```text
r24_physical_parent=1
real_loss_authority=1
real_loss_backward_authority=1
real_dfinal_hidden_adopted=1
real_dfinal_hidden_shape_b=1
real_dfinal_hidden_shape_q=32
real_dfinal_hidden_shape_h=2048
production_dfinal_fixture_creation=0
production_dfinal_fixture_consumption=0
fixture_to_real_upstream_promotion=0
selected_layer_count=1
selected_layer_identity_match=1
forward_tape_owner_pin_extension_to_r25=1
forward_tape_lineage_match=1
decoder_forward_recompute=0
attention_forward_recompute=0
qkv_forward_recompute=0
checkpoint_reopen=0
checkpoint_weight_reload=0
upstream_gradient_scale_application_count=0
loss_recompute=0
lm_head_backward=0
final_rmsnorm_rebackward=0
r13_external_upstream_entry=1
r13_oproj_fixture_validation_dispatch=2
production_oproj_fixture_candidate_authority=0
r13_ffn_backward_reused=1
r14_actual_chain_reused=1
r15_qkv_input_rms_backward_reused=1
r16_preferred_backend=TENSORCUBE
r16_tensorcube_math_frozen=1
r16_tensorcube_role_count=7
r16_performance_requalification=0
r17_deltaq_carrier_count=4
r17_gate_carrier_count=4
r18_horizon_count=4
r18_factor_count=6
r18_factor_source_gradient_count=24
r18_shared_factor_dw_count=6
r18_horizon_head_dw_count=4
complete_selected_layer_dinput_authority=1
complete_selected_layer_dinput_origin=REAL_LOSS
selected_layer_gradient_origin=REAL_LOSS
dfinal_deterministic_fixture_lineage=0
gradient_origin_deterministic_fixture=0
canonical_parameter_count=27
base_parameter_count=9
structural_parameter_count=18
linear_gradient_tile_count=42
rms_gradient_vector_count=2
gradient_payload_lease_count=44
parameter_gap=0
parameter_duplicate=0
gradient_tile_gap=0
gradient_tile_overlap=0
gradient_weight_alias=0
r24_final_norm_dgamma_selected_registry_entry=0
lm_head_gradient_entry_count=0
embedding_gradient_entry_count=0
bias_gradient_entry_count=0
complete_dinput_parameter_entry_count=0
canonical_gradient_atlas_publication=0
gradient_accumulation_dispatch=0
global_norm_dispatch=0
gradient_clip_dispatch=0
optimizer_candidate=0
optimizer_commit=0
weight_mutation=0
checkpoint_write=0
production_training_state_authority=0
full_model_gradient_authority=0
fixture_binding_equivalence_oracle=1
fixture_equivalence_scope=UPSTREAM_BINDING_IDENTITY
fixture_equivalence_payload_readback=0
negative_canaries=15
production_gradient_payload_readback=0
production_weight_payload_readback=0
gradient_payload_r26_owner_pin_count=44
status_abi=R25StatusV1
status_success_value=1
reproducibility_runs=2
reproducibility_match=1
r26_handoff_ready=1
receipt_atlas_waves=9
monolithic_final_json=0
proof_ledger=HOLD
```

## PASS seal

```text
PASS_ASH_BASETRAIN_BT_WGSL_REAL_LOSS_SELECTED_LAYER_BACKWARD_REBASE_06C_R25
```

## Authority transition

```text
R24 REAL dFinalHidden
        │
        ▼
R13 FFN
        │
        ▼
R14 Post-RMS / OProj / actual five-lane attention
        │
        ▼
R15 NeoX / RoPE / QKV / Input-RMS
        │
        ▼
R16 TensorCube seven base roles
        │
        ▼
R17 DeltaQ / Gate
        │
        ▼
R18 Factor / Head / Structural Residual
        │
        ├─ 27 real parameter-gradient sources
        │  └─ 44 GPU gradient leases
        │
        └─ REAL complete selected-layer dInput
                │
                ▼
               R26
```

Final R25 authority state:

```text
real_loss_authority=1
real_loss_backward_authority=1
selected_layer_real_backward_authority=1
selected_layer_gradient_origin=REAL_LOSS
complete_selected_layer_dinput_authority=1
canonical_gradient_atlas_authority=0
full_model_gradient_authority=0
optimizer_authority=0
production_training_state_authority=0
proof_ledger=HOLD
```
