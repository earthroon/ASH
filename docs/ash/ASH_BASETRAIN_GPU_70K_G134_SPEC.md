# ASH-BASETRAIN-GPU-70K-G134

## AtlasGroupedSequential Loss Tensor Backward Reachability Probe

PatchId: `ASH-BASETRAIN-GPU-70K-G134`  
SourcePatchId: `ASH-BASETRAIN-GPU-70K-G133`  
PreviousPassTarget: `PASS_ASH_BASETRAIN_GPU_70K_G133_ACTIVE_TRAINING_ROUTE_DECISION_GATE_NO_BACKWARD_NO_OPTIMIZER_NO_WEIGHT_COMMIT_NO_CHECKPOINT_MUTATION`

Seal: **No Backward / No Optimizer / No Weight Commit / No Checkpoint Mutation**

G134 statically audits the `AtlasGroupedSequentialBackwardCandidate` route selected by G133. It checks whether the loss surface remains a backward-reachable Burn tensor candidate or is consumed by scalar readback before G135.

## Local artifact generation

The baked ZIP does not include generated G134 artifacts. The Rust binary writes them locally:

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g134_atlas_grouped_loss_tensor_backward_reachability_probe -- `
  --local-root . `
  --out-dir artifacts `
  --source-patch-id ASH-BASETRAIN-GPU-70K-G133
```

## Input requirement

G134 expects the G133 artifacts under `--out-dir`, especially:

```text
ASH_BASETRAIN_GPU_70K_G133_ACTIVE_TRAINING_ROUTE_DECISION_GATE_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G133_ROUTE_OWNERSHIP_DECISION.json
ASH_BASETRAIN_GPU_70K_G133_BACKWARD_PROBE_OWNERSHIP_PACKET.json
```

## Output artifacts

```text
ASH_BASETRAIN_GPU_70K_G134_ATLAS_GROUPED_LOSS_TENSOR_BACKWARD_REACHABILITY_PROBE_RECEIPT.json
ASH_BASETRAIN_GPU_70K_G134_LOSS_TENSOR_REACHABILITY_REPORT.json
ASH_BASETRAIN_GPU_70K_G134_SCALAR_DETACH_BOUNDARY_AUDIT.json
ASH_BASETRAIN_GPU_70K_G134_ATLAS_GROUPED_BRANCH_SURFACE_AUDIT.json
ASH_BASETRAIN_GPU_70K_G134_G135_BACKWARD_SMOKE_TARGET_PACKET.json
ASH_BASETRAIN_GPU_70K_G134_FALLBACK_ROUTE_CONSTRAINT_AUDIT.json
ASH_BASETRAIN_GPU_70K_G134_NO_MUTATION_AUDIT.json
ASH_BASETRAIN_GPU_70K_G134_FORBIDDEN_CALL_AUDIT.json
ASH_BASETRAIN_GPU_70K_G134_NEXT_PATCH_PACKET.json
```

## Expected pass target

```text
PASS_ASH_BASETRAIN_GPU_70K_G134_ATLAS_GROUPED_LOSS_TENSOR_BACKWARD_REACHABILITY_PROBE_NO_BACKWARD_NO_OPTIMIZER_NO_WEIGHT_COMMIT_NO_CHECKPOINT_MUTATION
```

Expected successful summary:

```text
verdict=Pass
previous_g133_accepted=true
primary_training_route=AtlasGroupedSequentialBackwardCandidate
fallback_training_route=FreshInitTinyLoopRegressionOnly
atlas_grouped_branch_found=true
loss_tensor_candidate_found=true
detach_boundary_found=true
detach_severity=Low
loss_tensor_reachability_verdict=LossTensorReachableForBackwardSmoke
g135_backward_smoke_target_packet_created=true
backward_allowed_in_g135=true
output_files_written=9
```

## Detach rule

`loss.clone().inner()` is classified as Low severity scalar logging/readback because it does not consume the retained loss tensor. A consuming `loss.inner()` boundary before the backward candidate blocks G135 and routes to G134-R1.

## Next patch

If reachable: `ASH-BASETRAIN-GPU-70K-G135` performs a backward smoke with no optimizer and no commit.  
If detached: `ASH-BASETRAIN-GPU-70K-G134-R1` repairs loss tensor retention before scalar receipt readback.
