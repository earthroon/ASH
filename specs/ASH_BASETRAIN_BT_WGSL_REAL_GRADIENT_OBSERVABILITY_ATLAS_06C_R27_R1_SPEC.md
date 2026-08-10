# ASH-BASETRAIN-BT-WGSL-REAL-GRADIENT-OBSERVABILITY-ATLAS-06C-R27-R1

## Revision

- Patch ID: `ASH-BASETRAIN-BT-WGSL-REAL-GRADIENT-OBSERVABILITY-ATLAS-06C-R27-R1`
- Build revision: `bt-wgsl-real-gradient-observability-atlas-06c-r27-r1`
- Physical parent: `ASH-BASETRAIN-BT-WGSL-PRODUCTION-ADAM-STATE-CARRY-MULTISTEP-06C-R27`
- Parent production training generation: `2`
- Parent production optimizer generation: `2`
- Parent production optimizer step: `2`
- Next consumer: `ASH-BASETRAIN-BT-WGSL-GRADIENT-WAVE-TRANSACTION-06C-R27-R2`
- Proof ledger: `HOLD`

## SSOT

R27-R1 adds a read-only, device-local observability authority over the already-physical R27 step-2 REAL-loss backward path.

R27-R1 does not change forward mathematics, backward mathematics, loss mathematics, gradient values, clipping policy, Adam policy, parameter identity, production weights, optimizer state, or the atomic production training-state commit.

The single purpose is to establish where finite REAL-loss gradient values remain nonzero, where they become exact zero, whether the exact canonical 27-parameter / 44-segment gradient inventory is observed without gaps or aliasing, and whether the R20 finalized-gradient reduction consumed by R27 Adam agrees with an independent observation using the exact same R20 stable LASSQ shader authority.

R27-R1 must distinguish:

```text
NONZERO_OBSERVED
ZERO_OBSERVED
MIXED_ZERO_NONZERO
NONFINITE
EVIDENCE_INSUFFICIENT
```

Zero is an observation, not an automatic correctness failure.
Nonfinite values, lineage mismatch, inventory mismatch and R20/R27 reduction mismatch are fail-closed correctness failures.

## R27 physical parent

Required parent evidence:

```text
r27_physical_parent=1
canonical_production_training_state_generation=2
canonical_production_optimizer_generation=2
canonical_production_optimizer_step=2
next_step_forward_consumption_authority=1
step2_real_loss_authority=1
step2_real_loss_vjp=1
step2_selected_layer_real_backward=1
step2_gradient_origin=REAL_LOSS
production_multistep_state_carry_authority=1
full_model_training_state_authority=0
checkpoint_write=0
r28_handoff_ready=1
```

The exact R27 PASS token is bound. Receipt-only reconstruction, stale gradient lineage, historical fixture promotion and checkpoint reopening for observation are prohibited.

## No semantic mutation

Required:

```text
forward_math_change=0
backward_math_change=0
loss_math_change=0
optimizer_policy_change=0
gradient_mutation=0
gradient_clamp=0
gradient_epsilon_injection=0
gradient_nonzero_fabrication=0
weight_mutation_from_observer=0
optimizer_state_mutation_from_observer=0
training_root_mutation_from_observer=0
checkpoint_write=0
```

Observer kernels are read-only consumers of already-live GPU leases.

## Observation classes

R27-R1 publishes three observation classes.

### Carrier

Carrier observations track backward signal propagation and are not promoted to parameter-gradient authority.

The mandatory carrier frontier uses this ordered spine:

```text
R24 REAL dNormalizedHidden
R24 REAL dFinalHidden
R25 REAL upstream ingress
R13 dNormalizedFFNInput
R14 attention residual backward carrier
R15 dInputHiddenTotal
R18 dInputHiddenComplete
```

Additional carrier surfaces from R14/R15/R17/R18 may be observed for branch-local diagnosis.

### Parameter gradient

The canonical parameter inventory remains exactly 27 parameters:

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

Canonical segment inventory remains:

