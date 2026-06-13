# SFT-FFN-LORA-12 Acceptance

## Status

PASS_STATIC / PENDING_POST_SWITCH_RUNTIME_SMOKE

## Scope

Runtime current adapter smoke and post-switch health seal.

## SSOT

- Source current pointer switch seal
- Runtime current adapter evidence
- Post-switch smoke evidence
- Health ledger evidence
- Fallback guard
- Rollback availability evidence
- TextureLoad regression guard
- No mutation guard
- Post-switch health seal

## Confirmed Static Gates

- Current pointer switch seal is required.
- Current pointer switch must be accepted.
- Runtime current pointer must match expected pointer.
- Runtime current adapter digest must match expected adapter.
- Stale runtime cache fails closed.
- Post-switch output digest is required.
- Non-finite post-switch output fails closed.
- Collapsed post-switch output fails closed.
- Health ledger write is required.
- Health score below threshold fails closed.
- Fallback guard is required.
- Rollback availability is required.
- Rollback execution is forbidden in this commit.
- TextureLoad guard must remain valid.
- textureSample weight fetch remains forbidden.
- Unexpected current pointer update fails closed.
- Unexpected promotion apply fails closed.
- SFT training / gradient / optimizer remain closed.

## Opened

- runtime current adapter smoke
- post-switch smoke evidence
- post-switch health ledger
- fallback guard
- rollback availability check
- textureLoad regression guard
- post-switch no-mutation guard

## Closed

- new current pointer update
- promotion apply rerun
- rollback execution
- unreviewed adapter attach
- textureSample weight fetch
- SFT training in core
- gradient write in core
- optimizer step in core

## Runtime Acceptance Pending

Requires actual post-switch runtime smoke from target backend.
