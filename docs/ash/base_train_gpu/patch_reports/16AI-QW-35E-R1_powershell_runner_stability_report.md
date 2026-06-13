# 16AI-QW-35E-R1 — PowerShell Runner Stability Hotfix

## Status
PASS_STATIC

## Purpose
Fix `scripts/run_16AI_QW_35E_semantic_split.ps1` so Windows PowerShell 5.1 does not surface Cargo stderr warnings as `NativeCommandError` at the direct call site.

## Changed
- Replaced direct native invocation:
  - `& cargo @argsList 1> $StdoutPath 2> $StderrPath`
- With `Start-Process -Wait -PassThru` and explicit stdout/stderr redirection.
- Cargo failure is now judged only by process exit code.
- Warnings remain in stderr log and no longer stop the script.
- `$ErrorActionPreference` changed from `Stop` to `Continue` for the runner.
- Base compare is skipped safely if the base run did not complete.

## Non-Goals
- No model weight mutation.
- No tokenizer mutation.
- No safetensors mutation.
- No LoRA mutation.
- No prompt default mutation.

## Runtime Command
```powershell
.\scripts\run_16AI_QW_35E_semantic_split.ps1
```

## Expected Console
```txt
[16AI-QW-35E][cargo] stdout=...
[16AI-QW-35E][cargo] stderr=...
[16AI-QW-35E][run] kind=base_only exit_code=0 ...
[16AI-QW-35E][ok] cargo exit_code=0 kind=base_only
```
