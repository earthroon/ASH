# ASH-BASETRAIN-GPU-23 Acceptance Report

## Patch

```txt
ASH-BASETRAIN-GPU-23
Loss Repeatability Audit /
Repeated Local Window Target 1 Loss Scalar Stability No Backward No Optimizer Seal
```

## Scope

- Reads the existing raw 2048-logit payload from `ASH_BASETRAIN_GPU_21_RAW_LOGITS_2048_F32_LE_PATH`.
- Recomputes the same CPU f64 local-window NLL loss three times.
- Audits payload digest bit-exact repeatability and loss scalar epsilon stability.
- Does not open GPU dispatch, readback, backward, gradient, optimizer, delta, weight commit, or safetensors mutation.

## PASS verdict

```txt
PASS_ASH_BASETRAIN_GPU_23_LOSS_REPEATABILITY_AUDIT_REPEATED_LOCAL_WINDOW_TARGET_1_LOSS_SCALAR_STABILITY_NO_BACKWARD_NO_OPTIMIZER
```

## Boundary

```txt
repeat_local_loss_recomputed = true
full_vocab_loss_claimed = false
dataset_training_loss_claimed = false
backward_executed = false
optimizer_step_executed = false
safetensors_mutation_present = false
```
