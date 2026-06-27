# ASH-BASETRAIN-GPU-70K-G207A3

## Per-Step Loss Grad Delta Ledger Retention / No Artifacts Strip / Digest Bound Training Receipt

PatchId: `ASH-BASETRAIN-GPU-70K-G207A3`  
SourcePatchId: `ASH-BASETRAIN-GPU-70K-G207A2`  
NextPatchId: `ASH-BASETRAIN-GPU-70K-G207A4`  
RuntimePassTarget: `PASS_ASH_BASETRAIN_GPU_70K_G207A3_PER_STEP_LOSS_GRAD_DELTA_LEDGER_RETENTION_NO_ARTIFACTS_STRIP_DIGEST_BOUND_TRAINING_RECEIPT`

## Purpose

G207A3 consumes the G207A2 active FreshInit backward/optimizer smoke receipt and enables durable artifact retention for the Phase A training proof line.

This patch writes a per-step JSONL ledger containing loss, grad norm, delta norm, learning rate, step digest, input/target batch digests, and before/after scoped weight digests.

A3 proves retention and digest-bound reproducibility surface. It does not prove loss decrease, training quality, model improvement, production readiness, or deployment readiness.

## Runtime Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g207a3_per_step_ledger_retention -- `
  --local-root . `
  --out-dir artifacts `
  --source-patch-id ASH-BASETRAIN-GPU-70K-G207A2 `
  --phase phase-a `
  --active-route freshinit `
  --training-rs-route-required true `
  --artifact-retention-mode enable `
  --no-artifacts-mode forbid `
  --ledger-mode per-step-jsonl `
  --ledger-schema loss-grad-delta-v1 `
  --step-count 4 `
  --tiny-batch-mode deterministic `
  --freshinit-forward-mode execute `
  --loss-mode finite `
  --backward-mode execute `
  --optimizer-step-mode execute `
  --weight-delta-mode scoped `
  --digest-mode before-after-step-bound `
  --production-commit-mode forbid `
  --checkpoint-write-mode forbid `
  --safetensors-write-mode forbid `
  --route-pointer-write-mode forbid `
  --atlas-route-mode defer `
  --tensorcube-mode keep-disabled `
  --loss-trend-claim-mode forbid `
  --training-quality-claim-mode forbid `
  --deployment-ready-mode forbid `
  --next-patch ASH-BASETRAIN-GPU-70K-G207A4
```

## Local Artifact Policy

The baked ZIP contains the Rust artifact writer and this spec. Runtime JSON/JSONL artifacts are not pre-baked and are not committed. The Rust binary writes them locally under `--out-dir`.

## Output Artifacts Written By Rust

```text
ASH_BASETRAIN_GPU_70K_G207A3_LEDGER_RETENTION_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G207A3_G207A2_SOURCE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A3_ARTIFACT_RETENTION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A3_NO_ARTIFACTS_STRIP_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A3_PER_STEP_LOSS_GRAD_DELTA_LEDGER.jsonl
ASH_BASETRAIN_GPU_70K_G207A3_LEDGER_SCHEMA_VALIDATION.json
ASH_BASETRAIN_GPU_70K_G207A3_FINITE_VALUE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A3_DIGEST_CONTINUITY_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A3_SCOPED_WEIGHT_DELTA_RETENTION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A3_NO_PRODUCTION_COMMIT_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A3_NO_CHECKPOINT_REWRITE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A3_NO_SAFETENSORS_REWRITE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A3_ATLAS_DEFERRED_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A3_TENSORCUBE_DISABLED_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A3_NO_LOSS_TREND_CLAIM_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A3_NO_TRAINING_QUALITY_CLAIM_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A3_NEXT_G207A4_ENTRY_PACKET.json
```

## Ledger Row Shape

```json
{
  "patch_id": "ASH-BASETRAIN-GPU-70K-G207A3",
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
  "mutation_scope": "FreshInitTinyScoped",
  "production_base_weight_mutated": false,
  "checkpoint_rewritten": false,
  "safetensors_rewritten": false
}
```

## Expected PASS Summary

```text
previous_g207a2_accepted=true
source_patch_id=ASH-BASETRAIN-GPU-70K-G207A2
phase=PhaseA
training_loop_owner=training.rs
active_training_route=FreshInit
artifact_retention_enabled=true
no_artifacts_mode=false
artifact_strip_detected=false
per_step_ledger_created=true
ledger_mode=PerStepJsonl
ledger_schema=LossGradDeltaV1
ledger_row_count>=4
ledger_rows_contiguous=true
ledger_schema_valid=true
loss_values_written=true
grad_norm_values_written=true
delta_norm_values_written=true
learning_rate_values_written=true
step_digest_values_written=true
input_batch_digest_values_written=true
target_batch_digest_values_written=true
before_weight_digest_values_written=true
after_weight_digest_values_written=true
all_values_finite=true
all_digests_nonempty=true
at_least_one_before_after_digest_changed=true
production_base_weight_mutated=false
checkpoint_rewritten=false
safetensors_rewritten=false
route_pointer_rewritten=false
loss_trend_claimed=false
loss_decrease_claimed=false
training_quality_claimed=false
model_improvement_claimed=false
atlas_route_executed=false
atlas_grouped_route_deferred=true
tensorcube_8x8_kept_disabled=true
tensorcube_matmul_replacement_enabled=false
ready_for_g207a4=true
```

## Failure Conditions

```text
source_patch_id != ASH-BASETRAIN-GPU-70K-G207A2
phase != phase-a
active_route != freshinit
training_rs_route_required != true
artifact_retention_mode != enable
no_artifacts_mode != forbid
ledger_mode != per-step-jsonl
ledger_schema != loss-grad-delta-v1
step_count < 4
tiny_batch_mode != deterministic
freshinit_forward_mode != execute
loss_mode != finite
backward_mode != execute
optimizer_step_mode != execute
weight_delta_mode != scoped
digest_mode != before-after-step-bound
production_commit_mode != forbid
checkpoint_write_mode != forbid
safetensors_write_mode != forbid
route_pointer_write_mode != forbid
atlas_route_mode != defer
tensorcube_mode != keep-disabled
loss_trend_claim_mode != forbid
training_quality_claim_mode != forbid
deployment_ready_mode != forbid
next_patch != ASH-BASETRAIN-GPU-70K-G207A4
```

Forbidden states:

```text
artifact_strip_detected=true
no_artifacts_mode=true
per_step_ledger_created=false
ledger_schema_valid=false
nan_detected=true
inf_detected=true
loss_trend_claimed=true
loss_decrease_claimed=true
training_quality_claimed=true
model_improvement_claimed=true
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
- Do not add `#![recursion_limit]` as a workaround.
- Write ledger as JSONL, one row per step.
- Do not silently drop ledger rows.
- Do not silently coerce NaN or Inf to null.
- Loss direction is deferred to G207A4.

## Next Patch

`ASH-BASETRAIN-GPU-70K-G207A4` should run a longer bounded FreshInit sequence, consume the retained ledger schema, validate finite per-step values, check `loss_first > loss_last`, and still avoid training quality, production, or deployment claims.
