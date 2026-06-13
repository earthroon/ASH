# ASH-BASETRAIN-GPU-29 Acceptance Report

## Verdict

```txt
EXPECTED_VERDICT = PASS_ASH_BASETRAIN_GPU_29_GRADIENT_BUFFER_ZERO_INIT_BOUNDARY_READBACK_AUDIT_ALLOCATED_LOGITS_GRADIENT_CANDIDATE_BUFFER_ZERO_STATE_VERIFICATION_NO_GRADIENT_VALUE_NO_BACKWARD_NO_OPTIMIZER
SOURCE_CONFIRMED_PASS = ASH-BASETRAIN-GPU-28
NEXT_ROUTE = ASH-BASETRAIN-GPU-30
```

## Opened boundary

```txt
readback_buffer_created = true
copy_buffer_to_buffer_executed = true
queue_submit_executed_for_readback_copy = true
readback_map_async_executed = true
zero_digest_created = true
queue_submit_scope = zero_state_readback_copy_only
```

## Closed boundary

```txt
gradient_formula_evaluated = false
softmax_minus_target_computed = false
logits_gradient_values_materialized = false
gradient_value_computed = false
gradient_buffer_written_with_gradient = false
new_compute_dispatch_executed = false
backward_executed = false
optimizer_step_executed = false
model_weight_gradient_contract_created = false
safetensors_mutation_present = false
runtime_1p1b_training_claimed = false
```

## Zero digest

```txt
zero_digest_algorithm = sha256
zero_digest_scope = raw_8192_zero_bytes
expected_zero_digest_hex = 9f1dcbc35c350d6027f98be0f5c8b43b42ca52b7604459c0c42be3aa88913d47
```
