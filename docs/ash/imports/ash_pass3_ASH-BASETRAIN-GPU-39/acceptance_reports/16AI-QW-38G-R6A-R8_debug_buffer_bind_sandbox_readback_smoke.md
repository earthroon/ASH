# 16AI-QW-38G-R6A-R8 — Debug Buffer Bind Sandbox Readback Smoke / Scalar Tap Seal

## Status
PENDING_RUNTIME

## SSOT
- base: 16AI-QW-38G-R6A-R7 sandbox smoke baked state
- source: `workspace/qw38g_r6a_r7_sandbox_smoke.json`
- source receipt: `workspace/qw38g_r6a_r7_sandbox_smoke_receipt.json`
- mode: sandbox scalar tap smoke
- production apply: forbidden
- full vector readback: forbidden
- target default: `13`
- layer default: `last`
- stage default: `post_final_norm`

## Added Runtime Outputs
- `workspace/qw38g_r6a_r8_debug_buffer_scalar_trace.jsonl`
- `workspace/qw38g_r6a_r8_debug_buffer_scalar_summary.json`
- `workspace/qw38g_r6a_r8_debug_buffer_scalar_receipt.json`
- `workspace/qw38g_r6a_r8_debug_buffer_rollback_receipt.json`
- `workspace/infer_qw38g_r6a_r8_debug_buffer_scalar_live.log`

## Guard Policy
| guard | expected |
|---|---:|
| production apply rejected | true |
| full vector rejected | true |
| max steps <= 1 | true |
| target count <= 2 | true |
| max bytes <= 16384 | true |
| scalar only | true |
| normal path guard | true |
| rollback receipt | true |

## Runtime Decision
R8 reads scalar records only. The smoke currently seals scalar values available at the vocab projection boundary into the sandbox readback trace without enabling production apply or full-vector export.

## Next Patch
`16AI-QW-38G-R6A-R9 — Scalar Tap Layer/Stage Compare / Reserved Direction Source Probe Seal`
