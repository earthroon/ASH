# SFT-FFN-LORA-16 Bake Report

## Patch

SFT-FFN-LORA-16 — Operator-Reviewed Slot Action Apply / Lifecycle Transition Gate

## Base

ash_pass3_SFT-FFN-LORA-15_lifecycle_ledger_baked.zip

## Added

- crates/ash_core/src/sft_ffn_lora_slot_action_apply.rs
- crates/ash_core/tests/sft_ffn_lora_16_slot_action_apply.rs
- crates/burn_webgpu_backend/src/ffn_lora_slot_action_apply.rs
- crates/burn_webgpu_backend/tests/ffn_lora_slot_action_apply.rs
- acceptance_reports/SFT-FFN-LORA-16_slot_action_apply.md
- bake_artifacts/SFT-FFN-LORA-16_BAKE_REPORT.md
- bake_artifacts/SFT-FFN-LORA-16_STATIC_VALIDATION.txt
- bake_artifacts/SFT-FFN-LORA-16_FILE_DIGESTS.sha256

## Modified

- crates/ash_core/src/lib.rs
- crates/burn_webgpu_backend/src/lib.rs

## Opened

- operator-reviewed slot action apply
- operator review receipt
- slot action plan
- apply preflight
- apply receipt
- lifecycle transition event
- reviewed current pointer update
- reviewed demotion apply
- reviewed quarantine apply
- reviewed fallback activation

## Kept Closed

- unreviewed action apply
- recommendation mismatch apply
- promotion apply rerun
- rollback execution
- SFT training execution in core
- gradient write in core
- optimizer step in core
- textureSample weight fetch

## Notes

This bake adds only the LORA-16 reviewed-action gate. It does not add a runtime action executor beyond the backend boundary shell.
