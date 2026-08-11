# ASH-BASETRAIN-BT-WGSL-SUBLAYER-FORWARD-ZERO-FRONTIER-06C-R27-R1C

## Revision

- Patch ID: `ASH-BASETRAIN-BT-WGSL-SUBLAYER-FORWARD-ZERO-FRONTIER-06C-R27-R1C`
- Build revision: `bt-wgsl-sublayer-forward-zero-frontier-06c-r27-r1c`
- Physical parent: `ASH-BASETRAIN-BT-WGSL-R27R1A-OPERAND-IDENTITY-DIGEST-NORMALIZATION-06C-R27-R1A-R2`
- Diagnostic parent: `ASH-BASETRAIN-BT-WGSL-ATTENTION-BACKWARD-ZERO-CAUSE-FRONTIER-06C-R27-R1B`
- Proof ledger: `HOLD`

## SSOT

R27-R1C narrows the selected-layer zero frontier to the two operations physically admitted by R27-R1A-R2:

```text
self_attn_o_proj
  X nonzero = 0
  X active rows = 0
  dY nonzero = 14336
  dY active rows = 7

mlp_down_proj
  X nonzero = 0
  X active rows = 0
  dY nonzero = 14336
  dY active rows = 7
```

R27-R1A-R2 already established:

```text
canonical_operand_descriptor_count=54
source_identity_match_operand_count=54
source_identity_mismatch_operand_count=0
observer_false_zero_count=0
observer_false_nonzero_count=0
revalidated_source_x_zero_count=2
revalidated_source_dy_zero_count=25
r1a_source_observation_authority_ready=1
r1a_gradient_frontier_revalidated=1
basetrain_gradient_repair_authorized=1
```

Therefore R27-R1C does not reopen the generic 27-operation observer problem. It investigates the two sublayer throats only:

```text
Attention Stage12 context -> OProj input
FFN SiLU*Up product       -> DownProj input
```

and independently classifies the corresponding projection backward dX paths.

## No model-semantic repair

R27-R1C is diagnostic only.

Required:

```text
attention_forward_math_change=0
attention_backward_math_change=0
ffn_forward_math_change=0
ffn_backward_math_change=0
oproj_backward_math_change=0
downproj_backward_math_change=0
gradient_value_mutation=0
optimizer_change=0
weight_mutation=0
checkpoint_write=0
```

No epsilon injection, gradient fabrication, NaN-to-zero conversion, forced nonzero invariant, synthetic production activation or silent fallback is permitted.

## Forward attention observation authority

The selected-layer forward tape already retains these production surfaces:

```text
normalized_hidden
q_pre_rope
k_pre_rope
canonical_v
q_post_rope
k_post_rope
stage11_global_state
stage12_context
```

R27-R1C observes the retained production surfaces directly. It does not run a second decoder/attention forward to manufacture missing evidence.

For every retained numeric surface R27-R1C records compact GPU evidence:

```text
element_count
nonfinite_count
zero_count
nonzero_count
active_row_count
max_abs
```

The row-support observation is bound to the exact same raw lease and logical row geometry as the element observer.

## Stage10 evidence boundary

The current selected-layer backward tape does not retain a standalone Stage10 numeric surface suitable for direct R27-R1C value observation.

R27-R1C therefore records:

```text
stage10IntermediateEvidence=UNAVAILABLE
```

It does not reconstruct Stage10 and pretend that a recomputed value is the original production intermediate.

The attention forward frontier may therefore be bracketed rather than falsely exact.

## Stage11 authority

R27-R1C reuses the established Stage11 compact state scanner against the exact retained global-softmax state.

R27-R1B parent evidence must remain:

```text
stage11_backward_state_lineage_match=1
stage11_all_masked_row_count=0
```

R27-R1C rejects invalid/nonfinite Stage11 state and does not reintroduce `ALL_MASKED` as an explanation unless new physical evidence contradicts the parent.

## Stage12 direct retention

The current architecture retains the Stage12 context handle directly as the OProj forward input tape. There is no separate host-side or copied R27-R1C publication tensor between these two semantic roles.

Therefore R27-R1C records direct-retention authority rather than inventing a producer/copy boundary:

```text
directStage12TapeRetention=1
attentionProducerTapeIdentityMatch=1
```

If the retained Stage12 context is zero, the forward zero is real at or before Stage12. R27-R1C then reports the narrowest physically supported bracket.

Current classification set includes:

