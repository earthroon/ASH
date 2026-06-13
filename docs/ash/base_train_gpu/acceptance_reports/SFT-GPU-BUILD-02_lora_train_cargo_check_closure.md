# SFT-GPU-BUILD-02 Acceptance Report

## Scope
- sherpa_rs_sys_excluded_from_main_gpu_sft_check: true
- check_command: cargo check -p ash_core -p lora_train -p burn_webgpu_backend

## Source Error Layer
- previous_layer: ash_core BUILD-01 closure
- current_layer: lora_train
- initial_error_count: 5

## Vocab Atlas Seal Report Drift
- GpuVocabAtlasTrainStepSealReport audited: true
- vocab_tile_size_source: LoraTrainConfig.lm_head_vocab_atlas.vocab_tile_size
- parallel_tile_groups_source: LoraTrainConfig.lm_head_vocab_atlas.parallel_tile_groups
- group_count_calculation_preserved: true
- arbitrary_constant_fallback_used: false
- vocab_size_used_as_tile_size: false

## Runtime Delta Verify Deserialize
- LmHeadRuntimeDeltaVerifyReport_deserialize_enabled: true
- nested_deserialize_errors: not observed in static bake container
- serde_skip_used: false
- quality_eval_json_load_preserved: true

## Verification
- static_pattern_scan: pass
- cargo check -p ash_core -p lora_train -p burn_webgpu_backend: not run in bake container; cargo unavailable

## Result
- check_passed: judgment_pending_local_cargo_check
- remaining_errors: unknown_until_local_check
- remaining_warnings: unknown_until_local_check
