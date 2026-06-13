# MODELCORE-COMPILE-14 - LoRA Dump Config Path Seal

## Purpose

Seal the LoRA dump configuration SSOT before smoke/runtime execution.

This commit creates canonical dump configs and a local path validation script. It does not run the dump.

## Result

```text
STATUS: CONFIG_SSOT_CREATED_PATH_EXISTENCE_UNVERIFIED_IN_BAKE_ENVIRONMENT
```

The bake archive does not contain the local model/data assets referenced by the Windows absolute paths. Local validation remains required.

## Canonical Configs

```text
configs/lora_v5_guarded_dump_smoke.json
configs/lora_v5_guarded_dump_full.json
```

## Canonical Runtime Inputs

```text
model_path = D:\1111113232\DUST\1\ash_pass3\specs\model_spec_tinyllama_1p1b_v4.toml
tokenizer_path = D:\1111113232\DUST\1\ash_pass3\tokenizer_v5\artifacts\tokenizer_manifest_v5_final.json
teacher_full_model_path = D:\1111113232\DUST\1\ash_pass3\tokenizer_v5\artifacts\full_model_vocab_v5_resized.safetensors
train_jsonl = D:\1111113232\DUST\1\ash_pass3\v5_split\v5_guarded_lora_train.jsonl
eval_jsonl = D:\1111113232\DUST\1\ash_pass3\v5_split\v5_guarded_lora_val.jsonl
planned_layers = 6
bridge_dump_only = true
```

## Config Separation

### Smoke

```text
config = configs/lora_v5_guarded_dump_smoke.json
max_samples = 8
max_bridge_samples = 8
optimizer.max_steps = 1
output_dir = D:\1111113232\DUST\1\ash_pass3\workspace\lora_runs\tinyllama_1p1b_v5_guarded_dump_smoke
```

### Full

```text
config = configs/lora_v5_guarded_dump_full.json
max_samples = 60000
max_bridge_samples = 60000
optimizer.max_steps = 1000
output_dir = D:\1111113232\DUST\1\ash_pass3\workspace\lora_runs\tinyllama_1p1b_v5_guarded_dump_full
```

## Validation Command

Run from repo root on the machine that actually has the model/data files:

```powershell
.\scripts\validate_lora_dump_paths.ps1 -RepoRoot "D:\1111113232\DUST\1\ash_pass3"
```

## Expected PASS Conditions

```text
- both canonical config files exist
- training.bridge_dump_only=true
- bridge.enabled=true
- training.planned_layers=6
- model_path exists
- bridge.tokenizer_path exists
- bridge.teacher_full_model_path exists and points to full_model_vocab_v5_resized.safetensors
- dataset.train_jsonl_paths exist
- dataset.eval_jsonl exists
- feature_store_work_dir is set
- feature_store_archive_dir is set
```

## Non-Goals

```text
- no cargo check
- no lora_train execution
- no smoke dump execution
- no full dump execution
- no safetensors load verification
- no generated artifact correctness claim
```

## Next Gate

```text
MODELCORE-COMPILE-15: Smoke Dump Runtime Seal
```
