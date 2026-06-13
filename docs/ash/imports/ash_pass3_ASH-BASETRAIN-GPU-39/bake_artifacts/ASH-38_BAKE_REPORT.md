# ASH-38 Bake Report

## Commit
ASH-38 — Adapter Specialization / Event Tag Routing

## SSOT
Source zip: ash_pass3_ASH-37_event_weighted_lora_sft_planner_baked.zip

## Added
- crates/ash_core/src/adapter_event_specialization.rs
- crates/ash_core/src/event_tag_routing_policy.rs
- crates/ash_core/src/adapter_activation_policy.rs
- crates/orchestrator_local/src/ash_38_adapter_specialization_report.rs
- crates/orchestrator_local/src/bin/ash_38_adapter_specialization_audit.rs
- crates/ash_core/tests/ash_38_adapter_event_specialization.rs
- crates/ash_core/tests/ash_38_event_tag_routing_policy.rs
- crates/ash_core/tests/ash_38_adapter_activation_policy.rs
- crates/orchestrator_local/tests/ash_38_adapter_specialization_report.rs
- acceptance_reports/ASH-38_adapter_specialization_event_tag_routing.md

## Modified
- crates/ash_core/src/lib.rs
- crates/orchestrator_local/src/lib.rs

## Guardrails
- No SFT execution.
- No JSONL export.
- No runtime auto-apply.
- No adapter registry mutation.
- No current pointer mutation.
- No LoRA tensor mutation.
- No Python validator.

## Expected audit log
[ash_core][ASH-38] PASS_ADAPTER_SPECIALIZATION_EVENT_TAG_ROUTING
