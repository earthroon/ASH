# QW-50-R0P — lora_train hash tuple serialize / numeric / canary Eq fix

## Scope

- Target crate: `lora_train`
- Target files:
  - `crates/lora_train/src/qwave_auxiliary_loss_candidate.rs`
  - `crates/lora_train/src/hangul_structure_reconstruction_head.rs`
  - `crates/lora_train/src/word_salad_negative_corpus.rs`
  - `crates/lora_train/src/canary_adapter_apply.rs`

## Fix

- Replaced oversized tuple fingerprint inputs with `short_sha256_parts(...)` string-part hashing.
- Preserved nested complex values by hashing complex serializable fields first and then including their hash in the fingerprint parts.
- Added explicit `f32` type annotations for `score_min` and `score_max` in word salad corpus stats.
- Added `Eq` derive to `CanaryApplyCandidate` so `CanaryAdapterApplyPlan` can derive `Eq` without trait-bound failure.

## Guard

- No LoRA training execution.
- No backward execution.
- No optimizer step.
- No runtime pointer mutation.
- No production apply.
- No hash fallback added.

## Verification

```txt
cargo check --workspace --all-targets
```

## Status

PENDING_LOCAL_CARGO_CHECK
