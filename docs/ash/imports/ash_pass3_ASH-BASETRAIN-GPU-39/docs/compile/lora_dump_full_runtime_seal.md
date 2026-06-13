# MODELCORE-COMPILE-16 - Full LoRA Dump Runtime Seal

## Purpose

Seal the full runtime gate for LoRA dump generation.

This gate executes the canonical full config created in MODELCORE-COMPILE-14 and verifies that the full dump command exits successfully and writes full-scale artifacts.

## Result

```text
STATUS: UNVERIFIED_IN_BAKE_ENVIRONMENT
```

The bake environment does not contain the local Windows model/data paths and does not provide a verified Cargo runtime. Local execution is required before changing this status to `PASS`.

## Runtime Command

Run from the repository root on the machine that has the tokenizer, resized full model, and JSONL split files:

```powershell
.\scripts\run_lora_dump_full.ps1 -RepoRoot "D:\1111113232\DUST\1\ash_pass3"
```

Recommended strict form after the smoke seal has passed:

```powershell
.\scripts\run_lora_dump_full.ps1 -RepoRoot "D:\1111113232\DUST\1\ash_pass3" -RequireSmokeSummary
```

Equivalent direct command:

```powershell
cargo run --manifest-path ".\crates\lora_train\Cargo.toml" --bin lora_train -- ".\configs\lora_v5_guarded_dump_full.json" 6
```

## Config SSOT

```text
config = configs/lora_v5_guarded_dump_full.json
planned_layers = 6
bridge_dump_only = true
bridge.enabled = true
dataset.max_samples = 60000
bridge.max_bridge_samples = 60000
optimizer.max_steps = 1000
```

## Required Preflight

The full script first runs:

```powershell
.\scripts\validate_lora_dump_paths.ps1 -RepoRoot "D:\1111113232\DUST\1\ash_pass3" -ConfigPaths @("configs\lora_v5_guarded_dump_full.json")
```

The gate must fail if any of these are missing:

```text
- model_path
- bridge.tokenizer_path
- bridge.teacher_full_model_path
- dataset.train_jsonl_paths
- dataset.eval_jsonl
```

The gate also fails if the full config accidentally points at smoke scale:

```text
- config path contains "smoke"
- dataset.max_samples <= 16
- bridge.max_bridge_samples <= 16
- checkpoints.output_dir contains "smoke"
```

## Expected Full Outputs

The full command should create at least one file under one or more of these paths:

```text
checkpoints.output_dir
bridge.feature_store_work_dir
bridge.feature_store_archive_dir
```

Canonical full output locations:

```text
output_dir = D:\1111113232\DUST\1\ash_pass3\workspace\lora_runs\tinyllama_1p1b_v5_guarded_dump_full
feature_store_work_dir = D:\1111113232\DUST\1\ash_pass3\workspace\lora_runs\tinyllama_1p1b_v5_guarded_dump_full\feature_store_work
feature_store_archive_dir = D:\1111113232\DUST\1\ash_pass3\workspace\lora_runs\tinyllama_1p1b_v5_guarded_dump_full\feature_store_archive
```

## Pass Criteria

```text
- full config path validation passes
- bridge_dump_only=true
- bridge.enabled=true
- planned_layers=6
- full config is not smoke scale
- cargo run exits with code 0
- no compile/runtime failure pattern appears in the full log
- at least one full output directory is created
- at least one full artifact file is written
- target/MODELCORE_COMPILE_16_lora_dump_full_summary.json is written with status=PASS
```

## Failure Routing

```text
model_core compile failure -> MODELCORE-COMPILE-12R
lora_train compile failure -> MODELCORE-COMPILE-13R
config/path failure -> MODELCORE-COMPILE-14R
smoke runtime failure -> MODELCORE-COMPILE-15R
full dump runtime failure -> MODELCORE-COMPILE-16R
```

## Scope Confirmation

This seal verifies only:

```text
- full LoRA dump runtime execution using configs/lora_v5_guarded_dump_full.json
```

This seal does not verify:

```text
- training quality
- generated adapter quality
- downstream inference quality
- performance baseline
- warning hygiene
```

## Final Gate

```text
MODELCORE-COMPILE-16 is the final LoRA dump runtime seal in this sequence.
```
