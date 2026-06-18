# ASH-BASETRAIN-GPU-70K-G52

## Patch

```text
ASH-BASETRAIN-GPU-70K-G52
Gradient Boundary Preflight /
Finite Loss Candidate To Backward Readiness Audit Seal
No Gradient Write No Optimizer No Weight Commit
```

## Commit

```text
commit: ASH-BASETRAIN-GPU-70K-G52
title: Gradient Boundary Preflight
message: base_train: add gradient boundary preflight from finite loss candidate
```

## Purpose

G52 consumes the G51 finite loss candidate and creates a backward-readiness preflight receipt. This is still metadata-only. It creates readiness and boundary receipts but does not perform the training step or alter model state.

## Required SSOT Inputs

```text
specs/ASH_BASETRAIN_GPU_70K_G51_GROUP_LOCAL_FINITE_LOSS_CANDIDATE_RECEIPT.json
specs/ASH_BASETRAIN_GPU_70K_G51_FINITE_LOSS_VALUE_AUDIT.json
selected_group_id = vocab_row_group__lm_head_weight
```

Optional lineage inputs:

```text
specs/ASH_BASETRAIN_GPU_70K_G50_GROUP_LOCAL_LOGITS_CANDIDATE_RECEIPT.json
specs/ASH_BASETRAIN_GPU_70K_G49_SELECTED_ATLAS_GROUP_RESIDENT_CANDIDATE_RECEIPT.json
```

## State Ownership

G52 writes only JSON receipts under `specs/`. It does not change model weights, gradient buffers, optimizer state, checkpoint state, tokenizer state, runtime route state, tensor payloads, or committed training state.

## Source Files

```text
crates/base_train/src/ash_basetrain_gpu_70k_g52_gradient_boundary_preflight.rs
crates/base_train/src/bin/ash_basetrain_gpu_70k_g52_gradient_boundary_preflight.rs
```

## Cargo Bin

```toml
[[bin]]
name = "ash_basetrain_gpu_70k_g52_gradient_boundary_preflight"
path = "src/bin/ash_basetrain_gpu_70k_g52_gradient_boundary_preflight.rs"
```

## Receipts

```text
specs/ASH_BASETRAIN_GPU_70K_G52_GRADIENT_BOUNDARY_PREFLIGHT_RECEIPT.json
specs/ASH_BASETRAIN_GPU_70K_G52_BACKWARD_READINESS_AUDIT.json
specs/ASH_BASETRAIN_GPU_70K_G52_LOSS_CANDIDATE_LINEAGE_AUDIT.json
specs/ASH_BASETRAIN_GPU_70K_G52_GRADIENT_BUFFER_REQUIREMENT_PREFLIGHT.json
specs/ASH_BASETRAIN_GPU_70K_G52_BACKWARD_WOULD_RUN_CANDIDATE_ENVELOPE.json
specs/ASH_BASETRAIN_GPU_70K_G52_NO_BACKWARD_EXECUTION_AUDIT.json
specs/ASH_BASETRAIN_GPU_70K_G52_NO_GRADIENT_WRITE_AUDIT.json
specs/ASH_BASETRAIN_GPU_70K_G52_NO_OPTIMIZER_WEIGHT_COMMIT_AUDIT.json
specs/ASH_BASETRAIN_GPU_70K_G52_NO_CHECKPOINT_MUTATION_AUDIT.json
specs/ASH_BASETRAIN_GPU_70K_G52_FORBIDDEN_CLAIM_AUDIT.json
specs/ASH_BASETRAIN_GPU_70K_G52_STATIC_CHECKS.json
specs/ASH_BASETRAIN_GPU_70K_G52_BAKE_MANIFEST.json
specs/ASH_BASETRAIN_GPU_70K_G52_LOCAL_BAKE_VALIDATION.json
```

## PASS Target

```text
PASS_ASH_BASETRAIN_GPU_70K_G52_GRADIENT_BOUNDARY_PREFLIGHT
```

PASS requires G51 PASS lineage, finite loss input, selected group match, readiness metadata creation, gradient-buffer requirement preflight metadata creation, would-run envelope metadata creation, and `boundary_failures=0`.

## Failure States

```text
FAIL_ASH_BASETRAIN_GPU_70K_G52_G51_LOSS_LINEAGE_INVALID
FAIL_ASH_BASETRAIN_GPU_70K_G52_NON_FINITE_LOSS_INPUT
FAIL_ASH_BASETRAIN_GPU_70K_G52_SELECTED_GROUP_MISMATCH
FAIL_ASH_BASETRAIN_GPU_70K_G52_BACKWARD_EXECUTION_BOUNDARY_BREACH
FAIL_ASH_BASETRAIN_GPU_70K_G52_GRADIENT_WRITE_BOUNDARY_BREACH
FAIL_ASH_BASETRAIN_GPU_70K_G52_OPTIMIZER_OR_WEIGHT_COMMIT_BOUNDARY_BREACH
FAIL_ASH_BASETRAIN_GPU_70K_G52_CHECKPOINT_MUTATION_BOUNDARY_BREACH
```

## Runtime CLI

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_70k_g52_gradient_boundary_preflight -- `
  --g51-finite-loss-candidate .\specs\ASH_BASETRAIN_GPU_70K_G51_GROUP_LOCAL_FINITE_LOSS_CANDIDATE_RECEIPT.json `
  --g51-finite-loss-audit .\specs\ASH_BASETRAIN_GPU_70K_G51_FINITE_LOSS_VALUE_AUDIT.json `
  --selected-group-id vocab_row_group__lm_head_weight `
  --out-dir specs
```

## Packaging Note

The G52 lightweight bake excludes predecessor runtime receipt files for G48/G49/G50/G51 to avoid overwriting locally generated runtime PASS evidence when the ZIP is unpacked over an active workspace.

## Next Patch

```text
ASH-BASETRAIN-GPU-70K-G53
Backward Dispatch Candidate Envelope /
Backward Readiness Audit To Dispatch Candidate Seal
No Backward Execution No Gradient Write No Optimizer
```
