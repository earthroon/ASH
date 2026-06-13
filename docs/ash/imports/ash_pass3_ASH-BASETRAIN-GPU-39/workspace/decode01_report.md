# 16AI-QW-38G-R6A-DECODE-01 Report

## Scope
CPU Oracle Sampler / Greedy Fallback Elimination Seal.

## Implemented
- Added `crates/model_core/src/cpu_oracle_sampler.rs`.
- Added `SamplingApplyMode`, `CpuOracleContext`, `CpuOracleSampleResult`.
- Added deterministic CPU oracle sampling for `temperature`, `top_k`, `min_p`, active-set softmax renormalization, `top_p`, and seeded sampling.
- Replaced sampled decode greedy fallback in `NativeWgpuModel::select_next_token_with_sampling` with CPU oracle fallback.
- Routed `ReferenceCheckpoint::greedy_generate_streaming` through CPU oracle when `GenerationSamplingConfig::requests_sampled_decode()` is true.
- Extended DECODE-00 `DecodeStepProbe` with CPU oracle / candidate count fields.

## Non-scope
- WebGPU shader active-set renormalization.
- ΔK/QWave weighted Min-P.
- Context router training.

## Validation
Static validation only. `cargo`, `rustc`, and `rustfmt` are unavailable in this container.
