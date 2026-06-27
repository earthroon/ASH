# ASH-BASETRAIN-GPU-70K-G207A12

## Operator Approved Staged Candidate Promotion / Commit Candidate Route Pointer To Staging / No Production Route Pointer Switch

PatchId: `ASH-BASETRAIN-GPU-70K-G207A12`  
SourcePatchId: `ASH-BASETRAIN-GPU-70K-G207A11`  
NextPatchId: `ASH-BASETRAIN-GPU-70K-G207A13`  
RuntimePassTarget: `PASS_ASH_BASETRAIN_GPU_70K_G207A12_OPERATOR_APPROVED_STAGED_CANDIDATE_PROMOTION_COMMIT_CANDIDATE_ROUTE_POINTER_TO_STAGING_NO_PRODUCTION_ROUTE_POINTER_SWITCH`

## Purpose

G207A12 consumes the G207A11 promotion precheck receipt and performs the first real state-changing promotion step: commit candidate route pointer to staging.

This patch may mutate staging candidate pointer state only. It must not mutate production route pointer, production checkpoint, production safetensors, or production base weights.

A12 is an operator-approved staged candidate promotion patch. It is not a production switch patch.

## Runtime Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g207a12_staged_candidate_promotion -- `
  --local-root . `
  --out-dir artifacts `
  --source-patch-id ASH-BASETRAIN-GPU-70K-G207A11 `
  --phase phase-a `
  --active-route freshinit `
  --training-rs-route-mode required `
  --source-promotion-precheck-mode required `
  --source-candidate-artifact-diff-mode required `
  --source-candidate-route-pointer-plan-mode required `
  --source-production-apply-mode forbid `
  --operator-approval-mode explicit `
  --operator-approval-token APPROVE_STAGED_CANDIDATE_PROMOTION_G207A12 `
  --promotion-scope staging-only `
  --staged-promotion-mode commit-staging-pointer `
  --candidate-route-pointer-source scoped-candidate-artifact `
  --candidate-route-pointer-target staging `
  --staging-route-pointer-commit-mode allow `
  --staging-rollback-receipt-mode create `
  --staging-pointer-integrity-mode strict `
  --production-route-pointer-switch-mode forbid `
  --production-route-pointer-commit-mode forbid `
  --production-apply-mode forbid `
  --production-commit-mode forbid `
  --checkpoint-write-mode forbid `
  --safetensors-write-mode forbid `
  --base-weight-mutation-mode forbid `
  --promotion-verdict-mode strict `
  --artifact-retention-mode enable `
  --no-artifacts-mode forbid `
  --atlas-route-mode defer `
  --tensorcube-mode keep-disabled `
  --training-quality-claim-mode forbid `
  --model-improvement-claim-mode forbid `
  --deployment-ready-mode forbid `
  --next-patch ASH-BASETRAIN-GPU-70K-G207A13
```

## Output Artifacts Written By Rust

```text
ASH_BASETRAIN_GPU_70K_G207A12_STAGED_CANDIDATE_PROMOTION_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G207A12_G207A11_SOURCE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A12_OPERATOR_APPROVAL_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G207A12_STAGED_PROMOTION_POLICY.json
ASH_BASETRAIN_GPU_70K_G207A12_STAGING_ROUTE_POINTER.json
ASH_BASETRAIN_GPU_70K_G207A12_STAGING_ROUTE_POINTER_COMMIT_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G207A12_STAGING_POINTER_INTEGRITY_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A12_STAGING_ROLLBACK_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G207A12_NO_PRODUCTION_ROUTE_POINTER_SWITCH_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A12_NO_PRODUCTION_APPLY_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A12_NO_CHECKPOINT_REWRITE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A12_NO_SAFETENSORS_REWRITE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A12_NO_BASE_WEIGHT_MUTATION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A12_NO_QUALITY_CLAIM_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A12_ATLAS_DEFERRED_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A12_TENSORCUBE_DISABLED_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A12_NEXT_G207A13_ENTRY_PACKET.json
```

These artifacts must be generated locally by the Rust binary and must not be pre-baked into the ZIP.

## Staged Promotion Rule

```text
staged_candidate_promotion_allowed iff:

source_patch_id == ASH-BASETRAIN-GPU-70K-G207A11
AND source_promotion_precheck_passed == true
AND source_candidate_artifact_validated == true
AND source_candidate_route_pointer_plan_revalidated == true
AND operator_approval_mode == explicit
AND operator_approval_token == APPROVE_STAGED_CANDIDATE_PROMOTION_G207A12
AND promotion_scope == staging-only
AND staged_promotion_mode == commit-staging-pointer
AND candidate_route_pointer_target == staging
AND staging_route_pointer_commit_mode == allow
AND production_route_pointer_switch_mode == forbid
AND production_route_pointer_commit_mode == forbid
AND production_apply_mode == forbid
AND checkpoint_write_mode == forbid
AND safetensors_write_mode == forbid
AND base_weight_mutation_mode == forbid
```

## Expected PASS Summary

```text
previous_g207a11_accepted=true
source_patch_id=ASH-BASETRAIN-GPU-70K-G207A11
phase=PhaseA
training_loop_owner=training.rs
active_training_route=FreshInit
operator_approval_required=true
operator_approval_token_received=true
operator_approval_receipt_created=true
operator_approval_gate_passed=true
promotion_blocked_without_operator_approval=true
promotion_scope=StagingOnly
staged_promotion_mode=CommitStagingPointer
staged_candidate_promotion_executed=true
staged_candidate_promotion_receipt_created=true
candidate_route_pointer_source=ScopedCandidateArtifact
candidate_route_pointer_target=Staging
candidate_route_pointer_committed_to_staging=true
staging_route_pointer_commit_executed=true
staging_route_pointer_commit_receipt_created=true
staging_pointer_created=true
staging_pointer_owner=training.rs
staging_pointer_phase=PhaseA
staging_pointer_route=FreshInit
staging_pointer_scope=Staging
staging_pointer_points_to_candidate_artifact=true
staging_pointer_is_production=false
staging_pointer_integrity_checked=true
staging_pointer_integrity_passed=true
staging_rollback_receipt_created=true
staging_previous_pointer_captured=true
staging_rollback_target_recorded=true
rollback_path_available=true
rollback_executed=false
production_route_pointer_switch_executed=false
production_route_pointer_committed=false
production_route_pointer_rewritten=false
production_apply_executed=false
production_commit_executed=false
production_base_weight_mutated=false
checkpoint_rewritten=false
safetensors_rewritten=false
training_quality_claimed=false
model_improvement_claimed=false
production_claimed=false
deployment_ready_claimed=false
atlas_route_executed=false
atlas_grouped_route_deferred=true
tensorcube_8x8_kept_disabled=true
tensorcube_matmul_replacement_enabled=false
ready_for_g207a13=true
```

## Failure Conditions

```text
source_patch_id != ASH-BASETRAIN-GPU-70K-G207A11
phase != phase-a
active_route != freshinit
training_rs_route_mode != required
source_promotion_precheck_mode != required
source_candidate_artifact_diff_mode != required
source_candidate_route_pointer_plan_mode != required
source_production_apply_mode != forbid
operator_approval_mode != explicit
operator_approval_token != APPROVE_STAGED_CANDIDATE_PROMOTION_G207A12
promotion_scope != staging-only
staged_promotion_mode != commit-staging-pointer
candidate_route_pointer_source != scoped-candidate-artifact
candidate_route_pointer_target != staging
staging_route_pointer_commit_mode != allow
staging_rollback_receipt_mode != create
staging_pointer_integrity_mode != strict
production_route_pointer_switch_mode != forbid
production_route_pointer_commit_mode != forbid
production_apply_mode != forbid
production_commit_mode != forbid
checkpoint_write_mode != forbid
safetensors_write_mode != forbid
base_weight_mutation_mode != forbid
promotion_verdict_mode != strict
artifact_retention_mode != enable
no_artifacts_mode != forbid
atlas_route_mode != defer
tensorcube_mode != keep-disabled
training_quality_claim_mode != forbid
model_improvement_claim_mode != forbid
deployment_ready_mode != forbid
next_patch != ASH-BASETRAIN-GPU-70K-G207A13
```

Forbidden states:

```text
operator_approval_required=false
operator_approval_token_received=false
operator_approval_gate_passed=false
promotion_blocked_without_operator_approval=false
staged_candidate_promotion_executed=false
candidate_route_pointer_committed_to_staging=false
staging_route_pointer_commit_executed=false
staging_pointer_created=false
staging_pointer_is_production=true
staging_pointer_integrity_passed=false
staging_rollback_receipt_created=false
production_route_pointer_switch_executed=true
production_route_pointer_committed=true
production_route_pointer_rewritten=true
production_apply_executed=true
production_commit_executed=true
production_base_weight_mutated=true
checkpoint_rewritten=true
safetensors_rewritten=true
training_quality_claimed=true
model_improvement_claimed=true
production_claimed=true
deployment_ready_claimed=true
atlas_route_executed=true
tensorcube_matmul_replacement_enabled=true
```

## Acceptance Criteria

```text
PASS iff:

1. G207A11 source state is consumed.
2. training loop owner remains training.rs.
3. active route remains FreshInit.
4. operator approval is explicitly required.
5. operator approval token is received.
6. operator approval receipt is created.
7. operator approval gate passes.
8. promotion is blocked without operator approval.
9. promotion scope is StagingOnly.
10. staged promotion mode is CommitStagingPointer.
11. candidate route pointer source is scoped candidate artifact.
12. candidate route pointer target is staging.
13. candidate route pointer is committed to staging.
14. staging route pointer commit receipt is created.
15. staging pointer is created.
16. staging pointer is non-production.
17. staging pointer points to candidate artifact.
18. staging pointer integrity check passes.
19. staging rollback receipt is created.
20. previous staging pointer is captured.
21. rollback path is available but not executed.
22. production route pointer switch does not execute.
23. production route pointer is not committed.
24. production route pointer is not rewritten.
25. production apply does not execute.
26. production commit does not execute.
27. production base weights are not mutated.
28. checkpoint is not rewritten.
29. safetensors are not rewritten.
30. no training quality, model improvement, production, or deployment claim occurs.
31. Atlas remains deferred.
32. TensorCube 8x8 remains disabled.
33. G207A13 entry packet is created.
```

## Implementation Notes

- Implement as an operator-approved staged candidate promotion.
- This patch performs a real staging pointer commit.
- This patch does not perform production pointer switch.
- This patch does not perform production apply.
- It must consume or validate the G207A11 promotion precheck receipt.
- It must require explicit operator approval.
- Missing operator approval must block promotion.
- The candidate route pointer may be committed only to staging.
- The staging pointer must be marked non-production.
- A staging rollback receipt must be created.
- Rollback path may be recorded, but rollback execution remains false.
- Production route pointer switch must remain forbidden.
- Production checkpoint and safetensors must not be rewritten.
- Production base weights must not be mutated.
- Use explicit JSON atlas writer for large receipts.
- Do not use large serde JSON macro objects.
- Do not add recursion limit workarounds.
- Do not execute Atlas.
- Do not enable TensorCube 8x8.
- Invalid CLI enum values must fail closed.

## Next Patch

`ASH-BASETRAIN-GPU-70K-G207A13` should load the staging route pointer committed by A12, load the staged candidate artifact, run a runtime smoke against staging only, validate the staging rollback path without executing rollback, and preserve the prohibition against production route pointer switch, checkpoint rewrite, safetensors rewrite, Atlas execution, TensorCube enablement, and quality claims.
