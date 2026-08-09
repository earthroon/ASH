# ASH-BASETRAIN-BT-WGSL-G205D-LIVE-ADAM-OPTIMIZER-CANDIDATE-06C-R21

## Revision

- Patch ID: `ASH-BASETRAIN-BT-WGSL-G205D-LIVE-ADAM-OPTIMIZER-CANDIDATE-06C-R21`
- Build revision: `bt-wgsl-g205d-live-adam-optimizer-candidate-06c-r21`
- Physical parent: `ASH-BASETRAIN-BT-WGSL-G205D-DEVICE-LOCAL-GRADIENT-ACCUMULATION-FINALIZE-06C-R20`
- Next consumer: R22 atomic candidate-weight + optimizer-state commit
- Proof ledger: `HOLD`

## SSOT

R21 consumes R20's finalized selected-layer gradient authority without changing R20 gradient payloads. The input consists of 27 canonical parameter identities, 44 finalized F32 gradient segments, the finalized R20 atlas identity, and the R20 device-resident clip scale. R21 applies an explicit Adam-V1 policy with zero weight decay, creates 44 candidate first-moment segments and 44 candidate second-moment segments, advances optimizer generation/step and beta-power lineage, and evaluates the exact bias-corrected Adam update expression on device. The full parameter delta is never materialized. Only compact update-norm and update-max-abs witnesses are reduced from the transient update expression.

R21 publishes a noncanonical candidate optimizer-state descriptor for R22. It does not read parameter weight payloads, does not materialize candidate weights or a delta atlas, does not commit canonical optimizer state, does not mutate weights, and does not write checkpoints.

## R20 parent authority

Required:

```text
r20_physical_parent=1
canonical_parameter_count=27
gradient_segment_count=44
logical_gradient_scalar_count=50560768
finalized_mean_gradient_authority=1
stable_global_norm=1
clip_scale_device_authority=1
production_gradient_payload_readback=0
production_accumulator_payload_readback=0
production_weight_payload_readback=0
optimizer_state_read=0
optimizer_state_write=0
weight_delta_materialization=0
weight_mutation=0
final_loss_authority=0
full_model_gradient_authority=0
r21_handoff_ready=1
```

## Explicit Adam-V1 audit policy

The current 06C audit invocation explicitly binds:

```text
algorithm     = ADAM_V1
learning_rate = 0.0001
beta1         = 0.9
beta2         = 0.999
epsilon       = 0.00000001
weight_decay  = 0
candidate_step = 1
```

These are audit-fixture inputs, not silently installed training defaults. R21 also seals the same mathematical policy through the existing historical G205D optimizer-profile contract with `algorithm=adam`, `bias_correction=true`, `weight_decay_mode=none`.

AdamW authority is zero. No coupled or decoupled weight-decay term is admitted.

## Effective gradient

For every scalar:

```text
g_eff = finalized_mean_gradient * clip_scale
```

The clip scale is read directly from R20's device scalar and is applied exactly once in the candidate-moment shader. No clipped-gradient payload is materialized.

## Optimizer state source and bootstrap

Current physical R21 has no previously committed optimizer state. Therefore the source state is explicitly:

```text
source = BOOTSTRAP_ZERO
source_optimizer_generation = 0
source_optimizer_step = 0
source_m_segments = 0
source_v_segments = 0
beta1_power_previous = 1
beta2_power_previous = 1
```

Bootstrap is legal only when generation and committed step are both zero and candidate step is exactly one. A nonzero committed state may never silently fall back to zero moments.

For a future committed source generation N / step T, R21 requires 44 source M + 44 source V segments with exact semantic/segment geometry and requires candidate generation N+1 / step T+1.

## Candidate moment geometry

```text
canonical parameters = 27
gradient segments    = 44
candidate M segments = 44
candidate V segments = 44
candidate state leases = 88
```

Moment dtype is F32. No FP16/BF16 optimizer-state path is admitted.

