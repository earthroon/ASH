# 16AI-QW-37 — QWave Trajectory Smoothness Loss / Curvature Spike Penalty Seal

## Status
STATIC_BAKE_ONLY — source and artifact seal added. Native Rust execution was not run in this container because `cargo`/`rustc` are unavailable.

## Scope
- Added `crates/lora_train/src/qwave_trajectory_smoothness_loss.rs`.
- Exported QW-37 module and public API from `crates/lora_train/src/lib.rs`.
- Added trajectory loss report and receipt artifacts under `artifacts/qwave_trajectory_loss/`.

## SSOT
QW-37 introduces `QWaveTrajectorySmoothnessReceipt` as the static SSOT for the trajectory smoothness loss candidate. It references QW-35 auxiliary loss receipt, QW-36 geometry loss receipt, QWave feature receipt, and SFT batch plan identifiers by fingerprint.

## Guard Contract
- `affects_loss_candidate = true`
- `affects_total_loss = false`
- `affects_gradient = false`
- `affects_optimizer = false`
- `affects_lora_weights = false`
- `affects_base_model = false`

## Candidate Losses
- curvature spike loss
- phase discontinuity loss with wrap-around handling
- pressure spike loss
- closure break loss
- binding energy drop loss
- direction jitter loss
- mask validity loss

## Mutation Guard
The candidate path forbids backward execution, optimizer step, LoRA/base mutation, token/vocab/embedding mutation, sampler/backend mutation, and runtime pointer mutation.

## Execution Evidence
- Static source bake: COMPLETE
- Cargo check: NOT RUN — toolchain unavailable
- Unit tests: NOT RUN — toolchain unavailable
- Runtime training: NOT RUN

## Acceptance Result
PASS_STATIC_SOURCE_BAKE_WITH_TOOLCHAIN_UNAVAILABLE
