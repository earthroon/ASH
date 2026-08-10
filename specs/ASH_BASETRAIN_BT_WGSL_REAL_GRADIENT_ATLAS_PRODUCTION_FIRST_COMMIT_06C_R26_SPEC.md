# ASH-BASETRAIN-BT-WGSL-REAL-GRADIENT-ATLAS-PRODUCTION-FIRST-COMMIT-06C-R26

## Revision

- Patch ID: `ASH-BASETRAIN-BT-WGSL-REAL-GRADIENT-ATLAS-PRODUCTION-FIRST-COMMIT-06C-R26`
- Build revision: `bt-wgsl-real-gradient-atlas-production-first-commit-06c-r26`
- Physical parent: `ASH-BASETRAIN-BT-WGSL-REAL-LOSS-SELECTED-LAYER-BACKWARD-REBASE-06C-R25`
- Next consumer: `R27 PRODUCTION-ADAM-STATE-CARRY-MULTISTEP`
- Proof ledger: `HOLD`

## SSOT

R26 consumes the exact R25 `REAL_LOSS` selected-layer gradient authority and performs the first selected-layer production training-state commit. The 27-parameter / 44-lease R19 descriptor semantics are reused without relabeling or mutating the historical deterministic-fixture R19 atlas. R26 feeds the real leases directly into the proven R20 device-local accumulation backend, then into a fresh production-only Adam-V1 zero-state bootstrap, then into the proven R22 candidate-weight backend. Exactly 27 candidate weights + 44 M + 44 V = 115 payload leases are sealed under one `PRODUCTION_REAL_LOSS_SELECTED_LAYER` root and promoted by a single atomic root-descriptor commit.

The production root is a training-state authority. R26 does not yet prove that the decoder runtime consumes the committed candidate weights on the next forward. That state-carry/next-forward boundary belongs to R27.

## R25 parent and real atlas

Required physical parent state:

```text
r25_physical_parent=1
real_loss_authority=1
real_loss_backward_authority=1
selected_layer_gradient_origin=REAL_LOSS
gradient_origin_deterministic_fixture=0
r26_handoff_ready=1
```

R26 adopts exactly 44 R25 GPU gradient leases and preserves the selected-layer registry:

```text
selected_layer_count=1
canonical_parameter_count=27
base_parameter_count=9
structural_parameter_count=18
linear_gradient_tile_count=42
rms_gradient_vector_count=2
gradient_payload_lease_count=44
logical_gradient_scalar_count=50560768
logical_gradient_f32_bytes=202243072
```

Parameter identities and versions remain unchanged. The historical R19 fixture atlas is immutable and its payloads are never consumed. R26's canonical real atlas is the R25 atlas promoted under new production authority, with `canonical_gradient_atlas_origin=REAL_LOSS`.

Zero mega-gradient buffer, zero gradient payload copy, zero host gradient concatenation, exact coverage, and zero gradient/weight alias remain mandatory.

## R20 production accumulation

The R20 backend is reused directly rather than invoking the historical R20 orchestrator receipt path. One physical real microbatch is admitted:

```text
target_admissions=1
live_real_admission_count=1
production_multi_microbatch_physical=0
upstream_gradient_scale=1.0 explicit
contribution_weight=1.0 explicit
clip_max_norm=1.0 explicit
```

Device-local semantics remain:

```text
F32 accumulator
44 segments
max generations=2
unscale exactly once
contribution weight exactly once
mean exactly once
zero cross-microbatch float atomics
stable global norm
zero norm valid
clip scale derived once
zero clipped-gradient materialization
```

The R20 backend is executed twice from the same immutable real admission and all 44 finalized gradient payloads are compared GPU-side exact. The three-microbatch synthetic R20 oracle remains required but does not become production authority.

## Fresh production Adam namespace

R26 introduces `PRODUCTION_SELECTED_LAYER_ADAM_V1`. Historical fixture R21/R22 M/V/root state is neither source nor bootstrap evidence for production.

