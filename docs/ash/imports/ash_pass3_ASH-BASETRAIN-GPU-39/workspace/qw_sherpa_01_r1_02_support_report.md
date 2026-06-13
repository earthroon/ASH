# 16AI-QW-SHERPA-01-R1 + SHERPA-02 Support Report

## Status
STATIC_PASS

## Summary
- Workspace default build no longer includes `asr_sidecar` as a default member.
- `asr_sidecar` no longer has a direct optional dependency on `sherpa-rs-sys`; it enters the sys crate through `sherpa-rs` only when `speech_sherpa` is enabled.
- `sherpa-rs-sys/build.rs` now auto-selects an available Windows CMake generator and supports `SHERPA_CMAKE_GENERATOR`.
- PowerShell runner native output no longer contaminates function return values.

## Compile
Not executed in this container because Rust/Cargo is unavailable here.

## Next local commands
```powershell
.\scripts\run_16AI_QW_38G_R6A_R12A_R1_trace_capture_expansion.ps1 -Build
.\scripts\run_16AI_QW_SHERPA_02_windows_build_support.ps1 -AsrStubBuild
.\scripts\run_16AI_QW_SHERPA_02_windows_build_support.ps1 -SpeechSherpaBuild
```
