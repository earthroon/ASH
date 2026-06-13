# 16AI-QW-38G-R6A-EVAL-03 Candidate Calibration Regression Replay Seal

## SSOT
DECODE-03F calibration candidate + EVAL-00/01/02 replay matrix.

## Contract
- candidate replay only
- no runtime promotion
- no base config mutation
- default guard overlay promotion forbidden
- failed runs must remain in summary

## Implemented files
- `crates/model_core/src/eval03_candidate_replay.rs`
- `workspace/eval03_candidate_matrix.json`
- `workspace/eval03_candidate_runs.jsonl`
- `workspace/eval03_backend_diffs.jsonl`
- `workspace/eval03_summary.json`
- `workspace/eval03_metric_schema.json`

## Status
Static bake completed. Runtime replay, cargo check, backend parity execution are not run in this container.
