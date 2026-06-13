# 16AI-QW-38G-R1 Bake Report

## Patch
16AI-QW-38G-R1 — Rust-native Layerwise Trace Closure / No PowerShell Postprocess Seal

## Base
`ash_pass3_16AI-QW-38G_layerwise_reserved_direction_baked.zip`

## Changed Files
- `crates/model_core/src/native_wgpu.rs`
- `scripts/run_16AI_QW_38G_layerwise_reserved_direction.ps1`
- `acceptance_reports/16AI-QW-38G-R1_rust_native_layerwise_trace_closure.md`
- `patch_reports/16AI-QW-38G-R1_native_wgpu.diff`
- `patch_reports/16AI-QW-38G-R1_runner.diff`
- `target/16AI-QW-38G-R1_static_validation.json`

## What Changed
- Added Rust-native `qw38g_record_event()` path.
- Layerwise events are accumulated in Rust and summarized by Rust.
- Rust writes summary JSON and runtime receipt directly.
- Runner no longer calls Python summarize script.
- Runner builds `infer_only` in release mode and runs the exe directly.

## Runtime Outputs
- `workspace/qw38g_layerwise_reserved_direction_trace.jsonl`
- `workspace/qw38g_layerwise_reserved_direction_summary.json`
- `workspace/qw38g_runtime_receipt.json`

## Validation
- Static validation: PASS_STATIC
- Cargo check/build: NOT_RUN_CONTAINER_CARGO_UNAVAILABLE

## Non-mutation Seal
- No safetensors mutation.
- No tokenizer mutation.
- No banlist mutation.
- No weight mutation.
