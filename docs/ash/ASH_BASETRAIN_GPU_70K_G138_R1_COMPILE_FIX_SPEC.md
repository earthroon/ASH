# ASH-BASETRAIN-GPU-70K-G138-R1

## Bin Module Import Surface Rebind

PatchId: `ASH-BASETRAIN-GPU-70K-G138-R1`  
SourcePatchId: `ASH-BASETRAIN-GPU-70K-G138`

Seal: **Compile Fix Only / Runtime Contract Unchanged / No Base Weight Commit / No Checkpoint Mutation**

G138-R1 fixes the unresolved import caused by the G138 binary importing the module through the `base_train` crate root while the lightweight baked ZIP did not patch `lib.rs`.

## Error

```text
error[E0432]: unresolved import `base_train::ash_basetrain_gpu_70k_g138_optimizer_step_execution_quarantine`
```

## Root cause

The G138 module source file exists, but it was not exported from `base_train::lib.rs`. The binary therefore could not resolve the crate-root import.

## Fix

The binary now binds the sibling module directly:

```rust
#[path = "../ash_basetrain_gpu_70k_g138_optimizer_step_execution_quarantine.rs"]
mod ash_basetrain_gpu_70k_g138_optimizer_step_execution_quarantine;

use ash_basetrain_gpu_70k_g138_optimizer_step_execution_quarantine::run_from_env;
```

This avoids overwriting `lib.rs` and preserves the lightweight overlay contract.

## Runtime contract

Unchanged:

```text
PATCH_ID = ASH-BASETRAIN-GPU-70K-G138
PASS_ASH_BASETRAIN_GPU_70K_G138_OPTIMIZER_STEP_EXECUTION_QUARANTINE_NO_BASE_WEIGHT_COMMIT_NO_CHECKPOINT_MUTATION
```

## Run

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g138_optimizer_step_execution_quarantine -- `
  --local-root . `
  --out-dir artifacts `
  --source-patch-id ASH-BASETRAIN-GPU-70K-G137
```
