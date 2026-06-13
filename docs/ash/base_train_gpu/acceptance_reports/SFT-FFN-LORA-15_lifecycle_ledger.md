# SFT-FFN-LORA-15 Acceptance

## Status

PASS_STATIC / PENDING_LIFECYCLE_LEDGER_RUNTIME

## Scope

Adapter lifecycle ledger and promotion-demotion history seal.

## SSOT

- Source slot arbitration seal
- Lifecycle policy
- Lifecycle event table
- Lifecycle snapshot
- Lifecycle history digest
- Ledger integrity evidence
- No mutation guard
- Lifecycle ledger seal

## Confirmed Static Gates

- Slot arbitration seal is required.
- Slot arbitration must be accepted.
- Lifecycle ledger is required.
- Lifecycle event table is required.
- Lifecycle snapshot is required.
- Lifecycle history is required.
- Ledger integrity evidence is required.
- Append-only ledger is required.
- Event order must be monotonic.
- Recommendation and apply are separated.
- Demotion recommendation is allowed.
- Quarantine recommendation is allowed.
- Demotion apply is forbidden.
- Quarantine apply is forbidden.
- Current pointer update is forbidden.
- Promotion apply rerun is forbidden.
- Rollback execution is forbidden.
- SFT training / gradient / optimizer remain closed.

## Opened

- adapter lifecycle ledger
- lifecycle event table
- lifecycle snapshot
- promotion history
- health history
- rollback drill history
- arbitration history
- demotion recommendation history
- quarantine recommendation history
- ledger integrity guard

## Closed

- current pointer update
- promotion apply rerun
- rollback execution
- demotion apply
- quarantine apply
- SFT training in core
- gradient write in core
- optimizer step in core

## Runtime Acceptance Pending

Requires actual lifecycle ledger append from target backend.
