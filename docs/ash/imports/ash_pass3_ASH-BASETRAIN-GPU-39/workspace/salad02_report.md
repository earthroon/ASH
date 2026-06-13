# 16AI-QW-38G-R6A-SALAD-02 Bake Report

## Scope
- Added `crates/model_core/src/salad02_detector.rs`.
- Registered SALAD-02 module and exports in `crates/model_core/src/lib.rs`.
- Hooked `append_salad02_receipt_from_sampler03()` after DECODE-03D in `sampler_parity::append_receipt()`.
- Added detector schema, empty JSONL receipt, static summary, probe prompts, patch diff, and acceptance report.

## Contract
- `behavior_change=false`
- `detector_only=true`
- `action_executed=false`
- rollback/safe-stop/EOS are candidates only, not executed in SALAD-02.

## Status
- Static bake: `PASS_STATIC`
- Cargo check: `NOT_RUN_CARGO_UNAVAILABLE_IN_CONTAINER`
- Runtime smoke: `NOT_RUN`

## Next
- Run with `ASH_SALAD02_DETECTOR=receipt` after DECODE-03D controlled evidence.
- If receipt is PASS/PASS_WITH_WARNINGS, proceed to `16AI-QW-38G-R6A-SALAD-03 Rollback Candidate / Safe Resample Seal`.
