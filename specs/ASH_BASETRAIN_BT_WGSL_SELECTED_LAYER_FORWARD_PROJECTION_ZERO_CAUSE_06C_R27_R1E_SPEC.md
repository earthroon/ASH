# ASH-BASETRAIN-BT-WGSL-SELECTED-LAYER-FORWARD-PROJECTION-ZERO-CAUSE-06C-R27-R1E

## Revision

- Patch ID: `ASH-BASETRAIN-BT-WGSL-SELECTED-LAYER-FORWARD-PROJECTION-ZERO-CAUSE-06C-R27-R1E`
- Build revision: `bt-wgsl-selected-layer-forward-projection-zero-cause-06c-r27-r1e`
- Physical parent: `ASH-BASETRAIN-BT-WGSL-SUBLAYER-FORWARD-ZERO-FRONTIER-06C-R27-R1C`
- Weight-state parent: `ASH-BASETRAIN-BT-WGSL-PRODUCTION-ADAM-STATE-CARRY-MULTISTEP-06C-R27`
- Observation parent: `ASH-BASETRAIN-BT-WGSL-R27R1A-OPERAND-IDENTITY-DIGEST-NORMALIZATION-06C-R27-R1A-R2`
- R27-R1D dependency: `NONE`
- Proof ledger: `HOLD`

## SSOT

R27-R1C physically leaves two forward repair domains:

```text
attention_forward_repair_required=true
attention_backward_repair_required=false

ffn_forward_repair_required=true
ffn_backward_repair_required=false

sublayer_model_repair_target_count=2
```

The current forward-zero boundaries are:

```text
Attention
normalized_hidden != 0
-> Q/K/V projection domain
-> Stage12 context = 0
-> OProj X = 0

FFN
normalized_ffn_input != 0
-> GateProj / UpProj
-> gate_linear = 0
-> up_linear = 0
-> SiLU = 0
-> ffn_product = 0
-> DownProj X = 0
```

R27-R1D is not a physical parent of R27-R1E. The H4-only `26/1` premise is not present in the current R1A/R1A-R1 physical state. R1D remains historical diagnostic code and is not executed in the R1E terminal chain.

Required runtime authority:

```text
r27r1d_parent_required=0
r27r1d_execution_count=0
```

## Primary question

R27-R1E determines why a physically nonzero selected-layer normalized input produces zero projection outputs.

It separates:

```text
source production weight zero
production override copy/adoption corruption
weight semantic/version/range mismatch
projection input binding mismatch
projection executor false zero
mathematically legitimate zero projection
QKV lane-specific failure
shared QKV or Gate/Up executor failure
evidence insufficient
```

## Projection scope

Seven selected-layer base projection weights are observed:

```text
1 self_attn_q_proj
2 self_attn_k_proj
3 self_attn_v_proj
4 self_attn_o_proj
6 mlp_gate_proj
7 mlp_up_proj
8 mlp_down_proj
```

The causal forward-reference set is exactly:

```text
Q
K
V
Gate
Up
```

OProj and DownProj remain weight/lineage witnesses because their current forward inputs are already zero.

## R27 production weight binding retention

R27 step2 already copies the nine selected-layer base candidate weights into the live resident decoder block before the step2 forward.

R27-R1E retains a compact binding descriptor for each of the nine base weights:

```text
parameter ordinal
semantic ID
parameter version ID
R26 source candidate lease
actual forward-bound live destination lease
```

No checkpoint reopen is allowed.

Required:

```text
production_weight_override_registry=1
production_weight_override_count=27
production_weight_override_hit_count=27
production_weight_override_miss_count=0
selected_layer_base_override_count=9
selected_layer_projection_override_expected_count=7
checkpoint_reopen=0
checkpoint_weight_reload=0
```

## Source weight vs forward-bound weight

For each of the seven projection weights R1E performs exact GPU parity between:

```text
R26 source candidate lease
vs
actual resident live weight lease consumed by step2 forward
```

The comparison is nonpublishing and has zero tensor payload readback.

Per-weight adoption verdicts include:

