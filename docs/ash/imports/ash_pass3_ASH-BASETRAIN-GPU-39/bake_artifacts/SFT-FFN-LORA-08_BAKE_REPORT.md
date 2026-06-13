# SFT-FFN-LORA-08 Bake Report

## Patch

SFT-FFN-LORA-08 — Operator Approval Receipt / Promotion Intent Seal

## Applied on

SFT-FFN-LORA-07 promotion review candidate baked tree.

## Added

- `crates/ash_core/src/sft_ffn_lora_operator_approval.rs`
- `crates/ash_core/tests/sft_ffn_lora_08_operator_approval.rs`
- `crates/burn_webgpu_backend/src/ffn_lora_operator_approval.rs`
- `acceptance_reports/SFT-FFN-LORA-08_operator_approval_receipt.md`
- `bake_artifacts/SFT-FFN-LORA-08_BAKE_REPORT.md`
- `bake_artifacts/SFT-FFN-LORA-08_STATIC_VALIDATION.txt`

## Modified

- `crates/ash_core/src/lib.rs`
- `crates/burn_webgpu_backend/src/lib.rs`

## Opened

- operator approval receipt recording
- promotion intent recording
- operator identity digest
- operator approval signature digest
- approval count evidence
- review packet digest match
- artifact digest match
- eval digest match
- no runtime mutation guard

## Kept closed

- runtime attach
- promotion apply
- current pointer update
- slot ready mark
- ASH binding
- SFT training execution in core
- gradient write in core
- optimizer step in core

## Notes

This bake records approval intent only. It does not attach the approved adapter to runtime and does not mutate the current pointer.
