# DECODE-03A Bake Report

`16AI-QW-38G-R6A-DECODE-03A` adds an observe-only entropy/confidence receipt layer on top of the SAMPLER-05 parity lane.

## What changed

- CPU oracle candidate trace now records:
  - active/final entropy
  - active/final normalized entropy
  - active/final top1/top2 id, score, probability
- sampler parity runtime trace now carries entropy/confidence seed fields.
- DECODE-03A receipt generation is attached to `sampler_parity::append_receipt()`.
- The receipt writer is off by default and enabled through `ASH_DECODE03A_ENTROPY=receipt`.
- Summary aggregation is included through `write_decode03a_summary_from_receipt_file()`.

## What did not change

- No sampler behavior change.
- No dynamic temperature/min-p enable.
- No rollback or word-salad intervention.
- GPU entropy is optional and not required for this seal.

## Runtime gate

Status remains `STATIC_BAKE_DEFINED_NOT_RUN` until the target machine runs sampler parity + DECODE-03A receipt capture.
