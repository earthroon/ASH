# SFT-FFN-LORA-03 Acceptance

## Status

PASS_STATIC / PENDING_GPU_OPTIMIZER_STEP_RUNTIME

## Scope

LoRA optimizer step candidate and adapter weight update guard.

## SSOT

- Source LoRA gradient receipt seal
- Optimizer config
- LoRA A/B pre-update digest
- LoRA A/B post-update digest
- LoRA A/B update digest
- Update norm evidence
- Optimizer state digest before/after
- Optimizer step candidate seal

## Confirmed Static Gates

- LoRA gradient seal is required.
- Gradient receipt must be accepted.
- Adapter scope is required.
- Slot scope is required.
- Target module id is required.
- Optimizer config is required.
- Learning rate must be valid.
- Pre-weight digest is required and matched to the gradient source.
- Post-weight digest is required.
- LoRA A/B update digest is required.
- Weight update must be observed.
- Zero update fails closed.
- Non-finite update fails closed.
- Optimizer state mutation is required.
- Optimizer step index advance is required.
- Artifact write fails closed.
- Runtime attach fails closed.
- Promotion apply fails closed.
- Current pointer update fails closed.
- Optimizer step candidate is allowed.
- LoRA buffer write is allowed only for candidate update.
- LoRA texture update remains closed.
- SFT training in core remains closed.
- Gradient write in core remains closed.
- Optimizer step in core remains closed.
- Artifact write remains closed.
- Runtime attach remains closed.
- Promotion remains closed.
- Current pointer update remains closed.

## Opened

- LoRA optimizer step candidate
- LoRA buffer write for candidate update
- LoRA optimizer step candidate evidence
- LoRA weight pre/post digest
- LoRA update digest
- LoRA update norm recording
- Optimizer state mutation evidence

## Closed

- LoRA texture update
- SFT training in core
- Gradient write in core
- Optimizer step in core
- Artifact write
- Runtime attach
- Promotion apply
- Current pointer update

## Runtime Acceptance Pending

Requires actual GPU optimizer step candidate from target backend.
