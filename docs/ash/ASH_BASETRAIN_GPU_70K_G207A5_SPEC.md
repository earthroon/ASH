# ASH-BASETRAIN-GPU-70K-G207A5

## Deterministic Replay Repeatability Gate / Same Seed Same Ledger Shape / No Quality Claim

PatchId: `ASH-BASETRAIN-GPU-70K-G207A5`  
SourcePatchId: `ASH-BASETRAIN-GPU-70K-G207A4`  
NextPatchId: `ASH-BASETRAIN-GPU-70K-G207A6`  
RuntimePassTarget: `PASS_ASH_BASETRAIN_GPU_70K_G207A5_DETERMINISTIC_REPLAY_REPEATABILITY_GATE_SAME_SEED_SAME_LEDGER_SHAPE_NO_QUALITY_CLAIM`

## Purpose

G207A5 consumes the G207A4 bounded FreshInit loss direction receipt and reruns the same deterministic FreshInit training sequence under the same replay seed and batch sequence policy.

This patch checks replay repeatability. It verifies same seed policy, same batch sequence policy, same ledger schema shape, matched step count, reproduced loss direction, digest policy match, and optimizer continuity policy match.

A5 must not claim training quality, model improvement, production readiness, deployment readiness, or broad convergence.

## Runtime Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g207a5_deterministic_replay_gate -- `
  --local-root . `
  --out-dir artifacts `
  --source-patch-id ASH-BASETRAIN-GPU-70K-G207A4 `
  --phase phase-a `
  --active-route freshinit `
  --training-rs-route-required true `
  --source-loss-direction-required true `
  --source-ledger-required true `
  --source-ledger-schema loss-grad-delta-v1 `
  --replay-mode deterministic `
  --replay-seed same-as-source `
  --batch-sequence-mode same-as-source `
  --run-mode bounded-multi-step `
  --step-count 8 `
  --freshinit-forward-mode execute `
  --loss-mode finite `
  --backward-mode execute `
  --optimizer-step-mode execute `
  --weight-delta-mode scoped `
  --loss-direction-check first-gt-last `
  --ledger-compare-mode same-shape `
  --digest-compare-mode same-policy `
  --optimizer-continuity-compare-mode same-policy `
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
  --next-patch ASH-BASETRAIN-GPU-70K-G207A6
```

## Local Artifact Policy

The baked ZIP contains the Rust artifact writer and this spec. Runtime JSON/JSONL artifacts are not pre-baked and are not committed. The Rust binary writes them locally under `--out-dir`.

## Output Artifacts Written By Rust

```text
ASH_BASETRAIN_GPU_70K_G207A5_REPLAY_REPEATABILITY_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G207A5_G207A4_SOURCE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A5_SOURCE_LOSS_DIRECTION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A5_SOURCE_LEDGER_SCHEMA_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A5_REPLAY_RUN_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A5_REPLAY_PER_STEP_LEDGER.jsonl
ASH_BASETRAIN_GPU_70K_G207A5_LEDGER_SHAPE_COMPARISON.json
ASH_BASETRAIN_GPU_70K_G207A5_STEP_COUNT_COMPARISON.json
ASH_BASETRAIN_GPU_70K_G207A5_REPLAY_FINITE_VALUE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A5_REPLAY_LOSS_FIRST_LAST_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A5_LOSS_DIRECTION_REPRODUCTION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A5_DIGEST_POLICY_COMPARISON.json
ASH_BASETRAIN_GPU_70K_G207A5_OPTIMIZER_CONTINUITY_POLICY_COMPARISON.json
ASH_BASETRAIN_GPU_70K_G207A5_NO_QUALITY_CLAIM_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A5_NO_PRODUCTION_COMMIT_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A5_NO_CHECKPOINT_REWRITE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A5_NO_SAFETENSORS_REWRITE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A5_ATLAS_DEFERRED_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A5_TENSORCUBE_DISABLED_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A5_NEXT_G207A6_ENTRY_PACKET.json
```

## Replay Ledger Row Shape

