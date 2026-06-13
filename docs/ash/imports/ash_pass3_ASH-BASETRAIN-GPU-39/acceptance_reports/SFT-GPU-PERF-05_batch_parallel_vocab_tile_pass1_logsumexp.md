# SFT-GPU-PERF-05 — Batch-Parallel Vocab Tile Pass1 LogSumExp / No Per-Sample Serial Loop Seal

## Scope

This seal consumes the PERF-04 BatchAxisTrainPlan and constructs a batch-parallel GPU pass1 plan for LM head vocab tile logsumexp. It verifies that active_token and vocab_tile axes are both represented in dispatch records, that per-token max/logsumexp buffers are produced without full logits buffers or logits readback, and that no per-sample serial loop is used.

## Required Evidence

- PERF-04 batch train plan id
- PERF-04 batch train plan fingerprint
- active token count
- microbatch plan
- hidden buffer id
- LM head weight buffer id
- vocab size
- vocab tile size
- parallel tile groups
- pass1 kernel id/fingerprint
- dispatch records
- token result descriptors

## Guards

- batch-parallel dispatch verified
- active token axis required
- vocab tile axis required
- GPU-side reduction required
- all active tokens covered
- all vocab tiles covered
- tail tile GPU dispatched
- max logit buffer created
- logsumexp buffer created
- per-sample serial loop forbidden
- per-token serial dispatch forbidden
- full logits buffer forbidden
- logits readback forbidden
- CPU fallback forbidden

## Acceptance Tests

- builds batch-parallel pass1 plan from PERF-04 train plan
- dispatch covers all active tokens
- dispatch covers all vocab tiles
- tail tile is GPU dispatched
- per-sample serial loop rejected
- per-token serial dispatch rejected
- full logits buffer rejected
- logits readback rejected
- missing active token axis rejected
- deterministic pass1 receipt

## Result

PASS_STATIC once tests compile and pass.
PENDING_RUNTIME until connected to the real GPU pass1 logsumexp kernel and consumed by PERF-06 batch-parallel pass2 gradient accumulation.
