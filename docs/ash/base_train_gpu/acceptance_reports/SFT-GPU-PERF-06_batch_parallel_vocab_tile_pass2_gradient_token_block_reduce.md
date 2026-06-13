# SFT-GPU-PERF-06 — Batch-Parallel Vocab Tile Pass2 Gradient Accumulation / Token-Block Reduce Seal

## Scope

This seal consumes PERF-04 BatchAxisTrainPlan and PERF-05 BatchParallelPass1 outputs, then constructs a batch-parallel GPU pass2 gradient accumulation plan. It verifies active_token x vocab_tile dispatch, GPU-side token-block reduce, target subtraction, mean loss normalization, grad_B tile shards, grad_lora_mid token blocks, and grad_A partial shards without CPU gradient accumulation, full logits buffers, logits readback, or CPU fallback.

## Required Evidence

- PERF-04 batch train plan id/fingerprint
- PERF-05 pass1 plan id/fingerprint
- PERF-05 pass1 receipt id/fingerprint
- active token count
- microbatch plan
- max logit buffer id
- logsumexp buffer id
- hidden buffer id
- LoRA A/B buffer ids
- vocab size
- vocab tile size
- parallel tile groups
- pass2 kernel id/fingerprint
- target subtraction flag
- mean loss normalization flag
- dispatch records
- grad shard descriptors
- token block reduce descriptors

## Guards

- pass1 receipt must be ready
- batch-parallel dispatch verified
- active token axis required
- vocab tile axis required
- GPU-side token-block reduce required
- all active tokens covered
- all vocab tiles covered
- tail tile GPU dispatched
- target subtraction required
- mean loss normalization required
- grad_B shard required
- grad_lora_mid shard required
- grad_A partial shard required
- CPU gradient accumulation forbidden
- per-sample serial loop forbidden
- per-token serial dispatch forbidden
- full logits buffer forbidden
- logits readback forbidden
- CPU fallback forbidden

## Acceptance Tests

- builds pass2 grad plan from PERF-05 pass1
- dispatch covers all active tokens
- dispatch covers all vocab tiles
- creates grad_B / grad_lora_mid / grad_A partial shards
- pass1 receipt mismatch rejected
- missing target subtraction rejected
- missing mean loss normalization rejected
- CPU grad accumulation rejected
- full logits/readback rejected
- deterministic pass2 receipt

## Result

PASS_STATIC once tests compile and pass.
PENDING_RUNTIME until connected to the real GPU pass2 gradient kernel and consumed by PERF-07 batch-reduced LoRA A/B update.
