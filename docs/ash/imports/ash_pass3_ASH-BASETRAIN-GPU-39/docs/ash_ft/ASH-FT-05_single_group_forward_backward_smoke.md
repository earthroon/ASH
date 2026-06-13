# ASH-FT-05 Single Group Forward/Backward Smoke

FT-05 is the first local compute smoke after FT-04 GPU upload. It runs a small WGSL compute shader against one selected atlas group slice and deterministic synthetic buffers.

It is not optimizer application, not training, and not candidate mutation.

## Command

```powershell
cargo run --bin ash_ft05_single_group_forward_backward_smoke -- `
  --candidate "D:\1111113232\DUST\1\ash_pass3\tokenizer_v5\artifacts\ash_v5_native_genesis.forge01_smoke.safetensors" `
  --expected-sha256 "cecd088c8830d2c2c4ace4f684b9a06d119c0e00eda54f5d33f4016524c13537" `
  --manifest "artifacts\ash_ft\ash_ft00_full_coverage_manifest.json" `
  --budget "artifacts\ash_ft\ash_ft01_atlas_group_memory_budget.json" `
  --baseline "artifacts\ash_ft\ash_ft03_cpu_tensor_sanity_baseline.json" `
  --drift-registry "artifacts\ash_ft\ash_ft03_sampled_norm_drift_registry.json" `
  --ft04-upload-plan "artifacts\ash_ft\ash_ft04_single_group_gpu_upload_plan.json" `
  --ft04-upload-receipt "artifacts\ash_ft\ash_ft04_single_group_gpu_upload_receipt.json" `
  --ft04-gpu-snapshot "artifacts\ash_ft\ash_ft04_gpu_capability_snapshot.json" `
  --group-id "auto" `
  --micro-batch 1 `
  --max-compute-elements 262144 `
  --max-readback-bytes 1048576 `
  --shader-policy local_smoke_only `
  --allow-readback true `
  --optimizer-mode none `
  --candidate-write false `
  --worker-stack-mb 128 `
  --out-compute-plan "artifacts\ash_ft\ash_ft05_single_group_compute_plan.json" `
  --out-forward-receipt "artifacts\ash_ft\ash_ft05_forward_smoke_receipt.json" `
  --out-backward-receipt "artifacts\ash_ft\ash_ft05_backward_smoke_receipt.json" `
  --out-gradient-shape "artifacts\ash_ft\ash_ft05_gradient_shape_receipt.json" `
  --out-receipt "artifacts\ash_ft\ASH-FT-05_receipt.json"
```