First production state:

```text
production_optimizer_state_bootstrap=1
source_production_optimizer_generation=0
source_production_optimizer_step=0
candidate_optimizer_generation=1
candidate_optimizer_step=1
source_m_segments=0
source_v_segments=0
candidate_m_segments=44
candidate_v_segments=44
candidate_optimizer_state_leases=88
moment_dtype=F32
```

Adam policy is the established explicit Adam-V1 policy:

```text
lr=0.0001
beta1=0.9
beta2=0.999
epsilon=1e-8
weight_decay=0
AdamW authority=0
```

Clip scale is applied on gradient read exactly once. Beta powers are carried as state and no step-based `powf` re-derivation is admitted. Candidate Adam is built twice and all 88 M/V payloads are GPU-side exact compared. The independent synthetic step1/step2 CPU-F64 Adam oracle remains required.

## Candidate weights and exact update segments

R26 reacquires the exact 27 selected-layer source weights from the same canonical forward tape/weight generation used by R25. Source semantic identity and parameter version must match all 27 entries; checkpoint reopen, checkpoint weight reload and host weight shuttle remain zero.

Exactly 44 update segments map the 44 M/V pairs into the 27 parameter surfaces. Segment semantics preserve the repaired rule:

```text
optimizer ordering = global segment ordinal
semantic suffix    = parameter-local segment ordinal
```

Weight application consumes candidate M/V and Adam policy only. Gradient payloads are not reconsumed and clip is not reapplied.

Candidate geometry:

```text
candidate_weight_count=27
candidate_weight_dtype=F32
candidate_weight_logical_scalars=50560768
candidate_weight_logical_bytes=202243072
mega_candidate_weight_buffer=0
coverage_gap=0
coverage_overlap=0
out_of_range=0
candidate_weight_finite=1
candidate_weight_complete=1
```

Candidate weights are built twice and all 27 payloads are GPU-side exact compared. Numerical weight change is an observation, not a required gate.

## Production root

Bootstrap source root:

```text
lineage_class=PRODUCTION_BOOTSTRAP_SOURCE
training_generation=0
optimizer_generation=0
optimizer_step=0
W=27
M=0
V=0
payload_leases=27
production_training_state=0
```

Candidate/committed root:

```text
lineage_class=PRODUCTION_REAL_LOSS_SELECTED_LAYER
training_generation=1
optimizer_generation=1
optimizer_step=1
W=27
M=44
V=44
payload_leases=115
production_training_state=1
```

One root-descriptor promotion is authoritative. Per-parameter promotion, weight-before-optimizer publication, optimizer-before-weight publication and partial 114/115 roots are forbidden.

After PASS:

```text
production_weight_commit_authority=1
production_optimizer_commit_authority=1
production_training_state_authority=1
production_training_state_scope=SELECTED_LAYER
full_model_training_state_authority=0
```

The runtime decoder block is not yet rebound to candidate weights:

```text
next_step_forward_consumption_authority=0
next_optimizer_state_bootstrap_expected=0
```

R27 must consume this step-1 production root rather than bootstrap again.

## Fixture isolation and canaries

Historical fixture R19/R20/R21/R22 receipts and payloads remain immutable and nonproduction. R26 rejects fixture atlas contamination, fixture-root escalation, stale source roots, duplicate commit, pre-existing production state in first-commit mode, and partial 114/115 candidate roots. Backend synthetic abort/nonfinite oracles remain fail-closed.

Forbidden repair paths:

```text
NaN -> 0
Inf -> 0
missing real gradient -> fixture gradient
missing gradient -> zero
invalid production state -> bootstrap retry
nonfinite candidate weight -> source weight
```

## Lifetime and readback

Commit-before-GC is mandatory. R25's 44 lease owner pins are transferred into the R26 transaction. No gradient, weight, candidate-weight, accumulator, or optimizer-state payload may be read back on the production path. Compact scalar telemetry such as global norm, clip scale, update norm and update max abs is allowed.

