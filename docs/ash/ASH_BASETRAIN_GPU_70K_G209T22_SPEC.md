# ASH-BASETRAIN-GPU-70K-G209T22

## TensorCube Explicit Opt-In Candidate Dispatch Dry Run / Run Feature-Gated NonProduction Candidate Route Under Explicit Operator Opt-In / No Default Enable No Production Route No TensorCore Claim

PatchId: `ASH-BASETRAIN-GPU-70K-G209T22`  
SourcePatchId: `ASH-BASETRAIN-GPU-70K-G209T21`  
NextPatchId: `ASH-BASETRAIN-GPU-70K-G209T23`  
Phase: `PhaseT`

RuntimePassTarget: `PASS_ASH_BASETRAIN_GPU_70K_G209T22_TENSORCUBE_EXPLICIT_OPT_IN_CANDIDATE_DISPATCH_DRY_RUN_RUN_FEATURE_GATED_NONPRODUCTION_CANDIDATE_ROUTE_UNDER_EXPLICIT_OPERATOR_OPT_IN_NO_DEFAULT_ENABLE_NO_PRODUCTION_ROUTE_NO_TENSORCORE_CLAIM`

## Purpose

G209T22 consumes the G209T21 capability probe and disabled feature gate binding state. It creates an explicit operator opt-in receipt, opens the feature-gated TensorCube candidate route only inside `NonProductionCandidateOnly` scope, executes one candidate dispatch dry run, seals the dry run output capsule and telemetry receipt, then returns the feature gate to `Disabled`.

This patch does not enable the candidate route by default, change the default production route, switch production route pointers, apply candidate output to training, promote the candidate, grant replacement permission, or claim TensorCore hardware acceleration.

## Core Boundary

```text
source_patch_id=ASH-BASETRAIN-GPU-70K-G209T21
patch_id=ASH-BASETRAIN-GPU-70K-G209T22
next_patch_id=ASH-BASETRAIN-GPU-70K-G209T23
phase=PhaseT
training_loop_owner=training.rs
active_training_route=FreshInit
selected_tensorcube_policy=InternalTensorCube8x8CandidateRoute
tensorcube_candidate_route_scope=NonProductionCandidateOnly
source_tensorcube_capability_probe_receipt_loaded=true
source_tensorcube_dispatch_capability_verdict_loaded=true
source_tensorcube_feature_gate_receipt_loaded=true
source_tensorcube_feature_gate_default_disabled_receipt_loaded=true
source_tensorcube_feature_gate_explicit_opt_in_receipt_loaded=true
source_tensorcube_feature_gated_route_binding_receipt_loaded=true
source_tensorcube_dispatch_gate_policy_receipt_loaded=true
source_tensorcube_default_production_route_unchanged_receipt_loaded=true
source_tensorcube_post_feature_gate_rollback_latch_loaded=true
source_tensorcube_post_feature_gate_fallback_ready_loaded=true
tensorcube_explicit_operator_opt_in_receipt_created=true
tensorcube_explicit_operator_opt_in_scope=NonProductionCandidateOnly
tensorcube_explicit_operator_opt_in_status=Accepted
tensorcube_explicit_operator_opt_in_single_run_only=true
tensorcube_explicit_operator_opt_in_production_allowed=false
tensorcube_feature_gate_pre_dry_run_state=Disabled
tensorcube_feature_gate_dry_run_state=OptInDryRunEnabled
tensorcube_feature_gate_post_dry_run_state=Disabled
tensorcube_feature_gate_default_state_after_dry_run=Disabled
tensorcube_feature_gated_candidate_dry_run_session_created=true
tensorcube_feature_gated_candidate_dry_run_scope=NonProductionCandidateOnly
tensorcube_feature_gated_candidate_dry_run_started=true
tensorcube_feature_gated_candidate_dry_run_completed=true
tensorcube_feature_gated_candidate_dry_run_count=1
tensorcube_feature_gated_candidate_dry_run_status=Pass
tensorcube_feature_gated_candidate_dry_run_output_capsule_created=true
tensorcube_feature_gated_candidate_dry_run_output_sealed=true
tensorcube_feature_gated_candidate_dry_run_output_applied=false
tensorcube_feature_gated_candidate_dry_run_output_committed_to_training_route=false
tensorcube_feature_gated_candidate_dry_run_output_committed_to_production_route=false
tensorcube_feature_gated_candidate_dry_run_telemetry_created=true
tensorcube_feature_gated_candidate_dry_run_telemetry_status=Pass
tensorcube_feature_gate_relock_receipt_created=true
tensorcube_feature_gate_relock_status=Pass
tensorcube_feature_gate_relock_verified=true
tensorcube_post_opt_in_dry_run_rollback_latch_verified=true
tensorcube_post_opt_in_dry_run_fallback_ready=true
no_default_enable_dry_run_guard_created=true
no_production_route_dry_run_guard_created=true
no_production_pointer_switch_dry_run_guard_created=true
no_candidate_promotion_dry_run_guard_created=true
no_tensorcore_claim_dry_run_guard_created=true
default_production_route_changed=false
production_route_pointer_switch_executed=false
tensorcube_matmul_replacement_enabled=false
tensorcube_production_replacement_enabled=false
candidate_default_enabled=false
candidate_dispatch_enabled_by_default=false
candidate_dispatch_enabled_after_dry_run=false
candidate_promoted=false
replacement_permission_granted=false
tensorcore_route_enabled=false
tensorcore_hardware_acceleration_claimed=false
checkpoint_rewritten=false
safetensors_rewritten=false
production_base_weight_mutated=false
optimizer_state_mutated=false
training_weight_mutated=false
benchmark_claimed=false
model_improvement_claimed=false
deployment_ready_claimed=false
deployment_claimed=false
ready_for_g209t23=true
```

