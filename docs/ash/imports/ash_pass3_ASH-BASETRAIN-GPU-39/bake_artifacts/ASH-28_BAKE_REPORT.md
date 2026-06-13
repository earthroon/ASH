# ASH-28 Bake Report

## Commit
ASH-28 — Runtime Composite Attachment Smoke Gate

## SSOT Input
ASH-27 baked source tree.

## Implemented Files
- crates/ash_core/src/runtime_composite_smoke_gate.rs
- crates/ash_core/src/composite_promotion_ready.rs
- crates/runtime/src/ash_composite_attachment_smoke.rs
- crates/orchestrator_local/src/ash_28_runtime_composite_smoke_report.rs
- crates/orchestrator_local/src/bin/ash_28_runtime_composite_smoke_audit.rs
- crates/ash_core/tests/ash_28_runtime_composite_smoke_gate.rs
- crates/ash_core/tests/ash_28_composite_promotion_ready.rs
- crates/runtime/tests/ash_composite_attachment_smoke.rs
- crates/orchestrator_local/tests/ash_28_runtime_composite_smoke_report.rs

## Guardrails
- current pointer is not changed
- promotion is not automatic
- rollback is not automatic
- ASH-23 attached_lora_weights must be present for AdapterEnabled smoke pass
- replay-blocked candidates are blocked before smoke pass
- ready evidence requires manual promotion and current pointer gate
- no Python validator added

## Runtime Validation
Rust cargo/rustc is unavailable in this environment, so compile/tests were not executed here. Static file audit and zip integrity checks were used instead.
