# SFT-GPU-PERF-10 — Vocab Tile Tail Shape Compile Cache / Pass2 Dispatch Latency Seal

## Scope

This seal consumes the PERF-09 batch × vocab tile 2D dispatch grid and canonicalizes vocab tail tile shape for pass1/pass2 GPU kernels. It creates deterministic kernel pipeline cache keys, verifies tail tile padding, pass1/pass2 tail shape compatibility, compile cache reuse, pass2 dispatch latency thresholds, and rejects dynamic tail shape compile, tail CPU fallback, tail serial dispatch, full logits buffers, and logits readback.

## Required Evidence

- PERF-09 2D dispatch grid plan id/fingerprint
- PERF-09 2D dispatch receipt id/fingerprint
- pass1/pass2 kernel ids and fingerprints
- dtype policy id/fingerprint
- vocab size
- vocab tile size
- vocab tile count
- hidden dim
- rank
- workgroup size
- tail padding policy
- latency samples
- compile/dispatch thresholds

## Guards

- tail tile shape canonicalization required
- tail tile padding required when tail exists
- tail tile GPU dispatch required
- pass1/pass2 tail shape compatibility required
- pipeline cache key required
- compile cache reuse required after warmup
- dynamic tail shape compile forbidden
- tail CPU fallback forbidden
- tail serial dispatch forbidden
- pass2 dispatch latency threshold enforced
- tail latency penalty threshold enforced
- full logits buffer forbidden
- logits readback forbidden

## Acceptance Tests

- builds tail shape compile cache plan from 2D grid
- canonicalizes tail tile with padding
- cache key is deterministic
- warmup miss allowed but reuse required after warmup
- dynamic tail shape compile rejected
- tail CPU fallback rejected
- tail serial dispatch rejected
- pass2 dispatch latency exceeded rejected
- tail latency penalty exceeded rejected
- deterministic receipt

## Result

PASS_STATIC once tests compile and pass.
PENDING_RUNTIME until connected to real GPU pipeline cache telemetry and dispatch timing samples.
