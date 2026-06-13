# ASH-BASETRAIN-GPU-25 Acceptance

## Status

PENDING OPERATOR LOCAL RUN

## Required PASS verdict

`PASS_ASH_BASETRAIN_GPU_25_GPU_LOCAL_LOSS_REPEATABILITY_AUDIT_REPEATED_WINDOW_2048_TARGET_1_GPU_LOSS_CANDIDATE_STABILITY_NO_BACKWARD_NO_OPTIMIZER`

## Required checks

- `source_24_ssot_validated = true`
- `repeat_count = 3`
- `all_gpu_losses_finite = true`
- `all_gpu_losses_non_negative = true`
- `all_gpu_losses_within_repeat_epsilon = true`
- `all_gpu_losses_within_cpu_reference_epsilon = true`
- `full_vocab_loss_claimed = false`
- `dataset_training_loss_claimed = false`
- `backward_executed = false`
- `optimizer_step_executed = false`
- `safetensors_mutation_present = false`
