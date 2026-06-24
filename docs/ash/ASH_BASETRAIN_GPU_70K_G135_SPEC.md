# ASH-BASETRAIN-GPU-70K-G135

## AtlasGroupedSequential Backward Execution Gate

PatchId: `ASH-BASETRAIN-GPU-70K-G135`  
SourcePatchId: `ASH-BASETRAIN-GPU-70K-G134-R2`  
PreviousPassTarget: `PASS_ASH_BASETRAIN_GPU_70K_G134_R2_LOSS_TENSOR_RETENTION_RECHECK_TO_G135_BACKWARD_SMOKE_TARGET_NO_BACKWARD_NO_OPTIMIZER_NO_WEIGHT_COMMIT_NO_CHECKPOINT_MUTATION`

Seal: **Backward Allowed / No Optimizer / No Weight Commit / No Checkpoint Mutation**

G135 removes smoke terminology from its own patch name, status, and output artifacts. It still accepts G134-R2 input artifacts whose filenames or legacy pass string contain `SMOKE` for compatibility.

## Implemented execution gate

G135 adds a backward execution gate inside the AtlasGroupedSequential branch in `crates/base_train/src/training.rs`:

```rust
let ash_g135_retained_loss_tensor_for_backward_execution =
    ash_g134_r1_retained_loss_tensor_for_backward_smoke.clone();
let ash_g135_backward_gradients =
    ash_g135_retained_loss_tensor_for_backward_execution.backward();
let _ash_g135_backward_gradient_observation = &ash_g135_backward_gradients;
```

This backward execution is allowed. Optimizer construction, optimizer step, weight commit, checkpoint write, checkpoint mutation, runtime promotion, and training completion claim remain forbidden.

## Local artifact generation

The baked ZIP does not include generated G135 artifacts. The Rust binary writes them locally:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g135_atlas_grouped_backward_execution_gate -- `
  --local-root . `
  --out-dir artifacts `
  --source-patch-id ASH-BASETRAIN-GPU-70K-G134-R2
```

## Output artifacts

```text
ASH_BASETRAIN_GPU_70K_G135_ATLAS_GROUPED_BACKWARD_EXECUTION_GATE_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G135_RETAINED_LOSS_BACKWARD_EXECUTION_REPORT.json
ASH_BASETRAIN_GPU_70K_G135_GRADIENT_OBSERVATION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G135_OPTIMIZER_BLOCK_AUDIT.json
ASH_BASETRAIN_GPU_70K_G135_WEIGHT_MUTATION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G135_CHECKPOINT_MUTATION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G135_FORBIDDEN_CALL_AUDIT.json
ASH_BASETRAIN_GPU_70K_G135_NEXT_PATCH_PACKET.json
```

## PASS target

```text
PASS_ASH_BASETRAIN_GPU_70K_G135_ATLAS_GROUPED_BACKWARD_EXECUTION_GATE_NO_OPTIMIZER_NO_WEIGHT_COMMIT_NO_CHECKPOINT_MUTATION
```

Expected summary:

```text
verdict=Pass
previous_g134_r2_accepted=true
route=AtlasGroupedSequentialBackwardCandidate
retained_loss_tensor_target_found=true
backward_executed=true
backward_execution_verdict=BackwardExecutedNoMutation
gradient_observation_available=true
optimizer_step_executed=false
optimizer_adapter_created=false
weight_digest_unchanged=true
actual_weight_mutated=false
checkpoint_written=false
checkpoint_mutated=false
runtime_route_promoted=false
training_completion_claimed=false
output_files_written=8
```

## Next patch

`ASH-BASETRAIN-GPU-70K-G136` binds the observed gradient container to an optimizer candidate surface without running optimizer step, without weight commit, and without checkpoint mutation.
