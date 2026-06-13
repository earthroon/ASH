# 16AI-QW-38G-R6A-DECODE-05 Bake Report

## Result

status: PASS_STATIC_STEP_INTEGRITY_CONTRACT

## Applied Changes

1. Added `DecodeStepContext` and `DecodeStepSource` as the generation-step context contract.
2. Added `DecodeStepIntegritySnapshot` and mismatch reasons, including `PlaceholderZeroAfterFirstToken`.
3. Added `DecodeStepIntegrityReceipt` and deterministic Q4 key material.
4. Added aligned and negative placeholder-zero fixtures.
5. Extended DECODE-04 `TokenTraceQualitySnapshot` with step range and `step_integrity_hash` slots.
6. Added acceptance and patch reports.

## No Runtime Behavior Change

- runtime_decode_executed_count: 0
- model_forward_executed_count: 0
- sampling_executed_count: 0
- guard_executed_count: 0

## Compile Status

`cargo` / `rustc` were not available in this environment, so this bake is sealed as a static source/receipt contract rather than a compiled Rust proof.
