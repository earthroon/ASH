# ASH-BASETRAIN-BT-WGSL-REAL-PARAMETER-GRADIENT-DW-FRONTIER-06C-R27-R1A

## Revision

- Patch ID: `ASH-BASETRAIN-BT-WGSL-REAL-PARAMETER-GRADIENT-DW-FRONTIER-06C-R27-R1A`
- Build revision: `bt-wgsl-real-parameter-gradient-dw-frontier-06c-r27-r1a`
- Physical parent: `ASH-BASETRAIN-BT-WGSL-REAL-GRADIENT-OBSERVABILITY-ATLAS-06C-R27-R1`
- Semantic ancestor: `ASH-BASETRAIN-BT-WGSL-REAL-LOSS-SELECTED-LAYER-BACKWARD-REBASE-06C-R25`
- Canonical gradient registry ancestor: `ASH-BASETRAIN-BT-WGSL-CANONICAL-GRADIENT-ATLAS-G205D-LIVE-REBASE-06C-R19`
- Proof ledger: `HOLD`

## SSOT

R27-R1A is a read-only parameter-gradient frontier diagnostic.

It closes exactly one question left by the physical R27-R1 result:

> The REAL-loss carrier remains nonzero through the selected-layer backward chain, while all 27 selected-layer canonical parameter gradients / 44 canonical gradient segments are exact zero. R27-R1A determines whether zero originates from the exact forward operand `X`, the operation-specific backward operand `dY`, empty joint reduction support, the production dW/dGamma executor path, or canonical gradient publication.

R27-R1A does not repair gradients, change derivative equations, change forward/backward execution semantics, mutate weights or optimizer state, write checkpoints, or open BaseTrain production admission.

The production R20 accumulation / norm authority and R27 Adam source were already shown by R27-R1 to match the zero canonical gradient set, so R27-R1A does not reopen them as primary fault candidates.

## Physical parent boundary

R27-R1A requires the exact R27-R1 physical parent to preserve:

```text
step2_real_loss_authority=1
step2_real_loss_vjp=1
step2_selected_layer_real_backward=1
step2_gradient_origin=REAL_LOSS
canonical_parameter_count=27
gradient_segment_count=44
production_observation_nonfinite_count=0
r20_observer_segment_identity_match=44
r20_observer_global_norm_parity=1
r27_optimizer_gradient_source_match=1
gradient_value_path_verdict=ALL_CANONICAL_GRADIENT_ZERO
basetrain_gradient_value_admission_ready=0
reproducibility_match=1
```

The current physical parent observation also recorded nonzero REAL-loss carrier values into R25 while all canonical parameter gradients were zero. Those runtime counts motivate R27-R1A but are not re-hardcoded as a second numeric authority.

## Diagnostic equation boundary

For matrix parameters, R27-R1A uses the existing canonical semantic dW equation:

```text
dW[o,i] = sum_r dY[r,o] * X[r,i]
```

For the two selected-layer RMSNorm gamma parameters, R27-R1A uses:

```text
dGamma[i] = sum_r dY[r,i] * X[r,i] * invRms[r]
```

These equations are diagnostic reference equations only. Existing production parameter layouts, row-tile ownership, reduction order and optimizer semantics remain authoritative.

## Exact selected-layer operation registry

R27-R1A diagnoses exactly 27 parameter-gradient operations.

Base parameters:

```text
00 input_layernorm
01 self_attn_q_proj
02 self_attn_k_proj
03 self_attn_v_proj
04 self_attn_o_proj
05 post_attention_layernorm
06 mlp_gate_proj
07 mlp_up_proj
08 mlp_down_proj
```

Structural parameters:

```text
09 structural_deltaq_h1
10 structural_deltaq_h2
11 structural_deltaq_h3
12 structural_deltaq_h4
13 structural_gate_h1
14 structural_gate_h2
15 structural_gate_h3
16 structural_gate_h4
17 structural_factor_hangul_presence
18 structural_factor_hangul_count
19 structural_factor_hangul_descriptor
20 structural_factor_cji18
21 structural_factor_qwlocal12
22 structural_factor_qwedge10
23 structural_horizon_head_h1
24 structural_horizon_head_h2
25 structural_horizon_head_h3
26 structural_horizon_head_h4
```

The operation classes are:

```text
25 matrix-like dW operations
2 RMS dGamma operations
```

Canonical publication remains exactly 27 parameters / 44 GPU gradient segments.

## Retained operation-specific backward sources

R27-R1A must not infer a parameter-specific `dY` merely because a higher-level backward carrier is nonzero.

