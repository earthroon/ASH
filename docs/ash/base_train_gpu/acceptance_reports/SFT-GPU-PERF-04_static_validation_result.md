# SFT-GPU-PERF-04 Static Validation Result

## Scope

Static validation for Batch Axis Train Plan / Active Token Matrix Seal.

## Checks

- [x] crates/lora_train/src/batch_axis_train_plan.rs_exists
- [x] crates/lora_train/src/batch_axis_train_plan.rs_brace_balance
- [x] crates/lora_train/src/batch_axis_train_plan.rs_paren_balance
- [x] crates/lora_train/src/batch_axis_train_plan.rs_bracket_balance
- [x] crates/lora_train/tests/batch_axis_train_plan.rs_exists
- [x] crates/lora_train/tests/batch_axis_train_plan.rs_brace_balance
- [x] crates/lora_train/tests/batch_axis_train_plan.rs_paren_balance
- [x] crates/lora_train/tests/batch_axis_train_plan.rs_bracket_balance
- [x] crates/lora_train/src/lib.rs_exists
- [x] crates/lora_train/src/lib.rs_brace_balance
- [x] crates/lora_train/src/lib.rs_paren_balance
- [x] crates/lora_train/src/lib.rs_bracket_balance
- [x] module_contains_pub struct BatchAxisTrainPlanInput
- [x] module_contains_pub struct BatchAxisActiveTokenEntry
- [x] module_contains_pub struct BatchAxisMicrobatchPlan
- [x] module_contains_pub struct BatchAxisTrainPlanReceipt
- [x] module_contains_pub enum BatchAxisTrainPlanError
- [x] module_contains_pub fn build_batch_axis_train_plan
- [x] module_contains_CpuPerTokenSerialLoopForbidden
- [x] module_contains_FullLogitsBufferForbidden
- [x] module_contains_LogitsReadbackForbidden
- [x] module_contains_PromptLossTokenDetected
- [x] module_contains_MissingTargetTokenId
- [x] module_contains_TargetTokenOutOfVocab
- [x] lib_contains_pub mod batch_axis_train_plan;
- [x] lib_contains_pub use batch_axis_train_plan::{
- [x] lib_contains_build_batch_axis_train_plan
- [x] test_contains_perf04_builds_active_token_matrix_from_response_mask
- [x] test_contains_perf04_rejects_prompt_loss_token_when_response_only_required
- [x] test_contains_perf04_rejects_missing_target_token_id
- [x] test_contains_perf04_rejects_target_token_out_of_vocab
- [x] test_contains_perf04_computes_hidden_row_offsets
- [x] test_contains_perf04_computes_target_vocab_tile_mapping
- [x] test_contains_perf04_splits_microbatches_preserving_original_batch_indices
- [x] test_contains_perf04_rejects_cpu_per_token_serial_loop_flag
- [x] test_contains_perf04_rejects_full_logits_or_readback_flags
- [x] test_contains_perf04_batch_axis_plan_fingerprint_is_deterministic

## Native Test Status

`cargo test -p lora_train --test batch_axis_train_plan -- --nocapture` was not executed in this container because cargo/rustc is unavailable.

## Result

PASS_STATIC
