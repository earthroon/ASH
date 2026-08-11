# ASH-BASETRAIN-BT-WGSL-STRUCTURAL-HORIZON-H4-DY-ZERO-FRONTIER-06C-R27-R1D

## Revision

- Patch ID: `ASH-BASETRAIN-BT-WGSL-STRUCTURAL-HORIZON-H4-DY-ZERO-FRONTIER-06C-R27-R1D`
- Build revision: `bt-wgsl-structural-horizon-h4-dy-zero-frontier-06c-r27-r1d`
- Physical parent: `ASH-BASETRAIN-BT-WGSL-SUBLAYER-FORWARD-ZERO-FRONTIER-06C-R27-R1C`
- Observation parent: `ASH-BASETRAIN-BT-WGSL-R27R1A-OPERAND-IDENTITY-DIGEST-NORMALIZATION-06C-R27-R1A-R2`
- Structural backward ancestor: `ASH-BASETRAIN-BT-WGSL-STRUCTURAL-FACTOR-HEAD-RESIDUAL-BACKWARD-06C-R18`
- Proof ledger: `HOLD`

## SSOT

R27-R1D diagnoses the selected-layer structural horizon H4 backward source only after the following physical premise is re-established in the same invocation:

```text
structural_horizon_head_h4
X nonzero count = 65536
X active rows   = 32
X source identity match = true

dY nonzero count = 0
dY active rows   = 0
dY source identity match = true
observer authority = ready
```

The patch does not infer `H4 X = 0`. H4 forward X is already admitted nonzero.

The user-reported later premise:

```text
joint_active_operation_count=26
zero_gradient_parameter_count=1
zero_gradient_semantic_id=bt.06c.decoder.layer21.structural_horizon_head_h4.weight
```

is treated as a runtime precondition, not silently hardcoded from an unavailable parent receipt. R27-R1D recomputes zero-gradient and joint-active cardinality from current R1A/R1A-R1 receipts and fails closed with `BTR27R1DUniqueH4ZeroGradientPremiseNotEstablished` when the 26/1 state is not actually present.

## Actual structural dY producer chain

The current implementation binds H4 dY to the real R18 chain:

```text
R17 d_structural_cube_actual[h4]
    -> six R18 factor backward d_factor outputs
    -> R18 factor gradient reassembly
    -> R18 horizon_head_dy[h4]
    -> H4 horizon-head linear backward
```

R27-R1D retains the six R18 per-horizon factor source-gradient leases in `BaseTrainR18LayerOutput.factor_source_gradients` so the diagnostic can distinguish:

```text
R17 structural cube already zero
factor backward outputs all zero
factor outputs nonzero but reassembly zero
```

without rerunning the model forward or fabricating a replacement gradient.

## H1-H4 sibling comparison

R27-R1D observes H1, H2, H3 and H4 in one physical invocation. For each horizon it records:

```text
X nonzero count
X active rows
dY nonzero count
dY active rows
joint active rows
X/dY source identity match
R1A canonical gradient nonzero count
R17 structural-cube compact observation
number of nonzero R18 factor-source tensors
total nonzero R18 factor-source elements
R18 reassembled horizon-head dY compact observation
```

H1-H3 are not assigned assumed nonzero values.

## Target geometry is context, not current dY producer authority

R06A target slots are observed for H1-H4:

```text
active target slots
target-outside-valid-prefix slots
source-pad slots
valid token count
```

However current R06B/R18 training structure has deferred structural target loss VJP. The target geometry is therefore explicitly labeled:

```text
structural_target_loss_vjp_authority=DEFERRED_NO_DIRECT_LOSS_VJP
h4_target_geometry_causal_to_current_dy=false
```

R27-R1D must not claim H4 dY is zero because of target-slot geometry unless a later patch establishes a direct loss-VJP path.

## H4 producer and consumer authority

Current R18 output directly retains the reassembled `horizon_head_dy[h4]` consumed by H4 head backward. There is no invented copy/publication tensor in between.

Required:

```text
h4_dy_producer_semantic_id=r18.factor_gradient_reassembly.h4
h4_dy_upstream_semantic_id=r17.d_structural_cube_actual.h4
h4_producer_consumer_identity_match=1
```

## Dispatch/write distinction

R18 iterates all four horizons through the canonical loop. R27-R1D records:

```text
configured_horizon_count=4
backward_horizon_iteration_count=4
observed_horizon_ordinals=H1,H2,H3,H4
h4_backward_dispatch_present=1
```

The exact retained reassembly lease supplies expected/actual logical element count. An observed complete zero is classified as `H4_DY_COMPLETE_ZERO_WRITE`, not as an unwritten buffer.

## Root-cause classification

After the unique-H4 parent premise is established, R27-R1D classifies the actual retained chain:

```text
H4_DY_REAL_UPSTREAM_ZERO_R17_STRUCTURAL_CUBE
H4_FACTOR_BACKWARD_ZERO_FRONTIER
H4_FACTOR_REASSEMBLY_ZERO_FRONTIER
H4_DY_FRONTIER_CONTRADICTS_PARENT_ZERO
```

If the unique-H4 premise is not present, classification becomes:

