# SFT-GPU-OBS-05 Bake Report

## Patch

`SFT-GPU-OBS-05 — Operator Decision to Action Candidate Bridge / No-Apply Handoff Seal`

## Added

```txt
crates/ash_core/src/sft_gpu_decision_action_candidate.rs
crates/ash_core/tests/sft_gpu_obs_05_decision_action_candidate.rs
crates/lora_train/src/gpu_decision_action_candidate.rs
crates/lora_train/tests/gpu_decision_action_candidate.rs
crates/burn_webgpu_backend/src/gpu_decision_action_candidate_signals.rs
crates/burn_webgpu_backend/tests/gpu_decision_action_candidate_signals.rs
acceptance_reports/SFT-GPU-OBS-05_decision_action_candidate.md
acceptance_reports/SFT-GPU-OBS-05_static_verification.log
docs/roadmap/SFT-GPU-OBS-05_after_bake.md
patch_reports/SFT-GPU-OBS-05_bake_report.md
```

## Modified

```txt
crates/ash_core/src/lib.rs
crates/lora_train/src/lib.rs
crates/burn_webgpu_backend/src/lib.rs
```

## Summary

- Added deterministic decision-kind to candidate-kind mapping.
- Added no-apply handoff packet and handoff seal.
- Added explicit apply gate eligibility marker without applying.
- Added silent candidate kind rewrite guard.
- Added no-apply backend boundary.
- Added tests for mapping, missing source, previous handoff digest, no-apply boundary, silent rewrite, and mutation closure.

## Non-Executed Runtime Checks

`cargo`, `rustc`, and `rustfmt` were unavailable in this container, so runtime Rust tests were not executed here.
