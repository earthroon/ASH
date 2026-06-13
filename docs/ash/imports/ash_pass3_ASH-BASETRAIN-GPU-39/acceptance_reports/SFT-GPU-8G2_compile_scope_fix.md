# SFT-GPU-8G2 compile scope fix

## Status
PASS_STATIC

## Fix
- `crates/lora_train/src/model.rs`
- Added `let target_key_string = target_key.into();` inside `TrainableLoraAdapter::new(...)` before the struct initializer.

## Reason
The 8G guard patch introduced `target_key` ownership tracking in adapter structs. `TrainableModuleLoraAdapter::from_base_weight(...)` already declared `target_key_string`, but `TrainableLoraAdapter::new(...)` still referenced `target_key_string` without declaring it, causing:

```text
error[E0425]: cannot find value `target_key_string` in this scope
```

## Validation
```text
python tools/validate_sft_gpu_8g_static.py
PASS count: 19
[PASS_STATIC] SFT-GPU-8G lm_head vocab atlas grouped parallel projection / streaming CE seal
```

## Runtime note
Cargo/WGPU runtime validation must be re-run in the target environment.
