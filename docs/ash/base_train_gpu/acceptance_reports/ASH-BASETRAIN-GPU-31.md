# ASH-BASETRAIN-GPU-31 Acceptance Report

## Verdict

```txt
EXPECTED_VERDICT = PASS_ASH_BASETRAIN_GPU_31_GPU_LOGITS_GRADIENT_WRITE_SMOKE_CPU_CANDIDATE_TO_ALLOCATED_LOGITS_GRADIENT_BUFFER_WRITE_VERIFICATION_NO_BACKWARD_NO_OPTIMIZER
```

## Opened

```txt
gpu_logits_gradient_write_smoke_created = true
gpu_candidate_write_executed = true
gpu_gradient_buffer_written = true
gpu_written_readback_executed = true
gpu_written_candidate_digest_match = true
```

## Closed

```txt
gpu_compute_dispatch_executed = false
backward_executed = false
optimizer_step_executed = false
model_weight_gradient_contract_created = false
safetensors_mutation_present = false
runtime_1p1b_training_claimed = false
```

## Runtime note

This container did not execute cargo. User-local runtime is required.
