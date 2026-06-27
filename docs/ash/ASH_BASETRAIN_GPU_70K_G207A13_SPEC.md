# ASH-BASETRAIN-GPU-70K-G207A13

## Staged Candidate Runtime Load Smoke / Load Promoted Candidate From Staging / No Production Pointer Switch

PatchId: `ASH-BASETRAIN-GPU-70K-G207A13`  
SourcePatchId: `ASH-BASETRAIN-GPU-70K-G207A12`  
NextPatchId: `ASH-BASETRAIN-GPU-70K-G207A14`  
RuntimePassTarget: `PASS_ASH_BASETRAIN_GPU_70K_G207A13_STAGED_CANDIDATE_RUNTIME_LOAD_SMOKE_LOAD_PROMOTED_CANDIDATE_FROM_STAGING_NO_PRODUCTION_POINTER_SWITCH`

## Purpose

G207A13 consumes the G207A12 staged candidate promotion receipt and loads the promoted candidate from the staging route pointer.

A12 committed the candidate route pointer to staging. A13 must load that staging pointer, load the staged candidate artifact, run a staging-only runtime smoke, validate the staging rollback path without executing rollback, and keep production pointer switch forbidden.

A13 is a staged runtime load smoke patch. It is not a production switch patch.

## Runtime Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g207a13_staged_candidate_runtime_load_smoke -- `
  --local-root . `
  --out-dir artifacts `
  --source-patch-id ASH-BASETRAIN-GPU-70K-G207A12 `
  --phase phase-a `
  --active-route freshinit `
  --training-rs-route-mode required `
  --source-staged-promotion-mode required `
  --source-staging-route-pointer-mode required `
  --source-staging-pointer-integrity-mode required `
  --source-staging-rollback-receipt-mode required `
  --source-production-pointer-switch-mode forbid `
  --staging-route-pointer-load-mode required `
  --staging-route-pointer-scope staging `
  --staged-candidate-artifact-load-mode required `
  --staged-candidate-runtime-load-mode smoke `
  --runtime-load-scope staging-only `
  --runtime-smoke-mode staged-load-smoke `
  --runtime-smoke-verdict-mode strict `
  --staged-candidate-route freshinit `
  --staged-candidate-owner training.rs `
  --staging-rollback-path-validation-mode validate-only `
  --rollback-execution-mode forbid `
  --production-route-pointer-switch-mode forbid `
  --production-route-pointer-commit-mode forbid `
  --production-apply-mode forbid `
  --production-commit-mode forbid `
  --checkpoint-write-mode forbid `
  --safetensors-write-mode forbid `
  --base-weight-mutation-mode forbid `
  --artifact-retention-mode enable `
  --no-artifacts-mode forbid `
  --atlas-route-mode defer `
  --tensorcube-mode keep-disabled `
  --training-quality-claim-mode forbid `
  --model-improvement-claim-mode forbid `
  --deployment-ready-mode forbid `
  --next-patch ASH-BASETRAIN-GPU-70K-G207A14
```

## Output Artifacts Written By Rust

```text
ASH_BASETRAIN_GPU_70K_G207A13_STAGED_RUNTIME_LOAD_SMOKE_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G207A13_G207A12_SOURCE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A13_STAGING_ROUTE_POINTER_LOAD_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A13_STAGING_ROUTE_POINTER_INTEGRITY_RECHECK.json
ASH_BASETRAIN_GPU_70K_G207A13_STAGED_CANDIDATE_ARTIFACT_LOAD_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A13_STAGED_CANDIDATE_ARTIFACT_IDENTITY_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A13_RUNTIME_LOAD_SMOKE_POLICY.json
ASH_BASETRAIN_GPU_70K_G207A13_RUNTIME_LOAD_SMOKE_RESULT.json
ASH_BASETRAIN_GPU_70K_G207A13_STAGING_ROLLBACK_PATH_VALIDATION.json
ASH_BASETRAIN_GPU_70K_G207A13_NO_ROLLBACK_EXECUTION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A13_NO_PRODUCTION_POINTER_SWITCH_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A13_NO_PRODUCTION_APPLY_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A13_NO_CHECKPOINT_REWRITE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A13_NO_SAFETENSORS_REWRITE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A13_NO_QUALITY_CLAIM_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A13_ATLAS_DEFERRED_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A13_TENSORCUBE_DISABLED_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A13_NEXT_G207A14_ENTRY_PACKET.json
```

These artifacts must be generated locally by the Rust binary and must not be pre-baked into the ZIP.

## Staged Runtime Load Rule

```text
staged_candidate_runtime_load_allowed iff:

