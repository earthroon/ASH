# ASH-BASETRAIN-GPU-70K-G190D

## Explicit Rollback Execution Approval Gate / Rollback Candidate To Operator Rollback Execution Decision / No Rollback Execution No Production Claim

PatchId: `ASH-BASETRAIN-GPU-70K-G190D`

SourcePatchId: `ASH-BASETRAIN-GPU-70K-G189D`

UpstreamDeniedAcceptanceSourcePatchId: `ASH-BASETRAIN-GPU-70K-G188A`

UpstreamPostApplyHealthSourcePatchId: `ASH-BASETRAIN-GPU-70K-G187A`

UpstreamRouteApplySourcePatchId: `ASH-BASETRAIN-GPU-70K-G186A`

RuntimePassTarget: `PASS_ASH_BASETRAIN_GPU_70K_G190D_EXPLICIT_ROLLBACK_EXECUTION_APPROVAL_GATE_ROLLBACK_CANDIDATE_TO_OPERATOR_ROLLBACK_EXECUTION_DECISION_NO_ROLLBACK_EXECUTION_NO_PRODUCTION_CLAIM`

G190D consumes the G189D rollback candidate and binds an explicit operator rollback execution decision. G190D must not execute rollback, must not rewrite route pointers, and must not claim production readiness.

## Required G189D inputs

```text
artifacts/ASH_BASETRAIN_GPU_70K_G189D_ACTIVE_ROUTE_ROLLBACK_PREFLIGHT_RECEIPT.json
artifacts/ASH_BASETRAIN_GPU_70K_G189D_G188A_DENIED_ACCEPTANCE_SOURCE_AUDIT.json
artifacts/ASH_BASETRAIN_GPU_70K_G189D_CURRENT_ACTIVE_ROUTE_OBSERVATION_AUDIT.json
artifacts/ASH_BASETRAIN_GPU_70K_G189D_ROLLBACK_METADATA_BINDING_AUDIT.json
artifacts/ASH_BASETRAIN_GPU_70K_G189D_ACTIVE_ROUTE_ROLLBACK_CANDIDATE_PACKET.json
artifacts/ASH_BASETRAIN_GPU_70K_G189D_ROLLBACK_CANDIDATE_PREFLIGHT_RESULT_PACKET.json
artifacts/ASH_BASETRAIN_GPU_70K_G189D_NO_ROUTE_POINTER_REWRITE_AUDIT.json
artifacts/ASH_BASETRAIN_GPU_70K_G189D_NO_PRODUCTION_CLAIM_AUDIT.json
artifacts/ASH_BASETRAIN_GPU_70K_G189D_NO_TRAINING_OR_WEIGHT_MUTATION_AUDIT.json
artifacts/ASH_BASETRAIN_GPU_70K_G189D_NEXT_PATCH_PACKET.json
```

G190D may observe `artifacts/ASH_ACTIVE_LEARNING_ROUTE_POINTER.json`, but it must not rewrite it.

## Required previous state

```text
previous_g189d_accepted=true
rollback_candidate_created=true
rollback_candidate_present=true
rollback_candidate_scope=ActiveLearningRoutePointerOnly
rollback_candidate_authority=PreflightOnly
rollback_candidate_current_path=AtlasGroupedSequentialIntegrationCandidate
rollback_candidate_target_restore_path=FreshInitBurnNativeTinyProof
rollback_candidate_has_no_execution_authority=true
rollback_candidate_has_no_route_pointer_write_authority=true
rollback_candidate_has_no_production_authority=true
rollback_candidate_has_no_training_authority=true
ready_for_explicit_rollback_execution_approval_gate=true
ready_for_rollback_execution=false
ready_for_production_claim=false
```

## Operator decision policy

Accepted CLI aliases:

```text
approve
approved
allow
allowed
grant
granted
deny
denied
reject
rejected
hold
```

Canonical outputs:

```text
operator_rollback_execution_decision=Approved
operator_rollback_execution_decision=Denied
operator_rollback_execution_decision_is_explicit=true
operator_rollback_execution_decision_bound=true
operator_rollback_execution_decision_source=OperatorCLI
```

G190D must not infer rollback execution approval from rollback candidate existence.

## Approved path

```text
operator_rollback_execution_decision=Approved
operator_rollback_execution_granted=true
operator_rollback_execution_denied=false
rollback_execution_approval_receipt_created=true
rollback_execution_decision_packet_created=true
rollback_execution_decision_result=ApprovedForRollbackPointerUpdateExecutionGate
ready_for_rollback_pointer_update_execution_gate=true
ready_for_rollback_hold_state_audit=false
ready_for_rollback_execution=false
ready_for_production_claim=false
```

