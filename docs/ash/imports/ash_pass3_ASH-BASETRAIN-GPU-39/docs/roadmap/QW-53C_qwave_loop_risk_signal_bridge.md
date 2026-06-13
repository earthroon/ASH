# QW-53C Roadmap

## Goal

Bridge QW-53A repeat attractor trace and QW-53B decode context into a deterministic candidate policy JSONL.

## Implemented surface

```txt
crates/model_core/src/qw53c_loop_risk_signal_bridge.rs
crates/model_core/src/bin/qw53c_loop_risk_signal_bridge_validate.rs
crates/runtime/src/qw53c_loop_risk_signal.rs
crates/runtime/src/qw53c_risk_components.rs
crates/runtime/src/qw53c_trace_to_policy_bridge.rs
crates/runtime/src/qw53c_no_apply_invariant.rs
crates/runtime/src/bin/qw53c_trace_to_policy_bridge.rs
```

## Commands

```bash
cargo run -p runtime --bin qw53c_trace_to_policy_bridge -- . \
  --input workspace/runtime_traces/qw53a_real_runtime_topk_repeat_attractor_trace.jsonl \
  --output workspace/policy/qw53c_loop_risk_signal_candidates.jsonl \
  --qw53b-receipt workspace/trace/qw53b_subtitle_safe_sampled_decode_profile_receipt.json

cargo run -p model_core --bin qw53c_loop_risk_signal_bridge_validate -- . \
  --input workspace/policy/qw53c_loop_risk_signal_candidates.jsonl \
  --output workspace/trace/qw53c_loop_risk_signal_bridge_validation.json
```

## Required local proof

Run with a real QW-53A runtime trace. The baked environment does not include the local checkpoint/runtime execution context.
