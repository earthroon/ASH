# ASH-47 Bake Report

## Status
PASS_ASH_47_DPO_BRIDGE_MANIFEST

## Base SSOT
ash_pass3_ASH-46_plasticity_dataset_sanitizer_prompt_ref_resolver_baked.zip

## Added
- crates/ash_core/src/hard_negative_preference_dataset.rs
- crates/ash_core/src/dpo_bridge.rs
- crates/orchestrator_local/src/ash_47_hard_negative_preference_dataset_report.rs
- crates/orchestrator_local/src/bin/ash_47_hard_negative_preference_dataset_audit.rs
- acceptance_reports/ASH-47_hard_negative_preference_dataset_dpo_bridge.md
- workspace/event_sft/preference/* latest snapshots

## Guardrails
- Candidate only: DPO/SFT training is not executed.
- Runtime is not mutated.
- Current pointer is not changed.
- LoRA attach/detach is not executed.
- No Python validator was added.

## Rust-native verification commands
```bash
cargo test -p ash_core ash_47_hard_negative_preference_dataset
cargo test -p ash_core ash_47_dpo_bridge
cargo test -p ash_core ash_47_preference_pair_validation
cargo test -p ash_core ash_47_pair_contamination
cargo test -p orchestrator_local ash_47_hard_negative_preference_dataset_report
cargo run -p orchestrator_local --bin ash_47_hard_negative_preference_dataset_audit
```

## Local container note
The current container does not include cargo/rustc, so only static audit checks were executed here.
