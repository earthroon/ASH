# 16AI-QW-38G-R6A-R12 Bake Report

## Patch
`16AI-QW-38G-R6A-R12 — Root Cause Split Plan / Final Boundary vs LM Head Seal`

## Base
`ash_pass3_16AI-QW-38G-R6A-R10-R2_trace_backed_aggregation_baked.zip`

## Scope
This patch adds a no-mutation root cause split planner after the trace-backed multi-seed aggregation confirmed the token_id=13 reserved attractor with strong confidence at the final/projection boundary.

## Added
- R12 env gate in `crates/model_core/src/native_wgpu.rs`
- R12 root cause split plan writer
- R12 receipt writer
- R12 Markdown report writer
- R12 PowerShell runner
- R12 acceptance report

## Guard
The patch rejects production apply, full-vector readback, lm_head mutation, tokenizer mutation, and ban-mask mutation.

## Runtime Outputs
- `workspace/qw38g_r6a_r12_root_cause_split_plan.json`
- `workspace/qw38g_r6a_r12_root_cause_split_plan_receipt.json`
- `workspace/qw38g_r6a_r12_root_cause_split_plan_report.md`
- `workspace/infer_qw38g_r6a_r12_root_cause_split_plan_live.log`

## Validation
- Static validation: PASS_STATIC
- Cargo check: NOT_RUN_CONTAINER_CARGO_UNAVAILABLE
