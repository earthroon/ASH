# SFT-GPU-8E Acceptance

## Status

PENDING until run in the target Rust/WGPU environment.

## Scope

native_dump atlas grouped hidden batching / progress seal

## Required Contract

- native_dump uses `atlas_token_grouped` batching.
- teacher/checkpoint is loaded once.
- examples are grouped by token budget.
- group forward produces feature batches.
- hidden/labels token counts match through existing FeatureStore shards.
- prompt_loss_tokens remains 0.
- response_loss_tokens is greater than 0.
- group progress logs timing.
- native_dump_progress_report.json is written.
- native_dump_progress_report.md is written.

## Gates

- [ ] `dump_batching` config exists.
- [ ] `strategy = atlas_token_grouped`.
- [ ] `teacher_load_count == 1`.
- [ ] `group_count > 0`.
- [ ] `feature_batch_count > 0`.
- [ ] `prompt_loss_tokens == 0`.
- [ ] `response_loss_tokens > 0`.
- [ ] group timing logs exist.
- [ ] progress JSON report exists.
- [ ] progress MD report exists.
- [ ] no per-sample checkpoint reload.

## Non-goals

- This commit does not implement direct_train Atlas provider.
- This commit does not run experiment matrix.
- This commit does not evaluate generation quality.
