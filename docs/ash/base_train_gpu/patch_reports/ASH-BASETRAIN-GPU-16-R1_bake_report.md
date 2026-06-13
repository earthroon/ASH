# ASH-BASETRAIN-GPU-16-R1 Bake Report

## Patch

ASH-BASETRAIN-GPU-16-R1  
Dispatch X Type Bridge Fix / Source Receipt u64 To Runtime Dispatch u32 Boundary Seal

## Source

ASH-BASETRAIN-GPU-16 baked ZIP.

## Purpose

Fix compile errors caused by comparing and assigning `target_dispatch_x` from the ASH-BASETRAIN-GPU-15 receipt as `u64` against the ASH-BASETRAIN-GPU-16 runtime dispatch constant as `u32`.

## Changes

- Added `LOGITS_DISPATCH_X_RECEIPT_U64` for receipt-side comparison.
- Changed `source_target_dispatch_x` in `AshBaseTrainGpu16Source15ExpansionReadinessValidation` from `u32` to `u64`.
- Kept `LOGITS_DISPATCH_X` as `u32` for WGPU `dispatch_workgroups` and dispatch receipt runtime fields.

## Boundaries

- No readback added.
- No dispatch semantics changed.
- No optimizer/backward/loss path opened.
- No safetensors mutation introduced.

## Local validation

Container cannot run Cargo here (`cargo: command not found`). Operator local `cargo build/run` remains the SSOT.
