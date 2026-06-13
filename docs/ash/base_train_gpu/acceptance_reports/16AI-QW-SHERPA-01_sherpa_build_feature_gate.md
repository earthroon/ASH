# 16AI-QW-SHERPA-01 Acceptance — Sherpa Build Feature Gate

## Static Acceptance
- speech_sherpa_feature_exists: True
- speech_sherpa_default_off: True
- sherpa_dependency_optional: True
- sherpa_sys_dependency_optional: True
- sherpa_path_references_preserved: True
- sherpa_modules_cfg_gated: True
- sherpa_stub_backend_exists: True
- speech_disabled_returns_explicit_unsupported: True
- script_only_bypass_used: False
- vendor_sherpa_deleted: False
- sherpa_support_removed: False

## Runtime Acceptance
- compile_pass_default: not executed in bake container
- compile_pass_no_default_features: not executed in bake container
- r12a_r1_build_unblocked_by_sherpa: pending local cargo run

## Local Commands
```powershell
.\scripts\run_16AI_QW_SHERPA_01_build_feature_gate.ps1 -Tree -Build -NoDefault
# Optional support path, expected to remain SHERPA-02 territory if CMake generator still fails:
.\scripts\run_16AI_QW_SHERPA_01_build_feature_gate.ps1 -SpeechSherpa
```
