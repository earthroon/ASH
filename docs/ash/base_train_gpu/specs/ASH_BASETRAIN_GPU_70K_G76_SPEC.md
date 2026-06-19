# ASH-BASETRAIN-GPU-70K-G76

Patch: ASH-BASETRAIN-GPU-70K-G76
Title: Optimizer Boundary Candidate Review Gate

Status: source-baked specification record.

Source files:
- crates/base_train/src/lib.rs
- crates/base_train/src/ash_basetrain_gpu_70k_g76_optimizer_boundary_candidate_review_gate.rs
- crates/base_train/src/bin/ash_basetrain_gpu_70k_g76_optimizer_boundary_candidate_review_gate.rs

Required lib registration:

```rust
pub mod ash_basetrain_gpu_70k_g76_optimizer_boundary_candidate_review_gate;
```

PASS target:

PASS_ASH_BASETRAIN_GPU_70K_G76_OPTIMIZER_BOUNDARY_CANDIDATE_REVIEW_GATE

Required predecessor SSOT:
- specs/ASH_BASETRAIN_GPU_70K_G75_OPTIMIZER_BOUNDARY_CANDIDATE.json
- specs/ASH_BASETRAIN_GPU_70K_G75_OPTIMIZER_BOUNDARY_CANDIDATE_SCHEMA_AUDIT.json

Purpose:
- Read the G75 optimizer boundary candidate and schema audit.
- Create weight delta candidate preflight metadata only.
- Preserve G73-R1/G74-R1 hotfix lineage flags.
- Keep execution blocked for backward, gradient buffer allocation, gradient write, gradient accumulation, optimizer creation, optimizer execution, optimizer step, weight delta materialization, weight commit, and checkpoint paths.

Packaging note: G76 bake includes lib.rs registration, Cargo bin registration, path-mod bin guard, recursion limit, and excludes predecessor runtime receipts for G50 through G75.
