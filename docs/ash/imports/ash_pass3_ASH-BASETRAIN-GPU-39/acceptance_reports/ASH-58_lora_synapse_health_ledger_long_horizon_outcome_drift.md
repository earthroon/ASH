# ASH-58 — LoRA Synapse Health Ledger / Long-Horizon Outcome Drift

## Status
PASS_LORA_SYNAPSE_HEALTH_LEDGER_LONG_HORIZON_OUTCOME_DRIFT

## Scope
- Reads ASH-53 SFT outcome synapse delta ledger.
- Reads ASH-56 native smoke artifact binding report.
- Reads ASH-57 hard negative quarantine report.
- Optionally reads previous LoRA synapse health snapshot.
- Creates deterministic LoRA synapse health ledger entry.
- Creates updated health ledger snapshot.
- Computes health score, drift score, and long-horizon outcome drift trend.
- Does not persist health ledger files.
- Does not mutate registry.
- Does not attach runtime LoRA.
- Does not commit explicit apply.
- Does not change current pointer.
- Does not release quarantine.
- Does not approve promotion candidate.

## Files
- crates/ash_core/src/lora_synapse_health_ledger.rs
- crates/ash_core/src/lib.rs
- crates/ash_core/tests/ash_58_lora_synapse_health_ledger.rs

## Seal Flags
- health_ledger_created = true
- health_entry_appended = true
- long_horizon_drift_computed = true or false depending on history
- persistent_health_ledger_write_allowed = false
- registry_mutation_allowed = false
- runtime_attach_allowed = false
- explicit_apply_commit_allowed = false
- current_pointer_changed = false
- quarantine_release_allowed = false
- promotion_candidate_approval_allowed = false

## Decision States
- Healthy / Watch / Degraded / Quarantined / Critical severity is recorded as health evidence only.
- PassThroughCandidate does not allow runtime attach.
- QuarantineCandidate does not persist quarantine or release quarantine.
- ManualReviewRequired records operator-review pressure without approving promotion.

## Reproducibility
- entry_id is deterministically derived from source ledger, dry-run plan, smoke plan, quarantine record, binding candidate, schedule, SFT run, target adapter, target artifact, and observation timestamp.
- entry_hash is deterministically derived from entry_id, event kind, severity, health score, drift score, and previous entry id.
- snapshot_id is deterministically derived from target adapter, target artifact, latest entry id, entry count, long-horizon drift score, trend, and severity.
- drift signal id is deterministically derived from target adapter, SFT run id, current/previous scores, trend, and severity.

## Result
ASH-58 creates LoRA synapse health ledger and long-horizon outcome drift evidence only. Persistent ledger write, registry mutation, runtime attachment, explicit apply commit, current pointer movement, quarantine release, and promotion approval remain sealed.