source_patch_id == ASH-BASETRAIN-GPU-70K-G207A12
AND source_staged_candidate_promotion_passed == true
AND source_staging_route_pointer_available == true
AND source_staging_pointer_integrity_passed == true
AND source_staging_rollback_path_available == true
AND staging_route_pointer_load_mode == required
AND staging_route_pointer_scope == staging
AND staged_candidate_artifact_load_mode == required
AND runtime_load_scope == staging-only
AND staged_candidate_runtime_load_mode == smoke
AND runtime_smoke_mode == staged-load-smoke
AND production_route_pointer_switch_mode == forbid
AND production_route_pointer_commit_mode == forbid
AND production_apply_mode == forbid
AND checkpoint_write_mode == forbid
AND safetensors_write_mode == forbid
AND base_weight_mutation_mode == forbid
```

## Expected PASS Summary

```text
previous_g207a12_accepted=true
source_patch_id=ASH-BASETRAIN-GPU-70K-G207A12
phase=PhaseA
training_loop_owner=training.rs
active_training_route=FreshInit
staging_route_pointer_loaded=true
staging_route_pointer_scope=Staging
staging_route_pointer_owner=training.rs
staging_route_pointer_phase=PhaseA
staging_route_pointer_route=FreshInit
staging_route_pointer_points_to_candidate_artifact=true
staging_route_pointer_is_production=false
staging_route_pointer_integrity_rechecked=true
staging_route_pointer_integrity_recheck_passed=true
staged_candidate_artifact_loaded=true
staged_candidate_artifact_source=StagingRoutePointer
staged_candidate_artifact_scope=Staging
staged_candidate_artifact_owner=training.rs
staged_candidate_artifact_phase=PhaseA
staged_candidate_artifact_route=FreshInit
staged_candidate_artifact_is_production=false
staged_candidate_artifact_identity_matched=true
staged_candidate_artifact_load_validation_passed=true
runtime_load_scope=StagingOnly
staged_candidate_runtime_load_executed=true
staged_candidate_runtime_load_owner=training.rs
staged_candidate_runtime_load_route=FreshInit
staged_candidate_runtime_smoke_executed=true
staged_candidate_runtime_smoke_passed=true
runtime_smoke_quality_claimed=false
runtime_smoke_deployment_claimed=false
staging_rollback_receipt_loaded=true
staging_rollback_path_validated=true
staging_rollback_target_available=true
staging_rollback_validation_passed=true
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
ready_for_g207a14=true
```

## Failure Conditions

```text
source_patch_id != ASH-BASETRAIN-GPU-70K-G207A12
phase != phase-a
active_route != freshinit
training_rs_route_mode != required
source_staged_promotion_mode != required
source_staging_route_pointer_mode != required
source_staging_pointer_integrity_mode != required
source_staging_rollback_receipt_mode != required
source_production_pointer_switch_mode != forbid
staging_route_pointer_load_mode != required
staging_route_pointer_scope != staging
staged_candidate_artifact_load_mode != required
staged_candidate_runtime_load_mode != smoke
runtime_load_scope != staging-only
runtime_smoke_mode != staged-load-smoke
runtime_smoke_verdict_mode != strict
staged_candidate_route != freshinit
staged_candidate_owner != training.rs
staging_rollback_path_validation_mode != validate-only
rollback_execution_mode != forbid
production_route_pointer_switch_mode != forbid
production_route_pointer_commit_mode != forbid
production_apply_mode != forbid
production_commit_mode != forbid
checkpoint_write_mode != forbid
safetensors_write_mode != forbid
base_weight_mutation_mode != forbid
artifact_retention_mode != enable
no_artifacts_mode != forbid
atlas_route_mode != defer
tensorcube_mode != keep-disabled
training_quality_claim_mode != forbid
model_improvement_claim_mode != forbid
deployment_ready_mode != forbid
next_patch != ASH-BASETRAIN-GPU-70K-G207A14
```

Forbidden states:

```text
staging_route_pointer_loaded=false
staging_route_pointer_is_production=true
staging_route_pointer_integrity_recheck_passed=false
staged_candidate_artifact_loaded=false
staged_candidate_artifact_is_production=true
staged_candidate_artifact_identity_matched=false
staged_candidate_artifact_load_validation_passed=false
staged_candidate_runtime_load_executed=false
staged_candidate_runtime_smoke_executed=false
staged_candidate_runtime_smoke_passed=false
runtime_smoke_quality_claimed=true
runtime_smoke_deployment_claimed=true
staging_rollback_path_validated=false
staging_rollback_validation_passed=false
rollback_executed=true
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

1. G207A12 source state is consumed.
2. training loop owner remains training.rs.
3. active route remains FreshInit.
4. staging route pointer is loaded.
5. staging route pointer scope is Staging.
6. staging route pointer is non-production.
7. staging route pointer points to candidate artifact.
8. staging route pointer integrity recheck passes.
9. staged candidate artifact is loaded from staging pointer.
10. staged candidate artifact is non-production.
11. staged candidate artifact identity matches the staging pointer.
12. staged candidate artifact load validation passes.
13. staged candidate runtime load executes.
14. staged candidate runtime smoke executes.
15. staged candidate runtime smoke passes.
16. runtime smoke does not claim quality.
17. runtime smoke does not claim deployment readiness.
18. staging rollback receipt is loaded.
19. staging rollback path is validated.
20. rollback target is available.
21. rollback execution remains false.
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
33. G207A14 entry packet is created.
```

## Implementation Notes

- Implement as a staged candidate runtime load smoke.
- This patch loads the staging route pointer committed by A12.
- This patch loads the staged candidate artifact via the staging pointer.
- This patch performs a runtime smoke against staging only.
- This patch validates rollback path but does not execute rollback.
- This patch does not perform production route pointer switch.
- This patch does not perform production apply.
- This patch does not rewrite checkpoint or safetensors.
- Runtime smoke must not claim quality or model improvement.
- Use explicit JSON atlas writer for large receipts.
- Do not use large serde JSON macro objects.
- Do not add recursion limit workarounds.
- Use string mode CLI args only. Do not use boolean value flags.
- Do not execute Atlas.
- Do not enable TensorCube 8x8.
- Invalid CLI enum values must fail closed.

## Next Patch

`ASH-BASETRAIN-GPU-70K-G207A14` should consume the G207A13 staged runtime smoke receipt, require explicit operator approval for the production switch, switch the production route pointer to the staged candidate, create a production pointer switch receipt, create a production rollback receipt, and still forbid checkpoint rewrite, safetensors rewrite, Atlas execution, TensorCube enablement, and quality claims.
