# SFT-GPU-PERF-05 Static Validation Result

## Scope

Static validation for Batch-Parallel Vocab Tile Pass1 LogSumExp / No Per-Sample Serial Loop Seal.

## Checks

- [x] crates/lora_train/src/batch_parallel_vocab_tile_pass1.rs_exists
- [x] crates/lora_train/src/batch_parallel_vocab_tile_pass1.rs_brace_balance
- [x] crates/lora_train/src/batch_parallel_vocab_tile_pass1.rs_paren_balance
- [x] crates/lora_train/src/batch_parallel_vocab_tile_pass1.rs_bracket_balance
- [x] crates/lora_train/tests/batch_parallel_vocab_tile_pass1.rs_exists
- [x] crates/lora_train/tests/batch_parallel_vocab_tile_pass1.rs_brace_balance
- [x] crates/lora_train/tests/batch_parallel_vocab_tile_pass1.rs_paren_balance
- [x] crates/lora_train/tests/batch_parallel_vocab_tile_pass1.rs_bracket_balance
- [x] crates/lora_train/src/lib.rs_exists
- [x] crates/lora_train/src/lib.rs_brace_balance
- [x] crates/lora_train/src/lib.rs_paren_balance
- [x] crates/lora_train/src/lib.rs_bracket_balance
- [x] module_contains_pub struct BatchParallelPass1Input
- [x] module_contains_pub struct BatchParallelPass1DispatchRecord
- [x] module_contains_pub struct BatchParallelPass1TokenResult
- [x] module_contains_pub struct BatchParallelPass1Plan
- [x] module_contains_pub struct BatchParallelPass1Receipt
- [x] module_contains_pub enum BatchParallelPass1Error
- [x] module_contains_pub fn build_batch_parallel_pass1_plan
- [x] module_contains_pub fn evaluate_batch_parallel_pass1_receipt
- [x] module_contains_pub fn build_batch_parallel_pass1_plan_and_receipt
- [x] module_contains_PerSampleSerialLoopForbidden
- [x] module_contains_PerTokenSerialDispatchForbidden
- [x] module_contains_FullLogitsBufferForbidden
- [x] module_contains_LogitsReadbackForbidden
- [x] module_contains_CpuFallbackForbidden
- [x] module_contains_TailTileNotGpuDispatched
- [x] module_contains_DispatchDoesNotCoverAllActiveTokens
- [x] module_contains_DispatchDoesNotCoverAllVocabTiles
- [x] lib_contains_pub mod batch_parallel_vocab_tile_pass1;
- [x] lib_contains_pub use batch_parallel_vocab_tile_pass1::{
- [x] lib_contains_BatchParallelPass1Input
- [x] lib_contains_build_batch_parallel_pass1_plan_and_receipt
- [x] test_contains_perf05_builds_batch_parallel_pass1_plan_from_batch_axis_plan
- [x] test_contains_perf05_dispatch_covers_all_active_tokens
- [x] test_contains_perf05_dispatch_covers_all_vocab_tiles
- [x] test_contains_perf05_tail_tile_is_gpu_dispatched
- [x] test_contains_perf05_rejects_per_sample_serial_loop
- [x] test_contains_perf05_rejects_per_token_serial_dispatch
- [x] test_contains_perf05_rejects_full_logits_buffer
- [x] test_contains_perf05_rejects_logits_readback
- [x] test_contains_perf05_rejects_missing_active_token_axis
- [x] test_contains_perf05_pass1_receipt_id_is_deterministic

## Native Test Status

`cargo test -p lora_train --test batch_parallel_vocab_tile_pass1 -- --nocapture` was attempted, but cargo/rustc is unavailable in this container.

## Result

PASS_STATIC
