# QW-53C Acceptance Report

## Status

`PATCH_IMPLEMENTED_PENDING_LOCAL_CARGO_RUNTIME_TRACE`

## Implemented files

```txt
crates/model_core/src/qw53c_loop_risk_signal_bridge.rs
crates/model_core/src/bin/qw53c_loop_risk_signal_bridge_validate.rs
crates/model_core/tests/qw53c_loop_risk_signal_validation.rs
crates/model_core/tests/qw53c_no_runtime_apply_validation.rs
crates/runtime/src/qw53c_loop_risk_signal.rs
crates/runtime/src/qw53c_risk_components.rs
crates/runtime/src/qw53c_trace_to_policy_bridge.rs
crates/runtime/src/qw53c_no_apply_invariant.rs
crates/runtime/src/bin/qw53c_trace_to_policy_bridge.rs
crates/runtime/tests/qw53c_loop_risk_signal_build.rs
crates/runtime/tests/qw53c_qwave_unavailable_explicit.rs
crates/runtime/tests/qw53c_no_apply_invariant.rs
crates/runtime/tests/qw53c_risk_band_threshold.rs
```

## Acceptance gates

- QW-53A JSONL can be converted into QW-53C LoopRiskSignal JSONL.
- QW-53B receipt is optionally ingested as decode context.
- `risk_score` is clamped to `[0.0, 1.0]`.
- Risk band maps deterministically to recommended policy.
- QWave unavailable is explicit, not silent.
- Runtime apply, token mutation, logit mutation, and sampler mutation remain forbidden.
- QW-53D can consume `workspace/policy/qw53c_loop_risk_signal_candidates.jsonl`.

## Local commands

```bash
cargo test -p runtime qw53c
cargo test -p model_core qw53c

cargo run -p runtime --bin qw53c_trace_to_policy_bridge -- . \
  --input workspace/runtime_traces/qw53a_real_runtime_topk_repeat_attractor_trace.jsonl \
  --output workspace/policy/qw53c_loop_risk_signal_candidates.jsonl \
  --qw53b-receipt workspace/trace/qw53b_subtitle_safe_sampled_decode_profile_receipt.json

cargo run -p model_core --bin qw53c_loop_risk_signal_bridge_validate -- .
```

## Environment limitation

The bake environment does not expose the pinned Rust toolchain or the local ASH checkpoint runtime. Final cargo/runtime acceptance must be run in the local ASH workspace.
