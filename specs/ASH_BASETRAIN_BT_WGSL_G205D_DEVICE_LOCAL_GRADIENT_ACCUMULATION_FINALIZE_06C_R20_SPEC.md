# ASH-BASETRAIN-BT-WGSL-G205D-DEVICE-LOCAL-GRADIENT-ACCUMULATION-FINALIZE-06C-R20

## Revision

- Patch ID: `ASH-BASETRAIN-BT-WGSL-G205D-DEVICE-LOCAL-GRADIENT-ACCUMULATION-FINALIZE-06C-R20`
- Build revision: `bt-wgsl-g205d-device-local-gradient-accumulation-finalize-06c-r20`
- Physical parent: `ASH-BASETRAIN-BT-WGSL-CANONICAL-GRADIENT-ATLAS-G205D-LIVE-REBASE-06C-R19`
- Next consumer: R21 live Adam optimizer candidate
- Proof ledger: `HOLD`

## SSOT

R20 consumes the R19 descriptor-only selected-layer gradient atlas containing exactly 27 canonical parameters, 44 existing F32 GPU gradient leases and 50,560,768 logical gradient scalars. It creates a segmented device-local accumulation state, admits gradients only through explicit microbatch ordinal and batch-lineage contracts, applies upstream-gradient unscale exactly once, applies contribution weighting exactly once, commits each ordinal transactionally, finalizes the weighted mean exactly once, computes a stable device-local global norm, and publishes a nonmutating clip-scale device scalar with the finalized mean-gradient atlas.

R20 does not run Adam, read or write optimizer state, materialize a clipped-gradient copy, mutate weights, write checkpoints, establish final-loss authority, or claim full-model gradient authority.

The current 06C physical invocation contains only one distinct live R19 gradient atlas. R20 therefore admits exactly one real production microbatch and explicitly reports `productionMultiMicrobatchPhysical=false`. Multi-microbatch arithmetic is tested separately with an asymmetric three-microbatch synthetic oracle. Replaying one production atlas several times is not accepted as real multi-microbatch evidence.

## R19 physical parent

Required parent authority:

```text
r19_physical_parent=1
descriptor_atlas_authority=1
canonical_parameter_count=27
gradient_payload_lease_count=44
logical_gradient_scalar_count=50560768
mega_gradient_buffer=0
gradient_payload_copy=0
host_gradient_concat=0
production_gradient_payload_readback=0
g205d_live_descriptor_rebase=1
g205d_accumulation_window_admission=0
g205d_accumulation_dispatch=0
r20_handoff_ready=1
```

`dInputHiddenComplete` remains a non-parameter backward carrier and is preserved unchanged.

## Accumulation window identity

`R20GradientAccumulationWindowV1` binds selected layer, R19 selected-parameter-set digest, R19 canonical atlas digest, 27 parameter registry entries, 44 gradient segment identities, 50,560,768 logical F32 scalars, gradient origin class, target admission count, explicit upstream gradient scale, explicit contribution weight, explicit clip max norm, normalization policy and F32 accumulator dtype.

The current physical gate uses:

```text
target_admissions=1
upstream_gradient_scale=1.0
contribution_weight=1.0
clip_max_norm=1.0
gradient_origin=DETERMINISTIC_BACKWARD_FIXTURE_CHAIN
final_loss_authority=0
```

These values are explicit gate inputs, not silent defaults.

## Segmented device-local accumulator

One accumulator generation has the same 44-segment geometry as R19 and spans logically 50,560,768 F32 scalars or 202,243,072 bytes. R20 does not allocate one 202MB mega accumulator. Each R19 gradient segment maps to one corresponding accumulator segment. Canonical accumulation precision is F32. FP16/BF16 accumulation and implicit precision downgrade are prohibited.

## Two-generation transaction model

R20 maintains at most two logical accumulator generations: `COMMITTED/STABLE` and `CANDIDATE`. Peak logical accumulator payload across both generations is 404,486,144 bytes. This excludes R19 source-gradient ownership and small status/norm buffers, and is not a claim about allocator-reserved GPU bytes.

For admission `m`:

```text
factor_m = contribution_weight_m / upstream_gradient_scale_m
Candidate_m = Committed_(m-1) + source_gradient_m * factor_m
```

Ordinal 0 starts from an explicitly cleared stable generation. All 44 candidate segments must complete with valid identity and finite status before descriptor promotion. If any segment fails, the candidate generation is rejected and the previously committed generation is not mutated or published partially. No in-place mutation of the canonical committed accumulator is allowed.

## Ordinal and batch-lineage contract

Admission ordinals are exactly `0, 1, 2, ... target_admissions-1`. Every ordinal must bind a unique source-batch lineage. Duplicate ordinals, out-of-order ordinals, duplicate batch lineages, selected-set mismatches and segment-identity mismatches fail closed. Cross-microbatch floating-point atomics are not used. Accumulation order for a given segment is ascending microbatch ordinal.

## Unscale and contribution weighting