```text
ATTN_NORMALIZED_HIDDEN_ZERO
ATTN_Q_PROJECTION_ZERO
ATTN_K_PROJECTION_ZERO
ATTN_V_PROJECTION_ZERO
ATTN_ROPE_Q_ZERO
ATTN_ROPE_K_ZERO
ATTN_STAGE11_INVALID
ATTN_STAGE11_ALL_MASKED
ATTN_STAGE11_TO_STAGE12_ZERO_BRACKET
ATTN_FORWARD_NONZERO_THROUGH_STAGE12
```

## FFN forward observation authority

The selected-layer forward tape retains:

```text
normalized_ffn_input
gate_linear_pre_activation
up_linear
silu_gate
ffn_product
```

R27-R1C observes all five exact production surfaces.

The current architecture retains `ffn_product` directly as the DownProj X tape, so R27-R1C records:

```text
directProductTapeRetention=1
ffnProductTapeIdentityMatch=1
```

No artificial producer/copy boundary is introduced.

## Independent SiLU-product compact reference

R27-R1C adds the nonpublishing backend kernel:

```text
base_train_r27r1c_swiglu_product_reference.wgsl
```

It reads exactly:

```text
silu_gate
up_linear
production ffn_product
```

and computes compact reference evidence for:

```text
expected = silu_gate * up_linear
```

The kernel records:

```text
nonfinite_count
silu_nonzero_count
up_nonzero_count
reference_product_nonzero_count
production_mismatch_count
```

The reference never publishes a replacement activation, never feeds DownProj, never feeds gradient construction and never reaches the optimizer.

Possible FFN frontier classes include:

```text
FFN_NORMALIZED_INPUT_ZERO
FFN_GATE_LINEAR_ZERO
FFN_UP_LINEAR_ZERO
FFN_SILU_GATE_ZERO
FFN_PRODUCT_MATHEMATICALLY_ZERO
SWIGLU_PRODUCT_EXECUTOR_OR_BINDING_FAILURE
SWIGLU_PRODUCT_NONZERO_MISMATCH
FFN_FORWARD_NONZERO_THROUGH_PRODUCT
```

## Production backward dX retention repair

R27-R1C must compare the actual semantic backward result with an independent algorithmic path without re-labeling a fresh replay as production.

Therefore the existing outputs retain the already-computed dX surfaces:

```text
R13 semantic DownProj dX
  -> BaseTrainR13LayerOutput.d_ffn_product_actual

R16 TensorCube DownProj dX
  -> BaseTrainR16LayerOutput.down_dx_tensorcube

R14 semantic OProj dX
  -> BaseTrainR14LayerOutput.attention_actual_dcontext

R16 TensorCube OProj dX
  -> BaseTrainR16LayerOutput.oproj_dx_tensorcube
```

No backward mathematics is changed; only existing completed outputs are kept alive for diagnosis.

## Independent backward reference authority

The semantic R13/R14 executor and R16 TensorCube executor are distinct implementations whose exact selected-role parity was already part of R16 correctness admission.

R27-R1C therefore uses:

```text
OProj:
  production = R14 semantic attention_actual_dcontext
  reference  = R16 TensorCube oproj_dx_tensorcube

DownProj:
  production = R13 semantic d_ffn_product_actual
  reference  = R16 TensorCube down_dx_tensorcube
```

Both sides use the same physical selected-layer dY/weight lineage already sealed by R16. R27-R1C does not reopen checkpoint weights or create a new weight authority.

Required receipt:

```text
r16WeightLineageBound=1
reference_checkpoint_reopen=0
```

## dX classification

Each projection publishes compact zero/nonzero evidence for production and independent TensorCube reference and an exact GPU parity comparison.

Verdicts:

```text
DX_BOTH_ZERO
DX_BOTH_NONZERO_PARITY
PRODUCTION_DX_ZERO_REFERENCE_NONZERO
PRODUCTION_DX_NONZERO_REFERENCE_ZERO
DX_NONZERO_MISMATCH
```

Interpretation:

```text
DX_BOTH_ZERO
  -> two independent admitted implementations agree the backward dX is mathematically zero for the bound inputs

PRODUCTION_DX_ZERO_REFERENCE_NONZERO
  -> semantic production executor/binding failure candidate

DX_NONZERO_MISMATCH
  -> backward numerical/executor divergence
```

No full dX payload is read to the host.

## Current dY parent canary

R27-R1C requires the R27-R1A-R1 operation receipts to retain the physically observed live upstreams:

