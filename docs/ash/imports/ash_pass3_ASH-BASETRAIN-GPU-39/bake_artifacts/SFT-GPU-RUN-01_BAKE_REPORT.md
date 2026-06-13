# SFT-GPU-RUN-01 Bake Report

## Commit

SFT-GPU-RUN-01 — Strict Native GPU LoRA Train Run / No CPU Fallback Seal

## Base

Baked on top of `ash_pass3_SFT-FFN-LORA-16_slot_action_apply_baked.zip`.

## Added

- `crates/ash_core/src/sft_gpu_strict_train_run.rs`
- `crates/ash_core/tests/sft_gpu_run_01_strict_native_gpu.rs`
- `crates/lora_train/src/strict_native_gpu_run.rs`
- `crates/lora_train/tests/strict_native_gpu_run.rs`
- `crates/burn_webgpu_backend/src/strict_gpu_train_receipt.rs`
- `crates/burn_webgpu_backend/tests/strict_gpu_train_receipt.rs`
- `acceptance_reports/SFT-GPU-RUN-01_strict_native_gpu_lora_train.md`

## Modified

- `crates/ash_core/src/lib.rs`
- `crates/lora_train/src/lib.rs`
- `crates/lora_train/Cargo.toml`
- `crates/burn_webgpu_backend/src/lib.rs`

## Opened

- strict native GPU LoRA train run
- native GPU backend receipt
- no CPU fallback receipt
- GPU train step receipt
- adapter update receipt
- optimizer accounting receipt
- adapter artifact output receipt
- save-reload parity receipt

## Closed

- CPU fallback
- CPU materialized train path
- silent backend demotion
- runtime current pointer update
- promotion apply
- lifecycle mutation
- slot action apply
- ASH current binding

## Notes

This bake is static-only in the current environment because `cargo`, `rustc`, and `rustfmt` are unavailable. Runtime acceptance requires an actual strict GPU run on the target machine.
