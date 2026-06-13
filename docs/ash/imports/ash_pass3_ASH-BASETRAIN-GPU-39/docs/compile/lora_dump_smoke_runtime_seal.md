# MODELCORE-COMPILE-15 - Smoke Dump Runtime Seal

## Purpose

Seal the smoke runtime gate for LoRA dump generation.

This gate executes the canonical smoke config created in MODELCORE-COMPILE-14 and verifies that the dump command exits successfully and writes smoke artifacts.

## Result

```text
STATUS: UNVERIFIED_IN_BAKE_ENVIRONMENT
```

The bake environment does not contain the local Windows model/data paths and does not provide a verified Cargo runtime. Local execution is required before changing this status to `PASS`.

## Runtime Command

Run from the repository root on the machine that has the tokenizer, resized full model, and JSONL split files:

```powershell
.\scripts\run_lora_dump_smoke.ps1 -RepoRoot "D:\1111113232\DUST\1\ash_pass3"
```

Equivalent direct command:

```powershell
cargo run --manifest-path ".\crates\lora_train\Cargo.toml" --bin lora_train -- ".\configs\lora_v5_guarded_dump_smoke.json" 6
```

## Config SSOT

```text
config = configs/lora_v5_guarded_dump_smoke.json
planned_layers = 6
bridge_dump_only = true
bridge.enabled = true
dataset.max_samples = 8
bridge.max_bridge_samples = 8
optimizer.max_steps = 1
```

## Required Preflight

The smoke script first runs:

```powershell
.\scripts\validate_lora_dump_paths.ps1 -RepoRoot "D:\1111113232\DUST\1\ash_pass3" -ConfigPaths @("configs\lora_v5_guarded_dump_smoke.json")
```

The gate must fail if any of these are missing:

```text
- model_path
- bridge.tokenizer_path
- bridge.teacher_full_model_path
- dataset.train_jsonl_paths
- dataset.eval_jsonl
```

## Expected Smoke Outputs

The smoke command should create at least one file under one or more of these paths:

```text
checkpoints.output_dir
bridge.feature_store_work_dir
bridge.feature_store_archive_dir
```

Canonical smoke output locations:

```text
output_dir = D:\1111113232\DUST\1\ash_pass3\workspace\lora_runs\tinyllama_1p1b_v5_guarded_dump_smoke
feature_store_work_dir = D:\1111113232\DUST\1\ash_pass3\workspace\lora_runs\tinyllama_1p1b_v5_guarded_dump_smoke\feature_store_work
feature_store_archive_dir = D:\1111113232\DUST\1\ash_pass3\workspace\lora_runs\tinyllama_1p1b_v5_guarded_dump_smoke\feature_store_archive
```

## Pass Criteria

```text
- smoke config path validation passes
- cargo run exits with code 0
- no compile/runtime failure pattern appears in the smoke log
- at least one smoke output directory is created
- at least one smoke artifact file is written
- target/MODELCORE_COMPILE_15_lora_dump_smoke_summary.json is written with status=PASS
```

## Failure Routing

```text
model_core compile failure -> MODELCORE-COMPILE-12R
lora_train compile failure -> MODELCORE-COMPILE-13R
config/path failure -> MODELCORE-COMPILE-14R
smoke runtime failure -> MODELCORE-COMPILE-15R
full dump scale/runtime failure -> MODELCORE-COMPILE-16 or 16R
```

## Scope Confirmation

This seal verifies only:

```text
- smoke dump runtime execution using configs/lora_v5_guarded_dump_smoke.json
```

This seal does not verify:

```text
- full dump runtime
- full dataset completion
- full artifact quality
- training quality
- performance baseline
- warning hygiene
```

## Next Gate

```text
MODELCORE-COMPILE-16: Full LoRA Dump Runtime Seal
```
