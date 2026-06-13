# 16AI-QW-17 Static Validation Result

```txt
STATIC_VALIDATION: PASS
NATIVE_RUST_TEST: NOT_RUN_TOOLCHAIN_UNAVAILABLE
```

## File Checks

```txt
PASS crates/lora_train/src/qwave_sft_train_dry_run.rs
PASS crates/lora_train/tests/qwave_sft_train_dry_run.rs
PASS crates/lora_train/src/lib.rs
PASS acceptance_reports/16AI-QW-17_qwave_sft_train_dry_run_side_channel_read_only.md
PASS bake_artifacts/16AI-QW-17_BAKE_REPORT.md
```

## Required Symbol Checks

```txt
PASS QWaveSftTrainDryRunReceipt
PASS QWaveSftTrainStepSnapshot
PASS QWaveSftSideChannelReadReport
PASS QWaveSftTrainDryRunComparisonReport
PASS AcceptedSideChannelReadOnlyDryRun
PASS RejectedMissingQw12IntakeReceipt
PASS RejectedMissingQw16ParityReceipt
PASS RejectedSideChannelNotAttached
PASS RejectedSideChannelNotReadOnly
PASS RejectedSideChannelWriteDetected
PASS RejectedTrainResultChanged
PASS RejectedLogitsMismatch
PASS RejectedLossMismatch
PASS RejectedGradientMismatch
PASS RejectedOptimizerStateMismatch
PASS RejectedSchedulerStateMismatch
PASS RejectedSampleWeightsMismatch
PASS RejectedCurriculumOrderMismatch
PASS RejectedSampleWeightApply
PASS RejectedCurriculumApply
PASS RejectedLossRewrite
PASS RejectedGradientScaling
PASS RejectedOptimizerMutation
PASS RejectedSchedulerMutation
PASS RejectedDirectLogitMutation
PASS RejectedBackendSwitch
```

## Test Count

```txt
PASS test functions >= 40
ACTUAL 48
```

## Brace Balance

```txt
PASS crates/lora_train/src/qwave_sft_train_dry_run.rs
PASS crates/lora_train/tests/qwave_sft_train_dry_run.rs
PASS crates/lora_train/src/lib.rs
```

## Native Test

```txt
cargo: command not found
rustc: command not found
```

Run in a Rust-enabled environment:

```bash
cargo test -p lora_train qwave_sft_train_dry_run
```
