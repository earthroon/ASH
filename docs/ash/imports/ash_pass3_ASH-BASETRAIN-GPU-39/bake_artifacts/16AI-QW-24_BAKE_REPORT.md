# 16AI-QW-24 Bake Report

## Patch

`16AI-QW-24 — QWave-Conditioned SFT Smoke / Finite Loss & No Regression Seal`

## Base ZIP

`ash_pass3_16AI-QW-23_qwave_conditioning_train_candidate_baked.zip`

## Added / Modified

- Added `crates/lora_train/src/qwave_conditioned_sft_smoke.rs`
- Added `crates/lora_train/tests/qwave_conditioned_sft_smoke.rs`
- Updated `crates/lora_train/src/lib.rs`
- Added `acceptance_reports/16AI-QW-24_qwave_conditioned_sft_smoke.md`
- Added `acceptance_reports/16AI-QW-24_static_validation_result.md`
- Added `bake_artifacts/16AI-QW-24_BAKE_REPORT.md`

## Contract

QW-24 accepts a sandbox-only conditioned SFT smoke snapshot and verifies finite loss, finite gradients, bounded adapter/projection deltas, token/vocab/embedding immutability, base model immutability, pointer immutability, and baseline no-regression.

## Mutations Rejected

- production training apply
- runtime apply
- current pointer mutation
- artifact pointer mutation
- base model mutation
- token ID mutation
- vocab augmentation
- embedding resize
- new token creation
- unbounded adapter delta
- sampler mutation
- logit bias mutation
- direct logit mutation
- backend switch
- sample weight apply
- curriculum apply
- batch reorder
- loss rewrite
- global gradient scaling
- optimizer mutation outside sandbox
- scheduler mutation outside sandbox

## Validation

STATIC_VALIDATION: PASS  
NATIVE_RUST_TEST: NOT_RUN_TOOLCHAIN_UNAVAILABLE