```text
production_gradient_payload_readback=0
production_accumulator_payload_readback=0
production_optimizer_state_payload_readback=0
production_weight_payload_readback=0
production_candidate_weight_payload_readback=0
host_gradient_bundle=0
host_optimizer_state_bundle=0
host_weight_shuttle=0
checkpoint_write=0
```

## Reproducibility

R26 proves reproducibility before its one physical production commit:

```text
real atlas/descriptor reproducibility       2 runs
R20 finalized-gradient payload parity       44/44
Adam M/V payload parity                     88/88
candidate weight payload parity             27/27
candidate root descriptor parity             exact
physical production commit count             1
```

Reproducibility never means two production optimizer steps.

## Status ABI

```text
R26StatusV1
0 = INCOMPLETE
1 = COMPLETE
2 = NONFINITE
3 = R25_LINEAGE_MISMATCH
4 = REAL_ATLAS_COVERAGE_FAILURE
5 = FIXTURE_CONTAMINATION
6 = PRODUCTION_STATE_ALREADY_EXISTS
7 = OPTIMIZER_LINEAGE_FAILURE
8 = CANDIDATE_WEIGHT_FAILURE
9 = ATOMIC_COMMIT_FAILURE
```

Success is exactly 1.

## Receipt atlas

Exactly ten ordered waves:

```text
0 R25 parent / real gradient lease adoption
1 real parameter registry / R19 descriptor semantics
2 canonical REAL gradient atlas
3 R20 production accumulation / norm / clip
4 fresh production Adam candidate
5 exact source weights / candidate weights
6 115-payload atomic production root
7 fixture isolation / rollback / stale-root rejection
8 candidate reproducibility / lifetime / GC
9 production authority / R27 handoff / PASS / HOLD
```

```text
receipt_atlas_waves=10
monolithic_final_json=0
proof_ledger=HOLD
```

## CLI authority

Exactly 160 `--require-bt-wgsl-r26-*` gates are required and exact-once across runtime validation, short args, full args and resolved-args repair input.

### Exact gates

