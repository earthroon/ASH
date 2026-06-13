# SFT-GPU-RUN-07 Acceptance

## Status

PASS_STATIC / PENDING_PROMOTION_APPLY_CANDIDATE_RUNTIME

## Scope

GPU-trained promotion apply candidate and rollback ledger seal.

## SSOT

- Source RUN-06 runtime attach dry-run seal
- Promotion intent
- Apply plan
- Apply preflight
- Promotion apply candidate
- Rollback ledger candidate
- Rollback handle
- Rollback restore pointer
- Fallback target
- Failure recovery candidate
- TextureLoad pre-apply guard
- No mutation guard
- Promotion apply candidate seal

## Confirmed Static Gates

- RUN-06 runtime attach dry-run seal is required.
- RUN-06 attach dry-run must be accepted.
- Promotion intent is required.
- Current pointer must have remained unchanged in dry-run.
- Apply plan is required.
- Apply preflight is required.
- Apply preflight must pass.
- Promotion apply candidate is required.
- Rollback ledger candidate is required.
- Rollback handle is required.
- Rollback restore pointer is required.
- Fallback target is required.
- TextureLoad guard must remain valid.
- textureSample weight fetch is forbidden.
- Actual promotion apply is forbidden.
- Runtime current pointer update is forbidden.
- Current pointer switch is forbidden.
- Slot ready mark is forbidden.
- Lifecycle mutation is forbidden.
- ASH current binding is forbidden.

## Opened

- promotion apply candidate
- apply plan
- apply preflight
- rollback ledger candidate
- rollback handle
- rollback restore pointer
- fallback target
- failure recovery candidate
- textureLoad pre-apply guard

## Closed

- actual promotion apply
- runtime current pointer update
- current pointer switch
- slot ready mark
- lifecycle mutation
- slot action apply
- rollback execution
- ASH current binding
- runtime SFT training / gradient / optimizer

## Runtime Acceptance Pending

Requires actual promotion apply candidate and rollback ledger candidate generation from target backend.
