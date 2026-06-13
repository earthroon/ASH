# ASH-BASETRAIN-GPU-37H Bake Report

## Summary

Added progressive shader module compile candidate for the 37G verified dispatch candidate.

## Boundary

Allowed:

- 37G receipt read
- WGSL source generation
- GPU adapter/device request
- shader module creation

Denied:

- source shard read
- F32 decode
- GPU buffer creation
- queue upload
- readback
- compute pipeline
- bind group
- dispatch
- forward/backward/optimizer/mutation

## Static Result

Static artifact is sealed as `BLOCKED_37G_RECEIPT_NOT_FOUND` until a live 37G PASS receipt is provided locally.
