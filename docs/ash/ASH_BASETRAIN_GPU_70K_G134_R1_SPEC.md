# ASH-BASETRAIN-GPU-70K-G134-R1

## Loss Tensor Retention Surface Rebind

PatchId: `ASH-BASETRAIN-GPU-70K-G134-R1`  
SourcePatchId: `ASH-BASETRAIN-GPU-70K-G134`  
PreviousBlockedTarget: `BLOCKED_ASH_BASETRAIN_GPU_70K_G134_LOSS_DETACHED_BEFORE_BACKWARD`

Seal: **No Backward / No Optimizer / No Weight Commit / No Checkpoint Mutation**

G134-R1 repairs the G134 loss-detach block by adding an explicit retained loss tensor static anchor before scalar receipt readback in `crates/base_train/src/training.rs`.

## Code rebind

The patch adds and audits this anchor family:

```text
ash_g134_r1_retained_loss_tensor_for_backward_smoke
ash_g134_r1_loss_scalar_for_receipt
ash_g134_r1_scalar_receipt_readback_from_loss_clone
```

Required shape:

```rust
let ash_g134_r1_retained_loss_tensor_for_backward_smoke = loss.clone();
let ash_g134_r1_loss_scalar_for_receipt =
    ash_g134_r1_scalar_receipt_readback_from_loss_clone(loss.clone());
```

The retained tensor is for the later G135 backward smoke target. G134-R1 itself does not call backward or optimizer.

## Local artifact generation

The baked ZIP does not include generated G134-R1 artifacts. The Rust binary writes them locally:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g134_r1_loss_tensor_retention_surface_rebind -- `
  --local-root . `
  --out-dir artifacts `
  --source-patch-id ASH-BASETRAIN-GPU-70K-G134
```

## Output artifacts

```text
ASH_BASETRAIN_GPU_70K_G134_R1_LOSS_TENSOR_RETENTION_SURFACE_REBIND_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G134_R1_RETENTION_SURFACE_PATCH_PLAN.json
ASH_BASETRAIN_GPU_70K_G134_R1_SCALAR_LOGGING_BOUNDARY_REBIND_AUDIT.json
ASH_BASETRAIN_GPU_70K_G134_R1_RETAINED_LOSS_TENSOR_PACKET.json
ASH_BASETRAIN_GPU_70K_G134_R1_G134_R2_RECHECK_PACKET.json
ASH_BASETRAIN_GPU_70K_G134_R1_NO_MUTATION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G134_R1_FORBIDDEN_CALL_AUDIT.json
ASH_BASETRAIN_GPU_70K_G134_R1_NEXT_PATCH_PACKET.json
```

## PASS target

```text
PASS_ASH_BASETRAIN_GPU_70K_G134_R1_LOSS_TENSOR_RETENTION_SURFACE_REBIND_NO_BACKWARD_NO_OPTIMIZER_NO_WEIGHT_COMMIT_NO_CHECKPOINT_MUTATION
```

Expected summary:

```text
verdict=Pass
previous_g134_accepted_block=true
previous_blocked_reason_code=LOSS_DETACHED_BEFORE_BACKWARD
route=AtlasGroupedSequentialBackwardCandidate
retained_loss_tensor_symbol_found=true
retained_loss_tensor_before_scalar_readback=true
scalar_logging_symbol_found=true
scalar_logging_consumes_clone=true
scalar_logging_consumes_original_loss=false
detach_severity_after_rebind=Low
retained_loss_tensor_packet_created=true
g134_r2_recheck_packet_created=true
output_files_written=8
```

## Next patch

`ASH-BASETRAIN-GPU-70K-G134-R2` rechecks the retained loss tensor anchor and must still avoid backward, optimizer, weight commit, and checkpoint mutation.
