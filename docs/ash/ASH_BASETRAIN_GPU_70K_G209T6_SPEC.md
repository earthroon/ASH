# ASH-BASETRAIN-GPU-70K-G209T6

## Operator Explicit Candidate Decision Receipt And No Replacement Apply Gate / Seal Accept Hold Reject Input / No TensorCube Replacement

PatchId: `ASH-BASETRAIN-GPU-70K-G209T6`  
SourcePatchId: `ASH-BASETRAIN-GPU-70K-G209T5`  
NextPatchId: `ASH-BASETRAIN-GPU-70K-G209T7`  
Phase: `PhaseT`  
RuntimePassTarget: `PASS_ASH_BASETRAIN_GPU_70K_G209T6_OPERATOR_EXPLICIT_CANDIDATE_DECISION_RECEIPT_AND_NO_REPLACEMENT_APPLY_GATE_SEAL_ACCEPT_HOLD_REJECT_INPUT_NO_TENSORCUBE_REPLACEMENT`

## Purpose

G209T6 consumes the G209T5 operator candidate review queue, operator review option set, operator decision receipt surface, and no replacement decision gate. It accepts exactly one explicit operator decision input and seals that input into an operator decision receipt.

Allowed decision inputs:

```text
accept-candidate
hold-candidate
reject-candidate
```

This patch records the operator decision receipt only. It does not apply the decision, promote TensorCube, grant replacement permission, switch production route pointers, enable TensorCore, or claim benchmark/model/deployment improvement.

Allowed outputs:

```text
operator_explicit_decision_input_accepted=true
operator_decision_status=AcceptCandidate|HoldCandidate|RejectCandidate
operator_decision_receipt_created=true
operator_decision_sealed=true
operator_decision_application_executed=false
decision_apply_deferred=true
no_replacement_apply_gate_created=true
```

Forbidden states:

```text
operator_decision_application_executed=true
candidate_promoted=true
candidate_promotion_permission_granted=true
replacement_permission_granted=true
replacement_allowed=true
tensorcube_matmul_replacement_enabled=true
tensorcube_production_replacement_enabled=true
tensorcore_route_enabled=true
tensorcore_hardware_acceleration_claimed=true
matmul_replacement_enabled=true
production_route_pointer_switch_executed=true
benchmark_claimed=true
model_improvement_claimed=true
deployment_ready_claimed=true
deployment_claimed=true
```

## CLI

The example below uses `hold-candidate`. Replace it with `accept-candidate` or `reject-candidate` only when that is the explicit operator decision.

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g209t6_operator_explicit_candidate_decision_receipt -- `
  --local-root . `
  --out-dir artifacts `
  --source-patch-id ASH-BASETRAIN-GPU-70K-G209T5 `
  --phase phase-t `
  --active-route freshinit `
  --training-rs-route-mode required `
  --source-operator-candidate-review-queue-mode required `
  --source-operator-review-option-set-mode required `
  --source-operator-decision-receipt-surface-mode required `
  --source-no-replacement-decision-gate-mode required `
  --source-review-queue-status-ledger-mode required `
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
  --operator-candidate-review-queue-id operator-candidate-review-queue-v1 `
  --operator-review-queue-status open `
  --operator-review-option-set-id candidate-decision-options-v1 `
  --operator-decision-allowed-values accept-candidate,hold-candidate,reject-candidate `
  --operator-explicit-decision-input hold-candidate `
  --operator-decision-input-mode required `
  --operator-decision-validation-mode strict `
  --operator-decision-receipt-mode create `
  --operator-decision-receipt-id operator-explicit-decision-receipt-v1 `
  --operator-decision-seal-mode create `
  --operator-decision-application-mode forbid `
  --decision-apply-deferred-mode required `
  --no-replacement-apply-gate-mode create `
  --no-replacement-apply-gate-id no-replacement-apply-gate-v1 `
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
  --next-patch ASH-BASETRAIN-GPU-70K-G209T7
