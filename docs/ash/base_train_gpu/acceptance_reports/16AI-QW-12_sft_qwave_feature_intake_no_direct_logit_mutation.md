# 16AI-QW-12 — SFT QWave Feature Intake / No Direct Logit Mutation Seal

## 0. SSOT

- Base ZIP: `ash_pass3_16AI-QW-11_qwave_sft_feature_export_baked.zip`
- Previous sealed patch: `16AI-QW-11 — QWave SFT Feature Export / Pulse Vector Batch Matrix Seal`
- New intake SSOT: `QWaveSftFeatureIntakeReceipt`
- New module: `crates/lora_train/src/qwave_sft_feature_intake.rs`
- New test fixture: `crates/lora_train/tests/qwave_sft_feature_intake.rs`

## 1. Patch intent

QW-12 consumes the QW-11 side-channel feature export metadata and registers the QWave feature matrix into `lora_train` as a read-only SFT side-channel.

The patch intentionally does **not** mutate token ids, vocab, embeddings, logits, loss, optimizer, sampler, backend route, or LoRA routing.

## 2. Added files

```txt
crates/lora_train/src/qwave_sft_feature_intake.rs
crates/lora_train/tests/qwave_sft_feature_intake.rs
acceptance_reports/16AI-QW-12_sft_qwave_feature_intake_no_direct_logit_mutation.md
acceptance_reports/16AI-QW-12_static_validation_result.md
bake_artifacts/16AI-QW-12_BAKE_REPORT.md
```

## 3. Modified files

```txt
crates/lora_train/src/lib.rs
```

`lib.rs` now exports:

```rust
pub mod qwave_sft_feature_intake;

pub use qwave_sft_feature_intake::{
    build_qwave_sft_feature_intake_plan,
    build_qwave_sft_feature_intake_plan_and_receipt,
    build_qwave_sft_feature_intake_receipt,
    evaluate_qwave_sft_feature_intake_rejection,
    QWaveSftFeatureDType, QWaveSftFeatureIntakeDecision, QWaveSftFeatureIntakeError,
    QWaveSftFeatureIntakeInput, QWaveSftFeatureIntakeManifest,
    QWaveSftFeatureIntakePlan, QWaveSftFeatureIntakePolicy,
    QWaveSftFeatureIntakeReceipt, QWaveSftFeatureLayout,
    QWaveSftFeatureRequestedMutations, QWaveSftFeatureTensorLoadReceipt,
    QWaveSftSideChannelRegistration,
};
```

## 4. New SSOT objects

```txt
QWaveSftFeatureIntakeInput
QWaveSftFeatureIntakePolicy
QWaveSftFeatureRequestedMutations
QWaveSftFeatureTensorLoadReceipt
QWaveSftSideChannelRegistration
QWaveSftFeatureIntakeManifest
QWaveSftFeatureIntakePlan
QWaveSftFeatureIntakeReceipt
```

## 5. Guard contract

### Accepted path

```txt
QW-11 export receipt id/fingerprint present
feature matrix path/fingerprint present
feature mask path/fingerprint present
coverage mask path/fingerprint present
SFT batch plan id/fingerprint present
batch/sequence/feature_dim match expected SFT plan shape
dtype/layout match expected intake policy
feature values finite
token ids before/after fingerprints unchanged
requested mutation flags all false
side-channel registration enabled
```

### Rejected path

```txt
missing QW-11 receipt
missing matrix fingerprint
missing feature mask
missing coverage mask
shape mismatch
dtype mismatch
layout mismatch
non-finite feature value
token id mutation
direct logit mutation
loss rewrite
vocab augmentation
embedding resize
new token creation
LoRA routing finalization
backend switch
optimizer mutation
sampler mutation
side-channel registration disabled
```

## 6. Read-only side-channel seal

The side-channel registration is sealed with:

```txt
read_only = true
affects_logits = false
affects_loss = false
affects_token_ids = false
affects_vocab = false
affects_embeddings = false
affects_lora_routing = false
affects_optimizer = false
affects_sampler = false
```

## 7. Test coverage added

The integration test file contains 28 test cases covering:

```txt
PASS — consumes QW-11 feature export receipt
PASS — builds read-only side-channel registration
PASS — verifies matrix shape against SFT batch plan
PASS — verifies feature/coverage masks
PASS — preserves token ids
PASS — allows sample/curriculum candidate metadata flags only
PASS — deterministic intake receipt
FAIL — rejects missing QW-11 receipt
FAIL — rejects missing matrix fingerprint
FAIL — rejects missing feature mask
FAIL — rejects missing coverage mask
FAIL — rejects batch size mismatch
FAIL — rejects sequence length mismatch
FAIL — rejects feature dim mismatch
FAIL — rejects dtype mismatch
FAIL — rejects layout mismatch
FAIL — rejects non-finite feature matrix
FAIL — rejects token id mutation
FAIL — rejects direct logit mutation
FAIL — rejects loss rewrite
FAIL — rejects vocab augmentation
FAIL — rejects embedding resize
FAIL — rejects new token creation
FAIL — rejects LoRA routing finalization
FAIL — rejects backend switch
FAIL — rejects optimizer mutation
FAIL — rejects sampler mutation
```

## 8. Native test status

Native Rust tests were not executed in this container because `cargo` and `rustc` are unavailable.

Recommended validation on a Rust-enabled machine:

```bash
cargo test -p lora_train qwave_sft_feature_intake
cargo test -p lora_train
cargo test -p tokenizer_core hangul_qwave_sft_feature_export
```

## 9. Acceptance status

```txt
STATIC_VALIDATION: PASS
NATIVE_RUST_TEST: NOT_RUN_TOOLCHAIN_UNAVAILABLE
PATCH_STATUS: BAKED
```
