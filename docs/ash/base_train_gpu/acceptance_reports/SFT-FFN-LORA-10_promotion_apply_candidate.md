# SFT-FFN-LORA-10 Acceptance

## Status

PASS_STATIC / PENDING_PROMOTION_APPLY_CANDIDATE_RUNTIME

## Scope

Guarded promotion apply candidate with rollback ledger and no current pointer switch.

## SSOT

- Source runtime attach dry-run seal
- Source operator approval seal
- Source artifact candidate seal
- Promotion apply source evidence
- Artifact apply evidence
- Apply policy
- Apply preflight evidence
- Rollback ledger candidate
- Failure demotion path
- Current pointer guard
- Promotion apply candidate seal

## Confirmed Static Gates

- Runtime attach dry-run seal is required.
- Runtime attach dry-run must be accepted.
- Operator approval seal is required.
- Promotion intent is required.
- Artifact digests must match.
- Apply policy is required.
- Apply preflight is required.
- Rollback ledger candidate is required.
- Rollback handle is required.
- Rollback restore target is required.
- Failure demotion path is required.
- Current pointer must remain unchanged.
- Promotion apply commit fails closed.
- Current pointer update fails closed.
- Slot ready mark fails closed.
- ASH binding fails closed.
- Promotion apply candidate is allowed.
- Apply preflight is allowed.
- Rollback ledger candidate write is allowed.
- Failure demotion path is allowed.

## Opened

- guarded promotion apply candidate
- apply preflight evidence
- rollback ledger candidate
- rollback handle digest
- rollback restore target
- failure demotion path
- current pointer switch readiness
- current pointer unchanged guard
- backend promotion-apply candidate boundary shell

## Closed

- promotion apply commit
- current pointer update
- slot ready mark
- ASH binding
- SFT training in core
- gradient write in core
- optimizer step in core

## Runtime Acceptance Pending

Requires actual promotion apply candidate / rollback ledger write from target promotion backend.
