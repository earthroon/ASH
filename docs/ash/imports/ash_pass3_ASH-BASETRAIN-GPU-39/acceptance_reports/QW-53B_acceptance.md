# QW-53B Acceptance Report

## Status

`PATCH_IMPLEMENTED_PENDING_LOCAL_CARGO_RUNTIME_TRACE`

## Implemented files

```txt
crates/runtime/src/qw53b_subtitle_safe_sampled_profile.rs
crates/runtime/src/infer.rs
crates/runtime/src/lib.rs
crates/runtime/tests/qw53b_subtitle_safe_sampled_profile_materialization.rs
crates/runtime/tests/qw53b_no_greedy_default_trap.rs
crates/runtime/tests/qw53b_default_runtime_unchanged.rs
crates/runtime/tests/qw53b_explicit_enable_required.rs
crates/runtime/tests/qw53b_no_qwave_apply.rs
crates/model_core/src/qw53b_subtitle_safe_sampled_decode_profile.rs
crates/model_core/src/bin/qw53b_subtitle_safe_sampled_decode_profile_validate.rs
crates/model_core/tests/qw53b_decode_profile_receipt_validation.rs
```

## Acceptance gates

- Profile unset preserves runtime default.
- `subtitle_safe_sampled_v1` materializes sampled decode parameters.
- `requested_sampled_decode == true` for explicit profile.
- `decode_mode_after_materialization == sampled` for explicit profile.
- QWave/token/logit/model/LoRA mutation flags remain false.
- Receipt validation is performed in Rust model_core.

## Local commands

```bash
cargo test -p runtime qw53b
cargo test -p model_core qw53b

ASH_DECODE_PROFILE=subtitle_safe_sampled_v1 \
ASH_DECODE_SEED=42 \
ASH_QW53B_RECEIPT_DIR=. \
ASH_QW53A_TRACE=1 \
ASH_QW53A_TOPK=8 \
ASH_QW53A_REPEAT_WINDOW=32 \
cargo run -p runtime --example infer_only -- \
  --prompt-file workspace/probes/qw53b_subtitle_loop_probe.txt \
  --max-new-tokens 96

cargo run -p model_core --bin qw53b_subtitle_safe_sampled_decode_profile_validate -- .
```

## Environment limitation

The bake environment may not have the pinned Rust toolchain or full model checkpoint, so final runtime trace acceptance must be run on the local ASH workspace.
