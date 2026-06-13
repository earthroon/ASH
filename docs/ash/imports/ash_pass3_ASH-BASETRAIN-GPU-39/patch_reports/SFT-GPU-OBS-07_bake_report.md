# SFT-GPU-OBS-07 Bake Report

## Patch
SFT-GPU-OBS-07 — Reviewed Candidate Apply Plan / Dry-run Transaction Seal

## Summary
Added a dry-run transaction planning layer on top of OBS-06 action candidate preflight. The new layer creates a reviewed candidate apply plan and planned operation summary while preserving the no-apply boundary.

## Added
- `crates/ash_core/src/sft_gpu_candidate_apply_plan.rs`
- `crates/ash_core/tests/sft_gpu_obs_07_candidate_apply_plan.rs`
- `crates/lora_train/src/gpu_candidate_apply_plan.rs`
- `crates/lora_train/tests/gpu_candidate_apply_plan.rs`
- `crates/burn_webgpu_backend/src/gpu_candidate_apply_plan_signals.rs`
- `crates/burn_webgpu_backend/tests/gpu_candidate_apply_plan_signals.rs`
- `acceptance_reports/SFT-GPU-OBS-07_candidate_apply_plan.md`
- `acceptance_reports/SFT-GPU-OBS-07_static_verification.log`
- `docs/roadmap/SFT-GPU-OBS-07_after_bake.md`

## Modified
- `crates/ash_core/src/lib.rs`
- `crates/lora_train/src/lib.rs`
- `crates/burn_webgpu_backend/src/lib.rs`

## Contract
- Plan generation is allowed.
- `would_*` operation flags are allowed.
- Actual apply/mutation is forbidden.
- Dry-run ledger append is allowed.
- Runtime training/gradient/optimizer are forbidden.
- textureSample / sampler / normalized UV weight fetch remains closed.
