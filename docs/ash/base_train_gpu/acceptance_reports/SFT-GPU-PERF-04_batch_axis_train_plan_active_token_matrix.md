# SFT-GPU-PERF-04 — Batch Axis Train Plan / Active Token Matrix Seal

## Scope

This seal builds a deterministic batch-axis train plan and active token matrix for GPU SFT LoRA training. It preserves batch index, sequence position, target token id, hidden row mapping, response-only loss mask, and vocab tile mapping so later GPU pass1/pass2 kernels can process batch/sample/token dimensions without CPU per-token serial loops.

## Required Evidence

- run id
- step index
- batch size
- max sequence length
- hidden dim
- vocab size
- vocab tile size
- input ids
- target ids
- response loss mask
- attention mask
- hidden row base offsets
- microbatch policy

## Guards

- response-only loss verified
- prompt loss tokens rejected
- active token matrix required
- batch axis preserved
- sequence positions preserved
- target token ids validated
- hidden row offsets validated
- vocab tile mapping validated
- microbatch split preserves original batch indices
- CPU per-token serial loop forbidden
- full logits buffer forbidden
- logits readback forbidden

## Acceptance Tests

- builds active token matrix from response mask
- rejects prompt loss token
- rejects missing target token id
- rejects target token out of vocab
- computes hidden row offsets
- computes target vocab tile mapping
- splits microbatches preserving original batch indices
- rejects CPU per-token serial loop flag
- rejects full logits/readback flags
- deterministic plan fingerprint

## Result

PASS_STATIC once static file/export/guard checks are present.
PENDING_RUNTIME until consumed by PERF-05 batch-parallel pass1 and PERF-06 batch-parallel pass2 kernels.
