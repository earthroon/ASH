# 16AI-QW-38G-R6A-R11 — Projection Boundary Margin Audit / Masked Top1 Compare Seal

## Status
PENDING_RUNTIME

## SSOT
- Base: `ash_pass3_16AI-QW-38G-R6A-R10_final_boundary_confirm_baked.zip`
- Target boundary: `last / post_final_norm / projection boundary`
- Target token: `13 / <glossary:on>`
- Source inputs:
  - `workspace/qw38g_r6a_r8_debug_buffer_scalar_summary.json`
  - `workspace/qw38g_r6a_r8_debug_buffer_scalar_receipt.json`
  - `workspace/qw38g_r6a_r10_final_boundary_confirm_summary.json`
  - `workspace/qw38g_r6a_r10_final_boundary_confirm_receipt.json`
  - optional `workspace/qw38a_raw_topk_trace.jsonl`

## Implemented Guard
- Production apply is rejected in R11.
- Full vector readback is rejected in R11.
- Target count is capped to 2.
- `top_n` is capped to 64.
- Byte budget above 16384 is rejected.
- R8/R10 source validity is checked before margin audit.

## Runtime Outputs
- `workspace/qw38g_r6a_r11_projection_margin_trace.jsonl`
- `workspace/qw38g_r6a_r11_projection_margin_summary.json`
- `workspace/qw38g_r6a_r11_projection_margin_receipt.json`
- `workspace/qw38g_r6a_r11_projection_margin_rollback_receipt.json`
- `workspace/infer_qw38g_r6a_r11_projection_margin_live.log`

## Acceptance Criteria
| check | expected |
|---|---:|
| source_valid_for_r11 | true |
| projection_margin_confirmed | true/false explicit |
| projection_margin_strength | none/weak/medium/strong explicit |
| raw_top1_target_rate | written |
| ban_mask_displacement_rate | written |
| mean/min margin vs masked top1 | written |
| scalar_only | true |
| full_vector_readback_used | false |
| normal_path_guard_passed | true |
| rollback_receipt_written | true |

## Decision Rule
- Single-seed evidence cannot lift confidence to strong.
- If margin exceeds threshold but R10 confidence was weak/single-process, R11 caps strength to medium.
- Success recommends `16AI-QW-38G-R6A-R10-R1_MULTI_SEED_FINAL_BOUNDARY_AGGREGATION`.
