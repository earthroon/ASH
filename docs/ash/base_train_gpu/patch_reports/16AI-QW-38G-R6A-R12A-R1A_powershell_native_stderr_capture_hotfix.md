# 16AI-QW-38G-R6A-R12A-R1A — PowerShell Native stderr Capture Hotfix

## Status
STATIC_HOTFIX_BAKED_COMPILE_NOT_EXECUTED_IN_CONTAINER

## Cause
Windows PowerShell can wrap native stderr written through `2>&1 | Tee-Object` as `NativeCommandError`. Cargo prints normal progress and warning lines to stderr, so a normal line such as `Compiling memchr v2.8.0` can be surfaced as a script error before the native exit code is adjudicated.

## Change
- Replaced `cargo build 2>&1 | Tee-Object` with `cmd.exe /d /s /c "cargo build > log 2>&1"`.
- Replaced `infer_only.exe 2>&1 | Tee-Object` with the same logged native command helper.
- Preserved native exit code as the only build/run verdict.
- Preserved existing R12A-R1 env gates and artifacts.

## Guard
- No Rust model logic mutation.
- No lm_head mutation.
- No final_norm mutation.
- No tokenizer mutation.
- No safetensors mutation.
- No ban mask mutation.
