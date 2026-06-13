# SFT-FFN-TEX-ATLAS-04 Acceptance

## Status

PASS_STATIC / PENDING_DEVICE_LIMIT_RUNTIME_PROFILE

## Scope

Texture atlas scratch budget guard and device limit preflight.

## SSOT

- Source atlas bake seal
- Source projection parity seal
- Source batched dispatch seal
- Device limit profile
- Scratch estimate
- Atlas dimension check
- Storage binding check
- Dispatch limit check
- Safe token group candidate
- Budget guard seal

## Confirmed Static Gates

- Atlas bake seal is required.
- Projection parity seal is required.
- Batched dispatch seal is required.
- Device limit profile is required.
- Atlas dimension check is required.
- Storage binding check is required.
- Dispatch limit check is required.
- Scratch estimate is required.
- Safe token group candidate is required.
- Atlas dimension overflow fails closed.
- Storage binding overflow fails closed.
- Max buffer overflow fails closed.
- Workgroup size overflow fails closed.
- Dispatch dimension overflow fails closed.
- Scratch budget overflow fails closed.
- Silent group shrink fails closed.
- Budget preflight is allowed.
- Group size candidate selection is allowed.
- Batched dispatch execution remains closed.
- Shader execution for training remains closed.
- Shader execution for production remains closed.
- Batched dispatch as default remains closed.
- SFT training remains closed.
- Gradient write remains closed.
- Optimizer step remains closed.
- LoRA texture update remains closed.
- Runtime attach remains closed.
- Promotion remains closed.
- Current pointer update remains closed.

## Opened

- device limit profile receipt
- scratch budget estimate
- atlas dimension preflight
- storage binding limit preflight
- dispatch limit preflight
- safe token group candidate selection
- explicit group shrink receipt

## Closed

- batched dispatch execution
- training shader execution
- production shader execution
- default texture FFN path
- SFT training in core
- gradient write in core
- optimizer step in core
- LoRA texture update
- runtime attach
- promotion apply
- current pointer update

## Runtime Acceptance Pending

Requires actual device limit profile collected from target WGPU backend.