## Denied path

```text
operator_rollback_execution_decision=Denied
operator_rollback_execution_granted=false
operator_rollback_execution_denied=true
rollback_execution_approval_receipt_created=true
rollback_execution_decision_packet_created=true
rollback_execution_decision_result=DeniedRollbackHoldStateRequired
ready_for_rollback_pointer_update_execution_gate=false
ready_for_rollback_hold_state_audit=true
ready_for_rollback_execution=false
ready_for_production_claim=false
```

## Forbidden operations

```text
active_learning_route_pointer_rewritten_in_g190d=true
default_route_pointer_rewritten_in_g190d=true
production_route_pointer_rewritten_in_g190d=true
route_switch_rollback_executed_in_g190d=true
rollback_execution_performed=true
rollback_pointer_update_applied=true
rollback_candidate_rewritten=true
rollback_candidate_authority_rewritten=true
production_claimed=true
production_ready_claimed=true
deployment_ready_claimed=true
training_quality_claimed=true
optimizer_quality_claimed=true
model_improvement_claimed=true
loss_trend_claimed=true
base_weight_mutated_in_g190d=true
```

## CLI

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g190d_explicit_rollback_execution_approval_gate -- `
  --local-root . `
  --out-dir artifacts `
  --source-patch-id ASH-BASETRAIN-GPU-70K-G189D `
  --upstream-denied-acceptance-source-patch-id ASH-BASETRAIN-GPU-70K-G188A `
  --upstream-post-apply-health-source-patch-id ASH-BASETRAIN-GPU-70K-G187A `
  --upstream-route-apply-source-patch-id ASH-BASETRAIN-GPU-70K-G186A `
  --explicit-rollback-execution-approval-mode rollback-candidate-to-operator-rollback-execution-decision `
  --operator-rollback-execution-decision approved `
  --expected-current-active-learning-route atlas-grouped-sequential-integration-candidate `
  --expected-rollback-target-active-learning-route freshinit-burn-native-tiny-proof `
  --rollback-candidate-scope active-learning-route-pointer-only `
  --rollback-candidate-authority preflight-only `
  --route-pointer-observation-scope active-learning-only `
  --route-pointer-write-mode observe-only `
  --rollback-execution-mode forbid `
  --default-route-pointer-write-mode forbid `
  --production-route-pointer-write-mode forbid `
  --production-claim-mode forbid `
  --runtime-training-mode forbid `
  --optimizer-step-mode forbid `
  --checkpoint-write-mode forbid `
  --safetensors-write-mode forbid `
  --training-quality-claim-mode forbid `
  --optimizer-quality-claim-mode forbid `
  --model-improvement-claim-mode forbid `
  --training-completion-mode hold `
  --deployment-ready-mode hold
```

Denied path:

```powershell
--operator-rollback-execution-decision denied
```

## Output artifacts

```text
ASH_BASETRAIN_GPU_70K_G190D_EXPLICIT_ROLLBACK_EXECUTION_APPROVAL_GATE_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G190D_G189D_ROLLBACK_CANDIDATE_SOURCE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G190D_ROLLBACK_EXECUTION_DECISION_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G190D_ROLLBACK_EXECUTION_DECISION_PACKET.json
ASH_BASETRAIN_GPU_70K_G190D_CURRENT_ACTIVE_ROUTE_OBSERVATION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G190D_ROLLBACK_CANDIDATE_AUTHORITY_AUDIT.json
ASH_BASETRAIN_GPU_70K_G190D_NO_ROUTE_POINTER_REWRITE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G190D_NO_PRODUCTION_CLAIM_AUDIT.json
ASH_BASETRAIN_GPU_70K_G190D_NO_TRAINING_OR_WEIGHT_MUTATION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G190D_NEXT_PATCH_PACKET.json
```

Expected output count: `output_files_written=10`

## Next patch

Approved path:

```text
ASH-BASETRAIN-GPU-70K-G191D
Rollback Pointer Update Execution Gate /
Approved Rollback Execution Decision To Active Learning Route Pointer Restore /
No Production Claim
```

Denied path:

```text
ASH-BASETRAIN-GPU-70K-G191H
Rollback Execution Denial Hold State Audit /
Denied Rollback Execution Decision To Rollback Hold Ledger /
No Rollback Execution No Production Claim
```
