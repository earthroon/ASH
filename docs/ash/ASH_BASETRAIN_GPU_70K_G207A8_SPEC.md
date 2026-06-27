# ASH-BASETRAIN-GPU-70K-G207A8

## Diff Regression Matrix And Negative Fixture Gate / Fail Closed Drift Cases / No Quality Claim

PatchId: `ASH-BASETRAIN-GPU-70K-G207A8`  
SourcePatchId: `ASH-BASETRAIN-GPU-70K-G207A7`  
NextPatchId: `ASH-BASETRAIN-GPU-70K-G207A9`  
RuntimePassTarget: `PASS_ASH_BASETRAIN_GPU_70K_G207A8_DIFF_REGRESSION_MATRIX_AND_NEGATIVE_FIXTURE_GATE_FAIL_CLOSED_DRIFT_CASES_NO_QUALITY_CLAIM`

## Purpose

G207A8 consumes the G207A7 tolerance-applied replay diff execution gate and introduces a regression matrix of positive and negative fixtures.

G207A7 proved that the happy-path source/replay diff can pass under the A6 policy. G207A8 proves that the gate fails closed when fixture drift violates the policy.

A8 is a regression and fail-closed fixture gate. It is not a model quality gate.

## Runtime Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g207a8_diff_regression_matrix -- `
  --local-root . `
  --out-dir artifacts `
  --source-patch-id ASH-BASETRAIN-GPU-70K-G207A7 `
  --phase phase-a `
  --active-route freshinit `
  --training-rs-route-required true `
  --source-tolerance-applied-diff-required true `
  --source-policy-lineage-required true `
  --source-ledger-schema loss-grad-delta-v1 `
  --source-step-count 8 `
  --fixture-mode regression-matrix `
  --positive-fixture-mode require-pass `
  --negative-fixture-mode require-fail-closed `
  --loss-tolerance-negative-fixture enable `
  --grad-norm-tolerance-negative-fixture enable `
  --delta-norm-tolerance-negative-fixture enable `
  --learning-rate-exact-negative-fixture enable `
  --step-index-exact-negative-fixture enable `
  --ledger-shape-negative-fixture enable `
  --forbidden-claim-negative-fixture enable `
  --production-mutation-negative-fixture enable `
  --missing-section-negative-fixture enable `
  --unknown-required-field-negative-fixture enable `
  --expected-actual-verdict-mode strict `
  --fail-closed-mode required `
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
  --next-patch ASH-BASETRAIN-GPU-70K-G207A9
```

## Output Artifacts Written By Rust

```text
ASH_BASETRAIN_GPU_70K_G207A8_DIFF_REGRESSION_MATRIX_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G207A8_G207A7_SOURCE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A8_POLICY_LINEAGE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A8_FIXTURE_MATRIX.json
ASH_BASETRAIN_GPU_70K_G207A8_POSITIVE_FIXTURE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A8_NEGATIVE_TOLERANCE_FIXTURE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A8_NEGATIVE_EXACT_FIELD_FIXTURE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A8_NEGATIVE_FORBIDDEN_DRIFT_FIXTURE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A8_NEGATIVE_RECEIPT_STRUCTURE_FIXTURE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A8_EXPECTED_ACTUAL_VERDICT_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A8_FAIL_CLOSED_BEHAVIOR_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A8_NO_QUALITY_CLAIM_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A8_NO_PRODUCTION_COMMIT_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A8_NO_CHECKPOINT_REWRITE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A8_NO_SAFETENSORS_REWRITE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A8_ATLAS_DEFERRED_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A8_TENSORCUBE_DISABLED_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A8_NEXT_G207A9_ENTRY_PACKET.json
```

## Fixture Matrix

```text
FIXTURE_POSITIVE_BASELINE_PASS
FIXTURE_NEG_LOSS_TOLERANCE_FAIL
FIXTURE_NEG_GRAD_NORM_TOLERANCE_FAIL
FIXTURE_NEG_DELTA_NORM_TOLERANCE_FAIL
FIXTURE_NEG_LEARNING_RATE_EXACT_FAIL
FIXTURE_NEG_STEP_INDEX_EXACT_FAIL
FIXTURE_NEG_LEDGER_SHAPE_FAIL
FIXTURE_NEG_FORBIDDEN_CLAIM_FAIL
FIXTURE_NEG_PRODUCTION_MUTATION_FAIL
FIXTURE_NEG_MISSING_SECTION_FAIL
FIXTURE_NEG_UNKNOWN_REQUIRED_FIELD_FAIL
```

