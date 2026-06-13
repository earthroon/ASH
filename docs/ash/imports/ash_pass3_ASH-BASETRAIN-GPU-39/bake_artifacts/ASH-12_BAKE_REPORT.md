# ASH-12 Bake Report

## Commit
ASH-12 — RuntimeLoraAttachment loader connect / current pointer attach execution

## Source SSOT
ash_pass3_ASH-11_runtime_current_pointer_explicit_base_only_gate_baked.zip

## Files added/modified
- crates/runtime/src/ash_lora_attach_execution.rs
- crates/runtime/tests/ash_lora_attach_execution.rs
- crates/runtime/src/lib.rs
- crates/runtime/src/ash_current_pointer.rs
- crates/artifact_store/src/ash_synapse_registry_store.rs
- crates/artifact_store/src/ash_rollback_store.rs
- crates/orchestrator_local/src/ash_lora_attach_execution_integration.rs
- crates/orchestrator_local/src/bin/ash_12_lora_attach_audit.rs
- crates/orchestrator_local/tests/ash_lora_attach_execution_integration.rs
- crates/orchestrator_local/src/lib.rs
- acceptance_reports/ASH-12_runtime_lora_attachment_loader_connect.md

## Sealed
- current pointer attach request -> load plan
- RuntimeLoraAttachment sidecar render/write
- existing runtime LoRA sidecar loader execution
- attached_lora_ids / missing_lora_ids report
- explicit base-only pass without load attempt
- rejected load failure without silent fallback

## Validation commands
```powershell
cargo test -p runtime ash_lora_attach_execution
cargo test -p orchestrator_local ash_lora_attach_execution_integration
cargo run -p orchestrator_local --bin ash_12_lora_attach_audit
```

## Environment note
The bake environment does not provide cargo/rustc, so compile/runtime validation is pending on the user's machine. Static file/string sanity was performed.
