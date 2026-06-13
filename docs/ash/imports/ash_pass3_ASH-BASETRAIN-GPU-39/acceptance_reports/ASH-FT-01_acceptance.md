# ASH-FT-01 Acceptance

## Expected verdict

```txt
PASS_ASH_FT01_ATLAS_GROUP_MEMORY_BUDGET_NO_TENSOR_LOAD
```

## Required evidence

- FT-00 manifest read: true
- FT-00 atlas plan read: true
- FT-00 manifest SHA256 recorded
- FT-00 atlas plan SHA256 recorded
- memory budget JSON created
- optimizer shard estimate JSON created
- receipt JSON created
- total_group_count > 0
- full_load_required = false
- tensor_load_executed = false

## Guard evidence

```json
{
  "candidate_safetensors_data_opened": false,
  "tensor_value_materialized": false,
  "tensor_slice_read_executed": false,
  "full_tensor_load_executed": false,
  "mmap_materialization_executed": false,
  "gpu_device_created": false,
  "gpu_buffer_created": false,
  "gpu_upload_executed": false,
  "forward_executed": false,
  "backward_executed": false,
  "optimizer_step_executed": false,
  "candidate_weight_write_executed": false,
  "runtime_default_apply_executed": false,
  "checkpoint_alias_rebind_executed": false
}
```

## Notes

BLACK and RED feasibility groups do not automatically fail ASH-FT-01. They are planning outputs. The patch fails only if it misclassifies them as safe without tile/offload requirements, fails to compute budgets, or violates the no tensor load contract.
