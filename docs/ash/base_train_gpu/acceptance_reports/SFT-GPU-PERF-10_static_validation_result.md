# SFT-GPU-PERF-10 Static Validation Result

## Files Added

- `crates/lora_train/src/vocab_tail_shape_compile_cache.rs`
- `crates/lora_train/tests/vocab_tail_shape_compile_cache.rs`
- `acceptance_reports/SFT-GPU-PERF-10_vocab_tail_shape_compile_cache_pass2_dispatch_latency.md`
- `bake_artifacts/SFT-GPU-PERF-10_BAKE_REPORT.md`

## Files Updated

- `crates/lora_train/src/lib.rs`

## Static Checks

- module export present: `pub mod vocab_tail_shape_compile_cache;`
- public re-exports present for plan/receipt/input/error/decision/types/builders
- bridge present: `input_from_2d_dispatch_grid(...)`
- guard present: dynamic tail shape compile forbidden
- guard present: tail CPU fallback forbidden
- guard present: tail serial dispatch forbidden
- guard present: full logits buffer forbidden
- guard present: logits readback forbidden
- guard present: compile cache reuse after warmup
- guard present: pass2 dispatch latency threshold
- guard present: tail latency penalty threshold
- test file contains 10 PERF-10 acceptance tests
- brace/paren/bracket balance checked for changed Rust files

## Native Test Attempt

Command attempted:

```bash
cargo test -p lora_train --test vocab_tail_shape_compile_cache -- --nocapture
```

Result:

```txt
cargo: command not found
```

## Status

PASS_STATIC_STRUCTURE
PENDING_NATIVE_RUST_TESTS
PENDING_RUNTIME_GPU_TELEMETRY
