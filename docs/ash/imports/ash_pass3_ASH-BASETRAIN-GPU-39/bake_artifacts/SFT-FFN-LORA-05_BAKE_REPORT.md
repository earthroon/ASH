# SFT-FFN-LORA-05 Bake Report

## Patch

SFT-FFN-LORA-05 — Adapter Artifact Candidate Capture / No Runtime Attach Seal

## Added

- `crates/ash_core/src/sft_ffn_lora_artifact_candidate.rs`
- `crates/ash_core/tests/sft_ffn_lora_05_artifact_candidate_capture.rs`
- `crates/burn_webgpu_backend/src/ffn_lora_artifact_candidate.rs`
- `acceptance_reports/SFT-FFN-LORA-05_adapter_artifact_candidate_capture.md`
- `bake_artifacts/SFT-FFN-LORA-05_BAKE_REPORT.md`
- `bake_artifacts/SFT-FFN-LORA-05_STATIC_VALIDATION.txt`

## Modified

- `crates/ash_core/src/lib.rs`
- `crates/burn_webgpu_backend/src/lib.rs`

## Opened

- adapter artifact candidate capture
- artifact candidate write
- adapter manifest candidate
- payload digest evidence
- safetensors candidate digest evidence
- training lineage digest
- no runtime attach guard

## Kept Closed

- runtime attach
- promotion apply
- current pointer update
- slot ready mark
- ASH binding
- SFT training execution in core
- gradient write in core
- optimizer step in core

## SSOT

SFT-FFN-LORA-05 captures updated LoRA A/B as an adapter artifact candidate and seals manifest digest, payload digest, safetensors candidate digest, and lineage digest while keeping runtime attach, promotion, current pointer update, slot-ready mark, and ASH binding closed.
