# SFT-FFN-LORA-10 Bake Report

## Commit

SFT-FFN-LORA-10 — Guarded Promotion Apply Candidate / Rollback Ledger Seal

## Base

Baked on top of SFT-FFN-INFRA-GPU-SAFETY-01.

## Added

- `crates/ash_core/src/sft_ffn_lora_promotion_apply_candidate.rs`
- `crates/ash_core/tests/sft_ffn_lora_10_promotion_apply_candidate.rs`
- `crates/burn_webgpu_backend/src/ffn_lora_promotion_apply_candidate.rs`
- `acceptance_reports/SFT-FFN-LORA-10_promotion_apply_candidate.md`
- `bake_artifacts/SFT-FFN-LORA-10_STATIC_VALIDATION.txt`
- `bake_artifacts/SFT-FFN-LORA-10_FILE_DIGESTS.sha256`

## Modified

- `crates/ash_core/src/lib.rs`
- `crates/burn_webgpu_backend/src/lib.rs`

## Opened

- promotion apply candidate
- apply preflight evidence
- rollback ledger candidate
- rollback handle digest
- rollback restore target
- failure demotion path
- current pointer unchanged guard

## Still Closed

- promotion apply commit
- current pointer update
- slot ready mark
- ASH binding
- SFT training execution in core
- gradient write in core
- optimizer step in core

## Verification

Static validation was performed in this environment. Local Rust compilation remains pending because this environment does not provide `cargo`, `rustc`, or `rustfmt`.
