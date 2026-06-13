# ASH-22 Static Audit Result

## Required symbols
- PASS: AshHardNegativeReplayCase in crates/ash_core/src/hard_negative_replay.rs
- PASS: AshHardNegativeReplayBuffer in crates/ash_core/src/hard_negative_replay.rs
- PASS: build_hard_negative_fingerprint in crates/ash_core/src/hard_negative_replay.rs
- PASS: append_hard_negative_case in crates/ash_core/src/hard_negative_replay.rs
- PASS: AshSynapseSuppressionCandidate in crates/ash_core/src/synapse_suppression.rs
- PASS: build_synapse_suppression_candidates in crates/ash_core/src/synapse_suppression.rs
- PASS: hebbian_proposals_from_suppression_candidates in crates/ash_core/src/synapse_suppression.rs
- PASS: AshPromotionBlockEvidence in crates/ash_core/src/synapse_suppression.rs
- PASS: AshRollbackTriggerEvidence in crates/ash_core/src/synapse_suppression.rs
- PASS: build_orchestrator_ash_22_hard_negative_replay_report in crates/orchestrator_local/src/ash_22_hard_negative_replay_report.rs
- PASS: ash_22_hard_negative_replay_audit in crates/orchestrator_local/src/bin/ash_22_hard_negative_replay_audit.rs

## Forbidden artifacts
- PASS: no tools/validate_ash_22_static.py
- PASS: suppression bridge does not apply proposals

## Cargo availability
- cargo unavailable in this container; Rust tests not executed here
