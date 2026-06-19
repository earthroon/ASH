# ASH-BASETRAIN-GPU-70K-G75

Patch: ASH-BASETRAIN-GPU-70K-G75
Title: Gradient Accumulation Preflight Review Gate

Status: source-baked specification record.

Source files:
- crates/base_train/src/lib.rs
- crates/base_train/src/ash_basetrain_gpu_70k_g75_gradient_accumulation_preflight_review_gate.rs
- crates/base_train/src/bin/ash_basetrain_gpu_70k_g75_gradient_accumulation_preflight_review_gate.rs

Required lib registration:

```rust
pub mod ash_basetrain_gpu_70k_g75_gradient_accumulation_preflight_review_gate;
```

PASS target:

PASS_ASH_BASETRAIN_GPU_70K_G75_GRADIENT_ACCUMULATION_PREFLIGHT_REVIEW_GATE

Required predecessor SSOT:
- specs/ASH_BASETRAIN_GPU_70K_G74_GRADIENT_ACCUMULATION_PREFLIGHT.json
- specs/ASH_BASETRAIN_GPU_70K_G74_GRADIENT_ACCUMULATION_PREFLIGHT_SCHEMA_AUDIT.json

Purpose:
- Read the G74-R1 gradient accumulation preflight and schema audit.
- Create optimizer boundary candidate metadata only.
- Preserve G73-R1/G74-R1 hotfix lineage flags.
- Keep execution blocked for backward, gradient buffer allocation, gradient write, gradient accumulation, optimizer creation, optimizer execution, optimizer step, weight, and checkpoint paths.

Packaging note: G75 bake includes lib.rs registration, Cargo bin registration, path-mod bin guard, recursion limit, and excludes predecessor runtime receipts for G50 through G74.
