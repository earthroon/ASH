# ASH-BASETRAIN-GPU-30 Acceptance Report

## Verdict

```txt
EXPECTED_VERDICT = PASS_ASH_BASETRAIN_GPU_30_CPU_LOGITS_GRADIENT_FORMULA_RECEIPT_LOCAL_WINDOW_SOFTMAX_MINUS_TARGET_CANDIDATE_NO_GPU_WRITE_NO_BACKWARD_NO_OPTIMIZER
SOURCE_CONFIRMED_PASS = ASH-BASETRAIN-GPU-29
NEXT_ROUTE = ASH-BASETRAIN-GPU-31
```

## Opened boundary

```txt
cpu_softmax_computed = true
cpu_one_hot_target_applied = true
cpu_logits_gradient_candidate_materialized = true
cpu_candidate_digest_created = true
cpu_candidate_stats_created = true
```

## Closed boundary

```txt
gpu_gradient_buffer_write_executed = false
gpu_gradient_buffer_written = false
gpu_compute_dispatch_executed = false
backward_executed = false
optimizer_step_executed = false
model_weight_gradient_contract_created = false
safetensors_mutation_present = false
runtime_1p1b_training_claimed = false
```

## Required payload input

```txt
ASH_BASETRAIN_GPU_21_RAW_LOGITS_2048_F32_LE_PATH = path to raw 2048 f32le logits payload
expected_payload_digest = 856552759fc5e7f0b0b7c7b2de78fe0f1e59f82b2ff7c935f819758572878052
```
