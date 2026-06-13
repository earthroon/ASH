# 16AI-QW-38G-R6A-R12A-R7-R1 — PowerShell JSON Depth Clamp / R7 Artifact Flattening Seal

## Status
STATIC_PASS_R7_ARTIFACT_WRITER_DEPTH_CLAMP

## Purpose
Fix the R7 runner artifact writer failure where `ConvertTo-Json -Depth 120` exceeded PowerShell's maximum allowed depth of 100.

## Changes
- Added `Convert-R7SafeJson` helper that clamps requested JSON depth to `[1, 100]`.
- Replaced direct `ConvertTo-Json -Depth 120` writes with `Write-R7Json` defaulting to depth 80.
- Added `Append-R7JsonLine` for shallow JSONL trace records.
- Flattened the R7 summary trace record so the deep raw event payload remains in `raw_trace_path` and does not get duplicated into a deeply nested trace line.

## Guard
- R7 causal probe logic unchanged.
- Checkpoint/tokenizer/safetensors/lm_head/final_norm/ban_mask unchanged.
- Diagnostic-only intervention semantics preserved.