## Expected PASS Summary

```text
previous_g207a7_accepted=true
source_patch_id=ASH-BASETRAIN-GPU-70K-G207A7
phase=PhaseA
training_loop_owner=training.rs
active_training_route=FreshInit
fixture_mode=RegressionMatrix
fixture_count_total=11
positive_fixture_count=1
negative_fixture_count=10
all_fixture_ids_unique=true
all_fixture_expected_verdicts_defined=true
all_fixture_actual_verdicts_recorded=true
positive_diff_fixture_passed=true
negative_loss_tolerance_fixture_failed=true
negative_grad_norm_tolerance_fixture_failed=true
negative_delta_norm_tolerance_fixture_failed=true
negative_learning_rate_exact_fixture_failed=true
negative_step_index_exact_fixture_failed=true
negative_ledger_shape_fixture_failed=true
negative_forbidden_claim_fixture_failed=true
negative_production_mutation_fixture_failed=true
negative_missing_section_fixture_failed=true
negative_unknown_required_field_fixture_failed=true
expected_actual_verdict_parity_passed=true
all_positive_fixtures_passed=true
all_negative_fixtures_failed_closed=true
fail_closed_behavior_validated=true
regression_matrix_passed=true
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
ready_for_g207a9=true
```

## Failure Conditions

```text
source_patch_id != ASH-BASETRAIN-GPU-70K-G207A7
phase != phase-a
active_route != freshinit
training_rs_route_required != true
source_tolerance_applied_diff_required != true
source_policy_lineage_required != true
source_ledger_schema != loss-grad-delta-v1
source_step_count != 8
fixture_mode != regression-matrix
positive_fixture_mode != require-pass
negative_fixture_mode != require-fail-closed
loss_tolerance_negative_fixture != enable
grad_norm_tolerance_negative_fixture != enable
delta_norm_tolerance_negative_fixture != enable
learning_rate_exact_negative_fixture != enable
step_index_exact_negative_fixture != enable
ledger_shape_negative_fixture != enable
forbidden_claim_negative_fixture != enable
production_mutation_negative_fixture != enable
missing_section_negative_fixture != enable
unknown_required_field_negative_fixture != enable
expected_actual_verdict_mode != strict
fail_closed_mode != required
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
next_patch != ASH-BASETRAIN-GPU-70K-G207A9
```

Forbidden states:

```text
diff_regression_matrix_created=false
positive_diff_fixture_passed=false
negative_loss_tolerance_fixture_failed=false
negative_grad_norm_tolerance_fixture_failed=false
negative_delta_norm_tolerance_fixture_failed=false
negative_learning_rate_exact_fixture_failed=false
negative_step_index_exact_fixture_failed=false
negative_ledger_shape_fixture_failed=false
negative_forbidden_claim_fixture_failed=false
negative_production_mutation_fixture_failed=false
negative_missing_section_fixture_failed=false
negative_unknown_required_field_fixture_failed=false
expected_actual_verdict_parity_passed=false
all_positive_fixtures_passed=false
all_negative_fixtures_failed_closed=false
fail_closed_behavior_validated=false
regression_matrix_passed=false
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

## Implementation Notes

- Implement as a regression fixture matrix gate.
- This patch does not need to run a new training sequence.
- It must consume or validate the G207A7 tolerance-applied diff receipt.
- Positive fixture must pass.
- Negative fixtures must fail closed, not merely warn.
- Fixture verdicts must be explicit.
- Expected/actual verdict mismatch must fail.
- Missing required section must fail closed.
- Unknown required field drift must fail closed.
- Forbidden claim drift must fail closed.
- Production mutation drift must fail closed.
- Use explicit JSON atlas writer for large receipts.
- Do not use large serde JSON macro objects.
- Do not add recursion limit workarounds.
- Do not mutate production base weights.
- Do not rewrite checkpoints or safetensors.
- Do not execute Atlas.
- Do not enable TensorCube 8x8.
- Invalid CLI enum values must fail closed.

## Next Patch

`ASH-BASETRAIN-GPU-70K-G207A9` should bind the A8 diff regression matrix gate to the candidate apply boundary. Candidate apply must be blocked unless A8 positive/negative fixture regression matrix has passed, while still forbidding production checkpoint writes, safetensors rewrites, Atlas execution, TensorCube enablement, and quality claims.