Every admission requires finite positive `upstream_gradient_scale` and `contribution_weight`. The source gradient is unscaled exactly once and contribution weight is applied exactly once during accumulation. R20 never infers that the upstream loss scale is 1.0. The current gate explicitly supplies 1.0.

## Finalization and mean exactly once

After exactly `target_admissions` commits:

```text
W = sum(contribution_weight_m)
G_mean = committed_sum / W
```

`W` must be finite and positive. Finalization is transactional. The committed sum is not divided in place. Mean values are written to the opposite candidate generation, all 44 segments must pass, and only then is that generation promoted as `FinalizedMeanGradient`. A second finalization or admission after finalization is invalid. The normalization operation count is exactly one.

## Stable global norm

R20 computes the norm of the finalized mean gradient entirely on device using scaled sum-of-squares pairs `(scale, ssq)`, with `norm = scale * sqrt(ssq)`. The implementation uses per-segment chunk partial LASSQ pairs, deterministic per-segment pair reduction, and deterministic fixed-topology reduction across the 44 segment ordinals. No global floating-point atomic sum is used. A zero global norm is a valid observation. Only the compact final norm scalar may be copied to the host for telemetry. Gradient and accumulator payloads remain device-local.

## Clip-scale candidate

R20 requires finite positive `clip_max_norm` and computes:

```text
if global_norm == 0:
    clip_scale = 1
else:
    clip_scale = min(1, clip_max_norm / global_norm)
```

No epsilon is injected. R20 does not allocate or publish a clipped-gradient payload. It publishes 44 finalized mean-gradient leases plus global-norm and clip-scale device scalars. R21 applies `clip_scale` when consuming each gradient segment.

## Production readback boundary

Allowed production D2H is restricted to compact status words, global norm scalar and clip scale scalar. Production readback of R19 gradient payloads, accumulator-generation payloads, finalized mean-gradient payloads and weight payloads is forbidden.

Required:

```text
production_gradient_payload_readback=0
production_accumulator_payload_readback=0
production_weight_payload_readback=0
```

Synthetic oracle payload readback is isolated and does not authorize production payload readback.

## Current live physical path

The current gate exercises one actual R19 admission:

```text
live_r19_admission_count=1
microbatch_ordinal=0
target_admissions=1
upstream_gradient_scale=1.0
contribution_weight=1.0
production_multi_microbatch_physical=0
```

This still exercises real device-local segment allocation, candidate writes, transaction promotion, transactional finalization, stable global norm and clip-scale publication.

## Synthetic multi-microbatch oracle

An isolated asymmetric three-microbatch oracle uses distinct gradients, scales `[2,4,8]` and contribution weights `[1,2,3]`. It proves exact ordered F32 accumulation for the chosen dyadic fixture, CPU-F64 weighted-mean semantic parity, CPU-F64 global-norm parity and CPU-F64 clip-scale parity. It does not promote `productionMultiMicrobatchPhysical`.

## Real negative canaries

R20 negative evidence contains nine rejected cases:

1. transaction candidate fails at synthetic segment ordinal 17 due to a real GPU nonfinite source
2. duplicate ordinal rejected by the actual admission validator
3. out-of-order ordinal rejected by the actual admission validator
4. duplicate source-batch lineage rejected by the actual admission validator
5. selected-parameter-set mismatch rejected by the window identity validator
6. segment identity mismatch rejected by the actual admission validator
7. nonfinite gradient scale rejected by the actual admission validator
8. nonfinite gradient rejected by the GPU fail-closed status path
9. admission after `FINALIZED` rejected by the window-state validator

The transaction canary submits 18 synthetic segments and injects NaN into segment 17. The backend returns failure before candidate-to-committed swap, so a partial ordinal cannot become canonical.

## Lifecycle and GC

Accumulator generations follow `ALLOCATED -> CANDIDATE -> GPU_COMPLETED -> COMMITTED -> GC_ELIGIBLE -> RELEASED`. A previous generation becomes GC-eligible only after the next descriptor generation is committed. Required: `commit_before_gc=1`, `premature_release=0`, `orphan_accumulator_generation=0`. R19 source gradients remain immutable throughout R20.

## R20 output

`BaseTrainR20LayerOutput` preserves selected layer, `dInputHiddenComplete`, 27 canonical parameter identities through the inherited registry, 44 finalized mean-gradient leases, finalized gradient atlas digest, global norm device scalar, clip scale device scalar, compact norm/clip telemetry, committed admission count and total contribution weight. It publishes `finalized_mean_gradient_authority=true`, `canonical_selected_layer_gradient_authority=true`, `full_model_gradient_authority=false`, `final_loss_authority=false`, and `r21_handoff_ready=true`.

## Optimizer boundary

R20 keeps `optimizer_candidate`, `optimizer_state_read`, `optimizer_state_write`, `weight_delta_materialization`, `weight_mutation`, and `checkpoint_write` at zero. R21 exclusively owns live Adam candidate evaluation.

## Reproducibility