```text
self_attn_o_proj dY nonzero_count=14336
self_attn_o_proj dY active_row_count=7

mlp_down_proj dY nonzero_count=14336
mlp_down_proj dY active_row_count=7
```

If these parent boundaries change, R27-R1C fails closed rather than diagnosing a different run under the old assumptions.

## Forward/backward independence

A forward zero and a backward dX zero are separate judgments.

R27-R1C does not assume:

```text
forward zero => backward bug
backward zero => forward bug
```

Attention and FFN each publish independent forward/backward repair requirements.

Required fields:

```text
attention_forward_repair_required
attention_backward_repair_required
ffn_forward_repair_required
ffn_backward_repair_required
```

## Attention aggregate

Possible aggregate classes include:

```text
ATTENTION_FORWARD_AND_BACKWARD_DUAL_FAILURE
ATTENTION_FORWARD_INTERNAL_FRONTIER
OPROJ_BACKWARD_DX_EXECUTOR_OR_BINDING_FAILURE
OPROJ_BACKWARD_DX_MATHEMATICALLY_ZERO
ATTENTION_SUBLAYER_PATH_HEALTHY
```

## FFN aggregate

Possible aggregate classes include:

```text
FFN_FORWARD_AND_BACKWARD_DUAL_FAILURE
FFN_FORWARD_INTERNAL_FRONTIER
DOWNPROJ_BACKWARD_DX_EXECUTOR_OR_BINDING_FAILURE
DOWNPROJ_BACKWARD_DX_MATHEMATICALLY_ZERO
FFN_SUBLAYER_PATH_HEALTHY
```

## Repair target cardinality

The patch publishes the number of independently justified repair domains among:

```text
attention forward
attention backward
FFN forward
FFN backward
```

as:

```text
sublayer_model_repair_target_count
```

No repair domain is added merely because a downstream tensor is zero.

## Zero semantics

Required principle:

```text
zero_is_observation_not_failure
```

R27-R1C does not impose universal nonzero requirements on attention context, FFN product, OProj dContext or DownProj dFFNProduct.

A failure is established through lineage contradiction, independent-reference contradiction, nonfinite evidence or a later explicit semantic invariant.

## Production readback boundary

Required:

```text
production_forward_payload_readback=0
production_backward_payload_readback=0
production_weight_payload_readback=0
```

Allowed host evidence is compact telemetry/status only.

## Sequential-parallel Atlas execution

R27-R1C preserves ASH execution policy:

```text
semantic waves sequential
independent compact observations parallel where safe
bounded receipt chunks parallel
deterministic ordinal merge
streaming receipt write
```

No mega observation atlas is introduced.

Receipt construction requires:

```text
receipt_chunk_max_fields<=8
parallel_chunk_build=1
streaming_chunk_write=1
deterministic_wave_merge=1
monolithic_final_json=0
```

## Semantic waves

R27-R1C emits exactly 10 waves:

```text
Wave 0  R1A-R2 / R1B parent admission and exact two-zero registry
Wave 1  attention retained-source authority and Stage10 evidence boundary
Wave 2  Q/K/V and RoPE observations
Wave 3  Stage11 / Stage12 attention zero bracket
Wave 4  FFN retained-source authority
Wave 5  Gate / Up / SiLU / product plus independent compact product reference
Wave 6  OProj semantic production dX vs R16 TensorCube reference
Wave 7  DownProj semantic production dX vs R16 TensorCube reference
Wave 8  attention + FFN combined root-cause classification
Wave 9  canaries, reproducibility and handoff
```

Required:

```text
receipt_atlas_waves=10
```

## CLI authority

R27-R1C introduces exactly 48 gates:

```text
--require-bt-wgsl-r27r1c-contract-001
...
--require-bt-wgsl-r27r1c-contract-048
```

The exact set is present in:

```text
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c_r27r1c_contract.args
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c.args
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c_full.args
```

`tools/repair_r13r2r2_resolved_args.ps1` removes stale R1C gate copies, appends each required gate exactly once and verifies cardinality.

Expected repair output:

```text
r27r1c_required_gate_count=48
r27r1c_gate_cardinality_exact=1
```

## Reproducibility

R27-R1C constructs its compact snapshot twice against unchanged retained production sources.

Required:

```text
reproducibility_runs=2
reproducibility_match=1
```

The snapshot covers forward surface statistics, Stage11 state, SiLU-product reference evidence, semantic dX observations and TensorCube reference dX observations.

## Current static canaries

