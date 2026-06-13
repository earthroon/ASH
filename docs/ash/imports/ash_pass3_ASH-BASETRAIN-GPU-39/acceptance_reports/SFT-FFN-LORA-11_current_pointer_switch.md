# SFT-FFN-LORA-11 Acceptance

## Status

PASS_STATIC / PENDING_CURRENT_POINTER_SWITCH_RUNTIME

## Scope

Current pointer switch with rollback commit seal and FFN textureLoad weight fetch guard.

## SSOT

- Source promotion apply candidate seal
- Source runtime attach dry-run seal
- Source operator approval seal
- Pointer switch evidence
- Rollback commit evidence
- Failure recovery evidence
- Slot ready / ASH binding evidence
- TextureLoad weight fetch guard
- Current pointer switch seal

## Confirmed Static Gates

- Promotion apply candidate seal is required.
- Runtime attach dry-run seal is required.
- Operator approval seal is required.
- Pointer switch must be atomic.
- Current pointer before is required.
- Current pointer after is required.
- Pointer after must match approved artifact.
- Rollback commit is required.
- Rollback handle is required.
- Failure recovery path is required.
- Slot ready mark is required.
- ASH binding is required.
- FFN weight texture fetch must use textureLoad.
- textureSample is forbidden for FFN weight texture fetch.
- sampler binding is forbidden for FFN weight texture fetch.
- normalized UV weight fetch is forbidden.
- integer texel coordinate is required.
- explicit mip level zero is required.

## Opened

- current pointer switch
- promotion apply commit
- rollback commit
- failure recovery path
- slot ready mark
- approved ASH binding
- textureLoad weight fetch guard

## Closed

- unreviewed adapter attach
- textureSample weight fetch
- sampler based weight fetch
- normalized UV weight fetch
- SFT training in core
- gradient write in core
- optimizer step in core

## Runtime Acceptance Pending

Requires actual current pointer switch execution and WGSL shader guard verification in the target runtime.