```

## Runtime Output Artifacts

These artifacts are written locally by the Rust binary and must not be pre-baked into the ZIP.

```text
ASH_BASETRAIN_GPU_70K_G209T6_OPERATOR_EXPLICIT_DECISION_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G209T6_G209T5_SOURCE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T6_OPERATOR_REVIEW_QUEUE_LOAD_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T6_OPERATOR_REVIEW_OPTION_SET_LOAD_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T6_OPERATOR_DECISION_RECEIPT_SURFACE_LOAD_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T6_NO_REPLACEMENT_DECISION_GATE_LOAD_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T6_EXPLICIT_DECISION_INPUT_VALIDATION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T6_OPERATOR_DECISION_SEAL_LEDGER.json
ASH_BASETRAIN_GPU_70K_G209T6_NO_REPLACEMENT_APPLY_GATE.json
ASH_BASETRAIN_GPU_70K_G209T6_DECISION_APPLY_DEFERRED_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T6_NO_AUTO_PROMOTION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T6_NO_CANDIDATE_PROMOTION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T6_NO_REPLACEMENT_PERMISSION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T6_NO_MATMUL_REPLACEMENT_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T6_NO_TENSORCORE_ROUTE_ENABLE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T6_NO_TENSORCORE_HARDWARE_CLAIM_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T6_NO_CUDA_DEPENDENCY_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T6_NO_TORCH_DEPENDENCY_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T6_NO_CHECKPOINT_REWRITE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T6_NO_SAFETENSORS_REWRITE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T6_NO_BASE_WEIGHT_MUTATION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T6_NO_OPTIMIZER_STATE_MUTATION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T6_NO_TRAINING_WEIGHT_MUTATION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T6_NO_MODEL_IMPROVEMENT_CLAIM_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T6_NO_BENCHMARK_CLAIM_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T6_NO_DEPLOYMENT_CLAIM_AUDIT.json
ASH_BASETRAIN_GPU_70K_G209T6_NEXT_G209T7_ENTRY_PACKET.json
```

## Explicit Decision Receipt Rule

```text
operator_explicit_decision_receipt_allowed iff:
source_patch_id == ASH-BASETRAIN-GPU-70K-G209T5
AND phase == phase-t
AND active_route == freshinit
AND source_operator_candidate_review_queue_mode == required
AND source_operator_review_option_set_mode == required
AND source_operator_decision_receipt_surface_mode == required
AND source_no_replacement_decision_gate_mode == required
AND source_no_auto_promotion_audit_mode == required
AND source_no_candidate_promotion_audit_mode == required
AND source_no_replacement_permission_audit_mode == required
AND source_no_matmul_replacement_audit_mode == required
AND source_no_tensorcore_route_enable_audit_mode == required
AND source_no_tensorcore_hardware_claim_audit_mode == required
AND parity_tolerance_id == rc1-tensor-shadow-v1
AND repeatability_matrix_id == rc1-tensor-shadow-repeat-v1
AND operator_explicit_decision_input IN [accept-candidate, hold-candidate, reject-candidate]
AND operator_decision_receipt_mode == create
AND operator_decision_seal_mode == create
AND operator_decision_application_mode == forbid
AND decision_apply_deferred_mode == required
AND no_replacement_apply_gate_mode == create
AND auto_promotion_mode == forbid
AND candidate_promotion_permission_mode == forbid
AND candidate_promote_mode == forbid
AND replacement_permission_mode == forbid
AND tensorcube_matmul_replacement_mode == forbid
AND tensorcore_route_enable_mode == forbid
AND tensorcore_hardware_claim_mode == forbid
AND benchmark_claim_mode == forbid
AND deployment_claim_mode == forbid
```

## Expected PASS Summary

```text
previous_g209t5_accepted=true
source_patch_id=ASH-BASETRAIN-GPU-70K-G209T5
phase=PhaseT
training_loop_owner=training.rs
active_training_route=FreshInit
source_operator_candidate_review_queue_loaded=true
source_operator_review_option_set_loaded=true
source_operator_decision_receipt_surface_loaded=true
source_no_replacement_decision_gate_loaded=true
source_no_auto_promotion_audit_loaded=true
source_no_candidate_promotion_audit_loaded=true
source_no_replacement_permission_audit_loaded=true
source_no_matmul_replacement_audit_loaded=true
source_no_tensorcore_route_enable_audit_loaded=true
source_no_tensorcore_hardware_claim_audit_loaded=true
release_candidate_id=RC-1
parity_tolerance_id=rc1-tensor-shadow-v1
repeatability_matrix_id=rc1-tensor-shadow-repeat-v1
operator_explicit_decision_input_accepted=true
operator_decision_status=AcceptCandidate|HoldCandidate|RejectCandidate
operator_decision_receipt_created=true
operator_decision_sealed=true
operator_decision_application_executed=false
decision_apply_deferred=true
no_replacement_apply_gate_created=true
auto_promotion_enabled=false
candidate_promoted=false
candidate_promotion_permission_granted=false
replacement_permission_granted=false
replacement_allowed=false
fallback_route_preserved=true
tensorcube_shadow_route_mode=ShadowOnly
tensorcube_8x8_shadow_enabled=true
tensorcube_matmul_replacement_enabled=false
tensorcore_route_enabled=false
tensorcore_hardware_acceleration_claimed=false
cuda_dependency_required=false
torch_dependency_required=false
checkpoint_rewritten=false
safetensors_rewritten=false
production_base_weight_mutated=false
optimizer_state_mutated=false
training_weight_mutated=false
benchmark_claimed=false
model_improvement_claimed=false
deployment_ready_claimed=false
deployment_claimed=false
ready_for_g209t7=true
```

## Acceptance Criteria

PASS iff G209T5 source state is consumed, operator review queue and option set are loaded, an explicit operator decision input is provided, the input is one of `accept-candidate`, `hold-candidate`, or `reject-candidate`, the operator decision receipt is created and sealed, decision application is not executed, decision apply is deferred, no replacement apply gate is created, auto-promotion remains false, candidate is not promoted, replacement permission remains false, fallback route is preserved, TensorCube remains shadow-only, TensorCore remains observe-only, no CUDA/torch dependency is required, no checkpoint/safetensors/base/optimizer/training mutation occurs, and no benchmark/model-improvement/deployment claim occurs.

## Next Patch

`ASH-BASETRAIN-GPU-70K-G209T7`

Expected next title:

```text
Candidate Decision Branch Router And No Auto Apply Guard / Route Accept Hold Reject Receipt / No Replacement
```
