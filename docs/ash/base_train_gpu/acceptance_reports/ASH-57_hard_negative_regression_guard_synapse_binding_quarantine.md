# ASH-57 — Hard Negative Regression Guard / Synapse Binding Quarantine

## Status
PASS_HARD_NEGATIVE_REGRESSION_GUARD_SYNAPSE_BINDING_QUARANTINE

## Scope
- Reads ASH-53 SFT outcome synapse delta ledger.
- Reads ASH-54 registry mutation dry-run report.
- Reads ASH-56 native smoke artifact binding report.
- Optionally reads externally provided native smoke evidence.
- Builds hard negative regression signals.
- Builds deterministic synapse binding quarantine/pass-through/manual-review record.
- Does not mutate registry.
- Does not attach runtime LoRA.
- Does not commit explicit apply.
- Does not change current pointer.
- Does not delete or rewrite artifacts.
- Does not persist quarantine state.
- Does not release quarantine.

## Files
- `crates/ash_core/src/hard_negative_synapse_binding_quarantine.rs`
- `crates/ash_core/src/lib.rs`
- `crates/ash_core/tests/ash_57_hard_negative_synapse_binding_quarantine.rs`

## Seal Flags
- `quarantine_guard_created = true`
- `quarantine_candidate_created = true or false depending on decision`
- `pass_through_candidate_created = true or false depending on decision`
- `manual_review_required = true or false depending on decision`
- `quarantine_persistent_write_allowed = false`
- `registry_mutation_allowed = false`
- `runtime_attach_allowed = false`
- `explicit_apply_commit_allowed = false`
- `current_pointer_changed = false`
- `artifact_delete_allowed = false`
- `artifact_rewrite_allowed = false`
- `quarantine_release_allowed = false`

## Decision Policy
- Hard negative risk over threshold creates `QuarantineCandidate`.
- Dry-run rejected records create `QuarantineCandidate`.
- Failed provided smoke evidence creates `QuarantineCandidate`.
- Low delta confidence creates `ManualReviewRequired` unless paired with stronger quarantine reasons.
- Missing provided smoke evidence with a valid ASH-56 plan creates `ManualReviewRequired`, not immediate quarantine.
- Prior seal violation from ASH-53/ASH-54/ASH-56 rejects the report.

## Reproducibility
- `signal_id` is deterministically derived from:
  - ASH-53 `entry_id`
  - affected path/edge
  - target adapter
  - hard negative risk
  - delta confidence
  - risk-adjusted delta score

- `record_id` is deterministically derived from:
  - quarantine request id
  - ASH-53 ledger id
  - ASH-54 dry-run plan id
  - ASH-56 smoke plan id
  - decision
  - reasons
  - signal ids

## Result
ASH-57 creates hard negative regression quarantine evidence only. Registry mutation, runtime attachment, explicit apply commit, current pointer movement, artifact rewrite/delete, persistent quarantine write, and quarantine release remain sealed.