```text
WEIGHT_ADOPTION_PARITY
SOURCE_WEIGHT_NONZERO_OVERRIDE_ZERO
SOURCE_WEIGHT_ZERO_OVERRIDE_ZERO
WEIGHT_ADOPTION_MISMATCH
WEIGHT_NONFINITE
```

A nonzero source with a zero or mismatched live destination classifies the problem as weight adoption/binding authority, not projection math.

## Compact weight observation

For every seven projection weights, both source and forward-bound leases receive compact GPU observation:

```text
element_count
zero_count
nonzero_count
nonfinite_count
max_abs
l2_norm
```

`l2_norm` uses a dedicated one-workgroup stable LASSQ reduction and returns one compact scalar only.

Required:

```text
production_weight_payload_readback=0
```

## Direct production projection surfaces

R1E reuses exact retained step2 forward tape surfaces:

```text
attention input: normalized_hidden
Q output: q_pre_rope
K output: k_pre_rope
V output: canonical_v

FFN input: normalized_ffn_input
Gate output: gate_linear_pre_activation
Up output: up_linear
```

Q and K post-RoPE tensors are not substituted for the projection outputs.

The exact physical Q/K/V output counts are reported separately. R1C's `ATTN_Q_PROJECTION_ZERO` is therefore not interpreted as proof that only Q is zero.

## Independent projection reference

R27-R1E adds a dedicated nonpublishing F32 WGSL reference for Q/K/V/Gate/Up.

Canonical weight layout:

```text
weight[out, in]
```

Reference math:

```text
reference[row, out] = sum_k input[row, k] * weight[out, k]
```

The reference consumes the exact production input lease and exact forward-bound production weight lease.

It does not run a second decoder, second attention block, or second FFN block.

Required:

```text
decoder_forward_recompute=0
attention_forward_recompute=0
ffn_forward_recompute=0
reference_projection_payload_readback=0
```

## Reference compact evidence

Per projection:

```text
rows
input_width
output_width
output_element_count
nonfinite_count
reference_nonzero_count
reference_active_row_count
production_nonzero_count
production_active_row_count
production_mismatch_count
comparison_policy
```

Current numerical mismatch policy is explicit:

```text
ABS_1E-4_PLUS_REL_1E-4_F32_V1
```

with:

```text
tolerance = 1e-4 + 1e-4 * max(abs(reference), abs(production))
```

Zero/nonzero classification does not depend on this tolerance. The tolerance is used for nonzero numerical mismatch accounting.

## Projection verdicts

Per Q/K/V/Gate/Up:

```text
NONFINITE
WEIGHT_ADOPTION_FAILURE
INPUT_ZERO_PARENT_CONTRADICTION
WEIGHT_ALL_ZERO
PRODUCTION_ZERO_REFERENCE_NONZERO
PRODUCTION_REFERENCE_BOTH_ZERO
PRODUCTION_NONZERO_REFERENCE_ZERO
PRODUCTION_REFERENCE_NONZERO_PARITY
PRODUCTION_REFERENCE_NONZERO_MISMATCH
```

The strongest false-zero proof is:

```text
input != 0
weight != 0
reference != 0
production = 0
```

which authorizes a forward projection executor/binding repair.

If both production and independent reference are zero with nonzero input/weight, the result is classified as a mathematical zero and no executor repair is fabricated.

## Attention aggregate classification

Possible aggregate classes include:

```text
ATTENTION_QKV_WEIGHT_ADOPTION_FAILURE
ATTENTION_QKV_WEIGHT_ZERO
ATTENTION_QKV_FUSED_EXECUTOR_FAILURE
ATTENTION_QKV_LANE_FAILURE:<semantic IDs>
ATTENTION_QKV_MATHEMATICALLY_ZERO
ATTENTION_QKV_PROJECTION_HEALTHY
ATTENTION_PROJECTION_CAUSE_UNRESOLVED
```

If Q/K/V all produce false-zero against nonzero references, a shared QKV forward executor/binding frontier is authorized.

