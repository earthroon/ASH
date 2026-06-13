# ASH-59 — Operator-Reviewed Synapse Promotion Candidate

## Status
PASS_OPERATOR_REVIEWED_SYNAPSE_PROMOTION_CANDIDATE

## Scope
- Reads ASH-58 LoRA synapse health ledger report.
- Reads ASH-57 hard negative quarantine report.
- Reads ASH-56 native smoke artifact binding report.
- Reads explicit operator review input.
- Creates operator-reviewed synapse promotion candidate evidence.
- Creates ready-for-runtime-apply-candidate-gate evidence.
- Does not mutate registry.
- Does not attach runtime LoRA.
- Does not commit explicit apply.
- Does not change current pointer.
- Does not release quarantine.
- Does not apply promotion.
- Does not create apply receipt.

## Files
- `crates/ash_core/src/operator_reviewed_synapse_promotion_candidate.rs`
- `crates/ash_core/src/lib.rs`
- `crates/ash_core/tests/ash_59_operator_reviewed_synapse_promotion_candidate.rs`

## Seal Flags
- `operator_reviewed = true`
- `promotion_candidate_created = decision-dependent`
- `ready_for_runtime_apply_candidate_gate = decision-dependent`
- `registry_mutation_allowed = false`
- `runtime_attach_allowed = false`
- `explicit_apply_commit_allowed = false`
- `current_pointer_changed = false`
- `quarantine_release_allowed = false`
- `promotion_apply_allowed = false`
- `apply_receipt_allowed = false`

## Deterministic IDs
`promotion_candidate_id` is deterministically derived from:
- promotion review request id
- ASH-58 health snapshot id
- ASH-58 health entry id
- ASH-57 quarantine record id
- ASH-53 ledger id
- ASH-56 smoke plan id
- binding candidate id
- schedule id
- SFT run id
- target adapter id
- target artifact id
- operator id
- operator decision
- reviewed timestamp

## Review Decisions
- `PromoteCandidate` creates a promotion candidate only when health, drift, smoke, and quarantine gates are satisfied.
- `HoldForObservation` creates no candidate and remains a pass-state hold.
- `RequireMoreSmokeEvidence` creates no candidate and routes back to smoke evidence collection.
- `KeepQuarantined` creates no candidate and does not release quarantine.
- `RejectCandidate` creates no candidate and does not delete artifacts or mutate registries.

## Result
ASH-59 creates operator-reviewed synapse promotion candidate evidence only. Registry mutation, runtime attachment, explicit apply commit, current pointer movement, quarantine release, promotion apply, and apply receipt creation remain sealed.
