# SFT-GPU-PERF-12 — Real Batch-Parallel Multi-Step Train Run / No Serial Batch Fallback Seal

## Scope

This seal verifies that the GPU batch-parallel SFT LoRA path runs real multi-step training with batch size greater than one, finite loss/grad/delta values, PERF-04 through PERF-10 step receipts, PERF-11 parity receipt, and final adapter artifact output.

It rejects serial batch fallback, per-sample serial loops, per-token serial dispatch, CPU fallback, full logits buffers, logits readback, synthetic deltas, loss clamps, non-finite states, missing post-warm-step A deltas, and missing artifacts.

## Required Evidence

- train config id/fingerprint
- dataset slice id/fingerprint
- tokenizer fingerprint
- base model fingerprint
- effective batch size
- completed train steps
- PERF-11 parity receipt
- per-step PERF-04 through PERF-10 receipt chain
- per-step warm-step gate receipt
- per-step loss/grad/delta metrics
- final adapter artifact receipt

## Guards

- batch size greater than one required
- multi-step train required
- PERF-11 parity receipt required
- every step must have PERF-04 through PERF-10 receipts
- first step B-zero-init warm gate respected
- step 2+ requires nonzero A delta
- B delta must be nonzero
- all losses finite
- all gradients finite
- all deltas finite
- serial batch fallback forbidden
- per-sample serial loop forbidden
- per-token serial dispatch forbidden
- CPU fallback forbidden
- full logits buffer forbidden
- logits readback forbidden
- synthetic delta forbidden
- loss clamp forbidden
- final artifact required

## Acceptance Tests

- real batch-parallel multi-step train run passes
- batch size one rejected
- missing or failed parity receipt rejected
- missing PERF-04 through PERF-10 step receipt chain rejected
- serial batch fallback rejected
- CPU fallback rejected
- non-finite loss rejected
- step 2 zero A delta rejected
- missing artifact rejected
- deterministic train run receipt

## Result

PASS_STATIC once tests compile and pass.
PENDING_RUNTIME until exercised with an actual GPU batch-parallel training command.
