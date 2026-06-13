# ASH-FT-07 Operator Notes

FT-07 is an optimizer dry-run. It previews optimizer math for one atlas group but does not write candidate safetensors and does not persist optimizer state.

Recommended first run:

```powershell
cargo run --bin ash_ft07_single_group_optimizer_dryrun -- `
  --candidate "D:\1111113232\DUST\1\ash_pass3\tokenizer_v5\artifacts\ash_v5_native_genesis.forge01_smoke.safetensors" `
  --expected-sha256 "cecd088c8830d2c2c4ace4f684b9a06d119c0e00eda54f5d33f4016524c13537" `
  --manifest "artifacts\ash_ft\ash_ft00_full_coverage_manifest.json" `
  --budget "artifacts\ash_ft\ash_ft01_atlas_group_memory_budget.json" `
  --baseline "artifacts\ash_ft\ash_ft03_cpu_tensor_sanity_baseline.json" `
  --drift-registry "artifacts\ash_ft\ash_ft03_sampled_norm_drift_registry.json" `
  --ft04-upload-plan "artifacts\ash_ft\ash_ft04_single_group_gpu_upload_plan.json" `
  --ft04-upload-receipt "artifacts\ash_ft\ash_ft04_single_group_gpu_upload_receipt.json" `
  --ft05-compute-plan "artifacts\ash_ft\ash_ft05_single_group_compute_plan.json" `
  --ft05-forward-receipt "artifacts\ash_ft\ash_ft05_forward_smoke_receipt.json" `
  --ft05-backward-receipt "artifacts\ash_ft\ash_ft05_backward_smoke_receipt.json" `
  --ft05-gradient-shape "artifacts\ash_ft\ash_ft05_gradient_shape_receipt.json" `
  --ft06-gradient-plan "artifacts\ash_ft\ash_ft06_single_group_gradient_plan.json" `
  --ft06-gradient-receipt "artifacts\ash_ft\ash_ft06_gradient_receipt.json" `
  --ft06-gradient-norm-summary "artifacts\ash_ft\ash_ft06_gradient_norm_summary.json" `
  --ft06-optimizer-input-candidate "artifacts\ash_ft\ash_ft06_optimizer_input_candidate.json" `
  --group-id "auto" `
  --optimizer-mode adamw_dryrun `
  --learning-rate 1e-5 `
  --weight-decay 0.01 `
  --adam-beta1 0.9 `
  --adam-beta2 0.999 `
  --adam-eps 1e-8 `
  --gradient-clip-norm 1.0 `
  --delta-norm-soft-limit 10.0 `
  --preview-drift-warn-ratio 0.05 `
  --preview-drift-fail-ratio 0.20 `
  --max-optimizer-elements 262144 `
  --max-preview-readback-bytes 1048576 `
  --candidate-write false `
  --persist-optimizer-state false `
  --worker-stack-mb 128 `
  --out-optimizer-plan "artifacts\ash_ft\ash_ft07_optimizer_dryrun_plan.json" `
  --out-optimizer-state-preview "artifacts\ash_ft\ash_ft07_optimizer_state_preview.json" `
  --out-delta-preview "artifacts\ash_ft\ash_ft07_delta_preview_receipt.json" `
  --out-weight-preview "artifacts\ash_ft\ash_ft07_weight_after_preview_receipt.json" `
  --out-receipt "artifacts\ash_ft\ASH-FT-07_receipt.json"
```
