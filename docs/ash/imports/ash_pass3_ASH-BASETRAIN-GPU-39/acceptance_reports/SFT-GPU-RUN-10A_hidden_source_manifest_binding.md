# SFT-GPU-RUN-10A Acceptance Report

## Source Failure
- previous_failure: [A-SFT][hidden_source_guard]
- native_bootstrap_passed_before_failure: true
- failure_phase: direct_train
- forbidden_source: full checkpoint-backed teacher

## Hidden Source Binding
- hidden_source_config_added: true
- feature_store_manifest_path: workspace/lora_runs/ash_ko_short_sft_lm_head_lora_v1_smoke/feature_store_work/feature_store_manifest.json
- train_config_phase: train_from_features
- native_dump_config_added: configs/ash_ko_short_sft_lm_head_lora_v1_smoke.native_dump.json
- allow_direct_checkpoint_teacher_in_train: false

## Guard Decision
- direct checkpoint teacher guard preserved: true
- missing manifest rejected: true
- manifest mode accepted when file exists: true
- atlas grouped hidden provider mode accepted: true

## Verification
- cargo test -p lora_train --test sft_gpu_hidden_source_manifest_binding -- --nocapture
- cargo run -p lora_train -- .\configs\ash_ko_short_sft_lm_head_lora_v1_smoke.native_dump.json 1
- cargo run -p lora_train -- .\configs\ash_ko_short_sft_lm_head_lora_v1_smoke.json 1

## Result
- static_bake_completed: true
- runtime_execution_required_on_target_machine: true
