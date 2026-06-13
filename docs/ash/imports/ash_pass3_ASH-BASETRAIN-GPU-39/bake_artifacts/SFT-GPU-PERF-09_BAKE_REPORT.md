# SFT-GPU-PERF-09 Bake Report

## Added

- `crates/lora_train/src/batch_vocab_2d_dispatch_grid.rs`
- `crates/lora_train/tests/batch_vocab_2d_dispatch_grid.rs`
- `acceptance_reports/SFT-GPU-PERF-09_batch_vocab_tile_2d_dispatch_grid_kernel_occupancy.md`
- `acceptance_reports/SFT-GPU-PERF-09_static_validation_result.md`

## Modified

- `crates/lora_train/src/lib.rs`

## Contract

PERF-09 consumes PERF-08 microbatch dispatch estimates and binds them to a static 2D dispatch geometry:

- X axis: vocab tile groups
- Y axis: batch active-token blocks
- Z axis: microbatch/reduce groups

The seal rejects missing batch/vocab axes, CPU fallback, serial dispatch, full logits, logits readback, tail tile CPU handling, and dispatch budget overflow.

## Runtime Note

Native Rust tests were not executed in this container because `cargo` is unavailable. Static validation checked file presence, exports, brace balance, and required guard symbols.
