# ASH-FT-04-R1 Acceptance

## Expected

```txt
PASS_ASH_FT04_SINGLE_GROUP_GPU_UPLOAD_DRYRUN_NO_FORWARD_NO_TRAIN
```

## Acceptance criteria

1. `crates/model_core/src/ash_ft04_single_group_gpu_upload_dryrun.rs` no longer references a nonexistent local `total_uploaded_bytes`.
2. `AshFt04GpuUploadSummaryReceipt.total_uploaded_bytes` is initialized from `total_upload_bytes`.
3. No shader/pipeline/dispatch/forward/backward/train logic is introduced.
4. No candidate write/default apply path is introduced.
5. Runtime result artifacts are not packaged.

## Static receipt

```txt
compile_error_fixed: E0425_total_uploaded_bytes_shorthand
logic_scope: receipt_field_binding_only
no_forward_no_train_guard_changed: false
```
