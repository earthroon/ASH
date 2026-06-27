# ASH-BASETRAIN-GPU-70K-G209T7

## Candidate Decision Branch Router And No Auto Apply Guard / Route Accept Hold Reject Receipt / No Replacement

PatchId: `ASH-BASETRAIN-GPU-70K-G209T7`  
SourcePatchId: `ASH-BASETRAIN-GPU-70K-G209T6`  
NextPatchId: `ASH-BASETRAIN-GPU-70K-G209T8`  
Phase: `PhaseT`  
RuntimePassTarget: `PASS_ASH_BASETRAIN_GPU_70K_G209T7_CANDIDATE_DECISION_BRANCH_ROUTER_AND_NO_AUTO_APPLY_GUARD_ROUTE_ACCEPT_HOLD_REJECT_RECEIPT_NO_REPLACEMENT`

## Purpose

G209T7 consumes the G209T6 sealed operator decision receipt and decision seal ledger. It does not accept a new operator decision. It reads the already sealed decision and routes it to one of three branch surfaces.

Current source decision:

```text
operator_decision_status=HoldCandidate
```

Therefore this patch creates the hold branch selection and hold pending review state while preserving all no-apply and no-replacement guards.

Allowed outputs:

```text
candidate_decision_branch_router_created=true
accept_candidate_branch_created=true
hold_candidate_branch_created=true
reject_candidate_branch_created=true
selected_branch_ledger_created=true
hold_candidate_branch_selected=true
hold_candidate_pending_review_state_created=true
no_auto_apply_guard_created=true
no_replacement_route_guard_created=true
```

Forbidden states:

```text
operator_decision_reinput_allowed=true
operator_decision_application_executed=true
auto_apply_enabled=true
auto_promotion_enabled=true
candidate_promoted=true
candidate_promotion_permission_granted=true
replacement_permission_granted=true
tensorcube_matmul_replacement_enabled=true
tensorcore_route_enabled=true
tensorcore_hardware_acceleration_claimed=true
benchmark_claimed=true
model_improvement_claimed=true
deployment_ready_claimed=true
deployment_claimed=true
```

