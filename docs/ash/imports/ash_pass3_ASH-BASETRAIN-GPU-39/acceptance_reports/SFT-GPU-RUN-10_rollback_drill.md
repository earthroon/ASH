# SFT-GPU-RUN-10 Acceptance

## Patch

SFT-GPU-RUN-10 — GPU-Trained Rollback Drill / Failure Recovery Simulation Seal

## SSOT

- Source SSOT: `SFT-GPU-RUN-09_post_switch_health`
- Source current pointer switch: `SFT-GPU-RUN-08_current_pointer_switch`
- New seal: `gpu_trained_rollback_drill_seal_id`

## Opened in RUN-10

- failure injection fixture
- rollback drill simulation
- rollback handle verification
- rollback restore pointer dry-run
- fallback activation simulation
- demotion candidate generation
- quarantine candidate generation
- rollback drill seal

## Still closed in RUN-10

- production rollback execution
- actual current pointer rollback/update
- actual demotion apply
- actual quarantine apply
- lifecycle mutation
- slot action apply
- ASH current binding
- runtime SFT training
- runtime gradient write
- runtime optimizer step
- textureSample / sampler / normalized UV weight fetch

## Implemented files

- `crates/ash_core/src/sft_gpu_rollback_drill.rs`
- `crates/ash_core/tests/sft_gpu_run_10_rollback_drill.rs`
- `crates/lora_train/src/gpu_trained_rollback_drill.rs`
- `crates/lora_train/tests/gpu_trained_rollback_drill.rs`
- `crates/burn_webgpu_backend/src/gpu_trained_rollback_drill.rs`
- `crates/burn_webgpu_backend/tests/gpu_trained_rollback_drill.rs`

## Acceptance checks

```bash
cargo test -p ash_core sft_gpu_run_10 -- --nocapture
cargo test -p lora_train gpu_trained_rollback_drill -- --nocapture
cargo test -p burn_webgpu_backend gpu_trained_rollback_drill -- --nocapture
```

## Result

Static bake checks passed in this environment. Rust compile/test commands were not executed here because `cargo`/`rustc` are unavailable in the container.