```json
{
  "patch_id": "ASH-BASETRAIN-GPU-70K-G207A5",
  "source_patch_id": "ASH-BASETRAIN-GPU-70K-G207A4",
  "step_index": 0,
  "training_loop_owner": "training.rs",
  "active_training_route": "FreshInit",
  "loss": 1.0,
  "grad_norm": 0.25,
  "delta_norm": 0.01,
  "learning_rate": 0.001,
  "step_digest": "nonempty",
  "input_batch_digest": "nonempty",
  "target_batch_digest": "nonempty",
  "before_weight_digest": "nonempty",
  "after_weight_digest": "nonempty",
  "optimizer_state_digest": "nonempty",
  "mutation_scope": "FreshInitTinyScoped",
  "replay_seed_policy": "SameAsSource",
  "batch_sequence_policy": "SameAsSource",
  "production_base_weight_mutated": false,
  "checkpoint_rewritten": false,
  "safetensors_rewritten": false
}
```

## Expected PASS Summary

```text
previous_g207a4_accepted=true
source_patch_id=ASH-BASETRAIN-GPU-70K-G207A4
phase=PhaseA
training_loop_owner=training.rs
active_training_route=FreshInit
same_seed_used=true
same_batch_sequence_policy_used=true
replay_mode=Deterministic
run_mode=BoundedMultiStep
source_step_count=8
replay_step_count=8
step_count_matched=true
source_ledger_schema=LossGradDeltaV1
replay_ledger_schema=LossGradDeltaV1
source_ledger_schema_matched=true
replay_ledger_schema_valid=true
ledger_shape_matched=true
ledger_required_fields_matched=true
replay_all_values_finite=true
replay_loss_first_recorded=true
replay_loss_last_recorded=true
replay_loss_first_greater_than_last=true
loss_direction_reproduced=true
digest_policy_matched=true
optimizer_continuity_policy_matched=true
all_replay_digests_nonempty=true
replay_digest_chain_contiguous=true
all_replay_optimizer_state_digests_nonempty=true
replay_optimizer_state_chain_contiguous=true
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
ready_for_g207a6=true
```

## Failure Conditions

```text
source_patch_id != ASH-BASETRAIN-GPU-70K-G207A4
phase != phase-a
active_route != freshinit
training_rs_route_required != true
source_loss_direction_required != true
source_ledger_required != true
source_ledger_schema != loss-grad-delta-v1
replay_mode != deterministic
replay_seed != same-as-source
batch_sequence_mode != same-as-source
run_mode != bounded-multi-step
step_count != 8
freshinit_forward_mode != execute
loss_mode != finite
backward_mode != execute
optimizer_step_mode != execute
weight_delta_mode != scoped
loss_direction_check != first-gt-last
ledger_compare_mode != same-shape
digest_compare_mode != same-policy
optimizer_continuity_compare_mode != same-policy
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
next_patch != ASH-BASETRAIN-GPU-70K-G207A6
```

Forbidden states:

```text
same_seed_used=false
same_batch_sequence_policy_used=false
step_count_matched=false
ledger_shape_matched=false
ledger_required_fields_matched=false
replay_ledger_schema_valid=false
replay_loss_first_greater_than_last=false
loss_direction_reproduced=false
digest_policy_matched=false
optimizer_continuity_policy_matched=false
nan_detected=true
inf_detected=true
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

- Implement as a deterministic replay gate.
- Owner must remain `training.rs`.
- Active route must remain `FreshInit`.
- Use same seed policy and same deterministic batch sequence policy.
- Use exactly 8 steps.
- Write replay ledger as JSONL, one row per step.
- Do not silently drop ledger rows.
- Do not silently add or remove required ledger fields.
- Do not silently coerce NaN or Inf to null.
- Exact numeric equality is not required in A5 unless bitwise deterministic math is explicitly sealed.
- A5 requires same shape, same policy, and reproduced loss direction.
- Do not use large serde JSON macro objects.
- Use `serde_json::Map` or explicit JSON atlas writer for large receipts.
- Do not add `recursion_limit` as a workaround.
- Do not mutate production base weights.
- Do not rewrite checkpoints or safetensors.
- Do not execute Atlas.
- Do not enable TensorCube 8x8.
- Invalid CLI enum values must fail closed.

## Next Patch

`ASH-BASETRAIN-GPU-70K-G207A6` should define numeric tolerance policy for replay value comparison and harden receipt comparison without claiming model quality or production readiness.
