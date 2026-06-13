# SFT-FFN-TEX-ATLAS-06 Acceptance

## Status

PASS_STATIC / PENDING_GPU_HYBRID_LORA_RUNTIME

## Scope

Hybrid base texture FFN path plus storage-buffer LoRA delta path.

## SSOT

- Source atlas bake seal
- Source projection parity seal
- Source batched dispatch seal
- Source atomic compaction seal
- Source timing probe seal
- Adapter scope
- LoRA A/B buffer digests
- LoRA scale policy
- Base output digest
- LoRA delta digest
- Hybrid output digest
- Hybrid LoRA seal

## Confirmed Static Gates

- Timing probe seal is required.
- Adapter scope is required.
- Slot scope is required.
- Dataset/checkpoint/tensor scope is required.
- Target module id is required.
- LoRA A/B buffer digest is required.
- LoRA shape must match target projection.
- LoRA scale policy is required.
- Delta must be observed.
- Hybrid output must change from base output.
- Non-finite delta fails closed.
- Non-finite hybrid output fails closed.
- Cross-adapter contamination fails closed.
- Cross-slot contamination fails closed.
- Hybrid LoRA delta path is allowed only for smoke.
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

- hybrid base texture + LoRA buffer delta smoke path
- LoRA buffer read
- LoRA delta digest recording
- hybrid output digest recording
- delta norm recording

## Closed

- hybrid path for training
- hybrid path for production
- hybrid path as default
- LoRA buffer write
- LoRA optimizer step
- LoRA texture update
- SFT training in core
- gradient write in core
- optimizer step in core
- runtime attach
- promotion apply
- current pointer update

## Runtime Acceptance Pending

Requires actual GPU hybrid base texture + LoRA buffer delta run.
