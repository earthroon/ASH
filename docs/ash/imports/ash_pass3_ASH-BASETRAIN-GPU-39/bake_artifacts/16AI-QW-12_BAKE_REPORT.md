# 16AI-QW-12 Bake Report

## Patch

```txt
16AI-QW-12 — SFT QWave Feature Intake / No Direct Logit Mutation Seal
```

## Base

```txt
ash_pass3_16AI-QW-11_qwave_sft_feature_export_baked.zip
```

## Baked changes

```txt
Added lora_train QWave SFT feature intake module.
Added intake receipt/manifest/plan/tensor-load receipt/side-channel registration SSOT objects.
Added strict mutation guard for token/logit/loss/vocab/embedding/new-token/LoRA/backend/optimizer/sampler mutation requests.
Added read-only side-channel registration seal.
Added deterministic fingerprinted plan and receipt builders.
Added 28 integration tests for pass/fail guard behavior.
Updated crates/lora_train/src/lib.rs exports.
Added acceptance report and static validation report.
```

## Guard outcome

```txt
QW-11 receipt consumption: implemented
Feature matrix manifest/path/fingerprint validation: implemented
Feature mask validation: implemented
Coverage mask validation: implemented
SFT batch shape alignment: implemented
DType/layout alignment: implemented
Finite feature validation: implemented
Token id unchanged seal: implemented
Read-only side-channel registration: implemented
Direct logit mutation reject: implemented
Loss rewrite reject: implemented
Vocab augmentation reject: implemented
Embedding resize reject: implemented
New token creation reject: implemented
LoRA routing finalization reject: implemented
Backend switch reject: implemented
Optimizer mutation reject: implemented
Sampler mutation reject: implemented
```

## Native validation status

```txt
cargo/rustc unavailable in current container.
Static validation passed.
Native Rust test must be run in a Rust-enabled environment.
```

## Next patch

```txt
16AI-QW-13 — QWave Feature Coverage Telemetry / Batch Korean Structure Ratio Seal
```
