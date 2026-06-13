# SFT-GPU-PERF-09 — Batch × Vocab Tile 2D Dispatch Grid / Kernel Occupancy Seal

## Scope

This seal consumes the PERF-08 GPU microbatch scheduler output and constructs a 2D dispatch grid over batch active-token blocks and vocab tile groups. It verifies pass1/pass2 grid compatibility, active token coverage, vocab tile coverage, tail tile GPU dispatch, kernel occupancy estimates, and dispatch budget without CPU fallback, serial token dispatch, full logits buffers, or logits readback.

## Required Evidence

- PERF-08 microbatch packing plan id/fingerprint
- PERF-08 scheduler receipt id/fingerprint
- PERF-05 pass1 plan id/fingerprint
- PERF-06 pass2 plan id/fingerprint
- active token count
- microbatch count
- vocab tile count
- active tokens per block
- vocab tiles per group
- workgroup size
- microbatch dispatch estimates
- 2D dispatch records
- occupancy estimates

## Guards

- 2D dispatch grid required
- batch active-token axis required
- vocab tile axis required
- pass1/pass2 grid compatibility required
- all active tokens covered
- all vocab tiles covered
- tail tile GPU dispatched
- occupancy target checked
- dispatch budget respected
- per-sample serial loop forbidden
- per-token serial dispatch forbidden
- CPU fallback forbidden
- full logits buffer forbidden
- logits readback forbidden

## Acceptance Tests

- builds 2D dispatch grid from PERF-08 scheduler
- dispatch covers all active tokens
- dispatch covers all vocab tiles
- pass1/pass2 grid compatible
- tail tile GPU dispatched
- missing batch token axis rejected
- missing vocab tile axis rejected
- dispatch budget exceeded rejected
- CPU fallback or serial dispatch rejected
- deterministic 2D dispatch receipt

## Result

PASS_STATIC once tests compile and pass.
PENDING_RUNTIME until connected to real GPU dispatch telemetry and PERF-10 tail tile compile cache.
