# SFT-GPU-RUN-11 Acceptance Report

## Seal

`SFT-GPU-RUN-11 — GPU-Trained Slot Arbitration / Multi-Adapter Health Merge Seal`

## Source Seals

- `source_post_switch_health_seal_id`: required, must match RUN-09 report seal.
- `source_rollback_drill_seal_id`: required, must match RUN-10 report seal.
- `source_current_pointer_switch_seal_id`: required, must match RUN-09/RUN-10 current pointer switch source.
- `adapter_registry_snapshot_digest`: required.

## Current GPU-Trained Adapter

- `current_gpu_trained_adapter_id`: required, must match RUN-09/RUN-10 current adapter.
- `current_pointer_actual`: required, must match RUN-09/RUN-10 current pointer.
- `current_gpu_trained_health_score_milli`: emitted from RUN-11 health snapshot.

## Readiness Merge

- `fallback_ready`: true only when RUN-09 health readiness and RUN-10 fallback dry-run readiness are both present.
- `rollback_ready`: true only when RUN-09 rollback availability and RUN-10 rollback drill/restore pointer checks pass.

## Recommendations

RUN-11 emits recommendation identifiers only:

- `active_recommendation_id`
- `fallback_recommendation_id`
- `demotion_recommendation_id`
- `quarantine_recommendation_id`
- `recommendation_digest`

## Closed Actions Confirmed

These remain closed in RUN-11:

- `actual_action_apply_performed: false`
- `current_pointer_switch_performed: false`
- `rollback_execution_performed: false`
- `actual_demotion_apply_performed: false`
- `actual_quarantine_apply_performed: false`
- `lifecycle_mutation_performed: false`
- `ash_binding_performed: false`
- `runtime_sft_training_performed: false`
- `runtime_gradient_write_performed: false`
- `runtime_optimizer_step_performed: false`
- `textureSample/sampler/normalized UV weight fetch: false`
- `silent CPU fallback as success: false` at backend boundary.

## Implemented Files

- `crates/ash_core/src/sft_gpu_slot_arbitration.rs`
- `crates/ash_core/tests/sft_gpu_run_11_slot_arbitration.rs`
- `crates/lora_train/src/gpu_trained_slot_arbitration.rs`
- `crates/lora_train/tests/gpu_trained_slot_arbitration.rs`
- `crates/burn_webgpu_backend/src/gpu_trained_slot_arbitration.rs`
- `crates/burn_webgpu_backend/tests/gpu_trained_slot_arbitration.rs`

## Verification Commands

Expected local commands:

```bash
cargo test -p ash_core sft_gpu_run_11 -- --nocapture
cargo test -p lora_train gpu_trained_slot_arbitration -- --nocapture
cargo test -p burn_webgpu_backend gpu_trained_slot_arbitration -- --nocapture
```

Regression commands:

```bash
cargo test -p ash_core sft_gpu_run_10 -- --nocapture
cargo test -p ash_core sft_gpu_run_09 -- --nocapture
cargo test -p ash_core sft_gpu_run_08 -- --nocapture
```

## Container Verification

This bake environment did not provide `cargo` or `rustc`, so Rust compilation could not be executed here.
Static verification performed:

- Balanced delimiter scan for all newly added Rust source/test files.
- Export wiring check for `ash_core`, `lora_train`, and `burn_webgpu_backend` module exports.
- File inclusion check during ZIP bake.

## SSOT Statement

RUN-11 is a recommendation-only arbitration seal. It merges health/fallback/rollback readiness across adapter slots and emits recommendation IDs, but it does not apply any recommendation or mutate runtime/lifecycle/current pointer state.
