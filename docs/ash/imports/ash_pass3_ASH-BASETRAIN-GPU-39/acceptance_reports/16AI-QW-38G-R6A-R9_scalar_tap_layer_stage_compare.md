# 16AI-QW-38G-R6A-R9 — Scalar Tap Layer/Stage Compare / Reserved Direction Source Probe Seal

## Status
PENDING_RUNTIME

## SSOT
- Base: `ash_pass3_16AI-QW-38G-R6A-R8_debug_buffer_scalar_readback_baked.zip`
- Patch: `16AI-QW-38G-R6A-R9`
- Mode: sandbox scalar compare probe
- Target: `token_id=13 / <glossary:on>`
- Default layers: `mid,last`
- Default stages: `post_mlp,post_block,post_final_norm`
- Scalar only: true
- Full vector readback: forbidden
- Production apply: forbidden

## Runtime Outputs
- `workspace/qw38g_r6a_r9_scalar_tap_compare_trace.jsonl`
- `workspace/qw38g_r6a_r9_scalar_tap_compare_summary.json`
- `workspace/qw38g_r6a_r9_scalar_tap_compare_receipt.json`
- `workspace/qw38g_r6a_r9_scalar_tap_compare_rollback_receipt.json`
- `workspace/infer_qw38g_r6a_r9_scalar_tap_compare_live.log`

## Important Boundary Note
The current implementation preserves the R8 SSOT: the reliable scalar record is available at `last/post_final_norm` / projection boundary. Intermediate `mid/post_mlp`, `mid/post_block`, `last/post_mlp`, and `last/post_block` records are emitted as unavailable when that boundary is not exposed in the current sandbox. This avoids silently pretending that intermediate activation was actually captured.

## Acceptance Criteria
- R8 scalar readback source loaded and validated
- Compare plan written
- Scalar-only enforced
- Full-vector readback rejected
- Production apply rejected
- Trace JSONL written
- Summary JSON written
- Receipt JSON written
- Rollback receipt written
- Normal path guard passed
- Source candidate written as probe candidate, not final cause

## Decision Matrix
- `PASS_SCALAR_TAP_LAYER_STAGE_COMPARE`: at least one scalar event available, typically `last/post_final_norm`.
- `FAIL_SCALAR_TAP_COMPARE_NO_EVENTS`: no available scalar events.
- `FAIL_R8_SOURCE_INVALID_FOR_R9`: R8 source missing/invalid.

## Next
If pass with `final_norm_or_projection_boundary`, continue to:
`16AI-QW-38G-R6A-R10_FINAL_NORM_PROJECTION_BOUNDARY_CONFIRM`
