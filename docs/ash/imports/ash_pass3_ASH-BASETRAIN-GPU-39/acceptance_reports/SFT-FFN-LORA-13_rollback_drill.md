# SFT-FFN-LORA-13 Acceptance

## Status

PASS_STATIC / PENDING_ROLLBACK_DRILL_RUNTIME

## Scope

Current adapter rollback drill and failure recovery simulation seal.

## SSOT

- Source post-switch health seal
- Failure injection evidence
- Rollback handle resolution evidence
- Rollback simulation evidence
- Fallback candidate
- Demotion candidate
- Quarantine candidate
- TextureLoad drill guard
- No production mutation guard
- Rollback drill seal

## Confirmed Static Gates

- Post-switch health seal is required.
- Post-switch health must be accepted.
- Failure injection fixture is required.
- Failure must be detected.
- Rollback handle must resolve.
- Rollback restore pointer must be valid.
- Rollback simulation must pass.
- Production rollback execution is forbidden.
- Production current pointer touch is forbidden.
- Fallback candidate is required.
- Demotion candidate is required.
- Quarantine candidate is required.
- Demotion apply is forbidden.
- Quarantine apply is forbidden.
- TextureLoad guard must remain valid.
- textureSample weight fetch remains forbidden.
- Current pointer update remains closed.
- Promotion apply rerun remains closed.
- SFT training / gradient / optimizer remain closed.

## Opened

- rollback drill simulation
- failure injection fixture
- rollback handle resolution
- rollback simulation evidence
- fallback candidate
- demotion candidate
- quarantine candidate
- textureLoad drill guard
- no production mutation guard

## Closed

- production rollback execution
- new current pointer update
- promotion apply rerun
- demotion apply
- quarantine apply
- SFT training in core
- gradient write in core
- optimizer step in core
- textureSample weight fetch

## Runtime Acceptance Pending

Requires actual rollback drill simulation from target backend.
