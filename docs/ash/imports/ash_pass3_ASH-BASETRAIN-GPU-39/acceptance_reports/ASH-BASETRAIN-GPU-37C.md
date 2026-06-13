# ASH-BASETRAIN-GPU-37C Acceptance Report

## Patch
Selected Group Row-Block F32 Decode Smoke / Bounded Multi-Block Bytes To F32 Block Stats No Full Tensor No GPU Upload Seal

## Source SSOT
`artifacts/ASH_BASETRAIN_GPU_37B_SELECTED_GROUP_ROW_BLOCK_STREAMING_READ_SMOKE.json` must be supplied explicitly at runtime.

## Runtime PASS expectation
`PASS_ASH_BASETRAIN_GPU_37C_SELECTED_GROUP_ROW_BLOCK_F32_DECODE_SMOKE_BOUNDED_MULTI_BLOCK_BYTES_TO_F32_BLOCK_STATS_NO_FULL_TENSOR_NO_GPU_UPLOAD`

## Representative blocks
- `block_000000` = 2,097,152 bytes = 524,288 F32 samples
- `block_000094` = 2,097,152 bytes = 524,288 F32 samples
- `block_000188_tail` = 1,073,152 bytes = 268,288 F32 samples
- total = 5,267,456 bytes = 1,316,864 F32 samples

## Runtime checks
- re-read each selected block from source shard
- verify each re-read byte digest matches 37B digest
- decode F32 little-endian values
- emit per-block finite/NaN/Inf/min/max/mean/abs_mean/rms stats

## Closed boundaries
- no full selected group read
- no CPU tensor materialization
- no GPU upload
- no forward/backward/optimizer/mutation
