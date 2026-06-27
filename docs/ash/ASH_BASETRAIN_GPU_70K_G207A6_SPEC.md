# ASH-BASETRAIN-GPU-70K-G207A6

## Replay Tolerance And Receipt Comparison Hardening / Numeric Tolerance Policy / No Quality Claim

PatchId: `ASH-BASETRAIN-GPU-70K-G207A6`  
SourcePatchId: `ASH-BASETRAIN-GPU-70K-G207A5`  
NextPatchId: `ASH-BASETRAIN-GPU-70K-G207A7`  
RuntimePassTarget: `PASS_ASH_BASETRAIN_GPU_70K_G207A6_REPLAY_TOLERANCE_AND_RECEIPT_COMPARISON_HARDENING_NUMERIC_TOLERANCE_POLICY_NO_QUALITY_CLAIM`

## Purpose

G207A6 consumes the G207A5 deterministic replay repeatability receipt and defines a strict numeric tolerance and receipt comparison policy for future replay gates.

A5 proved same seed policy, same batch sequence policy, matched step count, same ledger shape, reproduced loss direction, digest policy match, and optimizer continuity policy match.

A6 hardens the comparison layer by defining which fields must match exactly and which numeric fields may be compared with bounded tolerance.

A6 is a comparison contract patch. It does not claim training quality, model improvement, production readiness, deployment readiness, or broad convergence.

## Runtime Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g207a6_replay_tolerance_hardening -- `
  --local-root . `
  --out-dir artifacts `
  --source-patch-id ASH-BASETRAIN-GPU-70K-G207A5 `
  --phase phase-a `
  --active-route freshinit `
  --training-rs-route-required true `
  --source-replay-repeatability-required true `
  --source-ledger-schema loss-grad-delta-v1 `
  --source-step-count 8 `
  --tolerance-policy define `
  --loss-abs-tolerance 0.000001 `
  --loss-rel-tolerance 0.000001 `
  --grad-norm-abs-tolerance 0.000001 `
  --grad-norm-rel-tolerance 0.000001 `
  --delta-norm-abs-tolerance 0.000001 `
  --delta-norm-rel-tolerance 0.000001 `
  --learning-rate-compare-mode exact `
  --step-index-compare-mode exact `
  --ledger-shape-compare-mode exact `
  --digest-compare-mode exact-policy `
  --optimizer-continuity-compare-mode exact-policy `
  --receipt-compare-mode hardened `
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
  --next-patch ASH-BASETRAIN-GPU-70K-G207A7
