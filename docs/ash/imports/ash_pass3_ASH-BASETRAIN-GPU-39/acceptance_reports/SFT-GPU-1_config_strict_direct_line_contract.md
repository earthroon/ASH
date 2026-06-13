# SFT-GPU-1 Acceptance

## Status

STATIC-PASS / RUNTIME-PENDING

## Scope

Config Strict Schema + A-SFT Direct Line Contract Seal.

## Checked Files

- `crates/lora_train/src/config.rs`
- `crates/lora_train/src/scaffold.rs`
- `crates/lora_train/src/bin/lora_train.rs`
- `configs/ash_ko_short_sft_lm_head_lora_v1_smoke.json`
- `configs/ash_ko_short_sft_lm_head_lora_v1_train_200.json`
- `configs/ash_ko_short_sft_lm_head_lora_v1b_native_dump.json`
- `configs/ash_ko_short_sft_lm_head_lora_v1b_train_from_features.json`
- `docs/A_SFT_GPU_DIRECT_LINE.md`

## Required Contract

- [x] `family = sft_lora`
- [x] `mode = train`
- [x] `dataset.loss_on = response_only`
- [x] `training.plan_kind = module_lora`
- [x] `hyper.target_modules = ["lm_head"]`
- [x] `lora.targets = ["lm_head"]`
- [x] `lora.artifact_family = module_lora`
- [x] `lora.merge_mode = runtime_attach`
- [x] `guards.expect_target_key = lm_head`

## Gates

- [x] Unknown top-level config fields are rejected by `LoraTrainConfig`.
- [x] Unknown dataset fields are rejected by `DatasetConfig`.
- [x] Unknown optimizer fields are rejected by `OptimizerConfig`.
- [x] Unknown logging fields are rejected by `LoggingConfig`.
- [x] Unknown LoRA contract fields are rejected by `LoraContractConfig`.
- [x] Unknown guard fields are rejected by `SftGuardConfig`.
- [x] A-SFT config without `training.plan_kind=module_lora|module_local_lora` fails.
- [x] A-SFT config with `dataset.loss_on != response_only` fails.
- [x] A-SFT config with `lora.artifact_family != module_lora` fails.
- [x] A-SFT config with `hyper.target_modules != ["lm_head"]` fails.
- [x] A-SFT config with `lora.targets != ["lm_head"]` fails.
- [x] A-SFT config without guards contract fails.
- [x] Native dump phase may use `optimizer.max_steps=0` only when `a_sft_native_contract.phase=native_dump`.
- [x] Train-from-features phase requires non-empty `dataset.feature_store_manifest` when `require_feature_store_manifest=true`.

## Expected Contract Log

```txt
[lora_train][contract] family=sft_lora mode=train loss_on=response_only plan_kind=module_lora lora_targets=Some(["lm_head"]) artifact_family=module_lora expect_target_key=lm_head
```

## Non-goals

- Response-only loss mask execution is not implemented in this commit.
- GPU LoRA A/B update is not implemented in this commit.
- `lm_head` module target resolver is not implemented in this commit.
- Runtime logits delta verification is not implemented in this commit.

## Runtime Note

If the current tree fails after this commit with `no module targets resolved for module_lora training plan`, that is accepted as the SFT-GPU-1 boundary and should be handled by SFT-GPU-2.
