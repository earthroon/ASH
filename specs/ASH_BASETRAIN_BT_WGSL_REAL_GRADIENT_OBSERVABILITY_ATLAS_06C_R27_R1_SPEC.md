# ASH-BASETRAIN-BT-WGSL-REAL-GRADIENT-OBSERVABILITY-ATLAS-06C-R27-R1

## Revision

- Patch ID: `ASH-BASETRAIN-BT-WGSL-REAL-GRADIENT-OBSERVABILITY-ATLAS-06C-R27-R1`
- Build revision: `bt-wgsl-real-gradient-observability-atlas-06c-r27-r1`
- Physical parent: `ASH-BASETRAIN-BT-WGSL-PRODUCTION-ADAM-STATE-CARRY-MULTISTEP-06C-R27`
- Next consumer: `ASH-BASETRAIN-BT-WGSL-GRADIENT-WAVE-TRANSACTION-06C-R27-R2`
- Proof ledger: `HOLD`

## SSOT

R27-R1 is a read-only observability layer over the already-physical R27 step-2 REAL-loss backward path.

It does not change forward, loss, backward, clipping, Adam, weight, optimizer-state, or production-root semantics. It observes the live GPU carriers and canonical selected-layer parameter gradients, classifies exact zero/nonzero/nonfinite values, compares the exact R25 source 44-gradient-segment set with the exact R20 finalized 44-segment set retained by R27, and checks that an independently executed R20 stable-LASSQ reduction over the same source gradients produces the exact R27 step-2 global-norm bits.

Zero is an observation, not an automatic correctness failure. Nonfinite values, lineage mismatch, canonical inventory mismatch, source/finalized segment mismatch, and R20/R27 norm mismatch fail closed.

## Parent authority

Required live R27 parent:

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
```

R27-R1 binds the exact R27 final receipt and the exact same-invocation live GPU leases. Receipt-only reconstruction, historical-fixture promotion, checkpoint reopen, and forward/backward recomputation for observation are forbidden.

## State ownership

```text
canonical gradient payload owner = existing R25/R20 producer
observer source access            = read-only borrowed GPU lease
observer-owned data               = compact stat/status buffers + receipts
R27 production root owner         = unchanged
```

R27 retains the exact step-2 R20 finalized-gradient leases plus step-2 global norm/clip scale only so R27-R1 can perform same-invocation parity checks. This retention does not create a second optimizer or gradient authority.

## Canonical gradient inventory

Selected-layer authority remains exactly:

```text
canonical parameters       = 27
base parameters            = 9
structural parameters      = 18
linear ROW_TILE segments   = 42
RMS FULL_VECTOR segments   = 2
GPU gradient segments      = 44
logical F32 scalars        = 50,560,768
```

The 27 roles and their immutable registry order remain the R19/R25 canonical registry.

Excluded from selected-layer parameter-gradient authority:

```text
FinalNorm dGamma sidecar
LM-head gradient
embedding gradient
bias gradient
complete dInput carrier
```

## Raw compact observation statistic

Each directly observed live GPU surface publishes only compact readback metadata:

```text
R27R1GradientObservationStat {
    element_count,
    finite_count,
    nonfinite_count,
    positive_count,
    negative_count,
    exact_zero_count,
    nonzero_count,
    max_abs,
    micro_atlas_page_count,
    max_page_workgroups,
    compact_readback_count,
    tensor_payload_readback_count,
}
```

No full carrier or gradient payload is copied to the host.

Exact-zero classification:

```text
+0.0              -> ZERO
-0.0              -> ZERO
finite value != 0 -> NONZERO
NaN / +/-Inf       -> NONFINITE
```

Subnormal finite nonzero values remain nonzero. No epsilon threshold is used for exact-zero authority.

Required partition:

```text
finite_count + nonfinite_count = element_count
exact_zero_count + nonzero_count = finite_count
positive_count + negative_count = nonzero_count
```

## R20 stable-LASSQ single norm authority

R27-R1 does not implement a second L2 formula.

Per-parameter, base, structural, and all-44 gradient norms are obtained through observer-private invocations of the existing R20 device-local accumulation/finalization path with exactly one admission, scale `1.0`, contribution weight `1.0`, and the existing R20 stable LASSQ shaders.

Required:

```text
r20_lassq_math_single_authority=1
observer_private_norm_formula=0
production_gradient_payload_readback=0
production_accumulator_payload_readback=0
```

The observer-private R20 runs allocate only temporary observer accumulation state and never mutate source gradient leases.

## Atlas chunk / wave execution

R27-R1 uses the existing `plan_micro_atlas_tensorcube_1d` geometry for direct zero/nonzero/nonfinite observation.

Execution authority is:

```text
semantic Wave 0
  -> observation lane A
       -> micro-atlas page 0
            -> GPU workgroups execute in parallel
       -> micro-atlas page 1
            -> GPU workgroups execute in parallel
  -> observation lane B
  -> deterministic wave receipt write

