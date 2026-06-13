# SFT-GPU-BUILD-02 Bake Report

## Patch
LoRA Train Cargo Check Closure / Vocab Atlas Seal Report Drift Seal

## Files Modified
- crates/lora_train/src/lm_head_vocab_atlas_gpu_multistep.rs
- crates/lora_train/src/lm_head_runtime_delta_verify.rs

## Files Added
- acceptance_reports/SFT-GPU-BUILD-02_lora_train_cargo_check_closure.md
- acceptance_reports/SFT-GPU-BUILD-02_static_verification.log
- patch_reports/SFT-GPU-BUILD-02_bake_report.md
- docs/roadmap/SFT-GPU-BUILD-02_after_bake.md

## What Changed
- Replaced stale `seal.vocab_tile_size` / `seal.parallel_tile_groups` reads with the active vocab atlas config SSOT from `LoraTrainConfig.lm_head_vocab_atlas`.
- Preserved the group_count calculation; no arbitrary constant fallback was introduced.
- Added `Deserialize` derive to `LmHeadRuntimeDeltaVerifyReport` so quality evaluation can deserialize the JSON report via `serde_json::from_str`.

## Not Changed
- No runtime GPU train claim.
- No OBS-08 feature expansion.
- No sherpa-rs-sys closure.
- No deletion of vocab atlas quality checks.
