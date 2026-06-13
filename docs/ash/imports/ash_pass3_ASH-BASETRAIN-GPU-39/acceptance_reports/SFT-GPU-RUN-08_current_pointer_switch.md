# SFT-GPU-RUN-08 Acceptance

## Status

PASS_STATIC / PENDING_CURRENT_POINTER_SWITCH_RUNTIME

## Scope

GPU-trained current pointer switch and TextureLoad revalidation seal.

## SSOT

- Source RUN-07 promotion apply candidate seal
- Promotion apply commit
- Current pointer before/after evidence
- Rollback ledger commit
- Slot ready mark
- TextureLoad revalidation
- No forbidden mutation guard
- Current pointer switch seal

## Confirmed Static Gates

- RUN-07 promotion apply candidate seal is required.
- RUN-07 promotion apply candidate must be accepted.
- Apply preflight must have passed.
- Rollback ledger candidate is required.
- Rollback handle is required.
- Rollback restore pointer is required.
- Promotion apply commit is required.
- Current pointer switch is required.
- Current pointer after must match planned current pointer.
- Rollback ledger commit is required.
- Rollback execution is forbidden.
- Slot ready mark is required.
- TextureLoad revalidation is required.
- textureSample weight fetch is forbidden.
- Lifecycle mutation is forbidden.
- Slot action apply is forbidden.
- ASH current binding is forbidden.
- Runtime SFT training / gradient / optimizer are forbidden.

## Opened

- reviewed promotion apply commit
- runtime current pointer update
- current pointer switch
- slot ready mark
- rollback ledger commit
- textureLoad revalidation
- post-switch health handoff candidate

## Closed

- unreviewed promotion apply
- rollback execution
- lifecycle mutation
- slot action apply
- ASH current binding
- runtime SFT training
- runtime gradient write
- runtime optimizer step

## Runtime Acceptance Pending

Requires actual guarded current pointer switch from target backend.