```text
linear ROW_TILE segments = 42
RMS FULL_VECTOR segments = 2
GPU gradient segments = 44
```

No FinalNorm dGamma, LM-head gradient, embedding gradient, bias gradient or complete dInput carrier is silently inserted into this selected-layer parameter registry.

### Reduction observation

Reduction observation publishes compact LASSQ evidence for:

```text
per observed surface
per canonical gradient segment
per canonical parameter
base 9 parameters
structural 18 parameters
all 27 parameters / all 44 segments
R20 finalized 44 segments
R27 step-2 Adam source
```

It does not create a second gradient authority.

## Canonical compact statistic

Each observed GPU surface produces compact metadata equivalent to:

```text
R27R1GradientObservationStatV1 {
    element_count,
    finite_count,
    nonfinite_count,
    positive_count,
    negative_count,
    exact_zero_count,
    nonzero_count,
    max_abs,
    lassq_scale,
    lassq_ssq,
    l2_norm,
    micro_atlas_page_count,
    max_page_workgroups,
    compact_readback_count,
    tensor_payload_readback_count,
}
```

No gradient payload is copied into the receipt.

## Exact-zero authority

Canonical classification is bit-exact for zero identity:

```text
+0.0 -> ZERO
-0.0 -> ZERO
finite x != 0 -> NONZERO
NaN -> NONFINITE
+Inf/-Inf -> NONFINITE
```

Subnormal finite nonzero values remain nonzero.
No epsilon threshold is permitted for exact-zero classification.

Required partition identity:

```text
nonfinite_count + exact_zero_count + nonzero_count = element_count
positive_count + negative_count = nonzero_count
```

## Nonfinite fail-closed policy

Any production observed carrier or canonical parameter gradient containing NaN or Inf fails before observation publication.

Forbidden:

```text
NaN -> 0
Inf -> 0
skip nonfinite values
clamp nonfinite values
omit nonfinite values from canonical norm authority
```

The live observation path requires:

```text
production_observation_nonfinite_count=0
```

## R20 LASSQ single mathematics authority

R27-R1 must not introduce a second gradient-norm formula.

It reuses the exact R20 WGSL reduction authorities:

```text
BASETRAIN_R20_NORM_PARTIAL_SHADER
BASETRAIN_R20_NORM_SEGMENT_REDUCE_SHADER
BASETRAIN_R20_NORM_GLOBAL_REDUCE_SHADER
R20_NORM_CHUNK_SIZE
```

Canonical stable norm remains scaled sum-of-squares:

```text
(scale, ssq)
norm = 0                         when scale == 0
norm = scale * sqrt(ssq)         otherwise
```

Required:

```text
r20_lassq_math_single_authority=1
observer_private_norm_formula=0
unordered_float_atomic_norm=0
```

## Micro-atlas chunk authority

R27-R1 does not create a mega observation or mega gradient buffer.

Each observed surface is split with the existing BaseTrain micro-atlas one-dimensional work decomposition. A logical page binds source lineage, element start/count and workgroup coverage. The observer scans each page on device and commits only compact atomic counts/max-abs evidence.

Required:

```text
mega_observation_buffer=0
mega_gradient_buffer=0
gradient_payload_copy=0
host_gradient_materialization=0
host_gradient_concat=0
parallel_chunks_within_lane=1
```

## Sequential-parallel wave execution

Semantic waves are sequential. Independent observation lanes inside a wave are parallel. GPU workgroups inside a lane are parallel.

```text
Step
  -> Wave 0 sequential
       -> lane 0 || lane 1 || ...
            -> micro-atlas pages/workgroups
       -> deterministic lane order
       -> compact wave receipt
  -> Wave 1 sequential
  -> ...
```

Required:

```text
waves_sequential=1
parallel_lanes_within_wave=1
parallel_chunks_within_lane=1
cross_wave_overlap=0
unordered_float_atomic_merge=0
```

The observer never reorders producer execution and never creates a new canonical backward dependency.

## Twelve semantic observation waves

R27-R1 has exactly 12 semantic receipt waves.

