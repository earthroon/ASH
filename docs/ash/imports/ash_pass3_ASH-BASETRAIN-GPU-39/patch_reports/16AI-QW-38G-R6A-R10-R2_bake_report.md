# 16AI-QW-38G-R6A-R10-R2 Bake Report

## Patch
- `16AI-QW-38G-R6A-R10-R2 — Multi-Seed Evidence Field Extraction Repair / Trace-backed Aggregation Seal`

## Base
- `ash_pass3_16AI-QW-38G-R6A-R10-R1_multiseed_aggregation_baked.zip`

## Static Validation
- `PASS_STATIC`

## Cargo
- `NOT_RUN_CONTAINER_CARGO_UNAVAILABLE`

## Implemented
- Added `ASH_MULTI_SEED_EVIDENCE_REPAIR` env gate.
- Added trace-backed aggregation function in `native_wgpu.rs`.
- Reads R11 seed trace JSONL as primary source.
- Extracts required seed fields:
  - `raw_top1_token_id`
  - `masked_top1_token_id`
  - `target_is_raw_top1`
  - `ban_mask_displaced_target`
  - `target_minus_masked_top1_margin`
- Classifies seed evidence as:
  - `VALID`
  - `PARTIAL_FIELD_LOSS`
  - `INVALID_SOURCE_MISSING`
  - `INVALID_GUARD_FAILED`
- Blocks confidence lift when required fields are missing.
- Writes repaired trace, summary, and receipt outputs.
- Added PowerShell runner:
  - `scripts/run_16AI_QW_38G_R6A_R10_R2_trace_backed_aggregation.ps1`

## Runtime Outputs
- `workspace/qw38g_r6a_r10_r2_trace_backed_aggregation_trace.jsonl`
- `workspace/qw38g_r6a_r10_r2_trace_backed_aggregation_summary.json`
- `workspace/qw38g_r6a_r10_r2_trace_backed_aggregation_receipt.json`

## Notes
This patch does not run new inference. It repairs the seed evidence ledger by reading already generated seed trace files. Summary-only confidence lift is intentionally blocked.
