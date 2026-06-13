# SFT-GPU-PERF-08 Static Validation Result

- file_exists:crates/lora_train/src/gpu_microbatch_scheduler.rs: PASS
- file_exists:crates/lora_train/tests/gpu_microbatch_scheduler.rs: PASS
- file_exists:acceptance_reports/SFT-GPU-PERF-08_gpu_microbatch_scheduler_batch_packing_occupancy.md: PASS
- file_exists:bake_artifacts/SFT-GPU-PERF-08_BAKE_REPORT.md: PASS
- file_exists:crates/lora_train/src/lib.rs: PASS
- src_contains:pub struct GpuMicrobatchSchedulerInput: PASS
- src_contains:pub struct GpuMicrobatchPackingPlan: PASS
- src_contains:pub struct GpuMicrobatchSchedulerReceipt: PASS
- src_contains:pub fn build_gpu_microbatch_packing_plan_and_receipt: PASS
- src_contains:CpuFallbackForbidden: PASS
- src_contains:VramBudgetExceeded: PASS
- src_contains:DispatchBudgetExceeded: PASS
- src_contains:MicrobatchShrinkRetryRequired: PASS
- lib_contains:pub mod gpu_microbatch_scheduler;: PASS
- lib_contains:pub use gpu_microbatch_scheduler::: PASS
- test_contains:perf08_builds_gpu_microbatch_packing_plan: PASS
- test_contains:perf08_splits_by_max_active_tokens_per_microbatch: PASS
- test_contains:perf08_rejects_active_token_reorder: PASS
- test_contains:perf08_rejects_lost_original_batch_index: PASS
- test_contains:perf08_estimates_vram_under_budget: PASS
- test_contains:perf08_requests_shrink_retry_when_vram_budget_exceeded: PASS
- test_contains:perf08_rejects_over_budget_when_retry_disabled: PASS
- test_contains:perf08_rejects_cpu_fallback: PASS
- test_contains:perf08_rejects_dispatch_budget_exceeded: PASS
- test_contains:perf08_scheduler_receipt_id_is_deterministic: PASS
- brace_balance:crates/lora_train/src/gpu_microbatch_scheduler.rs: PASS
- brace_balance:crates/lora_train/tests/gpu_microbatch_scheduler.rs: PASS

## Native Rust Test

`cargo test -p lora_train --test gpu_microbatch_scheduler -- --nocapture` was not executed because `cargo` is unavailable in this container.

## Static Result

PASS_STATIC