# ASH-BASETRAIN-GPU HANDOFF AFTER 34

## SSOT

```txt
LATEST_CONFIRMED_PASS = ASH-BASETRAIN-GPU-34
LATEST_VERDICT = PASS_ASH_BASETRAIN_GPU_34_SELECTED_ATLAS_GROUP_GRADIENT_SCOPE_CONTRACT_SINGLE_GROUP_ONLY_NO_FULL_MODEL_GRADIENT
NEXT_PATCH = ASH-BASETRAIN-GPU-35
NEXT_PATCH_KIND = Selected Group Gradient Buffer Allocation Candidate / Single Atlas Group Gradient Buffer Contract No Backward No Optimizer Seal
```

## 34 closed

- Source binding chain digest from 33: `431c13f73a8a111d9492ee30beb1dbe034c63120403d4c140d7d48a61826836a`
- Logits-gradient candidate digest: `4a9f3db1bb85a18497a99b42b7eb0b19394bbaee68b751a968f1ae22b97ba1d8`
- Selected group id: `SELECTED_ATLAS_GROUP_SLOT_0_CONTRACT_ONLY`
- Scope chain digest: `835f52ac541a7c1c488299466b6f3973b37b7dab2f4a3819cee54c23347abf8f`

## Guards

```txt
selected_group_materialized = false
selected_group_weights_loaded = false
selected_group_gradient_buffer_created = false
selected_group_gradient_value_computed = false
model_weight_gradient_computed = false
full_model_gradient_claimed = false
multi_group_gradient_claimed = false
backward_executed = false
optimizer_step_executed = false
safetensors_mutation_present = false
runtime_1p1b_training_claimed = false
unknown_group_weight_shape_policy = do_not_invent_shape
unknown_group_byte_range_policy = do_not_invent_byte_range
```

## Next

```txt
ASH-BASETRAIN-GPU-35
Selected Group Gradient Buffer Allocation Candidate /
Single Atlas Group Gradient Buffer Contract No Backward No Optimizer Seal
```
