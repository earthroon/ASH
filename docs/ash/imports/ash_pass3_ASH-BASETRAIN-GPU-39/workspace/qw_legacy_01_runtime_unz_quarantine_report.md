# 16AI-QW-LEGACY-01 — Runtime UNZ Legacy Default Build Quarantine / API Drift Isolation Seal

## Status
STATIC_PASS_RUNTIME_UNZ_LEGACY_DEFAULT_BUILD_QUARANTINE

## SSOT
- patch_id: 16AI-QW-LEGACY-01
- purpose: quarantine runtime_unz_legacy from default build
- legacy_deleted: false
- legacy_api_drift_repaired: false
- script_only_bypass_used: false

## Source Failure
- failed_crate: runtime_unz_legacy
- failed_path: crates/runtime_unz/src/infer.rs
- error_axes:
  - missing model_core::DecodeTokenGroups
  - missing model_core::GuidedDecodeConfig
  - TokenizerManifest.vocab_size drift
  - AshDecisionInput.loop_index required
  - ReferenceModel.guided_generate missing

## Workspace Graph
- runtime_unz_legacy_workspace_member: true
- runtime_unz_legacy_default_member: false
- runtime_unz_legacy_default_build_compiled: false

## Guard
- legacy source deletion: forbidden
- model_core API rollback: forbidden
- fake guided_generate shim: forbidden
