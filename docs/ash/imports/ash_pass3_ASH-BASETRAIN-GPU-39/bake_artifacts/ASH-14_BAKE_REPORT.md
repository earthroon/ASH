# ASH-14 Bake Report

## Commit
ASH-14 — causal_lm / infer_entry direct envelope consumption

## Source baseline
ASH-13 runtime current attachment into inference request baked zip.

## Files added
- crates/runtime/src/ash_causal_lm_envelope.rs
- crates/runtime/src/ash_infer_entry_envelope.rs
- crates/runtime/tests/ash_causal_lm_envelope.rs
- crates/runtime/tests/ash_infer_entry_envelope.rs
- crates/orchestrator_local/src/ash_direct_inference_integration.rs
- crates/orchestrator_local/src/bin/ash_14_direct_inference_audit.rs
- crates/orchestrator_local/tests/ash_direct_inference_integration.rs

## Files updated
- crates/runtime/src/lib.rs
- crates/orchestrator_local/src/lib.rs

## Sealed
- ASH-13 request envelope can be consumed by causal_lm/infer_entry wrapper entries.
- AdapterEnabled inference cannot start without attached_lora_ids.
- BaseOnlyExplicit is explicit and allows empty attached_lora_ids.
- Rejected attachments are blocked before inner inference.
- Output telemetry preserves attached_lora_ids, missing_lora_ids, runtime_registry_ready, base_only_explicit, silent_fallback_detected, target_auto_remap_detected, inference_started, and inference_completed.

## Validation commands
```powershell
cargo test -p runtime ash_causal_lm_envelope
cargo test -p runtime ash_infer_entry_envelope
cargo test -p orchestrator_local ash_direct_inference_integration
cargo run -p orchestrator_local --bin ash_14_direct_inference_audit
```

## Runtime limitation
This bake environment did not run cargo/rustc. Static file/string sanity was performed instead.
