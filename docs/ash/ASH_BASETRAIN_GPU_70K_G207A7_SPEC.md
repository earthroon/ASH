# ASH-BASETRAIN-GPU-70K-G207A7

## Tolerance Applied Replay Diff Execution Gate / Loss Grad Delta Compared Under Policy / No Quality Claim

PatchId: `ASH-BASETRAIN-GPU-70K-G207A7`  
SourcePatchId: `ASH-BASETRAIN-GPU-70K-G207A6`  
NextPatchId: `ASH-BASETRAIN-GPU-70K-G207A8`  
RuntimePassTarget: `PASS_ASH_BASETRAIN_GPU_70K_G207A7_TOLERANCE_APPLIED_REPLAY_DIFF_EXECUTION_GATE_LOSS_GRAD_DELTA_COMPARED_UNDER_POLICY_NO_QUALITY_CLAIM`

## Purpose

G207A7 consumes the G207A6 replay tolerance and receipt comparison hardening policy, then applies that policy to a source/replay diff gate.

This patch validates that source and replay values can be compared under the explicit A6 rules. A7 may claim policy loading, tolerance-applied diff execution, tolerance comparison of loss/grad_norm/delta_norm, exact comparison of learning rate and ledger shape fields, ledger hash validation, and receipt comparison success.

A7 must not claim training quality, model improvement, production readiness, deployment readiness, or broad convergence.

## Runtime Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g207a7_tolerance_applied_replay_diff -- `
  --local-root . `
  --out-dir artifacts `
  --source-patch-id ASH-BASETRAIN-GPU-70K-G207A6 `
  --phase phase-a `
  --active-route freshinit `
  --training-rs-route-required true `
  --source-tolerance-policy-required true `
  --source-receipt-comparison-policy-required true `
  --source-ledger-hash-policy-required true `
  --source-forbidden-drift-policy-required true `
  --source-ledger-schema loss-grad-delta-v1 `
  --source-step-count 8 `
  --diff-mode tolerance-applied `
  --numeric-tolerance-policy ReplayToleranceV1 `
  --receipt-comparison-policy ReceiptComparisonV1 `
  --ledger-hash-policy LedgerHashPolicyV1 `
  --loss-compare-mode tolerance `
  --grad-norm-compare-mode tolerance `
  --delta-norm-compare-mode tolerance `
  --learning-rate-compare-mode exact `
  --step-index-compare-mode exact `
  --step-count-compare-mode exact `
  --ledger-shape-compare-mode exact `
  --digest-compare-mode exact-policy `
  --optimizer-continuity-compare-mode exact-policy `
  --forbidden-drift-mode fail-closed `
  --artifact-retention-mode enable `
  --no-artifacts-mode forbid `
  --production-commit-mode forbid `
  --checkpoint-write-mode forbid `
  --safetensors-write-mode forbid `
  --route-pointer-write-mode forbid `
  --atlas-route-mode defer `
  --tensorcube-mode keep-disabled `
  --training-quality-claim-mode forbid `
  --model-improvement-claim-mode forbid `
  --deployment-ready-mode forbid `
  --next-patch ASH-BASETRAIN-GPU-70K-G207A8
```

## Output Artifacts Written By Rust

```text
ASH_BASETRAIN_GPU_70K_G207A7_TOLERANCE_APPLIED_DIFF_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G207A7_G207A6_SOURCE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A7_POLICY_LOAD_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A7_SOURCE_REPLAY_DIFF_EXECUTION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A7_NUMERIC_TOLERANCE_DIFF_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A7_EXACT_MATCH_DIFF_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A7_LEDGER_HASH_VALIDATION.json
ASH_BASETRAIN_GPU_70K_G207A7_FORBIDDEN_DRIFT_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A7_RECEIPT_COMPARISON_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A7_NO_QUALITY_CLAIM_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A7_NO_PRODUCTION_COMMIT_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A7_NO_CHECKPOINT_REWRITE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A7_NO_SAFETENSORS_REWRITE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A7_ATLAS_DEFERRED_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A7_TENSORCUBE_DISABLED_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A7_NEXT_G207A8_ENTRY_PACKET.json
```