## Source SSOT

```text
G209T21 TensorCube dispatch capability probe receipt
G209T21 TensorCube dispatch capability verdict receipt
G209T21 TensorCube candidate dispatch feature gate receipt
G209T21 TensorCube feature gate default disabled receipt
G209T21 TensorCube feature gate explicit opt-in receipt
G209T21 TensorCube feature-gated route binding receipt
G209T21 TensorCube dispatch gate policy receipt
G209T21 TensorCube default production route unchanged receipt
G209T21 TensorCube post-feature-gate rollback latch receipt
G209T21 TensorCube post-feature-gate fallback readiness receipt
G209T21 no default production route guard
G209T21 no default candidate enable guard
G209T21 no production pointer switch feature gate guard
G209T21 no candidate promotion feature gate guard
G209T21 no TensorCore claim feature gate guard
```

## New G209T22 SSOT

```text
TensorCube explicit operator opt-in receipt
TensorCube explicit opt-in scope receipt
TensorCube feature gate pre-dry-run state receipt
TensorCube feature gate dry-run state receipt
TensorCube feature-gated candidate dry run session receipt
TensorCube feature-gated candidate dry run execution receipt
TensorCube dry run output capsule
TensorCube dry run output non-apply audit
TensorCube dry run telemetry receipt
TensorCube feature gate relock receipt
TensorCube feature gate post-dry-run disabled receipt
TensorCube post-opt-in-dry-run rollback latch receipt
TensorCube post-opt-in-dry-run fallback readiness receipt
no default enable dry run guard
no production route dry run guard
no production pointer switch dry run guard
no candidate promotion dry run guard
no TensorCore claim dry run guard
G209T23 entry packet
```

## Explicit Opt-In Contract

```text
tensorcube_explicit_operator_opt_in_receipt_created=true
tensorcube_explicit_operator_opt_in_scope=NonProductionCandidateOnly
tensorcube_explicit_operator_opt_in_status=Accepted
tensorcube_explicit_operator_opt_in_single_run_only=true
tensorcube_explicit_operator_opt_in_production_allowed=false
```

Explicit opt-in allows exactly one dry run under `NonProductionCandidateOnly`. It does not allow default enable, production use, candidate promotion, or replacement permission.

## Feature Gate State Transition Contract

Allowed transition:

```text
Disabled -> OptInDryRunEnabled -> Disabled
```

Forbidden transitions:

