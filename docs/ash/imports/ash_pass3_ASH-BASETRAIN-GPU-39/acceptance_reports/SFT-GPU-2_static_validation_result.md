# SFT-GPU-2 Static Validation Result

[PASS] configs/ash_ko_short_sft_lm_head_lora_v1_smoke.json: family=sft_lora
[PASS] configs/ash_ko_short_sft_lm_head_lora_v1_smoke.json: loss_on=response_only
[PASS] configs/ash_ko_short_sft_lm_head_lora_v1_smoke.json: plan_kind=module_lora
[PASS] configs/ash_ko_short_sft_lm_head_lora_v1_smoke.json: hyper.target_modules=[lm_head]
[PASS] configs/ash_ko_short_sft_lm_head_lora_v1_smoke.json: lora.targets=[lm_head]
[PASS] configs/ash_ko_short_sft_lm_head_lora_v1_smoke.json: artifact_family=module_lora
[PASS] configs/ash_ko_short_sft_lm_head_lora_v1_train_200.json: family=sft_lora
[PASS] configs/ash_ko_short_sft_lm_head_lora_v1_train_200.json: loss_on=response_only
[PASS] configs/ash_ko_short_sft_lm_head_lora_v1_train_200.json: plan_kind=module_lora
[PASS] configs/ash_ko_short_sft_lm_head_lora_v1_train_200.json: hyper.target_modules=[lm_head]
[PASS] configs/ash_ko_short_sft_lm_head_lora_v1_train_200.json: lora.targets=[lm_head]
[PASS] configs/ash_ko_short_sft_lm_head_lora_v1_train_200.json: artifact_family=module_lora
[PASS] configs/ash_ko_short_sft_lm_head_lora_v1b_native_dump.json: family=sft_lora
[PASS] configs/ash_ko_short_sft_lm_head_lora_v1b_native_dump.json: loss_on=response_only
[PASS] configs/ash_ko_short_sft_lm_head_lora_v1b_native_dump.json: plan_kind=module_lora
[PASS] configs/ash_ko_short_sft_lm_head_lora_v1b_native_dump.json: hyper.target_modules=[lm_head]
[PASS] configs/ash_ko_short_sft_lm_head_lora_v1b_native_dump.json: lora.targets=[lm_head]
[PASS] configs/ash_ko_short_sft_lm_head_lora_v1b_native_dump.json: artifact_family=module_lora
[PASS] configs/ash_ko_short_sft_lm_head_lora_v1b_train_from_features.json: family=sft_lora
[PASS] configs/ash_ko_short_sft_lm_head_lora_v1b_train_from_features.json: loss_on=response_only
[PASS] configs/ash_ko_short_sft_lm_head_lora_v1b_train_from_features.json: plan_kind=module_lora
[PASS] configs/ash_ko_short_sft_lm_head_lora_v1b_train_from_features.json: hyper.target_modules=[lm_head]
[PASS] configs/ash_ko_short_sft_lm_head_lora_v1b_train_from_features.json: lora.targets=[lm_head]
[PASS] configs/ash_ko_short_sft_lm_head_lora_v1b_train_from_features.json: artifact_family=module_lora
[PASS] LM_HEAD_TARGET constant exists
[PASS] ModuleLoraTargetScope exists
[PASS] lm_head maps to Global
[PASS] module suffix maps to PerLayer
[PASS] MODULE_LOCAL_TRACE_TARGETS still excludes lm_head
[PASS] target_key_base returns LM_HEAD_TARGET for lm_head
[PASS] scaffold imports module_lora_target_scope
[PASS] resolved target struct exists
[PASS] resolve_module_targets returns Result scoped targets
[PASS] unsupported target errors explicitly
[PASS] global target bypasses layer loop
[PASS] per-layer target keeps layer loop
[PASS] duplicate target_key guard exists
[PASS] A-SFT requires exactly one attachment
[PASS] A-SFT requires target_key=lm_head
[PASS] CLI resolver log exists
[PASS] lib exports new target helpers
[PASS] docs updated with SFT-GPU-2
[PASS] acceptance report exists

STATIC-PASS checks= 43
