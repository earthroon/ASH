# SFT-GPU-PERF-10 Bake Report

## Patch

SFT-GPU-PERF-10 — Vocab Tile Tail Shape Compile Cache / Pass2 Dispatch Latency Seal

## Base

`ash_pass3_SFT-GPU-PERF-09_batch_vocab_tile_2d_dispatch_grid_kernel_occupancy_baked.zip`

## Implementation Summary

Added `vocab_tail_shape_compile_cache.rs`, which introduces:

- `VocabTailShapeCompileCacheInput`
- `VocabTailTileShapeProfile`
- `VocabTailKernelCacheKey`
- `VocabTailDispatchLatencySample`
- `VocabTailShapeCompileCachePlan`
- `VocabTailShapeCompileCacheReceipt`
- `VocabTailShapeCompileCacheDecision`
- `VocabTailShapeCompileCacheError`
- `input_from_2d_dispatch_grid(...)`
- `build_vocab_tail_shape_compile_cache_plan(...)`
- `evaluate_vocab_tail_shape_compile_cache_receipt(...)`
- `build_vocab_tail_shape_compile_cache_plan_and_receipt(...)`

## Seal Behavior

PERF-10 canonicalizes vocab tail tile shape by using padded canonical tile width, creates deterministic pass1/pass2 kernel cache keys, separates warmup cache miss from decision samples, enforces compile/cache reuse after warmup, and rejects tail CPU fallback, tail serial dispatch, dynamic tail shape compile, full logits buffer, logits readback, pass2 dispatch latency excess, and tail latency penalty excess.

## Export

`crates/lora_train/src/lib.rs` now exports the PERF-10 module and public types/builders.

## Test Coverage

Added `crates/lora_train/tests/vocab_tail_shape_compile_cache.rs` with acceptance tests for:

- tail shape cache plan construction
- padded canonical tail tile shape
- deterministic cache key
- warmup miss + post-warmup reuse
- dynamic tail shape compile rejection
- tail CPU fallback rejection
- tail serial dispatch rejection
- pass2 dispatch latency rejection
- tail latency penalty rejection
- deterministic receipt

## Native Test Status

Native Rust tests were not executed in this container because `cargo` is not installed.

## Result

PASS_STATIC_STRUCTURE
PENDING_NATIVE_RUST_TESTS
