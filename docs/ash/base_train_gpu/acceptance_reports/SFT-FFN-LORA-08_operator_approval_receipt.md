# SFT-FFN-LORA-08 Acceptance

## Status

PASS_STATIC / PENDING_OPERATOR_APPROVAL_RUNTIME

## Scope

Operator approval receipt and promotion intent seal.

## SSOT

- Source promotion review seal
- Approval source evidence
- Operator identity evidence
- Approval receipt evidence
- Approval count evidence
- Digest match evidence
- Promotion intent evidence
- No runtime mutation guard
- Operator approval seal

## Confirmed Static Gates

- Promotion review seal is required.
- Promotion review must be accepted.
- Operator identity digest is required.
- Operator signature digest is required.
- Operator authorization is required.
- Self approval fails closed.
- Auto approval fails closed.
- Duplicate approval fails closed.
- Approval count must be satisfied.
- Review packet digest must match.
- Artifact digests must match.
- Eval digests must match.
- Promotion intent digest is required.
- Runtime attach fails closed.
- Promotion apply fails closed.
- Current pointer update fails closed.
- Slot ready mark fails closed.
- ASH binding fails closed.
- Operator approval recording is allowed.
- Promotion intent recording is allowed.
- Runtime attach remains closed.
- Promotion apply remains closed.
- Current pointer update remains closed.

## Opened

- operator approval record
- promotion intent record
- operator identity digest
- operator signature digest
- approval receipt digest
- approval count evidence
- review packet digest match
- artifact digest match
- eval digest match
- no runtime mutation guard

## Closed

- runtime attach
- promotion apply
- current pointer update
- slot ready mark
- ASH binding
- SFT training in core
- gradient write in core
- optimizer step in core

## Runtime Acceptance Pending

Requires actual operator approval receipt from target approval backend.
