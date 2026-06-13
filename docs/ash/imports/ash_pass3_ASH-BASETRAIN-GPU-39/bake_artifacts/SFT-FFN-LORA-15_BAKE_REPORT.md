# SFT-FFN-LORA-15 Bake Report

## Status

Baked on top of SFT-FFN-INFRA-PERF-03 / LORA-14 line.

## Added

- `crates/ash_core/src/sft_ffn_lora_lifecycle_ledger.rs`
- `crates/ash_core/tests/sft_ffn_lora_15_lifecycle_ledger.rs`
- `crates/burn_webgpu_backend/src/ffn_lora_lifecycle_ledger.rs`
- `crates/burn_webgpu_backend/tests/ffn_lora_lifecycle_ledger.rs`
- `acceptance_reports/SFT-FFN-LORA-15_lifecycle_ledger.md`

## Modified

- `crates/ash_core/src/lib.rs`
- `crates/burn_webgpu_backend/src/lib.rs`

## Opened

- adapter lifecycle ledger
- lifecycle event table
- lifecycle snapshot
- promotion / health / rollback / arbitration history
- demotion recommendation history
- quarantine recommendation history
- append-only ledger integrity guard

## Closed

- current pointer update
- promotion apply rerun
- rollback execution
- demotion apply
- quarantine apply
- SFT training execution in core
- gradient write in core
- optimizer step in core

## Notes

This bake intentionally separates recommendation states from applied lifecycle actions. `DemotionRecommended` and `QuarantineRecommended` can be recorded, but demotion/quarantine apply remains closed.
