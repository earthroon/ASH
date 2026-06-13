# SFT-FFN-INFRA-PERF-03 Bake Report

## Patch

SFT-FFN-INFRA-PERF-03 — Infer Entry JSON Projection / Manual Probe Mapping Collapse Seal

## Base

`ash_pass3_SFT-FFN-LORA-14_slot_arbitration_baked.zip`

## Added

- `crates/orchestrator_local/src/infer_entry_json_projection.rs`
- `crates/orchestrator_local/tests/infer_entry_json_projection.rs`
- `acceptance_reports/SFT-FFN-INFRA-PERF-03_infer_entry_json_projection.md`
- `bake_artifacts/SFT-FFN-INFRA-PERF-03_BAKE_REPORT.md`
- `bake_artifacts/SFT-FFN-INFRA-PERF-03_STATIC_VALIDATION.txt`
- `bake_artifacts/SFT-FFN-INFRA-PERF-03_FILE_DIGESTS.sha256`

## Modified

- `crates/orchestrator_local/src/infer_entry.rs`
- `crates/orchestrator_local/src/lib.rs`
- `crates/runtime/src/infer.rs`

## Opened

- serde result projection
- probe serde projection
- centralized infer-entry compatibility aliases
- entry overlay merge
- projection seal emission

## Closed

- manual low-level probe mapping inside `infer_entry.rs`
- current pointer update
- promotion apply rerun
- runtime mutation
- SFT training / gradient / optimizer

## Notes

Compatibility aliases are still centralized in `infer_entry_json_projection.rs` so existing top-level output/response fields remain available while new result/probe fields can flow through the serde projection automatically.
