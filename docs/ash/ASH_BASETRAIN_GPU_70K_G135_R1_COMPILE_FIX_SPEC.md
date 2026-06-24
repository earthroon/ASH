# ASH-BASETRAIN-GPU-70K-G135-R1

## Backward Execution Gate Compile Exhaustiveness Fix

PatchId: `ASH-BASETRAIN-GPU-70K-G135-R1`  
SourcePatchId: `ASH-BASETRAIN-GPU-70K-G135`

Seal: **No Runtime Contract Drift / No Optimizer / No Weight Commit / No Checkpoint Mutation**

G135-R1 fixes the G135 compile failure caused by Rust match exhaustiveness with a guarded `forbidden_count > 0` arm.

## Error

```text
error[E0004]: non-exhaustive patterns:
(true, true, true, true, true, true, true, 1_u64..=u64::MAX) not covered
```

## Root cause

The original `classify_backward_execution` arm used a guard:

```rust
(true, true, true, true, true, true, true, count) if count > 0 =>
    BackwardExecutionVerdict::OptimizerCallDetected,
```

Rust exhaustiveness checking does not treat guarded arms as full coverage.

## Fix

The guarded arm is replaced by an explicit range pattern:

```rust
(true, true, true, true, true, true, true, 1..=u64::MAX) =>
    BackwardExecutionVerdict::OptimizerCallDetected,
```

The zero case remains:

```rust
(true, true, true, true, true, true, true, 0) =>
    BackwardExecutionVerdict::BackwardExecutedNoMutation,
```

## Runtime contract

This is a compile-only fix. Runtime `PATCH_ID`, binary name, output artifact names, and G135 PASS target remain unchanged:

```text
PASS_ASH_BASETRAIN_GPU_70K_G135_ATLAS_GROUPED_BACKWARD_EXECUTION_GATE_NO_OPTIMIZER_NO_WEIGHT_COMMIT_NO_CHECKPOINT_MUTATION
```

## Local run

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g135_atlas_grouped_backward_execution_gate -- `
  --local-root . `
  --out-dir artifacts `
  --source-patch-id ASH-BASETRAIN-GPU-70K-G134-R2
```