```text
H4_UNIQUENESS_NOT_ESTABLISHED
```

and the final PASS path is blocked.

Interpretation:

```text
R17 H4 cube zero
-> move upstream to R17 structural producer

R17 H4 cube nonzero + all six factor d_factor outputs zero
-> R18 factor backward frontier

one or more H4 factor d_factor outputs nonzero + reassembled H4 dY zero
-> R18 factor reassembly frontier
```

## Residual-forward-zero field isolation

The Pass78 code parent does not contain an authoritative `residual_forward_source_zero_count` field. R27-R1D therefore records:

```text
residual_forward_source_zero_count_parent_available=false
residual_forward_zero_related_to_h4_dy=EVIDENCE_INSUFFICIENT_PARENT_FIELD_UNAVAILABLE
```

It does not fabricate the value `1` or equate an unavailable residual-forward source to H4 X.

## No model mutation

Required:

```text
h4_forward_repair_required=0
forward_math_change=0
backward_math_change=0
gradient_value_mutation=0
optimizer_change=0
weight_mutation=0
checkpoint_write=0
```

No H3-to-H4 gradient fallback, epsilon injection, synthetic target, mask widening, forced nonzero invariant or reference-gradient publication is permitted.

## Production payload boundary

Allowed host evidence is compact counts/status only.

Required:

```text
production_structural_payload_readback=0
production_gradient_payload_readback=0
production_weight_payload_readback=0
```

## Semantic waves

R27-R1D emits 10 sequential diagnostic waves:

```text
0 parent H4 binding / unique-H4 preflight
1 H1-H4 sibling comparison
2 target geometry and deferred-loss authority
3 mask / ordinal authority
4 H4 dY producer lineage
5 H4 dispatch / write coverage
6 producer-consumer zero/parity result
7 residual-forward-zero relationship isolation
8 aggregate classification / repair target
9 canaries / reproducibility / handoff
```

Required:

```text
receipt_atlas_waves=10
receipt_chunk_max_fields<=8
parallel_chunk_build=1
streaming_chunk_write=1
deterministic_wave_merge=1
monolithic_final_json=0
```

## CLI authority

R27-R1D introduces exactly 48 gates:

```text
--require-bt-wgsl-r27r1d-contract-001
...
--require-bt-wgsl-r27r1d-contract-048
```

They are present in dedicated, short and full args and are regenerated exactly once by `tools/repair_r13r2r2_resolved_args.ps1`.

Expected repair output:

```text
r27r1d_required_gate_count=48
r27r1d_gate_cardinality_exact=1
```

## Reproducibility

The complete H1-H4 compact diagnostic snapshot is collected twice against unchanged retained production state.

Required:

```text
reproducibility_runs=2
reproducibility_match=1
```

## Expected current-parent result when the user-reported 26/1 state is physically present

```text
parameter_gradient_operation_count=27
joint_active_operation_count=26
zero_gradient_parameter_count=1
zero_gradient_semantic_id=bt.06c.decoder.layer21.structural_horizon_head_h4.weight
unique_h4_zero_gradient=1

h4_x_nonzero_count=65536
h4_x_active_row_count=32
h4_dy_nonzero_count=0
h4_dy_active_row_count=0

h1_dy_nonzero_count=<runtime>
h2_dy_nonzero_count=<runtime>
h3_dy_nonzero_count=<runtime>

h4_r17_structural_cube_nonzero_count=<runtime>
h4_factor_source_nonzero_tensor_count=<runtime>
h4_factor_source_total_nonzero_count=<runtime>
h4_dy_producer_nonzero_count=0

h4_backward_dispatch_present=1
h4_complete_zero_write=1
h4_aggregate_root_cause=<runtime>

h4_forward_repair_required=0
h4_backward_routing_repair_required=<runtime>
h4_loss_mask_repair_required=0
h4_backward_math_repair_required=<runtime>
h4_upstream_producer_repair_required=<runtime>
h4_repair_target_count=<runtime>

production_structural_payload_readback=0
production_gradient_payload_readback=0
production_weight_payload_readback=0
reproducibility_runs=2
reproducibility_match=1
proof_ledger=HOLD
```

## PASS semantics

R27-R1D PASS means the unique-H4 zero-gradient premise was physically re-established in the current invocation; H4 forward X remained nonzero and source-observation authority remained admitted; H1-H4 sibling dY states were reobserved rather than assumed; the exact R17 structural-cube to R18 factor-backward to R18 reassembly H4 dY chain was compactly observed; H4 dispatch and complete-zero write were separated from no-write conditions; target geometry was retained as context without falsely assigning deferred structural target loss as the current dY producer; unavailable residual-forward-zero evidence was explicitly deferred; no gradient/model/optimizer/checkpoint state was mutated; and the resulting H4 upstream, factor-backward, or reassembly frontier was reproducible.

PASS does not mean H4 must be nonzero for every sample, target geometry caused the current dY zero, H4 forward is defective, or a repair has already been applied.

## PASS seal

```text
PASS_ASH_BASETRAIN_BT_WGSL_STRUCTURAL_HORIZON_H4_DY_ZERO_FRONTIER_06C_R27_R1D
```
