# 16AI-QW-38G-R6A-R12A-R11A-R1 — Readiness Min Count Guard Repair

## Status
STATIC_PASS_READINESS_MIN_COUNT_GUARD_REPAIR

## Source
- source_patch: 16AI-QW-38G-R6A-R12A-R11A
- downstream trigger: R12 blocked with `Ready prompt variant case count is 1`

## What Changed
- Added `run_16AI_QW_38G_R6A_R12A_R11A_R1_readiness_min_count_guard_repair.ps1`.
- Recomputes ready case counts using strict case validity.
- Blocks R12 when ready prompt variants or negative controls are below the configured minimum.
- Writes R11A-R1 audit/receipt/readiness artifacts.
- Updates canonical `qw38g_r6a_r12a_r11a_validation_readiness.json` unless `-NoCanonicalUpdate` is provided.
- Tightened the R11A authoring script so future `ready=true` requires ready prompt variants >= 3 and ready negative controls >= 3.

## Guard
- Does not generate missing cases.
- Does not run inference.
- Does not modify checkpoint/tokenizer/safetensors/lm_head/final_norm/ban mask.
- Does not set production safe or root cause confirmed.
