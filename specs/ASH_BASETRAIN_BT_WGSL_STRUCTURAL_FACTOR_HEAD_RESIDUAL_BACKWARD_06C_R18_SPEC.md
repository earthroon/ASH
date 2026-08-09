# ASH-BASETRAIN-BT-WGSL-STRUCTURAL-FACTOR-HEAD-RESIDUAL-BACKWARD-06C-R18

## Revision

- Patch ID: `ASH-BASETRAIN-BT-WGSL-STRUCTURAL-FACTOR-HEAD-RESIDUAL-BACKWARD-06C-R18`
- Build revision: `bt-wgsl-structural-factor-head-residual-backward-06c-r18`
- Physical parent: `ASH-BASETRAIN-BT-WGSL-STRUCTURAL-DELTAQ-GATE-PROJECTOR-BACKWARD-06C-R17`
- Correctness ancestor: `ASH-BASETRAIN-BT-WGSL-TENSORCUBE-BACKWARD-PERFORMANCE-AUTHORITY-REPAIR-06C-R16-R1`
- Proof ledger: `HOLD`

## Corrected gate cardinality

The originally drafted R18 gate list was labeled as 69 gates, but the enumerated list contains **70 distinct gates**. R18 preserves every enumerated semantic gate and corrects the cardinality to 70 rather than silently dropping one gate.

## SSOT

R18 consumes the four canonical `dStructuralCube_H1..H4` authorities published by R17 and closes the structural source path back to the exact selected-layer `prepared_block.residual` input. It reverses six shared factor projectors, reassembles each horizon's 523-wide fused-prediction gradient, reverses four horizon-local fused heads, reduces the four structural residual gradients in deterministic H1->H2->H3->H4 order, then merges that structural residual with immutable `dInputHiddenBasePath` in BASE->STRUCTURAL order. The result `dInputHiddenComplete` is the first complete selected-layer input-gradient authority covering the currently admitted base and structural paths.

R18 does not create a canonical gradient atlas, run an optimizer, mutate weights, establish final-loss authority, or automatically promote new structural roles to TensorCube execution.

## Exact forward geometry

```text
B = 1
Q = 32
M = 32
hiddenWidth = 2048
horizonCount = 4
fusedPredictionWidth = 523
structuralCubeWidth = 256
factorCount = 6
rowCapacity = 9
edgeCapacity = 9
```

Factor partition:

```text
hangul_presence      start=0   width=9
hangul_count         start=9   width=10
hangul_descriptor    start=19  width=144
cji18                start=163 width=162
qwlocal12            start=325 width=108
qwedge10             start=433 width=90
end=523
```

Required partition evidence:

- zero gap
- zero overlap
- exact terminal end 523
- exact six-family order

## Parameter ownership

Six factor projectors are a single shared parameter set across H1-H4:

```text
WFactor_f = [256, factorWidth_f]
```

Four fused horizon heads are distinct:

```text
WHead_H1..H4 = [523,2048]
```

Factor families must not alias each other. Horizon heads must not alias each other. Factor sharing across horizons is intentional and canonical.

## Forward-tape extension

R18 extends the existing R17 structural tape without reopening checkpoints or rerunning forward computation.

Per horizon retained state:

- fused prediction `[1,32,523]`
- fused horizon-head weight `[523,2048]`
- horizon-head parameter identity

Shared selected-layer retained state:

- six factor weights
- exact factor manifest
- factor parameter identities

Owner-pin totals:

```text
base pins                     = 16
R17 structural pins           = 24
R18 horizon pins              = 8
R18 shared factor pins        = 6
total backward owner pins     = 54
```

No owner may be released before R18 completion.

## Factor backward and zero-copy strided source

A 523-wide fused prediction is row-major. A column slice is not a physically contiguous raw buffer across rows. R18 therefore does not fabricate a contiguous sub-lease and does not create a hidden factor-input copy.

The dedicated R18 strided factor executor reads:

```text
x_index = row * 523 + factorStart + localColumn
```

directly from the retained fused prediction.

It preserves R13 linear-backward mathematics and scalar accumulation order:

```text
dFactor_h,f = dStructuralCube_h * WFactor_f

dWFactor_h,f = dStructuralCube_h^T * Factor_h,f
```

The new strided executor is semantic-first and is not TensorCube-promoted in R18.

Production factor executions:

```text
4 horizons * 6 families = 24 backward roles
24 dFactor publications
24 horizon-local shared-weight dW partials
```

## Shared factor gradient reduction

