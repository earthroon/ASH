# SFT-FFN-INFRA-PERF-01 Bake Report

## Patch

SFT-FFN-INFRA-PERF-01 — Hot Path Allocation Hygiene / Error Enum + Stable Hash Input Seal

## Added

- `crates/ash_core/src/infra_error.rs`
- `crates/ash_core/src/infra_string.rs`
- `crates/ash_core/src/infra_hash.rs`
- `crates/ash_core/tests/sft_ffn_infra_perf_01_hot_path_hygiene.rs`
- `crates/burn_webgpu_backend/src/ffn_infra_perf_hygiene.rs`
- `acceptance_reports/SFT-FFN-INFRA-PERF-01_hot_path_allocation_hygiene.md`

## Modified

- `crates/ash_core/src/lib.rs`
- `crates/ash_core/src/event_driven_lora_router.rs`
- `crates/ash_core/src/event_sft_sample_ledger.rs`
- `crates/ash_core/src/event_tag_router_calibration.rs`
- `crates/burn_webgpu_backend/src/lib.rs`

## Opened

- lightweight `AshInfraError` enum/code path
- lazy public String rendering
- centralized string dedup utility
- calibration weight config for ASH-45 router calibration
- legacy-preserving allocation-free hash feeding via `stable_hash_fmt_v2(format_args!(...))`
- clone audit marker and `AshSharedStr` candidate

## Closed

- runtime attach
- promotion apply
- current pointer update
- slot ready mark
- ASH binding
- routing semantic change
- seal id semantic change

## Local validation

`cargo`, `rustc`, and `rustfmt` were not available in this execution environment. Static validation was performed instead.