```text
Disabled -> Enabled
Disabled -> ProductionEnabled
OptInDryRunEnabled -> Enabled
OptInDryRunEnabled -> ProductionEnabled
OptInDryRunEnabled -> DefaultEnabled
```

## Dry Run Dispatch Contract

```text
tensorcube_feature_gated_candidate_dry_run_count=1
tensorcube_feature_gated_candidate_dry_run_status=Pass
tensorcube_feature_gated_candidate_dry_run_output_applied=false
tensorcube_feature_gated_candidate_dry_run_output_committed_to_training_route=false
tensorcube_feature_gated_candidate_dry_run_output_committed_to_production_route=false
```

The candidate route is dispatched once, explicitly operator opted-in, scoped to `NonProductionCandidateOnly`, and relocked after the run.

## Acceptance Criteria

PASS iff G209T21 source state is consumed, explicit operator opt-in is created, opt-in scope is `NonProductionCandidateOnly`, opt-in status is `Accepted`, opt-in is single-run only, production allowed is false, the feature gate transitions `Disabled -> OptInDryRunEnabled -> Disabled`, dry run count is exactly `1`, dry run status is `Pass`, output capsule is created and sealed, dry run output is not applied or committed, telemetry is created with `Pass`, relock status is `Pass`, default production route remains unchanged, candidate is not enabled by default or after dry run, TensorCore route and hardware claim remain false, no checkpoint/safetensors/base/optimizer/training mutation occurs, no benchmark/model/deployment claim occurs, and G209T23 entry packet is created.

## Rejection Criteria

Reject if source receipts cannot be loaded, explicit opt-in is absent, opt-in scope is not `NonProductionCandidateOnly`, opt-in status is not `Accepted`, dry run count is not `1`, dry run fails, feature gate does not relock to `Disabled`, dry run output is applied or committed, default production route changes, production pointer switch occurs, candidate is enabled by default or after dry run, candidate is promoted, TensorCore is enabled or claimed, checkpoint/safetensors/base/optimizer/training state mutates, or benchmark/model/deployment claims are made.

## Suggested Runtime

```text
crates/base_train/src/bin/ash_basetrain_gpu_70k_g209t22_tensorcube_explicit_opt_in_dry_run.rs
```

Runtime binary:

```text
ash_basetrain_gpu_70k_g209t22_tensorcube_explicit_opt_in_dry_run
```

## Static Surface Expectations

```text
runtime_outputs_prebaked=0
target_writer_json_macro_count=0
target_writer_recursion_limit_count=0
serde_json_map_import=true
json_atlas_writer=true
target_writer_ensure_macro_count=1
boolean_value_flags_allowed=false
string_mode_args_required=true
ps1_files_included=0
py_files_included=0
sha256_files_included=0
source_patch_parse_check=true
selected_policy_parse_check=true
route_scope_parse_check=true
explicit_opt_in_status_parse_check=true
feature_gate_state_parse_check=true
dry_run_count_parse_check=true
dry_run_status_parse_check=true
dry_run_output_apply_status_parse_check=true
feature_gate_relock_status_parse_check=true
default_production_route_parse_check=true
candidate_default_enable_parse_check=true
tensorcore_claim_parse_check=true
verdict=PASS_STATIC_SURFACE
```

## Cargo Run Command

```bash
cargo run -p base_train --bin ash_basetrain_gpu_70k_g209t22_tensorcube_explicit_opt_in_dry_run
```

Expected local PASS marker:

```text
PASS_ASH_BASETRAIN_GPU_70K_G209T22_TENSORCUBE_EXPLICIT_OPT_IN_CANDIDATE_DISPATCH_DRY_RUN_RUN_FEATURE_GATED_NONPRODUCTION_CANDIDATE_ROUTE_UNDER_EXPLICIT_OPERATOR_OPT_IN_NO_DEFAULT_ENABLE_NO_PRODUCTION_ROUTE_NO_TENSORCORE_CLAIM
```

## Next Patch

`ASH-BASETRAIN-GPU-70K-G209T23`

```text
TensorCube Opt-In Dry Run Delta Receipt And Fallback Replay / Compare Explicit Opt-In Dry Run Output Against Frozen Baseline And Replay Fallback / No Persistent Enable No Production Route No TensorCore Claim
```
