# ASH-BASETRAIN-GPU-70K-G207A10

## Candidate Apply Dry Run With Scoped Candidate Artifact / No Production Route Pointer Commit / No Quality Claim

PatchId: `ASH-BASETRAIN-GPU-70K-G207A10`  
SourcePatchId: `ASH-BASETRAIN-GPU-70K-G207A9`  
NextPatchId: `ASH-BASETRAIN-GPU-70K-G207A11`  
RuntimePassTarget: `PASS_ASH_BASETRAIN_GPU_70K_G207A10_CANDIDATE_APPLY_DRY_RUN_WITH_SCOPED_CANDIDATE_ARTIFACT_NO_PRODUCTION_ROUTE_POINTER_COMMIT_NO_QUALITY_CLAIM`

## Purpose

G207A10 consumes the G207A9 candidate apply boundary binding receipt and performs a candidate apply dry-run against a scoped candidate artifact.

G207A9 proved that the candidate apply boundary was declared, the diff gate was bound to the boundary, A8 regression matrix pass is required before apply, invalid A8 states are blocked, the positive preflight path opens, negative boundary paths are blocked, and production commit remains forbidden.

G207A10 may create and validate a candidate-local artifact. It must not commit production apply, rewrite production checkpoint, rewrite production safetensors, rewrite production route pointer, mutate production base weights, claim training quality, claim model improvement, or claim deployment readiness.

A10 is a scoped candidate dry-run patch. It is not a production apply patch.

## Runtime Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g207a10_candidate_apply_dry_run -- `
  --local-root . `
  --out-dir artifacts `
  --source-patch-id ASH-BASETRAIN-GPU-70K-G207A9 `
  --phase phase-a `
  --active-route freshinit `
  --training-rs-route-required true `
  --source-candidate-apply-boundary-required true `
  --source-diff-gate-boundary-required true `
  --source-a8-regression-matrix-required true `
  --source-apply-boundary-validation-required true `
  --source-positive-boundary-path-required true `
  --source-negative-boundary-paths-required true `
  --candidate-apply-mode dry-run `
  --candidate-artifact-scope scoped `
  --candidate-artifact-write-mode allow `
  --candidate-artifact-kind dry-run-receipt `
  --candidate-route-pointer-plan-mode create-plan-only `
  --candidate-route-pointer-commit-mode forbid `
  --production-route-pointer-commit-mode forbid `
  --production-commit-mode forbid `
  --checkpoint-write-mode forbid `
  --safetensors-write-mode forbid `
  --base-weight-mutation-mode forbid `
  --dry-run-verdict-mode strict `
  --artifact-retention-mode enable `
  --no-artifacts-mode forbid `
  --atlas-route-mode defer `
  --tensorcube-mode keep-disabled `
  --training-quality-claim-mode forbid `
  --model-improvement-claim-mode forbid `
  --deployment-ready-mode forbid `
  --next-patch ASH-BASETRAIN-GPU-70K-G207A11
```

## Output Artifacts Written By Rust

```text
ASH_BASETRAIN_GPU_70K_G207A10_CANDIDATE_APPLY_DRY_RUN_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G207A10_G207A9_SOURCE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A10_BOUNDARY_GATE_LOAD_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A10_SCOPED_CANDIDATE_ARTIFACT.json
ASH_BASETRAIN_GPU_70K_G207A10_SCOPED_CANDIDATE_ARTIFACT_MANIFEST.json
ASH_BASETRAIN_GPU_70K_G207A10_CANDIDATE_ARTIFACT_VALIDATION.json
ASH_BASETRAIN_GPU_70K_G207A10_CANDIDATE_ROUTE_POINTER_PLAN.json
ASH_BASETRAIN_GPU_70K_G207A10_CANDIDATE_ROUTE_POINTER_PLAN_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A10_NO_PRODUCTION_ROUTE_POINTER_COMMIT_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A10_NO_PRODUCTION_COMMIT_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A10_NO_BASE_WEIGHT_MUTATION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A10_NO_CHECKPOINT_REWRITE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A10_NO_SAFETENSORS_REWRITE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A10_NO_QUALITY_CLAIM_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A10_ATLAS_DEFERRED_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A10_TENSORCUBE_DISABLED_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A10_NEXT_G207A11_ENTRY_PACKET.json
```