Because each factor parameter is shared across H1-H4:

```text
dWFactor_f = H1 + H2 + H3 + H4
```

Exact reduction order:

```text
H1 -> H2 -> H3 -> H4
```

The 24 horizon partials are non-canonical. Exactly six family gradients become canonical after deterministic reduction.

## Fused-gradient reassembly

Each horizon's six `dFactor` surfaces are written to their original disjoint column ranges in a dedicated GPU scatter/reassembly executor.

Required result:

```text
dFusedPrediction_h = [32,523]
```

Required invariants:

- 4 reassemblies
- zero overlap
- zero gap
- zero out-of-range write
- 523 columns fully completed per row
- no host materialization

## Horizon-head backward

Horizon heads are contiguous linear operations and reuse the admitted R13 semantic linear backward executor:

```text
Pred_h = X * WHead_h^T
X = prepared_block.residual = [32,2048]
WHead_h = [523,2048]

dStructuralResidual_h = dPred_h * WHead_h

dWHead_h = dPred_h^T * X
```

R18 publishes four structural residual gradients and four canonical horizon-head dW tiles.

## Structural residual merge

Exact reduction:

```text
T12   = H1 + H2
T123  = T12 + H3
Total = T123 + H4
```

`dStructuralResidualTotal` has shape `[1,32,2048]`.

No unordered float atomic reduction is admitted.

## Complete selected-layer input gradient

R17's `dInputHiddenBasePath` is immutable and is neither renamed nor recomputed.

R18 publishes:

```text
dInputHiddenComplete
  = dInputHiddenBasePath
  + dStructuralResidualTotal
```

Exact operand order:

```text
BASE -> STRUCTURAL
```

Only this R18 payload may claim:

```text
completeSelectedLayerDInputAuthority = true
```

The older R15/R16/R17 base-path payload remains a historical component authority.

## Semantic/TensorCube authority boundary

R16/R16-R1 TensorCube authority remains limited to the original seven roles:

```text
DOWN
GATE_FFN
UP
OPROJ
Q
K
V
```

R18 structural factor roles and horizon-head roles are semantic-first:

```text
structuralFactorTensorCubeAdoption = false
structuralHeadTensorCubeAdoption = false
```

A future R18A may benchmark/promote these roles using the repaired R16-R1 performance methodology after R18 correctness is physically closed.

## Numerics and zero policy

Production gradients may be numerically zero under the deterministic upstream fixture. Zero is an observation, not failure, provided writes are complete, finite, correctly bound and reproducible.

Forbidden:

- NaN/Inf clamp
- gradient clamp
- fabricated nonzero gradients
- unwritten zero interpreted as a valid complete output

No `BTR18GradientZero` failure exists.

## Oracles

R18 includes isolated synthetic evidence for:

- strided factor `dX` against CPU f64
- strided factor `dW` against CPU f64
- fused-gradient reassembly
- shared factor H1->H4 reduction
- directional finite difference
- nonzero structural-source canary

Synthetic payload readback is isolated from production authority. Production gradient/weight payload readback remains zero.

## Lifecycle

Factor and head gradient surfaces preserve the existing bounded Micro-Atlas/commit lifecycle semantics:

```text
PLANNED
-> RESIDENT
-> DISPATCHED
-> GPU_COMPLETED
-> COMMITTED
-> GC_ELIGIBLE
-> RELEASED
```

Factor `dFactor` survives until fused-gradient reassembly commits. Horizon-local factor dW partials survive until the canonical shared-family reduction commits. `dPred_h` survives until both horizon residual and horizon-head dW publication are complete.

## Reproducibility

The full R18 chain runs twice with no mutation. Exact comparisons cover:

- 24 factor-source gradients
- 24 factor dW partials
- 6 canonical shared factor gradients
- 4 fused-prediction gradients
- 4 structural residual gradients
- 4 horizon-head gradients
- structural residual total
- complete dInput

Required:

```text
reproducibilityRuns = 2
reproducibilityMatch = true
```

## R18 output

```text
BaseTrainR18LayerOutput {
    layer_index,
    d_input_hidden_base_path,
    d_structural_residual_horizons[4],
    d_structural_residual_total,
    d_input_hidden_complete,
    factor_weight_gradients[6],
    horizon_head_weight_gradients[4],
}
```

## R19 boundary

R18 ends with a complete selected-layer dInput and all currently implemented selected-layer parameter-gradient families exposed, but no canonical gradient atlas.

R19 exclusively owns:

