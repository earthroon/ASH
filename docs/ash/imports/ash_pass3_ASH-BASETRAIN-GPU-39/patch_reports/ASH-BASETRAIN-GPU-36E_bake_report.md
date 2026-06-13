# ASH-BASETRAIN-GPU-36E Bake Report

## Patch

Bounded Weight Slice Row Continuity Promotion Gate / Adjacent Window Continuity To CPU Tensor View Candidate No Full Tensor No GPU Upload Seal

## Implemented

- Added 36E Rust library runner.
- Added 36E bin entrypoint.
- Added static BLOCK receipt.
- Added acceptance report, static checks, and bake manifest.
- Removed live upstream receipt artifacts from package to avoid local PASS receipt overwrite.

## Guard

36E creates only a CPU tensor view candidate envelope. It does not materialize a CPU tensor view and does not read source safetensors bytes.

## Local command

```powershell
cargo run -p base_train --bin ash_basetrain_gpu_36e_bounded_weight_slice_row_continuity_promotion_gate -- --row-continuity-receipt .\artifacts\ASH_BASETRAIN_GPU_36D_BOUNDED_WEIGHT_SLICE_ROW_SAMPLE_CONTINUITY_PROBE.json
```