## Tolerance Comparison Formula

```text
abs(a - b) <= max(abs_tolerance, rel_tolerance * max(abs(a), abs(b)))
```

Applied fields:

```text
loss
grad_norm
delta_norm
```

Exact fields:

```text
learning_rate
step_index
step_count
ledger_schema
ledger_required_field_set
ledger_shape
digest_policy
optimizer_continuity_policy
guard booleans
production mutation flags
quality claim flags
```

## Expected PASS Summary

```text
previous_g207a6_accepted=true
source_patch_id=ASH-BASETRAIN-GPU-70K-G207A6
phase=PhaseA
training_loop_owner=training.rs
active_training_route=FreshInit
numeric_tolerance_policy_loaded=true
receipt_comparison_policy_loaded=true
ledger_hash_policy_loaded=true
forbidden_drift_policy_loaded=true
policy_versions_matched=true
policy_schema_valid=true
diff_mode=ToleranceApplied
source_replay_diff_executed=true
source_replay_pairing_valid=true
source_step_count=8
replay_step_count=8
step_count_exact_match_passed=true
loss_compared_under_tolerance=true
grad_norm_compared_under_tolerance=true
delta_norm_compared_under_tolerance=true
loss_tolerance_passed=true
grad_norm_tolerance_passed=true
delta_norm_tolerance_passed=true
all_tolerance_comparisons_passed=true
learning_rate_exact_match_passed=true
step_index_exact_match_passed=true
step_count_exact_match_passed=true
ledger_shape_exact_match_passed=true
ledger_required_fields_exact_match_passed=true
digest_policy_exact_match_passed=true
optimizer_continuity_policy_exact_match_passed=true
all_exact_comparisons_passed=true
ledger_hash_policy_validated=true
source_ledger_hash_created=true
replay_ledger_hash_created=true
ledger_hash_match_passed=true
forbidden_drift_policy_validated=true
forbidden_drift_detected=false
receipt_comparison_passed=true
training_quality_claimed=false
model_improvement_claimed=false
production_claimed=false
deployment_ready_claimed=false
production_base_weight_mutated=false
checkpoint_rewritten=false
safetensors_rewritten=false
route_pointer_rewritten=false
atlas_route_executed=false
atlas_grouped_route_deferred=true
tensorcube_8x8_kept_disabled=true
tensorcube_matmul_replacement_enabled=false
ready_for_g207a8=true
```

## Failure Conditions

```text
source_patch_id != ASH-BASETRAIN-GPU-70K-G207A6
phase != phase-a
active_route != freshinit
training_rs_route_required != true
source_tolerance_policy_required != true
source_receipt_comparison_policy_required != true
source_ledger_hash_policy_required != true
source_forbidden_drift_policy_required != true
source_ledger_schema != loss-grad-delta-v1
source_step_count != 8
diff_mode != tolerance-applied
numeric_tolerance_policy != ReplayToleranceV1
receipt_comparison_policy != ReceiptComparisonV1
ledger_hash_policy != LedgerHashPolicyV1
loss_compare_mode != tolerance
grad_norm_compare_mode != tolerance
delta_norm_compare_mode != tolerance
learning_rate_compare_mode != exact
step_index_compare_mode != exact
step_count_compare_mode != exact
ledger_shape_compare_mode != exact
digest_compare_mode != exact-policy
optimizer_continuity_compare_mode != exact-policy
forbidden_drift_mode != fail-closed
artifact_retention_mode != enable
no_artifacts_mode != forbid
production_commit_mode != forbid
checkpoint_write_mode != forbid
safetensors_write_mode != forbid
route_pointer_write_mode != forbid
atlas_route_mode != defer
tensorcube_mode != keep-disabled
training_quality_claim_mode != forbid
model_improvement_claim_mode != forbid
deployment_ready_mode != forbid
next_patch != ASH-BASETRAIN-GPU-70K-G207A8
```