The R27 step-2 real backward replay therefore retains the exact operation-specific leases needed by R27-R1A, including:

```text
R13 GateProj d_gate_pre
R13 UpProj d_up
R15 Input-RMS dY
R17 H1-H4 Gate preactivation dY
R18 H1-H4 Horizon Head dY
```

The pre-existing exact Q/K/V, OProj, DeltaQ, Factor and other backward sources are reused directly.

Retaining these leases is observational lifetime extension only. It does not create new gradient authority.

## Forward operand authority

Each diagnostic operation binds directly to the retained forward tape actually required by its derivative.

Important bindings include:

```text
Input RMS       -> exact input_hidden + retained invRms
Q/K/V Proj      -> exact normalized_hidden
OProj           -> exact W7 pre-OProj context lease
Post RMS        -> exact after_attention tape + retained invRms
Gate/Up Proj    -> exact normalized_ffn_input
DownProj        -> exact ffn_product
DeltaQ/Gate     -> exact per-horizon structural_cube
Factors         -> exact per-horizon fused_prediction factor slices
Horizon Heads   -> exact input_hidden
```

No checkpoint reopen, forward recomputation, latest-buffer heuristic or similarly-shaped buffer substitution is admitted.

## Joint row support

R27-R1A does not assume:

```text
X has a nonzero value + dY has a nonzero value => dW must be nonzero
```

For every operation it performs a device-local row-support scan and publishes compact counts:

```text
x_active_row_count
dy_active_row_count
joint_active_row_count
nonfinite_row_count
```

A row is active for an operand when at least one finite element in the operation's exact row slice is nonzero.

This distinguishes:

```text
SOURCE_X_ZERO
SOURCE_DY_ZERO
SOURCE_SUPPORT_DISJOINT
```

before any dW executor failure is claimed.

## Independent nonpublishing semantic reference

When the source geometry is valid, R27-R1A evaluates an independent GPU semantic reference directly from the retained `X` and `dY` leases.

The reference path does not reuse the production dW bind group and does not write into the production dW destination.

It uses four separate WGSL modules so no shader-module binding authority is accidentally shared:

```text
base_train_r27r1a_reference_linear_dw.wgsl
base_train_r27r1a_reference_rms_dgamma.wgsl
base_train_r27r1a_joint_row_support.wgsl
base_train_r27r1a_reference_factor_dw4.wgsl
```

Reference output values are not retained as a canonical tensor. Each bounded output element is immediately reduced into compact statistics:

```text
nonfinite_count
positive_count
negative_count
exact_zero_count
nonzero_count
max_abs
```

Required:

```text
reference_gradient_publication=0
reference_gradient_optimizer_feed=0
diagnostic_reference_payload_readback=0
```

The shared-factor reference follows the physical R18 authority: it computes the factor dW contribution for H1, H2, H3 and H4 and sums them in the diagnostic reference result for the shared parameter.

## Micro-atlas execution

Reference output domains are decomposed with the existing BaseTrain one-dimensional micro-atlas planner.

Required:

```text
bounded micro-atlas pages
bounded workgroup count
GPU workgroup parallelism
zero mega diagnostic gradient buffer
zero persistent reference dW tensor
```

Semantic diagnostic waves remain ordered. R27-R1A does not claim CPU-thread lane parallelism as authority.

## Production executor observation

R27-R1A observes the already-produced production dW/dGamma leases using the existing compact R27-R1 surface observer.

It independently observes:

```text
reference gradient zero/nonzero state
production executor gradient zero/nonzero state
canonical atlas gradient zero/nonzero state
```

The canonical atlas entry must match the exact registry ordinal, semantic parameter identity, expected parameter shape, finite authority and completion authority before classification.

Executor-to-canonical lease identity is checked by buffer owner identity, byte offset, byte span and element count for every canonical segment.

## Zero-frontier classification

Every one of the 27 operations receives exactly one frontier verdict:

```text
SOURCE_X_ZERO
SOURCE_DY_ZERO
SOURCE_SUPPORT_DISJOINT
REFERENCE_GRADIENT_ZERO
EXECUTOR_ZERO_REFERENCE_NONZERO
CANONICAL_PUBLICATION_DROP
HEALTHY_NONZERO
```

Interpretation:

### SOURCE_X_ZERO

The exact retained forward operand has no active row. The production executor must not be blamed before the forward operand lineage is investigated.

### SOURCE_DY_ZERO

The operation-specific backward source is zero. The boundary is upstream of dW arithmetic.

### SOURCE_SUPPORT_DISJOINT

