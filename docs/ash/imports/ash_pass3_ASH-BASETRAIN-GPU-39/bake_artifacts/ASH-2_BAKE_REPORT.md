# ASH-2 Bake Report

## Commit
ASH-2 — Adapter Synapse Registry seal

## Base
ASH-1 identity/capability schema bake

## Files changed
- crates/ash_core/src/adapter_synapse.rs
- crates/ash_core/src/bin/ash_adapter_synapse_audit.rs
- crates/ash_core/tests/ash_2_adapter_synapse.rs
- crates/ash_core/src/lib.rs
- acceptance_reports/ASH-2_adapter_synapse_registry.md

## Python policy
No Python validator was added.
ASH-2 validation is Rust-native through ash_core tests and audit bin.

## Expected commands
```powershell
cargo test -p ash_core ash_2_adapter_synapse
cargo run -p ash_core --bin ash_adapter_synapse_audit
```

Fallback when running outside workspace root:

```powershell
cargo test --manifest-path crates/ash_core/Cargo.toml ash_2_adapter_synapse
cargo run --manifest-path crates/ash_core/Cargo.toml --bin ash_adapter_synapse_audit
```

## Expected log
```txt
[ash_core][ASH-2] PASS_ASH_ADAPTER_SYNAPSE_REGISTRY
```
