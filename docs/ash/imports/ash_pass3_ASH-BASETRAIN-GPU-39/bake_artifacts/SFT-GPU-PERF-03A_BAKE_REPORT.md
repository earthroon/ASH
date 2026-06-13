# SFT-GPU-PERF-03A Bake Report

## Baked patch

`SFT-GPU-PERF-03A — LoRA A Delta Warm-Step Gate / Zero-B Init Allowance Seal`

## Files added

```txt
crates/lora_train/src/lora_a_delta_warm_step_gate.rs
crates/lora_train/tests/lora_a_delta_warm_step_gate.rs
acceptance_reports/SFT-GPU-PERF-03A_lora_a_delta_warm_step_gate.md
acceptance_reports/SFT-GPU-PERF-03A_static_validation_result.md
bake_artifacts/SFT-GPU-PERF-03A_BAKE_REPORT.md
```

## Files modified

```txt
crates/lora_train/src/lib.rs
crates/lora_train/src/lm_head_vocab_atlas_gpu_update.rs
crates/lora_train/src/lm_head_vocab_atlas_gpu_export.rs
```

## Contract

First real redispatch step with explicit B-zero-init may allow `a_delta_norm == 0`, but only when:

```txt
grad_b_norm > eps_grad
b_delta_norm > eps_delta
synthetic_step_report_used = false
cpu_serial_fallback_used = false
logits_readback_used = false
full_logits_buffer_used = false
```

Step 2+ requires:

```txt
grad_lora_mid_norm > eps_grad
a_delta_norm > eps_delta
b_delta_norm > eps_delta
```

## Runtime notes

The patch does not weaken the B update guard. It only defers the A delta requirement for the first B-zero-init step and records the reason in a receipt.

## Next patch

```txt
SFT-GPU-PERF-04 — Batch Axis Train Plan / Active Token Matrix Seal
```
