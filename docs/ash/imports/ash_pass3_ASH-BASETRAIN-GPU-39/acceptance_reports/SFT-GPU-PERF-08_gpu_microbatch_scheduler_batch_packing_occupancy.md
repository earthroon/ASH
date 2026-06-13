# SFT-GPU-PERF-08 — GPU Microbatch Scheduler / Batch Packing & Occupancy Seal

## Scope

This seal builds a GPU-only microbatch packing plan for batch-parallel SFT LoRA training. It uses active token count, batch coordinates, vocab tile count, VRAM budget hints, dispatch estimates, and occupancy policy to create a deterministic microbatch schedule without CPU fallback, full logits buffers, logits readback, batch-axis loss, or active token reordering.

## Required Evidence

- PERF-04 batch train plan id/fingerprint
- active token matrix
- batch size
- active token count
- hidden dim
- rank
- vocab size
- vocab tile size
- parallel tile groups
- VRAM budget hint
- dispatch budget
- occupancy policy
- microbatch policy

## Guards

- active token matrix required
- original batch indices preserved
- sequence positions preserved
- active token order preserved
- VRAM budget respected or shrink retry required
- dispatch budget respected
- GPU-only path required
- CPU fallback forbidden
- full logits buffer forbidden
- logits readback forbidden
- OOM retry may only shrink GPU microbatch size

## Acceptance Tests

- builds microbatch packing plan
- splits by max active tokens per microbatch
- active token reorder rejected
- lost original batch index / sequence position rejected
- estimates VRAM under budget
- requests shrink retry when over budget
- over budget rejected when retry disabled
- CPU fallback rejected
- dispatch budget exceeded rejected
- deterministic scheduler receipt

## Result

PASS_STATIC once tests compile and pass.
PENDING_RUNTIME until connected to real GPU allocator telemetry and PERF-09 batch × vocab 2D dispatch grid.
