# ASH-BASETRAIN-GPU-70K-G207A2

## Training.rs Active FreshInit Backward Optimizer Smoke / Scoped Weight Delta / No Production Commit

PatchId: `ASH-BASETRAIN-GPU-70K-G207A2`  
SourcePatchId: `ASH-BASETRAIN-GPU-70K-G207A1`  
NextPatchId: `ASH-BASETRAIN-GPU-70K-G207A3`  
RuntimePassTarget: `PASS_ASH_BASETRAIN_GPU_70K_G207A2_TRAINING_RS_ACTIVE_FRESHINIT_BACKWARD_OPTIMIZER_SMOKE_SCOPED_WEIGHT_DELTA_NO_PRODUCTION_COMMIT`

## Purpose

G207A2 consumes the G207A1 FreshInit route bind receipt and executes the first active FreshInit backward/optimizer smoke inside the `training.rs` active route.

This patch is the first Phase A runtime execution patch. It may execute FreshInit tiny batch creation, FreshInit forward, finite loss computation, loss backward, optimizer step, and scoped weight delta. It must not mutate production base weights, rewrite checkpoints, rewrite safetensors, rewrite route pointers, execute Atlas, enable TensorCube 8x8, claim training quality, or claim deployment readiness.

## Runtime Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g207a2_active_freshinit_backward_optimizer_smoke -- `
  --local-root . `
  --out-dir artifacts `
  --source-patch-id ASH-BASETRAIN-GPU-70K-G207A1 `
  --phase phase-a `
  --active-route freshinit `
  --training-rs-route-required true `
  --tiny-batch-mode deterministic `
  --freshinit-forward-mode execute `
  --loss-mode finite `
  --backward-mode execute `
  --optimizer-step-mode execute `
  --weight-delta-mode scoped `
  --production-commit-mode forbid `
  --checkpoint-write-mode forbid `
  --safetensors-write-mode forbid `
  --route-pointer-write-mode forbid `
  --atlas-route-mode defer `
  --tensorcube-mode keep-disabled `
  --training-quality-claim-mode forbid `
  --deployment-ready-mode forbid `
  --next-patch ASH-BASETRAIN-GPU-70K-G207A3
```

## Local Artifact Policy

The baked ZIP contains the Rust artifact writer and this spec. Runtime JSON artifacts are not pre-baked and are not committed. The Rust binary writes them locally under `--out-dir`.

## Output Artifacts Written By Rust

```text
ASH_BASETRAIN_GPU_70K_G207A2_ACTIVE_BACKWARD_OPTIMIZER_SMOKE_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G207A2_G207A1_SOURCE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A2_TRAINING_RS_ACTIVE_ROUTE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A2_TINY_BATCH_DIGEST_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A2_FRESHINIT_FORWARD_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A2_LOSS_COMPUTE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A2_LOSS_BACKWARD_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A2_OPTIMIZER_STEP_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A2_SCOPED_WEIGHT_DELTA_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A2_NO_PRODUCTION_COMMIT_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A2_NO_CHECKPOINT_REWRITE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A2_NO_SAFETENSORS_REWRITE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A2_ATLAS_DEFERRED_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A2_TENSORCUBE_DISABLED_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A2_NO_TRAINING_QUALITY_CLAIM_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A2_NEXT_G207A3_ENTRY_PACKET.json
```

## Expected PASS Summary

```text
previous_g207a1_accepted=true
source_patch_id=ASH-BASETRAIN-GPU-70K-G207A1
phase=PhaseA
training_loop_owner=training.rs
active_training_route=FreshInit
active_backward_optimizer_smoke_receipt_created=true
g207a1_source_audit_created=true
training_rs_active_route_audit_created=true
tiny_batch_digest_audit_created=true
freshinit_forward_audit_created=true
loss_compute_audit_created=true
loss_backward_audit_created=true
optimizer_step_audit_created=true
scoped_weight_delta_audit_created=true
no_production_commit_audit_created=true
no_checkpoint_rewrite_audit_created=true
no_safetensors_rewrite_audit_created=true
atlas_deferred_audit_created=true
tensorcube_disabled_audit_created=true
no_training_quality_claim_audit_created=true
next_g207a3_entry_packet_created=true
runtime_training_smoke_attempted=true
runtime_training_executed=true
tiny_batch_created=true
tiny_batch_mode=Deterministic
freshinit_forward_executed=true
loss_computed_as_training_result=true
loss_value_finite=true
loss_backward_executed=true
optimizer_step_executed=true
gradient_mutated=true
scoped_weight_delta_applied=true
at_least_one_scoped_delta_nonzero=true
scoped_weight_before_digest_nonempty=true
scoped_weight_after_digest_nonempty=true
scoped_weight_digest_changed=true
production_base_weight_mutated=false
checkpoint_rewritten=false
safetensors_rewritten=false
route_pointer_rewritten=false
production_claimed=false
deployment_ready_claimed=false
training_quality_claimed=false
model_improvement_claimed=false
loss_trend_claimed=false
atlas_route_executed=false
atlas_grouped_route_deferred=true
atlas_backward_executed=false
atlas_optimizer_step_executed=false
tensorcube_8x8_kept_disabled=true
tensorcube_matmul_replacement_enabled=false
ready_for_g207a3=true
```

## Failure Conditions

```text
source_patch_id != ASH-BASETRAIN-GPU-70K-G207A1
phase != phase-a
active_route != freshinit
training_rs_route_required != true
tiny_batch_mode != deterministic
freshinit_forward_mode != execute
loss_mode != finite
backward_mode != execute
optimizer_step_mode != execute
weight_delta_mode != scoped
production_commit_mode != forbid
checkpoint_write_mode != forbid
safetensors_write_mode != forbid
route_pointer_write_mode != forbid
atlas_route_mode != defer
tensorcube_mode != keep-disabled
training_quality_claim_mode != forbid
deployment_ready_mode != forbid
next_patch != ASH-BASETRAIN-GPU-70K-G207A3
```

The following states are forbidden by contract and must remain false:

```text
production_base_weight_mutated
checkpoint_rewritten
safetensors_rewritten
route_pointer_rewritten
production_route_pointer_rewritten
production_claimed
deployment_ready_claimed
training_quality_claimed
model_improvement_claimed
loss_trend_claimed
atlas_route_executed
atlas_route_reopened
atlas_backward_executed
atlas_optimizer_step_executed
tensorcube_matmul_replacement_enabled
```

## Implementation Surface

```text
crates/base_train/src/bin/ash_basetrain_gpu_70k_g207a2_active_freshinit_backward_optimizer_smoke.rs
specs/ASH_BASETRAIN_GPU_70K_G207A2_SPEC.md
specs/ASH_BASETRAIN_GPU_70K_G207A2_BAKE_MANIFEST.json
specs/ASH_BASETRAIN_GPU_70K_G207A2_LOCAL_BAKE_VALIDATION.json
specs/ASH_BASETRAIN_GPU_70K_G207A2_STATIC_CHECKS.json
```

## Next Patch

`ASH-BASETRAIN-GPU-70K-G207A3` should retain per-step loss, grad norm, delta norm, learning rate, step digest, before/after weight digest, and artifact retention receipts without claiming training quality or loss trend.