The logical scalar count per moment field is 50,560,768 F32 values. Therefore one candidate M+V generation spans:

```text
M logical bytes = 202,243,072
V logical bytes = 202,243,072
candidate M+V logical bytes = 404,486,144
```

R21 does not allocate a monolithic 404MB optimizer-state buffer. State remains segmented as 44 M + 44 V leases. A future non-bootstrap step may transiently hold source plus candidate generations, logically up to 808,972,288 bytes, still segmented and without a mega-state allocation.

## Adam equations

R21 uses:

```text
m_t = beta1 * m_(t-1) + (1-beta1) * g_eff
v_t = beta2 * v_(t-1) + (1-beta2) * g_eff^2
```

Candidate variance must remain finite and nonnegative.

## Beta-power lineage

R21 carries beta powers as optimizer state rather than recomputing `pow(beta, step)`:

```text
beta1_power_candidate = beta1_power_previous * beta1
beta2_power_candidate = beta2_power_previous * beta2
```

For the bootstrap step, prior powers are exactly one. `powf` step re-derivation count is zero.

## Bias correction and update operator

```text
m_hat = m_t / (1 - beta1_power_candidate)
v_hat = v_t / (1 - beta2_power_candidate)

DeltaTheta = -learning_rate * m_hat / (sqrt(v_hat) + epsilon)
```

Bias denominators must be finite and positive. R21 evaluates this update operator on GPU but never stores a full `DeltaTheta` tensor set.

## Device-local update witness

For each candidate segment, the update expression is evaluated transiently and reduced into fixed-topology scaled-sum-of-squares partials and maximum absolute value. Segment statistics are merged deterministically by segment ordinal. R21 publishes only:

```text
update_norm device scalar
update_max_abs device scalar
```

No unordered global floating-point atomic reduction is used. No weight payload is needed for pure Adam update evaluation.

## Current zero-gradient observation

The current R20 physical parent has a valid finalized live gradient norm of zero. Therefore the live R21 bootstrap may observe:

```text
candidate M = 0
candidate V = 0
update_norm = 0
update_max_abs = 0
```

This is a valid observation and is not a failure. There is no `BTR21OptimizerUpdateZero` failure. R21 never fabricates a nonzero update to satisfy a liveness gate.

## Synthetic nonzero Adam proof

Because current production fixture gradients are zero, R21 separately executes a small GPU synthetic proof.

Step 1:
- explicit zero-state bootstrap
- asymmetric positive/negative gradients
- clip scale 0.5
- nonzero M/V
- nonzero Adam update

Step 2:
- consumes the exact candidate M/V from synthetic step 1 as source state
- distinct asymmetric gradients
- clip scale 0.25
- advances generation and step
- advances beta-power lineage
- verifies state carry rather than re-bootstrap

GPU synthetic M/V and update witnesses are checked against an independent CPU-F64 Adam reference using bounded oracle-only tolerance. The fixture also verifies that applying clip scale changes at least one step-2 update component.

## Interior candidate-abort canary

R21 additionally creates an 18-segment nonzero synthetic optimizer state at step 1. Step 2 consumes that source state read-only and injects NaN into source gradient segment 17. The actual GPU candidate path must reject before publishing a complete candidate descriptor. Source optimizer state is never bound writable by the candidate kernel.

## Negative canaries

Eight required rejected contracts:

1. invalid beta
2. invalid epsilon
3. optimizer-step discontinuity
4. stale optimizer-state lineage
5. selected-parameter-set mismatch
6. state/gradient segment identity mismatch
7. zero-state bootstrap attempted over a prior generation
8. nonfinite gradient through the GPU fail-closed candidate path

The interior candidate abort is separately sealed as a transactional failure witness.

## Fail-closed numerics

Any nonfinite effective gradient, M, V, bias denominator, bias-corrected moment, update, update norm, or update max witness prevents candidate authority. NaN/Inf clamping, moment replacement, gradient fabrication, and silent epsilon substitution are prohibited.

## Production readback boundary

