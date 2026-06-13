# MODELCORE-COMPILE-14 - LoRA Dump Config Path Seal

## Purpose

Create canonical LoRA dump configs and a local validation script before smoke/full runtime execution.

## Changed Files

- configs/lora_v5_guarded_dump_smoke.json
- configs/lora_v5_guarded_dump_full.json
- scripts/validate_lora_dump_paths.ps1
- docs/compile/lora_dump_config_path_seal.md
- patch_reports/MODELCORE_COMPILE_14_LORA_DUMP_CONFIG_PATH_SEAL.md

## Changes

- Added smoke dump config with `bridge_dump_only=true` and `max_bridge_samples=8`.
- Added full dump config with `bridge_dump_only=true` and `max_bridge_samples=60000`.
- Bound tokenizer SSOT to `tokenizer_v5/artifacts/tokenizer_manifest_v5_final.json`.
- Bound teacher checkpoint SSOT to `tokenizer_v5/artifacts/full_model_vocab_v5_resized.safetensors`.
- Bound dataset SSOT to `v5_split/v5_guarded_lora_train.jsonl` and `v5_split/v5_guarded_lora_val.jsonl`.
- Added PowerShell validator for local path existence and key config booleans.

## Non-Goals

- No Rust source changes.
- No cargo check.
- No smoke dump runtime execution.
- No full dump runtime execution.
- No generated dump artifact claim.

## Validation

```powershell
.\scripts\validate_lora_dump_paths.ps1 -RepoRoot "D:\1111113232\DUST\1\ash_pass3"
```

## Status

CONFIG_SSOT_CREATED_PATH_EXISTENCE_UNVERIFIED_IN_BAKE_ENVIRONMENT.