Forbidden states:

```text
numeric_tolerance_policy_loaded=false
receipt_comparison_policy_loaded=false
ledger_hash_policy_loaded=false
forbidden_drift_policy_loaded=false
source_replay_diff_executed=false
source_replay_pairing_valid=false
loss_compared_under_tolerance=false
grad_norm_compared_under_tolerance=false
delta_norm_compared_under_tolerance=false
loss_tolerance_passed=false
grad_norm_tolerance_passed=false
delta_norm_tolerance_passed=false
all_tolerance_comparisons_passed=false
learning_rate_exact_match_passed=false
step_index_exact_match_passed=false
step_count_exact_match_passed=false
ledger_shape_exact_match_passed=false
ledger_required_fields_exact_match_passed=false
digest_policy_exact_match_passed=false
optimizer_continuity_policy_exact_match_passed=false
ledger_hash_policy_validated=false
ledger_hash_match_passed=false
forbidden_drift_detected=true
training_quality_claimed=true
model_improvement_claimed=true
production_claimed=true
deployment_ready_claimed=true
production_base_weight_mutated=true
checkpoint_rewritten=true
safetensors_rewritten=true
route_pointer_rewritten=true
atlas_route_executed=true
tensorcube_matmul_replacement_enabled=true
```

## Acceptance Criteria

```text
PASS iff:

1. G207A6 source state is consumed.
2. training loop owner remains training.rs.
3. active route remains FreshInit.
4. A6 numeric tolerance policy is loaded.
5. A6 receipt comparison policy is loaded.
6. A6 ledger hash policy is loaded.
7. A6 forbidden drift policy is loaded.
8. policy versions match.
9. source/replay diff executes.
10. source/replay pairing is valid.
11. loss is compared under tolerance and passes.
12. grad_norm is compared under tolerance and passes.
13. delta_norm is compared under tolerance and passes.
14. learning_rate exact match passes.
15. step_index exact match passes.
16. step_count exact match passes.
17. ledger shape exact match passes.
18. ledger required fields exact match passes.
19. digest policy exact-policy match passes.
20. optimizer continuity exact-policy match passes.
21. ledger hash policy is validated.
22. source and replay ledger hashes match under policy.
23. forbidden drift policy is validated.
24. forbidden drift is not detected.
25. receipt comparison passes.
26. no training quality, model improvement, production, or deployment claim occurs.
27. production base weights are not mutated.
28. checkpoint and safetensors are not rewritten.
29. Atlas remains deferred.
30. TensorCube 8x8 remains disabled.
31. G207A8 entry packet is created.
```

## Implementation Notes

- Implement as a tolerance-applied replay diff execution gate.
- This patch does not need to run a new training sequence.
- It must consume or validate the G207A6 policy receipt.
- It must compare source/replay values using A6 policy.
- Use explicit JSON atlas writer for large receipts.
- Do not use large serde JSON macro objects.
- Do not add recursion limit workarounds.
- Numeric tolerance applies only to loss, grad_norm, and delta_norm.
- Learning rate must be exact.
- Step index and step count must be exact.
- Ledger schema and required fields must be exact.
- Digest policy must be exact-policy.
- Optimizer continuity policy must be exact-policy.
- Forbidden drift must fail closed.
- Missing required sections must fail closed.
- Unknown required field drift must fail closed.
- Do not mutate production base weights.
- Do not rewrite checkpoints or safetensors.
- Do not execute Atlas.
- Do not enable TensorCube 8x8.
- Invalid CLI enum values must fail closed.

## Next Patch

`ASH-BASETRAIN-GPU-70K-G207A8` should introduce positive and negative fixtures for the A7 diff gate, including tolerance pass, tolerance fail, exact-field drift fail, forbidden-claim drift fail, missing-section fail, and unknown-required-field fail cases.
