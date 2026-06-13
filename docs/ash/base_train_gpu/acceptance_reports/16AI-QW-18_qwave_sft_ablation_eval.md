# 16AI-QW-18 — QWave SFT Ablation Eval / Baseline vs Feature Side-channel Seal

## Status

ACCEPTANCE: STATIC_PASS / NATIVE_RUST_TEST_NOT_RUN_TOOLCHAIN_UNAVAILABLE

## Base ZIP

`ash_pass3_16AI-QW-17_qwave_sft_train_dry_run_baked.zip`

## Input SSOT

- `crates/lora_train/src/qwave_sft_train_dry_run.rs`
- `crates/lora_train/src/qwave_sft_feature_intake.rs`
- `crates/lora_train/src/qwave_feature_intake_parity_smoke.rs`
- `crates/lora_train/src/qwave_feature_coverage_telemetry.rs`
- `crates/lora_train/src/qwave_sample_weight_candidate.rs`
- `crates/lora_train/src/qwave_curriculum_metadata.rs`

## New SSOT

- `crates/lora_train/src/qwave_sft_ablation_eval.rs`
- `QWaveSftAblationEvalReceipt`

## Acceptance Checklist

1. Patch name recorded: PASS
2. Base ZIP recorded: PASS
3. Input SSOT recorded: PASS
4. New SSOT recorded: PASS
5. QW-17 dry-run receipt consumed: PASS
6. QW-12 intake receipt referenced: PASS
7. QW-13 telemetry receipt referenced: PASS
8. QW-14 sample weight candidate receipt referenced: PASS
9. QW-15 curriculum metadata receipt referenced: PASS
10. QW-16 parity receipt referenced: PASS
11. Baseline group guard implemented: PASS
12. Ablation group guard implemented: PASS
13. Eval-only group guard implemented: PASS
14. Mutation unapplied guard implemented: PASS
15. Loss delta calculation implemented: PASS
16. Gradient finite delta calculation implemented: PASS
17. Korean eval delta calculation implemented: PASS
18. Outcome calculation implemented: PASS
19. Recommendation calculation implemented: PASS
20. Auto promotion blocked: PASS
21. Sample weight/curriculum apply blocked: PASS
22. Runtime apply blocked: PASS
23. Deterministic receipt fingerprint implemented: PASS
24. Native cargo test: NOT_RUN_TOOLCHAIN_UNAVAILABLE

## Guard Summary

QW-18 is eval-only. It accepts ablation group snapshots, compares them against a BaselineNoQWave group, emits comparison reports, and refuses auto-promotion, sample-weight apply, curriculum apply, runtime apply, loss rewrite, optimizer mutation, scheduler mutation, adapter mutation, and backend switch attempts.

## 판단불가

Native Rust compile/test was not executed in this container because `cargo` / `rustc` are unavailable. Run:

```bash
cargo test -p lora_train qwave_sft_ablation_eval
```
