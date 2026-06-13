# ASH-8 bake report

## Status
REBaked / PASS_STATIC_SANITY

## Source SSOT
- ash_pass3_ASH-7_eval_arbitration_promotion_brain_baked.zip

## Added
- crates/ash_core/src/public_api.rs
- crates/ash_core/src/cli_bridge.rs
- crates/ash_core/src/bin/ash_api.rs
- crates/ash_core/src/bin/ash_public_api_audit.rs
- crates/ash_core/tests/ash_8_public_api_cli.rs
- acceptance_reports/ASH-8_public_api_cli_bridge.md

## Modified
- crates/ash_core/src/lib.rs
- crates/ash_core/Cargo.toml
- crates/ash_core/src/ssot.rs
- crates/ash_core/src/crate_audit.rs
- crates/ash_core/tests/ash_0_boundary.rs
- crates/ash_core/src/runtime_router.rs

## Re-bake correction
- Removed duplicate `intent` field from the BaseOnly branch in runtime_router.rs.
- Added serde_json as an allowed Rust dependency for JSON CLI/API I/O.
- Updated ASH-0 dependency boundary records to include serde_json.

## Validation commands
```powershell
cargo test -p ash_core ash_8_public_api_cli
cargo run -p ash_core --bin ash_public_api_audit
cargo run -p ash_core --bin ash_api -- audit-all
```

## Python
No ASH-8 Python validator was added.
