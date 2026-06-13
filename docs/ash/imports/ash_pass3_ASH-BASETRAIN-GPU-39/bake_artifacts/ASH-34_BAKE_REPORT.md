# ASH-34 Bake Report

## SSOT
Source archive: ASH-33 baked state.

## Added
- crates/ash_core/src/event_driven_lora_router.rs
- crates/ash_core/src/temporal_penalty_overlay.rs
- crates/ash_core/src/lora_cooldown_ledger.rs
- crates/runtime/src/ash_lora_runtime_events.rs
- crates/orchestrator_local/src/ash_34_event_driven_lora_report.rs
- crates/orchestrator_local/src/bin/ash_34_event_driven_lora_audit.rs
- crates/ash_core/tests/ash_34_event_driven_lora_router.rs
- crates/ash_core/tests/ash_34_temporal_penalty_overlay.rs
- crates/ash_core/tests/ash_34_lora_cooldown_ledger.rs
- crates/runtime/tests/ash_lora_runtime_events.rs
- crates/orchestrator_local/tests/ash_34_event_driven_lora_report.rs
- acceptance_reports/ASH-34_event_driven_lora_activation_temporal_penalty.md

## Modified
- crates/ash_core/src/lib.rs
- crates/runtime/src/lib.rs
- crates/orchestrator_local/src/lib.rs

## Contract
ASH-34 adds event-driven short-term suppression. It does not mutate source route plans, soft ensemble plans, registries, current pointers, or LoRA tensors.
