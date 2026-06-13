# ASH-18 Bake Report

## Commit
ASH-18 — Coactivation Ledger / Hebbian Path Cost Update

## Input SSOT
- ASH-17 baked tree
- ASH-17 path integral route result contract
- ASH-16 weighted LoRA synapse graph contract
- ASH-15 telemetry preservation contract

## Implemented files
- crates/ash_core/src/coactivation_ledger.rs
- crates/ash_core/src/hebbian_update.rs
- crates/orchestrator_local/src/ash_18_coactivation_ledger_report.rs
- crates/orchestrator_local/src/bin/ash_18_coactivation_ledger_audit.rs
- crates/ash_core/tests/ash_18_coactivation_ledger.rs
- crates/ash_core/tests/ash_18_hebbian_update.rs
- crates/orchestrator_local/tests/ash_18_coactivation_ledger_report.rs
- acceptance_reports/ASH-18_coactivation_ledger_hebbian_path_cost_update.md

## Modified files
- crates/ash_core/src/lib.rs
- crates/orchestrator_local/src/lib.rs

## Sealed behavior
- Coactivation events validate ASH-15 telemetry evidence.
- Pass cannot hide silent fallback or registry-not-ready state.
- Base-only events cannot contain activated adapters.
- Activated adapters and telemetry attached_lora_ids must match without silent correction.
- Stable adapter pairs update coactivation pass/fail/warning/rejected stats.
- Pair fail ratio and confidence are recomputed deterministically.
- Hebbian update generation emits proposal sets only.
- Proposal sets never auto-apply.
- All proposals require explicit apply.
- Registry mutation during proposal generation is forbidden by audit fixture.
- Ledger instability penalty can be used by ASH-17 path action in follow-up wiring.

## Validation commands
```bash
cargo test -p ash_core ash_18_coactivation_ledger
cargo test -p ash_core ash_18_hebbian_update
cargo test -p orchestrator_local ash_18_coactivation_ledger_report
cargo run -p orchestrator_local --bin ash_18_coactivation_ledger_audit
```

## Expected audit log
```txt
[ash_core][ASH-18] PASS_COACTIVATION_LEDGER_HEBBIAN_UPDATE
```

## Limitation
This environment has no cargo/rustc binary, so Rust compile/test execution was not possible here. Static file audit was performed instead.