Production D2H is restricted to compact status words and the two update witness scalars. Required:

```text
production_gradient_payload_readback=0
production_optimizer_state_payload_readback=0
production_weight_payload_readback=0
```

Synthetic-oracle moment readback is isolated and does not establish production payload-readback authority.

## Candidate and commit boundary

R21 publishes:

```text
candidate_optimizer_state_authority=1
canonical_optimizer_state_authority=0
optimizer_state_commit=0
weight_delta_materialization=0
weight_candidate_materialization=0
weight_mutation=0
checkpoint_write=0
```

R22 exclusively owns candidate-weight materialization and the joint transaction that commits new weights, candidate M/V, step, and beta powers together.

## Reproducibility

The live R21 bootstrap is executed twice against the same immutable R20 parent. While both candidates are resident, all 44 M and 44 V leases are compared through the existing exact GPU parity pipeline, for 88 exact payload comparisons with zero production tensor payload readback. Required equality additionally covers semantic candidate-state digest, update-operator digest, beta-power bits, update-norm bits, update-max-abs bits, and backend receipt digest. The first candidate generation is dropped immediately after these comparisons.

## Required receipts

```text
r21_parent_r20_receipt.json
r21_optimizer_policy_receipt.json
r21_optimizer_source_state_receipt.json
r21_zero_state_bootstrap_receipt.json
r21_state_lineage_receipt.json
r21_moment_layout_receipt.json
r21_candidate_moment_execution_receipt.json
r21_bias_power_receipt.json
r21_bias_correction_receipt.json
r21_update_operator_receipt.json
r21_update_witness_receipt.json
r21_live_zero_update_receipt.json
r21_synthetic_step1_oracle_receipt.json
r21_synthetic_step2_state_carry_oracle_receipt.json
r21_cpu_f64_adam_oracle_receipt.json
r21_negative_canary_receipt.json
r21_candidate_abort_receipt.json
r21_candidate_lifecycle_receipt.json
r21_reproducibility_receipt.json
r21_r22_handoff_receipt.json
bt_wgsl_g205d_live_adam_optimizer_candidate_06c_r21_final.json
```

## Receipt Atlas

Nine deterministic waves:

```text
Wave 0 R20 parent / selected-layer scope / optimizer policy
Wave 1 source optimizer-state bootstrap / generation+step lineage
Wave 2 44 M + 44 V candidate geometry
Wave 3 Adam moment execution / beta-power lineage / bias correction
Wave 4 update operator / norm / max-abs witness
Wave 5 live zero-update observation / production readback boundary
Wave 6 synthetic step1 + step2 / CPU-F64 oracle
Wave 7 negative canaries / candidate abort / reproducibility
Wave 8 R22 boundary / PASS / proof ledger
```

Required:

```text
receipt_atlas_waves=9
parallel_receipt_lane_build=1
streaming_receipt_merge=1
deterministic_receipt_merge=1
monolithic_final_json=0
```

The final R21 atlas owns one global key owner for every field and fails closed on duplicate global keys.

## CLI gates

Exactly 85 R21 gates, each exactly once in runtime validation, short args, full args and resolved-args repair input:

