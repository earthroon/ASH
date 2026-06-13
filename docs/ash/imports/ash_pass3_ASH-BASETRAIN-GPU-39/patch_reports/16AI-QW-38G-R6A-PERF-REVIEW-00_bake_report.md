# 16AI-QW-38G-R6A-PERF-REVIEW-00 Bake Report

## Status

`PASS_STATIC_PERFORMANCE_REVIEW_BASELINE`

## Generated

- model/tokenizer/runtime/sampler/checkpoint reports
- 100-case EN-KO subtitle baseline fixture
- static performance review document
- bottleneck classification
- static validation receipt

## Not Executed

- cargo/rust runtime
- model forward
- WebGPU benchmark
- actual EN-KO generation
- translation quality scoring

## Critical Finding

Ash 1.1B lineage is confirmed by specs, but `48256` is not confirmed as a runtime vocab cap in static archive evidence; `48259` is the strongly confirmed v5 model/tokenizer/checkpoint vocab line.
