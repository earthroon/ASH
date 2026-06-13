# 16AI-QW-12 Static Validation Result

## Validation summary

```txt
PASS exists: crates/lora_train/src/qwave_sft_feature_intake.rs
PASS exists: crates/lora_train/tests/qwave_sft_feature_intake.rs
PASS exists: crates/lora_train/src/lib.rs
PASS module contains: QWaveSftFeatureIntakeReceipt
PASS module contains: QWaveSftFeatureTensorLoadReceipt
PASS module contains: QWaveSftSideChannelRegistration
PASS module contains: RejectedDirectLogitMutation
PASS module contains: RejectedLossRewrite
PASS module contains: RejectedTokenIdMutation
PASS module contains: RejectedVocabAugmentation
PASS module contains: RejectedEmbeddingResize
PASS module contains: RejectedNewTokenCreation
PASS module contains: RejectedLoraRoutingFinalization
PASS module contains: RejectedBackendSwitch
PASS module contains: RejectedOptimizerMutation
PASS module contains: RejectedSamplerMutation
PASS module contains: AcceptedReadOnlySideChannel
PASS module contains: loaded_as_side_channel
PASS module contains: affects_logits: false
PASS module contains: affects_loss: false
PASS module contains: affects_token_ids: false
PASS lib export: pub mod qwave_sft_feature_intake;
PASS lib export: build_qwave_sft_feature_intake_plan
PASS lib export: QWaveSftFeatureIntakeReceipt
PASS module brace balance
PASS test brace balance
PASS test functions >= 15
PASS test_count = 28
```

## Toolchain status

```txt
cargo: unavailable
rustc: unavailable
native compile/test: not run
```

## Recommended native command

```bash
cargo test -p lora_train qwave_sft_feature_intake
```
