# ASH-FT-04 Single Group GPU Upload Dry-run

FT-04 uploads one selected atlas group bounded slice set to GPU buffers.
It is not a training patch. It creates no shader module, no pipeline, and dispatches no work.

## Command

```powershell
cargo run --bin ash_ft04_single_group_gpu_upload_dryrun -- `
  --candidate "D:\1111113232\DUST\1\ash_pass3\tokenizer_v5\artifacts\ash_v5_native_genesis.forge01_smoke.safetensors" `
  --expected-sha256 "cecd088c8830d2c2c4ace4f684b9a06d119c0e00eda54f5d33f4016524c13537" `
  --manifest "artifacts\ash_ft\ash_ft00_full_coverage_manifest.json" `
  --budget "artifacts\ash_ft\ash_ft01_atlas_group_memory_budget.json" `
  --slice-probe "artifacts\ash_ft\ash_ft02_full_coverage_slice_probe.json" `
  --baseline "artifacts\ash_ft\ash_ft03_cpu_tensor_sanity_baseline.json" `
  --drift-registry "artifacts\ash_ft\ash_ft03_sampled_norm_drift_registry.json" `
  --group-id "auto" `
  --max-upload-bytes 67108864 `
  --max-bytes-per-tensor 65536 `
  --tile-policy auto `
  --adapter-policy high_performance `
  --allow-readback false `
  --worker-stack-mb 128 `
  --out-upload-plan "artifacts\ash_ft\ash_ft04_single_group_gpu_upload_plan.json" `
  --out-upload-receipt "artifacts\ash_ft\ash_ft04_single_group_gpu_upload_receipt.json" `
  --out-gpu-snapshot "artifacts\ash_ft\ash_ft04_gpu_capability_snapshot.json" `
  --out-receipt "artifacts\ash_ft\ASH-FT-04_receipt.json"
```

Use an explicit `--group-id` when a specific GREEN group is selected. `auto` chooses the smallest GREEN non-unknown non-norm group from FT-01 budget.
