# ASH-3 Bake Report

## Commit
ASH-3 — Runtime Attachment Plan contract

## Base
ASH-2 Adapter Synapse Registry baked tree

## Added
- `crates/ash_core/src/runtime_attachment_plan.rs`
- `crates/ash_core/src/bin/ash_runtime_attachment_plan_audit.rs`
- `crates/ash_core/tests/ash_3_runtime_attachment_plan.rs`
- `acceptance_reports/ASH-3_runtime_attachment_plan.md`

## Rust-native validation
- `cargo test -p ash_core ash_3_runtime_attachment_plan`
- `cargo run -p ash_core --bin ash_runtime_attachment_plan_audit`

## Python policy
No Python validator was added for ASH-3.

## Boundary
`ash_core` remains a domain decision crate. It emits runtime attachment plan metadata only and does not execute runtime forward, parse safetensors, copy adapter artifacts, or invoke GPU training kernels.
