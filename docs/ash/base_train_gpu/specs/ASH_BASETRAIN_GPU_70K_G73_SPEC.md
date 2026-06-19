# ASH-BASETRAIN-GPU-70K-G73

Patch: ASH-BASETRAIN-GPU-70K-G73
Title: Gradient Buffer Layout Preflight Review Gate

Status: source-baked specification record.

Source files:
- crates/base_train/src/lib.rs
- crates/base_train/src/ash_basetrain_gpu_70k_g73_gradient_buffer_layout_preflight_review_gate.rs
- crates/base_train/src/bin/ash_basetrain_gpu_70k_g73_gradient_buffer_layout_preflight_review_gate.rs

Required lib registration:

```rust
pub mod ash_basetrain_gpu_70k_g73_gradient_buffer_layout_preflight_review_gate;
```

PASS target:

PASS_ASH_BASETRAIN_GPU_70K_G73_GRADIENT_BUFFER_LAYOUT_PREFLIGHT_REVIEW_GATE

Required predecessor SSOT:
- specs/ASH_BASETRAIN_GPU_70K_G72_GRADIENT_BUFFER_LAYOUT_PREFLIGHT.json
- specs/ASH_BASETRAIN_GPU_70K_G72_GRADIENT_BUFFER_LAYOUT_PREFLIGHT_SCHEMA_AUDIT.json

Purpose:
- Read the G72 gradient buffer layout preflight and schema audit.
- Create gradient write candidate metadata only.
- Keep execution blocked for backward, gradient buffer allocation, gradient write, accumulation, optimizer, weight, and checkpoint paths.

Packaging note: G73 bake includes lib.rs registration, Cargo bin registration, path-mod bin guard, recursion limit, and excludes predecessor runtime receipts for G50 through G72.
