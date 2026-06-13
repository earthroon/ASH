# 16AI-QW-38G-R6A-LORA-RT-02B-C

## PowerShell ProcessStartInfo Native Stderr Isolation Hotfix

This hotfix replaces the remaining direct native command invocation in `lora_rt02b_full_backoff.ps1` with `System.Diagnostics.ProcessStartInfo`.

Reason:
Windows PowerShell 5.1 may still surface native stderr lines as `NativeCommandError` even with `2>` redirection when `$ErrorActionPreference = "Stop"` is active. The orchestrator debug stderr line is not necessarily a process failure.

Implemented:
- No `& .\target\debug\orchestrator_local.exe` native invocation in the backoff runner.
- stdin/stdout/stderr are handled through redirected .NET process streams.
- stdout and stderr are written to log files explicitly.
- only non-zero process exit code fails the wrapper.
- scripts remain ASCII-only.
