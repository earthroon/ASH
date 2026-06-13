# SFT-FFN-TEX-ATLAS-03 Acceptance

## Status

PASS_STATIC / PENDING_GPU_BATCHED_TEXTURE_FFN_RUNTIME

## Scope

Batched token texture FFN dispatch and adapter-scoped atlas group parallel seal.

## SSOT

- Source atlas bake seal
- Source projection parity seal
- Adapter-scoped token group
- Input hidden group digest
- Dispatch shape digest
- Output group digest
- Batched dispatch seal

## Confirmed Static Gates

- Atlas bake seal is required.
- Projection parity seal is required.
- Projection parity must be accepted.
- Adapter scope is required.
- Slot scope is required.
- Dataset/checkpoint/tensor scope is required.
- Token group must be non-empty.
- Token group max size is enforced.
- Cross-adapter contamination fails closed.
- Cross-slot contamination fails closed.
- textureLoad is required.
- textureSample is forbidden.
- Integer coordinates are required.
- Normalized UV, linear filtering, mipmap, and sRGB remain forbidden.
- Scratch budget evidence is required.
- Scratch budget overflow fails closed.
- Output digest is required.
- Non-finite output fails closed.
- Batched dispatch is allowed only for smoke.
- Batched dispatch for training remains closed.
- Batched dispatch for production remains closed.
- Batched dispatch as default remains closed.
- SFT training remains closed.
- Gradient write remains closed.
- Optimizer step remains closed.
- LoRA texture update remains closed.
- Runtime attach remains closed.
- Promotion remains closed.
- Current pointer update remains closed.

## Opened

- batched texture FFN dispatch smoke path
- adapter-scoped token group seal
- input/output group digest recording
- dispatch shape digest recording
- scratch budget evidence recording

## Closed

- training batched dispatch
- production batched dispatch
- default texture FFN projection path
- SFT training in core
- gradient write in core
- optimizer step in core
- LoRA texture update
- runtime attach
- promotion apply
- current pointer update

## Runtime Acceptance Pending

Requires actual GPU batched texture FFN dispatch run.
