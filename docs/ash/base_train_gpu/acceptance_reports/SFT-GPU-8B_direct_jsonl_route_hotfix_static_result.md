# SFT-GPU-8B Direct JSONL Route Hotfix Static Result

## Status

PASS_STATIC

## Trigger Log

The user run reached:

```txt
[lora_train] plan kind: module_local_lora
[lora_train] target modules: lm_head
[lora_train] target key count: 1
[lora_train][module_lora_resolver] target=lm_head scope=global target_key=lm_head
[lora_train] module_lora bundle complete targets=0 feature_batches=0
```

This means SFT-GPU-1 and SFT-GPU-2 passed, but the binary routed response-only `lm_head` SFT into the legacy module-lora bundle branch before the direct JSONL SFT path could run.

## Patch

- `crates/lora_train/src/bin/lora_train.rs`
  - Added an early `response_only_direct_jsonl` route before `plan.plan_kind.is_module_local()`.
  - The route requires:
    - `dataset.loss_on == response_only`
    - no `dataset.feature_store_manifest`
    - `bridge.enabled == true`
    - `bridge.extract_only == false`
  - It calls `run_direct_jsonl_training_loop()` directly.

- `crates/lora_train/src/sft_lm_head_artifact.rs`
  - `sft_lm_head_artifact_dir()` now avoids double nesting when `checkpoints.output_dir` already ends with `lm_head_lora`.

## Expected Next Log

```txt
[lora_train] A-SFT response-only direct JSONL path selected before module_lora bundle
[lora_train] direct JSONL training path enabled (no feature store dump)
[lora_train][sft_mask] loss_on=response_only shift=builder ignore_index=-100
```

The old terminal line below should no longer be the terminal result for this config:

```txt
[lora_train] module_lora bundle complete targets=0 feature_batches=0
```

## Remaining Runtime Scope

This report is static-only. Compile and WGPU runtime smoke must be run in the user's Rust environment.
