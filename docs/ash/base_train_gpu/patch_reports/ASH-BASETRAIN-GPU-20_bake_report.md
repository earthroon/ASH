# ASH-BASETRAIN-GPU-20 Bake Report

## Changed files

- crates/base_train/src/ash_basetrain_gpu_20_fixed_target_loss_candidate_gate.rs
- crates/base_train/src/bin/ash_basetrain_gpu_20_fixed_target_loss_candidate_gate.rs

## Seal

Static fixed target loss candidate gate. No WGPU dispatch, no readback, no loss, no backward, no optimizer.

## PASS verdict

PASS_ASH_BASETRAIN_GPU_20_FIXED_TARGET_LOSS_CANDIDATE_GATE_WINDOW_2048_STABLE_LOGITS_TO_LOCAL_TARGET_LOSS_SCOPE_NO_BACKWARD_NO_OPTIMIZER
