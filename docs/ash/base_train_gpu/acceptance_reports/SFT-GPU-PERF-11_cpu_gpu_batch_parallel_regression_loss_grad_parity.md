# SFT-GPU-PERF-11 — CPU Reference vs GPU Batch-Parallel Regression / Loss+Grad Parity Seal

## Scope

This seal compares CPU reference SFT LoRA training results against GPU batch-parallel results across loss, per-token loss/logprob, pass1 max/logsumexp, grad_B, grad_lora_mid, grad_A, LoRA A/B delta, and AdamW state parity.

It requires batch size greater than one when configured and rejects CPU fallback, full logits buffers, logits readback, non-finite values, active token order mismatch, and tolerance violations.

## Required Evidence

- PERF-04 batch train plan receipt id/fingerprint
- PERF-05 pass1 receipt id/fingerprint
- PERF-06 pass2 grad receipt id/fingerprint
- PERF-07 update receipt id/fingerprint
- PERF-08 scheduler receipt id/fingerprint
- PERF-09 2D dispatch receipt id/fingerprint
- PERF-10 tail cache receipt id/fingerprint
- CPU reference result fingerprint
- GPU batch-parallel result fingerprint
- tolerance profile id/fingerprint
- active token fingerprints
- per-metric CPU/GPU values or fingerprints

## Guards

- batch size > 1 when batch regression is required
- active token order must match
- CPU/GPU values must be finite
- mean loss parity required
- per-token loss/logprob parity required
- pass1 max/logsumexp parity required
- grad_B parity required
- grad_lora_mid parity required
- grad_A parity required
- A/B delta parity required
- AdamW state parity required
- CPU fallback forbidden
- full logits buffer forbidden
- logits readback forbidden
- step 2+ zero A-delta rejected when configured

## Acceptance Tests

- CPU/GPU parity passes for matching batch result
- batch size one rejected when required
- active token order mismatch rejected
- mean loss mismatch rejected
- pass1 logsumexp mismatch rejected
- grad_B mismatch rejected
- grad_A mismatch rejected
- A/B delta mismatch rejected
- CPU fallback/logits readback rejected
- deterministic regression receipt

## Result

PASS_STATIC once tests compile and pass.
PENDING_RUNTIME until exercised with real CPU reference and GPU batch-parallel training outputs.
