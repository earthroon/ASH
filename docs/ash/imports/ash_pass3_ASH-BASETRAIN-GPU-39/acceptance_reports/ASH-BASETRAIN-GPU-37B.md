# ASH-BASETRAIN-GPU-37B Acceptance Report

## Patch
Selected Group Row-Block Streaming Read Smoke / Sequential Row-Block Plan To Bounded Multi-Block Read No GPU Upload Seal

## Source SSOT
`artifacts/ASH_BASETRAIN_GPU_37A_SELECTED_GROUP_FULL_ROW_BLOCK_STREAMING_PLAN.json` must be supplied explicitly at runtime.

## Runtime PASS expectation
`PASS_ASH_BASETRAIN_GPU_37B_SELECTED_GROUP_ROW_BLOCK_STREAMING_READ_SMOKE_SEQUENTIAL_ROW_BLOCK_PLAN_TO_BOUNDED_MULTI_BLOCK_READ_NO_GPU_UPLOAD`

## Representative blocks
- `block_000000` = 2,097,152 bytes
- `block_000094` = 2,097,152 bytes
- `block_000188_tail` = 1,073,152 bytes
- total = 5,267,456 bytes

## Closed boundaries
- no F32 decode
- no CPU tensor materialization
- no full selected group read
- no GPU upload
- no forward/backward/optimizer/mutation