## CLI

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g209t7_candidate_decision_branch_router -- `
  --local-root . `
  --out-dir artifacts `
  --source-patch-id ASH-BASETRAIN-GPU-70K-G209T6 `
  --phase phase-t `
  --active-route freshinit `
  --training-rs-route-mode required `
  --source-operator-explicit-decision-receipt-mode required `
  --source-operator-decision-seal-ledger-mode required `
  --source-explicit-decision-input-validation-audit-mode required `
  --source-no-replacement-apply-gate-mode required `
  --source-decision-apply-deferred-audit-mode required `
  --source-no-auto-promotion-audit-mode required `
  --source-no-candidate-promotion-audit-mode required `
  --source-no-replacement-permission-audit-mode required `
  --source-no-matmul-replacement-audit-mode required `
  --source-no-tensorcore-route-enable-audit-mode required `
  --source-no-tensorcore-hardware-claim-audit-mode required `
  --release-candidate-id RC-1 `
  --release-candidate-source frozen-production-pointer-state `
  --release-candidate-target staged-candidate `
  --eval-matrix-id rc1-ko-short-matrix-v1 `
  --baseline-reference-id ko-short-reference-v1 `
  --parity-baseline-source rc1 `
  --parity-baseline-scope frozen-production-pointer-state `
  --parity-tolerance-id rc1-tensor-shadow-v1 `
  --repeatability-matrix-id rc1-tensor-shadow-repeat-v1 `
  --candidate-promotion-precheck-status review-ready `
  --operator-decision-receipt-id operator-explicit-decision-receipt-v1 `
  --operator-decision-status hold-candidate `
  --operator-decision-status-allowed-values accept-candidate,hold-candidate,reject-candidate `
  --operator-decision-status-source sealed-receipt `
  --operator-decision-reinput-mode forbid `
  --candidate-decision-branch-router-mode create `
  --candidate-decision-branch-router-id candidate-decision-branch-router-v1 `
  --branch-routing-mode strict `
  --branch-routing-source operator-explicit-decision-receipt-v1 `
  --accept-candidate-branch-mode create `
  --hold-candidate-branch-mode create `
  --reject-candidate-branch-mode create `
  --selected-branch-ledger-mode create `
  --selected-branch-expected hold-candidate `
  --hold-candidate-pending-review-state-mode create `
  --accept-candidate-promotion-preflight-mode forbid `
  --reject-candidate-terminal-apply-mode forbid `
  --operator-decision-application-mode forbid `
  --decision-apply-deferred-mode required `
  --no-auto-apply-guard-mode create `
  --no-auto-apply-guard-id no-auto-apply-guard-v1 `
  --no-replacement-route-guard-mode create `
  --no-replacement-route-guard-id no-replacement-route-guard-v1 `
  --auto-apply-mode forbid `
  --auto-promotion-mode forbid `
  --candidate-promotion-permission-mode forbid `
  --candidate-promote-mode forbid `
  --replacement-permission-mode forbid `
  --fallback-route-preservation-mode required `
  --fallback-route-target normal-freshinit-route `
  --fallback-required-before-replacement-mode required `
  --tensorcube-shadow-route-mode shadow-only `
  --tensorcube-8x8-shadow-mode enabled `
  --tensorcube-kernel-family internal-tensorcube-8x8 `
  --tensorcube-matmul-replacement-mode forbid `
  --tensorcube-production-replacement-mode forbid `
  --tensorcore-probe-receipt-mode preserve `
  --tensorcore-backend-status-mode observe-only `
  --tensorcore-route-enable-mode forbid `
  --tensorcore-hardware-claim-mode forbid `
  --matmul-replacement-mode forbid `
  --production-pointer-remain-switched-mode required `
  --production-route-pointer-switch-mode forbid `
  --rollback-execution-mode forbid `
  --checkpoint-write-mode forbid `
  --safetensors-write-mode forbid `
  --base-weight-mutation-mode forbid `
  --optimizer-state-mutation-mode forbid `
  --training-weight-mutation-mode forbid `
  --artifact-retention-mode enable `
  --no-artifacts-mode forbid `
  --cuda-dependency-mode forbid `
  --torch-dependency-mode forbid `
  --training-quality-claim-mode forbid `
  --model-improvement-claim-mode forbid `
  --production-quality-claim-mode forbid `
  --benchmark-claim-mode forbid `
  --convergence-claim-mode forbid `
  --deployment-ready-mode forbid `
  --deployment-claim-mode forbid `
  --next-patch ASH-BASETRAIN-GPU-70K-G209T8
