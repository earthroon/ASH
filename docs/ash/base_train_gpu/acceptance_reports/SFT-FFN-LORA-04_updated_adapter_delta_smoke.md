# SFT-FFN-LORA-04 Acceptance

## Status

PASS_STATIC / PENDING_GPU_UPDATED_DELTA_RUNTIME

## Scope

Updated adapter delta smoke and pre/post weight-output diff seal.

## SSOT

- Source LoRA optimizer step candidate seal
- Input scope
- Pre/post LoRA A/B weight digest
- Pre/post LoRA delta digest
- Delta diff digest
- Pre/post hybrid output digest
- Hybrid output diff digest
- Diff policy
- Side effect guard
- Updated adapter delta smoke seal

## Confirmed Static Gates

- LoRA optimizer step candidate seal is required.
- Optimizer step candidate must be accepted.
- Adapter scope is required.
- Slot scope is required.
- Target module id is required.
- Input scope must match.
- Pre/post LoRA A/B digest is required.
- Weight update must be observed.
- Pre/post LoRA delta digest is required.
- Delta diff must be observed.
- Pre/post hybrid output digest is required.
- Hybrid output diff must be observed.
- Non-finite diff fails closed.
- Diff explosion fails closed.
- Artifact write fails closed.
- Runtime attach fails closed.
- Promotion apply fails closed.
- Current pointer update fails closed.
- LoRA texture update fails closed.
- Updated adapter delta smoke is allowed.
- Artifact write remains closed.
- Runtime attach remains closed.
- Promotion remains closed.
- Current pointer update remains closed.

## Opened

- updated adapter delta smoke
- pre/post LoRA delta digest
- pre/post hybrid output digest
- delta diff digest
- hybrid output diff digest
- delta diff norm recording
- hybrid output diff norm recording
- side effect guard

## Closed

- artifact write
- runtime attach
- promotion apply
- current pointer update
- LoRA texture update
- SFT training in core
- gradient write in core
- optimizer step in core

## Runtime Acceptance Pending

Requires actual GPU updated adapter delta smoke from target backend.
