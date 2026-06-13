# 16AI-QW-38G-R6A-MINP-C1A — Weighted Min-P Build / WGSL Compile Smoke Receipt Bake Report

## Scope

This patch does not add a new QWave/DeltaK score provider. It adds smoke fixtures and receipts for the MINP-C1 weighted Min-P path.

## Code changes

- Added `crates/model_core/src/minp_c1a_smoke.rs`.
- Exported `MinpC1aFixtureReceipt` and `run_minp_c1a_cpu_smoke_fixtures()` from `model_core`.
- Added static receipts for Rust build smoke, WGSL compile smoke, binding layout, zero-source fallback, weighted fixture formula, and strict readiness guard.

## Executed checks in this container

- Static file checks: PASS
- cargo check: NOT_RUN
- cargo test: NOT_RUN
- rustfmt: NOT_RUN
- WGSL runtime compile: NOT_RUN

`NOT_RUN` is intentionally not treated as PASS. The container does not expose cargo/rustc/rustfmt or a WebGPU/WGSL validator, so execution is still judgment-unavailable until run in the target Rust/WebGPU environment.

## Smoke contracts baked

- Zero-source fallback: semantic prior enabled without qwave/deltak score buffers must remain equivalent to vanilla scaled-logit sampling.
- Weighted fixture: `0.2*0.8 + 0.15*0.5 + 0.1*0.8*0.5 = 0.275`.
- Prior rescue: a near-threshold candidate may survive only through bounded semantic bias.
- Banned token cannot resurrect: ban/eos guard precedes semantic prior.
- Strict readiness unknown/blocked disables semantic prior effectiveness.

## Next gate

Run in the target environment:

```bash
cargo check
cargo test -p model_core minp_c1a
# plus the project-specific WebGPU/WGSL shader validation path
```
