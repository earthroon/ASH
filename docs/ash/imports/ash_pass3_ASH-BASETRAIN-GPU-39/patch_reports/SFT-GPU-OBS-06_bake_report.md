# SFT-GPU-OBS-06 Bake Report

## Added

```txt
crates/ash_core/src/sft_gpu_action_candidate_preflight.rs
crates/ash_core/tests/sft_gpu_obs_06_action_candidate_preflight.rs
crates/lora_train/src/gpu_action_candidate_preflight.rs
crates/lora_train/tests/gpu_action_candidate_preflight.rs
crates/burn_webgpu_backend/src/gpu_action_candidate_preflight_signals.rs
crates/burn_webgpu_backend/tests/gpu_action_candidate_preflight_signals.rs
acceptance_reports/SFT-GPU-OBS-06_action_candidate_preflight.md
docs/roadmap/SFT-GPU-OBS-06_after_bake.md
patch_reports/SFT-GPU-OBS-06_bake_report.md
```

## Modified

```txt
crates/ash_core/src/lib.rs
crates/lora_train/src/lib.rs
crates/burn_webgpu_backend/src/lib.rs
```

## Core Contract

OBS-06 is a no-apply candidate preflight. It can mark `apply_gate_intake_allowed = true`, but it always keeps `apply_performed = false` and all mutation flags closed.

## Static Result

Static delimiter checks passed for the new Rust files. Rust compilation was not executed because the current container does not include cargo/rustc/rustfmt.