These artifacts must be generated locally by the Rust binary and must not be pre-baked into the ZIP.

## Candidate Dry-Run Rule

```text
candidate_apply_dry_run_allowed iff:

source_patch_id == ASH-BASETRAIN-GPU-70K-G207A9
AND source_candidate_apply_boundary_declared == true
AND source_diff_gate_bound_to_candidate_apply_boundary == true
AND source_apply_boundary_validation_passed == true
AND source_candidate_apply_positive_path_opened == true
AND source_all_candidate_apply_negative_paths_blocked == true
AND source_ready_for_g207a10 == true
AND candidate_apply_mode == dry-run
AND candidate_artifact_scope == scoped
AND production_commit_mode == forbid
AND checkpoint_write_mode == forbid
AND safetensors_write_mode == forbid
AND production_route_pointer_commit_mode == forbid
AND base_weight_mutation_mode == forbid
```

Candidate route pointer plan may be created and validated, but candidate route pointer commit, production route pointer commit, production route pointer rewrite, checkpoint rewrite, safetensors rewrite, and production base weight mutation must remain forbidden.

## Expected PASS Summary

```text
previous_g207a9_accepted=true
source_patch_id=ASH-BASETRAIN-GPU-70K-G207A9
phase=PhaseA
training_loop_owner=training.rs
active_training_route=FreshInit
candidate_apply_dry_run_receipt_created=true
g207a9_source_audit_created=true
boundary_gate_load_audit_created=true
scoped_candidate_artifact_created=true
scoped_candidate_artifact_manifest_created=true
candidate_artifact_validation_created=true
candidate_route_pointer_plan_created=true
candidate_route_pointer_plan_audit_created=true
no_production_route_pointer_commit_audit_created=true
no_production_commit_audit_created=true
no_base_weight_mutation_audit_created=true
no_checkpoint_rewrite_audit_created=true
no_safetensors_rewrite_audit_created=true
no_quality_claim_audit_created=true
atlas_deferred_audit_created=true
tensorcube_disabled_audit_created=true
next_g207a11_entry_packet_created=true
candidate_apply_boundary_loaded=true
diff_gate_boundary_loaded=true
a8_regression_matrix_requirement_loaded=true
apply_boundary_validation_loaded=true
candidate_apply_entry_allowed=true
scoped_candidate_artifact_created=true
candidate_artifact_scope=Scoped
candidate_artifact_owner=training.rs
candidate_artifact_phase=PhaseA
candidate_artifact_route=FreshInit
candidate_artifact_kind=DryRunReceipt
candidate_artifact_is_production=false
candidate_artifact_manifest_created=true
candidate_artifact_receipt_created=true
candidate_apply_mode=DryRun
candidate_apply_dry_run_executed=true
candidate_apply_dry_run_receipt_created=true
candidate_apply_boundary_gate_verified=true
candidate_apply_dry_run_validation_passed=true
candidate_route_pointer_plan_created=true
candidate_route_pointer_plan_scope=CandidateLocal
candidate_route_pointer_plan_validated=true
candidate_route_pointer_committed=false
production_route_pointer_committed=false
production_route_pointer_rewritten=false
route_pointer_rewritten=false
production_commit_executed=false
production_apply_executed=false
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
ready_for_g207a11=true
```

## Failure Conditions

