# 16AI-QW-38G-R6A-WCTX-14 Bake Report

## Seal
`EN-KO Subtitle Decode Candidate Human Review Approval / No-Target-Commit Seal`

## Domain SSOT
`en_to_ko_translation_subtitle_machine`

## Implemented
- Added human review approval decision model.
- Added human review checklist model.
- Added decode candidate approval receipt.
- Added target update candidate gate.
- Added no-target-commit risk model.
- Added default approval builder:
  - candidate unavailable -> `NoCandidate`
  - candidate available -> `Pending`
- Added matrix runner.
- Added CLI runner.
- Added static receipt artifacts.

## Guarded invariants
- No auto approval.
- No candidate missing approval.
- No target subtitle commit.
- No target text mutation.
- No runtime default apply.
- No rerank apply.
- No decode/generation/model_forward/sampling during approval.

## Static result
- `total_cases=24`
- `pass_cases=24`
- `no_candidate_count=24`
- `target_update_candidate_gate_open_count=0`
- `target_commit_gate_open_count=0`
- `runtime_default_apply_count=0`

## Verification limitation
Rust toolchain unavailable in container. Static Rust files and JSON receipts were generated; local cargo verification remains required.