```text
Wave 0  R27 parent / generation / observer identity
Wave 1  R24 REAL-loss VJP surfaces
Wave 2  R25/R13 REAL ingress + FFN
Wave 3  R14 Post-RMS / OProj / actual attention
Wave 4  R15 NeoX / QKV / Input-RMS
Wave 5  R17 DeltaQ / Gate
Wave 6  R18 Factor / Head / residual
Wave 7  canonical 27/44 segment observations
Wave 8  exact 27 per-parameter aggregates
Wave 9  base / structural / all-gradient aggregates
Wave 10 R20 finalized-gradient and R27 Adam-source parity
Wave 11 frontier / negative canaries / reproducibility / handoff / PASS
```

`receipt_atlas_waves=12` is semantic SSOT.

Receipt field count and physical receipt chunk count are runtime-derived from emitted registry/wave geometry. A second hand-maintained numeric field-count authority is prohibited.

Required:

```text
receipt_field_count_derived_from_registry=1
receipt_chunk_count_derived_from_wave_geometry=1
monolithic_final_json=0
```

## Wave 1: R24 REAL-loss VJP

Observe exact live:

```text
R24 real_dnormalized_hidden
R24 real_dfinal_hidden
```

Required parent lineage:

```text
real_loss_authority=1
real_loss_backward_authority=1
```

No second logit VJP or FinalNorm backward is run for observation.

## Wave 2: R25/R13 ingress and FFN

Observe:

```text
R25 exact REAL dFinal upstream ingress
R13 dNormalizedFFNInput carrier
R13 DownProj dW tiles
R13 GateProj dW tiles
R13 UpProj dW tiles
```

The previously computed REAL dFinal ingress nonzero witness is no longer semantically discarded. The GPU source itself is observed by the new observer authority.

## Wave 3: R14 Post-RMS / OProj / actual attention

Observe live R14 carriers and gradients including:

```text
attention residual backward carrier
base dQ
H1-H4 DeltaQ carriers
shared dK
shared dV
H1-H4 Gate carriers
Post-Attention RMSNorm dGamma
actual OProj dW tiles
```

Historical R12 fixture-derived authority remains excluded.

## Wave 4: R15 NeoX / QKV / Input-RMS

Observe:

```text
Q pre-RoPE gradient
K pre-RoPE gradient
V gradient
dInputHiddenTotal
QProj dW tiles
KProj dW tiles
VProj dW tiles
Input RMSNorm dGamma
```

No QKV forward recompute, checkpoint reopen or selected-layer weight reload is permitted.

## Wave 5: R17 structural projector backward

Observe:

```text
H1-H4 structural cube gradients
H1-H4 DeltaQ projector dW
H1-H4 Gate projector dW
```

A mathematically zero Gate-derived path caused by the current zero Gate parent remains a legal zero observation.

## Wave 6: R18 factor/head/residual

Observe:

```text
H1-H4 structural residual carriers
dStructuralResidualTotal
dInputHiddenComplete
six shared Factor dW outputs
four Horizon Head dW outputs
```

Existing deterministic H1 -> H2 -> H3 -> H4 reduction authority remains unchanged.

## Wave 7: canonical 27/44 segment atlas

The exact R25 REAL-loss canonical candidate atlas is validated and every one of its 44 live GPU leases is observed.

Required:

```text
canonical_parameter_count=27
gradient_segment_count=44
linear_gradient_tile_count=42
rms_gradient_vector_count=2
parameter_gap=0
parameter_duplicate=0
gradient_tile_gap=0
gradient_tile_overlap=0
gradient_weight_alias=0
```

Each entry must bind canonical registry ordinal, canonical role, exact selected layer, source authority digest, completion authority, finite authority, segment ordinal and lease lineage.

## Wave 8: per-parameter aggregate

The 44 segment observations reduce to exactly 27 parameter aggregates.

Each aggregate publishes:

```text
registry_ordinal
semantic_id
segment_count
logical_scalar_count
nonzero_count
exact_zero_count
max_abs
l2_norm
classification
```

