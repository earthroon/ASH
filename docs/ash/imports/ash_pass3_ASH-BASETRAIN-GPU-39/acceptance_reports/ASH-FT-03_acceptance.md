# ASH-FT-03 Acceptance

```txt
status: PENDING_RUNTIME
expected_pass: PASS_ASH_FT03_CPU_TENSOR_SANITY_BASELINE_NO_TRAIN
```

## Runtime command

```powershell
cargo run --bin ash_ft03_cpu_tensor_sanity_baseline -- `
  --manifest "artifacts\ash_ft\ash_ft00_full_coverage_manifest.json" `
  --budget "artifacts\ash_ft\ash_ft01_atlas_group_memory_budget.json" `
  --slice-probe "artifacts\ash_ft\ash_ft02_full_coverage_slice_probe.json" `
  --family-summary "artifacts\ash_ft\ash_ft02_tensor_family_slice_summary.json" `
  --baseline-policy conservative `
  --drift-threshold-policy relative `
  --norm-zero-epsilon 1e-12 `
  --max-abs-soft-limit 100.0 `
  --outlier-z-threshold 6.0 `
  --worker-stack-mb 128 `
  --out-baseline "artifacts\ash_ft\ash_ft03_cpu_tensor_sanity_baseline.json" `
  --out-drift-registry "artifacts\ash_ft\ash_ft03_sampled_norm_drift_registry.json" `
  --out-outlier-queue "artifacts\ash_ft\ash_ft03_tensor_outlier_review_queue.json" `
  --out-receipt "artifacts\ash_ft\ASH-FT-03_receipt.json"
```

## Guard contract

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