```

## Output Artifacts Written By Rust

```text
ASH_BASETRAIN_GPU_70K_G207A6_REPLAY_TOLERANCE_HARDENING_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G207A6_G207A5_SOURCE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A6_NUMERIC_TOLERANCE_POLICY.json
ASH_BASETRAIN_GPU_70K_G207A6_EXACT_MATCH_FIELD_POLICY.json
ASH_BASETRAIN_GPU_70K_G207A6_TOLERANCE_MATCH_FIELD_POLICY.json
ASH_BASETRAIN_GPU_70K_G207A6_RECEIPT_COMPARISON_POLICY.json
ASH_BASETRAIN_GPU_70K_G207A6_LEDGER_HASH_POLICY.json
ASH_BASETRAIN_GPU_70K_G207A6_FORBIDDEN_DRIFT_POLICY.json
ASH_BASETRAIN_GPU_70K_G207A6_POLICY_SCHEMA_VALIDATION.json
ASH_BASETRAIN_GPU_70K_G207A6_COMPARISON_HARDENING_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A6_NO_QUALITY_CLAIM_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A6_NO_PRODUCTION_COMMIT_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A6_NO_CHECKPOINT_REWRITE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A6_NO_SAFETENSORS_REWRITE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A6_ATLAS_DEFERRED_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A6_TENSORCUBE_DISABLED_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A6_NEXT_G207A7_ENTRY_PACKET.json
```

## Numeric Comparison Formula

```text
abs(a - b) <= max(abs_tolerance, rel_tolerance * max(abs(a), abs(b)))
```

This rule applies only to:

```text
loss
grad_norm
delta_norm
```

It must not be used for learning rate, step index, step count, ledger schema, digest fields, guard booleans, production mutation flags, or quality claim flags. Those fields require exact or exact-policy comparison.

## Expected PASS Summary

```text
previous_g207a5_accepted=true
source_patch_id=ASH-BASETRAIN-GPU-70K-G207A5
phase=PhaseA
training_loop_owner=training.rs
active_training_route=FreshInit
numeric_tolerance_policy_defined=true
tolerance_policy_version=ReplayToleranceV1
loss_abs_tolerance=0.000001
loss_rel_tolerance=0.000001
grad_norm_abs_tolerance=0.000001
grad_norm_rel_tolerance=0.000001
delta_norm_abs_tolerance=0.000001
delta_norm_rel_tolerance=0.000001
learning_rate_exact_match_required=true
step_index_exact_match_required=true
step_count_exact_match_required=true
ledger_shape_exact_match_required=true
digest_policy_exact_match_required=true
optimizer_continuity_policy_exact_match_required=true
exact_match_fields_defined=true
tolerance_match_fields_defined=true
receipt_comparison_policy_defined=true
ledger_hash_policy_defined=true
forbidden_drift_fields_defined=true
policy_schema_valid=true
comparison_hardening_applied=true
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
ready_for_g207a7=true
```

## Failure Conditions

```text
source_patch_id != ASH-BASETRAIN-GPU-70K-G207A5
phase != phase-a
active_route != freshinit
training_rs_route_required != true
source_replay_repeatability_required != true
source_ledger_schema != loss-grad-delta-v1
source_step_count != 8
tolerance_policy != define
loss_abs_tolerance <= 0
loss_rel_tolerance <= 0
grad_norm_abs_tolerance <= 0
grad_norm_rel_tolerance <= 0
delta_norm_abs_tolerance <= 0
delta_norm_rel_tolerance <= 0
learning_rate_compare_mode != exact
step_index_compare_mode != exact
ledger_shape_compare_mode != exact
digest_compare_mode != exact-policy
optimizer_continuity_compare_mode != exact-policy
receipt_compare_mode != hardened
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
next_patch != ASH-BASETRAIN-GPU-70K-G207A7
```

Forbidden states:

```text
numeric_tolerance_policy_defined=false
receipt_comparison_policy_defined=false
ledger_hash_policy_defined=false
forbidden_drift_fields_defined=false
policy_schema_valid=false
comparison_hardening_applied=false
learning_rate_exact_match_required=false
step_index_exact_match_required=false
ledger_shape_exact_match_required=false
digest_policy_exact_match_required=false
optimizer_continuity_policy_exact_match_required=false
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

- Implement as a policy hardening patch.
- This patch does not need to run a new training sequence.
- It must consume or validate the G207A5 replay repeatability receipt.
- Use explicit JSON atlas writer for large policy receipts.
- Do not use large serde JSON macro objects.
- Do not add recursion limit workarounds.
- Numeric comparison policy must use both absolute and relative tolerance.
- Learning rate, step index, step count, ledger schema, digest policy, and optimizer continuity policy must remain exact or exact-policy.
- Missing required receipt sections must fail closed.
- Unknown required field drift must fail closed.
- Do not mutate production base weights.
- Do not rewrite checkpoints or safetensors.
- Do not execute Atlas.
- Do not enable TensorCube 8x8.
- Invalid CLI enum values must fail closed.

## Next Patch

`ASH-BASETRAIN-GPU-70K-G207A7` should load the A6 tolerance policy, compare source and replay loss/grad/delta values under tolerance, compare learning rate exactly, validate ledger hash policy, and write a tolerance-applied diff receipt without claiming model quality or production readiness.
