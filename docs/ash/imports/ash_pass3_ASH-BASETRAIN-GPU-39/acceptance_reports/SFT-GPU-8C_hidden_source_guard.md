# SFT-GPU-8C Acceptance

## Status

PENDING_STATIC_BAKED

## Scope

A-SFT hidden source guard / forbid full checkpoint teacher in train.

## Required Contract

- A-SFT train phase forbids full checkpoint-backed teacher.
- Full checkpoint teacher is allowed only in `phase=native_dump`.
- Train phase must use `dataset.feature_store_manifest` or an explicitly wired Atlas grouped hidden provider.
- Missing train hidden source must fail before `model_core::load_full_checkpoint_weights` or `ReferenceModel::from_full_checkpoints`.
- No silent fallback to full checkpoint teacher.

## Gates

- [x] `sft_hidden_source.rs` defines `ASftPhase`.
- [x] `sft_hidden_source.rs` defines `ASftHiddenSourceDecision`.
- [x] `decide_a_sft_hidden_source()` exists.
- [x] `guard_a_sft_full_checkpoint_teacher()` exists.
- [x] `run_direct_jsonl_training_loop()` calls the hidden-source guard before full checkpoint weight load.
- [x] `run_direct_jsonl_training_loop()` calls the hidden-source guard before `ReferenceModel::from_full_checkpoints`.
- [x] `direct_train` smoke config declares `forbid_teacher_full_model_in_train=true`.
- [x] `native_dump` config declares `phase=native_dump` and allows full teacher only there.
- [x] `train_from_features` config declares `require_feature_store_manifest=true`.

## Expected Safe Failure

For `ash_ko_short_sft_lm_head_lora_v1_smoke.json`, until Atlas grouped hidden is wired into the direct loop or a feature store manifest is provided, the expected behavior is a clear failure before full checkpoint teacher loading:

```txt
[A-SFT][hidden_source_guard] A-SFT train phase forbids full checkpoint-backed teacher
```

## Non-goals

- This patch does not implement the Atlas grouped hidden provider inside the direct JSONL train loop.
- This patch does not run SFT-GPU-9 experiment matrix.
- This patch does not judge generation quality.
