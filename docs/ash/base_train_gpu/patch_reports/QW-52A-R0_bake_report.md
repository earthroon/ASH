# QW-52A-R0 Bake Report

## Patch
- `QW-52A-R0`
- `Cheonjiin Structural Probe Library Lift / No Logic Rewrite Seal`

## Base
- `QW-52A`

## Summary
Existing `af16ai6b_cheonjiin_structural_probe.rs` structural probe logic was lifted into a reusable Rust library module without adding new Cheonjiin/QWave math.

## Rust-owned changes
- Added `crates/model_core/src/cheonjiin_structural_probe/mod.rs`
- Rewrote `crates/model_core/src/bin/af16ai6b_cheonjiin_structural_probe.rs` as a thin Rust wrapper that calls the library CLI runner
- Exported structural probe API through `crates/model_core/src/lib.rs`
- Added Rust validator binary: `crates/model_core/src/bin/qw52a_r0_cheonjiin_probe_lift_validate.rs`
- Extended QW-52A implementation audit with library lift evidence

## Exported API
- `run_cheonjiin_structural_probe_cli()`
- `run_cheonjiin_structural_probe(...)`
- `analyze_candidate_surface(...)`
- `summarize_candidate_surface(...)`
- `CheonjiinSignature`
- `HangulSyllableNode`
- `BoundaryCandidate`
- `CheonjiinStructuralProbeResult`
- `CheonjiinStructuralSummary`

## Mutation policy
- Decode policy mutation: false
- Guard policy mutation: false
- LoRA scale mutation: false
- Model weight mutation: false
- Token ban added: false
- Logit mutation: false
- Sampler mutation: false
- WebGPU shader added: false
- Python trace/receipt mutation: false

## Validation
- Static validation: PASS
- Zip integrity: PASS
- Cargo check: NOT RUN - cargo unavailable in bake environment
- Runtime parity replay: NOT RUN - cargo unavailable in bake environment

## Next
- `QW-52A-R1 — Existing Cheonjiin Jaso Stroke Tensor Facade / No Math Rewrite Seal`
