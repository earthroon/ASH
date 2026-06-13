# 16AI-QW-38G-R6A-R12A-R4-R1 — Component Attribution Runner Build Exit Capture / Run Phase Handoff Seal

## Status
STATIC_BAKED

## Purpose
R4-R1 patches the R4 runner handoff only. It does not change the R4 component attribution logic, hidden capture logic, model weights, tokenizer, final norm, LM head, or ban mask.

## Source Failure
The R4 runner allowed cargo warning output to flow through the same PowerShell pipeline used for the build exit code. This polluted the `[build_done] exit_code=` field with warning text and prevented a clean build/run/artifact handoff judgement.

## Changes
- `Invoke-Qw38gLoggedNative` now redirects native process output to a log file through `cmd.exe`.
- Native output is displayed with `Write-Host`, not returned into the pipeline.
- Build and run exit codes are cast to numeric `[int]` values.
- R4 binary handoff manifest is written.
- R4 required artifacts are checked after run.
- R4-R1 handoff receipt, summary, trace, and report are written.
- Dedicated R4-R1 wrapper script was added.

## Guard
- r4_component_logic_modified: false
- tokenizer_modified: false
- safetensors_modified: false
- lm_head_modified: false
- final_norm_modified: false
- ban_mask_modified: false
