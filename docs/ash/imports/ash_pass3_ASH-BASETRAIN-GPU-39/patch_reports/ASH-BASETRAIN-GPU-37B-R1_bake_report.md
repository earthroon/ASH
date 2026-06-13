# ASH-BASETRAIN-GPU-37B-R1 Bake Report

## Result
Baked source rebind fix over ASH-BASETRAIN-GPU-37B.

## Fixed blocker
`BLOCKED_COMBINED_ROW_BLOCK_STREAMING_PLAN_DIGEST_MISSING` was triggered even though 37A PASS receipt exposes `combined_row_block_streaming_plan_digest_hex` under `row_block_schedule_summary`.

## Change
- Removed the false requirement that input `source_binding` must contain `combined_row_block_streaming_plan_digest_hex`.
- Kept `source_binding` presence as an upstream receipt boundary.
- Kept digest SSOT binding from `row_block_schedule_summary.combined_row_block_streaming_plan_digest_hex`.

## No logic boundary changes
- Representative targets unchanged: `block_000000`, `block_000094`, `block_000188_tail`.
- Max bounded row-block read unchanged: `5,267,456` bytes.
- No F32 decode added.
- No GPU upload added.
- No full selected group read added.
- No mutation path added.

## Build note
Cargo/rustc were not available in this container, so local cargo build/run must be performed by operator.
