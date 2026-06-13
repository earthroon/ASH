# SFT-GPU-STREAM-01 Bake Report

## Baked files

- `crates/ash_core/src/sft_gpu_stream_step_telemetry.rs`
- `crates/ash_core/tests/sft_gpu_stream_01_step_telemetry_receipt.rs`
- `crates/ash_core/src/lib.rs`
- `acceptance_reports/SFT-GPU-STREAM-01_native_gpu_lora_sft_step_telemetry_receipt.md`

## Seal line

SFT-GPU-STREAM-01 receives native GPU LoRA SFT step telemetry as evidence only. It records the step ledger digest and confirms GPU backend/device/sequence/finite-metric guards, while keeping training execution, artifact capture, slot ready, runtime attach, promotion, and current pointer update closed.

## Runtime status

Static bake only in this environment. Runtime GPU stream validation requires a local Rust toolchain and native GPU runner JSONL emission.
