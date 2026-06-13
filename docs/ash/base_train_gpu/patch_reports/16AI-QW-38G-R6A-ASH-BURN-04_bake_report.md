# 16AI-QW-38G-R6A-ASH-BURN-04 Bake Report

## Contract
Burn Same Device Raw Bridge Strict Probe / No Backend Default Promotion Seal

## Baked files
- crates/ash_core/src/ash_burn_04_same_device_raw_bridge_strict_probe.rs
- crates/ash_core/src/bin/ash_burn_04_same_device_raw_bridge_strict_probe.rs
- crates/ash_core/src/lib.rs
- acceptance_reports/16AI-QW-38G-R6A-ASH-BURN-04.md
- patch_reports/16AI-QW-38G-R6A-ASH-BURN-04_bake_report.md
- ASH_BURN_04_STATIC_CHECKS.txt
- ASH_BURN_04_BAKE_MANIFEST.json

## Static-only note
Cargo/rustc were not available in the bake container, so this bake is sealed as BAKED_STATIC_NO_CARGO.

## Key guard
Strict probe evidence is allowed. Backend default promotion, active pointer mutation, forward execution, tensor write, runtime mutation, and production output are blocked.