No parameter payload concatenation is allowed.

## Wave 9: base / structural / all aggregate

Three aggregate device-local R20-LASSQ norms are published:

```text
BASE_9_PARAMETER_GRADIENTS
STRUCTURAL_18_PARAMETER_GRADIENTS
ALL_27_PARAMETER_GRADIENTS
```

Required:

```text
base_parameter_count=9
structural_parameter_count=18
all_parameter_count=27
```

This wave establishes whether any exact finite nonzero canonical gradient exists in base, structural and total selected-layer scopes.

## Wave 10: R20 finalized-gradient / R27 Adam source parity

R27 retains the exact 44 R20 finalized-gradient leases used by step-2 Adam long enough for the observer to compare them with the R25 source gradient set.

Required:

```text
r20_observer_segment_identity_match=44
r20_observer_global_norm_parity=1
r27_optimizer_gradient_source_match=1
```

For the current one-admission / unit-scale / unit-contribution R27 path, exact element parity between R25 source and R20 finalized gradient is required.

The observer recomputes all-44 norm using the same R20 norm shaders and requires the resulting F32 norm bits to equal R27 step-2 global norm bits.

If canonical source gradients contain nonzero values while the R20 finalized atlas or R27 optimizer source is zero/mismatched, the patch fails closed.

## Mandatory carrier zero frontier

The mandatory carrier spine is evaluated in exact order:

```text
R24 dNormalizedHidden
R24 dFinalHidden
R25 REAL upstream ingress
R13 dNormalizedFFNInput
R14 attention residual carrier
R15 dInputHiddenTotal
R18 dInputHiddenComplete
```

Frontier result is one of:

```text
SOURCE_ZERO
FIRST_ZERO_AFTER_NONZERO
NO_ZERO_FRONTIER
EVIDENCE_INSUFFICIENT
```

`FIRST_ZERO_AFTER_NONZERO` requires a live upstream carrier with nonzero_count > 0 followed by a live finite carrier with nonzero_count == 0.

Independent parameter-gradient families are not forced into a fake single ordering.

## Gradient value verdict

The canonical selected-layer gradient verdict is one of:

```text
NONZERO_PATH_PRESENT
PARTIAL_ZERO_WITH_NONZERO_PATH
ALL_CANONICAL_GRADIENT_ZERO
```

Nonfinite, lineage and reduction-parity failures reject before a normal verdict is published.

Definitions:

```text
ALL_CANONICAL_GRADIENT_ZERO
  all 44 canonical segments are finite and exact zero

PARTIAL_ZERO_WITH_NONZERO_PATH
  canonical total contains at least one nonzero value and at least one zero-containing parameter/segment

NONZERO_PATH_PRESENT
  canonical selected-layer gradient contains finite nonzero values without requiring all independent families to be nonzero
```

## BaseTrain value admission split

Observer PASS and meaningful BaseTrain gradient-value admission are separate authorities.

R27-R1 can PASS with:

```text
gradient_value_path_verdict=ALL_CANONICAL_GRADIENT_ZERO
basetrain_gradient_value_admission_ready=0
```

BaseTrain gradient-value admission requires:

```text
production_observation_nonfinite_count=0
canonical_parameter_count=27
gradient_segment_count=44
base_nonzero_observed=1
r20_observer_global_norm_parity=1
r27_optimizer_gradient_source_match=1
```

No silent admission of an all-zero canonical gradient set is permitted.

## Production readback boundary

Allowed D2H is compact observation telemetry only:

```text
integer counts
max_abs scalar
per-segment LASSQ pair
global L2 norm scalar
compact status words
receipt/digest metadata
```

Forbidden:

```text
full carrier payload readback
full gradient segment readback
host gradient vector
host gradient concatenation
full dInputHidden readback
weight payload readback
optimizer state payload readback
```

Required:

```text
production_gradient_payload_readback=0
production_carrier_payload_readback=0
production_weight_payload_readback=0
production_optimizer_state_payload_readback=0
compact_observation_readback=1
```

