# MODELCORE-COMPILE-13 - LoRA Train Compile Seal

## Purpose

Seal `lora_train` compile status after `model_core` compile repair.

## Command

```powershell
cargo check -p lora_train 2>&1 | Tee-Object ".\target\MODELCORE_COMPILE_13_lora_train_check.log"
```

Fallback:

```powershell
cargo check --manifest-path ".\crates\lora_train\Cargo.toml" 2>&1 | Tee-Object ".\target\MODELCORE_COMPILE_13_lora_train_check.log"
```

## Result

```text
STATUS: UNVERIFIED_IN_BAKE_ENVIRONMENT
compile_errors: UNKNOWN_UNTIL_LOCAL_CARGO_CHECK
```

## Scope Confirmation

This seal verifies only `crates/lora_train` compile status after local validation. It does not verify dump config paths, tokenizer files, safetensors loading, smoke dump runtime, full dump runtime, artifacts, or performance.
