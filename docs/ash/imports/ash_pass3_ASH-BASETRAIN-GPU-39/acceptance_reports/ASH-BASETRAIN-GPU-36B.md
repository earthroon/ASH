# ASH-BASETRAIN-GPU-36B Acceptance

## Patch
ASH-BASETRAIN-GPU-36B

## Title
Bounded Weight Slice F32 Window Sanity / Limited Window Bytes To F32 Sample Stats No Full Tensor No GPU Upload Seal

## Source SSOT
`artifacts/ASH_BASETRAIN_GPU_36A_BOUNDED_WEIGHT_SLICE_READ_SMOKE.json`

## Static baked verdict
`BLOCKED_36A_RECEIPT_NOT_FOUND`

This is a valid sealed result for the bake container because the live 36A PASS receipt and source safetensors are local operator artifacts and are not included at their live artifact paths in this package.

## Runtime PASS expectation
`PASS_ASH_BASETRAIN_GPU_36B_BOUNDED_WEIGHT_SLICE_F32_WINDOW_SANITY_LIMITED_WINDOW_BYTES_TO_F32_SAMPLE_STATS_NO_FULL_TENSOR_NO_GPU_UPLOAD`

## Guards
- lookup table control flow required
- Rust standalone `if` keyword absent in 36B source
- Rust standalone `match` keyword absent in 36B source
- bounded window re-read only
- full tensor load blocked
- safetensors header parse blocked
- mmap blocked
- GPU upload blocked
- forward/backward/optimizer/mutation blocked

## Operator command
```powershell
cargo run -p base_train --bin ash_basetrain_gpu_36b_bounded_weight_slice_f32_window_sanity -- --window-read-receipt .\artifacts\ASH_BASETRAIN_GPU_36A_BOUNDED_WEIGHT_SLICE_READ_SMOKE.json
```
