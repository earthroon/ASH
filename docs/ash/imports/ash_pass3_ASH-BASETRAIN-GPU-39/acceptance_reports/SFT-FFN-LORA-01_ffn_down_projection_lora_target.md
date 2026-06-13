# SFT-FFN-LORA-01 Acceptance

## Status

PASS_STATIC / PENDING_GPU_FFN_DOWN_LORA_TARGET_RUNTIME

## Scope

FFN down projection LoRA target module contract and GPU delta path seal.

## SSOT

- Source hybrid LoRA seal
- Source hybrid timing seal
- Adapter scope
- Target module contract
- Target module fingerprint
- LoRA shape evidence
- LoRA scale evidence
- LoRA A/B digests
- LoRA delta evidence
- FFN LoRA target seal

## Confirmed Static Gates

- Hybrid LoRA seal is required.
- Hybrid timing seal is required.
- Adapter scope is required.
- Slot scope is required.
- Dataset/checkpoint/tensor scope is required.
- Target module contract is required.
- Target module fingerprint is required.
- Only FFN down projection target is allowed.
- Gate/up projection targets remain closed.
- Target auto-remap is forbidden.
- LoRA A/B shape must match.
- Rank / alpha / scale must be valid.
- LoRA A/B digest is required.
- LoRA delta must be observed.
- Non-finite delta fails closed.
- Cross-adapter contamination fails closed.
- Cross-slot contamination fails closed.
- LoRA target candidate is allowed.
- LoRA training target remains closed.
- LoRA production target remains closed.
- LoRA target as default remains closed.
- LoRA buffer read is allowed.
- LoRA buffer write remains closed.
- LoRA optimizer step remains closed.
- LoRA texture update remains closed.
- SFT training remains closed.
- Gradient write remains closed.
- Optimizer step remains closed.
- Runtime attach remains closed.
- Promotion remains closed.
- Current pointer update remains closed.

## Opened

- FFN down projection LoRA target candidate
- Target module contract
- Target module fingerprint
- LoRA shape contract
- LoRA scale policy
- LoRA delta target evidence
- LoRA buffer read

## Closed

- FFN gate/up LoRA target
- Target auto-remap
- LoRA target for training
- LoRA target for production
- LoRA target as default
- LoRA buffer write
- LoRA optimizer step
- LoRA texture update
- SFT training in core
- Gradient write in core
- Optimizer step in core
- Runtime attach
- Promotion apply
- Current pointer update

## Runtime Acceptance Pending

Requires actual GPU FFN down projection LoRA target runtime evidence.