## Ownership and lifetime

The observer does not become canonical source-payload owner.

```text
producer owns source lease
observer borrows source lease read-only
observer owns compact stat buffers/receipts only
```

R27 retains step-2 R20 finalized gradient leases in `BaseTrainR27LayerOutput` only to support exact same-invocation observation/parity. This retention does not redefine optimizer or gradient ownership.

No observer path may release a source before its semantic consumers and compact observation complete.

## No recomputation fallback

Forbidden:

```text
decoder_forward_recompute_for_observation
attention_forward_recompute_for_observation
qkv_forward_recompute_for_observation
loss_recompute_for_observation
backward_recompute_for_observation
checkpoint_reopen_for_observation
checkpoint_weight_reload_for_observation
```

Missing live evidence is not silently reconstructed.

## Negative canaries

The current R27-R1 bake includes 12 actual atlas-inventory validator negative mutations and requires all to be rejected:

1. missing canonical parameter entry
2. duplicate canonical parameter semantic identity
3. wrong canonical registry ordinal
4. wrong selected-layer identity
5. missing source authority digest
6. finite authority removed
7. completion authority removed
8. gradient payload segment removed
9. gradient segment metadata removed
10. tile-gap receipt injected
11. tile-overlap receipt injected
12. gradient/weight-alias receipt injected

In addition, live production nonfinite values, R27 PASS-token mismatch, R24/R25 authority mismatch, selected-layer cross-stage mismatch, R20 finalized/source payload mismatch and R20/R27 norm mismatch are hard fail-closed paths in the real execution path.

The current patch does not promote metadata-only canaries to production payload authority.

Required:

```text
negative_canaries=12
```

## Reproducibility

The complete compact observation digest is built twice from unchanged observation records, per-parameter aggregates, frontier, global norms and parity state.

Required:

```text
reproducibility_runs=2
reproducibility_match=1
```

The same live source leases and deterministic registry ordering are required.

## CLI authority

Exactly 64 R27-R1 gates are required, contiguous and exact-once:

```text
--require-bt-wgsl-r27r1-contract-001
...
--require-bt-wgsl-r27r1-contract-064
```

The same exact 64-gate set must exist in:

```text
runtime validator
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c.args
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c_full.args
resolved-args repair input/output
```

The dedicated contract fragment is:

```text
specs/cli/ash_basetrain_structural_lookahead_decoder_coupling_06c_r27r1_contract.args
```

## Required receipts

```text
r27r1_wave_00_parent_identity.json
r27r1_wave_01_r24_real_loss_vjp.json
r27r1_wave_02_r25_r13_ingress_ffn.json
r27r1_wave_03_r14_postrms_oproj_attention.json
r27r1_wave_04_r15_neox_qkv_inputrms.json
r27r1_wave_05_r17_deltaq_gate.json
r27r1_wave_06_r18_factor_head_residual.json
r27r1_wave_07_canonical_27x44_gradient_segments.json
r27r1_wave_08_parameter_aggregates.json
r27r1_wave_09_base_structural_global_aggregate.json
r27r1_wave_10_r20_r27_parity.json
r27r1_wave_11_frontier_reproducibility_seal.json
bt_wgsl_real_gradient_observability_atlas_06c_r27_r1_final.json
```

Receipt filenames may be emitted through the canonical wave writer naming convention as long as wave ordinal, semantic wave name and deterministic digest remain exact.

## Expected physical summary

