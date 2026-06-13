# 16AI-QW-38G-R6A-MEM-01 — Inference RAM Budget Guard / Atlas Cache Bound Seal

## Summary

MEM-01 introduces a first-pass runtime memory budget guard at the `orchestrator_local` inference entry boundary. The guard reads memory budget payload options, applies safe default limits, clamps candidate snapshots and native vocab tile sizing, writes a memory receipt, and fails closed with a controlled partial response before inference when the planned memory watermark exceeds the configured hard limit.

## SSOT

RAM budget policy is centralized in `crates/orchestrator_local/src/memory_budget_guard.rs` for this bake.

## Default budget

- hard limit: 32GiB / 34,359,738,368 bytes
- soft limit: 24GiB / 25,769,803,776 bytes
- atlas cache budget: 2GiB
- readback staging budget: 1GiB
- generation artifact budget: 256MiB
- candidate snapshot budget: 128MiB
- max in-flight atlas tiles: 1
- max in-flight GPU readbacks: 1

## Behavior

- `candidatePoolSnapshotTopN` is clamped to `1..=16` under MEM-01.
- `nativeVocabTileSize` is clamped to `1..=1024` under MEM-01.
- `nativeMaxSingleGpuBufferBytes` is clamped to `<= 268435456` under MEM-01.
- A memory budget receipt is written to `memoryBudgetReceiptPath` or `workspace/mem01_memory_budget_receipt.json`.
- If estimated planned memory exceeds `ramHardLimitBytes`, inference is not started; a controlled partial response is emitted.

## Validation

Static validation passed. Local cargo build is required because this bake container does not include Rust/Cargo.

## Mutation policy

No checkpoint, tokenizer, safetensors, lm_head, final_norm, or ban_mask file is modified.
