# 16AI-QW-25 Bake Report

## Patch

`16AI-QW-25 — QWave Korean Minimal Pair SFT Eval / Cheon-Ji-In Contrast Seal`

## Baked on

Base: `ash_pass3_16AI-QW-24_qwave_conditioned_sft_smoke_baked.zip`

## Files added / modified

- Added `crates/lora_train/src/qwave_korean_minimal_pair_eval.rs`
- Added `crates/lora_train/tests/qwave_korean_minimal_pair_eval.rs`
- Modified `crates/lora_train/src/lib.rs`
- Added acceptance and static validation reports

## Test inventory

`crates/lora_train/tests/qwave_korean_minimal_pair_eval.rs` contains 45 test functions.

## Native tests

`cargo` / `rustc` unavailable in this container, so native Rust tests were not executed.

Recommended native command:

```bash
cargo test -p lora_train qwave_korean_minimal_pair_eval
```

## Seal

- Evaluation-only: sealed
- Training rerun: rejected
- Runtime apply: rejected
- Token/vocab/embedding mutation: rejected
- Sampler/logit/backend mutation: rejected
- Deterministic receipt: sealed