```text
r27_physical_parent=1
canonical_production_training_state_generation=2
canonical_production_optimizer_generation=2
canonical_production_optimizer_step=2
step2_real_loss_authority=1
step2_real_loss_vjp=1
step2_selected_layer_real_backward=1
step2_gradient_origin=REAL_LOSS
observer_math_mutation=0
gradient_mutation=0
optimizer_mutation=0
weight_mutation=0
r20_lassq_math_single_authority=1
observer_private_norm_formula=0
canonical_parameter_count=27
gradient_segment_count=44
linear_gradient_tile_count=42
rms_gradient_vector_count=2
production_observation_nonfinite_count=0
r24_dnormalized_nonzero_count=<runtime>
r24_dfinal_nonzero_count=<runtime>
r25_real_upstream_nonzero_count=<runtime>
base_gradient_nonzero_count=<runtime>
structural_gradient_nonzero_count=<runtime>
canonical_gradient_nonzero_count=<runtime>
base_nonzero_observed=<runtime>
structural_nonzero_observed=<runtime>
canonical_gradient_nonzero_observed=<runtime>
observer_all44_l2_norm=<runtime>
r20_global_norm=<runtime>
r27_step2_global_norm=<runtime>
r20_observer_segment_identity_match=44
r20_observer_global_norm_parity=1
r27_optimizer_gradient_source_match=1
mandatory_carrier_frontier_class=<runtime>
mandatory_carrier_frontier_stage=<runtime>
gradient_value_path_verdict=<runtime>
basetrain_gradient_value_admission_ready=<runtime>
mega_observation_buffer=0
gradient_payload_copy=0
host_gradient_materialization=0
production_gradient_payload_readback=0
production_carrier_payload_readback=0
production_weight_payload_readback=0
production_optimizer_state_payload_readback=0
compact_observation_readback=1
waves_sequential=1
parallel_lanes_within_wave=1
parallel_chunks_within_lane=1
cross_wave_overlap=0
receipt_atlas_waves=12
receipt_field_count_derived_from_registry=1
receipt_chunk_count_derived_from_wave_geometry=1
negative_canaries=12
reproducibility_runs=2
reproducibility_match=1
forward_math_change=0
backward_math_change=0
loss_math_change=0
optimizer_policy_change=0
full_model_gradient_authority=0
full_model_training_state_authority=0
checkpoint_write=0
r27r2_handoff_ready=1
proof_ledger=HOLD
```

## R27-R2 handoff

R27-R2 transport work may consume R27-R1 only after physical R27-R1 PASS plus:

```text
production_observation_nonfinite_count=0
r20_observer_global_norm_parity=1
r27_optimizer_gradient_source_match=1
reproducibility_match=1
```

Meaningful BaseTrain training-value admission additionally requires:

```text
basetrain_gradient_value_admission_ready=1
```

If all canonical gradients are zero, observation may PASS and R27-R2 transport mechanics may be tested, but production BaseTrain training-value admission remains HOLD.

## Authority transition

```text
R27 step-2 REAL backward
        |
        +-> live carrier leases
        |
        +-> 27 canonical parameters / 44 gradient segments
                 |
                 v
        R27-R1 read-only observer
                 |
       micro-atlas chunk parallelism
                 |
          semantic wave ordering
                 |
         compact observation atlas
                 |
        +--------+---------+
        |                  |
        v                  v
 zero frontier       R20/R27 parity
        |                  |
        +--------+---------+
                 v
       gradient-value verdict
                 |
                 v
 BaseTrain value admission READY/HOLD
                 |
                 v
             R27-R2
```

## PASS semantics

R27-R1 PASS means the exact live REAL-loss backward path was observed without mutating or materializing production gradient payloads; the 27-parameter / 44-segment inventory was completely bound; exact-zero, nonzero and nonfinite states were distinguished; device-local chunk/wave observation used R20's stable LASSQ mathematics as the single norm authority; R25 source gradients, R20 finalized gradients and R27 Adam source were cross-checked; zero-frontier evidence and BaseTrain value-admission state were published; negative inventory canaries were rejected; receipt geometry was runtime-derived; and the observer result was reproducible.

R27-R1 PASS does not mean:

```text
all gradients are nonzero
loss decreases
full-model gradients exist
production multi-microbatch exists
BaseTrain production loop is admitted
full-model training is admitted
checkpoint persistence is admitted
```

## PASS seal

```text
PASS_ASH_BASETRAIN_BT_WGSL_REAL_GRADIENT_OBSERVABILITY_ATLAS_06C_R27_R1
```
