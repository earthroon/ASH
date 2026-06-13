# ASH-FT-02 Runtime Guide

This command performs a read-only bounded slice probe over the ASH shadow candidate safetensors.

```powershell
cargo run --bin ash_ft02_full_coverage_slice_read_probe -- `
  --candidate "D:\1111113232\DUST\1\ash_pass3\tokenizer_v5\artifacts\ash_v5_native_genesis.forge01_smoke.safetensors" `
  --expected-sha256 "cecd088c8830d2c2c4ace4f684b9a06d119c0e00eda54f5d33f4016524c13537" `
  --manifest "artifacts\ash_ft\ash_ft00_full_coverage_manifest.json" `
  --atlas-plan "artifacts\ash_ft\ash_ft00_atlas_group_plan.json" `
  --budget "artifacts\ash_ft\ash_ft01_atlas_group_memory_budget.json" `
  --optimizer-shards "artifacts\ash_ft\ash_ft01_optimizer_shard_estimate.json" `
  --probe-seed "ash-ft02" `
  --max-samples-per-tensor 3 `
  --max-bytes-per-tensor 65536 `
  --max-total-read-mb 512 `
  --worker-stack-mb 128 `
  --out-probe "artifacts\ash_ft\ash_ft02_full_coverage_slice_probe.json" `
  --out-family-summary "artifacts\ash_ft\ash_ft02_tensor_family_slice_summary.json" `
  --out-receipt "artifacts\ash_ft\ASH-FT-02_receipt.json"
```

Expected success line:

```txt
PASS_ASH_FT02_FULL_COVERAGE_SLICE_READ_NO_GPU_UPLOAD
```

Runtime JSON files are generated locally and must not be included in baked patch zips.