```text
--require-bt-wgsl-r21-r20-physical-parent
--require-bt-wgsl-r21-r20-finalized-mean-gradient-authority
--require-bt-wgsl-r21-r20-gradient-leases-44
--require-bt-wgsl-r21-r20-parameter-registry-27
--require-bt-wgsl-r21-r20-clip-scale-device-authority
--require-bt-wgsl-r21-selected-layer-scope
--require-bt-wgsl-r21-gradient-origin-class-binding
--require-bt-wgsl-r21-adam-v1-no-weight-decay-policy
--require-bt-wgsl-r21-explicit-learning-rate
--require-bt-wgsl-r21-explicit-beta1
--require-bt-wgsl-r21-explicit-beta2
--require-bt-wgsl-r21-explicit-epsilon
--require-bt-wgsl-r21-explicit-step-index
--require-bt-wgsl-r21-zero-silent-hyperparameter-default
--require-bt-wgsl-r21-zero-adamw-authority
--require-bt-wgsl-r21-bootstrap-zero-state-explicit
--require-bt-wgsl-r21-bootstrap-only-without-prior-state
--require-bt-wgsl-r21-source-state-generation-binding
--require-bt-wgsl-r21-source-state-step-binding
--require-bt-wgsl-r21-source-state-selected-set-binding
--require-bt-wgsl-r21-source-state-segment-geometry-binding
--require-bt-wgsl-r21-beta1-power-lineage
--require-bt-wgsl-r21-beta2-power-lineage
--require-bt-wgsl-r21-candidate-step-exact-plus-one
--require-bt-wgsl-r21-candidate-state-generation-exact-plus-one
--require-bt-wgsl-r21-f32-moment-state
--require-bt-wgsl-r21-forty-four-m-segments
--require-bt-wgsl-r21-forty-four-v-segments
--require-bt-wgsl-r21-eighty-eight-candidate-state-leases
--require-bt-wgsl-r21-zero-mega-optimizer-state-buffer
--require-bt-wgsl-r21-segment-identity-exact-match
--require-bt-wgsl-r21-effective-gradient-clip-scale-applied-on-read
--require-bt-wgsl-r21-first-moment-exact-adam-equation
--require-bt-wgsl-r21-second-moment-exact-adam-equation
--require-bt-wgsl-r21-bias-correction-power-chain
--require-bt-wgsl-r21-no-powf-step-rederivation
--require-bt-wgsl-r21-update-operator-exact-adam-equation
--require-bt-wgsl-r21-zero-weight-decay-term
--require-bt-wgsl-r21-zero-weight-payload-read
--require-bt-wgsl-r21-zero-weight-delta-materialization
--require-bt-wgsl-r21-update-witness-device-local
--require-bt-wgsl-r21-update-norm-device-authority
--require-bt-wgsl-r21-update-max-abs-device-authority
--require-bt-wgsl-r21-zero-update-valid
--require-bt-wgsl-r21-candidate-state-nonpublishing
--require-bt-wgsl-r21-zero-canonical-optimizer-state-mutation
--require-bt-wgsl-r21-zero-weight-mutation
--require-bt-wgsl-r21-atomic-candidate-descriptor-seal
--require-bt-wgsl-r21-zero-partial-candidate-publication
--require-bt-wgsl-r21-fail-closed-numerics
--require-bt-wgsl-r21-zero-nan-clamp
--require-bt-wgsl-r21-zero-gradient-fabrication
--require-bt-wgsl-r21-production-gradient-payload-readback-zero
--require-bt-wgsl-r21-production-optimizer-state-payload-readback-zero
--require-bt-wgsl-r21-production-weight-payload-readback-zero
--require-bt-wgsl-r21-compact-scalar-telemetry-only
--require-bt-wgsl-r21-existing-g205d-optimizer-math-reuse
--require-bt-wgsl-r21-zero-host-gradient-bundle
--require-bt-wgsl-r21-zero-host-optimizer-state-bundle
--require-bt-wgsl-r21-synthetic-nonzero-step1-oracle
--require-bt-wgsl-r21-synthetic-nonzero-step2-state-carry-oracle
--require-bt-wgsl-r21-synthetic-bias-correction-oracle
--require-bt-wgsl-r21-synthetic-clip-applied-oracle
--require-bt-wgsl-r21-synthetic-update-norm-oracle
--require-bt-wgsl-r21-cpu-f64-adam-semantic-oracle
--require-bt-wgsl-r21-invalid-beta-negative-canary
--require-bt-wgsl-r21-invalid-epsilon-negative-canary
--require-bt-wgsl-r21-step-discontinuity-negative-canary
--require-bt-wgsl-r21-stale-state-lineage-negative-canary
--require-bt-wgsl-r21-selected-set-mismatch-negative-canary
--require-bt-wgsl-r21-segment-identity-mismatch-negative-canary
--require-bt-wgsl-r21-bootstrap-with-prior-state-negative-canary
--require-bt-wgsl-r21-nonfinite-gradient-negative-canary
--require-bt-wgsl-r21-candidate-abort-preserves-source-state
--require-bt-wgsl-r21-candidate-state-lifecycle
--require-bt-wgsl-r21-commit-deferred-to-r22
--require-bt-wgsl-r21-zero-checkpoint-write
--require-bt-wgsl-r21-final-loss-authority-deferred
--require-bt-wgsl-r21-full-model-gradient-authority-zero
--require-bt-wgsl-r21-current-live-bootstrap-step-one
--require-bt-wgsl-r21-current-live-zero-update-valid
--require-bt-wgsl-r21-double-run-reproducibility
--require-bt-wgsl-r21-atlas-wave-streaming-receipt
--require-bt-wgsl-r21-zero-monolithic-final-json
--require-bt-wgsl-r21-r22-handoff-ready
```

