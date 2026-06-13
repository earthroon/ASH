# WCTX-APPROVAL-02 Bake Report

## Contract

`Approved Candidate Commit Candidate / No Runtime Apply Seal`

## Baked files

```txt
crates/ash_core/src/word_context_approval_02_approved_candidate_commit_candidate.rs
crates/ash_core/src/bin/ash_word_context_approval_02_approved_candidate_commit_candidate.rs
crates/ash_core/src/lib.rs
acceptance_reports/16AI-QW-38G-R6A-WCTX-APPROVAL-02.md
patch_reports/16AI-QW-38G-R6A-WCTX-APPROVAL-02_bake_report.md
WCTX_APPROVAL_02_STATIC_CHECKS.txt
WCTX_APPROVAL_02_BAKE_MANIFEST.json
```

## Boundary

Opened:

```txt
approved_commit_candidate_created = true
approved_candidate_bound_as_commit_candidate = true
```

Closed:

```txt
candidate_commit_executed = false
commit_receipt_created = false
runtime_apply_executed = false
runtime_token_append_executed = false
runtime_sequence_mutated = false
runtime_output_created = false
```

## Build status

`BAKED_STATIC_NO_CARGO`

`cargo` and `rustc` were not available in the baking container, so this bake includes static file checks only.
