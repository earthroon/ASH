# SFT-FFN-TEX-ATLAS-01 Acceptance

## Status

PASS_STATIC / PENDING_TEXTURE_RUNTIME_BAKE

## Scope

Frozen FFN weight texture atlas bake manifest and numeric fetch policy seal.

## SSOT

- checkpoint fingerprint
- tensor index hash
- source FFN tensor digests
- texture atlas manifest
- atlas sha256
- manifest sha256
- tile map digest

## Confirmed Static Gates

- FFN source tensors are required.
- Gate / Up / Down projection entries are explicit.
- Texture format policy is required.
- Packing policy is required.
- Numeric fetch policy is required.
- `textureLoad` is required.
- `textureSample` is forbidden.
- Integer coordinates are required.
- Normalized UV sampling is forbidden.
- Linear filtering is forbidden.
- Mipmap is forbidden.
- sRGB format is forbidden.
- Tile bounds are checked.
- Tile overlap fails closed.
- Shader execution remains closed.
- FFN projection execution remains closed.
- SFT training execution remains closed.
- Gradient write remains closed.
- Optimizer step remains closed.
- LoRA weight texture update remains closed.
- Runtime attach remains closed.
- Promotion remains closed.
- Current pointer update remains closed.

## Opened

- frozen FFN texture atlas bake manifest
- gate/up/down tile map
- atlas digest recording
- manifest digest recording
- numeric fetch policy seal
- RGB payload + alpha checksum mode for guarded probe/seal paths

## Closed

- shader execution
- FFN projection execution
- LoRA trainable texture update
- SFT training in core
- gradient write in core
- optimizer step in core
- runtime attach
- promotion apply
- current pointer update

## Runtime Acceptance Pending

Actual GPU texture creation and textureLoad parity are deferred to SFT-FFN-TEX-ATLAS-02.
