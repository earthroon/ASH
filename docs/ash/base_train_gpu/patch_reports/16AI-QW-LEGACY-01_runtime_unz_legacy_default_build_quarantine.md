# 16AI-QW-LEGACY-01 — Runtime UNZ Legacy Default Build Quarantine / API Drift Isolation Seal

## Patch Type
Build graph quarantine patch.

## SSOT
`crates/runtime_unz` remains a workspace member and source tree is preserved, but `crates/runtime_unz` is removed from root `default-members` so normal `cargo build` and R12A-R1 hidden trace capture builds are not blocked by archived runtime API drift.

## Confirmed Upstream Blocker
The prior R12A-R1 build reached `runtime_unz_legacy` and failed because the legacy tree references removed or drifted APIs: `DecodeTokenGroups`, `GuidedDecodeConfig`, `TokenizerManifest.vocab_size`, missing `AshDecisionInput.loop_index`, and `ReferenceModel.guided_generate`.

## Changes
- Removed `crates/runtime_unz` from workspace `default-members`.
- Preserved `crates/runtime_unz` in workspace `members` for explicit legacy repair builds.
- Added `scripts/run_16AI_QW_LEGACY_01_runtime_unz_quarantine.ps1` for default build and metadata evidence.
- Added receipt/report placeholders under `workspace/`.

## Guard
- No legacy source deletion.
- No fake compatibility shim.
- No model_core API rollback.
- No R12A-R1 hidden capture logic mutation.
