# ASH-BASETRAIN-GPU-70K-G72

Patch: ASH-BASETRAIN-GPU-70K-G72
Title: Gradient Boundary Candidate Review Gate

Status: source-baked specification record.

Source files:
- crates/base_train/src/lib.rs
- crates/base_train/src/ash_basetrain_gpu_70k_g72_gradient_boundary_candidate_review_gate.rs
- crates/base_train/src/bin/ash_basetrain_gpu_70k_g72_gradient_boundary_candidate_review_gate.rs

Required lib registration:

```rust
pub mod ash_basetrain_gpu_70k_g72_gradient_boundary_candidate_review_gate;
```

PASS target:

PASS_ASH_BASETRAIN_GPU_70K_G72_GRADIENT_BOUNDARY_CANDIDATE_REVIEW_GATE

Required predecessor SSOT:
- specs/ASH_BASETRAIN_GPU_70K_G71_GRADIENT_BOUNDARY_CANDIDATE.json
- specs/ASH_BASETRAIN_GPU_70K_G71_GRADIENT_BOUNDARY_CANDIDATE_SCHEMA_AUDIT.json

Purpose:
- Read the G71 gradient boundary candidate and schema audit.
- Create gradient buffer layout preflight metadata only.
- Keep execution blocked for backward, gradient write, accumulation, optimizer, weight, and checkpoint paths.

Packaging note: G72 bake includes lib.rs registration, Cargo bin registration, path-mod bin guard, recursion limit, and excludes predecessor runtime receipts for G50 through G71.