```text
--require-bt-wgsl-r26-r25-physical-parent
--require-bt-wgsl-r26-real-loss-authority
--require-bt-wgsl-r26-real-loss-backward-authority
--require-bt-wgsl-r26-selected-layer-real-backward-authority
--require-bt-wgsl-r26-gradient-origin-real-loss
--require-bt-wgsl-r26-zero-gradient-origin-fixture
--require-bt-wgsl-r26-r26-handoff-parent
--require-bt-wgsl-r26-r25-pass-token-binding
--require-bt-wgsl-r26-r25-real-atlas-binding
--require-bt-wgsl-r26-r25-gradient-lease-count-44
--require-bt-wgsl-r26-r25-gradient-owner-pins-44
--require-bt-wgsl-r26-selected-layer-count-one
--require-bt-wgsl-r26-r25-production-state-zero
--require-bt-wgsl-r26-r25-full-model-gradient-zero
--require-bt-wgsl-r26-r19-descriptor-semantics-reuse
--require-bt-wgsl-r26-historical-r19-fixture-atlas-immutable
--require-bt-wgsl-r26-historical-r19-fixture-payload-zero
--require-bt-wgsl-r26-zero-fixture-atlas-to-real-promotion
--require-bt-wgsl-r26-canonical-parameter-count-27
--require-bt-wgsl-r26-base-parameter-count-nine
--require-bt-wgsl-r26-structural-parameter-count-18
--require-bt-wgsl-r26-linear-gradient-tile-count-42
--require-bt-wgsl-r26-rms-gradient-vector-count-two
--require-bt-wgsl-r26-gradient-payload-lease-count-44
--require-bt-wgsl-r26-logical-gradient-scalars-exact
--require-bt-wgsl-r26-logical-gradient-bytes-exact
--require-bt-wgsl-r26-parameter-semantic-identity-exact
--require-bt-wgsl-r26-parameter-version-binding-exact
--require-bt-wgsl-r26-parameter-gap-zero
--require-bt-wgsl-r26-parameter-duplicate-zero
--require-bt-wgsl-r26-gradient-tile-gap-zero
--require-bt-wgsl-r26-gradient-tile-overlap-zero
--require-bt-wgsl-r26-gradient-out-of-range-zero
--require-bt-wgsl-r26-gradient-weight-alias-zero
--require-bt-wgsl-r26-descriptor-only-real-atlas
--require-bt-wgsl-r26-canonical-real-gradient-atlas-authority
--require-bt-wgsl-r26-production-accumulation-window
--require-bt-wgsl-r26-single-real-microbatch-admission
--require-bt-wgsl-r26-target-admissions-one
--require-bt-wgsl-r26-production-multimicrobatch-zero
--require-bt-wgsl-r26-explicit-upstream-gradient-scale
--require-bt-wgsl-r26-gradient-scale-one
--require-bt-wgsl-r26-explicit-contribution-weight
--require-bt-wgsl-r26-contribution-weight-one
--require-bt-wgsl-r26-f32-accumulator
--require-bt-wgsl-r26-accumulator-segments-44
--require-bt-wgsl-r26-two-generation-accumulator
--require-bt-wgsl-r26-zero-mega-accumulator
--require-bt-wgsl-r26-unscale-exactly-once
--require-bt-wgsl-r26-contribution-weight-exactly-once
--require-bt-wgsl-r26-mean-exactly-once
--require-bt-wgsl-r26-zero-cross-microbatch-float-atomic
--require-bt-wgsl-r26-stable-global-norm
--require-bt-wgsl-r26-zero-global-norm-valid
--require-bt-wgsl-r26-clip-max-norm-one
--require-bt-wgsl-r26-clip-scale-authority
--require-bt-wgsl-r26-fresh-production-optimizer-namespace
--require-bt-wgsl-r26-zero-fixture-optimizer-source
--require-bt-wgsl-r26-zero-fixture-training-root-source
--require-bt-wgsl-r26-zero-fixture-m-consumption
--require-bt-wgsl-r26-zero-fixture-v-consumption
--require-bt-wgsl-r26-production-zero-state-bootstrap
--require-bt-wgsl-r26-source-production-generation-zero
--require-bt-wgsl-r26-source-production-step-zero
--require-bt-wgsl-r26-candidate-production-generation-one
--require-bt-wgsl-r26-candidate-production-step-one
--require-bt-wgsl-r26-adam-v1
--require-bt-wgsl-r26-zero-adamw
--require-bt-wgsl-r26-zero-weight-decay
--require-bt-wgsl-r26-learning-rate-explicit
--require-bt-wgsl-r26-beta1-explicit
--require-bt-wgsl-r26-beta2-explicit
--require-bt-wgsl-r26-epsilon-explicit
--require-bt-wgsl-r26-candidate-step-explicit
--require-bt-wgsl-r26-zero-silent-hyperparameter-default
--require-bt-wgsl-r26-candidate-m-segments-44
--require-bt-wgsl-r26-candidate-v-segments-44
--require-bt-wgsl-r26-candidate-optimizer-leases-88
--require-bt-wgsl-r26-f32-moment-authority
--require-bt-wgsl-r26-clip-scale-applied-on-read
--require-bt-wgsl-r26-source-weight-count-27
--require-bt-wgsl-r26-source-weight-semantic-match-27
--require-bt-wgsl-r26-source-weight-version-match-27
--require-bt-wgsl-r26-source-weight-read-only
--require-bt-wgsl-r26-zero-checkpoint-reopen
--require-bt-wgsl-r26-zero-checkpoint-weight-reload
--require-bt-wgsl-r26-candidate-weight-count-27
--require-bt-wgsl-r26-candidate-weight-f32
--require-bt-wgsl-r26-candidate-weight-scalars-exact
--require-bt-wgsl-r26-candidate-weight-bytes-exact
--require-bt-wgsl-r26-zero-mega-candidate-weight
--require-bt-wgsl-r26-update-segment-count-44
--require-bt-wgsl-r26-parameter-local-segment-semantic-id
--require-bt-wgsl-r26-zero-gradient-reconsumption
--require-bt-wgsl-r26-zero-clip-reapplication
--require-bt-wgsl-r26-candidate-weight-gap-zero
--require-bt-wgsl-r26-candidate-weight-overlap-zero
--require-bt-wgsl-r26-candidate-weight-out-of-range-zero
--require-bt-wgsl-r26-zero-cross-segment-weight-atomic
--require-bt-wgsl-r26-candidate-weight-finite
--require-bt-wgsl-r26-candidate-weight-complete
--require-bt-wgsl-r26-candidate-group-115-leases
--require-bt-wgsl-r26-atomic-root-descriptor-promotion
--require-bt-wgsl-r26-zero-per-parameter-promotion
--require-bt-wgsl-r26-zero-partial-training-state-publication
--require-bt-wgsl-r26-zero-weight-before-optimizer-commit
--require-bt-wgsl-r26-zero-optimizer-before-weight-commit
--require-bt-wgsl-r26-single-physical-production-commit
--require-bt-wgsl-r26-production-state-absent-before-first-commit
--require-bt-wgsl-r26-production-root-scope-selected-layer
--require-bt-wgsl-r26-zero-fixture-training-state-mutation
--require-bt-wgsl-r26-zero-fixture-optimizer-state-mutation
--require-bt-wgsl-r26-fixture-to-production-escalation-rejected
--require-bt-wgsl-r26-stale-root-rejection
--require-bt-wgsl-r26-duplicate-root-rejection
--require-bt-wgsl-r26-transaction-abort-source-preservation
--require-bt-wgsl-r26-production-root-priority-over-fixture
--require-bt-wgsl-r26-historical-fixture-prepass-authority-zero
--require-bt-wgsl-r26-zero-full-model-training-authority
--require-bt-wgsl-r26-zero-full-model-gradient-authority
--require-bt-wgsl-r26-zero-lm-head-gradient
--require-bt-wgsl-r26-zero-finalnorm-gradient-promotion
--require-bt-wgsl-r26-zero-embedding-gradient
--require-bt-wgsl-r26-zero-checkpoint-write
--require-bt-wgsl-r26-commit-before-gc
--require-bt-wgsl-r26-r25-gradient-owner-transfer
--require-bt-wgsl-r26-zero-premature-gradient-release
--require-bt-wgsl-r26-zero-premature-weight-release
--require-bt-wgsl-r26-zero-premature-optimizer-release
--require-bt-wgsl-r26-zero-orphan-candidate-weight
--require-bt-wgsl-r26-zero-orphan-candidate-optimizer
--require-bt-wgsl-r26-zero-production-gradient-readback
--require-bt-wgsl-r26-zero-production-accumulator-readback
--require-bt-wgsl-r26-zero-production-optimizer-readback
--require-bt-wgsl-r26-zero-production-weight-readback
--require-bt-wgsl-r26-zero-production-candidate-weight-readback
--require-bt-wgsl-r26-real-atlas-double-build-reproducibility
--require-bt-wgsl-r26-accumulator-double-build-reproducibility
--require-bt-wgsl-r26-adam-candidate-double-build-reproducibility
--require-bt-wgsl-r26-candidate-weight-double-build-reproducibility
--require-bt-wgsl-r26-gpu-payload-parity
--require-bt-wgsl-r26-r20-synthetic-multimicrobatch-oracle
--require-bt-wgsl-r26-r21-synthetic-adam-oracle
--require-bt-wgsl-r26-r22-synthetic-weight-update-oracle
--require-bt-wgsl-r26-fixture-contamination-negative-canary
--require-bt-wgsl-r26-stale-parameter-version-negative-canary
--require-bt-wgsl-r26-production-state-existing-negative-canary
--require-bt-wgsl-r26-partial-root-negative-canary
--require-bt-wgsl-r26-nonfinite-fail-closed-canary
--require-bt-wgsl-r26-zero-is-observation-not-failure
--require-bt-wgsl-r26-canonical-gradient-atlas-origin-real-loss
--require-bt-wgsl-r26-finalized-gradient-origin-real-loss
--require-bt-wgsl-r26-production-weight-commit-authority
--require-bt-wgsl-r26-production-optimizer-commit-authority
--require-bt-wgsl-r26-production-training-state-authority
--require-bt-wgsl-r26-selected-layer-production-scope
--require-bt-wgsl-r26-next-step-forward-consumption-zero
--require-bt-wgsl-r26-next-bootstrap-expected-zero
--require-bt-wgsl-r26-r27-handoff-ready
--require-bt-wgsl-r26-proof-ledger-hold
```

