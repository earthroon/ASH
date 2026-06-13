# 16AI-QW-36 — Hangul Structure Reconstruction Head / Geometry Loss Smoke Seal

## Status

STATIC SOURCE BAKE ONLY. Native Rust compilation and tests were not executed because `cargo` / `rustc` are unavailable in the container.

## Scope

QW-36 adds a static Hangul structure reconstruction smoke module in `crates/lora_train/src/hangul_structure_reconstruction_head.rs` and exports it from `crates/lora_train/src/lib.rs`.

## Implemented Surface

- `HangulStructureTarget`
- `build_hangul_structure_target_from_char()`
- `HangulStructureReconstructionHeadConfig`
- `HangulStructureReconstructionLogits`
- `HangulGeometryLossBundle`
- `HangulGeometryTargetStats`
- `HangulGeometryLossSmokeInput`
- `HangulGeometryLossSmokePolicy`
- `HangulGeometryLossSmokeReport`
- `HangulGeometryLossSmokeManifest`
- `HangulGeometryLossSmokePlan`
- `HangulGeometryLossSmokeReceipt`
- `build_hangul_geometry_loss_smoke_plan()`
- `build_hangul_geometry_loss_smoke_receipt()`
- `build_hangul_geometry_loss_smoke_plan_and_receipt()`

## Policy Seal

- `affects_loss_candidate = true`
- `affects_total_loss = false`
- `affects_gradient = false`
- `affects_optimizer = false`
- `affects_lora_weights = false`
- `affects_base_model = false`
- backward execution forbidden
- optimizer step forbidden
- LoRA/base/tokenizer/vocab/embedding/runtime mutation forbidden

## Artifact Evidence

- `artifacts/qwave_geometry_loss/qw36_geometry_loss_report.json`
- `artifacts/qwave_geometry_loss/qw36_geometry_loss_receipt.json`

## Acceptance Notes

QW-36 creates the geometry reconstruction candidate loss measurement path only. It does not connect the candidate loss into total loss, does not execute backward, does not step an optimizer, and does not mutate LoRA or base model weights.

## Next Patch

QW-37 — QWave Trajectory Smoothness Loss / Curvature Spike Penalty Seal