X and dY may each contain nonzero values but have no row where both are active. A zero dW may therefore be mathematically legal.

### REFERENCE_GRADIENT_ZERO

The independent semantic reference is exact zero. R27-R1A does not claim an executor fault from production zero in this case. This preserves exact-cancellation semantics.

### EXECUTOR_ZERO_REFERENCE_NONZERO

This is the strong dW frontier witness:

```text
X support exists
dY support exists
joint support exists
independent semantic reference contains nonzero output
production executor output is exact zero
```

This authorizes the next repair stage to inspect the production dW bind/dispatch/reduction/write path.

### CANONICAL_PUBLICATION_DROP

The production executor contains a nonzero gradient but the canonical R19/R25-shaped gradient entry is zero or does not retain the exact executor lease lineage.

This authorizes a canonical publication / lease-lineage repair rather than a dW arithmetic repair.

### HEALTHY_NONZERO

Reference, production executor and canonical publication all preserve a nonzero gradient path.

## Scope discipline

R27-R1A is intentionally a **zero-frontier authority**, not a full production numerical parity replacement.

The current physical problem is an all-zero canonical dW/dGamma set. Therefore R27-R1A establishes whether an independently computed reference is nonzero while the production output is zero.

It does not claim a full element-by-element numerical parity proof for two nonzero tensors, and it does not create a second persistent reference tensor solely to make such a claim.

A later repair may add executor-local numerical parity if the frontier reaches `EXECUTOR_ZERO_REFERENCE_NONZERO` and a narrower kernel defect must be isolated.

## Completion authority

R27-R1A inherits production completion authority from the exact R19/R25 canonical gradient metadata and the already-physical R13-R18 backward stages.

It distinguishes a canonical completed zero gradient from missing canonical completion authority.

R27-R1A does not claim a new per-element production write-coverage counter that is not present in the current physical executor ABI.

## Aggregate root-cause class

The 27 operation verdicts reduce to one aggregate class:

```text
CANONICAL_PUBLICATION_FAILURE
DW_EXECUTOR_OR_BINDING_FAILURE
FORWARD_OPERAND_ZERO_OR_BINDING_FRONTIER
BACKWARD_ROLE_SOURCE_ZERO
MATHEMATICALLY_ZERO_GRADIENT_SET
PARAMETER_GRADIENT_PATH_HEALTHY
EVIDENCE_INSUFFICIENT
```

Priority is fail-closed:

```text
canonical lineage/publication mismatch
-> executor zero against nonzero reference
-> forward source zero
-> backward source zero
-> disjoint/zero semantic reference
-> healthy nonzero canonical path
-> evidence insufficient
```

No majority vote is used.

## BaseTrain admission boundary

R27-R1A publishes:

```text
basetrain_gradient_frontier_resolved
basetrain_gradient_repair_required
basetrain_gradient_value_admission_candidate
```

`basetrain_gradient_value_admission_candidate=1` requires at least one nonzero canonical base-parameter gradient and zero executor/reference-zero-frontier failure and zero canonical publication-lineage mismatch.

This is only a candidate. R27-R1A does not itself open production BaseTrain authority.

## Negative classifier canaries

R27-R1A executes eight nonpublishing classifier canaries covering:

```text
SOURCE_X_ZERO
SOURCE_DY_ZERO
SOURCE_SUPPORT_DISJOINT
REFERENCE_GRADIENT_ZERO
EXECUTOR_ZERO_REFERENCE_NONZERO
CANONICAL_PUBLICATION_DROP by zero canonical output
CANONICAL_PUBLICATION_DROP by lineage mismatch
HEALTHY_NONZERO
```

The canary count is derived from the actual case registry used by the validator.

These canaries validate frontier classification logic. They are not promoted to production gradient evidence.

## Production readback boundary

Allowed D2H is compact diagnostic telemetry only.

Forbidden:

```text
full forward X payload readback
full backward dY payload readback
full production dW/dGamma payload readback
full reference dW/dGamma payload readback
host gradient concatenation
host diagnostic mega tensor
```

Required:

```text
production_forward_payload_readback=0
production_backward_payload_readback=0
production_gradient_payload_readback=0
diagnostic_reference_payload_readback=0
reference_gradient_publication=0
reference_gradient_optimizer_feed=0
```

## Nonfinite policy

Any nonfinite value observed in live X, dY, production gradient, canonical gradient or semantic reference is fail-closed.

No NaN/Inf-to-zero conversion, clamp, skip or silent fallback is admitted.

## Receipt waves

Exactly 11 semantic waves are published:

