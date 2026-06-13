# ASH-33 Bake Report

## Commit
ASH-33 — Runtime Composite Latency / Memory Guard

## Source SSOT
ASH-32 baked workspace / zip.

## Added
- crates/ash_core/src/runtime_composite_perf_guard.rs
- crates/ash_core/src/runtime_composite_memory_guard.rs
- crates/ash_core/src/composite_perf_gate_evidence.rs
- crates/runtime/src/ash_composite_perf_observer.rs
- crates/orchestrator_local/src/ash_33_runtime_composite_perf_guard_report.rs
- crates/orchestrator_local/src/bin/ash_33_runtime_composite_perf_guard_audit.rs
- crates/ash_core/tests/ash_33_runtime_composite_perf_guard.rs
- crates/ash_core/tests/ash_33_runtime_composite_memory_guard.rs
- crates/ash_core/tests/ash_33_composite_perf_gate_evidence.rs
- crates/runtime/tests/ash_composite_perf_observer.rs
- crates/orchestrator_local/tests/ash_33_runtime_composite_perf_guard_report.rs
- acceptance_reports/ASH-33_runtime_composite_latency_memory_guard.md

## Modified
- crates/ash_core/src/lib.rs
- crates/runtime/src/lib.rs
- crates/orchestrator_local/src/lib.rs

## Sealed Behavior
- Runtime observed metrics are explicit and never zero-filled.
- Missing required metrics return NeedsRuntimeMeasurement.
- Latency and memory hard limits can block promotion.
- Warning pressure can generate compression recommendation without executing compression.
- Critical pressure on a current pointer recommends rollback review without executing rollback.
- ASH-28 smoke pass can be required before perf evaluation.
- Attached LoRA weights from ASH-23 smoke telemetry can be required.
- Current pointer and artifact registry are not mutated.

## Compile Note
cargo/rustc/rustfmt were unavailable in this container, so Rust compilation was not executed here. Static audit and zip integrity checks were performed instead.
