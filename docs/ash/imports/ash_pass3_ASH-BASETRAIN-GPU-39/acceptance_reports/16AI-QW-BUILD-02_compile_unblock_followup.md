# 16AI-QW-BUILD-02 — QWave Compile Unblock Follow-up / Shadow, Export, Clamp, Borrow Seal

## Base

- `ash_pass3_16AI-QW-34A_dp_bridge_graph_scope_fix_baked.zip`

## Purpose

Fix the next compile blockers reported after the DP bridge graph scope patch, without weakening QWave SSOT contracts or bypassing QWave feature/telemetry logic.

## Fixed blockers

1. `tokenizer_core/tests/hangul_qwave_graph_serialization.rs`
   - Renamed the local variable in `qw10_rejects_graph_recompute_or_tokenizer_mutation` from `input` to `graph_input` so the helper function `input(...)` is no longer shadowed before the second call.

2. `crates/lora_train/src/lib.rs`
   - Resolved duplicate re-export of `qwave_runtime_canary_rollback_disable_ready` by aliasing the execution-gate export as `qwave_runtime_canary_execution_rollback_disable_ready`.

3. `crates/lora_train/src/lm_head_vocab_atlas_gpu_export.rs`
   - Added the three missing markdown format fields for:
     - `first_step_zero_a_delta_allowed`
     - `a_delta_required`
     - `b_delta_required`
   - This preserves the existing seal evidence instead of dropping unused arguments.

4. `crates/lora_train/src/qwave_conditioning_train_candidate.rs`
   - Annotated `score` as `f32` before `.clamp(0.0, 1.0)`.

5. `crates/lora_train/src/qwave_runtime_apply_gate.rs`
   - Annotated `score` as `f32` before `.clamp(0.0, 1.0)`.

6. `crates/lora_train/src/qwave_runtime_canary_apply_candidate.rs`
   - Annotated `score` as `f32` before `.clamp(0.0, 1.0)`.

7. `crates/lora_train/src/real_batch_parallel_train_run.rs`
   - Copied final-step scalar values before moving `step_receipts` into the receipt.
   - This resolves the borrow/move conflict while keeping final loss and LoRA delta evidence intact.

## Guard

- No QWave feature path was deleted.
- No tokenizer/vocab/embedding mutation was introduced.
- No sampler/backend/current/artifact/adapter/runtime pointer mutation was introduced.
- No silent fallback was added.
- No test expectation was changed to hide a regression.

## Native test status

- `cargo` is unavailable in this container.
- Native Rust tests were not executed here.
- Static validation was performed only.