The current live one-admission R20 path runs twice against the same immutable R19 parent and requires exact equality of accumulation window digest, finalized gradient atlas digest, global norm bits, clip scale bits and backend receipt digest. The first temporary finalized atlas is dropped before the second authority is retained.

## Required receipts

```text
r20_parent_r19_receipt.json
r20_window_identity_receipt.json
r20_explicit_scaling_policy_receipt.json
r20_accumulator_layout_receipt.json
r20_accumulator_generation_receipt.json
r20_live_admission_receipt.json
r20_transaction_commit_receipt.json
r20_transaction_abort_canary_receipt.json
r20_finalization_receipt.json
r20_mean_exactly_once_receipt.json
r20_stable_global_norm_receipt.json
r20_clip_candidate_receipt.json
r20_production_multi_microbatch_boundary_receipt.json
r20_synthetic_multi_microbatch_oracle_receipt.json
r20_negative_canary_receipt.json
r20_lifecycle_gc_receipt.json
r20_reproducibility_receipt.json
r20_r21_handoff_receipt.json
bt_wgsl_g205d_device_local_gradient_accumulation_finalize_06c_r20_final.json
```

## Receipt atlas

Exactly nine streaming waves:

```text
Wave 0 R19 parent / scope / window identity
Wave 1 accumulator layout / generation policy
Wave 2 live R19 admission / candidate execution
Wave 3 transaction commit / negative canaries
Wave 4 transactional finalization / mean exactly once
Wave 5 stable global norm / readback boundary
Wave 6 clip-scale candidate / compact telemetry
Wave 7 synthetic multi-microbatch oracle / reproducibility / lifecycle
Wave 8 R21 boundary / PASS / proof ledger
```

Required: `receipt_atlas_waves=9`, parallel receipt lane build, streaming deterministic merge, and `monolithic_final_json=0`.

## CLI gates

Exactly 87 R20 gates are required exactly once in runtime validation, short args, full args and resolved-args repair input. The canonical gate set is the 87 `--require-bt-wgsl-r20-*` entries baked into this revision's short args, full args, runtime validator and repair script. Static bake verification requires total=87 and unique=87 in each location.

## Expected physical summary

```text
r19_physical_parent=1
r19_descriptor_atlas_authority=1
selected_layer_count=1
canonical_parameter_count=27
gradient_segment_count=44
logical_gradient_scalar_count=50560768
accumulator_dtype=F32
accumulator_segment_count=44
accumulator_generation_logical_bytes=202243072
max_accumulator_generations=2
mega_accumulator_buffer=0
window_identity_bound=1
target_admissions=1
live_r19_admission_count=1
production_multi_microbatch_physical=0
microbatch_ordinal_monotonic=1
duplicate_source_batch_lineage=0
upstream_gradient_scale_explicit=1
current_gradient_scale=1.0
contribution_weight_explicit=1
current_contribution_weight=1.0
silent_loss_scale_default=0
candidate_generation_nonpublishing=1
atomic_descriptor_generation_promotion=1
partial_ordinal_publication=0
previous_generation_preserved_on_fault=1
unscale_exactly_once=1
contribution_weight_exactly_once=1
cross_microbatch_float_atomic_merge=0
gradient_payload_copy=0
host_gradient_materialization=0
r19_gradient_payload_mutation=0
committed_admission_count=1
total_contribution_weight=1.0
mean_exactly_once=1
finalized_mean_gradient_authority=1
admission_after_finalize=0
double_finalize=0
stable_global_norm=1
global_norm=<runtime>
global_norm_zero_valid=1
clip_max_norm=1.0
clip_scale=<runtime>
clipped_gradient_materialization=0
clip_candidate_nonmutating=1
synthetic_multi_microbatch_count=3
synthetic_ordered_f32_oracle=1
synthetic_cpu_f64_oracle=1
synthetic_global_norm_oracle=1
synthetic_clip_scale_oracle=1
transaction_abort_canary=1
negative_canaries=9
commit_before_gc=1
premature_release=0
orphan_accumulator_generation=0
production_gradient_payload_readback=0
production_accumulator_payload_readback=0
production_weight_payload_readback=0
optimizer_candidate=0
optimizer_state_read=0
optimizer_state_write=0
weight_delta_materialization=0
weight_mutation=0
checkpoint_write=0
final_loss_authority=0
full_model_gradient_authority=0
reproducibility_runs=2
reproducibility_match=1
r21_handoff_ready=1
receipt_atlas_waves=9
monolithic_final_json=0
proof_ledger=HOLD
```

## PASS seal

`PASS_ASH_BASETRAIN_BT_WGSL_G205D_DEVICE_LOCAL_GRADIENT_ACCUMULATION_FINALIZE_06C_R20`

The expanded runtime PASS token additionally seals explicit window/scaling policy, segmented transactional generation ownership, mean-exactly-once finalization, stable global norm, nonmaterialized clip-scale candidate, live-single-admission evidence discipline, synthetic three-microbatch arithmetic proof, real negative canaries, zero production payload readback, zero optimizer/weight mutation, R21 handoff, nine-wave receipt streaming and proof-ledger HOLD.