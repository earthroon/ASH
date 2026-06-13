# 16AI-QW-38G-R6A-DECODE-00 Acceptance

## Static acceptance

| Check | Result |
|---|---|
| decode SSOT module exists | PASS |
| tokenizer_core exports decode_ssot | PASS |
| NativeTokenizer::decode uses decode_ssot | PASS |
| runtime final output uses decode_ssot | PASS |
| model_core streaming output uses decode_ssot | PASS |
| DecodeStepProbe exists | PASS |
| TopTokenProbe exists | PASS |
| sampler_requested / sampler_applied separated in schema | PASS |
| fallback_applied / fallback_reason fields exist | PASS |
| summary/report/schema/probe artifacts created | PASS |

## Execution acceptance

`cargo`, `rustc`, and `rustfmt` were not available in the container, so compile-time and runtime execution acceptance is marked **NOT_RUN** rather than PASS.

## Scope note

This patch seals decode SSOT and probe schema. It does not claim to fix CPU greedy fallback, WebGPU top-p/min-p renormalization, or ΔK/QWave weighted sampling.
