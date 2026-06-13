# 16AI-QW-38G-R6A-EVAL-02 Report

## Status

- Static bake: PASS_STATIC
- Cargo check: NOT_RUN_CARGO_UNAVAILABLE_IN_CONTAINER
- Runtime soak: NOT_RUN

## Implemented

- `crates/model_core/src/eval02_long_horizon.rs`
- Long prompt suite with 10 Korean long-horizon cases
- Soak matrix with 6 profiles, 3 seeds, 3 backends
- Window metric structures for PCI, entropy, SALAD-02, SALAD-04, guard overlay, fallback, stop pressure
- Drift score and risk judgement structure
- `sampler_parity::append_receipt()` integration hook

## Contract

EVAL-02 is an evaluation harness only. It does not change decode behavior. It seals long horizon drift evidence by prompt/profile/backend/seed/window.
