# ASH-BASETRAIN-GPU-70K-G207A4

## Training.rs FreshInit Multi-Step Loss Direction Run / Loss First Greater Than Last / No Quality Claim

PatchId: `ASH-BASETRAIN-GPU-70K-G207A4`  
SourcePatchId: `ASH-BASETRAIN-GPU-70K-G207A3`  
NextPatchId: `ASH-BASETRAIN-GPU-70K-G207A5`  
RuntimePassTarget: `PASS_ASH_BASETRAIN_GPU_70K_G207A4_TRAINING_RS_FRESHINIT_MULTI_STEP_LOSS_DIRECTION_RUN_LOSS_FIRST_GT_LAST_NO_QUALITY_CLAIM`

## Purpose

G207A4 consumes the G207A3 digest-bound per-step ledger retention receipt and runs a bounded FreshInit multi-step training sequence through the `training.rs` active route.

This patch observes only whether `loss_first > loss_last` inside the bounded FreshInit smoke scope. It may write `bounded_loss_direction_observed=true` and `loss_first_greater_than_last=true`.

It must not claim training quality, model improvement, production readiness, deployment readiness, or broad convergence.

## Runtime Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g207a4_loss_direction_run -- `
  --local-root . `
  --out-dir artifacts `
  --source-patch-id ASH-BASETRAIN-GPU-70K-G207A3 `
  --phase phase-a `
  --active-route freshinit `
  --training-rs-route-required true `
  --source-ledger-required true `
  --source-ledger-schema loss-grad-delta-v1 `
  --run-mode bounded-multi-step `
  --step-count 8 `
  --tiny-batch-mode deterministic-sequence `
  --freshinit-forward-mode execute `
  --loss-mode finite `
  --backward-mode execute `
  --optimizer-step-mode execute `
  --weight-delta-mode scoped `
  --loss-direction-check first-gt-last `
  --digest-mode before-after-step-bound `
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
  --next-patch ASH-BASETRAIN-GPU-70K-G207A5
```

## Local Artifact Policy

The baked ZIP contains the Rust artifact writer and this spec. Runtime JSON/JSONL artifacts are not pre-baked and are not committed. The Rust binary writes them locally under `--out-dir`.

## Output Artifacts Written By Rust

```text
ASH_BASETRAIN_GPU_70K_G207A4_LOSS_DIRECTION_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G207A4_G207A3_SOURCE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A4_SOURCE_LEDGER_SCHEMA_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A4_MULTI_STEP_RUN_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A4_PER_STEP_LOSS_GRAD_DELTA_LEDGER.jsonl
ASH_BASETRAIN_GPU_70K_G207A4_LEDGER_SCHEMA_VALIDATION.json
ASH_BASETRAIN_GPU_70K_G207A4_FINITE_VALUE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A4_LOSS_FIRST_LAST_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A4_LOSS_DIRECTION_OBSERVATION.json
ASH_BASETRAIN_GPU_70K_G207A4_DIGEST_CONTINUITY_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A4_OPTIMIZER_CONTINUITY_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A4_SCOPED_WEIGHT_DELTA_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A4_NO_QUALITY_CLAIM_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A4_NO_PRODUCTION_COMMIT_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A4_NO_CHECKPOINT_REWRITE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A4_NO_SAFETENSORS_REWRITE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A4_ATLAS_DEFERRED_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A4_TENSORCUBE_DISABLED_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A4_NEXT_G207A5_ENTRY_PACKET.json
```

## Ledger Row Shape

```json
{
  "patch_id": "ASH-BASETRAIN-GPU-70K-G207A4",
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
  "production_base_weight_mutated": false,
  "checkpoint_rewritten": false,
  "safetensors_rewritten": false
}
```

## Expected PASS Summary

```text
previous_g207a3_accepted=true
source_patch_id=ASH-BASETRAIN-GPU-70K-G207A3
phase=PhaseA
training_loop_owner=training.rs
active_training_route=FreshInit
run_mode=BoundedMultiStep
step_count>=8
artifact_retention_enabled=true
no_artifacts_mode=false
per_step_ledger_created=true
ledger_schema=LossGradDeltaV1
ledger_row_count>=8
ledger_rows_contiguous=true
ledger_schema_valid=true
all_values_finite=true
loss_first_recorded=true
loss_last_recorded=true
loss_first_value_finite=true
loss_last_value_finite=true
loss_first_greater_than_last=true
bounded_loss_direction_observed=true
all_digests_nonempty=true
all_optimizer_state_digests_nonempty=true
digest_chain_contiguous=true
optimizer_state_chain_contiguous=true
at_least_one_before_after_digest_changed=true
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
ready_for_g207a5=true
```

## Failure Conditions

```text
source_patch_id != ASH-BASETRAIN-GPU-70K-G207A3
phase != phase-a
active_route != freshinit
training_rs_route_required != true
source_ledger_required != true
source_ledger_schema != loss-grad-delta-v1
run_mode != bounded-multi-step
step_count < 8
tiny_batch_mode != deterministic-sequence
freshinit_forward_mode != execute
loss_mode != finite
backward_mode != execute
optimizer_step_mode != execute
weight_delta_mode != scoped
loss_direction_check != first-gt-last
digest_mode != before-after-step-bound
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
next_patch != ASH-BASETRAIN-GPU-70K-G207A5
```

Forbidden states:

```text
loss_first_greater_than_last=false
bounded_loss_direction_observed=false
ledger_schema_valid=false
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

- Do not use large `serde_json::json!` macro objects.
- Use `serde_json::Map` or explicit JSON atlas writer for large receipts.
- Do not add `#![recursion_limit]`.
- Write ledger as JSONL, one row per step.
- Do not silently drop ledger rows.
- Do not silently coerce NaN or Inf to null.
- The only allowed direction check is `loss_first > loss_last`.
- Do not claim broad convergence, training quality, model improvement, production readiness, or deployment readiness.

## Next Patch

`ASH-BASETRAIN-GPU-70K-G207A5` should rerun the same deterministic seed and batch sequence, compare ledger schema, step digest chain, loss direction receipt, and optimizer continuity policy without claiming model quality or production readiness.
