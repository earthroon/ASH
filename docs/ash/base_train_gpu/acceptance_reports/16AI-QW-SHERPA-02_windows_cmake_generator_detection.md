# 16AI-QW-SHERPA-02 — Sherpa CMake Generator Detection / Windows Build Support Seal

## Status
STATIC_PATCHED_COMPILE_NOT_EXECUTED_IN_CONTAINER

## SSOT
- `sherpa-rs-sys/build.rs` now selects a Windows CMake generator before `Config::build()`.
- Explicit env is supported: `SHERPA_CMAKE_GENERATOR`, `CMAKE_GENERATOR`, `HOST_CMAKE_GENERATOR`.
- If an env generator is unavailable in `cmake --help`, it is rejected with a warning and fallback candidates are tried.
- Fallback order: `Visual Studio 17 2022`, `Visual Studio 16 2019`, `Visual Studio 15 2017`, `Ninja`, `NMake Makefiles`.

## Why
The observed failure requested `Visual Studio 18 2026`, while installed CMake advertised `Visual Studio 17 2022`. This patch prevents cmake crate auto-detection from choosing an unavailable VS 18 generator when a valid local generator exists.

## Commands
- Default inference/audit build: `cargo build`
- ASR stub build: `cargo build -p asr_sidecar --no-default-features`
- Sherpa support build: `cargo build -p asr_sidecar --features speech_sherpa`
- Optional override: `$env:SHERPA_CMAKE_GENERATOR = "Visual Studio 17 2022"`

## Guard
- sherpa support is not removed
- vendor source is preserved
- CMake generator is selected in Rust `build.rs`, not by PowerShell-only bypass
