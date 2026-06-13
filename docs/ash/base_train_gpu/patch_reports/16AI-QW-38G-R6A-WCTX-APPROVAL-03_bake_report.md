# WCTX-APPROVAL-03 Bake Report

## Contract

`Candidate Commit Receipt Bind / No Runtime Apply Seal`

## Baked files

```txt
crates/ash_core/src/word_context_approval_03_candidate_commit_receipt_bind.rs
crates/ash_core/src/bin/ash_word_context_approval_03_candidate_commit_receipt_bind.rs
crates/ash_core/src/lib.rs
acceptance_reports/16AI-QW-38G-R6A-WCTX-APPROVAL-03.md
patch_reports/16AI-QW-38G-R6A-WCTX-APPROVAL-03_bake_report.md
WCTX_APPROVAL_03_STATIC_CHECKS.txt
WCTX_APPROVAL_03_BAKE_MANIFEST.json
```

## Boundary

Opened:

```txt
candidate_commit_executed = true
candidate_commit_receipt_created = true
commit_receipt_bound_as_candidate_commit = true
```

Closed:

```txt
runtime_apply_executed = false
runtime_apply_gate_created = false
runtime_apply_receipt_created = false
runtime_token_append_executed = false
runtime_sequence_mutated = false
runtime_output_created = false
```

## Build status

`BAKED_STATIC_NO_CARGO`

`cargo` and `rustc` were not available in the baking container, so this bake includes static file checks only.
