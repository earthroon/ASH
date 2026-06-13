# SFT-FFN-TEX-ATLAS-02 Acceptance

## Status

PASS_STATIC / PENDING_GPU_TEXTURELOAD_PARITY_RUNTIME

## Scope

TextureLoad FFN projection shader and storage buffer parity gate.

## SSOT

- Source atlas bake seal: `AshSftFfnTextureAtlasBakeReport`
- Texture atlas manifest: `AshSftFfnTextureAtlasManifest`
- Atlas SHA256
- Manifest SHA256
- Tile map digest
- Input hidden digest
- Storage baseline output digest
- Texture projection output digest
- Projection parity seal: `AshSftFfnTextureAtlasProjectionParitySeal`

## Confirmed Static Gates

- Atlas bake seal is required.
- Atlas manifest is required.
- Atlas digest must match.
- Manifest digest must match.
- Tile map digest must match.
- `textureLoad` integer coordinate fetch is required.
- `textureSample` is forbidden.
- Normalized UV is forbidden.
- Linear filtering is forbidden.
- Mipmap is forbidden.
- sRGB is forbidden.
- Alpha checksum mismatch fails closed when checksum mode is enabled.
- Projection output must match storage buffer baseline within tolerance.
- NaN/Inf output fails closed.
- Native GPU backend evidence is required.
- Shader execution is allowed only for parity.
- FFN projection execution is allowed only for parity.
- Shader execution for training remains closed.
- Shader execution for production remains closed.
- Texture projection cannot become the default path in this commit.
- SFT training remains closed.
- Gradient write remains closed.
- Optimizer step remains closed.
- LoRA texture update remains closed.
- Runtime attach remains closed.
- Promotion remains closed.
- Current pointer update remains closed.

## Opened

- TextureLoad FFN projection shader parity path.
- Storage buffer baseline comparison.
- Projection output digest recording.
- Parity diff metric recording.
- Alpha checksum validation receipt.
- Backend shader shell for parity-only numeric fetch.

## Closed

- Production texture FFN path.
- Training shader execution.
- Default projection switch.
- LoRA trainable texture update.
- SFT training in core.
- Gradient write in core.
- Optimizer step in core.
- Runtime attach.
- Promotion apply.
- Current pointer update.

## Runtime Acceptance Pending

Requires actual GPU textureLoad projection run and storage buffer baseline comparison.