semantic Wave 1
  -> ...
```

Therefore the physical R27-R1 bake seals:

```text
waves_sequential=1
parallel_observation_lanes=0
gpu_workgroups_parallel_within_chunk=1
micro_atlas_chunk_planning=1
cross_wave_overlap=0
```

R27-R1 does not falsely claim CPU-thread-parallel observation lanes. Parallel lane scheduling is deferred to a later transport/performance patch after the value authority is physically established.

This still satisfies the current Atlas sequential-parallel contract at the physical compute level: dependency-bearing semantic waves are ordered, while workgroups inside each bounded micro-atlas dispatch execute in GPU parallel.

## Twelve semantic waves

Exactly 12 semantic receipt waves:

```text
Wave 0  R27 parent / generation / observer identity
Wave 1  R24 REAL-loss VJP surfaces
Wave 2  R25/R13 REAL ingress + FFN
Wave 3  R14 Post-RMS / OProj / actual attention
Wave 4  R15 NeoX / QKV / Input-RMS
Wave 5  R17 DeltaQ / Gate
Wave 6  R18 Factor / Head / residual
Wave 7  canonical 27/44 gradient segments
Wave 8  exact 27 per-parameter aggregates
Wave 9  base / structural / all-gradient aggregate norms
Wave 10 R25 source vs R20 finalized vs R27 norm parity
Wave 11 zero frontier / canaries / reproducibility / PASS
```

`receipt_atlas_waves=12` is semantic SSOT.

Receipt field count and physical receipt chunk count are runtime-derived from the emitted registry/wave list. Fixed duplicate field-count/chunk-count constants are prohibited.

## Wave 1: R24

Observe exact live:

```text
R24 real_dnormalized_hidden
R24 real_dfinal_hidden
```

Requires R24 REAL-loss backward authority. No second logit VJP or FinalNorm backward is executed.

## Wave 2: R25/R13

Observe:

```text
R25 REAL dFinal upstream ingress
R13 dDown output carrier
R13 DownProj dW tiles
R13 GateProj dW tiles
R13 UpProj dW tiles
```

The step-2 R13 output is explicitly retained from the real R25 replay and handed to R27-R1. No historical R13 fixture output is substituted.

## Wave 3: R14

Observe:

```text
attention residual backward carrier
base dQ
shared dK
shared dV
H1-H4 DeltaQ carriers
H1-H4 Gate carriers
Post-Attention RMSNorm dGamma
actual OProj dW tiles
```

Historical R12 fixture gradient authority remains retired.

## Wave 4: R15

Observe:

```text
Q pre-RoPE gradient
K pre-RoPE gradient
V gradient
dInputHiddenTotal
QProj/KProj/VProj dW tiles
Input RMSNorm dGamma
```

No QKV forward recompute or checkpoint reload is admitted.

## Wave 5: R17

Observe:

```text
H1-H4 structural cube gradients
H1-H4 DeltaQ projector dW
H1-H4 Gate projector dW
```

An exact-zero Gate-derived path remains a legal observation when mathematically produced by the current parent state.

## Wave 6: R18

Observe:

```text
H1-H4 structural residual carriers
dStructuralResidualTotal
dInputHiddenComplete
six shared Factor dW outputs
four Horizon Head dW outputs
```

Existing deterministic H1 -> H2 -> H3 -> H4 reductions remain unchanged.

## Wave 7: canonical 27/44 observation

Every live segment of the exact R25 REAL-loss candidate atlas is observed.

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

## Wave 8: per-parameter aggregation

The 44 segment stats are reduced by canonical parameter entry into exactly 27 parameter observations.

Each parameter publishes:

```text
registry_ordinal
semantic_id
segment_count
logical_scalar_count
exact_zero_count
nonzero_count
positive_count
negative_count
max_abs
l2_norm_from_R20_LASSQ
classification
```

Classification is one of:

```text
ZERO_OBSERVED
NONZERO_OBSERVED
MIXED_ZERO_NONZERO
EVIDENCE_INSUFFICIENT
```

## Wave 9: base / structural / all

R20-LASSQ observer-private reductions publish:

```text
base 9-parameter norm
structural 18-parameter norm
all 27-parameter / 44-segment norm
```

Alongside exact-zero/nonzero counts from the direct observer, this establishes whether base, structural, and canonical selected-layer gradient scopes contain any finite nonzero value.

## Wave 10: R20/R27 parity

R27 retains the exact 44 finalized R20 gradient leases used as the step-2 Adam source.

R27-R1 requires:

```text
R25 source segment count = 44
R20 finalized segment count = 44
exact GPU payload parity matches = 44
r20_observer_segment_identity_match=44
r27_optimizer_gradient_source_match=1
```

The all-44 observer-private R20 norm must have the exact same F32 bit pattern as `r27.step2_global_norm`:

```text
r20_observer_global_norm_parity=1
```

Any segment or norm mismatch fails closed.

## Mandatory carrier zero frontier

Mandatory ordered carrier spine:

```text
R24 dNormalizedHidden
R24 dFinalHidden
R25 REAL upstream ingress
R13 dDown output
R14 attention residual carrier
R15 dInputHiddenTotal
R18 dInputHiddenComplete
```

Frontier classification:

```text
SOURCE_ZERO
FIRST_ZERO_AFTER_NONZERO
NO_ZERO_FRONTIER
EVIDENCE_INSUFFICIENT
```

Independent parameter families are not forced into a false single derivative order.

## Canonical gradient verdict

```text
ALL_CANONICAL_GRADIENT_ZERO
PARTIAL_ZERO_WITH_NONZERO_PATH
NONZERO_PATH_PRESENT
EVIDENCE_INSUFFICIENT
```

R27-R1 observer PASS and BaseTrain value admission are separate.

Meaningful BaseTrain gradient-value admission requires:

```text
production_observation_nonfinite_count=0
canonical_parameter_count=27
gradient_segment_count=44
base_nonzero_observed=1
r20_observer_global_norm_parity=1
r27_optimizer_gradient_source_match=1
```

Thus an all-zero finite gradient can produce a valid R27-R1 observer PASS while:

```text
basetrain_gradient_value_admission_ready=0
```

No silent BaseTrain admission occurs.

## Negative canaries

R27-R1 reuses the canonical R19 metadata validator as the validator SSOT and physically mutates copies of the exact live metadata for 12 invalid cases:

1. missing parameter entry
2. duplicate semantic identity
3. wrong registry ordinal
4. selected-layer mismatch
5. missing source-authority digest
6. finite authority removed
7. completion authority removed
8. missing gradient-segment metadata
9. missing lease-lineage digest
10. row-tile gap
11. row-tile overlap
12. weight-alias authority removed

All 12 must reject through the real canonical validator.

Required:

```text
negative_canaries=12
```

## Readback boundary

Allowed production D2H:

```text
compact u32 observation counters
compact max-abs bits
R20 compact status words
R20 compact norm/clip scalar telemetry
parity status/compact receipts
```

Forbidden:

```text
full carrier payload readback
full gradient payload readback
host gradient concatenation
weight payload readback
optimizer-state payload readback
```

Required:

```text
production_gradient_payload_readback=0
production_carrier_payload_readback=0
production_weight_payload_readback=0
production_optimizer_state_payload_readback=0
compact_observation_readback=1
```

## Reproducibility

R27-R1 builds the final compact observation digest twice from the unchanged physical observation records, 27 parameter aggregates, zero-frontier result, all-44 norm and parity state.

Required:

```text
reproducibility_runs=2
reproducibility_match=1
```

This is receipt/digest reproducibility of the already-completed observation set. It is not falsely described as a second full backward or second full GPU observation replay.

## CLI authority

Exactly 64 R27-R1 gates, contiguous and exact-once:

```text
--require-bt-wgsl-r27r1-contract-001
...
--require-bt-wgsl-r27r1-contract-064
```

They must be exact-once in short args, full args, the dedicated R27-R1 contract fragment, runtime validation, and regenerated resolved args.

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
canonical_parameter_count=27
gradient_segment_count=44
production_observation_nonfinite_count=0
r24_dnormalized_nonzero_count=<runtime>
r24_dfinal_nonzero_count=<runtime>
r25_real_upstream_nonzero_count=<runtime>
base_gradient_nonzero_count=<runtime>
structural_gradient_nonzero_count=<runtime>
canonical_gradient_nonzero_count=<runtime>
observer_all44_l2_norm=<runtime>
r20_global_norm=<runtime>
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
parallel_observation_lanes=0
gpu_workgroups_parallel_within_chunk=1
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

R27-R2 transport work requires R27-R1 physical PASS plus:

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

If all 44 canonical gradients are finite exact zero, R27-R1 may PASS and later transport mechanics may still be tested, but production BaseTrain training-value admission stays HOLD.

## PASS semantics

R27-R1 PASS means the exact live R27 REAL-loss backward values were observed without source-payload mutation or full payload readback; the canonical 27/44 inventory was completely checked; 12 real invalid metadata mutations were rejected by the R19 validator; R25 source and R20 finalized gradient payloads matched for all 44 segments; the all-44 R20-LASSQ observation norm matched the R27 step-2 norm; zero-frontier and BaseTrain-value admission state were published; receipt geometry was runtime-derived; and no training semantic authority was silently widened.

PASS does not mean all gradients are nonzero, loss is decreasing, full-model gradients exist, real multi-microbatch training exists, or BaseTrain production is admitted.

## PASS seal

```text
PASS_ASH_BASETRAIN_BT_WGSL_REAL_GRADIENT_OBSERVABILITY_ATLAS_06C_R27_R1
```
