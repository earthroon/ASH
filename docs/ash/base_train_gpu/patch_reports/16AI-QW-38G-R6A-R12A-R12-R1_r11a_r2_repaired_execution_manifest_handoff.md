# 16AI-QW-38G-R6A-R12A-R12-R1 — R11A-R2 Repaired Execution Manifest Handoff

## Status
Baked patch.

## Source Failure
- R12 previously read legacy prompt/negative case files directly.
- R11A-R2 repaired execution manifest can contain the correct 3/3 ready cases.

## Implemented
- Patched `scripts/run_16AI_QW_38G_R6A_R12A_R12_case_set_execution_validation.ps1`.
- Added case source priority loader:
  1. `qw38g_r6a_r12a_r11a_r2_r12_execution_manifest_candidate.json`
  2. `qw38g_r6a_r12a_r11a_validation_case_manifest.json`
  3. legacy prompt/negative case files
- Added support for `execution_cases`, `case_groups`, raw array, and wrapper `.cases` shapes.
- Added R12-R1 handoff audit runner.

## Guard
- runtime_default_apply remains false.
- production_safe_confirmed remains false.
- root_cause_confirmed remains false.
- no model artifacts are modified.
