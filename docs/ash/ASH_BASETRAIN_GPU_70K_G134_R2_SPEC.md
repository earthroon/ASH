# ASH-BASETRAIN-GPU-70K-G134-R2

## Loss Tensor Retention Recheck

PatchId: `ASH-BASETRAIN-GPU-70K-G134-R2`  
SourcePatchId: `ASH-BASETRAIN-GPU-70K-G134-R1`  
PreviousPassTarget: `PASS_ASH_BASETRAIN_GPU_70K_G134_R1_LOSS_TENSOR_RETENTION_SURFACE_REBIND_NO_BACKWARD_NO_OPTIMIZER_NO_WEIGHT_COMMIT_NO_CHECKPOINT_MUTATION`

Seal: **No Backward / No Optimizer / No Weight Commit / No Checkpoint Mutation**

G134-R2 rechecks the G134-R1 retained loss tensor anchor in `training.rs` and decides whether G135 may run the first AtlasGroupedSequential backward smoke.

## Local artifact generation

The baked ZIP does not include generated G134-R2 artifacts. The Rust binary writes them locally:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g134_r2_loss_tensor_retention_recheck -- `
  --local-root . `
  --out-dir artifacts `
  --source-patch-id ASH-BASETRAIN-GPU-70K-G134-R1
```

## Input requirement

G134-R2 expects the G134-R1 artifacts under `--out-dir`, especially:

```text
ASH_BASETRAIN_GPU_70K_G134_R1_LOSS_TENSOR_RETENTION_SURFACE_REBIND_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G134_R1_RETAINED_LOSS_TENSOR_PACKET.json
ASH_BASETRAIN_GPU_70K_G134_R1_G134_R2_RECHECK_PACKET.json
```

## Static anchors

```text
ash_g134_r1_retained_loss_tensor_for_backward_smoke
ash_g134_r1_loss_scalar_for_receipt
ash_g134_r1_scalar_receipt_readback_from_loss_clone
```

The retained tensor anchor must appear before scalar receipt readback. Scalar logging must consume a clone/read-only boundary, not the original loss.

## Output artifacts

```text
ASH_BASETRAIN_GPU_70K_G134_R2_LOSS_TENSOR_RETENTION_RECHECK_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G134_R2_RETAINED_LOSS_TENSOR_STATIC_ANCHOR_AUDIT.json
ASH_BASETRAIN_GPU_70K_G134_R2_SCALAR_BOUNDARY_RECHECK_AUDIT.json
ASH_BASETRAIN_GPU_70K_G134_R2_G135_BACKWARD_SMOKE_TARGET_PACKET.json
ASH_BASETRAIN_GPU_70K_G134_R2_NO_MUTATION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G134_R2_FORBIDDEN_CALL_AUDIT.json
ASH_BASETRAIN_GPU_70K_G134_R2_NEXT_PATCH_PACKET.json
```

## PASS target

```text
PASS_ASH_BASETRAIN_GPU_70K_G134_R2_LOSS_TENSOR_RETENTION_RECHECK_TO_G135_BACKWARD_SMOKE_TARGET_NO_BACKWARD_NO_OPTIMIZER_NO_WEIGHT_COMMIT_NO_CHECKPOINT_MUTATION
```

Expected summary:

```text
verdict=Pass
previous_g134_r1_accepted=true
route=AtlasGroupedSequentialBackwardCandidate
retained_loss_tensor_symbol_found=true
retained_loss_tensor_before_scalar_readback=true
scalar_logging_symbol_found=true
scalar_logging_consumes_clone=true
scalar_logging_consumes_original_loss=false
detach_severity=Low
retention_recheck_verdict=LossTensorRetainedForG135BackwardSmoke
g135_backward_smoke_target_packet_created=true
backward_allowed_in_g135=true
output_files_written=7
```

## Next patch

If G134-R2 passes, proceed to `ASH-BASETRAIN-GPU-70K-G135` for AtlasGroupedSequential backward smoke. G135 may call backward, but optimizer, weight commit, and checkpoint mutation remain forbidden.