- canonical parameter identity registry
- gradient-tile inventory
- canonical gradient atlas
- G205D accumulation rebase

Required:

```text
canonicalGradientAtlas = false
optimizer = false
weightMutation = false
finalLossAuthority = false
r19HandoffReady = true
```

## Required receipts

- `r18_parent_r17_receipt.json`
- `r18_factor_manifest_binding_receipt.json`
- `r18_structural_head_tape_receipt.json`
- `r18_owner_pin_extension_receipt.json`
- `r18_factor_h1_backward_receipt.json`
- `r18_factor_h2_backward_receipt.json`
- `r18_factor_h3_backward_receipt.json`
- `r18_factor_h4_backward_receipt.json`
- `r18_factor_partial_gradient_receipt.json`
- `r18_shared_factor_gradient_reduction_receipt.json`
- `r18_factor_gradient_reassembly_receipt.json`
- `r18_horizon_head_h1_backward_receipt.json`
- `r18_horizon_head_h2_backward_receipt.json`
- `r18_horizon_head_h3_backward_receipt.json`
- `r18_horizon_head_h4_backward_receipt.json`
- `r18_structural_residual_merge_receipt.json`
- `r18_complete_dinput_merge_receipt.json`
- `r18_full_structural_cpu_f64_oracle_receipt.json`
- `r18_directional_finite_difference_receipt.json`
- `r18_shared_weight_reduction_oracle_receipt.json`
- `r18_nonzero_structural_source_canary_receipt.json`
- `r18_micro_atlas_lifecycle_receipt.json`
- `r18_reproducibility_receipt.json`
- `r18_r19_handoff_receipt.json`
- `bt_wgsl_structural_factor_head_residual_backward_06c_r18_final.json`

## Receipt Atlas

Eight deterministic parallel/streaming waves:

1. parent/correctness/handoff
2. factor manifest/tape/owner pins
3. H1-H4 factor backward
4. shared factor reduction/reassembly
5. H1-H4 horizon-head backward
6. structural residual/complete-dInput merge
7. oracle/lifecycle/reproducibility
8. R19 boundary/PASS seal

No monolithic final JSON construction is admitted.

## CLI gates

Exactly **70** distinct R18 gates:

```text
--require-bt-wgsl-r18-r17-physical-parent
--require-bt-wgsl-r18-r16r1-correctness-authority-preserved
--require-bt-wgsl-r18-base-dinput-exact-adoption
--require-bt-wgsl-r18-four-structural-cube-exact-handoff
--require-bt-wgsl-r18-four-horizon-order
--require-bt-wgsl-r18-factor-manifest-binding
--require-bt-wgsl-r18-factor-partition-exact
--require-bt-wgsl-r18-row-capacity-nine
--require-bt-wgsl-r18-edge-capacity-nine
--require-bt-wgsl-r18-fused-width-523
--require-bt-wgsl-r18-structural-cube-width-256
--require-bt-wgsl-r18-structural-head-forward-tape
--require-bt-wgsl-r18-shared-factor-forward-tape
--require-bt-wgsl-r18-base-owner-pins-16
--require-bt-wgsl-r18-r17-structural-owner-pins-24
--require-bt-wgsl-r18-horizon-owner-pins-8
--require-bt-wgsl-r18-shared-factor-owner-pins-6
--require-bt-wgsl-r18-total-owner-pins-54
--require-bt-wgsl-r18-horizon-head-weight-identities
--require-bt-wgsl-r18-factor-weight-identities
--require-bt-wgsl-r18-factor-projectors-shared-across-horizons
--require-bt-wgsl-r18-zero-horizon-head-alias
--require-bt-wgsl-r18-zero-factor-alias
--require-bt-wgsl-r18-six-factor-backward-families
--require-bt-wgsl-r18-h1-factor-backward
--require-bt-wgsl-r18-h2-factor-backward
--require-bt-wgsl-r18-h3-factor-backward
--require-bt-wgsl-r18-h4-factor-backward
--require-bt-wgsl-r18-factor-source-gradient-publication
--require-bt-wgsl-r18-factor-weight-horizon-partials
--require-bt-wgsl-r18-deterministic-shared-factor-weight-reduction
--require-bt-wgsl-r18-six-canonical-factor-weight-gradients
--require-bt-wgsl-r18-fused-gradient-reassembly
--require-bt-wgsl-r18-zero-factor-reassembly-overlap
--require-bt-wgsl-r18-zero-factor-reassembly-gap
--require-bt-wgsl-r18-h1-horizon-head-backward
--require-bt-wgsl-r18-h2-horizon-head-backward
--require-bt-wgsl-r18-h3-horizon-head-backward
--require-bt-wgsl-r18-h4-horizon-head-backward
--require-bt-wgsl-r18-four-horizon-head-weight-gradients
--require-bt-wgsl-r18-four-structural-residual-publications
--require-bt-wgsl-r18-deterministic-h1-h2-h3-h4-residual-merge
--require-bt-wgsl-r18-structural-residual-total-publication
--require-bt-wgsl-r18-base-structural-final-merge
--require-bt-wgsl-r18-complete-dinput-authority
--require-bt-wgsl-r18-base-dinput-immutable-preservation
--require-bt-wgsl-r18-r13-linear-semantic-authority
--require-bt-wgsl-r18-zero-structural-tensorcube-auto-promotion
--require-bt-wgsl-r18-r16-seven-role-tensorcube-authority-unchanged
--require-bt-wgsl-r18-full-structural-cpu-f64-oracle
--require-bt-wgsl-r18-directional-finite-difference
--require-bt-wgsl-r18-shared-weight-reduction-oracle
--require-bt-wgsl-r18-nonzero-structural-source-canary
--require-bt-wgsl-r18-fail-closed-numerics
--require-bt-wgsl-r18-zero-observation-not-failure
--require-bt-wgsl-r18-production-payload-readback-zero
--require-bt-wgsl-r18-micro-atlas-lifecycle-preserved
--require-bt-wgsl-r18-zero-r17-rebackward
--require-bt-wgsl-r18-zero-factor-forward-recompute
--require-bt-wgsl-r18-zero-horizon-forward-recompute
--require-bt-wgsl-r18-zero-checkpoint-reopen
--require-bt-wgsl-r18-zero-decoder-clone
--require-bt-wgsl-r18-zero-gradient-atlas
--require-bt-wgsl-r18-zero-optimizer
--require-bt-wgsl-r18-zero-weight-mutation
--require-bt-wgsl-r18-final-loss-authority-deferred
--require-bt-wgsl-r18-atlas-wave-streaming-receipt
--require-bt-wgsl-r18-zero-monolithic-final-json
--require-bt-wgsl-r18-double-run-reproducibility
--require-bt-wgsl-r18-r19-handoff-ready
```

