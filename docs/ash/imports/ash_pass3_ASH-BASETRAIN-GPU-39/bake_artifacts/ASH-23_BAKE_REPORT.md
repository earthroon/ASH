# ASH-23 Bake Report

## Status
PASS_STATIC_BAKE

## SSOT
Input SSOT: ASH-22 baked tree.
Output artifact: ASH-23 runtime ensemble weight telemetry baked tree.

## Implemented Files
- `crates/runtime/src/ash_lora_weight_telemetry.rs`
- `crates/runtime/tests/ash_lora_weight_telemetry.rs`
- `crates/orchestrator_local/src/ash_23_lora_weight_final_merge.rs`
- `crates/orchestrator_local/src/bin/ash_23_lora_weight_telemetry_audit.rs`
- `crates/orchestrator_local/tests/ash_23_lora_weight_final_merge.rs`
- `acceptance_reports/ASH-23_runtime_ensemble_weight_telemetry.md`

## Modified Files
- `crates/runtime/src/ash_infer_entry_envelope.rs`
- `crates/runtime/src/ash_streaming_telemetry.rs`
- `crates/runtime/src/lib.rs`
- `crates/orchestrator_local/src/ash_final_output_merge.rs`
- `crates/orchestrator_local/src/lib.rs`

## Sealed Checks
- `attached_lora_ids` remains unchanged.
- `attached_lora_weights` is added using snake_case.
- SoftEnsemble and CompositeProfile weight builders are present.
- Streaming header carries weight telemetry.
- Final orchestrator telemetry carries weight telemetry.
- Missing weights are surfaced through `weight_missing` and validation failures.
- Adapter id/weight mismatches are surfaced through `weight_mismatch_detected` and validation failures.
- BaseOnlyExplicit requires empty weights.
- Python validator was not added.

## Judgment
Rust compiler was unavailable in the execution container, so this bake is statically audited and zipped. Run the Rust-native commands in a local Rust environment.
