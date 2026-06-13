# 16AI-QW-38G-R6A-ASH-BURN-06 Bake Report

## Contract
Burn Backend Apply Sandbox Execution / No Production Commit Seal

## Baked files
- crates/ash_core/src/ash_burn_06_backend_apply_sandbox_execution.rs
- crates/ash_core/src/bin/ash_burn_06_backend_apply_sandbox_execution.rs
- crates/ash_core/src/lib.rs
- acceptance_reports/16AI-QW-38G-R6A-ASH-BURN-06.md
- patch_reports/16AI-QW-38G-R6A-ASH-BURN-06_bake_report.md
- ASH_BURN_06_STATIC_CHECKS.txt
- ASH_BURN_06_BAKE_MANIFEST.json

## Static-only note
Cargo/rustc were not available in the bake container, so this bake is sealed as BAKED_STATIC_NO_CARGO.

## Key guard
Backend apply sandbox execution is allowed. Production commit, production default change, active backend pointer mutation, backend shadow commit, rollback ledger mutation, runtime output, and final response emission are blocked.
