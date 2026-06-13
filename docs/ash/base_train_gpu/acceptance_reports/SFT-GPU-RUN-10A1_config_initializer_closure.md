# SFT-GPU-RUN-10A1 Acceptance Report

## Scope
- previous_patch: SFT-GPU-RUN-10A
- issue: `LoraTrainConfig` gained `hidden_source`, but `build_config_from_specs()` in `pipeline.rs` used a manual struct literal without the new field.
- error: `E0063 missing field hidden_source in initializer of LoraTrainConfig`

## Fix
- file: `crates/lora_train/src/pipeline.rs`
- change: added `hidden_source: None` to the manual `LoraTrainConfig` initializer in `build_config_from_specs()`.

## Guard Contract
- hidden_source_guard_removed: false
- direct_checkpoint_teacher_allowed_in_train: false
- default_pipeline_generated_config_keeps_hidden_source_unbound: true
- explicit smoke config hidden_source binding remains in `configs/ash_ko_short_sft_lm_head_lora_v1_smoke.json`.

## Verification
- static_pattern_pipeline_initializer_has_hidden_source: true
- cargo_test_required_locally: true

## Suggested Local Command
```powershell
cargo test -p lora_train --test sft_gpu_hidden_source_manifest_binding -- --nocapture
cargo run -p lora_train -- .\configs\ash_ko_short_sft_lm_head_lora_v1_smoke.native_dump.json 1
cargo run -p lora_train -- .\configs\ash_ko_short_sft_lm_head_lora_v1_smoke.json 1
```