If only a subset fails, lane-specific repair is authorized instead.

## FFN aggregate classification

Possible aggregate classes include:

```text
FFN_GATE_UP_WEIGHT_ADOPTION_FAILURE
FFN_GATE_UP_WEIGHT_ZERO
FFN_GATE_UP_SHARED_EXECUTOR_FAILURE
FFN_PROJECTION_EXECUTOR_FAILURE:<semantic ID>
FFN_GATE_UP_MATHEMATICALLY_ZERO
FFN_GATE_UP_PROJECTION_HEALTHY
FFN_PROJECTION_CAUSE_UNRESOLVED
```

Gate/Up zero is diagnosed before SiLU/product. Existing R1C SwiGLU reference remains authoritative for the downstream product.

## OProj and DownProj witness role

OProj and DownProj weights receive the same source/live observation and exact adoption parity.

They are not forward-executor repair targets in R1E because:

```text
OProj X = 0
DownProj X = 0
```

Their weight observations remain useful for explaining the R1C backward `DX_BOTH_ZERO` results and for forward/backward weight identity continuity.

Required:

```text
attention_backward_repair_required=0
ffn_backward_repair_required=0
```

## H4 isolation

R1E does not execute or repair the H4 diagnostic frontier.

Required:

```text
h4_diagnostic_repair_attempt=0
structural_horizon_mutation=0
```

The H4-only hypothesis may be reopened only after the main selected-layer forward projection failure is repaired and all 27 gradients are physically reobserved.

## Mutation boundary

R27-R1E is diagnostic only.

Required:

```text
forward_math_change=0
backward_math_change=0
gradient_value_mutation=0
optimizer_state_write=0
weight_mutation=0
checkpoint_write=0
```

No zero gradient fabrication, epsilon injection, silent checkpoint fallback, source-weight substitution, or reference-output publication is allowed.

## Production payload boundary

Required:

```text
production_input_payload_readback=0
production_weight_payload_readback=0
production_projection_payload_readback=0
reference_projection_payload_readback=0
```

Only compact statistics and parity decisions reach the host.

## Semantic waves

R27-R1E emits 11 sequential semantic waves:

```text
0  R27 / R1A-R2 / R1C parent authority and R1D retirement
1  selected-layer base/projection weight registry
2  seven projection source/live weight observations
3  normalized-hidden + Q/K/V production observations
4  Q/K/V independent references
5  attention projection cause
6  normalized-FFN + Gate/Up production observations
7  Gate/Up independent references
8  OProj/DownProj weight witnesses
9  aggregate repair target
10 reproducibility / canaries / handoff
```

Required:

```text
receipt_atlas_waves=11
receipt_chunk_max_fields<=8
parallel_chunk_build=1
streaming_chunk_write=1
deterministic_wave_merge=1
monolithic_final_json=0
```

## CLI authority

Exactly 48 new gates are required:

```text
--require-bt-wgsl-r27r1e-contract-001
...
--require-bt-wgsl-r27r1e-contract-048
```

They must exist exactly once in dedicated, short and full args, and the resolved-args repair script must regenerate and verify them.

Expected repair output:

```text
r27r1e_required_gate_count=48
r27r1e_gate_cardinality_exact=1
```

## Negative canaries

At least 18 diagnostic canaries cover:

```text
Q/K/V semantic cross-binding
Gate/Up cross-binding
stale OProj/DownProj weight generation
zero-length weight ranges
QKV lane alias/range errors
unrelated zero input lease binding
production-zero/reference-nonzero
production-nonzero/reference-zero
source-nonzero/live-zero adoption
parameter version mismatch
nonfinite weight
observation before adoption completion
reference executor aliasing production authority
attempted structural/H4 mutation
```

## Reproducibility

The full compact R1E snapshot is collected twice against unchanged retained state.

Required:

```text
reproducibility_runs=2
reproducibility_match=1
```

The comparison includes weight identities, parameter versions, compact source/live weight statistics, production projection observations, independent reference observations, per-lane verdicts and aggregate repair targets.

## Expected runtime summary

