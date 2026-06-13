# ASH-BASETRAIN-GPU-37P-R1 Acceptance

## Verdict

```txt
PASS_STATIC_BAKE_CHECKS
```

## Accepted Static Conditions

- [x] `patch_id_r1`
- [x] `base_patch_id_preserved`
- [x] `pass_status_r1`
- [x] `default_37o_runtime_receipt_path`
- [x] `default_37f_runtime_receipt_path`
- [x] `new_window_sum_receipt_arg`
- [x] `legacy_window_sum_receipt_arg_preserved`
- [x] `37o_wrong_artifact_kind_guard`
- [x] `37o_read_failed_split`
- [x] `37f_payload_error_namespace`
- [x] `37f_source_error_split`
- [x] `runtime_artifact_paths_declared`
- [x] `write_default_artifact_present`
- [x] `bin_calls_write_default_artifact`
- [x] `receipt_has_artifact_write_section`
- [x] `receipt_has_blocked_reason_code`
- [x] `guards_no_forward_optimizer_mutation`

## Required Local Runtime Acceptance

- `pass = true`
- `verdict = PASS`
- `status starts_with PASS_ASH_BASETRAIN_GPU_37P_R1`
- `source_binding.window_sum_receipt_pass = true`
- `source_binding.payload_37f_receipt_pass = true`
- `runtime_execution.actual_dispatch_executed = true`
- `runtime_execution.actual_readback_executed = true`
- `artifact_write.runtime_receipt_written = true`
- all forward/backward/optimizer/checkpoint/safetensors mutation guards remain false
