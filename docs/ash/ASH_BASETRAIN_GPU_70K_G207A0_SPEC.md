# ASH-BASETRAIN-GPU-70K-G207A0

## Phase A FreshInit Active Route Preflight / G167 To Training.rs Execution Boundary / No Runtime Mutation

PatchId: `ASH-BASETRAIN-GPU-70K-G207A0`  
SourcePatchId: `ASH-BASETRAIN-GPU-70K-G207-SSOT`  
NextPatchId: `ASH-BASETRAIN-GPU-70K-G207A1`  
RuntimePassTarget: `PASS_ASH_BASETRAIN_GPU_70K_G207A0_PHASE_A_FRESHINIT_ACTIVE_ROUTE_PREFLIGHT_G167_TO_TRAINING_RS_EXECUTION_BOUNDARY_NO_RUNTIME_MUTATION`

## Purpose

G207A0 consumes the G207-SSOT PASS boundary and creates the first Phase A preflight packet. It binds G167 FreshInit scoped proof as source evidence only, declares the `training.rs` execution boundary, declares FreshInit as the Phase A active route target, keeps Atlas deferred, keeps TensorCube 8x8 disabled, and drafts the Phase A loss/grad/delta ledger schema.

This patch does not execute training, backward, optimizer step, gradient mutation, weight delta commit, checkpoint rewrite, safetensors rewrite, route pointer rewrite, atlas reopen, TensorCube enable, production claim, or deployment claim.

## Runtime Command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g207a0_phase_a_freshinit_active_route_preflight -- `
  --local-root . `
  --out-dir artifacts `
  --source-patch-id ASH-BASETRAIN-GPU-70K-G207-SSOT `
  --phase phase-a `
  --preflight-mode freshinit-active-route `
  --freshinit-source-patch-id ASH-BASETRAIN-GPU-70K-G167 `
  --training-rs-boundary declare `
  --active-route-target freshinit `
  --atlas-route-mode defer `
  --tensorcube-mode keep-disabled `
  --ledger-schema-mode draft `
  --training-execution-mode forbid `
  --runtime-mutation-mode forbid `
  --production-claim-mode forbid `
  --next-patch ASH-BASETRAIN-GPU-70K-G207A1
```

## Local Artifact Policy

The baked ZIP contains the Rust artifact writer and this spec. Runtime JSON artifacts are not pre-baked and are not committed. The Rust binary writes them locally under `--out-dir`.

## Output Artifacts Written By Rust

```text
ASH_BASETRAIN_GPU_70K_G207A0_PHASE_A_PREFLIGHT_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G207A0_G207_SSOT_SOURCE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A0_G167_FRESHINIT_SOURCE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A0_TRAINING_RS_EXECUTION_BOUNDARY.json
ASH_BASETRAIN_GPU_70K_G207A0_ACTIVE_ROUTE_TARGET_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A0_ATLAS_DEFERRED_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A0_TENSORCUBE_DISABLED_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A0_PHASE_A_LEDGER_SCHEMA_DRAFT.json
ASH_BASETRAIN_GPU_70K_G207A0_NO_RUNTIME_MUTATION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A0_NO_TRAINING_CLAIM_AUDIT.json
ASH_BASETRAIN_GPU_70K_G207A0_NEXT_G207A1_ENTRY_PACKET.json
```

## Expected PASS Summary

```text
previous_g207_ssot_accepted=true
source_patch_id=ASH-BASETRAIN-GPU-70K-G207-SSOT
phase=PhaseA
preflight_mode=FreshInitActiveRoute
phase_a_preflight_created=true
g207_ssot_source_audit_created=true
g167_freshinit_source_audit_created=true
training_rs_execution_boundary_created=true
active_route_target_audit_created=true
atlas_deferred_audit_created=true
tensorcube_disabled_audit_created=true
phase_a_ledger_schema_draft_created=true
no_runtime_mutation_audit_created=true
no_training_claim_audit_created=true
next_g207a1_entry_packet_created=true
source_ready_for_phase_a0=true
g167_freshinit_source_bound=true
freshinit_source_scope=Scoped
freshinit_source_promoted_to_training_result=false
training_rs_execution_boundary_declared=true
training_rs_active_route_bound=false
active_route_target=FreshInit
freshinit_route_bound_in_training_rs=false
atlas_route_deferred=true
tensorcube_8x8_kept_disabled=true
ledger_field_step_index_declared=true
ledger_field_loss_declared=true
ledger_field_grad_norm_declared=true
ledger_field_delta_norm_declared=true
ledger_field_learning_rate_declared=true
ledger_field_step_digest_declared=true
ledger_field_before_weight_digest_declared=true
ledger_field_after_weight_digest_declared=true
ledger_runtime_rows_written=false
runtime_training_executed=false
loss_computed_as_training_result=false
loss_backward_executed=false
optimizer_step_executed=false
gradient_mutated=false
weight_delta_committed=false
checkpoint_rewritten=false
safetensors_rewritten=false
route_pointer_rewritten=false
production_claimed=false
deployment_ready_claimed=false
ready_for_g207a1=true
```

## Failure Conditions

```text
source_patch_id != ASH-BASETRAIN-GPU-70K-G207-SSOT
phase != phase-a
preflight_mode != freshinit-active-route
freshinit_source_patch_id != ASH-BASETRAIN-GPU-70K-G167
training_rs_boundary != declare
active_route_target != freshinit
atlas_route_mode != defer
tensorcube_mode != keep-disabled
ledger_schema_mode != draft
training_execution_mode != forbid
runtime_mutation_mode != forbid
production_claim_mode != forbid
next_patch != ASH-BASETRAIN-GPU-70K-G207A1
```

The following states are forbidden by contract and must remain false:

```text
runtime_training_executed
loss_computed_as_training_result
loss_backward_executed
optimizer_step_executed
gradient_mutated
weight_delta_committed
checkpoint_rewritten
safetensors_rewritten
route_pointer_rewritten
production_claimed
deployment_ready_claimed
training_quality_claimed
model_improvement_claimed
atlas_route_reopened
atlas_backward_executed
tensorcube_matmul_replacement_enabled
freshinit_route_bound_in_training_rs
```

## Implementation Surface

```text
crates/base_train/src/bin/ash_basetrain_gpu_70k_g207a0_phase_a_freshinit_active_route_preflight.rs
specs/ASH_BASETRAIN_GPU_70K_G207A0_SPEC.md
specs/ASH_BASETRAIN_GPU_70K_G207A0_BAKE_MANIFEST.json
specs/ASH_BASETRAIN_GPU_70K_G207A0_LOCAL_BAKE_VALIDATION.json
specs/ASH_BASETRAIN_GPU_70K_G207A0_STATIC_CHECKS.json
```

## Next Patch

`ASH-BASETRAIN-GPU-70K-G207A1` should bind FreshInit as the active route in `training.rs`, create route seal and no-silent-fallback audits, keep Atlas deferred, keep TensorCube disabled, and still avoid backward, optimizer step, and runtime training mutation.