```text
r27_physical_parent=1
r27r1ar2_observation_parent=1
r27r1c_physical_parent=1
r27r1d_parent_required=0
r27r1d_execution_count=0

canonical_parameter_count=27
production_weight_override_registry=1
production_weight_override_count=27
production_weight_override_hit_count=27
production_weight_override_miss_count=0
selected_layer_base_override_count=9
selected_layer_projection_override_expected_count=7
selected_layer_projection_override_hit_count=<runtime>
selected_layer_projection_override_miss_count=<runtime>

normalized_hidden_nonzero_count=<runtime>
normalized_ffn_input_nonzero_count=<runtime>

q_weight_nonzero_count=<runtime>
k_weight_nonzero_count=<runtime>
v_weight_nonzero_count=<runtime>
oproj_weight_nonzero_count=<runtime>
gate_weight_nonzero_count=<runtime>
up_weight_nonzero_count=<runtime>
downproj_weight_nonzero_count=<runtime>

q_projection_nonzero_count=<runtime>
k_projection_nonzero_count=<runtime>
v_projection_nonzero_count=<runtime>
q_reference_nonzero_count=<runtime>
k_reference_nonzero_count=<runtime>
v_reference_nonzero_count=<runtime>
q_projection_verdict=<runtime>
k_projection_verdict=<runtime>
v_projection_verdict=<runtime>

gate_projection_nonzero_count=<runtime>
up_projection_nonzero_count=<runtime>
gate_reference_nonzero_count=<runtime>
up_reference_nonzero_count=<runtime>
gate_projection_verdict=<runtime>
up_projection_verdict=<runtime>

attention_projection_root_cause=<runtime>
ffn_projection_root_cause=<runtime>

attention_weight_repair_required=<runtime>
attention_projection_executor_repair_required=<runtime>
ffn_weight_repair_required=<runtime>
ffn_projection_executor_repair_required=<runtime>
selected_layer_weight_registry_repair_required=<runtime>
projection_repair_target_count=<runtime>

attention_backward_repair_required=0
ffn_backward_repair_required=0
h4_diagnostic_repair_attempt=0

production_input_payload_readback=0
production_weight_payload_readback=0
production_projection_payload_readback=0
reference_projection_payload_readback=0

receipt_atlas_waves=11
required_gate_count=48
negative_canaries=18
reproducibility_runs=2
reproducibility_match=1
proof_ledger=HOLD
```

## Handoff

If source weights are nonzero but live forward-bound weights differ or become zero, repair the production weight override/adoption path only.

If live weights and inputs are nonzero and the independent reference is nonzero while production is zero, repair only the exact failing projection lane/shared executor.

If source and live weights are both zero, move upstream into selected-layer parameter weight provenance rather than patching matmul.

If production and reference both agree on zero with nonzero input/weight, do not fabricate a projection fix; open a later mathematical/state-distribution frontier.

After any R1E repair, rerun and remeasure all 27 canonical parameter gradients before reopening any H4-only hypothesis.

## PASS semantics

R27-R1E PASS means the selected-layer Attention and FFN forward-zero branches were traced through the exact R27 production weight source, live override destination and forward projection execution boundaries; seven base projection weights were compactly observed; source-to-live weight adoption was checked exactly without tensor payload readback; Q/K/V/Gate/Up production outputs were compared with an independent nonpublishing F32 projection reference using the same production inputs and live weights; weight zero, override corruption, input binding failure, executor false-zero and mathematical zero were separated; OProj/DownProj remained witnesses rather than false forward repair targets; R1D/H4 was excluded from current runtime authority; no model/gradient/optimizer/weight/checkpoint state was mutated; and the resulting repair target was reproducible.

PASS does not mean projection outputs must always be nonzero, weights must always be nonzero, H4 is repaired, structural gradients are healthy, or full-model BaseTrain authority is open.

## PASS seal

```text
PASS_ASH_BASETRAIN_BT_WGSL_SELECTED_LAYER_FORWARD_PROJECTION_ZERO_CAUSE_06C_R27_R1E
```
