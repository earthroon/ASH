# 16AI-QW-38G-R6A-R11-R1 — Projection Margin Hook Reachability / Receipt Fallback Seal

## Status
PENDING_RUNTIME / STATIC_PASS

## SSOT
- Base: `ash_pass3_16AI-QW-38G-R6A-R11_projection_margin_audit_baked.zip`
- Patch: `16AI-QW-38G-R6A-R11-R1`
- Purpose: ensure R11 margin audit reachability and fallback receipt generation
- Production apply: forbidden
- Full vector readback: forbidden

## Implemented
- Added R11-R1 reachability writer in `crates/model_core/src/native_wgpu.rs`.
- Added fallback receipt writer for hook-not-reached, source-load failure, and guarded rollback.
- Added runtime entry probe before projection branch can silently disappear.
- Added projection boundary hook attempt heartbeat.
- Added source-load and margin-plan reachability stages.
- Added final reachability update on successful R11 audit completion.
- Added runner: `scripts/run_16AI_QW_38G_R6A_R11_R1_projection_margin_reachability.ps1`.

## Required Runtime Artifacts
- `workspace/qw38g_r6a_r11_projection_margin_receipt.json`
- `workspace/qw38g_r6a_r11_projection_margin_summary.json`
- `workspace/qw38g_r6a_r11_projection_margin_trace.jsonl`
- `workspace/qw38g_r6a_r11_projection_margin_rollback_receipt.json`
- `workspace/qw38g_r6a_r11_r1_projection_margin_reachability.json`

## Expected Decisions
| Case | Status | Next |
|---|---|---|
| R11 audit reaches and writes event | `PASS_PROJECTION_MARGIN_AUDIT` | Multi-seed aggregation |
| Hook not reached | `FAIL_PROJECTION_MARGIN_HOOK_NOT_REACHED` | R11-R2 hot path hook relocation |
| Source load failed | `FAIL_PROJECTION_MARGIN_SOURCE_LOAD` | source path/schema repair |
| Event not written | `FAIL_PROJECTION_MARGIN_EVENT_NOT_WRITTEN` | event writer repair |

## Guard
- `ASH_BACKEND_EXTENSION_PRODUCTION_APPLY=1` must be rejected.
- `ASH_DEBUG_BUFFER_FULL_VECTOR=1` must be rejected.
- Missing receipt is no longer acceptable; fallback receipt must be written.