Each gate must occur exactly once in source validation, short args, full args and regenerated resolved args.

## Expected physical summary

```text
r17_physical_parent=1
r16r1_correctness_authority_preserved=1
r17_dstructural_cube_adopted=4
horizon_count=4
row_capacity=9
edge_capacity=9
fused_width=523
structural_cube_width=256
factor_count=6
factor_partition_gap=0
factor_partition_overlap=0
factor_projectors_shared_across_horizons=1
horizon_head_count=4
base_owner_pins=16
r17_structural_owner_pins=24
r18_horizon_owner_pins=8
r18_shared_factor_owner_pins=6
all_backward_owner_pins=54
factor_backward_role_count=24
factor_source_gradients_published=24
factor_dw_horizon_partials=24
canonical_shared_factor_dw_tiles=6
shared_factor_reduction_order_h1_h2_h3_h4=1
fused_gradient_reassembly_count=4
fused_gradient_reassembly_gap=0
fused_gradient_reassembly_overlap=0
horizon_head_backward_count=4
horizon_head_dw_tiles=4
dstructural_residual_published=4
structural_residual_merge_order_h1_h2_h3_h4=1
dstructural_residual_total_published=1
base_dinput_adopted=1
complete_dinput_merge_order_base_then_structural=1
dinput_hidden_complete_published=1
complete_selected_layer_dinput_authority=1
structural_factor_tensorcube_adoption=0
structural_head_tensorcube_adoption=0
full_structural_cpu_f64_oracle=1
directional_finite_difference=1
shared_weight_reduction_oracle=1
nonzero_structural_source_canary=1
production_gradient_payload_readback=0
production_weight_payload_readback=0
reproducibility_runs=2
reproducibility_match=1
r19_handoff_ready=1
receipt_atlas_waves=8
monolithic_final_json=0
proof_ledger=HOLD
```

## PASS seal

`PASS_ASH_BASETRAIN_BT_WGSL_STRUCTURAL_FACTOR_HEAD_RESIDUAL_BACKWARD_06C_R18`

The runtime token additionally seals exact factor geometry, shared-factor reduction, horizon-head backward, complete dInput authority, semantic-first structural execution, zero payload readback, reproducibility, R19 boundary and proof-ledger HOLD.