```text
source_patch_id != ASH-BASETRAIN-GPU-70K-G207A9
phase != phase-a
active_route != freshinit
training_rs_route_required != true
source_candidate_apply_boundary_required != true
source_diff_gate_boundary_required != true
source_a8_regression_matrix_required != true
source_apply_boundary_validation_required != true
source_positive_boundary_path_required != true
source_negative_boundary_paths_required != true
candidate_apply_mode != dry-run
candidate_artifact_scope != scoped
candidate_artifact_write_mode != allow
candidate_artifact_kind != dry-run-receipt
candidate_route_pointer_plan_mode != create-plan-only
candidate_route_pointer_commit_mode != forbid
production_route_pointer_commit_mode != forbid
production_commit_mode != forbid
checkpoint_write_mode != forbid
safetensors_write_mode != forbid
base_weight_mutation_mode != forbid
dry_run_verdict_mode != strict
artifact_retention_mode != enable
no_artifacts_mode != forbid
atlas_route_mode != defer
tensorcube_mode != keep-disabled
training_quality_claim_mode != forbid
model_improvement_claim_mode != forbid
deployment_ready_mode != forbid
next_patch != ASH-BASETRAIN-GPU-70K-G207A11
```

Forbidden states:

```text
candidate_apply_boundary_loaded=false
diff_gate_boundary_loaded=false
a8_regression_matrix_requirement_loaded=false
apply_boundary_validation_loaded=false
candidate_apply_entry_allowed=false
scoped_candidate_artifact_created=false
candidate_artifact_is_production=true
candidate_artifact_manifest_created=false
candidate_artifact_receipt_created=false
candidate_apply_dry_run_executed=false
candidate_apply_dry_run_receipt_created=false
candidate_apply_boundary_gate_verified=false
candidate_apply_dry_run_validation_passed=false
candidate_route_pointer_plan_created=false
candidate_route_pointer_plan_validated=false
candidate_route_pointer_committed=true
production_route_pointer_committed=true
production_route_pointer_rewritten=true
production_commit_executed=true
production_apply_executed=true
production_base_weight_mutated=true
checkpoint_rewritten=true
safetensors_rewritten=true
route_pointer_rewritten=true
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

1. G207A9 source state is consumed.
2. training loop owner remains training.rs.
3. active route remains FreshInit.
4. candidate apply boundary is loaded.
5. diff gate boundary is loaded.
6. A8 regression matrix requirement is loaded.
7. apply boundary validation is loaded.
8. candidate apply entry is allowed only under valid A9 state.
9. scoped candidate artifact is created.
10. scoped candidate artifact is marked non-production.
11. scoped candidate artifact manifest is created.
12. scoped candidate artifact receipt is created.
13. candidate apply dry-run executes.
14. candidate apply dry-run receipt is created.
15. candidate apply boundary gate is verified.
16. candidate apply dry-run validation passes.
17. candidate route pointer plan is created.
18. candidate route pointer plan is validated.
19. candidate route pointer is not committed.
20. production route pointer is not committed.
21. production route pointer is not rewritten.
22. production commit does not execute.
23. production apply does not execute.
24. production base weights are not mutated.
25. checkpoint is not rewritten.
26. safetensors are not rewritten.
27. no training quality, model improvement, production, or deployment claim occurs.
28. Atlas remains deferred.
29. TensorCube 8x8 remains disabled.
30. G207A11 entry packet is created.
```

## Implementation Notes

- Implement as a scoped candidate apply dry-run.
- This patch does not perform production apply.
- This patch does not need to run a new training sequence.
- It must consume or validate the G207A9 boundary binding receipt.
- Candidate artifact must be scoped and non-production.
- Candidate route pointer plan may be created but must not be committed.
- Production route pointer must not be committed or rewritten.
- Production checkpoint and safetensors must not be rewritten.
- Production base weights must not be mutated.
- Use explicit JSON atlas writer for large receipts.
- Do not use large serde JSON macro objects.
- Do not add recursion limit workarounds.
- Do not execute Atlas.
- Do not enable TensorCube 8x8.
- Invalid CLI enum values must fail closed.

## Next Patch

`ASH-BASETRAIN-GPU-70K-G207A11` should load the scoped candidate artifact from A10, compare it against the expected apply surface, validate the candidate route pointer plan without committing it, and write a promotion precheck receipt while still forbidding production checkpoint, safetensors, route pointer rewrite, Atlas execution, TensorCube enablement, and quality claims.
