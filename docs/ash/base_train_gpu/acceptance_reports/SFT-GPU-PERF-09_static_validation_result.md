# SFT-GPU-PERF-09 Static Validation Result

Overall: PASS_STATIC

## Checks
- [x] crates/lora_train/src/batch_vocab_2d_dispatch_grid.rs
- [x] crates/lora_train/tests/batch_vocab_2d_dispatch_grid.rs
- [x] crates/lora_train/src/lib.rs
- [x] acceptance_reports/SFT-GPU-PERF-09_batch_vocab_tile_2d_dispatch_grid_kernel_occupancy.md
- [x] bake_artifacts/SFT-GPU-PERF-09_BAKE_REPORT.md
- [x] symbol::BatchVocab2DDispatchGridInput
- [x] symbol::BatchVocab2DDispatchGridPlan
- [x] symbol::BatchVocab2DDispatchRecord
- [x] symbol::BatchVocab2DKernelOccupancyEstimate
- [x] symbol::BatchVocab2DDispatchReceipt
- [x] symbol::BatchVocab2DDispatchDecision
- [x] symbol::BatchVocab2DDispatchError
- [x] symbol::build_batch_vocab_2d_dispatch_grid_plan
- [x] symbol::evaluate_batch_vocab_2d_dispatch_receipt
- [x] symbol::build_batch_vocab_2d_dispatch_grid_plan_and_receipt
- [x] symbol::input_from_microbatch_scheduler
- [x] symbol::BatchTokenAxisMissing
- [x] symbol::VocabTileAxisMissing
- [x] symbol::DispatchBudgetExceeded
- [x] symbol::CpuFallbackForbidden
- [x] symbol::PerTokenSerialDispatchForbidden
- [x] test::perf09_builds_2d_dispatch_grid_from_microbatch_scheduler
- [x] test::perf09_dispatch_covers_all_active_tokens
- [x] test::perf09_dispatch_covers_all_vocab_tiles
- [x] test::perf09_pass1_pass2_grid_is_compatible
- [x] test::perf09_tail_tile_is_gpu_dispatched
- [x] test::perf09_rejects_missing_batch_token_axis
- [x] test::perf09_rejects_missing_vocab_tile_axis
- [x] test::perf09_rejects_dispatch_budget_exceeded
- [x] test::perf09_rejects_cpu_fallback_or_serial_dispatch
- [x] test::perf09_2d_dispatch_receipt_id_is_deterministic
- [x] brace_balance::crates/lora_train/src/batch_vocab_2d_dispatch_grid.rs
- [x] brace_balance::crates/lora_train/tests/batch_vocab_2d_dispatch_grid.rs
- [x] brace_balance::crates/lora_train/src/lib.rs

## Native Test Status

Not executed: `cargo` is not available in this container.

Attempted command:

```bash
cargo test -p lora_train --test batch_vocab_2d_dispatch_grid -- --nocapture
```

Observed:

```txt
bash: line 1: cargo: command not found
```
