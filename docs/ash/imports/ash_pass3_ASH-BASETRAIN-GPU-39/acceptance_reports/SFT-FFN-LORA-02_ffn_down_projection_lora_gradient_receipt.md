# SFT-FFN-LORA-02 Acceptance

## Status

PASS_STATIC / PENDING_GPU_BACKWARD_GRADIENT_RUNTIME

## Scope

FFN down projection LoRA backward gradient receipt without optimizer step.

## SSOT

- Source FFN down projection LoRA target seal
- Loss source evidence
- Backward pass evidence
- Gradient shape contract
- LoRA A gradient digest
- LoRA B gradient digest
- Gradient norm evidence
- Weight mutation guard
- Gradient receipt seal

## Confirmed Static Gates

- FFN down projection LoRA target seal is required.
- Target must be accepted.
- Adapter scope is required.
- Slot scope is required.
- Loss source digest is required.
- Loss must be finite.
- Backward pass id is required.
- Backward must be GPU-native.
- LoRA A/B gradient digest is required.
- Gradient shape must match LoRA A/B shape.
- Gradient must be observed.
- Zero gradient fails closed.
- Non-finite gradient fails closed.
- LoRA weight mutation fails closed.
- Optimizer step fails closed.
- Optimizer state mutation fails closed.
- Artifact write fails closed.
- Cross-adapter contamination fails closed.
- Cross-slot contamination fails closed.
- Backward gradient receipt is allowed.
- Gradient accumulation remains closed.
- LoRA buffer read is allowed.
- LoRA buffer write remains closed.
- LoRA optimizer step remains closed.
- LoRA texture update remains closed.
- SFT training in core remains closed.
- Gradient write in core remains closed.
- Optimizer step in core remains closed.
- Artifact write remains closed.
- Runtime attach remains closed.
- Promotion remains closed.
- Current pointer update remains closed.

## Opened

- FFN down projection LoRA backward gradient receipt
- loss source evidence
- backward pass evidence
- LoRA A gradient digest
- LoRA B gradient digest
- gradient norm recording
- weight mutation guard

## Closed

- gradient accumulation receipt
- LoRA buffer write
- LoRA optimizer step
- LoRA texture update
- SFT training in core
- gradient write in core
- optimizer step in core
- artifact write
- runtime attach
- promotion apply
- current pointer update

## Runtime Acceptance Pending

Requires actual GPU backward gradient receipt from target backend.
