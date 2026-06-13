# 16AI-QW-38G-R6A-EVAL-00 Report

## Scope

Fixed Prompt Suite / Decode Regression Bench Seal baked on top of SALAD-04.

## Files

- `crates/model_core/src/eval00_regression.rs`
- `crates/model_core/src/lib.rs`
- `crates/model_core/src/sampler_parity.rs`
- `workspace/eval00_prompt_suite.jsonl`
- `workspace/eval00_matrix.json`
- `workspace/eval00_metric_schema.json`
- `workspace/eval00_runs.jsonl`
- `workspace/eval00_summary.json`
- `workspace/eval00_static_checks.json`

## SSOT

`fixed_prompt_suite + seed_config_backend_matrix + generated_output_receipt` is the regression SSOT. Single sample impressions are not accepted as promotion evidence.

## Runtime Status

Static bake only. Cargo and runtime smoke were not run in this container because `cargo` is unavailable.