## Expected physical summary

```text
r25_physical_parent=1
selected_layer_gradient_origin=REAL_LOSS
gradient_origin_deterministic_fixture=0
r25_gradient_lease_adoption_count=44
canonical_parameter_count=27
linear_gradient_tile_count=42
rms_gradient_vector_count=2
gradient_payload_lease_count=44
canonical_gradient_atlas_authority=1
canonical_gradient_atlas_origin=REAL_LOSS
target_admissions=1
live_real_admission_count=1
production_multi_microbatch_physical=0
current_gradient_scale=1.0
current_contribution_weight=1.0
stable_global_norm=1
global_norm=<runtime>
clip_scale=<runtime>
optimizer_namespace=PRODUCTION_SELECTED_LAYER_ADAM_V1
fixture_optimizer_state_source=0
fixture_training_root_source=0
production_optimizer_state_bootstrap=1
source_production_optimizer_generation=0
source_production_optimizer_step=0
candidate_optimizer_generation=1
candidate_optimizer_step=1
candidate_m_segments=44
candidate_v_segments=44
candidate_optimizer_state_leases=88
source_weight_count=27
candidate_weight_count=27
update_segment_count=44
training_state_candidate_payload_leases=115
atomic_root_descriptor_promotion=1
production_weight_commit_authority=1
production_optimizer_commit_authority=1
production_training_state_authority=1
production_training_state_scope=SELECTED_LAYER
full_model_training_state_authority=0
canonical_production_training_state_generation=1
canonical_production_optimizer_generation=1
canonical_production_optimizer_step=1
candidate_reproducibility_runs=2
candidate_reproducibility_match=1
physical_production_commit_count=1
stale_candidate_rejection=1
fixture_to_production_escalation_rejected=1
commit_before_gc=1
checkpoint_write=0
next_step_forward_consumption_authority=0
next_optimizer_state_bootstrap_expected=0
status_abi=R26StatusV1
status_success_value=1
r27_handoff_ready=1
receipt_atlas_waves=10
monolithic_final_json=0
proof_ledger=HOLD
```

## PASS seal

```text
PASS_ASH_BASETRAIN_BT_WGSL_REAL_GRADIENT_ATLAS_PRODUCTION_FIRST_COMMIT_06C_R26
```

## Authority transition

```text
R25 REAL 27-param / 44-lease gradients
        ↓
R26 canonical REAL gradient atlas
        ↓
R20 device-local finalize / norm / clip
        ↓
fresh production Adam gen0/step0 -> gen1/step1
        ↓
44 M + 44 V
        ↓
27 candidate weights
        ↓
115-payload production transaction
        ↓
atomic selected-layer production root
        ↓
R27 state carry / next-forward consumption
```
