# ASH-BASETRAIN-GPU-70K-G65

Patch: ASH-BASETRAIN-GPU-70K-G65
Title: Submit Permission Grant Preflight Operator Review Gate

Status: source-baked specification record.

Source files:
- crates/base_train/src/lib.rs
- crates/base_train/src/ash_basetrain_gpu_70k_g65_submit_permission_grant_preflight_operator_review_gate.rs
- crates/base_train/src/bin/ash_basetrain_gpu_70k_g65_submit_permission_grant_preflight_operator_review_gate.rs

Required lib registration:

```rust
pub mod ash_basetrain_gpu_70k_g65_submit_permission_grant_preflight_operator_review_gate;
```

PASS target:

PASS_ASH_BASETRAIN_GPU_70K_G65_SUBMIT_PERMISSION_GRANT_PREFLIGHT_OPERATOR_REVIEW_GATE

Packaging note: G65 bake includes lib.rs registration, Cargo bin registration, proactive lib registration script, and excludes predecessor runtime receipts for G50 through G64.
