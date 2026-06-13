# SFT-FFN-LORA-07 Acceptance

## Status

PASS_STATIC / PENDING_PROMOTION_REVIEW_RUNTIME

## Scope

Adapter promotion review candidate and operator approval gate.

## SSOT

- Source adapter eval candidate seal
- Source artifact candidate seal
- Promotion review source evidence
- Review packet digest
- Approval policy
- Approval gate evidence
- Review queue evidence
- No runtime promotion guard
- Promotion review candidate seal

## Confirmed Static Gates

- Eval candidate seal is required.
- Eval candidate must be accepted.
- Artifact candidate seal is required.
- Artifact digest is required.
- Review packet is required.
- Review packet digest is required.
- Approval policy is required.
- Approval gate is required.
- Operator approval must be required.
- Auto approval fails closed.
- Existing operator approval fails closed.
- Review queue evidence is required.
- Review queue write is required.
- Runtime attach fails closed.
- Promotion apply fails closed.
- Current pointer update fails closed.
- Slot ready mark fails closed.
- ASH binding fails closed.
- Promotion review candidate is allowed.
- Review queue enqueue is allowed.
- Operator approval recording remains closed.
- Runtime attach remains closed.
- Promotion apply remains closed.
- Current pointer update remains closed.

## Opened

- promotion review candidate
- review queue enqueue
- review packet digest
- approval gate creation
- operator approval required state
- no runtime promotion guard

## Closed

- operator approval record
- runtime attach
- promotion apply
- current pointer update
- slot ready mark
- ASH binding
- SFT training in core
- gradient write in core
- optimizer step in core

## Runtime Acceptance Pending

Requires actual promotion review queue write from target review backend.
