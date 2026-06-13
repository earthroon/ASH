# 16AI-QW-38G-R6A-ASH-BURN-05 Bake Report

## Contract
Burn Backend Route Promotion Candidate / No Production Default Change Seal

## Baked files
- crates/ash_core/src/ash_burn_05_backend_route_promotion_candidate.rs
- crates/ash_core/src/bin/ash_burn_05_backend_route_promotion_candidate.rs
- crates/ash_core/src/lib.rs
- acceptance_reports/16AI-QW-38G-R6A-ASH-BURN-05.md
- patch_reports/16AI-QW-38G-R6A-ASH-BURN-05_bake_report.md
- ASH_BURN_05_STATIC_CHECKS.txt
- ASH_BURN_05_BAKE_MANIFEST.json

## Static-only note
Cargo/rustc were not available in the bake container, so this bake is sealed as BAKED_STATIC_NO_CARGO.

## Key guard
Backend route candidate creation is allowed. Production default change, active backend pointer mutation, backend apply sandbox execution, backend shadow commit, forward execution, tensor write, runtime mutation, and output emission are blocked.
