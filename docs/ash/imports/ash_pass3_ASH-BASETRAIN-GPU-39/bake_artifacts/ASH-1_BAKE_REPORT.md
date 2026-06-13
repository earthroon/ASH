# ASH-1 Bake Report

## Status
Baked

## Scope
ASH-1 adds Rust-native Ash identity and capability schema to crates/ash_core.

## Files added
- crates/ash_core/src/identity_profile.rs
- crates/ash_core/src/capability.rs
- crates/ash_core/src/bin/ash_identity_capability_audit.rs
- crates/ash_core/tests/ash_1_identity_capability.rs
- acceptance_reports/ASH-1_identity_capability_schema.md

## Boundary
No Python validator was added.
No runtime/model_core/lora_train/artifact_store/WGPU/Burn/safetensors dependency was added to ash_core.
