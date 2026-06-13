# 16AI-QW-38G-R6A-R12A-R12B - Scope Tightening and Guard Repair

## Status
Baked patch package. Runtime execution must be performed on the Windows ASH workspace.

## Purpose
This patch reads R12 execution matrices, separates output stability failures from margin overeffect failures, and writes a guarded scope tightening policy candidate for HEAD2_TARGET_DIRECTION_ORTHOGONAL_ONLY.

## Guard
- runtime_default_apply: false
- production_safe_confirmed: false
- root_cause_confirmed: false
- checkpoint/tokenizer/safetensors/lm_head/final_norm/ban_mask modified: false

## Execute
```powershell
.\scripts\run_16AI_QW_38G_R6A_R12A_R12B_scope_tightening_and_guard_repair.ps1 -Build
```
