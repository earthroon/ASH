# SFT-FFN-LORA-09 Acceptance

## Status

PASS_STATIC / PENDING_RUNTIME_ATTACH_DRY_RUN

## Scope

Approved adapter runtime attach dry-run with current pointer guard.

## SSOT

- Source operator approval seal
- Approval source evidence
- Artifact digest evidence
- Dry-run runtime evidence
- Adapter load sanity evidence
- Dry-run output evidence
- Rollback requirement evidence
- Current pointer guard
- Runtime attach dry-run seal

## Confirmed Static Gates

- Operator approval seal is required.
- Operator approval must be accepted.
- Promotion intent is required.
- Artifact digests must match.
- Dry-run runtime is required.
- Dry-run runtime must be isolated from production runtime.
- Adapter load sanity is required.
- Target module must match.
- Adapter shape must match.
- Adapter scale must match.
- Dry-run output digest is required.
- Non-finite dry-run output fails closed.
- Collapsed dry-run output fails closed.
- Rollback requirement is required.
- Current pointer must remain unchanged.
- Production runtime attach fails closed.
- Promotion apply fails closed.
- Current pointer update fails closed.
- Slot ready mark fails closed.
- ASH binding fails closed.
- Runtime attach dry-run is allowed.
- Artifact read for dry-run is allowed.

## Opened

- approved adapter runtime attach dry-run
- artifact read for dry-run
- dry-run runtime sandbox
- adapter load sanity evidence
- dry-run output sanity evidence
- rollback requirement evidence
- current pointer unchanged guard

## Closed

- production runtime attach
- promotion apply
- current pointer update
- slot ready mark
- ASH binding
- SFT training in core
- gradient write in core
- optimizer step in core

## Runtime Acceptance Pending

Requires actual runtime attach dry-run from target backend.
