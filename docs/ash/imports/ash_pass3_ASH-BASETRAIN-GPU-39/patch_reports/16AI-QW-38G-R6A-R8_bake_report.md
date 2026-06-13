# 16AI-QW-38G-R6A-R8 Bake Report

## Patch
16AI-QW-38G-R6A-R8 — Debug Buffer Bind Sandbox Readback Smoke / Scalar Tap Seal

## Base
ash_pass3_16AI-QW-38G-R6A-R7_sandbox_smoke_baked.zip

## Files Changed
- `crates/model_core/src/native_wgpu.rs`
- `scripts/run_16AI_QW_38G_R6A_R8_debug_buffer_scalar_readback.ps1`
- `acceptance_reports/16AI-QW-38G-R6A-R8_debug_buffer_bind_sandbox_readback_smoke.md`

## Implementation Notes
- Added env-gated R8 sandbox scalar readback smoke.
- Consumes R7 sandbox smoke source/receipt before writing R8 artifacts.
- Rejects production apply, full-vector readback, oversized byte budgets, too many steps, and too many target ids.
- Writes trace JSONL, summary JSON, receipt JSON, and rollback receipt.
- Leaves normal path unchanged and records normal path guard status.

## Static Validation
PASS_STATIC

## Cargo
Not run in container: cargo unavailable.
