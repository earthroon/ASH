# SFT-GPU-8D Static Validation Result

Sandbox compile was not available; this is a static bake validation.

- [x] native dump entry exists (`crates/lora_train/src/sft_feature_store.rs`)
- [x] train from feature entry exists (`crates/lora_train/src/sft_feature_store.rs`)
- [x] lm_head snapshot writer exists (`crates/lora_train/src/sft_feature_store.rs`)
- [x] lm_head-only loader exists (`crates/lora_train/src/sft_feature_store.rs`)
- [x] uses existing FeatureStoreManifest (`crates/lora_train/src/sft_feature_store.rs`)
- [x] response-only stats validated (`crates/lora_train/src/sft_feature_store.rs`)
- [x] manifest path sealed (`crates/lora_train/src/sft_feature_store.rs`)
- [x] small lm_head snapshot sealed (`crates/lora_train/src/sft_feature_store.rs`)
- [x] native dump CLI route exists (`crates/lora_train/src/bin/lora_train.rs`)
- [x] train from features CLI route exists (`crates/lora_train/src/bin/lora_train.rs`)
- [x] lib module exported (`crates/lora_train/src/lib.rs`)
- [x] native dump export exists (`crates/lora_train/src/lib.rs`)
- [x] train config points to native dump manifest (`configs/ash_ko_short_sft_lm_head_lora_v1b_train_from_features.json`)
- [x] acceptance documents lm_head snapshot (`acceptance_reports/SFT-GPU-8D_native_dump_feature_store_bridge.md`)

PASS_STATIC 14 / 14
