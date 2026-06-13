# ASH-15 Bake Report

## Commit
ASH-15 runtime streaming telemetry header / orchestrator final attached_lora output merge seal

## Applied files
- crates/runtime/src/ash_streaming_telemetry.rs
- crates/runtime/src/ash_infer_entry_envelope.rs
- crates/runtime/src/lib.rs
- crates/runtime/tests/ash_streaming_telemetry.rs
- crates/orchestrator_local/src/ash_final_output_merge.rs
- crates/orchestrator_local/src/bin/ash_15_output_merge_audit.rs
- crates/orchestrator_local/src/lib.rs
- crates/orchestrator_local/tests/ash_final_output_merge.rs
- acceptance_reports/ASH-15_streaming_telemetry_final_output_merge.md

## Seal
ASH-14 output telemetry is now surfaced through streaming header events and orchestrator final output DTOs.
The final output rejects AdapterEnabled responses without attached_lora_ids, preserves explicit base-only mode, and prevents rejected runtime output from becoming PASS output.