```text
Wave 0  parent / selected-layer / 27-operation registry
Wave 1  forward-source binding summary
Wave 2  R13 FFN triplets
Wave 3  R14/R15 base attention + RMS triplets
Wave 4  R17 structural projector triplets
Wave 5  R18 factor/head triplets
Wave 6  X/dY joint-support summary
Wave 7  independent semantic reference summary
Wave 8  executor/reference/canonical zero-frontier parity
Wave 9  per-operation frontier + aggregate root cause
Wave 10 reproducibility / canaries / BaseTrain handoff / PASS
```

Required:

```text
receipt_atlas_waves=11
receipt_field_count_derived_from_registry=1
receipt_chunk_count_derived_from_wave_geometry=1
monolithic_final_json=0
```

No second fixed receipt-field-count authority is introduced.

## CLI gate authority

R27-R1A adds exactly 48 contiguous gates:

```text
--require-bt-wgsl-r27r1a-contract-001
...
--require-bt-wgsl-r27r1a-contract-048
```

The runtime gate registry is the canonical ordered registry and runtime required count uses its length.

The same exact 48 gates are baked into:

```text
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c_r27r1a_contract.args
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c.args
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c_full.args
```

The resolved-args repair script generates the R27-R1A sequence from `1..48`, removes stale occurrences and requires exact-once cardinality before writing the resolved file.

## Reproducibility

The ordered 27-operation diagnostic receipt is serialized twice from unchanged live observation results and requires exact digest equality.

Required:

```text
reproducibility_runs=2
reproducibility_match=1
```

The diagnostic does not mutate the source leases between builds.

## Expected physical summary

```text
r27r1_physical_parent=1
parameter_gradient_operation_count=27
linear_dw_operation_count=25
rms_dgamma_operation_count=2
x_nonzero_operation_count=<runtime>
dy_nonzero_operation_count=<runtime>
joint_support_operation_count=<runtime>
reference_gradient_nonzero_operation_count=<runtime>
executor_gradient_nonzero_operation_count=<runtime>
canonical_gradient_nonzero_operation_count=<runtime>
source_x_zero_count=<runtime>
source_dy_zero_count=<runtime>
source_support_disjoint_count=<runtime>
reference_gradient_zero_count=<runtime>
executor_zero_reference_nonzero_count=<runtime>
canonical_publication_drop_count=<runtime>
aggregate_root_cause_class=<runtime>
basetrain_gradient_frontier_resolved=<runtime>
basetrain_gradient_repair_required=<runtime>
basetrain_gradient_value_admission_candidate=<runtime>
production_forward_payload_readback=0
production_backward_payload_readback=0
production_gradient_payload_readback=0
diagnostic_reference_payload_readback=0
reference_gradient_publication=0
reference_gradient_optimizer_feed=0
receipt_atlas_waves=11
required_gate_count=48
negative_canaries=8
reproducibility_runs=2
reproducibility_match=1
proof_ledger=HOLD
```

## Repair handoff

R27-R1A does not select a repair before the physical frontier is known.

Handoff is evidence-driven:

```text
SOURCE_X_ZERO
-> forward tape / activation ownership review

SOURCE_DY_ZERO
-> branch-local backward source review

SOURCE_SUPPORT_DISJOINT or REFERENCE_GRADIENT_ZERO
-> no executor repair without further mathematical evidence

EXECUTOR_ZERO_REFERENCE_NONZERO
-> production dW/dGamma bind / dispatch / reduction / destination review

CANONICAL_PUBLICATION_DROP
-> R19/R25 canonical lease publication repair

HEALTHY_NONZERO
-> candidate for later gradient-wave transaction admission
```

## PASS semantics

R27-R1A PASS means the exact physical R27-R1 all-zero canonical parameter-gradient state was decomposed into operation-specific forward operand, operation-specific backward operand, joint support, independent nonpublishing semantic reference, production executor output and canonical publication boundaries for all 27 selected-layer parameters; the zero frontier was classified without fabricating nonzero gradients; no production payload was read back; diagnostic reference values were never promoted to gradient/optimizer authority; 11 deterministic semantic receipt waves were published; 48 gates were admitted exactly; classifier canaries passed; and the ordered diagnostic result was reproducible.

PASS does not mean:

```text
the gradient defect is repaired
all parameter gradients are required to be nonzero
full numerical dW parity is proved
BaseTrain production admission is open
R27-R2 is automatically admitted
full-model gradient authority exists
```

## PASS seal

```text
PASS_ASH_BASETRAIN_BT_WGSL_REAL_PARAMETER_GRADIENT_DW_FRONTIER_06C_R27_R1A
```
