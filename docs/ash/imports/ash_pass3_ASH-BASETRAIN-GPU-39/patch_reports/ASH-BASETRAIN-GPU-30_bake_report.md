# ASH-BASETRAIN-GPU-30 Bake Report

## Summary

`ASH-BASETRAIN-GPU-30` adds a CPU-only local-window softmax-minus-target logits-gradient candidate receipt.

## Implemented files

```txt
crates/base_train/src/ash_basetrain_gpu_30_cpu_logits_gradient_formula_receipt.rs
crates/base_train/src/bin/ash_basetrain_gpu_30_cpu_logits_gradient_formula_receipt.rs
```

## Boundary

```txt
CPU formula and candidate digest are opened.
GPU write is closed.
GPU compute dispatch is closed.
Backward is closed.
Optimizer is closed.
Model weight gradient is closed.
```

## Local validation

Container cargo availability is recorded in `ASH_BASETRAIN_GPU_30_LOCAL_VALIDATION.txt`. User-local runtime execution remains the final SSOT because the raw logits payload path is local.