## Expected physical summary

```text
r20_physical_parent=1
r20_finalized_mean_gradient_authority=1
selected_layer_count=1
canonical_parameter_count=27
gradient_segment_count=44
gradient_origin_deterministic_fixture=1
adam_algorithm=ADAM_V1
adamw_authority=0
weight_decay=0
learning_rate_explicit=1
beta1_explicit=1
beta2_explicit=1
epsilon_explicit=1
step_explicit=1
silent_hyperparameter_default=0
optimizer_state_bootstrap=1
source_optimizer_generation=0
source_optimizer_step=0
candidate_optimizer_generation=1
candidate_optimizer_step=1
source_m_segments=0
source_v_segments=0
candidate_m_segments=44
candidate_v_segments=44
candidate_optimizer_state_leases=88
candidate_optimizer_state_logical_bytes=404486144
mega_optimizer_state_buffer=0
moment_dtype=F32
segment_identity_match=44
clip_scale_applied_on_read=1
first_moment_adam_equation=1
second_moment_adam_equation=1
beta1_power_lineage=1
beta2_power_lineage=1
powf_step_rederivation=0
bias_correction=1
weight_payload_read=0
weight_delta_materialization=0
weight_candidate_materialization=0
update_operator_device_execution=1
stable_update_norm=1
update_norm=<runtime>
update_max_abs=<runtime>
current_live_update_zero_observed=<runtime>
current_live_update_nonzero_required=0
candidate_optimizer_state_authority=1
canonical_optimizer_state_authority=0
candidate_descriptor_complete=1
partial_candidate_publication=0
source_optimizer_state_mutation=0
synthetic_step1_nonzero_oracle=1
synthetic_step2_state_carry_oracle=1
synthetic_bias_correction_oracle=1
synthetic_clip_applied_oracle=1
synthetic_update_norm_oracle=1
cpu_f64_adam_semantic_oracle=1
negative_canaries=8
candidate_abort_canary=1
candidate_abort_source_state_preserved=1
production_gradient_payload_readback=0
production_optimizer_state_payload_readback=0
production_weight_payload_readback=0
host_gradient_bundle=0
host_optimizer_state_bundle=0
optimizer_state_commit=0
weight_mutation=0
checkpoint_write=0
final_loss_authority=0
full_model_gradient_authority=0
reproducibility_runs=2
state_payload_parity_count=88
reproducibility_match=1
r22_handoff_ready=1
receipt_atlas_waves=9
monolithic_final_json=0
proof_ledger=HOLD
```

## PASS seal

`PASS_ASH_BASETRAIN_BT_WGSL_G205D_LIVE_ADAM_OPTIMIZER_CANDIDATE_06C_R21`

R21 ends with an actual device-local Adam candidate state and update witness, but not a committed training step. R22 must reacquire the selected parameter weights, apply the sealed update operator into candidate weight storage, validate candidate weight/version/finite lineage, and atomically commit weights and optimizer state together or reject the entire step.
