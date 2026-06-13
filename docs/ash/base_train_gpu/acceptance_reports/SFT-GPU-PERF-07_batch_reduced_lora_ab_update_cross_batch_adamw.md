# SFT-GPU-PERF-07 — Batch-Reduced LoRA A/B Update / Cross-Batch AdamW Seal

## Scope

This seal consumes PERF-06 batch-parallel pass2 gradient shards and performs a batch-reduced LoRA A/B AdamW update receipt. It verifies cross-batch reduce, AdamW state shard updates, finite A/B gradients, finite A/B deltas, B-zero-init warm-step behavior, and post-warm-step A delta requirements without CPU reduce, CPU AdamW update, synthetic deltas, delta clamps, full logits buffers, or logits readback.

## Required Evidence

- PERF-06 pass2 plan id/fingerprint
- PERF-06 pass2 receipt id/fingerprint
- grad_B shard ids/fingerprints
- grad_lora_mid shard ids/fingerprints
- grad_A partial shard ids/fingerprints
- LoRA A/B buffer ids
- AdamW A/B state shard ids/fingerprints
- optimizer hyperparameters
- real step index
- B-zero-init detection source
- previous B delta norm when applicable

## Guards

- pass2 receipt must be ready
- grad_B shards required
- grad_lora_mid shards required
- grad_A partial shards required
- cross-batch reduce required
- AdamW state update required
- B delta nonzero required
- first step B-zero-init may allow zero A delta only if B delta is nonzero
- step 2+ requires grad_lora_mid nonzero
- step 2+ requires A delta nonzero
- CPU reduce forbidden
- CPU AdamW update forbidden
- synthetic delta forbidden
- delta clamp forbidden
- full logits buffer forbidden
- logits readback forbidden

## Acceptance Tests

- builds batch-reduced A/B update from PERF-06 shards
- first step zero A delta allowed with B-zero-init and B delta nonzero
- first step rejects missing B delta
- step 2 requires A delta and passes
- step 2 rejects zero A delta
- missing AdamW state shard rejected
- CPU AdamW update rejected
- synthetic delta rejected
- delta clamp rejected
- deterministic update receipt

## Result

PASS_STATIC once tests compile and pass.
PENDING_RUNTIME until connected to real GPU batch-reduced AdamW update and real multi-step train runs.