The implementation carries 18 nonpublishing structural/runtime-bound canaries covering:

```text
R1A-R2 identity admission
zero observer contradictions
exact OProj/DownProj parent X/dY boundaries
Stage11 validity/all-masked parent
SiLU reference finiteness
semantic and TensorCube dX finiteness
zero production payload readback through parity
snapshot reproducibility
```

Canaries validate diagnostic authority only.

## Expected physical summary

```text
r27r1ar2_physical_parent=1
r27r1b_diagnostic_parent=1
forward_zero_operation_count=2

oproj_x_nonzero_count=0
oproj_dy_nonzero_count=14336

downproj_x_nonzero_count=0
downproj_dy_nonzero_count=14336

attention_stage11_all_masked_row_count=0
attention_stage12_context_nonzero_count=<runtime>
attention_forward_zero_frontier=<runtime>

ffn_gate_linear_nonzero_count=<runtime>
ffn_up_linear_nonzero_count=<runtime>
ffn_gate_silu_nonzero_count=<runtime>
ffn_product_producer_nonzero_count=<runtime>
swiglu_reference_product_nonzero_count=<runtime>
swiglu_production_mismatch_count=<runtime>
ffn_forward_zero_frontier=<runtime>

oproj_production_dcontext_nonzero_count=<runtime>
oproj_reference_dcontext_nonzero_count=<runtime>
oproj_dx_verdict=<runtime>

downproj_production_dffn_product_nonzero_count=<runtime>
downproj_reference_dffn_product_nonzero_count=<runtime>
downproj_dx_verdict=<runtime>

attention_sublayer_root_cause=<runtime>
ffn_sublayer_root_cause=<runtime>

attention_forward_repair_required=<runtime>
attention_backward_repair_required=<runtime>
ffn_forward_repair_required=<runtime>
ffn_backward_repair_required=<runtime>

sublayer_model_repair_target_count=<runtime>

production_forward_payload_readback=0
production_backward_payload_readback=0
production_weight_payload_readback=0
forward_math_change=0
backward_math_change=0
gradient_value_mutation=0
optimizer_change=0
weight_mutation=0
checkpoint_write=0
receipt_atlas_waves=10
parallel_chunk_build=1
streaming_chunk_write=1
deterministic_wave_merge=1
monolithic_final_json=0
required_gate_count=48
negative_canaries=18
reproducibility_runs=2
reproducibility_match=1
proof_ledger=HOLD
```

## Handoff

If Stage12 is zero while Q/K/V/RoPE are live and Stage11 is valid/non-all-masked, the next attention-forward patch must remain inside the Stage11-to-Stage12 bracket. Stage10 cannot be blamed without new retained evidence.

If `PRODUCTION_DX_ZERO_REFERENCE_NONZERO` is observed for OProj or DownProj, a projection backward executor/binding repair is authorized for that projection only.

If semantic and TensorCube dX are both zero, backward repair is not authorized from zero evidence alone; diagnosis stays on the forward-zero branch.

If the SiLU-product compact reference is nonzero while production product is zero/mismatched, a SwiGLU product executor/binding repair is authorized. If the independent product reference is also zero, the zero is mathematical for the observed Gate/Up values and the frontier stays upstream.

## BaseTrain authority

R27-R1C does not open full-model BaseTrain authority.

Required:

```text
full_model_gradient_authority=0
basetrain_admission_mutation=0
```

The patch only selects the next physically supported repair boundary.

## PASS semantics

R27-R1C PASS means the two R27-R1A-R2 admitted forward-zero sublayer inputs were traced through retained production evidence without second-forward substitution; unavailable Stage10 evidence was explicitly deferred; the retained Stage11 state and Stage12 context were observed; Gate/Up/SiLU/FFN product were directly observed; SiLU*Up received an independent compact nonpublishing reference; actual R13/R14 semantic projection dX surfaces were retained rather than replayed and mislabeled; independent R16 TensorCube dX surfaces were retained and compared; attention-forward, attention-backward, FFN-forward and FFN-backward repair requirements were separated; no model/gradient/weight/optimizer/checkpoint state or production payload was mutated; and the compact result was reproducible.

PASS does not mean any zero must become nonzero, that Stage10 is defective, that OProj/DownProj backward is defective, or that BaseTrain full-model training is admitted.

## PASS seal

```text
PASS_ASH_BASETRAIN_BT_WGSL_SUBLAYER_FORWARD_ZERO_FRONTIER_06C_R27_R1C
```