```

## Runtime Output Artifacts

These artifacts are written locally by the Rust binary and must not be pre-baked into the ZIP.

```text
ASH_BASETRAIN_GPU_70K_G209T7_CANDIDATE_DECISION_BRANCH_ROUTER_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G209T7_G209T6_SOURCE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T7_OPERATOR_EXPLICIT_DECISION_RECEIPT_LOAD_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T7_OPERATOR_DECISION_SEAL_LEDGER_LOAD_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T7_EXPLICIT_DECISION_INPUT_VALIDATION_LOAD_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T7_NO_REPLACEMENT_APPLY_GATE_LOAD_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T7_DECISION_APPLY_DEFERRED_LOAD_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T7_CANDIDATE_DECISION_BRANCH_ROUTER.json
ASH_BASETRAIN_GPU_70K_G209T7_ACCEPT_CANDIDATE_BRANCH_SURFACE.json
ASH_BASETRAIN_GPU_70K_G209T7_HOLD_CANDIDATE_BRANCH_SURFACE.json
ASH_BASETRAIN_GPU_70K_G209T7_REJECT_CANDIDATE_BRANCH_SURFACE.json
ASH_BASETRAIN_GPU_70K_G209T7_SELECTED_BRANCH_LEDGER.json
ASH_BASETRAIN_GPU_70K_G209T7_HOLD_CANDIDATE_PENDING_REVIEW_STATE.json
ASH_BASETRAIN_GPU_70K_G209T7_NO_AUTO_APPLY_GUARD.json
ASH_BASETRAIN_GPU_70K_G209T7_NO_REPLACEMENT_ROUTE_GUARD.json
ASH_BASETRAIN_GPU_70K_G209T7_NO_AUTO_PROMOTION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T7_NO_CANDIDATE_PROMOTION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T7_NO_REPLACEMENT_PERMISSION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T7_NO_MATMUL_REPLACEMENT_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T7_NO_TENSORCORE_ROUTE_ENABLE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T7_NO_TENSORCORE_HARDWARE_CLAIM_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T7_NO_CUDA_DEPENDENCY_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T7_NO_TORCH_DEPENDENCY_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T7_NO_CHECKPOINT_REWRITE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T7_NO_SAFETENSORS_REWRITE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T7_NO_BASE_WEIGHT_MUTATION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T7_NO_OPTIMIZER_STATE_MUTATION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T7_NO_TRAINING_WEIGHT_MUTATION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T7_NO_MODEL_IMPROVEMENT_CLAIM_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T7_NO_BENCHMARK_CLAIM_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T7_NO_DEPLOYMENT_CLAIM_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T7_NEXT_G209T8_ENTRY_PACKET.json
```

## Branch Routing Rule

```text
operator_decision_status is read from sealed receipt.
operator_decision_reinput_mode must be forbid.
operator_decision_status must be hold-candidate for the current chain.
selected_branch_expected must be hold-candidate.
HoldCandidate routes to HoldCandidatePendingReview.
No branch may execute apply, promotion, replacement, rollback, checkpoint rewrite, or production pointer switch in G209T7.
```

## Expected PASS Summary

```text
previous_g209t6_accepted=true
source_patch_id=ASH-BASETRAIN-GPU-70K-G209T6
phase=PhaseT
training_loop_owner=training.rs
active_training_route=FreshInit
source_operator_explicit_decision_receipt_loaded=true
source_operator_decision_seal_ledger_loaded=true
source_explicit_decision_input_validation_audit_loaded=true
source_no_replacement_apply_gate_loaded=true
source_decision_apply_deferred_audit_loaded=true
operator_decision_receipt_id=operator-explicit-decision-receipt-v1
operator_decision_status=HoldCandidate
operator_decision_status_source=SealedReceipt
operator_decision_reinput_allowed=false
candidate_decision_branch_router_created=true
candidate_decision_branch_router_id=candidate-decision-branch-router-v1
accept_candidate_branch_created=true
hold_candidate_branch_created=true
reject_candidate_branch_created=true
selected_branch_ledger_created=true
accept_candidate_branch_selected=false
hold_candidate_branch_selected=true
reject_candidate_branch_selected=false
hold_candidate_pending_review_state_created=true
auto_apply_enabled=false
auto_promotion_enabled=false
operator_decision_application_executed=false
decision_apply_deferred=true
candidate_promoted=false
replacement_permission_granted=false
tensorcube_matmul_replacement_enabled=false
tensorcore_route_enabled=false
tensorcore_hardware_acceleration_claimed=false
ready_for_g209t8=true
```

## Acceptance Criteria

PASS iff G209T6 sealed decision receipt is consumed, the decision status is read as `HoldCandidate`, decision re-input is forbidden, branch router and all branch surfaces are created, exactly the hold branch is selected, hold candidate pending review state is created, operator decision application is not executed, decision apply remains deferred, no auto-apply/no-replacement guards are created, candidate is not promoted, replacement permission remains false, TensorCube remains shadow-only, TensorCore remains observe-only, no CUDA/torch dependency is required, no checkpoint/safetensors/base/optimizer/training mutation occurs, and no benchmark/model-improvement/deployment claim occurs.

## Next Patch

`ASH-BASETRAIN-GPU-70K-G209T8`

Expected next title:

```text
Hold Candidate Pending Review Receipt And Reopen Decision Gate / Preserve TensorCube Shadow Candidate / No Replacement
```
