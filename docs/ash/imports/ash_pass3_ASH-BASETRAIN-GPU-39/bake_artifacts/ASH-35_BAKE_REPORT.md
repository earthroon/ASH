# ASH-35 Bake Report

## SSOT
Source archive: ASH-34 baked zip.

## Added
- crates/ash_core/src/event_sft_sample_ledger.rs
- crates/ash_core/src/event_sft_sample_classifier.rs
- crates/ash_core/src/event_sft_privacy_gate.rs
- crates/orchestrator_local/src/ash_35_event_sft_sampling_report.rs
- crates/orchestrator_local/src/bin/ash_35_event_sft_sample_ledger_audit.rs
- crates/ash_core/tests/ash_35_event_sft_sample_ledger.rs
- crates/ash_core/tests/ash_35_event_sft_sample_classifier.rs
- crates/ash_core/tests/ash_35_event_sft_privacy_gate.rs
- crates/orchestrator_local/tests/ash_35_event_sft_sampling_report.rs
- acceptance_reports/ASH-35_event_to_sft_sample_ledger.md

## Modified
- crates/ash_core/src/lib.rs
- crates/orchestrator_local/src/lib.rs

## Policy Sealed
- Event samples are candidates, not JSONL datasets.
- MetadataOnly is the default privacy mode.
- Raw prompt/output is never fabricated.
- Duplicate fingerprints increment occurrence_count.
- SFT training is not executed.
- Registry/current pointer/LoRA tensor mutations are forbidden.
