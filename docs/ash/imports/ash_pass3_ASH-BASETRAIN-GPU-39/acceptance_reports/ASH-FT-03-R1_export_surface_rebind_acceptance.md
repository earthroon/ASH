# ASH-FT-03-R1 Acceptance

```txt
patch_id: ASH-FT-03-R1
title: Export Surface Rebind / Bin Import Closure / No Train Seal
status: PENDING_LOCAL_RUN
```

## Expected local check

```powershell
cargo run --bin ash_ft03_cpu_tensor_sanity_baseline -- --help
```

Then run the full ASH-FT-03 command.

## Expected final PASS

```txt
PASS_ASH_FT03_CPU_TENSOR_SANITY_BASELINE_NO_TRAIN
```

## Guards

```txt
candidate_safetensors_data_opened = false
tensor_slice_read_executed = false
gpu_upload_executed = false
forward_executed = false
backward_executed = false
optimizer_step_executed = false
candidate_weight_write_executed = false
runtime_default_apply_executed = false
train_executed = false
```
