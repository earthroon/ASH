# Acceptance Report — ASH-BASETRAIN-GPU-35

## PASS Boundary

Expected PASS:

```txt
PASS_ASH_BASETRAIN_GPU_35_SELECTED_GROUP_GRADIENT_BUFFER_ALLOCATION_CANDIDATE_SINGLE_ATLAS_GROUP_GRADIENT_BUFFER_CONTRACT_NO_BACKWARD_NO_OPTIMIZER
```

## Default Accepted Blocked State

```txt
allocation_candidate_status = BLOCKED_MISSING_SELECTED_GROUP_MANIFEST
selected_group_manifest_present = false
selected_group_gradient_buffer_allocated = false
selected_group_gradient_buffer_descriptor_finalized = false
unknown_shape_not_invented = true
unknown_byte_range_not_invented = true
```

## Closed

```txt
selected_group_weights_loaded = false
selected_group_backward_executed = false
selected_group_gradient_value_computed = false
model_weight_gradient_computed = false
optimizer_step_executed = false
safetensors_mutation_present = false
runtime_1p1b_training_claimed = false
```
