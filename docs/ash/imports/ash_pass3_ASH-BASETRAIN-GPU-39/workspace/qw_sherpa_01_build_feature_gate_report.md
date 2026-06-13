# 16AI-QW-SHERPA-01 — Sherpa Build Feature Gate / Optional Speech Backend Isolation Seal

## Status
STATIC_PASS_SHERPA_BUILD_FEATURE_GATE

## SSOT
- patch_id: 16AI-QW-SHERPA-01
- purpose: isolate sherpa-rs/sherpa-rs-sys from the default asr_sidecar build graph
- speech_sherpa_default_off: True
- vendor_sherpa_present_in_bake: False
- vendor_path_references_preserved: True
- vendor_sherpa_deleted: False
- script_only_bypass_used: False
- sherpa_support_removed: False

## Source Failure Addressed
- failed axis: sherpa-rs-sys custom build blocked unrelated R12A-R1 audit build
- SHERPA-01 fix: move sherpa-rs/sherpa-rs-sys behind explicit `speech_sherpa` feature
- SHERPA-02 remains responsible for Windows CMake generator support when `speech_sherpa` is enabled

## Cargo Feature Graph
- asr_sidecar_member_preserved: True
- speech_sherpa_feature_exists: True
- sherpa_dependency_optional: True
- sherpa_sys_dependency_optional: True
- default feature set: []

## Rust Module Gate
- adapter_cfg_gated: True
- online_cfg_gated: True
- transcribe_cfg_gated: True

## Stub Backend
- stub_backend_exists: True
- speech_disabled_returns_explicit_unsupported: True

## Build Execution
- compile_pass_default: not executed in bake container
- compile_pass_no_default_features: not executed in bake container
- compile_pass_speech_sherpa: not executed in bake container
- reason: cargo unavailable in bake container

## Local Verification Commands
```powershell
.\scripts\run_16AI_QW_SHERPA_01_build_feature_gate.ps1 -Tree -Build -NoDefault
.\scripts\run_16AI_QW_SHERPA_01_build_feature_gate.ps1 -SpeechSherpa
```

## Guard
- vendor sherpa deletion: forbidden / no delete action performed
- script-only bypass: forbidden / Cargo feature graph changed instead
- silent speech fallback: forbidden / explicit unsupported stub installed
- R12A-R1 hidden capture logic: not modified by this patch

## Recommended Next
16AI-QW-SHERPA-02 — Sherpa CMake Generator Detection / Windows Build Support Seal
