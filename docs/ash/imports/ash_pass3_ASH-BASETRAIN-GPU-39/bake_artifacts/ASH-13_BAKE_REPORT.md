# ASH-13 Bake Report

## Commit
ASH-13 — Runtime current attachment into inference request / attached_lora telemetry seal

## Baked files
- crates/runtime/src/ash_inference_attachment.rs
- crates/runtime/tests/ash_inference_attachment.rs
- crates/runtime/src/lib.rs
- crates/orchestrator_local/src/ash_inference_attachment_integration.rs
- crates/orchestrator_local/src/bin/ash_13_inference_attachment_audit.rs
- crates/orchestrator_local/tests/ash_inference_attachment_integration.rs
- crates/orchestrator_local/src/lib.rs
- acceptance_reports/ASH-13_runtime_current_attachment_into_inference_request.md
- bake_artifacts/ASH-13_BAKE_REPORT.md
- bake_artifacts/ASH-13_STATIC_SANITY.txt

## Contract
ASH-13 carries RuntimeLoraAttachExecutionReport into an inference request envelope and preserves attached_lora_ids, missing_lora_ids, runtime_registry_ready, base_only_explicit, silent_fallback_detected, and target_auto_remap_detected telemetry.

## Rust-native validation commands
```powershell
cargo test -p runtime ash_inference_attachment
cargo test -p orchestrator_local ash_inference_attachment_integration
cargo run -p orchestrator_local --bin ash_13_inference_attachment_audit
```

## Python
No ASH-13 Python validator is added.
