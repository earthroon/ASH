# ASH-0 Bake Report

## Status
BAKED_STATIC_RUST_NATIVE

## Applied files
- crates/ash_core/src/ssot.rs
- crates/ash_core/src/role_boundary.rs
- crates/ash_core/src/crate_audit.rs
- crates/ash_core/src/bin/ash_core_audit.rs
- crates/ash_core/tests/ash_0_boundary.rs
- crates/ash_core/src/lib.rs
- acceptance_reports/ASH-0_crate_role_audit.md
- bake_artifacts/ASH-0_BAKE_REPORT.md

## SSOT correction
ASH-0 does not add a Python validator. Boundary validation is owned by Rust-native `ash_core` tests and the `ash_core_audit` bin.

## Intended commands
```powershell
cargo test -p ash_core ash_0_boundary
cargo run -p ash_core --bin ash_core_audit
```

If the repository is not arranged as a Cargo workspace, use:

```powershell
cargo test --manifest-path crates/ash_core/Cargo.toml ash_0_boundary
cargo run --manifest-path crates/ash_core/Cargo.toml --bin ash_core_audit
```

## Expected audit log
```txt
[ash_core][ASH-0] PASS_ASH_CORE_ROLE_AUDIT
```
