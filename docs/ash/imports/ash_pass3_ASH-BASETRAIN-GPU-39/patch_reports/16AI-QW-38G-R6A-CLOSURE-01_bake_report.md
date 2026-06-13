# 16AI-QW-38G-R6A-CLOSURE-01 Bake Report

## Result

status: PASS_STATIC_RUST_MODULE_SURFACE_RECONCILIATION_CONTRACT
domain_ssot: en_to_ko_translation_subtitle_machine
base: ash_pass3_16AI-QW-38G-R6A-CLOSURE-00_decode_chain_freeze_receipt_manifest_seal_baked.zip
output: ash_pass3_16AI-QW-38G-R6A-CLOSURE-01_rust_module_surface_reconciliation_compile_contract_candidate_seal_baked.zip

## Summary

- Added Rust module surface reconciliation modules.
- Updated `crates/ash_core/src/lib.rs` with CLOSURE-01 module declarations and closure export surface.
- Created source module inventory, lib.rs export surface snapshot, module export gap index, type surface collision index, compile contract candidate, and reconciliation receipt.
- Did not run cargo check, rustc, runtime decode, model forward, sampling, or subtitle export.

## Counts

source_module_count: 108
expected_export_count: 108
actual_export_detected_count: 108
missing_mod_declaration_count: 0
missing_pub_use_count: 0
export_gap_count: 0
blocking_gap_count: 0
type_collision_count: 4
compile_blocking_collision_count: 0
ready_for_cargo_check: true

deterministic_receipt_key: q4sha256:0d1685785d4221f27045de27f5d33f55ad0cea5e47febd2f306dc370ffc1e7ca
