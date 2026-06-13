# SFT-GPU-OBS-03 Bake Report

## Summary

Implemented Operator Health Review Console / Long-Horizon Attention Queue Seal on top of OBS-02.

The patch converts long-horizon health/drift evidence into review queue items and console projection summaries. It explicitly keeps action controls disabled and blocks all mutation paths.

## Core Contract

- OBS-03 may create review queue items.
- OBS-03 may create console projection and queue digest.
- OBS-03 may mark Blocker/Urgent/Review/Watch counts.
- OBS-03 may expose operator attention requirements.
- OBS-03 may not apply actions or mutate state.

## SSOT Locations

- ash_core: crates/ash_core/src/sft_gpu_operator_health_review.rs
- lora_train: crates/lora_train/src/gpu_health_review_queue.rs
- burn_webgpu_backend: crates/burn_webgpu_backend/src/gpu_health_review_signals.rs

## Key Guards

- action_controls_enabled = false
- current_pointer_update_enabled = false
- rollback_execution_enabled = false
- demotion_apply_enabled = false
- quarantine_apply_enabled = false
- runtime training / gradient / optimizer = false
- textureSample weight fetch = false

## Blocker Promotion

The following conditions become Blocker items:
- adapter digest drift
- digest mismatch
- CPU fallback accepted
- source seal missing
- silent backend switch / silent registry correction
- textureSample weight fetch via texture load guard drift item

## Test Notes

Rust toolchain unavailable in this container. Static delimiter/export/file-presence verification was performed. Run cargo test locally with the commands in the acceptance report.
