# 16AI-QW-SHERPA-01-R1 — Workspace Default Member Isolation / Sherpa Sys Graph Escape Seal

## Status
STATIC_PATCHED_COMPILE_NOT_EXECUTED_IN_CONTAINER

## SSOT
- Root `Cargo.toml` now keeps `crates/asr_sidecar` as a workspace member but removes it from `default-members`.
- `cargo build` at workspace root should build default members only and should not enter `asr_sidecar` or `sherpa-rs-sys`.
- `asr_sidecar` remains buildable explicitly with `cargo build -p asr_sidecar --no-default-features`.

## Changes
- Added `[workspace].default-members` excluding `crates/asr_sidecar`.
- Added `[workspace].exclude` for vendor sherpa crates so nested vendor workspace is never treated as an active workspace member.
- Removed direct optional `sherpa-rs-sys` dependency from `crates/asr_sidecar`.
- Kept `speech_sherpa = ["dep:sherpa-rs"]` as the single speech backend feature gate.
- Changed `online.rs` to import sys through `sherpa_rs::sherpa_rs_sys` only when `speech_sherpa` is enabled.

## Guard
- vendor sherpa deletion: forbidden and not performed
- script-only bypass: not used
- silent speech fallback: forbidden and not performed
