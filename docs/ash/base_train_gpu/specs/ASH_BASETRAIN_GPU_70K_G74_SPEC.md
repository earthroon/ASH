# ASH-BASETRAIN-GPU-70K-G74

Patch: ASH-BASETRAIN-GPU-70K-G74
Title: Gradient Write Candidate Review Gate

Status: source-baked specification record.

Source files:
- crates/base_train/src/lib.rs
- crates/base_train/src/ash_basetrain_gpu_70k_g74_gradient_write_candidate_review_gate.rs
- crates/base_train/src/bin/ash_basetrain_gpu_70k_g74_gradient_write_candidate_review_gate.rs

Required lib registration:

```rust
pub mod ash_basetrain_gpu_70k_g74_gradient_write_candidate_review_gate;
```

PASS target:

PASS_ASH_BASETRAIN_GPU_70K_G74_GRADIENT_WRITE_CANDIDATE_REVIEW_GATE

Required predecessor SSOT:
- specs/ASH_BASETRAIN_GPU_70K_G73_GRADIENT_WRITE_CANDIDATE.json
- specs/ASH_BASETRAIN_GPU_70K_G73_GRADIENT_WRITE_CANDIDATE_SCHEMA_AUDIT.json

Purpose:
- Read the G73 gradient write candidate and schema audit.
- Create gradient accumulation preflight metadata only.
- Keep execution blocked for backward, gradient buffer allocation, gradient write, accumulation, optimizer, weight, and checkpoint paths.

Packaging note: G74 bake includes lib.rs registration, Cargo bin registration, path-mod bin guard, recursion limit, and excludes predecessor runtime receipts for G50 through G73.
