# QW-53A Acceptance

## Status

`PATCH_IMPLEMENTED_PENDING_LOCAL_CARGO_RUNTIME_TRACE`

## Implemented

- Rust runtime trace capture module added.
- Rust model_core schema/validator/report module added.
- Runtime inference path now calls QW-53A capture from Rust when `ASH_QW53A_TRACE=1`.
- S6 compatibility output path is written by the same Rust writer.
- No token/logit/sampler mutation path was added.
- No TypeScript/JavaScript was added outside frontend scope.

## Not executed in this bake environment

- `cargo check`
- `cargo test`
- real checkpoint inference

Reason: this container does not expose `cargo` or `rustc`.

## Local execution

```bash
ASH_QW53A_TRACE=1 \
ASH_QW53A_TOPK=8 \
ASH_QW53A_REPEAT_WINDOW=32 \
ASH_QW53A_OUTPUT_DIR=. \
cargo run -p runtime --example infer_only -- --prompt-file workspace/probes/qw53a_loop_probe.txt --max-new-tokens 96

cargo run -p model_core --bin qw53a_real_runtime_topk_repeat_attractor_trace -- .
cargo run -p model_core --bin qw53a_real_runtime_topk_repeat_attractor_trace_validate -- .
cargo run -p model_core --bin qw52c_r13_s6_runtime_topk_shadow_observation_replay -- .
```
