# 16AI-QW-17 Baked Report

## Patch

`16AI-QW-17 — QWave SFT Train Dry-run / Side-channel Read Only Seal`

## Base

`ash_pass3_16AI-QW-16_qwave_feature_intake_cpu_gpu_parity_smoke_baked.zip`

## Added

```txt
crates/lora_train/src/qwave_sft_train_dry_run.rs
crates/lora_train/tests/qwave_sft_train_dry_run.rs
acceptance_reports/16AI-QW-17_qwave_sft_train_dry_run_side_channel_read_only.md
acceptance_reports/16AI-QW-17_static_validation_result.md
bake_artifacts/16AI-QW-17_BAKE_REPORT.md
```

## Modified

```txt
crates/lora_train/src/lib.rs
```

## Implemented SSOT

```txt
QWaveSftTrainDryRunInput
QWaveSftTrainDryRunPolicy
QWaveSftTrainDryRunRequestedMutations
QWaveSftTrainStepSnapshot
QWaveSftSideChannelReadReport
QWaveSftTrainDryRunComparisonReport
QWaveSftTrainDryRunManifest
QWaveSftTrainDryRunPlan
QWaveSftTrainDryRunReceipt
```

## Guard Summary

```txt
QW-12 intake receipt required
QW-16 parity receipt required
BaselineNoQWave snapshot required
QWaveSideChannelReadOnly snapshot required
side-channel attached required
side-channel read-only required
side-channel write count must be zero
baseline vs qwave token/logit/loss/gradient/optimizer/scheduler checksums must match
sample weights and curriculum order must remain unchanged
finite parity required
dry_run_only must remain true
```

## Rejection Summary

```txt
sample weight apply rejected
curriculum apply rejected
batch reorder rejected
loss rewrite rejected
gradient scaling rejected
optimizer mutation rejected
scheduler mutation rejected
direct logit mutation rejected
token id mutation rejected
vocab augmentation rejected
embedding resize rejected
new token creation rejected
LoRA routing finalization rejected
adapter pointer mutation rejected
sampler mutation rejected
backend switch rejected
GPU write buffer rejected
shader mutation rejected
```

## Validation

```txt
STATIC_VALIDATION: PASS
TEST_CASES: 48
NATIVE_RUST_TEST: NOT_RUN_TOOLCHAIN_UNAVAILABLE
```

## Next Patch

`16AI-QW-18 — QWave SFT Ablation Eval / Baseline vs Feature Side-channel Seal`
